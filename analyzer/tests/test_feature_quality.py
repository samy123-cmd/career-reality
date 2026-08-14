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


class ResultPresentationTests(TestCase):
    """Raw internal values must never surface in the interface."""

    def _result(self):
        return self.client.post(
            reverse("tools:salary_reality_engine"),
            {
                "role": "Software Engineer",
                "experience_years": "5",
                "city": "Bengaluru",
                "current_ctc": "18",
            },
        )

    def test_pay_label_is_humanised(self):
        content = self._result().content.decode()
        self.assertNotIn("AT_MARKET", content)
        self.assertNotIn("At_Market", content)

    def test_confidence_line_explains_itself_without_data(self):
        content = self._result().content.decode()
        self.assertNotIn("0 samples", content)

    def test_pay_label_display_covers_every_engine_value(self):
        from analyzer.services.salary_engine import SalaryRealityResult

        for raw in ("underpaid", "at_market", "overpaid"):
            with self.subTest(pay_label=raw):
                display = SalaryRealityResult.PAY_LABEL_DISPLAY[raw]
                self.assertNotIn("_", display)
                self.assertTrue(display[0].isupper())

    def test_badge_variant_has_matching_style(self):
        from pathlib import Path

        from django.conf import settings

        from analyzer.services.salary_engine import SalaryRealityResult

        css = (Path(settings.BASE_DIR) / "static" / "css" / "feature-product.css").read_text()
        for raw in SalaryRealityResult.PAY_LABEL_DISPLAY:
            with self.subTest(pay_label=raw):
                self.assertIn(
                    f".cr-result-hero__badge--{raw}",
                    css,
                    msg=f"badge variant for {raw!r} renders unstyled",
                )


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

    def test_primary_cta_survives_the_button_reset(self):
        """`all: unset` must not out-specify the rules that paint the CTA.

        The reset names the element (0,3,1); a class-only fill rule (0,3,0)
        loses to it and the main call to action renders as bare text.
        """
        from pathlib import Path

        from django.conf import settings

        css = (Path(settings.BASE_DIR) / "static" / "css" / "feature-product.css").read_text()
        reset_index = css.find("all: unset")
        self.assertNotEqual(reset_index, -1)
        fill = css.find("button.az-calc-btn", reset_index)
        self.assertNotEqual(fill, -1, msg="CTA fill rules must also name `button` to beat the reset")

    def test_hidden_attribute_still_hides(self):
        """Setting `display` on buttons beats the UA `[hidden]` rule."""
        from pathlib import Path

        from django.conf import settings

        css = (Path(settings.BASE_DIR) / "static" / "css" / "feature-product.css").read_text()
        self.assertIn(".cr-feature [hidden]", css)
        self.assertIn("display: none !important", css)

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
