# Migrate CareerReality.in off Vercel → Fly.io

## Why leave Vercel

This app is **Django + Gunicorn**, not a Next.js frontend.

| | Vercel Python serverless | Fly.io Machines (chosen) |
|--|--|--|
| Cold start | Common; multi-second TTFB | Always-on; warm process |
| Pricing | Per-invocation + bandwidth surprises | Flat small VM (~$5–10/mo web+cron) |
| Region | Typically US/edge mismatch for India | **`bom` (Mumbai)** next to readers |
| Crons | `vercel.json` HTTP crons | In-process `deploy/cron-runner.sh` |
| Fit | Fighting the platform | Native long-running WSGI |

Supabase Postgres can stay. Redis should move off Vercel KV to Upstash/Redis Cloud/Fly Redis.

## Target architecture

```
DNS (careerreality.in / www)
        │
        ▼
Fly HTTP proxy (bom) ──► web process: gunicorn config.wsgi
                     └──► cron process: deploy/cron-runner.sh
        │
        ├── Supabase Postgres (DATABASE_URL)
        └── Redis (REDIS_URL)
```

Optional later: Cloudflare in front for CDN/WAF (honor existing `Cache-Control` from `EdgeCacheHeadersMiddleware`).

## Files added

- `Dockerfile` — Python 3.12 + gunicorn
- `fly.toml` — `bom`, web + cron processes, health checks
- `docker-compose.yml` — local prod-like web+redis(+cron)
- `deploy/entrypoint.sh` — migrate / collectstatic / role switch
- `deploy/cron-runner.sh` — replaces `vercel.json` schedules
- `deploy/trigger-cron.sh` — optional HTTP cron via `CRON_SECRET`

`vercel.json` is kept temporarily as **rollback reference** only. Do not rely on it after DNS cutover.

## Cutover checklist

### 1. Create Fly app

```bash
fly auth login
fly apps create career-reality
fly regions set bom -a career-reality
```

### 2. Secrets (copy from Vercel project `ainews`)

```bash
fly secrets set -a career-reality \
  DEBUG=False \
  SECRET_KEY=... \
  DATABASE_URL=... \
  REDIS_URL=... \
  CRON_SECRET=... \
  RAZORPAY_KEY_ID=... \
  RAZORPAY_KEY_SECRET=... \
  RAZORPAY_WEBHOOK_SECRET=... \
  RESEND_API_KEY=... \
  OPENAI_API_KEY=... \
  GOOGLE_CLIENT_ID=... \
  GOOGLE_CLIENT_SECRET=... \
  GA_MEASUREMENT_ID=... \
  CANONICAL_BASE_URL=https://www.careerreality.in \
  ALLOWED_HOSTS=careerreality.in,www.careerreality.in,career-reality.fly.dev \
  CSRF_TRUSTED_ORIGINS=https://careerreality.in,https://www.careerreality.in,https://career-reality.fly.dev \
  DB_CONN_MAX_AGE=0
```

Use `DB_CONN_MAX_AGE=0` with Supabase **transaction** pooler (`:6543`). Session mode / direct can use `60`.

### 3. Deploy

```bash
fly deploy -a career-reality
fly status
curl -I https://career-reality.fly.dev/robots.txt
python manage.py preflight_release --strict   # against Fly env / staging
```

Scale processes:

```bash
fly scale count web=1 cron=1 -a career-reality
```

### 4. DNS

1. Add Fly IPs: `fly ips list -a career-reality`
2. Point `www` + apex to Fly (A/AAAA or CNAME per Fly docs)
3. Keep Vercel DNS briefly with a lower TTL for rollback (300s)
4. After Google/crawl looks healthy, remove Vercel domain binding

### 5. Post-cutover

- [ ] `preflight_release --strict --check-freshness` on production
- [ ] Spot-check article + AI hub + salary tools
- [ ] Confirm cron logs: `fly logs -a career-reality -i <cron-machine>`
- [ ] Update AdSense / OAuth redirect URIs if they listed `*.vercel.app`
- [ ] Disable Vercel production deploys / delete project when stable
- [ ] Delete or archive `vercel.json` in a follow-up PR

## Cheaper alternatives (if not Fly)

| Host | When to pick |
|------|----------------|
| **Railway** | Fastest UX; weaker India latency |
| **Render** | Simple web+cron; Singapore region |
| **Hetzner CX22 + Coolify** | Lowest $/perf; more ops |
| **DigitalOcean Bangalore** | India region without Fly |

Compose + gunicorn files here work on all of the above with minor env tweaks.

## Rollback

1. Repoint DNS to Vercel
2. Re-enable Vercel production
3. Keep Supabase as source of truth either way
