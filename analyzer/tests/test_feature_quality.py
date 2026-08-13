"""Production-quality contracts for the career tool pages.

These cover the failure modes that are invisible in a happy-path click-through
but make the product unusable in the field: a broken no-JS fallback, silent
validation failures, and missing assistive-technology wiring.
"""

import re

from django.test import TestCase
from django.urls import reverse

TOOL_URLS = (
    "tools:salary_reality_engine",
    "tools:offer_analyzer",
    "tools:stay_vs_switch",
    "tools:ai_career_impact",
    "tools:next_career_move",
    "tools:ask_career_reality",
)

WIZARD_URLS = ("tools:salary_reality_engine", "tools:stay_vs_switch")


class ProgressiveEnhancementTests(TestCase):
    """Every tool must be submittable when JavaScript never runs."""

    def test_every_tool_form_has_a_real_submit_button(self):
        for url_name in TOOL_URLS:
            with self.subTest(url_name=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                form = re.search(r"<form[^>]*method=\"post\".*?</form>", content, re.S)
                self.assertIsNotNone(form, "no POST form rendered")
                self.assertIn(
                    'type="submit"',
                    form.group(0),
                    msg=f"{url_name} has no submit button; form is unusable without JS",
                )

    def test_wizard_panels_are_not_hidden_in_markup(self):
        # Panels must ship open; only JS may collapse them.
        for url_name in WIZARD_URLS:
            with self.subTest(url_name=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                self.assertNotIn(
                    "data-cr-panel hidden",
                    content,
                    msg=f"{url_name} hides fields without JS, making them unreachable",
                )

    def test_wizard_exposes_all_fields_without_js(self):
        content = self.client.get(reverse("tools:salary_reality_engine")).content.decode()
        for field_id in ("id_role", "id_city", "id_current_ctc"):
            self.assertIn(field_id, content)

    def test_no_js_submission_succeeds(self):
        """A plain form POST (as a JS-less browser sends) must produce a result."""
        response = self.client.post(
            reverse("tools:salary_reality_engine"),
            {
                "role": "Software Engineer",
                "experience_years": "5",
                "city": "Bengaluru",
                "industry": "",
                "company_type": "",
                "current_ctc": "18",
                "role_level": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cr-result-hero")


class ValidationFeedbackTests(TestCase):
    """Invalid input must be explained, never silently discarded."""

    def test_invalid_submission_renders_error_summary(self):
        response = self.client.post(reverse("tools:salary_reality_engine"), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cr-form-error-summary")
        self.assertContains(response, "problem")

    def test_invalid_submission_marks_field_aria_invalid(self):
        response = self.client.post(reverse("tools:salary_reality_engine"), {})
        self.assertContains(response, 'aria-invalid="true"')

    def test_invalid_submission_links_error_to_field(self):
        response = self.client.post(reverse("tools:salary_reality_engine"), {})
        content = response.content.decode()
        self.assertIn('id="id_role-error"', content)
        self.assertIn('aria-describedby="id_role-error"', content)

    def test_valid_submission_has_no_error_summary(self):
        response = self.client.post(
            reverse("tools:salary_reality_engine"),
            {
                "role": "Software Engineer",
                "experience_years": "5",
                "city": "Bengaluru",
                "current_ctc": "18",
            },
        )
        self.assertNotContains(response, "cr-form-error-summary")

    def test_offer_analyzer_reports_missing_required_fields(self):
        response = self.client.post(reverse("tools:offer_analyzer"), {})
        self.assertContains(response, "cr-form-error-summary")
        self.assertContains(response, 'aria-invalid="true"')


class AccessibilityContractTests(TestCase):
    """Structural a11y guarantees that are easy to regress on."""

    def test_stepper_uses_valid_tablist_semantics(self):
        for url_name in WIZARD_URLS:
            with self.subTest(url_name=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                self.assertIn('role="tablist"', content)
                self.assertIn('role="tab"', content)
                self.assertIn('role="tabpanel"', content)
                self.assertIn("aria-controls=", content)
                self.assertIn("aria-labelledby=", content)

    def test_every_input_has_an_associated_label(self):
        for url_name in TOOL_URLS:
            with self.subTest(url_name=url_name):
                content = self.client.get(reverse(url_name)).content.decode()
                labelled = set(re.findall(r'<label[^>]*for="([^"]+)"', content))
                rendered = set(re.findall(r'<(?:input|select|textarea)[^>]*id="(id_[^"]+)"', content))
                # Hidden inputs (CSRF, priority weights) carry no visible label.
                hidden = set(re.findall(r'<input[^>]*type="hidden"[^>]*id="(id_[^"]+)"', content))
                unlabelled = rendered - labelled - hidden
                self.assertEqual(unlabelled, set(), msg=f"{url_name} unlabelled inputs: {unlabelled}")

    def test_results_region_is_announced(self):
        response = self.client.post(
            reverse("tools:salary_reality_engine"),
            {
                "role": "Software Engineer",
                "experience_years": "5",
                "city": "Bengaluru",
                "current_ctc": "18",
            },
        )
        self.assertContains(response, 'aria-live="polite"')
