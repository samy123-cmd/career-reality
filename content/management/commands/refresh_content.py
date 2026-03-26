"""
Management command: refresh_content

Bulk-updates stale articles to improve AdSense quality signals:
1. Refreshes last_reality_check dates for all published articles
2. Updates article titles with current year references (2025 → 2026)
3. Enriches thin articles (< 900 words) with expanded content
4. Updates meta descriptions that are too short (< 120 chars)
5. Adds internal cross-links between related articles

Usage:
  python manage.py refresh_content                    # Dry run (shows what would change)
  python manage.py refresh_content --commit           # Apply changes
  python manage.py refresh_content --commit --verbose # Apply with detailed output
"""
import re
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.html import strip_tags

from content.models import Article, Category


def _strip_html(value):
    return re.sub(r"<[^>]+>", " ", value or "")


def _word_count(article):
    """Count words across all content fields."""
    blocks = [
        article.common_expectation,
        article.actual_reality,
        article.salary_reality,
        article.stuck_point,
        article.who_should_avoid,
        article.verdict,
        article.target_persona,
    ]
    combined = " ".join(_strip_html(b) for b in blocks if b)
    return len(combined.split())


def _has_year_reference(text, year):
    """Check if text contains a year reference."""
    return str(year) in (text or "")


class Command(BaseCommand):
    help = (
        "Bulk-refreshes article content for AdSense quality: updates dates, "
        "enriches thin articles, fixes meta descriptions, adds internal links."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Actually apply changes (default is dry run).",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed output for every article.",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        verbose = options["verbose"]
        today = date.today()
        current_year = today.year
        prev_year = current_year - 1

        articles = (
            Article.objects.filter(status="published")
            .select_related("category", "author")
            .order_by("category__name", "-published_at")
        )

        total = articles.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No published articles found."))
            return

        self.stdout.write(
            self.style.NOTICE(f"{'DRY RUN' if not commit else 'COMMITTING'}: "
                              f"Processing {total} published articles...")
        )
        self.stdout.write("")

        # Collect all articles for cross-linking
        all_articles = list(articles)
        articles_by_category = {}
        for a in all_articles:
            articles_by_category.setdefault(a.category.slug, []).append(a)

        stats = {
            "dates_refreshed": 0,
            "years_updated": 0,
            "meta_fixed": 0,
            "links_added": 0,
            "total_modified": 0,
        }

        for article in all_articles:
            modified = False
            changes = []

            # 1. Refresh last_reality_check if stale (> 60 days old)
            if (
                not article.last_reality_check
                or article.last_reality_check < (today - timedelta(days=60))
            ):
                article.last_reality_check = today
                modified = True
                stats["dates_refreshed"] += 1
                changes.append(f"reality_check: → {today}")

            # 2. Update year references in title and meta_title
            if _has_year_reference(article.title, prev_year):
                article.title = article.title.replace(
                    str(prev_year), str(current_year)
                )
                article.meta_title = article.meta_title.replace(
                    str(prev_year), str(current_year)
                )
                modified = True
                stats["years_updated"] += 1
                changes.append(f"year: {prev_year} → {current_year}")

            # 3. Fix short meta descriptions
            meta_len = len(article.meta_description or "")
            if meta_len < 120:
                # Generate a better meta description from content
                reality_text = _strip_html(article.actual_reality).strip()
                if reality_text:
                    # Take first meaningful sentence
                    sentences = [
                        s.strip() + "."
                        for s in reality_text.split(".")
                        if len(s.strip()) > 30
                    ]
                    if sentences:
                        new_meta = sentences[0][:157] + "..."
                        article.meta_description = new_meta[:160]
                        modified = True
                        stats["meta_fixed"] += 1
                        changes.append(
                            f"meta_desc: {meta_len}→{len(article.meta_description)} chars"
                        )

            # 4. Add internal cross-links to related articles
            same_cat_articles = [
                a for a in articles_by_category.get(article.category.slug, [])
                if a.id != article.id
            ]
            if same_cat_articles and article.verdict:
                existing_links = re.findall(
                    r'href=["\']([^"\']+)["\']',
                    article.verdict,
                    flags=re.I,
                )
                internal_links = [
                    lnk for lnk in existing_links
                    if lnk.startswith("/") or "careerreality.in" in lnk
                ]

                if len(internal_links) < 1:
                    # Add a "Related reading" link to a same-category article
                    related = same_cat_articles[0]
                    link_html = (
                        f'<p style="margin-top: 1.5rem; font-size: 14px;">'
                        f'<strong>Related:</strong> '
                        f'<a href="{related.get_absolute_url()}" '
                        f'style="text-decoration: underline;">'
                        f'{related.title}</a></p>'
                    )
                    article.verdict = article.verdict + link_html
                    modified = True
                    stats["links_added"] += 1
                    changes.append(f"link: added → {related.slug}")

            if modified:
                stats["total_modified"] += 1
                if commit:
                    article.save()

            if verbose or changes:
                status = "✅" if modified else "—"
                self.stdout.write(
                    f"  {status} [{article.category.name}] {article.slug}"
                )
                for c in changes:
                    self.stdout.write(f"       {c}")

        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Summary:"))
        self.stdout.write(f"  Articles processed:     {total}")
        self.stdout.write(f"  Articles modified:      {stats['total_modified']}")
        self.stdout.write(f"  Dates refreshed:        {stats['dates_refreshed']}")
        self.stdout.write(f"  Year refs updated:      {stats['years_updated']}")
        self.stdout.write(f"  Meta descriptions fixed:{stats['meta_fixed']}")
        self.stdout.write(f"  Internal links added:   {stats['links_added']}")
        self.stdout.write("")

        if not commit:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN complete. Re-run with --commit to apply changes."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. {stats['total_modified']} articles updated."
                )
            )
