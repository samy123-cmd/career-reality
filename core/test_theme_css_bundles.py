from django.test import TestCase
from django.urls import reverse


class ThemeCssBundleTests(TestCase):
    def test_homepage_loads_core_and_home_bundles(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("style-core.css", content)
        self.assertIn("style-home.css", content)
        self.assertIn("theme.js", content)
        self.assertIn("data-theme-toggle", content)
        self.assertNotIn("style-tools.css", content)
        self.assertNotIn("style-companies.css", content)

    def test_homepage_has_flash_free_theme_init(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("localStorage.getItem('cr-theme')", content)
        self.assertIn('data-theme="dark"', content)

    def test_salary_calculator_loads_tools_bundle_only(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("style-core.css", content)
        self.assertIn("style-tools.css", content)
        self.assertNotIn("style-home.css", content)
        self.assertNotIn("style-companies.css", content)

    def test_company_directory_loads_companies_bundle_only(self):
        response = self.client.get(reverse("company_directory"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("style-core.css", content)
        self.assertIn("style-companies.css", content)
        self.assertNotIn("style-home.css", content)
        self.assertNotIn("style-tools.css", content)

    def test_dark_contrast_layer_loaded_after_themes(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        contrast_pos = content.find("theme-dark-contrast.css")
        premium_pos = content.find("theme-premium-dark.css")
        self.assertGreater(contrast_pos, 0)
        self.assertGreater(premium_pos, 0)
        self.assertGreater(contrast_pos, premium_pos)

    def test_homepage_includes_ink_inverse_tokens_in_critical_css(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("--c-ink-inverse", content)
        self.assertIn("brand-mark", content)

    def test_homepage_ui_polish_markup(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("nav-utilities", content)
        self.assertIn("hp-ticker-chip", content)

    def test_footer_has_column_grid(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("footer-grid", content)
        self.assertIn("footer-col-title", content)
        self.assertIn("footer-newsletter", content)

    def test_ai_pulse_hub_loads_ai_pulse_css(self):
        response = self.client.get(reverse("ai_news_hub"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("ai_pulse.css", content)
        self.assertIn('data-theme="dark"', content)
        self.assertIn("style-core.css", content)
