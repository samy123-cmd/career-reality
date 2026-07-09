"""Tests for article source citation extraction."""

from django.test import TestCase
from django.utils import timezone

from content.models import Article, Author, Category
from content.source_citations import article_source_references, extract_body_sources


class SourceCitationTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Jane",
            display_name="Jane",
            bio="bio " * 10,
            linkedin_url="https://www.linkedin.com/in/jane/",
            experience_summary="8+ years",
            is_active=True,
        )
        self.category = Category.objects.create(name="Data Science", slug="data-science")

    def test_prefers_body_citations_over_generic_defaults(self):
        article = Article.objects.create(
            title="Data Test",
            slug="data-test-sources",
            author=self.author,
            category=self.category,
            status="published",
            target_persona="Analysts",
            who_should_avoid="Hype seekers",
            common_expectation="Expectation " * 50,
            actual_reality=(
                '<p>See <a href="https://www.kaggle.com/competitions">Kaggle competitions</a> '
                'and <a href="https://labour.gov.in/">Labour ministry data</a> for context.</p>'
            ),
            salary_reality="Salary " * 50,
            stuck_point="Stuck " * 50,
            verdict="Verdict " * 50,
            meta_title="Data Test",
            meta_description="Meta " * 20,
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )
        body_sources = extract_body_sources(article)
        self.assertGreaterEqual(len(body_sources), 2)
        urls = {s["url"] for s in body_sources}
        self.assertIn("https://www.kaggle.com/competitions", urls)
        self.assertIn("https://labour.gov.in/", urls)

    def test_category_defaults_when_body_has_few_links(self):
        article = Article.objects.create(
            title="Thin Sources",
            slug="thin-sources-test",
            author=self.author,
            category=self.category,
            status="published",
            target_persona="Analysts",
            who_should_avoid="Hype seekers",
            common_expectation="Expectation " * 50,
            actual_reality="Reality " * 50,
            salary_reality="Salary " * 50,
            stuck_point="Stuck " * 50,
            verdict="Verdict " * 50,
            meta_title="Thin Sources",
            meta_description="Meta " * 20,
            published_at=timezone.now(),
        )
        refs = article_source_references(article)
        self.assertGreaterEqual(len(refs), 3)
        names = {r["name"] for r in refs}
        self.assertIn("AmbitionBox Salary Insights", names)
