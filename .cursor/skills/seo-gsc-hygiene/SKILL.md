---
name: seo-gsc-hygiene
description: SEO and Google Search Console hygiene for CareerReality.in — canonical redirects, thin category handling, sitemap exclusions, vercel.json 301s, noindex cleanup. Use for crawl issues, duplicate URLs, or indexing fixes.
paths:
  - "content/seo_redirects.py"
  - "vercel.json"
  - "core/sitemaps.py"
  - "core/sitemap*.py"
  - "core/seo_pages.py"
  - "templates/partials/meta.html"
---

# SEO / GSC Hygiene

## Source of truth

- **Django redirects & sitemap rules:** `content/seo_redirects.py`
  - `ARTICLE_CANONICAL_REDIRECTS` — loser slug → winner (301)
  - `CATEGORY_CANONICAL_REDIRECTS` — thin categories → richer sibling
  - `ARTICLE_SITEMAP_EXCLUDE_SLUGS` — losers stay out of sitemap
  - `MIN_INDEXABLE_CATEGORY_ARTICLES = 3` — thin hubs must not be indexable
- **Edge/CDN redirects:** mirror critical article 301s in `vercel.json` `redirects`
- **Sitemaps:** `core/sitemaps.py`, `core/sitemap_view.py`, `core/sitemap_fallback.py`

## Rules that caused past GSC fires

1. Duplicate topic clusters compete — always pick one canonical winner.
2. Thin category archives (`< 3` published) → permanent redirect, do not leave noindex traps that stay “Excluded”.
3. Dead / superseded AI or article URLs need both Django handling and `vercel.json` when crawl lag persists.
4. After fixing redirects/noindex, **bust Redis + warm cache** so production serves the new headers/body.

## Checklist when adding a redirect

1. Add mapping to `ARTICLE_CANONICAL_REDIRECTS` or `CATEGORY_CANONICAL_REDIRECTS`.
2. Add matching permanent entries in `vercel.json` (with and without trailing slash if that pattern is used).
3. Confirm loser is excluded from sitemap helpers (`published_article_q`).
4. Invalidate sitemap cache: helpers in `core/cache_utils.py` (`invalidate_sitemap_cache`).
5. Spot-check: winner returns 200 indexable; loser returns 301 to winner.

## Useful commands

```bash
python manage.py seo_audit
python manage.py draft_redirect_losers
python manage.py preflight_release --strict
```

## AdSense / thin-content safety

Do not create indexable empty hubs, doorway pages, or near-duplicate articles. Prefer expanding the canonical URL.
