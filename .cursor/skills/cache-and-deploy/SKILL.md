---
name: cache-and-deploy
description: Redis page cache, CDN edge rules, cache-key busting, and Vercel deploy awareness for CareerReality.in. Use after template/CSS/content changes that must appear in production, or when debugging stale HTML.
paths:
  - "core/cache_utils.py"
  - "config/settings.py"
  - "vercel.json"
  - "api/index.py"
  - "static/**"
  - "templates/**"
---

# Cache & Deploy

## Why this matters

Production is **Vercel serverless + Redis**. Without Redis, page cache does not persist across instances (see warning in `config/settings.py`). UI redesigns and footer/tool fixes repeatedly required an explicit cache bust to go live.

## Key mechanisms (`core/cache_utils.py`)

- Page HTML caching + `invalidate_cached_pages(paths)`
- `warm_page_cache()` — hits `STATIC_WARM_PATHS` and recent articles
- `invalidate_sitemap_cache()` / `invalidate_career_index_cache()`
- `EDGE_CACHE_RULES` — CDN TTL hints by path regex
- `EDGE_CACHE_DENY_PREFIXES` — separate deny list (`/admin/`, `/accounts/`, `/payments/`, `/search/`, …)

Commands live in `core/management/commands/` (`warm_page_cache`, `run_production_maintenance`).

## Settings knobs (`config/settings.py`)

- `REDIS_URL` or `KV_URL`
- `CACHE_TIMEOUT_SECONDS` (default ~300)
- **`CACHE_KEY_PREFIX`** (e.g. `cr-tools-v2`) — **bump this** when you need a global HTML/CSS cache bust across all keys
- Per-view timeouts: `PAGE_CACHE_ARTICLE_SECONDS`, `PAGE_CACHE_HOME_SECONDS`, etc.

## After public-facing changes

1. Prefer targeted invalidation for changed paths.
2. If a redesign still looks stale in prod → bump `CACHE_KEY_PREFIX` and redeploy.
3. Warm critical paths:

```bash
python manage.py warm_page_cache
# or full maintenance:
python manage.py run_production_maintenance
```

4. Cron already warms/freshens via `vercel.json` (`/internal/cron/warm-cache/`, freshness crons).

## Static assets

- CSS lives in `static/css/` (`design-system.css`, `mobile.css`, `style-tools.css`, theme files).
- Some templates cache-bust with `?v=` query params — bump when theme/JS must refresh without Redis prefix change.
- `collectstatic` is part of release flow (`release-preflight`).

## Do not

- Cache authenticated or payment/search responses at the edge.
- Assume a Vercel deploy alone clears Redis HTML keys — it does not.
