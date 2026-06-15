"""Tests for article audit and refresh pipeline."""

from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from content.article_market_data import MARKET_PERIOD
from content.article_refresh import apply_article_refresh, audit_article
from content.models import Article, Author, Category


def _make_article(**overrides):
    author = Author.objects.create(
        name="Editor",
        display_name="Editor",
        bio="bio " * 20,
        linkedin_url="https://www.linkedin.com/in/editor/",
        experience_summary="10+ years",
        is_active=True,
    )
    cat = Category.objects.create(name="Engineering", slug="engineering")
    defaults = {
        "title": "Senior Developer Salary Ceiling India",
        "slug": "senior-developer-salary-ceiling-india",
        "author": author,
        "category": cat,
        "status": "published",
        "target_persona": "Mid-senior engineers",
        "who_should_avoid": "Hype chasers",
        "common_expectation": "<p>" + "Expectation paragraph with enough words. " * 40 + "</p>",
        "actual_reality": "<p>" + "Reality paragraph with enough words. " * 40 + "</p>",
        "salary_reality": "<p>" + "Salary paragraph with enough words. " * 30 + "</p>",
        "stuck_point": "<p>" + "Stuck point paragraph with enough words. " * 25 + "</p>",
        "verdict": "<p>" + "Verdict paragraph with enough words. " * 25 + "</p>",
        "meta_title": "Senior Dev Ceiling 2024",
        "meta_description": ("Meta description long enough for SEO testing purposes here in 2024."),
        "published_at": timezone.now(),
        "last_reality_check": timezone.localdate() - timedelta(days=120),
    }
    defaults.update(overrides)
    return Article.objects.create(**defaults)


class ArticleRefreshTests(TestCase):
    def test_audit_flags_stale_article(self):
        article = _make_article()
        audit = audit_article(article, stale_days=30)
        self.assertTrue(audit.needs_refresh)
        self.assertTrue(any("stale_reality_check" in i for i in audit.issues))

    def test_apply_refresh_adds_market_block_and_sources(self):
        article = _make_article()
        changes = apply_article_refresh(article)
        self.assertIn("market_update", changes)
        self.assertIn("external_sources", changes)
        self.assertIn(MARKET_PERIOD, article.actual_reality)
        self.assertIn("ambitionbox.com", article.actual_reality.lower())
        self.assertIn("cr-salary-refresh", article.salary_reality)
        self.assertEqual(article.last_reality_check, timezone.localdate())

    def test_refresh_is_idempotent_for_same_period(self):
        article = _make_article()
        apply_article_refresh(article)
        article.save()
        article.refresh_from_db()
        before = article.actual_reality
        apply_article_refresh(article)
        self.assertEqual(before, article.actual_reality)

    def test_management_command_apply_updates_article(self):
        _make_article()
        call_command("refresh_published_articles", "--apply", "--slug=senior-developer-salary-ceiling-india")
        article = Article.objects.get(slug="senior-developer-salary-ceiling-india")
        self.assertIn(MARKET_PERIOD, article.actual_reality)
        self.assertEqual(article.last_reality_check, timezone.localdate())

    def test_meta_year_bumped_on_refresh(self):
        article = _make_article(meta_title="Title 2024", meta_description="Desc 2024 " * 10)
        apply_article_refresh(article)
        self.assertIn("2026", article.meta_title)
        self.assertIn("2026", article.meta_description)
