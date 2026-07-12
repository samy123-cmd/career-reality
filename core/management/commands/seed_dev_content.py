"""
One-shot local dev bootstrap: articles, AI Pulse, and company intelligence.

    python manage.py seed_dev_content
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed articles, AI Pulse, and company intelligence for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-articles",
            action="store_true",
            help="Skip article/AI Pulse bootstrap.",
        )
        parser.add_argument(
            "--skip-companies",
            action="store_true",
            help="Skip company intelligence seed.",
        )

    def handle(self, *args, **options):
        if not options["skip_articles"]:
            self.stdout.write("Bootstrapping July 2026 articles and AI Pulse…")
            call_command("bootstrap_july_2026")

        if not options["skip_companies"]:
            self.stdout.write("Seeding company intelligence…")
            call_command("seed_company_intelligence")

        self.stdout.write(self.style.SUCCESS("Local dev content seed complete."))
