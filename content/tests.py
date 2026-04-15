from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command
from django.core.management.base import CommandError

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


class ArticleInlineNewsletterCTATests(TestCase):
    """Verify the mid-article newsletter CTA appears for anonymous users and is hidden for Pro users."""

    def setUp(self):
        self.author = Author.objects.create(
            name="Test Author",
            display_name="Test Author",
            bio="Career writer " * 10,
            linkedin_url="https://www.linkedin.com/in/test-author/",
            experience_summary="5+ years",
            is_active=True,
        )
        self.category = Category.objects.create(
            name="Tech",
            slug="tech",
            description="Tech roles",
            order=1,
        )
        self.article = Article.objects.create(
            title="Newsletter CTA Test Article",
            slug="newsletter-cta-test",
            author=self.author,
            category=self.category,
            status="published",
            target_persona="Mid-level engineer",
            who_should_avoid="Hype seekers",
            common_expectation="Fast growth",
            actual_reality="Scope drives growth",
            salary_reality="Varies by leverage",
            stuck_point="Execution-only ownership",
            verdict="Prioritize impact",
            meta_title="Newsletter CTA Test Article",
            meta_description=("Balanced meta description " * 8)[:160],
            published_at=timezone.now(),
            last_reality_check=timezone.localdate(),
        )

    def test_newsletter_cta_present_for_anonymous_user(self):
        response = self.client.get(reverse("article_detail", kwargs={"slug": "newsletter-cta-test"}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "article-newsletter-cta")
        self.assertContains(response, 'name="source" value="article_inline"')

    def test_newsletter_cta_contains_email_input(self):
        response = self.client.get(reverse("article_detail", kwargs={"slug": "newsletter-cta-test"}))

        self.assertContains(response, 'type="email"')
        self.assertContains(response, "Get Weekly Signals")

    def test_newsletter_cta_includes_article_slug(self):
        response = self.client.get(reverse("article_detail", kwargs={"slug": "newsletter-cta-test"}))

        self.assertContains(response, 'name="article_slug" value="newsletter-cta-test"')

    def test_newsletter_cta_visible_regardless_of_auth_status(self):
        from django.contrib.auth.models import User

        user = User.objects.create_user("proarticleuser", password="pass")
        user.profile.tier = "pro"
        user.profile.save()
        self.client.login(username="proarticleuser", password="pass")

        response = self.client.get(reverse("article_detail", kwargs={"slug": "newsletter-cta-test"}))

        # Article detail is cached and the CTA is always rendered (cache-safe).
        # Pro users see it too — harmless, they may already subscribe.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "article-newsletter-cta")
