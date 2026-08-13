"""End-to-end coverage for all ten CareerReality features.

Every case here corresponds to a defect that shipped while the page still
returned HTTP 200: an unsubmittable form, a dashboard that raised, or a routing
loop that left the user with nowhere to go.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import CareerProfile
from companies.models import Company

TOOL_URLS = (
    "tools:salary_reality_engine",
    "tools:offer_analyzer",
    "tools:stay_vs_switch",
    "tools:ai_career_impact",
    "tools:next_career_move",
    "tools:ask_career_reality",
)

DASHBOARD_URLS = (
    "my_career_reality",
    "career_progression",
    "career_risk_radar",
    "career_profile_edit",
)

PROFILE_PAYLOAD = {
    "role": "Software Engineer",
    "title": "SDE II",
    "experience_years": "5",
    "city": "Bengaluru",
    "company_type": "service",
    "current_ctc": "18",
    "company_name": "",
    "skills": "python, django",
}

# Minimum valid payload per tool, plus a marker proving the result rendered.
TOOL_SUBMISSIONS = {
    "tools:salary_reality_engine": (
        {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru", "current_ctc": "18"},
        "cr-result-hero",
    ),
    "tools:stay_vs_switch": (
        {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru",
         "company_type": "service", "current_ctc": "18"},
        "cr-result__verdict",
    ),
    "tools:ai_career_impact": (
        {"job_title": "Software Engineer", "experience_years": "5", "seniority": "mid"},
        "cr-result__verdict",
    ),
    "tools:next_career_move": (
        {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru",
         "company_type": "service", "current_ctc": "18"},
        "cr-path-card",
    ),
    "tools:ask_career_reality": (
        {"question": "Am I underpaid as an SDE in Bengaluru?"},
        "cr-ask-block",
    ),
    "tools:offer_analyzer": (
        {"role": "Software Engineer", "experience_years": "5",
         "offer_a_company": "Google", "offer_a_ctc": "30", "offer_a_fixed_pct": "70",
         "offer_a_variable_pct": "10", "offer_a_work_mode": "hybrid", "offer_a_growth": "4",
         "offer_b_company": "Infosys", "offer_b_ctc": "22", "offer_b_fixed_pct": "80",
         "offer_b_variable_pct": "5", "offer_b_work_mode": "office", "offer_b_growth": "2"},
        "cr-result__verdict",
    ),
}


class ProUserMixin:
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user("suite_pro", password="pw", email="p@example.com")
        profile = self.user.profile
        profile.tier = "pro"
        profile.save()
        self.client.login(username="suite_pro", password="pw")

    def create_profile(self):
        return CareerProfile.objects.create(
            user=self.user,
            role="Software Engineer",
            title="SDE II",
            experience_years=5,
            city="Bengaluru",
            company_type="service",
            current_ctc=18,
        )


class ToolSubmissionTests(ProUserMixin, TestCase):
    """Each tool must accept a realistic submission and render a result."""

    def test_every_tool_renders_a_result(self):
        for url_name, (payload, marker) in TOOL_SUBMISSIONS.items():
            with self.subTest(tool=url_name):
                response = self.client.post(reverse(url_name), payload)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode()
                self.assertNotIn(
                    "cr-form-error-summary",
                    content,
                    msg=f"{url_name} rejected a valid submission",
                )
                self.assertIn(marker, content, msg=f"{url_name} rendered no result")

    def test_offer_analyzer_priority_inputs_are_reachable(self):
        """The weights are required by the engine, so the UI must expose them."""
        content = self.client.get(reverse("tools:offer_analyzer")).content.decode()
        for name in ("priority_salary", "priority_stability", "priority_growth", "priority_wlb"):
            self.assertIn(name, content, msg=f"{name} is not rendered; form cannot be submitted")

    def test_offer_analyzer_submits_without_priorities(self):
        """Omitted sliders must fall back to defaults, never fail validation."""
        payload, marker = TOOL_SUBMISSIONS["tools:offer_analyzer"]
        response = self.client.post(reverse("tools:offer_analyzer"), payload)
        self.assertNotContains(response, "cr-form-error-summary")
        self.assertContains(response, marker)

    def test_tools_work_for_anonymous_visitors(self):
        self.client.logout()
        for url_name, (payload, marker) in TOOL_SUBMISSIONS.items():
            with self.subTest(tool=url_name):
                response = self.client.post(reverse(url_name), payload)
                self.assertEqual(response.status_code, 200)


class DashboardTests(ProUserMixin, TestCase):
    """Pro surfaces must render, not raise, once a profile exists."""

    def test_dashboards_render_with_profile(self):
        self.create_profile()
        for url_name in DASHBOARD_URLS:
            with self.subTest(page=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_risk_radar_counts_unread_alerts(self):
        """Regression: unread count filtered an already-sliced queryset."""
        self.create_profile()
        response = self.client.get(reverse("career_risk_radar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "unread")

    def test_progression_handles_no_snapshots(self):
        self.create_profile()
        response = self.client.get(reverse("career_progression"))
        self.assertEqual(response.status_code, 200)


class ProfileRoutingTests(ProUserMixin, TestCase):
    """A Pro user with no profile must still be able to create one."""

    def test_profile_edit_renders_without_existing_profile(self):
        response = self.client.get(reverse("career_profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Location", response.get("Location") or "")

    def test_dashboard_sends_profileless_user_to_the_builder(self):
        response = self.client.get(reverse("my_career_reality"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Must land somewhere a profile can actually be created.
        self.assertContains(response, "id_role")

    def test_no_redirect_loop_for_profileless_pro_user(self):
        response = self.client.get(reverse("my_career_reality"), follow=True)
        visited = [url for url, _ in response.redirect_chain]
        self.assertEqual(len(visited), len(set(visited)), msg=f"redirect loop: {visited}")

    def test_profile_can_be_created_then_dashboard_opens(self):
        response = self.client.post(reverse("career_profile_edit"), PROFILE_PAYLOAD, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CareerProfile.objects.filter(user=self.user).exists())
        self.assertEqual(self.client.get(reverse("my_career_reality")).status_code, 200)

    def test_profile_edit_updates_rather_than_duplicates(self):
        self.create_profile()
        self.client.post(reverse("career_profile_edit"), {**PROFILE_PAYLOAD, "current_ctc": "25"})
        self.assertEqual(CareerProfile.objects.filter(user=self.user).count(), 1)
        self.assertEqual(CareerProfile.objects.get(user=self.user).current_ctc, 25)


class CompanyRealityScoreTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            slug="suite-testcorp", name="SuiteTestCorp", headquarters="Bengaluru"
        )

    def test_reality_score_section_renders(self):
        response = self.client.get(reverse("company_detail", kwargs={"slug": self.company.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="reality-score"')

    def test_reality_score_loads_its_stylesheet(self):
        response = self.client.get(reverse("company_detail", kwargs={"slug": self.company.slug}))
        self.assertContains(response, "feature-product.css")

    def test_scoring_engine_returns_all_dimensions(self):
        from companies.scoring import compute_company_reality_score

        score = compute_company_reality_score(self.company)
        self.assertIsNotNone(score.overall)
        self.assertTrue(score.dimensions)
        for dimension in score.dimensions:
            self.assertTrue(dimension.label)
            self.assertIsNotNone(dimension.score)
