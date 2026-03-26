from django.core.management.base import BaseCommand
from django.test import Client

from ainews.models import AINewsItem
from content.models import Article, Category


class Command(BaseCommand):
    help = "Warms key page caches to reduce cold-start latency after deploys."

    def handle(self, *args, **options):
        client = Client()

        paths = [
            "/",
            "/ai/",
            "/career-reality-index/",
            "/salary-calculator/",
        ]

        first_article = Article.objects.filter(status="published").order_by("-published_at").first()
        if first_article:
            paths.append(first_article.get_absolute_url())

        first_category = Category.objects.order_by("order", "name").first()
        if first_category:
            paths.append(first_category.get_absolute_url())

        first_ai = AINewsItem.objects.filter(status="published").order_by("-published_at").first()
        if first_ai:
            paths.append(first_ai.get_absolute_url())

        self.stdout.write(self.style.NOTICE("Warming core caches"))
        for path in paths:
            response = client.get(path)
            status = response.status_code
            if status == 200:
                self.stdout.write(self.style.SUCCESS(f"✓ warmed {path}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ {path} returned {status}"))

        self.stdout.write(self.style.SUCCESS("Cache warming run complete."))
