# CareerReality UI/UX Migration Audit

**Audit date:** 2026-08-27  
**Current application:** https://www.careerreality.in/ (Django production, Vercel)  
**Reference / UX benchmark:** https://real-career-compass.lovable.app/ (Lovable SPA)  
**Codebase:** Django 6 + django-allauth + Whitenoise + Razorpay + Postgres/SQLite  

> **Product clarification:** Both products are **salary / career-intelligence platforms for Indian tech**, not generic career-coaching apps (no skills roadmap, personality assessment, or goal OKRs in either product). Generic “assessment → goals → roadmap” items from a generic career-product template are marked **N/A** unless they map to an existing CareerReality capability (e.g. Resignation Risk Analyzer).

---

## 0. Architecture snapshot (repository)

| Layer | Finding |
| ----- | ------- |
| Framework | Django ≥6, server-rendered Jinja/Django templates |
| Apps | `core`, `content`, `analyzer`, `companies`, `ainews`, `accounts`, `payments`, `search`, `api` |
| Auth | django-allauth (+ Google OAuth env); **no custom login/signup templates** |
| Styling | Multi-file CSS (~9.8k LOC): `style-core`, `style-home`, `style-tools`, `style-companies`, `ai_pulse`, `mobile`, `design-system`, `theme-premium-dark`, `theme-light`, `theme-dark-contrast` |
| Design tokens | CSS variables (`--cr-*`, `--c-*`); dark default (`theme-dark`); light opt-in |
| JS | `main.js`, `theme.js`, `animations.js`; inline analytics `crTrack` |
| Data | Postgres via `DATABASE_URL`; models for salaries, layoffs, index snapshots, articles, companies, AI news, orders |
| Payments | Razorpay; buttons disabled when key missing (“Payments coming soon”) |
| Deploy | `vercel.json` crons + redirects; Whitenoise static |

**Important:** Live `careerreality.in` is **not** a redirect to Lovable. Production HTML is Django (`theme-dark`). The Lovable app is a **separate UX prototype** of the same brand/product concept.

---

## SECTION 1 — CareerReality current application

