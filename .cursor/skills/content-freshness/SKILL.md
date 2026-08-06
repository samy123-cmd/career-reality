---
name: content-freshness
description: Keep published Career Reality articles and market blocks current — freshness audits, reality-check dates, market period refresh, expansion commands. Use for stale content, monthly bootstrap, or refresh-published-articles work.
paths:
  - "content/**"
  - "docs/article_freshness*"
  - "docs/published_core*"
  - "core/management/commands/bootstrap_*.py"
  - "seed_*.py"
---

# Content Freshness

## Signals of staleness

- `last_reality_check` older than policy thresholds (preflight `--check-freshness`)
- Market block period behind current month (e.g. still `2026-07` when target is `2026-08`)
- Missing external sources, thin salary sections, short meta (see upgrade sheet)
- Docs: `docs/article_freshness_audit.md`, `docs/published_core_article_upgrade_sheet.md`

## Commands / scripts

```bash
python manage.py refresh_published_articles
python manage.py expand_core_articles
python manage.py expand_low_word_articles
python manage.py harden_content_quality
python manage.py append_reality_review_block
python manage.py generate_upgrade_sheet
python manage.py quality_audit
python manage.py apply_release_content_fixes   # if present in release path
```

Monthly bootstraps (examples):

- `python manage.py bootstrap_august_2026`
- `python manage.py bootstrap_july_2026`
- Root seed scripts: `seed_august_2026.py`, `seed_july_2026.py`, etc.

Crons: `vercel.json` freshness endpoints with `commit_refresh`, `refresh_articles`, `bootstrap_august`, `prune_ai`.

## Refresh checklist

1. Update facts, LPA ranges, and year-in-title framing for the current market period.
2. Set `last_reality_check` to the review date.
3. Ensure ≥2–3 external sources in body HTML.
4. Expand thin `salary_reality` sections.
5. Regenerate or update `docs/article_freshness_audit.md` when doing a batch pass.
6. Invalidate/warm caches for touched article URLs.

## Market data helpers

- `content/article_market_data.py`, `content/article_refresh.py`
- Company-linked salary context may come from `companies/` seeds (`seed_company_intelligence`)
