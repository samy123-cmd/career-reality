from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.cache import cache

from .models import Article, Author, Category
from core.publishing import INDEXABLE_AUTHOR_MIN_ARTICLES, INDEXABLE_CATEGORY_MIN_ARTICLES


class ContentModelAndViewTests(TestCase):
    def setUp(self):
        cache.clear()
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

    def test_article_detail_uses_content_derived_evidence_copy(self):
        article = self._create_article("PM Reality", "pm-reality")
        article.actual_reality = "Unique reality sentence for regression coverage. Another supporting sentence."
        article.salary_reality = "Salary variance depends on scope, city, and negotiating leverage."
        article.stuck_point = "Most PMs stall when they own process but not metrics."
        article.save(update_fields=["actual_reality", "salary_reality", "stuck_point"])

        response = self.client.get(reverse("article_detail", kwargs={"slug": "pm-reality"}))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Unique reality sentence for regression coverage.", response.context["evidence_map"][1]["claim"])
        self.assertTrue(all(source.get("note") for source in response.context["source_references"]))

    def test_category_detail_noindexes_thin_pages(self):
        self._create_article("Published One", "published-one", status="published")

        response = self.client.get(reverse("category_detail", kwargs={"slug": "product"}))

        self.assertEqual(response.context["meta_robots"], "noindex, follow")

    def test_category_detail_indexes_only_after_threshold(self):
        for idx in range(INDEXABLE_CATEGORY_MIN_ARTICLES):
            self._create_article(f"Published {idx}", f"published-{idx}", status="published")

        response = self.client.get(reverse("category_detail", kwargs={"slug": "product"}))

        self.assertEqual(response.context["meta_robots"], "index, follow")

    def test_author_page_requires_stronger_threshold_for_indexing(self):
        for idx in range(INDEXABLE_AUTHOR_MIN_ARTICLES - 1):
            self._create_article(f"Published {idx}", f"author-published-{idx}", status="published")

        response = self.client.get(reverse("author_detail", kwargs={"author_id": self.author.id}))

        self.assertEqual(response.context["meta_robots"], "noindex, follow")


class QualityAuditCommandTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Trustworthy Author",
            display_name="Trustworthy Author",
            bio=("Evidence-based career analysis " * 30).strip(),
            linkedin_url="https://www.linkedin.com/in/trustworthy-author/",
            experience_summary="10+ years in tech hiring research and compensation benchmarking.",
            is_active=True,
        )
        self.category = Category.objects.create(
            name="Engineering",
            slug="engineering",
            description="Engineering roles",
            order=1,
        )

    def _create_quality_article(self, slug="well-formed-article"):
        repeated = "This section explains practical role trade-offs with evidence. " * 40
        two_internal_links = (
            "<a href='/about/'>About</a> "
            "<a href='https://www.careerreality.in/editorial/'>Editorial</a>"
        )
        return Article.objects.create(
            title="Well-Formed Article",
            slug=slug,
            author=self.author,
            category=self.category,
            status="published",
            target_persona="Mid-career software engineer",
            who_should_avoid=repeated + two_internal_links,
            common_expectation=repeated,
            actual_reality=repeated,
            salary_reality=repeated,
            stuck_point=repeated,
            verdict=repeated,
            meta_title="Well-Formed Article Meta",
            meta_description=("Reliable career analysis with evidence and methodology transparency. " * 3)[:160],
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )

    def test_quality_audit_strict_passes_with_no_findings(self):
        self._create_quality_article()

        call_command("quality_audit", "--strict")

    def test_quality_audit_strict_fails_when_threshold_exceeded(self):
        self._create_quality_article()
        weak_author = Author.objects.create(
            name="Weak Author",
            display_name="Weak Author",
            bio="Short bio",
            linkedin_url="",
            experience_summary="",
            is_active=True,
        )
        Article.objects.create(
            title="Low Quality Article",
            slug="low-quality-article",
            author=weak_author,
            category=self.category,
            status="published",
            target_persona="Entry-level engineer",
            who_should_avoid="avoid",
            common_expectation="expectation",
            actual_reality="reality",
            salary_reality="salary",
            stuck_point="stuck",
            verdict="verdict",
            meta_title="Low Quality Article Meta",
            meta_description="too short",
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )

        with self.assertRaises(CommandError):
            call_command("quality_audit", "--strict")
