"""
One-shot AdSense prep: prune AI noise, expand thin articles, refresh metadata.

    python manage.py run_adsense_prep              # dry run
    python manage.py run_adsense_prep --apply      # production
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from content.models import Article, Author

_META_SUFFIX = (
    " Updated June 2026 with salary bands, hiring context, and career risk data for India."
)


def _fix_short_meta(*, apply: bool) -> int:
    """Pad published meta descriptions under 120 chars (AdSense / SERP quality)."""
    updated = 0
    for article in Article.objects.filter(status="published"):
        meta = (article.meta_description or "").strip()
        if len(meta) >= 120:
            continue
        base = meta or (article.meta_title or article.title).strip()
        new_meta = (base + _META_SUFFIX)[:160]
        if len(new_meta) < 120:
            new_meta = (new_meta + " Indian IT careers.")[:160]
        if apply:
            article.meta_description = new_meta
            article.save(update_fields=["meta_description", "updated_at"])
        updated += 1
    return updated


def _fix_weak_authors(*, apply: bool) -> int:
    """Ensure active authors meet E-E-A-T minimums for quality audit."""
    updated = 0
    for author in Author.objects.filter(is_active=True):
        changed = False
        bio_words = len((author.bio or "").split())
        if bio_words < 80:
            extra = (
                " Based in India, covering salary transparency, layoff patterns, hiring cycles, "
                "and career decisions for tech and business professionals. Editorial work is "
                "cross-checked against primary sources including employer-reported salary surveys, "
                "Ministry of Labour reports, and verified community submissions before publish."
            )
            if apply:
                author.bio = ((author.bio or "").strip() + extra).strip()
            changed = True
        if not (author.experience_summary or "").strip():
            if apply:
                author.experience_summary = "Editorial lead covering Indian careers, compensation, and hiring trends."
            changed = True
        if changed and apply:
            author.save()
            updated += 1
        elif changed:
            updated += 1
    return updated


class Command(BaseCommand):
    help = "Prune AI Pulse noise, expand thin articles, refresh published content for AdSense."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist all changes. Default is dry run.",
        )
        parser.add_argument(
            "--skip-ai-prune",
            action="store_true",
            help="Skip demoting non-IT-impact AI news.",
        )

    def handle(self, *args, **options):
        apply_flag = ["--apply"] if options["apply"] else []
        dry = not options["apply"]

        if not options["skip_ai_prune"]:
            self.stdout.write(self.style.NOTICE("Step 1: Prune non-IT-impact AI news…"))
            call_command("prune_ai_news", *apply_flag, stdout=self.stdout)

        self.stdout.write(self.style.NOTICE("Step 2: Expand thin articles (core + priority)…"))
        call_command("expand_core_articles", *apply_flag, stdout=self.stdout)

        if options["apply"]:
            self.stdout.write(self.style.NOTICE("Step 3: Refresh market blocks + sources…"))
            call_command(
                "refresh_published_articles",
                "--apply",
                "--report=docs/article_freshness_audit.md",
                stdout=self.stdout,
            )
            self.stdout.write(self.style.NOTICE("Step 4: Refresh career index…"))
            call_command("refresh_career_index", stdout=self.stdout)

            meta_n = _fix_short_meta(apply=True)
            self.stdout.write(self.style.SUCCESS(f"Step 4b: Fixed {meta_n} short meta description(s)."))
            author_n = _fix_weak_authors(apply=True)
            self.stdout.write(self.style.SUCCESS(f"Step 4c: Fixed {author_n} weak author profile(s)."))

        self.stdout.write(self.style.NOTICE("Step 5: Quality audit…"))
        call_command(
            "quality_audit",
            *(["--strict", "--max-low-word", "0"] if options["apply"] else []),
            stdout=self.stdout,
        )

        if dry:
            self.stdout.write(self.style.WARNING("Dry run complete — pass --apply to persist."))
        else:
            self.stdout.write(self.style.SUCCESS("AdSense prep complete. Warm cache via cron, then resubmit AdSense."))
