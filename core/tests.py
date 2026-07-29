from datetime import timedelta, date
from unittest.mock import patch
import os

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from content.models import Article, Author, Category
from core.models import NewsletterSubscriber, CareerRealityIndexSnapshot


class CoreViewsTests(TestCase):
    def setUp(self):
        cache.clear()
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
        self.assertIn("Disallow: /api/", body)
        self.assertIn("Disallow: /resignation-risk/step/", body)
        self.assertIn("Disallow: /discussions/", body)
        self.assertIn("Sitemap: https://www.careerreality.in/sitemap.xml", body)

    def test_career_reality_index_has_expected_latest_band(self):
        response = self.client.get(reverse("career_reality_index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["latest_row"]["overall"], 61)
        self.assertEqual(response.context["latest_band"], "Elevated Pressure")

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

    def test_robots_txt_does_not_disallow_layoff_radar(self):
        response = self.client.get(reverse("robots_txt"))

        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertNotIn("Disallow: /layoff-radar/", body)

    def test_salary_calculator_page_contains_newsletter_cta(self):
        response = self.client.get(reverse("salary_calculator"))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("calc-newsletter-cta", content)
        self.assertIn("/newsletter/signup/", content)
        self.assertIn("ctc_decoder", content)

    def test_salary_calculator_newsletter_form_targets_signup_url(self):
        response = self.client.get(reverse("salary_calculator"))

        self.assertEqual(response.status_code, 200)
        # The form action must point to the newsletter signup endpoint
        self.assertContains(response, 'name="source" value="ctc_decoder"')
        self.assertContains(response, 'type="email"')

    def test_hero_social_proof_assessment_count_present(self):
        """Homepage hero shows assessment proof only when count is non-zero."""
        from analyzer.models import AssessmentLog
        from core.cache_utils import get_social_proof_counts

        AssessmentLog.objects.create(risk_level="Low", scenario_type="stable")
        get_social_proof_counts(rebuild=True)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "risk assessments run")
        self.assertIn("assessment_count", response.context)
        self.assertTrue(response.context["assessment_count"])

    def test_hero_social_proof_salary_data_points_present(self):
        """Homepage hero shows salary proof only when count is non-zero."""
        from analyzer.models import SalarySubmission
        from core.cache_utils import get_social_proof_counts

        SalarySubmission.objects.create(
            role="SDE",
            experience_years=3,
            city="Bengaluru",
            company_type="product",
            ctc=1800000,
        )
        get_social_proof_counts(rebuild=True)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "salary data points")
        self.assertIn("salary_count", response.context)
        self.assertTrue(response.context["salary_count"])

    def test_hero_social_proof_layoff_reports_present(self):
        """Homepage hero shows layoff proof only when count is non-zero."""
        from analyzer.models import LayoffReport
        from core.cache_utils import get_social_proof_counts

        LayoffReport.objects.create(
            company_name="Example Co",
            status="freeze",
        )
        get_social_proof_counts(rebuild=True)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "layoff reports tracked")
        self.assertIn("layoff_count", response.context)
        self.assertTrue(response.context["layoff_count"])

    def test_hero_hides_zero_social_proof(self):
        """Empty counters must not render misleading zero proof labels."""
        from core.cache_utils import get_social_proof_counts

        get_social_proof_counts(rebuild=True)
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "risk assessments run")
        self.assertNotContains(response, "salary data points")
        self.assertNotContains(response, "layoff reports tracked")
        self.assertEqual(response.context["assessment_count"], "")
        self.assertEqual(response.context["salary_count"], "")
        self.assertEqual(response.context["layoff_count"], "")

    def test_homepage_newsletter_section_present(self):
        """Homepage must contain the inline newsletter capture section."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hp-newsletter")
        self.assertContains(response, "home_footer_cta")

    def test_homepage_newsletter_form_targets_signup_url(self):
        """Newsletter form on homepage must POST to the newsletter signup endpoint."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/newsletter/signup/")
        self.assertContains(response, 'type="email"')

    def test_homepage_newsletter_copy_present(self):
        """Homepage newsletter section must include the headline and trust lines."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Monday Reality Check")
        self.assertIn("newsletter_count", response.context)


class CareerRealityIndexTests(TestCase):
    """Tests for the DB-backed Career Reality Index."""

    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_index_view_renders(self):
        response = self.client.get(reverse("career_reality_index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("index_rows", response.context)
        self.assertIn("latest_row", response.context)
        self.assertIn("latest_band", response.context)

    def test_index_fallback_when_no_snapshots(self):
        """Without any DB snapshots, falls back to editorial July 2026 baseline."""
        self.assertEqual(CareerRealityIndexSnapshot.objects.count(), 0)
        response = self.client.get(reverse("career_reality_index"))
        self.assertEqual(response.context["latest_row"]["overall"], 61)

    def test_index_reads_from_db_snapshots(self):
        """When snapshots exist, the view reports from the DB."""
        CareerRealityIndexSnapshot.objects.create(
            month="January 2026",
            month_date=date(2026, 1, 1),
            salary_pressure=80,
            switch_difficulty=75,
            layoff_risk=70,
            overall=77,
        )
        response = self.client.get(reverse("career_reality_index"))
        self.assertEqual(response.context["latest_row"]["overall"], 77)
        self.assertEqual(response.context["latest_band"], "Severe Pressure")

    def test_index_rows_ordered_newest_first(self):
        """_career_reality_index_rows should return most recent month first."""
        CareerRealityIndexSnapshot.objects.create(
            month="January 2026", month_date=date(2026, 1, 1),
            salary_pressure=60, switch_difficulty=60, layoff_risk=60, overall=60,
        )
        CareerRealityIndexSnapshot.objects.create(
            month="February 2026", month_date=date(2026, 2, 1),
            salary_pressure=70, switch_difficulty=70, layoff_risk=70, overall=70,
        )
        response = self.client.get(reverse("career_reality_index"))
        rows = response.context["index_rows"]
        self.assertEqual(rows[0]["month"], "February 2026")
        self.assertEqual(rows[1]["month"], "January 2026")

    def test_index_snapshot_model_str(self):
        snap = CareerRealityIndexSnapshot(month="March 2026", overall=65)
        self.assertIn("March 2026", str(snap))

    def test_delta_overall_in_context(self):
        CareerRealityIndexSnapshot.objects.create(
            month="January 2026", month_date=date(2026, 1, 1),
            salary_pressure=60, switch_difficulty=60, layoff_risk=60, overall=55,
        )
        CareerRealityIndexSnapshot.objects.create(
            month="February 2026", month_date=date(2026, 2, 1),
            salary_pressure=70, switch_difficulty=70, layoff_risk=70, overall=65,
        )
        response = self.client.get(reverse("career_reality_index"))
        self.assertEqual(response.context["delta_overall"], 10)


class CareerIndexCronTests(TestCase):
    """Tests for the cron endpoint that refreshes the Career Reality Index."""

    def test_cron_rejects_missing_token(self):
        with patch.dict(os.environ, {"CRON_SECRET": "secret-tok"}, clear=False):
            response = self.client.get(reverse("run_career_index_cron"))
        self.assertEqual(response.status_code, 403)

    def test_cron_rejects_wrong_token(self):
        with patch.dict(os.environ, {"CRON_SECRET": "correct"}, clear=False):
            response = self.client.get(
                reverse("run_career_index_cron"),
                HTTP_AUTHORIZATION="Bearer wrong-token",
            )
        self.assertEqual(response.status_code, 403)

    @patch("core.views.call_command")
    def test_cron_accepts_correct_bearer_token(self, mock_cmd):
        with patch.dict(os.environ, {"CRON_SECRET": "correct"}, clear=False):
            response = self.client.get(
                reverse("run_career_index_cron"),
                HTTP_AUTHORIZATION="Bearer correct",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


class LayoffAlertsCronTests(TestCase):
    def test_cron_rejects_missing_token(self):
        with patch.dict(os.environ, {"CRON_SECRET": "secret-tok"}, clear=False):
            response = self.client.get(reverse("run_layoff_alerts_cron"))
        self.assertEqual(response.status_code, 403)

    @patch("django.core.management.call_command")
    def test_layoff_alerts_cron_accepts_correct_bearer_token(self, mock_cmd):
        with patch.dict(os.environ, {"CRON_SECRET": "correct"}, clear=False):
            response = self.client.get(
                reverse("run_layoff_alerts_cron"),
                HTTP_AUTHORIZATION="Bearer correct",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        mock_cmd.assert_called_once()
        self.assertEqual(mock_cmd.call_args.args[0], "send_layoff_alerts")

