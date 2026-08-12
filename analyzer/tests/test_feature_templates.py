"""Template integration tests for premium feature UI shell."""

from django.test import TestCase
from django.urls import reverse


class FeatureTemplateShellTests(TestCase):
    """Each tool page must load feature-product.css and premium card shell."""

    TOOL_URLS = (
        "tools:salary_reality_engine",
        "tools:offer_analyzer",
        "tools:stay_vs_switch",
        "tools:ai_career_impact",
        "tools:next_career_move",
        "tools:ask_career_reality",
    )

    def test_tool_pages_include_feature_product_css(self):
        for url_name in self.TOOL_URLS:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "feature-product.css")

    def test_tool_pages_include_premium_card_shell(self):
        for url_name in self.TOOL_URLS:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                content = response.content.decode()
                self.assertTrue(
                    "az-calc-card" in content or "cr-tool-card" in content,
                    msg=f"{url_name} missing az-calc-card/cr-tool-card",
                )

    def test_tool_pages_use_az_calc_inputs(self):
        for url_name in self.TOOL_URLS:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertContains(response, "az-calc-input")

    def test_salary_reality_has_stepper(self):
        response = self.client.get(reverse("tools:salary_reality_engine"))
        self.assertContains(response, "cr-stepper")
        self.assertContains(response, "az-calc-btn")
