---
name: career-reality-overview
description: CareerReality.in project map — Django 6 + Vercel stack, apps, voice, and where to change things. Use when onboarding, exploring architecture, or deciding which app owns a feature.
---

# Career Reality — Project Overview

Site: **CareerReality.in** — India-focused career reality checks (salary truth, skill decay, trade-offs). Honest, anti-hype editorial voice. Not a generic job board.

## Stack

- **Django 6** (`config/` settings, `manage.py`)
- **Postgres** via `DATABASE_URL` / `POSTGRES_URL`
- **Redis** page cache (`REDIS_URL` / `KV_URL`) — required for production TTFB
- **Vercel** serverless (`api/index.py` WSGI, `vercel.json` crons + redirects)
- **WhiteNoise** static files; templates under `templates/`; CSS under `static/css/`
- **Razorpay** payments, **django-allauth** accounts, **Resend** email, optional **OpenAI** for analyzer tools

## Apps (ownership)

| App | Owns |
|-----|------|
| `content/` | Articles, authors, categories, expansions, SEO redirects, citations |
| `core/` | Homepage, tools hubs, sitemaps, cache helpers, SEO pages, crons |
| `ainews/` | AI Pulse hub, feed fetch/prune, impact filters |
| `companies/` | Company profiles, reviews, discussions; surfaces analyzer salary/layoff data |
| `analyzer/` | Salary submissions/layoffs data, calculator, resignation risk, layoff radar |
| `accounts/` | Auth, Pro access |
| `payments/` | Pricing, Razorpay |
| `search/` | Site search |
| `api/` | Vercel WSGI deploy entry only (`index.py`) — not an `INSTALLED_APPS` app |

## Editorial voice (non-negotiable)

- Reality over motivation. Quantify with LPA, cities, YOE where possible.
- Name myths vs reality. Include `who_should_avoid` and stuck points.
- Prefer AmbitionBox / Glassdoor / Naukri / gov / primary sources over vague “guides”.
- Strip generic “safety pad” boilerplate (`content/boilerplate.py`).

## Where change usually lands

- New long-form article → seed script + `content.models.Article` fields → templates in `templates/content/`
- UI / mobile shell → `templates/partials/`, `static/css/mobile.css`, `design-system.css`
- SEO / GSC → `content/seo_redirects.py`, `vercel.json` redirects, `core/sitemaps.py`
- Cache after public HTML/CSS change → bump `CACHE_KEY_PREFIX` or invalidate via `core/cache_utils.py`
- Production safety → `python manage.py preflight_release --strict` (see `release-preflight`)

## Docs worth reading

- `docs/ai-pulse-production-checklist.md`
- `docs/article_freshness_audit.md`
- `docs/published_core_article_upgrade_sheet.md`
- `docs/top5_credibility_report.md`
- `docs/adsense-rereview-checklist-2026-02-16.md`