| Area | Route | Current Implementation | Status | Quality | Notes |
| ---- | ----- | ---------------------- | ------ | ------- | ----- |
| Homepage / Terminal | `/` | Dark SaaS hero + index card + live ticker + tools list + articles + FAQ + newsletter | COMPLETE | MEDIUM | Functional; visual language ≠ reference (dark/SaaS vs light editorial terminal) |
| Live salary ticker | `/` + `/api/salary-feed/` | Scrolling ticker from submissions | COMPLETE | MEDIUM | Exists; styling differs from black monospace reference bar |
| Career Reality Index (home widget) | `/` | Score + 3 meters from `CareerRealityIndexSnapshot` | COMPLETE | HIGH | Real data path |
| Career Reality Index (full) | `/career-reality-index/` | Monthly table + methodology | COMPLETE | HIGH | Strong; denser than reference sidebar |
| Salary Reality / explorer | `/salary-reality/` | Editorial salary bands table + methodology | PARTIAL | MEDIUM | Data exists; missing reference percentile explorer UX (p25/median/p90/n filters) |
| CTC Decoder | `/salary-calculator/` | Form submit → decode (CTC, variable %, rent, city) | PARTIAL | MEDIUM | Logic exists; not live slider+ledger UX of reference |
| Layoff Radar | `/layoff-radar/` | Searchable company risk cards + report flow | PARTIAL | MEDIUM | Functional; no employer-group stability score table / timeline like reference |
| Report layoff | `/layoff-radar/report/` | Form → `LayoffReport` | COMPLETE | MEDIUM | Preserve |
| Analysis / articles | `/article/<slug>/`, categories, authors | Full CMS articles | COMPLETE | MEDIUM | Richer than reference; KEY TAKEAWAYS truncation bug observed live |
| Analysis hub equivalent | home + categories | No dedicated `/analysis` list matching reference feed layout | PARTIAL | MEDIUM | Content exists; IA differs |
| AI Pulse | `/ai/`, `/ai/<slug>/`, tags | Editorial AI news hub | COMPLETE | HIGH | CR-only; preserve & restyle |
| Companies directory | `/companies/` | Grid, search, filters, salary counts | COMPLETE | MEDIUM | CR-only; white cards on dark |
| Company detail / reviews / discussions | `/companies/<slug>/`, discussions | Reviews, discussions, upvotes | COMPLETE | MEDIUM | Preserve |
| Resignation Risk Analyzer | `/resignation-risk/` + wizard steps + result | Multi-step wizard (`AssessmentLog`) | COMPLETE | MEDIUM | Maps loosely to “assessment”; keep business logic |
| Salary drop / unlock | `/salary-drop/`, unlock | Anonymous salary submission flywheel | COMPLETE | MEDIUM | Backend for public benchmarks |
| Escape plan | `/escape-plan/`, `/payments/escape-roadmap/` | Content + paid checklist | COMPLETE | MEDIUM | Preserve |
| Pricing / Pro | `/payments/pricing/`, `/pro/` | Free / Pro / checklist tiers | PARTIAL | MEDIUM | UI exists; Razorpay may be disabled without keys |
| Pro dashboard | `/pro/dashboard/` | Authenticated Pro area | PARTIAL | MEDIUM | Exists in templates; needs visual parity pass |
| Onboarding | `/pro/onboarding/` | Profile onboarding | PARTIAL | LOW | Present but not reference-aligned |
| Search | `/search/`, suggest API | Global search | COMPLETE | MEDIUM | Preserve |
| Auth login/signup | `/accounts/login/`, `/accounts/signup/` | Default allauth HTML | BROKEN | LOW | **Unstyled, no brand shell, light page on dark site** |
| Auth (reference-style member ledger) | N/A | Private salary ledger UX from reference | MISSING | — | Backend has submissions; no personal ledger UI |
| Theme toggle | header | Dark default / light opt-in | COMPLETE | MEDIUM | Reference is light-default with Night toggle (inverted) |
| Navigation shell | header + mobile dock | Mega Explore/Topics + utility dock | PARTIAL | MEDIUM | Busy vs reference flat Terminal/Salary/CTC/Layoff/Analysis |
| About / editorial / legal | `/about/`, `/editorial/`, policies | Static pages | COMPLETE | MEDIUM | Preserve |
| Newsletter | `/newsletter/signup/` | Subscriber model | COMPLETE | LOW | “2 subscribers” copy weak |
| Health / robots / sitemap | various | Ops endpoints | COMPLETE | HIGH | N/A for UX |

**Status legend used:** COMPLETE = UI+route+data+states acceptable for current product; PARTIAL = works but gaps vs target UX or incomplete polish; BROKEN = fails production quality; MISSING = not present; UNKNOWN = not verified end-to-end in this audit.

---

## SECTION 2 — Reference application inventory

| Reference Feature | Screen | Route | Components | User Interaction | Responsive Behavior |
| ----------------- | ------ | ----- | ---------- | ---------------- | ------------------- |
| Live ticker | Global | all | Black scrolling monospace bar, ±% colors | Passive-only | Full-width retained |
| Primary nav | Global | all | Serif wordmark; Terminal / Salary explorer / CTC / Layoff / Analysis; Night; Create account | Click routes; Night toggles theme | Collapses to MENU |
| Terminal homepage | Home | `/` | Two-column: Index sidebar + hero + percentile salary table + dark CTA + analysis list + instruments | Open explorer; Create account | Stacks; salary rows → cards |
| Career Reality Index | Home sidebar | `/` | Big score, band label, 3 meters, instrument links | Links to tools | Full-width card on mobile |
| Salary explorer | Explorer | `/salary-explorer` | Expanded compensation bands with sources/sample sizes | Browse / open bands | Table → cards |
| CTC decoder | Tool | `/ctc-decoder` | Instrument label, 3 range sliders, monthly in-hand card, annual ledger | Real-time recalculation | Stacked columns |
| Layoff radar | Tool | `/layoff-radar` | Status badge, stability table (employer group/sector/signal/risk/stability), event timeline | Scan / compare | Wide table → stacked |
| Analysis index | Newsroom | `/analysis` | Category tags, date, read time, headline, dek, All analysis CTA | Open articles | Single column |
| Analysis article | Article | `/analysis/<slug>` | Editorial long-form | Read | Reading column |
| Auth / member | Auth | `/auth` | Branded create/sign-in, private ledger pitch | Form submit | Centered form |
| Submit / write | Footer | `/submit` | Contributor CTA | Navigate | — |
| Footer standards | Global | — | Tools, Newsroom, Methodology, Privacy | Links | Stacked |
| Empty/loading/error | Various | — | Not fully observed publicly | — | — |

