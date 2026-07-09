"""
Daily / scheduled audit and refresh for all published articles.

    python manage.py refresh_published_articles              # audit report (dry run)
    python manage.py refresh_published_articles --apply      # apply updates
    python manage.py refresh_published_articles --apply --report docs/article_freshness_audit.md
"""

from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.article_market_data import MARKET_LABEL, MARKET_PERIOD
from content.article_refresh import (
    apply_article_refresh,
    audit_article,
    build_audit_report_markdown,
)
from content.models import Article


class Command(BaseCommand):
    help = "Audit published articles for staleness and apply market/salary refreshes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist refresh updates. Default is audit-only (dry run).",
        )
        parser.add_argument(
            "--stale-days",
            type=int,
            default=30,
            help="Treat last_reality_check older than N days as stale (default: 30).",
        )
        parser.add_argument(
            "--report",
            default="",
            help="Write markdown audit report to this path (default: docs/article_freshness_audit.md when --apply).",
        )
        parser.add_argument(
            "--slug",
            default="",
            help="Refresh a single article slug only.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        stale_days = options["stale_days"]
        today = timezone.localdate()

        qs = Article.objects.filter(status="published").select_related("category", "author")
        if options["slug"]:
            qs = qs.filter(slug=options["slug"])

        articles = list(qs.order_by("slug"))
        if not articles:
            self.stdout.write(self.style.WARNING("No published articles found."))
            return

        self.stdout.write(
            self.style.NOTICE(
                f"Article refresh audit — {MARKET_LABEL} ({MARKET_PERIOD}) | "
                f"{len(articles)} article(s) | stale threshold: {stale_days}d"
            )
        )
        self.stdout.write("")

        audits = [audit_article(a, today=today, stale_days=stale_days) for a in articles]
        needs = [a for a in audits if a.needs_refresh]

        self.stdout.write(f"Needs refresh: {len(needs)} / {len(audits)}")
        self.stdout.write("")

        updated = 0
        for article, audit in zip(articles, audits):
            if not apply_changes:
                if audit.needs_refresh:
                    self.stdout.write(f"- {article.slug}: {', '.join(audit.issues)}")
                continue

            if not audit.needs_refresh:
                continue

            changes = apply_article_refresh(article, today=today)
            if changes:
                update_fields = [
                    "common_expectation",
                    "actual_reality",
                    "salary_reality",
                    "stuck_point",
                    "who_should_avoid",
                    "verdict",
                    "meta_title",
                    "meta_description",
                    "last_reality_check",
                    "updated_at",
                ]
                article.save(update_fields=update_fields)
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {article.slug}: {', '.join(changes)}")
                )

        if apply_changes:
            audits = [audit_article(a, today=today, stale_days=stale_days) for a in articles]

        report_path = options["report"] or (
            "docs/article_freshness_audit.md" if apply_changes else ""
        )
        if report_path:
            path = Path(report_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(build_audit_report_markdown(audits), encoding="utf-8")
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(f"Wrote audit report to {path}"))

        self.stdout.write("")
        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"Applied refresh to {updated} article(s)."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run complete. Re-run with --apply to persist updates."
                )
            )
