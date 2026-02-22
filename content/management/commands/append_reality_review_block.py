from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import Article


class Command(BaseCommand):
    help = "Append a standardized review/change-log block to published articles."

    MARKER = "<!-- reality-review-block -->"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag, runs in dry mode.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        today = timezone.localdate()
        updated = 0

        for article in Article.objects.filter(status="published").order_by("slug"):
            verdict = article.verdict or ""
            if self.MARKER in verdict:
                continue

            review_date = article.last_reality_check.isoformat() if article.last_reality_check else "Needs update"
            updated_date = article.updated_at.date().isoformat()
            block = (
                "<hr>"
                f"{self.MARKER}"
                "<section class='reality-review-meta'>"
                "<h3>Reality Check Metadata</h3>"
                f"<p><strong>Last reality check:</strong> {review_date}</p>"
                f"<p><strong>Last updated:</strong> {updated_date}</p>"
                f"<p><strong>Change log entry:</strong> {today.isoformat()} - Added standardized review metadata block.</p>"
                "<p><strong>Sources to verify during next refresh:</strong> Add 2-3 external references for salary and hiring claims.</p>"
                "</section>"
            )
            article.verdict = verdict + block
            updated += 1
            self.stdout.write(f"- {article.slug}")

            if apply_changes:
                article.save(update_fields=["verdict", "updated_at"])

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"{mode}: {updated} article(s) require review block insertion."))
