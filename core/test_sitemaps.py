from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import Article, Author, Category
from content.seo_redirects import (
    ARTICLE_SITEMAP_EXCLUDE_SLUGS,
    MIN_INDEXABLE_CATEGORY_ARTICLES,
)
from core.sitemaps import ArticleSitemap, AuthorSitemap, CategorySitemap, StaticViewSitemap, ToolSitemap, AITagSitemap


class SitemapHygieneTests(TestCase):
    """P0: sitemap must match index/noindex rules."""

    def setUp(self):
        self.author = Author.objects.create(
            name="Author",
            display_name="Author",
            bio="Bio " * 10,
            linkedin_url="https://www.linkedin.com/in/author/",
            experience_summary="10+ years",
            is_active=True,
        )
        self.thin_cat = Category.objects.create(
            name="Marketing", slug="marketing", description="", order=1
        )
        self.rich_cat = Category.objects.create(
            name="Engineering", slug="engineering", description="", order=2
        )
        for idx in range(2):
            Article.objects.create(
                title=f"Mkt {idx}",
                slug=f"mkt-{idx}",
                author=self.author,
                category=self.thin_cat,
                status="published",
                target_persona="p",
                who_should_avoid="a",
                common_expectation="e",
                actual_reality="r",
                salary_reality="s",
                stuck_point="st",
                verdict="v",
                meta_title="t",
                meta_description="Meta description long enough for SEO purposes here.",
                published_at=timezone.now(),
            )
        for idx in range(MIN_INDEXABLE_CATEGORY_ARTICLES):
            Article.objects.create(
                title=f"Eng {idx}",
                slug=f"eng-{idx}",
                author=self.author,
                category=self.rich_cat,
                status="published",
                target_persona="p",
                who_should_avoid="a",
                common_expectation="e",
                actual_reality="r",
                salary_reality="s",
                stuck_point="st",
                verdict="v",
                meta_title="t",
                meta_description="Meta description long enough for SEO purposes here.",
                published_at=timezone.now(),
            )
        Article.objects.create(
            title="Duplicate Topic",
            slug="junior-data-scientist-reality-india-sql-janitor",
            author=self.author,
            category=self.rich_cat,
            status="published",
            target_persona="p",
            who_should_avoid="a",
            common_expectation="e",
            actual_reality="r",
            salary_reality="s",
            stuck_point="st",
            verdict="v",
            meta_title="t",
            meta_description="Meta description long enough for SEO purposes here.",
            published_at=timezone.now(),
        )

    def test_category_sitemap_excludes_thin_categories(self):
        slugs = [c.slug for c in CategorySitemap().items()]
        self.assertNotIn("marketing", slugs)
        self.assertIn("engineering", slugs)

    def test_tool_sitemap_urls_resolve(self):
        for name in ToolSitemap().items():
            url = reverse(name)
            self.assertTrue(url.startswith("/"))

    def test_article_sitemap_excludes_redirect_slugs(self):
        slugs = [a.slug for a in ArticleSitemap().items()]
        for excluded in ARTICLE_SITEMAP_EXCLUDE_SLUGS:
            self.assertNotIn(excluded, slugs)

    def test_category_sitemap_excludes_redirect_losers_from_article_threshold(self):
        """Redirect losers must not inflate category counts toward the indexable threshold."""
        borderline = Category.objects.create(name="Borderline", slug="borderline", order=99)
        for idx in range(2):
            Article.objects.create(
                title=f"Border {idx}",
                slug=f"border-{idx}",
                author=self.author,
                category=borderline,
                status="published",
                target_persona="p",
                who_should_avoid="a",
                common_expectation="e",
                actual_reality="r",
                salary_reality="s",
                stuck_point="st",
                verdict="v",
                meta_title="t",
                meta_description="Meta description long enough for SEO purposes here.",
                published_at=timezone.now(),
            )
        Article.objects.create(
            title="Redirect Loser In Borderline",
            slug="networking-myth-professional-relationships-worthless",
            author=self.author,
            category=borderline,
            status="published",
            target_persona="p",
            who_should_avoid="a",
            common_expectation="e",
            actual_reality="r",
            salary_reality="s",
            stuck_point="st",
            verdict="v",
            meta_title="t",
            meta_description="Meta description long enough for SEO purposes here.",
            published_at=timezone.now(),
        )
        slugs = [c.slug for c in CategorySitemap().items()]
        self.assertNotIn("borderline", slugs)
        self.assertIn("engineering", slugs)

    def test_static_sitemap_excludes_ai_hub_when_no_published_items(self):
        urls = [StaticViewSitemap().location(item) for item in StaticViewSitemap().items()]
        self.assertNotIn(reverse("ai_news_hub"), urls)

    def test_author_sitemap_includes_authors_with_two_plus_articles(self):
        author_ids = [a.id for a in AuthorSitemap().items()]
        self.assertIn(self.author.id, author_ids)

        thin_author = Author.objects.create(
            name="Thin",
            display_name="Thin",
            bio="Bio " * 10,
            linkedin_url="https://www.linkedin.com/in/thin/",
            experience_summary="1 year",
            is_active=True,
        )
        Article.objects.create(
            title="Only One",
            slug="only-one-author-article",
            author=thin_author,
            category=self.rich_cat,
            status="published",
            target_persona="p",
            who_should_avoid="a",
            common_expectation="e",
            actual_reality="r",
            salary_reality="s",
            stuck_point="st",
            verdict="v",
            meta_title="t",
            meta_description="Meta description long enough for SEO purposes here.",
            published_at=timezone.now(),
        )
        author_ids = [a.id for a in AuthorSitemap().items()]
        self.assertNotIn(thin_author.id, author_ids)
