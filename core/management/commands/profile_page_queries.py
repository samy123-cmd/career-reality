import time

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.test import Client


class Command(BaseCommand):
    help = "Profiles query count and latency for key public pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail with non-zero exit code if page exceeds query budget or non-200 status.",
        )
        parser.add_argument(
            "--query-budget",
            type=int,
            default=25,
            help="Maximum query count allowed per page in strict mode (default: 25).",
        )

    def handle(self, *args, **options):
        strict = options["strict"]
        query_budget = options["query_budget"]

        client = Client()
        paths = [
            "/",
            "/ai/",
            "/career-reality-index/",
            "/salary-calculator/",
        ]

        violations = []

        self.stdout.write(self.style.NOTICE("Profiling page query budgets"))
        for path in paths:
            connection.force_debug_cursor = True
            start = time.perf_counter()
            with CaptureQueriesContext(connection) as query_context:
                response = client.get(path)
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            query_count = len(query_context)

            line = f"{path} | status={response.status_code} | queries={query_count} | elapsed_ms={elapsed_ms}"
            if response.status_code != 200 or query_count > query_budget:
                violations.append(line)
                self.stdout.write(self.style.WARNING(f"⚠ {line}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ {line}"))

        if violations and strict:
            raise CommandError(
                "Page query profiling failed strict budget checks:\n" + "\n".join(violations)
            )

        if violations:
            self.stdout.write(self.style.WARNING("Completed with warnings."))
        else:
            self.stdout.write(self.style.SUCCESS("All pages are within query budget."))
