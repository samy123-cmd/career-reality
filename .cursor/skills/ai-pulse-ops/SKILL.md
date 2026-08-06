---
name: ai-pulse-ops
description: Operate the AI Pulse / ainews pipeline — fetch, prune, fact-check status, hub indexability, and production checklist. Use when working on /ai/ pages, feed ingestion, or AI editorial quality.
paths:
  - "ainews/**"
  - "templates/ainews/**"
  - "docs/ai-pulse*"
  - "static/css/ai_pulse.css"
---

# AI Pulse Operations

## Purpose

`/ai/` translates model/news updates into **engineering skills, workflow impact, and India hiring leverage** — not hype recaps. High-signal items need Skill Map + Decision Checklist value.

## App surface

- Models/views/indexing: `ainews/`
- Commands: `fetch_ai_news`, `prune_ai_news`
- Templates: `templates/ainews/`
- Styles: `static/css/ai_pulse.css`
- Production checklist: `docs/ai-pulse-production-checklist.md`

## Publish readiness

Before promoting an AI item publicly:

- `status=published`
- `fact_check_status=verified` when ready for promotion
- `event_date` set (actual event)
- `reviewed_at` set (latest editorial update)
- Source links + timeline consistency spot-checked

## Ops commands

```bash
python manage.py fetch_ai_news --limit 1   # smoke
python manage.py prune_ai_news
python manage.py preflight_release --strict --check-freshness
```

Crons in `vercel.json` already fetch/prune/refresh on a schedule — prefer fixing pipeline code over one-off prod hacks.

## SEO notes

- Hub must remain indexable when it has real content; past work cleared GSC noindex exclusions for AI hub and dead AI URLs.
- Thin or dead AI URLs → canonicalize/redirect (`seo-gsc-hygiene`), then cache bust.

## Editorial bar

Prefer items that change a reader’s next 30-day plan (skills, hiring, tooling). Skip vanity model launches with no India workflow impact.
