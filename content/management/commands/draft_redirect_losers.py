"""
Unpublish article slugs that 301 to canonical URLs (duplicate content hygiene).

    python manage.py draft_redirect_losers              # dry run
    python manage.py draft_redirect_losers --apply
"""

from django.core.management.base import BaseCommand

from content.models import Article
from content.seo_redirects import ARTICLE_SITEMAP_EXCLUDE_SLUGS


class Command(BaseCommand):
    help = "Set redirect-loser articles to draft (canonical URLs remain live via 301)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Default is dry run.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        losers = sorted(ARTICLE_SITEMAP_EXCLUDE_SLUGS)

        self.stdout.write(f"Redirect-loser slugs: {len(losers)}")

        to_draft = []
        for slug in losers:
            article = Article.objects.filter(slug=slug).first()
            if not article:
                self.stdout.write(f"  skip {slug}: not in database")
                continue
            if article.status == "draft":
                self.stdout.write(f"  already draft: {slug}")
                continue
            to_draft.append(article)
            self.stdout.write(f"  would draft: {slug} (status={article.status})")

        if apply_changes and to_draft:
            ids = [a.pk for a in to_draft]
            count = Article.objects.filter(pk__in=ids).update(status="draft")
            self.stdout.write(self.style.SUCCESS(f"Demoted {count} redirect-loser article(s) to draft."))
        elif not apply_changes:
            self.stdout.write(self.style.WARNING("Dry run — pass --apply to draft."))
