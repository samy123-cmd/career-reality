"""
Apply 900+ word editorial expansions to thin core articles.

    python manage.py expand_core_articles              # dry run
    python manage.py expand_core_articles --apply      # persist to DB
    python manage.py expand_core_articles --apply --slug junior-data-scientist-reality-india
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.expansions import CORE_ARTICLE_EXPANSIONS, expansion_word_count, resolve_slugs
from content.models import Article

CONTENT_FIELDS = (
    "title",
    "target_persona",
    "who_should_avoid",
    "common_expectation",
    "actual_reality",
    "salary_reality",
    "stuck_point",
    "verdict",
    "meta_title",
    "meta_description",
)


class Command(BaseCommand):
    help = "Apply 900+ word editorial expansions to six thin core articles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist updates. Default is dry run.",
        )
        parser.add_argument(
            "--slug",
            default="",
            help="Apply a single canonical or alias slug only.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        slug_filter = options["slug"]
        today = timezone.localdate()

        targets = CORE_ARTICLE_EXPANSIONS.items()
        if slug_filter:
            matched = None
            for primary, data in CORE_ARTICLE_EXPANSIONS.items():
                if slug_filter in resolve_slugs(primary, data):
                    matched = (primary, data)
                    break
            if not matched:
                self.stdout.write(self.style.ERROR(f"No expansion defined for slug: {slug_filter}"))
                return
            targets = [matched]

        updated = 0
        for primary, data in targets:
            slugs = resolve_slugs(primary, data)
            word_count = expansion_word_count(data)
            self.stdout.write(
                self.style.NOTICE(f"\n{primary} ({word_count} words) → aliases: {', '.join(slugs[1:]) or 'none'}")
            )

            for slug in slugs:
                article = Article.objects.filter(slug=slug).first()
                if not article:
                    self.stdout.write(f"  skip {slug}: not in database")
                    continue

                if apply_changes:
                    for field in CONTENT_FIELDS:
                        setattr(article, field, data[field])
                    article.last_reality_check = today
                    if article.status != "published":
                        article.status = "published"
                    article.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"  updated {slug}"))
                else:
                    self.stdout.write(f"  would update {slug} (status={article.status})")

        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"\nDone — {updated} article(s) expanded."))
        else:
            self.stdout.write(self.style.WARNING("\nDry run — pass --apply to persist."))
