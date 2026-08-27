# CareerReality — UI/UX Implementation Plan

Based on `docs/UI_UX_MIGRATION_AUDIT.md` and `docs/TARGET_DESIGN_SYSTEM.md`.

**Strategy:** Evolve the Django + template + CSS stack. Do not rebuild as SPA. Do not replace business logic with mocks. Do not invent generic career-coach features absent from both products.

---

## PHASE 0 — Architecture

**Objective:** Confirm extension points; freeze constraints.

- [x] Audit apps, routes, templates, CSS, models, auth, payments
- [ ] Inventory reusable partials (`header`, `footer`, `utility_dock`, tool hubs)
- [ ] Establish token file as single source (`design-system.css` + theme files)
- [ ] Constraints: keep allauth, Razorpay honesty, Postgres models, Vercel crons, AdSense layout safety

**Exit:** Tokens documented; risk list accepted.

---

## PHASE 1 — Design system

**Objective:** Codify target tokens and base components.

**Files:** `static/css/design-system.css`, `theme-light.css`, `theme-premium-dark.css`, `partials/meta.html`, `static/fonts/*`

**Work:**
1. Add display serif + UI sans (self-hosted).
2. Retokenize colors (paper / terracotta / ink).
3. Radius → sharp; shadows → minimal.
4. Button, input, badge, table, meter, ticker base classes.
5. Focus rings + reduced-motion.

**Validation:** Visual spot-check light+dark; no TS (N/A); CSS loads on home.

---

## PHASE 2 — Application shell

**Objective:** Reference-aligned navigation without deleting CR features.

**Files:** `templates/partials/header.html`, `footer.html`, `base.html`, `mobile_more_sheet.html`, `static/css/style-core.css`, `mobile.css`

**Work:**
1. Primary nav: Terminal · Salary explorer · CTC decoder · Layoff radar · Analysis.
2. Secondary: Companies, AI Pulse, Risk Analyzer, Pro via “More” / dock / footer.
3. Wordmark serif; Night toggle; Create account → branded auth.
4. Footer IA: Tools / Newsroom / Standards.
5. Remove emoji from primary chrome.

**Validation:** All primary routes reachable desktop+mobile; no broken `{% url %}`.

---

## PHASE 3 — Core dashboard (Terminal home)

**Objective:** Homepage matches terminal composition; data remains Django-driven.

**Files:** `templates/core/home.html`, `static/css/style-home.css`, `core/views.py` (only if context needs aggregates)

**Work:**
1. Two-column layout: Index + instruments | hero + salary table + CTA + analysis.
2. Restyle ticker to full-bleed market bar.
3. Salary preview table from real submissions / existing salary-reality context — **no Lovable hardcode**.
4. Dark conversion CTA band.
5. Preserve FAQ/newsletter below fold or relocate thoughtfully.

**Validation:** Home 200; index numbers match DB; mobile stack OK.

---

## PHASE 4 — User profile / member

**Objective:** Branded auth + honest account surfaces.

**Files:** new `templates/account/*`, `accounts/*`, optional ledger view

**Work:**
1. Override allauth login/signup/password templates with CR shell.
2. Align copy with reference member pitch where accurate.
3. Pro dashboard / onboarding restyle (keep logic).
4. P2: private salary ledger UI bound to authenticated user submissions.

**Validation:** Login/signup styled; Google OAuth link intact; CSRF OK.

---

## PHASE 5 — Career discovery (salary explorer + companies)

**Objective:** Salary explorer UX parity; companies restyled.

**Files:** `templates/core/salary.html`, companies templates, CSS

**Work:**
1. Explorer layout: filters/bands, p25/median/p90/n when data allows.
2. Card layout on mobile.
3. Companies directory tokens (no feature removal).

---

## PHASE 6 — Assessment (Resignation Risk + CTC)

**Objective:** Tool UX parity; preserve scoring logic.

**Files:** analyzer templates, `salary_calculator.html`, `style-tools.css`, calculator JS

**Work:**
1. CTC: sliders + live ledger; reuse formulas.
2. Risk wizard: visual restyle only; same steps/result.
3. Loading/error on calculate.

---

## PHASE 7 — Career planning (Escape / Pro roadmap)

**Objective:** Restyle escape plan / paid roadmap; no fake progress engines.

**Files:** `escape_plan.html`, `payments/escape_roadmap.html`, pricing

---

## PHASE 8 — Secondary features

- AI Pulse visual pass  
- Analysis hub route or restyled category list (`/analysis/` alias → articles)  
- Search results  
- Article detail fix (KEY TAKEAWAYS truncation)  
- Layoff radar table + timeline presentation  

---

## PHASE 9 — Responsive

Explicit QA at 1440, 1280, 1024, 768, 430, 390, 375 for shell, home, CTC, layoff, explorer, auth.

---

## PHASE 10 — Accessibility

Skip link, focus, form labels, contrast on terracotta, dialog a11y, ticker motion preference.

---

## PHASE 11 — PERFORMANCE

Font subsetting; avoid duplicate CSS; ticker DOM cost; no extra heavy JS frameworks.

---

## PHASE 12 — QA + parity report

- Regression on core routes  
- Visual compare vs reference  
- Write `docs/UI_UX_FINAL_PARITY_REPORT.md` + `docs/UI_UX_MIGRATION_CHANGELOG.md`  
- Recompute completion % from checklist  

---

## Batch execution rules

For each batch: state objective → touch files → implement → validate → fix → changelog entry → next.

**Priority order:** P0 (tokens, shell, auth, terminal home) → P1 (CTC, explorer, layoff, analysis, theme) → P2 (ledger, secondary restyles) → P3 (polish).

---

## Out of scope (explicit)

- Rebuilding as React/Lovable clone  
- New database for demo data  
- Fake payments  
- Generic skills/goals/OKR coaching modules  
- Deleting Companies / AI Pulse / Risk Analyzer  

---

## Success criteria (not “build passed”)

1. Auth pages match brand shell.  
2. Home reads as editorial terminal with real CR data.  
3. Primary nav matches reference IA; secondary features still reachable.  
4. CTC offers live ledger UX with same math.  
5. Light default + Night works.  
6. Mobile usable at 390px.  
7. Final parity report with evidence-based %.  
