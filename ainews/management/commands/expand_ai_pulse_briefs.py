from django.core.management.base import BaseCommand

from ainews.expansions_gsc_aug2026 import MIN_INDEXABLE_BODY_WORDS, apply_expansions
from core.cache_utils import invalidate_cached_pages, invalidate_sitemap_cache


class Command(BaseCommand):
    help = (
        "Expand thin AI Pulse briefs that trigger GSC "
        "'Crawled - currently not indexed' validation failures."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show word-count deltas without writing to the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        results = apply_expansions(commit=not dry_run)
        if not results:
            self.stdout.write(self.style.WARNING("No matching AI Pulse rows found."))
            return

        for slug, old_words, new_words in results:
            status = "ok" if new_words >= MIN_INDEXABLE_BODY_WORDS else "still-thin"
            self.stdout.write(
                f"{slug}: {old_words} -> {new_words} words [{status}]"
            )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run only — no DB or cache writes."))
            return

        paths = ["/ai/"] + [f"/ai/{slug}/" for slug, _, _ in results]
        paths += [
            "/ai/tag/career-impact/",
            "/ai/tag/industry-news/",
            "/ai/tag/model-release/",
            "/ai/tag/benchmark/",
        ]
        deleted = invalidate_cached_pages(paths)
        invalidate_sitemap_cache()
        self.stdout.write(
            self.style.SUCCESS(
                f"Expanded {len(results)} briefs; invalidated {deleted} page cache keys."
            )
        )
