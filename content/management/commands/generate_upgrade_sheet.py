import re
from datetime import timedelta
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import Article


def _strip_html(value):
    return re.sub(r"<[^>]+>", " ", value or "")


def _extract_links(value):
    return re.findall(r"<a\s+[^>]*href=['\"]([^'\"]+)['\"]", value or "", flags=re.I)


def _count_numbers(value):
    return len(re.findall(r"\b\d+(?:[.,]\d+)?\b", value or ""))


class Command(BaseCommand):
    help = "Generate a markdown upgrade sheet for all published core articles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="docs/published_core_article_upgrade_sheet.md",
            help="Output markdown path.",
        )

    def handle(self, *args, **options):
        today = timezone.localdate()
        output_path = Path(options["output"])
        articles = Article.objects.filter(status="published").select_related("category").order_by("slug")

        lines = []
        lines.append("# Published Core Article Upgrade Sheet")
        lines.append("")
        lines.append(f"Generated on: {today.isoformat()}")
        lines.append(f"Published articles audited: {articles.count()}")
        lines.append("")
        lines.append("## Global Priorities")
        lines.append("")
        lines.append("1. Add 2-3 external sources per article (gov/report/credible primary references).")
        lines.append("2. Add a visible review metadata block on each article.")
        lines.append("3. Increase quantified examples where numeric detail is low.")
        lines.append("")
        lines.append("## Per-Article Recommendations")
        lines.append("")

        low_quant_slugs = []
        thin_salary_slugs = []
        stale_review_slugs = []

        for article in articles:
            blocks = [
                article.target_persona,
                article.who_should_avoid,
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.verdict,
            ]
            combined = " ".join(blocks)
            links = _extract_links(combined)
            internal_links = [l for l in links if l.startswith("/") or "careerreality.in" in l]
            external_links = [l for l in links if l.startswith("http") and "careerreality.in" not in l]

            salary_words = len(_strip_html(article.salary_reality).split())
            number_count = _count_numbers(_strip_html(combined))
            meta_len = len((article.meta_description or "").strip())

            recs = []
            if len(external_links) < 2:
                recs.append("Add 2-3 external source links in `salary_reality` or `actual_reality`.")
            if number_count < 20:
                recs.append("Add quantified examples (at least 3-5 concrete numbers/ranges).")
                low_quant_slugs.append(article.slug)
            if salary_words < 150:
                recs.append("Expand `salary_reality` with role x experience x city ranges.")
                thin_salary_slugs.append(article.slug)
            if article.last_reality_check and article.last_reality_check < (today - timedelta(days=120)):
                recs.append("Refresh `last_reality_check` and verify all key claims.")
                stale_review_slugs.append(article.slug)
            if meta_len < 130:
                recs.append("Tighten meta description with clearer value + stronger search intent.")
            if len(internal_links) < 4:
                recs.append("Increase internal links to related tools and category pillars.")

            if not recs:
                recs.append("No urgent additions needed. Keep monthly refresh cadence.")

            lines.append(f"### {article.title} (`{article.slug}`)")
            lines.append("")
            lines.append(
                f"- Metrics: words={len(_strip_html(combined).split())}, internal_links={len(internal_links)}, "
                f"external_links={len(external_links)}, numeric_refs={number_count}, salary_words={salary_words}, "
                f"last_reality_check={article.last_reality_check}, meta_len={meta_len}"
            )
            lines.append("- Additions needed:")
            for rec in recs:
                lines.append(f"  - {rec}")
            lines.append("")

        lines.append("## Priority Buckets")
        lines.append("")
        lines.append(f"- Low quant detail: {len(low_quant_slugs)}")
        if low_quant_slugs:
            lines.append(f"  - {', '.join(low_quant_slugs)}")
        lines.append(f"- Thin salary sections: {len(thin_salary_slugs)}")
        if thin_salary_slugs:
            lines.append(f"  - {', '.join(thin_salary_slugs)}")
        lines.append(f"- Stale review dates (>120 days): {len(stale_review_slugs)}")
        if stale_review_slugs:
            lines.append(f"  - {', '.join(stale_review_slugs)}")
        lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Wrote upgrade sheet to {output_path}"))
