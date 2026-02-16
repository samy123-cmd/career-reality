import re
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from content.models import Article, Author


def _strip_html(value):
    return re.sub(r"<[^>]+>", " ", value or "")


def _extract_links(value):
    return re.findall(r"<a\s+[^>]*href=['\"]([^'\"]+)['\"]", value or "", flags=re.I)


class Command(BaseCommand):
    help = "Runs an editorial quality audit for published content."

    def handle(self, *args, **options):
        today = timezone.localdate()
        articles = Article.objects.filter(status="published").select_related("author", "category").order_by("-updated_at")

        total = articles.count()
        self.stdout.write(self.style.NOTICE(f"Published articles: {total}"))
        self.stdout.write("")

        low_word = []
        low_internal = []
        stale_check = []
        stale_update = []
        short_meta = []

        for article in articles:
            blocks = [
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.who_should_avoid,
                article.verdict,
            ]
            combined = " ".join(blocks)
            word_count = len(_strip_html(combined).split())
            links = _extract_links(combined)
            internal_links = [
                link for link in links if link.startswith("/") or "careerreality.in" in link
            ]

            if word_count < 900:
                low_word.append((article.slug, word_count))
            if len(internal_links) < 2:
                low_internal.append((article.slug, len(internal_links)))
            if article.last_reality_check and article.last_reality_check < (today - timedelta(days=180)):
                stale_check.append((article.slug, article.last_reality_check))
            if article.updated_at.date() < (today - timedelta(days=180)):
                stale_update.append((article.slug, article.updated_at.date()))
            if len(article.meta_description or "") < 120:
                short_meta.append((article.slug, len(article.meta_description or "")))

        self.stdout.write("Article-level findings")
        self.stdout.write(f"- Low word count (<900): {len(low_word)}")
        self.stdout.write(f"- Low internal links in body (<2): {len(low_internal)}")
        self.stdout.write(f"- Stale last reality check (>180d): {len(stale_check)}")
        self.stdout.write(f"- Stale updated_at (>180d): {len(stale_update)}")
        self.stdout.write(f"- Meta descriptions under 120 chars: {len(short_meta)}")
        self.stdout.write("")

        if low_word:
            self.stdout.write(self.style.WARNING("Articles with low word count"))
            for slug, count in low_word[:30]:
                self.stdout.write(f"  - {slug}: {count}")
            self.stdout.write("")

        if low_internal:
            self.stdout.write(self.style.WARNING("Articles with low internal link density"))
            for slug, count in low_internal[:30]:
                self.stdout.write(f"  - {slug}: {count}")
            self.stdout.write("")

        authors = Author.objects.filter(is_active=True)
        weak_authors = []
        for author in authors:
            bio_words = len((author.bio or "").split())
            if not author.linkedin_url or not author.experience_summary or bio_words < 80:
                weak_authors.append((author.display_name, bool(author.linkedin_url), bool(author.experience_summary), bio_words))

        self.stdout.write("Author-level findings")
        self.stdout.write(f"- Active authors: {authors.count()}")
        self.stdout.write(f"- Weak trust profiles: {len(weak_authors)}")
        for name, has_linkedin, has_exp, bio_words in weak_authors:
            self.stdout.write(
                f"  - {name}: linkedin={has_linkedin}, experience_summary={has_exp}, bio_words={bio_words}"
            )
        self.stdout.write("")

        if not low_word and not low_internal and not stale_check and not stale_update and not short_meta and not weak_authors:
            self.stdout.write(self.style.SUCCESS("Quality audit passed with no major findings."))
        else:
            self.stdout.write(self.style.WARNING("Quality audit completed with findings. Prioritize low-word articles and freshness."))
