---
name: publish-career-article
description: Publish or expand Career Reality long-form articles with the strict Article field structure, SEO meta, citations, and quality bars. Use when seeding articles, expanding thin content, or fixing credibility gaps.
paths:
  - "content/**"
  - "seed_*.py"
  - "publish_*.py"
  - "expand_*.py"
  - "templates/content/**"
  - "docs/*article*"
  - "docs/*credibility*"
---

# Publish / Expand Career Articles

## Article model contract (`content.models.Article`)

Every published article must fill these editorial fields (HTML paragraphs OK):

| Field | Purpose |
|-------|---------|
| `target_persona` | Who this is for |
| `who_should_avoid` | Trust signal — who should NOT pursue this |
| `common_expectation` | The myth |
| `actual_reality` | The truth |
| `salary_reality` | Real ranges/tables — role × YOE × city when possible |
| `stuck_point` | Where people plateau |
| `verdict` | Honest conclusion |
| `meta_title` | ≤ 60 chars |
| `meta_description` | ≤ 160 chars, clear search intent |
| `last_reality_check` | Date of last factual review |
| `status` | `published` only when ready |
| `author` / `category` | Real author with LinkedIn; indexable category |

## Quality bars (from audits / credibility work)

- Prefer **≥ ~1800–2000+ words** for new long-form pieces (see August 2026 seeds).
- **≥ 2–3 external citations** (gov/report/AmbitionBox/Glassdoor/Naukri — claim-level links in body).
- Internal links to related tools (`/salary-reality/`, `/salary-calculator/`, `/companies/`, `/ai/`) and sibling articles.
- Salary section must not be thin — expand `salary_reality` with concrete LPA numbers.
- No duplicated safety-pad paragraphs; strip with `content.boilerplate.strip_safety_pad`.
- Update `docs/article_freshness_audit.md` / upgrade sheets when doing batch refreshes.

## Preferred workflow

1. Follow patterns in `seed_august_2026.py` / `seed_july_2026.py` (helpers `_p`, `_h3`, `_section`).
2. Use existing `Author` + `Category` (avoid creating thin categories — see `seo-gsc-hygiene`).
3. Check slug is not a redirect loser in `content/seo_redirects.py`.
4. After DB write, run quality commands when available:
   - `python manage.py quality_audit`
   - `python manage.py seo_audit`
   - `python manage.py generate_upgrade_sheet`
5. Bust/warm cache if pages are live (`cache-and-deploy`).

## Voice

Anti-hype. Quantify. Call out certificate theatre and API-wrapper “AI” roles when relevant. India market framing (LPA, GCCs, IT services, metros).

## Do not

- Ship drafts as `published` without sources and salary substance.
- Create competing slugs for the same intent — canonicalize instead.
- Inject generic padding to inflate word count.
