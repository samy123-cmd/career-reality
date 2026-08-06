---
name: frontend-cr-design
description: Career Reality frontend design system — CSS variables, templates, mobile shell (utility dock / more-sheet), themes, and editorial layout patterns. Use for UI, homepage, footer, tools hub, or mobile UX work.
paths:
  - "templates/**"
  - "static/css/**"
  - "static/js/**"
---

# Frontend — Career Reality Design

## Brand / layout intent

Editorial product, not a SaaS dashboard. Homepage should read as one editorial composition (recent work: simplify homepage, slim ticker, minimal chrome). Tools hub is a premium editorial panel, not a card farm.

## Design tokens

Primary file: `static/css/design-system.css` (`--cr-*` colors, spacing, radii).

Also:

- `static/css/mobile.css` — touch-first mobile layer
- `static/css/style-home.css`, `style-tools.css`, `style-core.css`, `style-companies.css`
- Theme files: `theme-dark-contrast.css`, `theme-light.css`, `theme-premium-dark.css`
- Theme boot: `static/js/theme.js` + inline theme in `templates/partials/meta.html`

Default document theme is dark (`theme-dark` on `<html>` in `base.html`).

## Shell / mobile patterns (preserve these)

- Header: `templates/partials/header.html`
- Footer: `templates/partials/footer.html` (multi-column; avoid more-sheet leak into footer)
- Utility dock: `templates/partials/utility_dock.html`
- Mobile more sheet: `templates/partials/mobile_more_sheet.html` (swipe-to-close, overlay)
- Base layout: `templates/base.html` — **no global `main.container`**; each template chooses wide/med/reading width

## Implementation rules for this repo

- Prefer existing `cr-*` / `dock-*` / `more-sheet-*` classes over inventing a parallel system.
- After CSS/template changes that must hit production, follow `cache-and-deploy` (Redis prefix or path invalidation).
- Keep drawers/sheets from leaking on desktop; past bugs: broken tool hub CSS on mobile, footer rendering on Vercel, more-sheet leak.
- Touch targets and swipe-to-close matter more than decorative motion.

## When redesigning

Match established editorial density and India career product context. Do not replace the design system with a generic purple/Inter landing template unless explicitly asked to rebrand.
