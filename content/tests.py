from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class ContentModelAndViewTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Jane Doe",
            display_name="Jane Doe",
            bio="Research-backed career writer " * 10,
            linkedin_url="https://www.linkedin.com/in/jane-doe/",
            experience_summary="8+ years in tech hiring and compensation analysis",
            is_active=True,
        )
        self.category = Category.objects.create(
            name="Product",
            slug="product",
            description="Product roles",
            order=1,
        )

    def _create_article(self, title, slug, status="published"):
        return Article.objects.create(
            title=title,
            slug=slug,
            author=self.author,
            category=self.category,
            status=status,
            target_persona="Mid-level product professional",
            who_should_avoid="People seeking only hype",
            common_expectation="Fast growth from title alone",
            actual_reality="Scope and impact drive growth",
            salary_reality="Ranges vary by leverage and org quality",
            stuck_point="Execution-only ownership",
            verdict="Prioritize impact evidence over title optics",
            meta_title=f"{title} Meta"[:60],
            meta_description=("Balanced meta description " * 8)[:160],
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )

    def test_article_get_absolute_url(self):
        article = self._create_article("PM Reality", "pm-reality")

        self.assertEqual(article.get_absolute_url(), "/article/pm-reality/")

    def test_article_detail_returns_404_for_draft(self):
        self._create_article("Draft Reality", "draft-reality", status="draft")

        response = self.client.get("/article/draft-reality/")

        self.assertEqual(response.status_code, 404)

    def test_category_detail_shows_only_published_articles(self):
        self._create_article("Published One", "published-one", status="published")
        self._create_article("Draft One", "draft-one", status="draft")

        response = self.client.get(reverse("category_detail", kwargs={"slug": "product"}))

        self.assertEqual(response.status_code, 200)
        articles = list(response.context["articles"])
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].slug, "published-one")
