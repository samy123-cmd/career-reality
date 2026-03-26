from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs the production freshness pipeline: ingest, refresh, audit, and warm caches."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fetch-limit",
            type=int,
            default=12,
            help="Maximum items per feed for AI ingest run.",
        )
        parser.add_argument(
            "--commit-refresh",
            action="store_true",
            help="Apply article refresh changes with --commit.",
        )
        parser.add_argument(
            "--strict-freshness",
            action="store_true",
            help="Fail if freshness audit breaches allowed stale thresholds.",
        )
        parser.add_argument(
            "--warm-cache",
            action="store_true",
            help="Warm key page caches at the end of the pipeline.",
        )

    def handle(self, *args, **options):
        fetch_limit = options["fetch_limit"]
        commit_refresh = options["commit_refresh"]
        strict_freshness = options["strict_freshness"]
        warm_cache = options["warm_cache"]

        self.stdout.write(self.style.NOTICE("Starting production maintenance pipeline"))

        self.stdout.write("Step 1/4: Fetch AI news")
        call_command("fetch_ai_news", auto_publish=True, limit=fetch_limit)

        self.stdout.write("Step 2/4: Refresh core content")
        if commit_refresh:
            call_command("refresh_content", commit=True)
        else:
            self.stdout.write(self.style.WARNING("Running refresh_content in dry-run mode (no --commit)."))
            call_command("refresh_content")

        self.stdout.write("Step 3/4: Freshness audit")
        if strict_freshness:
            call_command("audit_freshness", strict=True)
        else:
            call_command("audit_freshness")

        self.stdout.write("Step 4/4: Query budget profile")
        if strict_freshness:
            call_command("profile_page_queries", strict=True)
        else:
            call_command("profile_page_queries")

        if warm_cache:
            self.stdout.write("Optional: Warm caches")
            call_command("warm_core_caches")

        self.stdout.write(self.style.SUCCESS("Production maintenance pipeline completed."))
