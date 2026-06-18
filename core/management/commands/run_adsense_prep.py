"""
One-shot AdSense prep: prune AI noise, expand thin articles, refresh metadata.

    python manage.py run_adsense_prep              # dry run
    python manage.py run_adsense_prep --apply      # production
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prune AI Pulse noise, expand thin articles, refresh published content for AdSense."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist all changes. Default is dry run.",
        )
        parser.add_argument(
            "--skip-ai-prune",
            action="store_true",
            help="Skip demoting non-IT-impact AI news.",
        )

    def handle(self, *args, **options):
        apply_flag = ["--apply"] if options["apply"] else []
        dry = not options["apply"]

        if not options["skip_ai_prune"]:
            self.stdout.write(self.style.NOTICE("Step 1: Prune non-IT-impact AI news…"))
            call_command("prune_ai_news", *apply_flag, stdout=self.stdout)

        self.stdout.write(self.style.NOTICE("Step 2: Expand thin articles (core + priority)…"))
        call_command("expand_core_articles", *apply_flag, stdout=self.stdout)

        if options["apply"]:
            self.stdout.write(self.style.NOTICE("Step 3: Refresh market blocks + sources…"))
            call_command(
                "refresh_published_articles",
                "--apply",
                "--report=docs/article_freshness_audit.md",
                stdout=self.stdout,
            )
            self.stdout.write(self.style.NOTICE("Step 4: Refresh career index…"))
            call_command("refresh_career_index", stdout=self.stdout)

        self.stdout.write(self.style.NOTICE("Step 5: Quality audit…"))
        call_command(
            "quality_audit",
            *(["--strict", "--max-low-word", "0"] if options["apply"] else []),
            stdout=self.stdout,
        )

        if dry:
            self.stdout.write(self.style.WARNING("Dry run complete — pass --apply to persist."))
        else:
            self.stdout.write(self.style.SUCCESS("AdSense prep complete. Warm cache via cron, then resubmit AdSense."))
