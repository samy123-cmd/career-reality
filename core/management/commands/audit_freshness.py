from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ainews.models import AINewsItem
from content.models import Article


class Command(BaseCommand):
    help = "Audit freshness of published content and optionally fail release checks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--article-max-age-days",
            type=int,
            default=60,
            help="Maximum allowed age (days) since last_reality_check for published articles.",
        )
        parser.add_argument(
            "--ai-max-age-days",
            type=int,
            default=21,
            help="Maximum allowed age (days) since verification/review for published AI news.",
        )
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Exit with non-zero code if stale percentage exceeds threshold.",
        )
        parser.add_argument(
            "--max-stale-percent",
            type=float,
            default=20.0,
            help="Maximum stale percentage allowed in strict mode (default: 20).",
        )

    def handle(self, *args, **options):
        article_max_age_days = options["article_max_age_days"]
        ai_max_age_days = options["ai_max_age_days"]
        strict = options["strict"]
        max_stale_percent = options["max_stale_percent"]

        now = timezone.now()
        today = timezone.localdate()

        article_cutoff = today - timedelta(days=article_max_age_days)
        ai_cutoff = now - timedelta(days=ai_max_age_days)

        published_articles = Article.objects.filter(status="published")
        stale_articles = published_articles.filter(last_reality_check__lt=article_cutoff)
        unknown_article_dates = published_articles.filter(last_reality_check__isnull=True)

        published_ai = AINewsItem.objects.filter(status="published")
        stale_ai = []
        for item in published_ai.only("id", "title", "last_verified_at", "reviewed_at", "published_at"):
            effective = item.last_verified_at or item.reviewed_at or item.published_at
            if effective and effective < ai_cutoff:
                stale_ai.append(item)

        article_total = published_articles.count()
        article_stale_count = stale_articles.count() + unknown_article_dates.count()
        article_stale_pct = (article_stale_count / article_total * 100) if article_total else 0.0

        ai_total = published_ai.count()
        ai_stale_count = len(stale_ai)
        ai_stale_pct = (ai_stale_count / ai_total * 100) if ai_total else 0.0

        self.stdout.write(self.style.NOTICE("Freshness audit results"))
        self.stdout.write(
            f"  Articles: {article_stale_count}/{article_total} stale or missing checks "
            f"({article_stale_pct:.1f}%) | threshold={article_max_age_days}d"
        )
        self.stdout.write(
            f"  AI News:  {ai_stale_count}/{ai_total} stale "
            f"({ai_stale_pct:.1f}%) | threshold={ai_max_age_days}d"
        )

        if strict and (article_stale_pct > max_stale_percent or ai_stale_pct > max_stale_percent):
            raise CommandError(
                "Freshness gate failed: stale content percentage exceeds configured threshold. "
                f"articles={article_stale_pct:.1f}% ai={ai_stale_pct:.1f}% max={max_stale_percent:.1f}%"
            )

        if article_stale_count or ai_stale_count:
            self.stdout.write(self.style.WARNING("Stale content detected. Run refresh workflows before release."))
        else:
            self.stdout.write(self.style.SUCCESS("All published content passes freshness thresholds."))
