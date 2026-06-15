from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import timedelta
import os

from ainews.models import AINewsItem
from content.models import Article


class Command(BaseCommand):
    help = "Validate production-critical settings before release."

    def add_arguments(self, parser):
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail with non-zero exit code if any blocking issue is found.",
        )
        parser.add_argument(
            "--check-freshness",
            action="store_true",
            help="Validate stale-content ratios for published articles and AI news.",
        )
        parser.add_argument(
            "--article-max-age-days",
            type=int,
            default=60,
            help="Staleness threshold for published articles (last_reality_check).",
        )
        parser.add_argument(
            "--ai-max-age-days",
            type=int,
            default=21,
            help="Staleness threshold for published AI news (verification/review date).",
        )
        parser.add_argument(
            "--max-stale-percent",
            type=float,
            default=20.0,
            help="Maximum allowed stale percentage for each content group when strict mode is enabled.",
        )

    def handle(self, *args, **options):
        strict = options["strict"]
        check_freshness = options["check_freshness"]
        article_max_age_days = options["article_max_age_days"]
        ai_max_age_days = options["ai_max_age_days"]
        max_stale_percent = options["max_stale_percent"]
        issues = []
        warnings = []

        if settings.DEBUG:
            issues.append("DEBUG=True (must be False in production).")

        if not settings.ALLOWED_HOSTS:
            issues.append("ALLOWED_HOSTS is empty.")

        if not getattr(settings, "SECURE_SSL_REDIRECT", False):
            issues.append("SECURE_SSL_REDIRECT is not enabled.")

        if not os.environ.get("REDIS_URL") and not os.environ.get("KV_URL"):
            warnings.append(
                "REDIS_URL is not set — page cache will not persist across Vercel "
                "serverless instances (expect 1-5s TTFB on cold hits)."
            )

        if not getattr(settings, "SESSION_COOKIE_SECURE", False):
            issues.append("SESSION_COOKIE_SECURE is not enabled.")

        if not getattr(settings, "CSRF_COOKIE_SECURE", False):
            issues.append("CSRF_COOKIE_SECURE is not enabled.")

        hsts_seconds = int(getattr(settings, "SECURE_HSTS_SECONDS", 0) or 0)
        if hsts_seconds <= 0:
            warnings.append("SECURE_HSTS_SECONDS is not set (>0 recommended for HTTPS-only deployments).")

        if check_freshness:
            today = timezone.localdate()
            now = timezone.now()
            article_cutoff = today - timedelta(days=article_max_age_days)
            ai_cutoff = now - timedelta(days=ai_max_age_days)

            published_articles = Article.objects.filter(status="published")
            stale_articles = (
                published_articles.filter(last_reality_check__lt=article_cutoff).count()
                + published_articles.filter(last_reality_check__isnull=True).count()
            )
            total_articles = published_articles.count()
            article_stale_pct = (stale_articles / total_articles * 100) if total_articles else 0.0

            published_ai = AINewsItem.objects.filter(status="published")
            stale_ai = 0
            for item in published_ai.only("last_verified_at", "reviewed_at", "published_at"):
                effective = item.last_verified_at or item.reviewed_at or item.published_at
                if effective and effective < ai_cutoff:
                    stale_ai += 1
            total_ai = published_ai.count()
            ai_stale_pct = (stale_ai / total_ai * 100) if total_ai else 0.0

            if strict and article_stale_pct > max_stale_percent:
                issues.append(
                    f"Published article freshness gate failed ({article_stale_pct:.1f}% stale > {max_stale_percent:.1f}%)."
                )
            elif article_stale_pct > max_stale_percent:
                warnings.append(
                    f"Published article freshness is high ({article_stale_pct:.1f}% stale > {max_stale_percent:.1f}%)."
                )

            if strict and ai_stale_pct > max_stale_percent:
                issues.append(
                    f"AI news freshness gate failed ({ai_stale_pct:.1f}% stale > {max_stale_percent:.1f}%)."
                )
            elif ai_stale_pct > max_stale_percent:
                warnings.append(
                    f"AI news freshness is high ({ai_stale_pct:.1f}% stale > {max_stale_percent:.1f}%)."
                )

        if issues:
            self.stdout.write(self.style.ERROR("Release preflight: BLOCKING ISSUES"))
            for issue in issues:
                self.stdout.write(self.style.ERROR(f" - {issue}"))
        else:
            self.stdout.write(self.style.SUCCESS("Release preflight: no blocking issues found."))

        if warnings:
            self.stdout.write(self.style.WARNING("Release preflight: WARNINGS"))
            for warning in warnings:
                self.stdout.write(self.style.WARNING(f" - {warning}"))

        if strict and issues:
            raise CommandError("Preflight failed with blocking issues.")
