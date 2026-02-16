# AdSense Re-Review Checklist
Date: February 16, 2026
Site: `https://www.careerreality.in`

## 1. Pre-Submit Technical Checks
- Run: `python manage.py check`
- Run: `python manage.py quality_audit`
- Confirm `robots.txt` is reachable at `/robots.txt` and includes sitemap URL.
- Confirm `/sitemap.xml` loads and includes article, category, and static URLs.
- Confirm noindex pages are not in sitemap and include `<meta name="robots" content="noindex, follow">`.

## 2. Trust and Policy Pages (Manual Spot Check)
- Home: `/`
- About: `/about/`
- Editorial standards: `/editorial/`
- Contact: `/contact/`
- Privacy policy: `/privacy-policy/`
- Terms: `/terms/`
- Verify each page renders correctly on mobile and desktop.

## 3. Content Quality Baseline
- Minimum targets before submission:
- At least 30 published long-form articles (already satisfied).
- Each article includes:
- `What Changed` block with dated entries.
- `Sources` block with external references and checked date.
- At least 3 contextual internal links in the rendered article body.
- Last reality check not older than 180 days.

## 4. Search Console Actions (Day 0 After Deploy)
- Submit/refresh sitemap: `https://www.careerreality.in/sitemap.xml`
- Use URL Inspection and request indexing for:
- `/`
- `/about/`
- `/editorial/`
- `/privacy-policy/`
- Top 10 updated article URLs
- Confirm no manual actions and no security issues in Search Console.

## 5. AdSense Re-Application Timing
- Wait at least 7-14 days after indexing requests so Google can recrawl updated templates.
- Re-apply only after:
- Search Console shows fresh crawl/index dates for core trust pages.
- Quality audit has no freshness failures and internal link findings are addressed.

## 6. Ongoing Weekly Routine
- Weekly:
- Run `python manage.py quality_audit`
- Update at least 2 existing articles with dated log entries.
- Add contextual internal links for any article flagged by audit.
- Monthly:
- Refresh salary methodology and source checked dates on `/salary-reality/`.
- Publish at least 2 new original long-form articles.
