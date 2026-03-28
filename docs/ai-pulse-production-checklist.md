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

This command fails if blocking settings are unsafe for production.

## 3. Database and Assets

Run in order:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 4. Content/Editorial Checks

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

## 6. Post-Deploy Smoke Tests

- `/ai/` renders and paginates
- `/ai/<slug>/` renders timeline + visual sections
- `/ai/tag/<slug>/` filtering works
- `/sitemap.xml` includes `/ai/` URLs
- Home header links include `AI Pulse`

## 7. Rollback Plan

If post-deploy regression occurs:

1. Disable AI promotional links if needed (header/home).
2. Set problematic items to `draft`.
3. Roll back release to previous stable build.
4. Re-run `preflight_release --strict` before redeploy.
