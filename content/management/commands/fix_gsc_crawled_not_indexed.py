"""
Apply GSC indexing remediation to crawled-but-not-indexed URLs.

Adds external source blocks, market/salary refresh markers, bumps
last_reality_check, and busts page + sitemap cache for affected slugs.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.gsc_indexing_fixes import (
    GSC_CRAWLED_NOT_INDEXED_ARTICLE_SLUGS,
    apply_gsc_indexing_fixes,
)
from content.models import Article
from content.seo_redirects import ARTICLE_SITEMAP_EXCLUDE_SLUGS
from core.cache_utils import invalidate_cached_pages, invalidate_sitemap_cache


class Command(BaseCommand):
    help = (
        "Fix GSC 'Crawled - currently not indexed' articles: external sources, "
        "freshness markers, and cache bust."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report changes without saving.",
        )
        parser.add_argument(
            "--slug",
            default="",
            help="Fix a single slug instead of the full GSC batch.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        slugs = (options["slug"],) if options["slug"] else GSC_CRAWLED_NOT_INDEXED_ARTICLE_SLUGS

        articles = list(
            Article.objects.filter(status="published", slug__in=slugs)
            .exclude(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)
            .select_related("category")
            .order_by("slug")
        )
        if not articles:
            self.stdout.write(self.style.WARNING("No matching published articles found."))
            return

        updated = 0
        paths = []
        for article in articles:
            changes = apply_gsc_indexing_fixes(article)
            if not changes:
                self.stdout.write(f"{article.slug}: already up to date")
                continue
            self.stdout.write(f"{article.slug}: {', '.join(changes)}")
            paths.append(f"/article/{article.slug}/")
            if dry_run:
                continue
            article.save(
                update_fields=[
                    "actual_reality",
                    "salary_reality",
                    "meta_title",
                    "meta_description",
                    "last_reality_check",
                    "updated_at",
                ]
            )
            updated += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run — no database or cache writes."))
            return

        paths.extend(["/sitemap.xml", "/"])
        deleted = invalidate_cached_pages(paths)
        invalidate_sitemap_cache()
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} article(s); invalidated {deleted} cache keys at "
                f"{timezone.now().isoformat()}."
            )
        )