**Not in reference (CareerReality-only):** Companies intelligence, AI Pulse, Resignation Risk wizard, Escape Plan, Razorpay Pro tiers, discussions, search mega-menu. These stay in CR and get design-system restyle — not deleted.

---

## SECTION 3 — Feature parity matrix

| Feature | CareerReality | Reference | Status | Gap | Required Work | Priority |
| ------- | ------------- | --------- | ------ | --- | ------------- | -------- |
| Terminal homepage IA | Dark marketing hero | Light editorial terminal + table | PARTIAL | Composition, hierarchy, density | Redesign home to terminal layout; keep Django data | P0 |
| Flat product nav | Mega Explore/Topics | 5 primary links | PARTIAL | Cognitive load | Simplify primary nav; move extras to secondary | P0 |
| Auth branded UI | Unstyled allauth | Branded `/auth` | BROKEN | No shell/CSS | Custom allauth templates + tokens | P0 |
| Design tokens / light editorial default | Dark SaaS + Inter | Cream page, serif display, terracotta accent, sharp edges | PARTIAL | Entire visual system | Extend CSS variables; fonts; radius; accents | P0 |
| Live ticker styling | Inline “Live” strip | Full black market ticker | PARTIAL | Visual | Restyle ticker component | P1 |
| Salary explorer percentiles | Salary Reality editorial table | p25/median/p90/n explorer | PARTIAL | Interaction model | Enhance `/salary-reality/` UI; wire existing submissions | P1 |
| CTC live ledger | Form decode | Sliders + ledger | PARTIAL | Interaction | Keep calc logic; add live slider UI | P1 |
| Layoff stability table | Card list | Group stability + timeline | PARTIAL | Information design | Restyle + optional stability score from existing fields | P1 |
| Analysis feed layout | Home list / categories | Dedicated analysis index | PARTIAL | Route/IA | Add analysis list view or restyle category hub | P1 |
| Index presentation | Widget + full page | Sidebar instrument | PARTIAL | Layout | Align home sidebar presentation | P1 |
| Member private ledger | Submissions anonymous | Private ledger account | MISSING | Product surface | New UI on existing `SalarySubmission` + auth; careful privacy | P2 |
| Night / theme | Dark default | Light default + Night | PARTIAL | Default inversion | Align defaults with target (light editorial primary) while preserving dark | P1 |
| Companies / AI / Risk / Pro | Present | Absent in reference | COMPLETE* | Visual only | Restyle into design system (*feature complete, not reference-cloned) | P2 |
| Payments | Conditional keys | N/A | PARTIAL | Env-dependent | Do not fake; document gap | P2 |
| Generic skills/goals/roadmap coaching | N/A | N/A | N/A | Out of product scope | Do not invent | — |
| Accessibility | Mixed | Not audited fully | PARTIAL | Focus, auth forms, contrast on pricing cards | Phase 10 pass | P1 |
| Loading/empty/error states | Inconsistent | Minimal demo | PARTIAL | Skeletons/empty CTAs | Standardize components | P2 |

