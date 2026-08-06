---
name: fly-deploy
description: Deploy CareerReality.in on Fly.io (Django gunicorn) instead of Vercel. Use when deploying, migrating off Vercel, configuring fly.toml, Docker, or production crons.
paths:
  - "Dockerfile"
  - "fly.toml"
  - "docker-compose.yml"
  - "deploy/**"
  - "docs/migrate-off-vercel.md"
  - "vercel.json"
---

# Fly.io deploy (post-Vercel)

## Canonical docs

Follow `docs/migrate-off-vercel.md`.

## Quick commands

```bash
fly deploy -a career-reality
fly scale count web=1 cron=1 -a career-reality
fly logs -a career-reality
fly secrets list -a career-reality
```

## Process model

- `web` → `deploy/entrypoint.sh web` → gunicorn
- `cron` → `deploy/entrypoint.sh cron` → `deploy/cron-runner.sh` (replaces `vercel.json` crons)

## Do not

- Rely on Vercel serverless `api/index.py` for production after DNS cutover
- Leave `REDIS_URL` empty in production
- Use Supabase transaction pooler with high `DB_CONN_MAX_AGE` (set `0`)
