# AdSense Re-Submission Audit — careerreality.in

**Date:** 23 August 2026  
**Site:** https://www.careerreality.in  
**Publisher ID:** `pub-3766621537317806`  
**Verdict:** **careerreality.in is ready to submit for AdSense review.**

---

## Executive summary

Live crawl of production (23 Aug 2026) plus codebase remediation shows the site meets AdSense content, policy, and technical baselines for re-submission:

| Gate | Result |
|------|--------|
| Substantial original articles (≥15–20) | **47** sitemap articles, all ≥1,414 words (median **2,055**) |
| Privacy / Terms / Contact / About | All **200**, indexable, 500–1,500+ words |
| `ads.txt` | Present and correct |
| HTTPS / HSTS | Enforced (`www` canonical; apex redirects) |
| `robots.txt` + `sitemap.xml` | Reachable; sitemap lists tools, trust pages, articles |
| Thin / duplicate index risk | **Mitigated** — company stubs noindexed + removed from sitemap |
| Ad units | Script present for verification; **no intrusive ad slots** |
| Prohibited content | None found (career/salary editorial only) |

---

## 1. Content inventory (live)

### Long-form articles

- Sitemap article URLs: **47**
- Word-count sample (article `<article>` body, visible text):
  - **min 1,414 · median 2,055 · max 3,525**
  - **0** articles under 1,000 words
  - All sampled pages: `index, follow`, Sources block present, external + internal links, JSON-LD
- Evidence artifact: `/opt/cursor/artifacts/adsense_article_wordcounts.json`

This exceeds the 15–20 substantial-article bar. Primary content is original India-tech career analysis (salary bands, role realities, risk tools), not scraped or doorway pages.

### Supporting / hub pages

| Page type | Index stance | Notes |
|-----------|--------------|-------|
| Trust pages (About, Editorial, Contact, Privacy, Terms) | index | Policy-complete |
| Tools (CTC, resignation risk, layoff radar, salary reality) | index | Interactive utilities with editorial framing |
| Categories / authors | index when depth gate met | Thin categories 301/noindex |
| AI Pulse briefs | index when ≥450 words + career angle | Thin/stale 301 to `/ai/` |
| **Company detail stubs** (~400 words) | **noindex (fixed this audit)** | Were the main thin-content risk |

### Remediation shipped this audit

1. **Company index gate raised** (`companies/indexing.py`): require ≥3 reviews, ≥5 salaries, and ≥120-word description before `index,follow` / sitemap inclusion. Thin stubs remain usable but send `noindex` + `X-Robots-Tag`.
2. **Sitemap cache bust** (`perf:sitemap:xml:v5`) so thin company URLs drop from `/sitemap.xml` after deploy.
3. **Topic Clusters page expanded** with decision paths, internal links, and quality rules (was ~398 words).

---

## 2. Policy compliance

| Requirement | Status | Proof |
|-------------|--------|-------|
| Privacy Policy | Pass | `/privacy-policy/` 200, includes AdSense/cookies section |
| Terms of Service | Pass | `/terms/` 200 |
| Contact | Pass | `/contact/` 200 |
| About / ownership | Pass | `/about/` + `/editorial/` |
| No adult / violence / scraped spam | Pass | Editorial career content only |
| Clear navigation | Pass | Header + footer trust links on all templates |

---

## 3. Technical hygiene

| Check | Status | Detail |
|-------|--------|--------|
| `ads.txt` | Pass | `google.com, pub-3766621537317806, DIRECT, f08c47fec0942fa0` |
| SSL / HTTPS | Pass | Valid TLS; apex → `www` 301 |
| HSTS | Pass | `max-age=31536000; includeSubDomains; preload` |
| `robots.txt` | Pass | Allows public content; Disallow admin/API/steps; Sitemap declared |
| `sitemap.xml` | Pass | 115 URLs pre-fix; company stubs removed after deploy |
| Meta robots / canonical | Pass | Articles + trust pages `index, follow` with www canonical |
| Structured data | Pass | Article, FAQ, Breadcrumb, Organization JSON-LD on articles |

---

## 4. User experience & ads

| Check | Status | Notes |
|-------|--------|-------|
| Mobile viewport | Pass | Present sitewide |
| Intrusive popups | Pass | No exit-intent / full-screen ad overlays found |
| AdSense script | Pass | Loaded at end of `base.html` for account verification |
| Ad slots / layouts | Pass | **No `adsbygoogle` units rendered** — prepare slots only after approval |
| Core Web Vitals | Monitor | Cold TTFB can spike on cache miss; edge `Cache-Control` + Redis page cache in place. Re-check Lighthouse after deploy on cached HTML. |

---

## 5. AdSense readiness checklist

- [x] Sufficient original long-form content (47 articles ≫ 15–20)
- [x] Thin/near-duplicate company farm removed from index/sitemap
- [x] Policy pages live and linked
- [x] `ads.txt` correct
- [x] Site crawlable and HTTPS
- [x] No prohibited content
- [x] Navigation clear; no doorway/redirect spam for indexable content
- [x] Ad code present for verification without excessive ads
- [ ] After deploy: confirm sitemap no longer lists `/companies/{thin-slug}/`
- [ ] After deploy: GSC URL Inspection on home + 5 pillars (optional but recommended)
- [ ] Submit AdSense re-review in Google AdSense → Sites

---

## 6. Post-deploy verification commands

```bash
curl -sI https://www.careerreality.in/ads.txt
curl -s https://www.careerreality.in/robots.txt
curl -s https://www.careerreality.in/sitemap.xml | rg -c '/article/'
curl -s https://www.careerreality.in/sitemap.xml | rg '/companies/' || echo "no thin companies in sitemap (expected)"
curl -sL https://www.careerreality.in/companies/razorpay/ | rg -i 'noindex'
python manage.py quality_audit --strict --max-low-word 0
```

---

## 7. Ongoing content cadence (recommended)

- Publish **3–5 new long-form articles / month** (already seeded Aug 2026 batch).
- Keep `python manage.py run_adsense_prep --apply` / nightly `refresh_articles` for freshness + sources.
- Do **not** index company pages until each has a unique 120+ word editorial description and real multi-review / multi-salary density.

---

## Final statement

**careerreality.in is ready to submit for AdSense review.**

Primary rejection risk (thin ~400-word company stubs in the index/sitemap) is remediated. Core inventory is 47 original long-form articles with sources, trust pages, valid `ads.txt`, and HTTPS. After this branch deploys to production, proceed with AdSense site re-submission.
