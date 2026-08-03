"""
One-shot August 2026 production bootstrap: seed new content and refresh all articles.

    python manage.py bootstrap_august_2026
"""
import os
import subprocess
import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed August 2026 articles and refresh all published content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-seeds",
            action="store_true",
            help="Skip seed scripts (refresh only).",
        )

    def handle(self, *args, **options):
        base = settings.BASE_DIR
        env = os.environ.copy()

        if not options["skip_seeds"]:
            for script in ("seed_august_2026.py",):
                path = base / script
                if not path.exists():
                    self.stdout.write(self.style.WARNING(f"Missing {script}, skipping."))
                    continue
                self.stdout.write(f"Running {script}…")
                result = subprocess.run(
                    [sys.executable, str(path)],
                    cwd=str(base),
                    env=env,
                    capture_output=True,
                    text=True,
                )
                if result.stdout:
                    self.stdout.write(result.stdout)
                if result.returncode != 0:
                    self.stderr.write(result.stderr or f"{script} failed")
                    raise SystemExit(result.returncode)

        self.stdout.write("Refreshing published articles…")
        call_command(
            "refresh_published_articles",
            "--apply",
            "--report=docs/article_freshness_audit.md",
            stdout=self.stdout,
        )

        self.stdout.write("Refreshing career reality index…")
        call_command("refresh_career_index", stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS("August 2026 bootstrap complete."))
