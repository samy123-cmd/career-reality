from datetime import timedelta
from unittest.mock import patch
import os

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import Article, Author, Category
from core.models import NewsletterSubscriber


class CoreViewsTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Test Author",
            display_name="Test Author",
            bio="Experienced writer " * 10,
            linkedin_url="https://www.linkedin.com/in/test-author/",
            experience_summary="10+ years in software and product",
            is_active=True,
        )
        self.category = Category.objects.create(
            name="Engineering",
            slug="engineering",
            description="Engineering roles",
            order=1,
        )

    def _create_article(self, slug, status="published", published_at=None):
        return Article.objects.create(
            title=f"Article {slug}",
            slug=slug,
            author=self.author,
            category=self.category,
            status=status,
            target_persona="Persona",
            who_should_avoid="Avoid",
            common_expectation="Expectation",
            actual_reality="Reality",
            salary_reality="Salary",
            stuck_point="Stuck",
            verdict="Verdict",
            meta_title=f"Meta {slug}"[:60],
            meta_description=(f"Meta description for {slug} " * 6)[:160],
            published_at=published_at or timezone.now(),
            last_reality_check=timezone.localdate() - timedelta(days=10),
        )

    def test_home_lists_only_published_and_limits_to_ten(self):
        for idx in range(12):
            self._create_article(slug=f"pub-{idx}")
        self._create_article(slug="draft-1", status="draft")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["articles"]), 10)
        self.assertTrue(all(a.status == "published" for a in response.context["articles"]))

    def test_robots_txt_contains_expected_directives(self):
        response = self.client.get(reverse("robots_txt"))

        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("User-agent: *", body)
        self.assertIn("Disallow: /resignation-risk/step/", body)
        self.assertIn("Sitemap: https://www.careerreality.in/sitemap.xml", body)

    def test_career_reality_index_has_expected_latest_band(self):
        response = self.client.get(reverse("career_reality_index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["latest_row"]["overall"], 65)
        self.assertEqual(response.context["latest_band"], "High Pressure")

    def test_newsletter_signup_creates_subscriber_and_redirects(self):
        response = self.client.post(
            reverse("newsletter_signup"),
            {"email": "reader@example.com"},
            HTTP_REFERER=reverse("home"),
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        self.assertTrue(NewsletterSubscriber.objects.filter(email="reader@example.com").exists())

    def test_run_freshness_cron_rejects_invalid_token(self):
        with patch.dict(os.environ, {"CRON_SECRET": "expected-token"}, clear=False):
            response = self.client.get(reverse("run_freshness_cron"), {"token": "wrong-token"})

        self.assertEqual(response.status_code, 403)

    @patch("core.views.call_command")
    def test_run_freshness_cron_allows_valid_token(self, mock_call_command):
        with patch.dict(os.environ, {"CRON_SECRET": "expected-token"}, clear=False):
            response = self.client.get(reverse("run_freshness_cron"), {"token": "expected-token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertTrue(mock_call_command.called)