---

## SECTION 4 — UI parity matrix

| UI Area | CareerReality Current | Reference | Difference | Required Implementation | Priority |
| ------- | --------------------- | --------- | ---------- | ----------------------- | -------- |
| Typography | Inter / system; SaaS weights | Serif display + clean sans + mono data | Brand voice mismatch | Add display serif; keep mono for data; retire Inter-as-brand | P0 |
| Font sizes | Large marketing H1 | Editorial H1 with restrained scale | Hierarchy | Tokenize type scale | P0 |
| Colors | Near-black page, sky accent, orange hero accent | Off-white `#F5F5F0`-ish, near-black ink, terracotta accent | Invert default theme | New token set; map semantic colors | P0 |
| Backgrounds | Flat dark + glow accents | Paper / editorial flat | Atmosphere | Paper bg + subtle texture optional (not purple gradients) | P0 |
| Spacing | Dense mega-nav; marketing sections | Generous editorial whitespace | Density | Section rhythm tokens | P1 |
| Containers | `container-wide` ~1100px | ~1200 editorial | Minor | Align max-widths | P2 |
| Cards | Rounded, bordered, hover lift | Minimal radius, hairline rules, flat | Over-carded | Prefer rows/ledgers; cards only for interactive clusters | P0 |
| Borders / radius | 8–16px common | 0–4px sharp | Soft SaaS vs terminal | Lower radii in tokens | P0 |
| Shadows | Multi-level shadows | Nearly flat | Reduce shadow usage | Shadow tokens → none/sm only | P1 |
| Buttons | Filled rounded primary | Sharp primary terracotta / ghost outline | Style | Button variants in design system | P0 |
| Inputs | Standard forms | Range sliders + ledger | Interaction | Slider component for CTC | P1 |
| Badges | Pills | Small caps labels / risk chips | Style | Restyle badges | P1 |
| Navigation | Mega dropdown + emoji | Flat text links + underline active | IA | Rebuild header partial | P0 |
| Sidebar | Utility dock icons | Index as content sidebar | Pattern | Homepage two-column shell | P0 |
| Mobile nav | Hamburger + bottom dock | MENU text + stacked | Keep dock; restyle | Restyle mobile header | P1 |
| Tables | Editorial + zebra | Borderless hairline salary table | Visual | Shared `DataTable` styles | P1 |
| Progress bars | Index meters | Thin meters | Close | Unify meter component | P2 |
| Empty / loading | Sparse | Sparse | Both weak | Shared EmptyState/Skeleton | P2 |
| Auth UI | Unstyled | Branded | Critical gap | Templates | P0 |
| Icons / emoji | Emoji in CTAs/nav | Minimal / none | Clutter | Replace emoji with SVG or remove | P1 |
| Charts | Limited | Progress + tables | OK | Avoid chart bloat | P3 |

---

## SECTION 5 — Route parity

| Route | CareerReality | Reference Equivalent | Functional | Visual Match | Action |
| ----- | ------------- | -------------------- | ---------- | ------------ | ------ |
| `/` | home | Terminal `/` | Yes | Low | Redesign template/CSS |
| `/salary-reality/` | salary explorer | `/salary-explorer` | Yes | Low | Restyle + enhance explorer UX |
| `/salary-calculator/` | CTC | `/ctc-decoder` | Yes | Low | Live slider ledger UI |
| `/layoff-radar/` | layoff | `/layoff-radar` | Yes | Medium-Low | Restyle table/timeline |
| `/career-reality-index/` | index | Home sidebar + instruments | Yes | Medium | Align presentation |
| Article/category | analysis | `/analysis`, `/analysis/:slug` | Yes | Medium | Add `/analysis/` alias or hub; restyle |
| `/accounts/*` | allauth | `/auth` | Partial | None | Brand templates; optional path alias |
| `/ai/*` | AI Pulse | — | Yes | — | Restyle only (keep) |
| `/companies/*` | Companies | — | Yes | — | Restyle only (keep) |
| `/resignation-risk/*` | Analyzer | — | Yes | — | Restyle wizard (keep logic) |
| `/payments/*` | Pro | — | Partial | — | Restyle; no fake payments |
| `/escape-plan/` | Escape | — | Yes | — | Restyle |
| `/search/` | Search | — | Yes | — | Restyle |
| `/submit` (ref) | salary-drop / contact | Write for us | Partial | — | Map footer link to existing flows |
| Methodology / privacy (ref footer) | editorial / privacy | Standards links | Yes | Medium | Align footer IA |

