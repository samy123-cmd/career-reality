from django.core.management.base import BaseCommand

from core.cache_utils import warm_page_cache


class Command(BaseCommand):
    help = "Warm Redis page cache for critical public URLs."

    def add_arguments(self, parser):
        parser.add_argument("--article-limit", type=int, default=15)

    def handle(self, *args, **options):
        summary = warm_page_cache(
            article_limit=options["article_limit"],
            stdout=self.stdout,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Done: warmed {summary['warmed']}/{summary['paths_total']} paths."
            )
        )
