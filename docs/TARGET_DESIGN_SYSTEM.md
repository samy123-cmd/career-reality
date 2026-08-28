# CareerReality — Target Design System

Derived from **Real Career Compass** (https://real-career-compass.lovable.app/) as UX/visual benchmark, adapted for the existing Django CareerReality product — not a pixel clone of Lovable chrome (no Lovable badge, no fake demo data).

**Principles:** premium · modern · clean · trustworthy · career-focused · highly readable · consistent · responsive · accessible  

**Avoid:** excessive gradients · glassmorphism · oversized rounded containers · random decoration · heavy multi-layer shadows · AI-slop purple SaaS · broadsheet-dense newspaper pastiche · emoji as UI.

---

## 1. Design principles

1. **Editorial terminal** — Feels like a financial desk for Indian tech compensation, not a startup marketing site.
2. **Evidence first** — Sample sizes, versions, and methodology stay visible near figures.
3. **Sharp and flat** — Hairline rules over cards; near-zero radius; almost no shadows.
4. **Typography does the branding** — Serif wordmark/headlines carry brand; body stays highly legible sans.
5. **One accent** — Terracotta/muted red for CTAs, risk, and active emphasis — not sky-blue SaaS chrome.
6. **Light primary, dark available** — Match reference: paper light as primary reading theme; Night mode preserved for power users (migrate stored preference carefully).
7. **Preserve product depth** — Companies, AI Pulse, Risk Analyzer, Pro remain first-class under the same tokens.

---

## 2. Color tokens (target)

Map into existing `--cr-*` / `--c-*` variables; extend rather than invent a second system.

| Token | Light (primary) | Dark (night) | Usage |
| ----- | --------------- | ------------ | ----- |
| `--cr-page` | `#F5F5F0` | `#0B0B0C` | Page background |
| `--cr-surface` | `#FFFFF8` / `#FFFFFF` | `#141416` | Panels |
| `--cr-ink` | `#141414` | `#F2F2F0` | Primary text |
| `--cr-ink-secondary` | `#5C5C56` | `#A3A39A` | Body secondary |
| `--cr-ink-muted` | `#8A8A82` | `#6E6E68` | Labels, meta |
| `--cr-border` | `rgba(20,20,20,0.12)` | `rgba(255,255,255,0.12)` | Hairlines |
| `--cr-accent` | `#C45C3E` | `#D4694A` | CTA, links emphasis, instrument labels |
| `--cr-accent-ink` | `#FFFFFF` | `#0B0B0C` | Text on accent |
| `--cr-danger` | `#B42318` | `#F97066` | Deductions, high risk |
| `--cr-success` | `#1B7F4E` | `#3DDC97` | Positive deltas |
| `--cr-warning` | `#B54708` | `#FDB022` | Elevated risk |
| `--cr-ticker-bg` | `#0B0B0C` | `#000000` | Live ticker |
| `--cr-ticker-fg` | `#F5F5F0` | `#F5F5F0` | Ticker text |
| `--cr-ledger-bg` | `#141414` | `#1A1A1C` | In-hand summary card |

**Do not** use purple-indigo gradients or sky `#0284c7` as primary brand accent going forward (may remain briefly as legacy alias during migration).

---

## 3. Typography

| Role | Family | Fallback | Notes |
| ---- | ------ | -------- | ----- |
| Display / brand / H1–H2 | Source Serif 4 or Fraunces (self-host) | `Georgia, "Times New Roman", serif` | Wordmark “CareerReality”, page titles |
| UI / body | Source Sans 3 or IBM Plex Sans (self-host) | `system-ui, sans-serif` | Nav, body, tables |
| Data / ticker | IBM Plex Mono or JetBrains Mono (already referenced) | `ui-monospace, monospace` | Salaries, ledger, ticker |

**Scale (desktop):**

| Token | Size | Weight | Line-height |
| ----- | ---- | ------ | ----------- |
| `--text-xs` | 11–12px | 600 | 1.3 | labels, small caps meta |
| `--text-sm` | 13–14px | 400–500 | 1.45 | secondary |
| `--text-md` | 16px | 400 | 1.6 | body |
| `--text-lg` | 18–20px | 400 | 1.5 | lead |
| `--text-xl` | 28–32px | 600 serif | 1.15 | section |
| `--text-2xl` | 40–48px | 600–700 serif | 1.08 | page title |
| `--text-hero` | 48–56px | 600 serif | 1.05 | terminal headline |
| `--text-metric` | 56–72px | 500–600 | 1 | index score |

Letter-spacing: labels `0.08–0.14em` uppercase; headlines slight negative tracking.

---

## 4. Spacing, layout, radius, shadow

| Token | Value |
| ----- | ----- |
| Space scale | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 |
| `--w-terminal` | 1180–1240px |
| `--w-reading` | 680–720px |
| Gutter | 16px mobile / 24–32px desktop |
| `--radius-none` | 0 |
| `--radius-sm` | 2px |
| `--radius-md` | 4px |
| `--radius-lg` | 6px (rare) |
| Shadows | default `none`; optional `--shadow-sm: 0 1px 2px rgba(0,0,0,.06)` |

**Grid:** Terminal home = ~32% index column / ~68% main on ≥1024px; stack below.

---

## 5. Motion

Intentional, sparse (2–3 patterns sitewide):

1. Ticker continuous translate (respect `prefers-reduced-motion`: pause).
2. Underline/active nav transition ~150ms.
3. Meter fill width transition ~300ms ease-out on index.

No bounce, no parallax, no glow pulses on CTAs.

---

## 6. Component specifications

### Button
- **Primary:** `--cr-accent` fill, `--cr-accent-ink` text, radius 2px, uppercase optional small tracking OR sentence case per reference (“Create account”).
- **Ghost:** 1px `--cr-ink` border, transparent fill.
- **Utility:** compact outline (“Night”, “Menu”).
- Height ~40–44px; focus ring 2px accent offset.

### Input / Select / Textarea
- Hairline border, 4px radius max, quiet focus ring.
- Labels above, muted helper below.

### Range slider (CTC)
- Track muted; fill accent; circular thumb accent.
- Live value adjacent; recalculate on `input`.

### Card
- Default: **no card**. Prefer section + hairline.
- Allowed when interactive cluster (pricing, company result) — still low radius, weak border, no lift hover.

### Badge / risk chip
- Small caps; HIGH/ELEVATED use accent/danger backgrounds at low opacity; not pill-full rounded.

### Tabs
- Text tabs with underline active (match nav).

### Modal / Dialog
- Flat surface, sharp edge, focus trap, Escape closes; reuse for auth messaging if needed.

### Navigation
- Desktop: wordmark + 5 primary links (Terminal, Salary explorer, CTC decoder, Layoff radar, Analysis) + theme + account.
- Secondary product areas (Companies, AI Pulse, Risk Analyzer, Pro) via compact overflow “More” or footer + existing mobile dock — **do not delete**.
- Mobile: logo | Night | Menu; keep utility dock for tools.

### Data table
- No vertical rules; horizontal hairlines; numeric columns tabular nums right-aligned; caption for units (₹ LPA).

### Progress / meter
- Thin track; fill by severity; number + qualitative label.

### Ticker
- Full-bleed black bar; mono; green/red deltas; always paired with non-color cue if possible.

### Empty / Loading / Error
- Empty: one sentence + one CTA (e.g. Drop a salary).
- Loading: skeleton hairlines matching table rows.
- Error: inline message + retry; never silent fail.

### Avatar
- Rare; initials square 2px radius for companies (keep).

---

## 7. Iconography

- Prefer inline SVG stroke icons (1.5px), 16–20px.
- Remove emoji from primary CTAs and mega-nav during migration.
- No illustration packs required for parity.

---

## 8. Accessibility baseline

- Contrast ≥ 4.5:1 body on page; accent-on-paper verified for CTAs (terracotta may need darker `#A84830` for small text).
- Visible `:focus-visible` on all controls.
- Skip link to `#main`.
- Dialogs: `role="dialog"`, labelled.
- Ticker: `aria-hidden` decorative duplicate if duplicated DOM for marquee; announce summary elsewhere.
- Prefer reduced motion.

---

## 9. Implementation mapping (repo)

| Action | File(s) |
| ------ | ------- |
| Extend tokens | `static/css/design-system.css`, `theme-light.css`, `theme-premium-dark.css` |
| Self-host fonts | `static/fonts/` + `partials/meta.html` |
| Shell | `templates/partials/header.html`, `footer.html`, `base.html` |
| Home terminal | `templates/core/home.html`, `static/css/style-home.css` |
| Tools | `style-tools.css`, calculator + layoff templates |
| Auth | new `templates/account/*.html` |
| Mobile | `static/css/mobile.css`, utility dock |

**Rule:** extend Tailwind-less CSS variable system already in use — do **not** add another UI framework.

---

## 10. Theme default policy

1. Ship **light editorial** as default `data-theme` for new sessions (align reference).
2. Honor existing `localStorage['cr-theme']` when set.
3. Night toggle remains first-class.
4. Update `theme-color` meta per theme.

---

## 11. Content & voice (UI copy)

- Direct, evidence-backed, slightly sharp (“Stop guessing what the market pays.”).
- Prefer “CTC decoder”, “Salary explorer”, “Layoff radar”, “Terminal” naming in primary nav (can keep SEO titles on pages).
- Never invent Lovable’s hardcoded band numbers; show CR’s real aggregates or existing editorial tables with sources.

---

*Companion docs:* `UI_UX_MIGRATION_AUDIT.md`, `UI_UX_IMPLEMENTATION_PLAN.md`.
