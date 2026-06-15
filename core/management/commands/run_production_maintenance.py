"""
Production maintenance orchestrator — invoked by Vercel cron at /internal/cron/freshness/.

Handles:
- Optional AI news fetch (lightweight, bounded)
- Sitemap cache rebuild
- Redis page-cache warming for critical paths
"""

from core.sitemaps import SITEMAPS
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.cache_utils import (
    build_and_cache_sitemap,
    invalidate_sitemap_cache,
    warm_page_cache,
)


class Command(BaseCommand):
    help = "Run scheduled production maintenance: fetch, cache rebuild, page warm."

    def add_arguments(self, parser):
        parser.add_argument("--fetch-limit", type=int, default=0)
        parser.add_argument("--commit-refresh", action="store_true", default=False)
        parser.add_argument("--strict-freshness", action="store_true", default=False)
        parser.add_argument("--warm-cache", action="store_true", default=True)
        parser.add_argument("--article-warm-limit", type=int, default=15)
        parser.add_argument(
            "--refresh-articles",
            action="store_true",
            default=False,
            help="Run refresh_published_articles --apply after cache warm.",
        )

    def handle(self, *args, **options):
        fetch_limit = options["fetch_limit"]
        warm_cache = options["warm_cache"]
        article_warm_limit = options["article_warm_limit"]

        if fetch_limit > 0:
            self.stdout.write(f"Fetching up to {fetch_limit} AI news items…")
            try:
                call_command("fetch_ai_news", limit=fetch_limit, stdout=self.stdout)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"AI fetch skipped: {exc}"))

        if options["commit_refresh"]:
            self.stdout.write("Refreshing career reality index…")
            try:
                call_command("refresh_career_index", stdout=self.stdout)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"Index refresh skipped: {exc}"))

        # Always rebuild sitemap cache during maintenance (cheap vs 5s live generation).
        self.stdout.write("Rebuilding sitemap cache…")
        invalidate_sitemap_cache()

        def _generate() -> bytes:
            from django.test import RequestFactory

            request = RequestFactory().get("/sitemap.xml")
            response = django_sitemap(request, sitemaps=SITEMAPS)
            if hasattr(response, "render"):
                response.render()
            return response.content

        build_and_cache_sitemap(_generate)
        self.stdout.write(self.style.SUCCESS("Sitemap cache rebuilt."))

        if warm_cache:
            self.stdout.write("Warming page cache…")
            summary = warm_page_cache(article_limit=article_warm_limit, stdout=self.stdout)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Warmed {summary['warmed']}/{summary['paths_total']} paths; "
                    f"nav categories={summary['nav_categories']}"
                )
            )
            if summary["failed"]:
                self.stdout.write(self.style.WARNING(f"Warm failures: {summary['failed']}"))

        if options["strict_freshness"]:
            self.stdout.write("Running strict freshness preflight…")
            call_command("preflight_release", "--strict", "--check-freshness", stdout=self.stdout)

        if options.get("refresh_articles"):
            self.stdout.write("Refreshing published articles…")
            try:
                call_command(
                    "refresh_published_articles",
                    "--apply",
                    "--report=docs/article_freshness_audit.md",
                    stdout=self.stdout,
                )
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"Article refresh skipped: {exc}"))

        self.stdout.write(self.style.SUCCESS("Maintenance complete."))
