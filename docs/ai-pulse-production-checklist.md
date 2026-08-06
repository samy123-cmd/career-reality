# AI Pulse Production Checklist

## 1. Environment Requirements

Set these environment values in production:

- `DEBUG=False`
- `ALLOWED_HOSTS=<comma-separated-hosts>` (or configured equivalent in settings logic)
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_HSTS_SECONDS=31536000` (after confirming HTTPS-only delivery)
- `DATABASE_URL` or `POSTGRES_URL` configured
- `SECRET_KEY` set to a production secret

Optional but recommended:

- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- `SECURE_HSTS_PRELOAD=True`

## 2. Release Preflight

Run:

```bash
python manage.py preflight_release --strict
```

One-command pre-prod bundle (recommended):

```powershell
./scripts/preprod_release_bundle.ps1 -ProductionLike
```

Optional full run including tests:

```powershell
./scripts/preprod_release_bundle.ps1 -ProductionLike -RunTests
```

This command fails if blocking settings are unsafe for production.

Phase-2 recommendation:

```bash
python manage.py preflight_release --strict --check-freshness
```

This additionally enforces stale-content thresholds for published core and AI pages.

## 3. Database and Assets

Run in order:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 4. Content/Editorial Checks

- Apply deterministic content hardening fixes (if needed):

```bash
python manage.py apply_release_content_fixes
```

- Confirm AI items have:
  - `status=published`
  - `fact_check_status=verified` for pieces ready for public promotion
  - `event_date` populated (actual event date)
  - `reviewed_at` populated (latest editorial update date)
- Spot-check at least 3 random items for source links and timeline consistency.

## 5. Feed Ingestion Health

Run a smoke fetch:

```bash
python manage.py fetch_ai_news --limit 1
```

Then verify latest `AINewsFetchRun` in admin:

- `status` should be `success` or acceptable `partial`
- warnings/errors are understood and tracked

Run source verification/update for published AI items:

```bash
python manage.py verify_ai_news_sources --commit --set-verified
```

This updates `reviewed_at`, `last_verified_at`, and (when enabled) promotes `fact_check_status` to `verified` for reachable source URLs.

## 6. Post-Deploy Smoke Tests

- `/ai/` renders and paginates
- `/ai/<slug>/` renders timeline + visual sections
- `/ai/tag/<slug>/` filtering works
- `/sitemap.xml` includes `/ai/` URLs
- Home header links include `AI Pulse`
- `/healthz` returns `200` with `{"status":"ok"}`
- response headers include `X-Request-ID` and `X-Response-Time-ms`

## 7. Continuous Integration

- GitHub Actions workflow: `.github/workflows/ci.yml`
- Runs on push/PR:
  - `python manage.py check`
  - `python manage.py test core content ainews`
  - `python manage.py preflight_release --strict --check-freshness`
  - `python manage.py quality_audit --strict --max-low-word 0 --max-low-internal 0 --max-stale-check 0 --max-stale-update 0 --max-short-meta 0 --max-weak-authors 0`

## 8. Scheduled Maintenance (Phase 3)

- Configure one of these env vars in production:
  - `CRON_SECRET` (preferred)
  - `FRESHNESS_CRON_TOKEN` (fallback)
- Configure optional env controls:
  - `CRON_FETCH_LIMIT` (default `12`)
  - `CRON_REFRESH_COMMIT` (`True` to persist content refresh writes)
  - `CRON_STRICT_FRESHNESS` (`True` to fail maintenance run if stale thresholds breach)
  - `CRON_WARM_CACHE` (`True` to warm key pages after maintenance)
- Scheduled jobs:
  - **Preferred:** Fly `cron` process (`deploy/cron-runner.sh`) — see `docs/migrate-off-vercel.md`
  - **HTTP fallback:** `/internal/cron/freshness/` with `Authorization: Bearer $CRON_SECRET`
- Former Vercel cron split (now mirrored by `deploy/cron-runner.sh`):
  - Frequent lightweight run (every 6h)
  - Nightly committed refresh run (02:30 Asia/Kolkata)
- Manual maintenance run:

```bash
python manage.py run_production_maintenance --commit-refresh --strict-freshness --warm-cache
```

- Query-budget profiling run:

```bash
python manage.py profile_page_queries --strict --query-budget 25
```

- Cache warm run:

```bash
python manage.py warm_core_caches
```

## 9. Rollback Plan

If post-deploy regression occurs:

1. Disable AI promotional links if needed (header/home).
2. Set problematic items to `draft`.
3. Roll back release to previous stable build.
4. Re-run `preflight_release --strict` before redeploy.
