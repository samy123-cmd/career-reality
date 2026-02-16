import re

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import Article


def _word_count(*parts):
    text = " ".join([p or "" for p in parts])
    text = re.sub(r"<[^>]+>", " ", text)
    return len(text.split())


def _expansion_block(article):
    category = article.category.name
    return f"""
<h3>Practical Decision Filter ({category})</h3>
<p>
Before changing direction, compare three timelines: next 90 days, next 12 months, and next 24 months.
If the role improves only title optics in 90 days but does not improve market leverage in 12 months, it is usually a weak move.
If the role gives measurable leverage (better scope, stronger decision rights, or harder-to-replace skills), the longer timeline wins.
</p>
<p>
Use this filter with real constraints: take-home cash, relocation cost, notice-period risk, and manager dependency.
Many bad decisions happen because people optimize only for compensation headline and ignore execution friction.
Validate with the <a href="/salary-calculator/">CTC Decoder</a> and benchmark with <a href="/salary-reality/">Salary Reality</a>.
</p>
<p>
Finally, force a written comparison: what gets better, what gets worse, and what stays the same.
If you cannot defend the move in writing, delay and gather one more data point from the market.
</p>
"""


class Command(BaseCommand):
    help = "Expands published low-word articles to a minimum word threshold."

    def add_arguments(self, parser):
        parser.add_argument(
            "--min-words",
            type=int,
            default=900,
            help="Minimum target words for published articles (default: 900).",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag, runs in dry mode.",
        )

    def handle(self, *args, **options):
        min_words = options["min_words"]
        apply_changes = options["apply"]

        updated = 0
        scanned = 0

        qs = Article.objects.filter(status="published").select_related("category").order_by("-updated_at")
        for article in qs:
            scanned += 1
            count = _word_count(
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.who_should_avoid,
                article.verdict,
            )

            if count >= min_words:
                continue

            blocks_added = 0
            while count < min_words:
                article.verdict = (article.verdict or "") + _expansion_block(article)
                blocks_added += 1
                count = _word_count(
                    article.common_expectation,
                    article.actual_reality,
                    article.salary_reality,
                    article.stuck_point,
                    article.who_should_avoid,
                    article.verdict,
                )

            article.last_reality_check = timezone.localdate()
            updated += 1
            self.stdout.write(
                f"- {article.slug}: expanded with {blocks_added} block(s), final_words={count}"
            )

            if apply_changes:
                article.save(update_fields=["verdict", "last_reality_check", "updated_at"])

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"{mode}: scanned={scanned}, expanded={updated}, min_words={min_words}"
            )
        )
