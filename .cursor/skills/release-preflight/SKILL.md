---
name: release-preflight
description: Production release checklist for CareerReality.in — preflight_release, migrations, collectstatic, content hardening, AdSense/security settings. Use before shipping risky changes or diagnosing production misconfig.
paths:
  - "core/management/commands/preflight_release.py"
  - "core/management/commands/run_production_maintenance.py"
  - "docs/ai-pulse-production-checklist.md"
  - "docs/adsense*"
  - "config/settings.py"
  - "vercel.json"
  - ".env.example"
---

# Release Preflight

## Mandatory gate

```bash
python manage.py preflight_release --strict
```

With stale-content enforcement:

```bash
python manage.py preflight_release --strict --check-freshness
```

Fails on unsafe production settings / freshness blockers.

Optional Windows bundle (if used locally): `scripts/preprod_release_bundle.ps1 -ProductionLike [-RunTests]`

## Release order (from AI Pulse checklist)

1. Confirm env: `DEBUG=False`, `ALLOWED_HOSTS`, SSL/cookie secure flags, `SECRET_KEY`, `DATABASE_URL`/`POSTGRES_URL`, `REDIS_URL`
2. `python manage.py migrate`
3. `python manage.py collectstatic --noinput`
4. Content hardening: `python manage.py apply_release_content_fixes` (when applicable)
5. Spot-check AI items + a few articles for sources/dates
6. Smoke: `python manage.py fetch_ai_news --limit 1`
7. Maintenance/warm: `python manage.py run_production_maintenance` or `warm_page_cache`

## Ongoing production jobs (`vercel.json` crons)

- Freshness / refresh / prune / bootstrap
- Warm cache
- Weekly digest
- Layoff alerts
- Career index monthly refresh

Internal cron views live under `/internal/cron/...` in `core` — protect with the project’s existing secret/auth pattern; do not expose without checks.

## AdSense / trust

Follow `docs/adsense-rereview-checklist-*.md` and credibility docs — no thin doorways, clear authorship, real policies pages (`/privacy-policy/`, `/terms/`, `/editorial/`).

## After UI-only deploys

Still verify cache (`cache-and-deploy`). A green Vercel build can serve stale Redis HTML.
