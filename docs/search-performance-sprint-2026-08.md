# Search Performance Sprint — August 2026

**Date:** 23 Aug 2026  
**GSC snapshot (last 7 days to 21 Aug):** 0 clicks · 329 impressions · **0% CTR** · avg position **23.8**

## Diagnosis (not a content collapse)

| Signal | Meaning |
|--------|---------|
| Position ~24 | Mostly page 2–3 → CTR near zero is expected |
| 329 impressions / week | Discovery is tiny; brand + long-tail only |
| 47 long-form articles live | Inventory is fine; **ranking depth** is the bottleneck |
| AdSense path | Separate from organic; do both, don’t confuse them |

This is an early-site ranking problem, not “another disaster” of empty pages. Soft launches often show impressions before clicks until tools break into page-1 for high-intent queries.

## What we shipped in code (this sprint)

1. **CTR-tuned titles/descriptions** for Home, CTC Calculator, Salary Reality, Layoff Radar, Resignation Risk — lead with query language (`CTC to in-hand`, `IT layoffs India 2026`, `software engineer salary India 2026`).
2. **Snippet-ready FAQs** on CTC + Layoff (longer answers) + homepage FAQs rewritten around real search questions.
3. **Homepage subtitle** now names the free tools Google should associate with the brand.
4. **Home cache bust** (`home_v4`) so production HTML updates after deploy.

## Your 14-day operator checklist (GSC)

Do these in Search Console — code cannot click “Request indexing” for you:

### Day 0 (after deploy)
1. Performance → filter last 28 days → **Queries** + **Pages**. Export CSV.
2. URL Inspection → Request indexing for:
   - `/`
   - `/salary-calculator/`
   - `/salary-reality/`
   - `/layoff-radar/`
   - `/resignation-risk/`
   - Top 5 articles by impressions (even if position 20+)
3. Sitemaps → resubmit `https://www.careerreality.in/sitemap.xml`

### Days 1–7
4. For every query with **≥10 impressions and CTR 0%**, open the landing page title — if it doesn’t match the query intent, we rewrite again.
5. Pages with impressions but position **>15**: add 1 internal link from homepage tools + 1 from a related article (already partially wired via tool hub).
6. Do **not** publish thin company stubs or duplicate topics — that killed AdSense once.

### Days 8–14
7. Publish **2–3** long-form pieces aimed at page-1 long-tail (examples):
   - “CTC vs in-hand salary India example 12 LPA / 20 LPA / 30 LPA”
   - “Notice period buyout India — how companies calculate”
   - “IT hiring freeze vs layoff — how to tell the difference”
8. Re-check Performance: goal is **impressions ↑** first, then position **&lt;15** on tool queries, then clicks.

## Targets (realistic for next 30 days)

| Metric | Now | 30-day target |
|--------|-----|----------------|
| Weekly impressions | ~330 | **1,000+** |
| Avg position (site) | 23.8 | **&lt;18** |
| Clicks / week | 0 | **20–50** (mostly tools) |
| Tool query position (CTC / layoffs) | unknown / deep | **Top 20 → Top 10** |

## What will *not* fix this overnight

- More noindex alone
- AdSense approval alone
- Publishing 50 thin pages
- Waiting without requesting indexing on money URLs

Authority compounds: consistent tool utility + long-form + internal links + external mentions. Keep shipping weekly; panic publishing will recreate the thin-content failure mode.
