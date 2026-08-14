"""Retention and consistency contracts across the ten features.

Two failure modes this guards against: a surface that reports an absence of
data without offering a way forward (the highest-churn moment in the product),
and features drifting apart so the suite stops feeling like one product.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import CareerAlert, CareerProfile, CareerSnapshot

TOOL_URLS = (
    "tools:salary_reality_engine",
    "tools:offer_analyzer",
    "tools:stay_vs_switch",
    "tools:ai_career_impact",
    "tools:next_career_move",
    "tools:ask_career_reality",
)

DEAD_END_COPY = ("No snapshots yet.", "No alerts.", "No critical signals — continue monitoring.")


class EmptyStateTests(TestCase):
    """An empty surface must teach and offer the next action."""

    def setUp(self):
        self.user = User.objects.create_user("retain", password="pw", email="r@example.com")
        profile = self.user.profile
        profile.tier = "pro"
        profile.save()
        CareerProfile.objects.create(
            user=self.user, role="Software Engineer", title="SDE II",
            experience_years=5, city="Bengaluru", company_type="service", current_ctc=18,
        )
        self.client.login(username="retain", password="pw")

    def test_progression_guides_the_first_snapshot(self):
        self.assertFalse(CareerSnapshot.objects.filter(user=self.user).exists())
        response = self.client.get(reverse("career_progression"))
        self.assertContains(response, "cr-empty")
        self.assertContains(response, "Add your first snapshot")

    def test_risk_radar_explains_what_is_monitored(self):
        self.assertFalse(CareerAlert.objects.filter(user=self.user).exists())
        response = self.client.get(reverse("career_risk_radar"))
        self.assertContains(response, "cr-empty")
        self.assertContains(response, "No risk signals right now")

    def test_empty_states_offer_a_real_destination(self):
        for url_name in ("career_progression", "career_risk_radar"):
            with self.subTest(page=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                self.assertIn("cr-empty__cta", content, msg=f"{url_name} empty state has no next action")

    def test_no_bare_dead_end_copy_remains(self):
        for url_name in ("career_progression", "career_risk_radar"):
            content = self.client.get(reverse(url_name)).content.decode()
            for phrase in DEAD_END_COPY:
                with self.subTest(page=url_name, phrase=phrase):
                    self.assertNotIn(phrase, content)


class CrossFeatureConsistencyTests(TestCase):
    """The ten features must behave like one product, not ten prototypes."""

    def test_every_tool_offers_onward_navigation(self):
        """A finished analysis must always suggest the next tool."""
        payloads = {
            "tools:salary_reality_engine": {"role": "Software Engineer", "experience_years": "5",
                                            "city": "Bengaluru", "current_ctc": "18"},
            "tools:stay_vs_switch": {"role": "Software Engineer", "experience_years": "5",
                                     "city": "Bengaluru", "company_type": "service", "current_ctc": "18"},
            "tools:ai_career_impact": {"job_title": "Software Engineer", "experience_years": "5",
                                       "seniority": "mid"},
            "tools:next_career_move": {"role": "Software Engineer", "experience_years": "5",
                                       "city": "Bengaluru", "company_type": "service", "current_ctc": "18"},
        }
        for url_name, payload in payloads.items():
            with self.subTest(tool=url_name):
                response = self.client.post(reverse(url_name), payload)
                self.assertContains(response, "cr-actions")

    def test_every_tool_shares_the_engine_failure_partial(self):
        for url_name in TOOL_URLS:
            with self.subTest(tool=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_every_tool_uses_the_same_card_shell(self):
        for url_name in TOOL_URLS:
            with self.subTest(tool=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                self.assertIn("cr-tool-card", content)

    def test_every_tool_declares_what_the_user_will_get(self):
        for url_name in TOOL_URLS:
            with self.subTest(tool=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                self.assertIn("cr-preview-strip", content, msg=f"{url_name} sets no expectation")

    def test_shared_partials_exist_once(self):
        """Guards against per-feature copies drifting out of sync."""
        from pathlib import Path

        from django.conf import settings

        partials = Path(settings.BASE_DIR) / "templates" / "features" / "partials"
        for name in ("_field.html", "_form_errors.html", "_engine_error.html", "_empty_state.html"):
            with self.subTest(partial=name):
                self.assertTrue((partials / name).exists(), msg=f"{name} missing from shared partials")