---

## SECTION 6 — Fake / stub / incomplete findings

| Finding | Location | Severity |
| ------- | -------- | -------- |
| Payments disabled when `razorpay_key_id` missing (“Payments coming soon”) | `templates/payments/pricing.html`, `escape_roadmap.html` | Expected env gap — **do not fake** |
| Hardcoded Career Index baseline fallback if no snapshots | `core/views.py` (commented) | Medium — prefer DB snapshots |
| No custom allauth templates → raw Django UI | Missing `templates/account/` | **P0 broken** |
| Newsletter “2 subscribers” weak social proof (live) | Live copy | Low |
| Layoff cards share stale relative timestamps (live observation) | Layoff radar | Medium data freshness UX |
| Article KEY TAKEAWAYS mid-word truncation (live) | Article detail | High content/CSS bug |
| Company logo initials placeholders | Companies directory | Acceptable fallback |
| Debug HTML prototypes in repo root | `debug_calc.html`, `debug_radar.html` | Debt — not production routes |
| Design-system Inter + rounded SaaS tokens diverge from reference | `static/css/design-system.css` | Migration target |

No systematic “Coming Soon” feature stubs found on core tools (CTC, layoff, analyzer, salary). Core tools are real.

---

## SECTION 7 — Design system audit (current)

### Typography
- Primary: Inter / system (`design-system.css`, legacy `style.min.css`)
- Mono: JetBrains Mono referenced
- No dedicated editorial serif display font in production tokens
- Heading scale marketing-heavy on home

### Color
- Dark default: near-black page, sky `--cr-accent`, danger red, success green
- Light theme: `#fafafa` page, `#0284c7` accent
- Reference accent is terracotta/muted red, not sky blue

### Components (CSS-level, not React)
- Buttons, cards, badges, inputs in `design-system.css`
- Many page-specific classes in `style-home`, `style-tools`, `style-companies`, `ai_pulse`
- Partial duplication / token drift across theme files

### Layout
- `--w-wide` ~1100px, medium/narrow reading widths
- Mobile: `@media (max-width: 768px)` + dedicated `mobile.css` + utility dock

**Verdict:** A design system **exists** but is fragmented and visually aligned to **dark SaaS**, not the **light editorial terminal** reference.

---

## SECTION 8 — Responsive gap analysis

| Breakpoint | CareerReality | Reference | Gap |
| ---------- | ------------- | --------- | --- |
| 1440 / 1280 | Two-column hero works | Two-column terminal | Need terminal grid |
| 1024 | Nav crowding / mega menu | Flat nav | Simplify nav |
| 768 | Dock + hamburger good | MENU | Restyle; keep dock utility |
| 430 / 390 / 375 | Generally strong | Card salary rows | Port card pattern for salary tables |

CareerReality mobile is **relatively strong**. Primary gap is **desktop visual language** and **auth**.

---

## SECTION 9 — Backend / data dependency analysis

