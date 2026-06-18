"""
Demote AI Pulse items that are not IT workplace-impact editorial content.

    python manage.py prune_ai_news              # dry run
    python manage.py prune_ai_news --apply      # set non-indexable published → draft
"""

from django.core.management.base import BaseCommand

from ainews.indexing import item_is_indexable
from ainews.models import AINewsItem


class Command(BaseCommand):
    help = "Unpublish AI news that fails IT workplace-impact / career_angle gates."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist demotions. Default is dry run.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        published = AINewsItem.objects.filter(status="published").order_by("-published_at")
        demote = [item for item in published if not item_is_indexable(item)]

        self.stdout.write(f"Published AI items: {published.count()}")
        self.stdout.write(f"Would demote to draft: {len(demote)}")

        for item in demote[:25]:
            reason = []
            if not (item.career_angle or "").strip():
                reason.append("missing career_angle")
            elif len((item.career_angle or "").strip()) < 80:
                reason.append("thin career_angle")
            self.stdout.write(f"  - {item.slug}: {', '.join(reason) or 'not IT impact / stale'}")

        if len(demote) > 25:
            self.stdout.write(f"  … and {len(demote) - 25} more")

        if apply_changes:
            ids = [item.pk for item in demote]
            updated = AINewsItem.objects.filter(pk__in=ids).update(status="draft")
            self.stdout.write(self.style.SUCCESS(f"Demoted {updated} item(s) to draft."))
        else:
            self.stdout.write(self.style.WARNING("Dry run — pass --apply to demote."))
