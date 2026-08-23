"""Tests for GSC crawled-not-indexed remediation helpers."""

from django.test import TestCase
from django.utils import timezone

from content.gsc_indexing_fixes import apply_gsc_indexing_fixes
from content.models import Article, Author, Category


class GSCIndexingFixTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Editor",
            display_name="Editor",
            bio="Bio " * 10,
            linkedin_url="https://www.linkedin.com/in/editor/",
            experience_summary="10 years",
            is_active=True,
        )
        self.category = Category.objects.create(
            name="Career Strategy",
            slug="career-strategy",
            description="Strategy",
            order=1,
        )

    def _article(self, slug: str) -> Article:
        return Article.objects.create(
            title=f"Article {slug}",
            slug=slug,
            author=self.author,
            category=self.category,
            status="published",
            target_persona="Persona " * 20,
            who_should_avoid="Avoid " * 20,
            common_expectation="Expectation " * 40,
            actual_reality="Reality " * 80,
            salary_reality="Salary " * 40,
            stuck_point="Stuck " * 20,
            verdict="Verdict " * 20,
            meta_title=f"Meta {slug}"[:60],
            meta_description=("Description " * 12)[:160],
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )

    def test_apply_gsc_fixes_adds_external_sources_when_missing(self):
        article = self._article("green-careers-esg-renewable-sustainability-india-2026")
        changes = apply_gsc_indexing_fixes(article)
        self.assertIn("external_sources", changes)
        self.assertIn("mnre.gov.in", article.actual_reality)
        self.assertIn("cr-external-sources", article.actual_reality)

    def test_apply_gsc_fixes_skips_sources_when_body_already_cited(self):
        article = self._article("remote-work-salary-trap-india")
        article.actual_reality += (
            '<p>See <a href="https://www.naukri.com/">Naukri</a> and '
            '<a href="https://www.glassdoor.co.in/">Glassdoor</a> for data.</p>'
        )
        changes = apply_gsc_indexing_fixes(article)
        self.assertNotIn("external_sources", changes)
