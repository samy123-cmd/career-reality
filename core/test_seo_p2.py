from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from content.models import Article, Author, Category
from core.seo_pages import HOME, SEO_TOOL_HUB
from core.sitemaps import ToolSitemap, StaticViewSitemap


class ToolSitemapTests(TestCase):
    def test_tool_sitemap_includes_traffic_pages(self):
        names = ToolSitemap().items()
        self.assertIn("salary_calculator", names)
        self.assertIn("analyzer_home", names)
        self.assertIn("layoff_radar", names)

    def test_static_sitemap_excludes_tools_to_avoid_duplicates(self):
        static = StaticViewSitemap().items()
        self.assertNotIn("salary_calculator", static)
        self.assertNotIn("analyzer_home", static)


class LandingPageSEOTests(TestCase):
    def test_homepage_has_keyword_rich_title(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CTC Calculator")

    def test_ctc_calculator_page_has_target_keywords(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In-Hand Salary Calculator")

    def test_resignation_analyzer_landing_indexable(self):
        response = self.client.get(reverse("analyzer_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resignation Risk Analyzer")

    def test_layoff_radar_has_layoff_keywords(self):
        response = self.client.get(reverse("layoff_radar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Layoff Radar")

    def test_ctc_calculator_has_structured_data(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertContains(response, '"@type": "SoftwareApplication"')
        self.assertContains(response, "ctc to in hand salary calculator india")

    def test_resignation_analyzer_has_faq_schema(self):
        response = self.client.get(reverse("analyzer_home"))
        self.assertContains(response, '"@type": "FAQPage"')

    def test_salary_reality_has_faq_schema(self):
        response = self.client.get(reverse("salary_reality"))
        self.assertContains(response, '"@type": "FAQPage"')

    def test_layoff_radar_has_dataset_schema(self):
        response = self.client.get(reverse("layoff_radar"))
        self.assertContains(response, '"@type": "Dataset"')

    def test_homepage_includes_pillar_links(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "layoff-recovery-timeline-india")


class DiscoveryLinkTests(TestCase):
    def test_onboarding_links_to_analyzer_landing(self):
        user = User.objects.create_user("onboard", password="pass")
        self.client.login(username="onboard", password="pass")
        response = self.client.get(reverse("onboarding"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("analyzer_home"))
        self.assertNotContains(response, reverse("wizard_start"))


class AuthorEEATTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Jane Doe",
            display_name="Jane Doe",
            bio="bio " * 20,
            experience_summary="12 years in Indian tech",
            linkedin_url="https://www.linkedin.com/in/janedoe/",
            is_active=True,
        )
        cat = Category.objects.create(name="Engineering", slug="engineering")
        for idx in range(2):
            Article.objects.create(
                title=f"Article {idx}",
                slug=f"author-article-{idx}",
                author=self.author,
                category=cat,
                status="published",
                target_persona="p",
                who_should_avoid="a",
                common_expectation="e",
                actual_reality="r",
                salary_reality="s",
                stuck_point="st",
                verdict="v",
                meta_title="t",
                meta_description="Meta description long enough for SEO testing purposes here.",
                published_at=timezone.now(),
            )

    def test_author_page_has_person_schema(self):
        response = self.client.get(
            reverse("author_detail", kwargs={"author_id": self.author.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"@type": "Person"')
        self.assertContains(response, "linkedin.com/in/janedoe")

    def test_author_page_title_matches_og_title(self):
        response = self.client.get(
            reverse("author_detail", kwargs={"author_id": self.author.id})
        )
        self.assertContains(response, "Jane Doe — Career Reality Author")


class InternalLinkingTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="A", display_name="A", bio="bio " * 20,
            linkedin_url="https://www.linkedin.com/in/a/",
        )
        self.cat = Category.objects.create(name="Engineering", slug="engineering")
        Article.objects.create(
            title="Test Article for SEO Hub",
            slug="test-seo-hub-article",
            author=self.author, category=self.cat, status="published",
            target_persona="p", who_should_avoid="a", common_expectation="e",
            actual_reality="r", salary_reality="s", stuck_point="st",
            verdict="v", meta_title="t",
            meta_description="Meta description long enough for SEO testing purposes here.",
            published_at=timezone.now(),
        )

    def test_article_page_includes_tool_hub(self):
        response = self.client.get(reverse("article_detail", kwargs={"slug": "test-seo-hub-article"}))
        self.assertContains(response, "FREE CAREER TOOLS")
        self.assertContains(response, reverse("salary_calculator"))

    def test_article_links_resignation_tool_to_landing_page(self):
        response = self.client.get(reverse("article_detail", kwargs={"slug": "test-seo-hub-article"}))
        self.assertContains(response, reverse("analyzer_home"))
        self.assertNotContains(response, reverse("wizard_start"))

    def test_footer_links_to_tools(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("salary_calculator"))
        self.assertContains(response, reverse("analyzer_home"))
        self.assertContains(response, reverse("layoff_radar"))


class SEOContextProcessorTests(TestCase):
    def test_seo_tool_hub_in_context(self):
        from core.context_processors import seo_internal_links

        ctx = seo_internal_links(RequestFactory().get("/"))
        self.assertEqual(len(ctx["seo_tool_hub"]), len(SEO_TOOL_HUB))