| Feature | Frontend need | Backend capability | Gap | Proposal | Risk |
| ------- | ------------- | ------------------ | --- | -------- | ---- |
| Terminal salary table | Percentile bands | `SalarySubmission` + salary-reality content | Aggregation UX | Query aggregates; avoid hardcoding Lovable numbers | Low |
| CTC ledger | Live calc | Existing calculator JS/views | UI only | Reuse formulas | Low |
| Layoff stability scores | 0–100 score | `LayoffReport` status fields | May lack numeric stability | Derive heuristic score or show qualitative only | Medium |
| Auth ledger | Private entries | Submissions + UserProfile | Ownership linking | Optional migrate anonymous→user; privacy review | Medium |
| Analysis hub | List route | `Article` queryset | Thin | New view or category list template | Low |
| Payments | Checkout | Razorpay | Env keys | No fake checkout | Low (ops) |
| Index | Score display | `CareerRealityIndexSnapshot` | None | Use DB | Low |

**Database safety:** No destructive migrations planned for UI migration. Additive fields only if ledger ownership requires them.

---

## SECTION 10 — Technical risks

1. **CSS surface area (~10k LOC)** — token migration can regress dark theme / AdSense layout.
2. **allauth template override** — must not break Google OAuth or CSRF.
3. **Default theme flip (dark→light)** — SEO/OG `theme-color`, screenshots, returning users’ `localStorage` theme.
4. **Hardcoding Lovable sample salaries** — forbidden; must use CR data or clearly labeled editorial tables.
5. **Scope creep into fake “career coach” features** — out of product; reject.
6. **Payment buttons** — must remain honestly disabled without keys.
7. **Performance** — avoid shipping large unused font files; subset serif.
8. **Repo hygiene (from full codebase explore):** multiple root seed/migrate scripts appear to embed Supabase/Postgres connection strings — treat as a **security debt** outside UI migration scope; rotate credentials and purge from history separately. Do not expand that pattern during UX work.

---

## SECTION 11 — Completion baseline (pre-implementation)

Requirements counted from parity matrices (reference-aligned + critical CR quality), **n = 48** scored items:

| Category | Complete | Partial | Broken/Missing | Score method |
| -------- | -------- | ------- | -------------- | ------------ |
| Functional | 28 | 14 | 6 | Complete=1, Partial=0.5, Broken/Missing=0 |
| UI/Visual | 6 | 28 | 14 | same |
| UX/Interaction | 12 | 24 | 12 | same |
| Responsive | 22 | 18 | 8 | same |
| Accessibility | 14 | 20 | 14 | same |
| QA / verified states | 16 | 18 | 14 | same |

**Weighted overall (equal category weights):**

| Dimension | Completion % |
| --------- | ------------ |
| Functional | **72.9%** |
| UI / Visual | **41.7%** |
| UX / Interaction | **50.0%** |
| Responsive | **64.6%** |
| Accessibility | **50.0%** |
| QA | **52.1%** |
| **Overall (mean)** | **55.2%** |

These percentages are **audit baselines before migration work**, not aspirational targets.

---

## SECTION 12 — Already implemented / partial / missing / broken (executive)

### Already implemented (functional)
1. Homepage with live index + ticker + tools
2. CTC calculator (backend/logic)
3. Layoff radar + report
4. Salary reality content + submissions flywheel
5. Articles, AI Pulse, Companies, Risk analyzer, Search, Pro pricing shell

### Partially implemented
1. Visual language vs reference terminal
2. Nav IA (mega vs flat)
3. CTC interaction (form vs live ledger)
4. Salary explorer percentile UX
5. Layoff stability table presentation
6. Theme default / Night pattern
7. Pro dashboard / onboarding polish

### Missing
1. Branded member “private ledger” UX
2. Dedicated reference-style `/analysis` hub (optional alias)
3. Unified sharp editorial component kit
4. Shared Empty/Skeleton system
5. Contributor `/submit` surface matching reference footer story

### Broken
1. **Login / signup completely unstyled**
2. Article KEY TAKEAWAYS truncation (live)
3. Payments gated without keys (honest but conversion-broken)
4. Token drift / conflicting design systems
5. Emoji-heavy CTAs vs brand target

---

*Next documents:* `docs/TARGET_DESIGN_SYSTEM.md`, `docs/UI_UX_IMPLEMENTATION_PLAN.md`.
