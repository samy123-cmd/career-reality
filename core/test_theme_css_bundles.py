from django.test import TestCase
from django.urls import reverse


class ThemeCssBundleTests(TestCase):
    def test_homepage_loads_core_and_home_bundles(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("style-core.css", content)
        self.assertIn("style-home.css", content)
        self.assertIn("components/tool-hub.css", content)
        self.assertIn("theme.js", content)
        self.assertIn("data-theme-toggle", content)
        self.assertIn("Stop guessing what the market pays.", content)
        self.assertIn("Instruments", content)
        self.assertNotIn("style-tools.css", content)
        self.assertNotIn("style-companies.css", content)

    def test_homepage_has_flash_free_theme_init(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("localStorage.getItem('cr-theme')", content)
        self.assertIn('data-theme="light"', content)

    def test_salary_calculator_loads_tools_bundle_only(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("style-core.css", content)
        self.assertIn("style-tools.css", content)
        self.assertIn("components/tool-hub.css", content)
        self.assertNotIn("style-home.css", content)
        self.assertNotIn("style-companies.css", content)

    def test_layoff_radar_loads_tool_hub_css_without_home_bundle(self):
        response = self.client.get(reverse("layoff_radar"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("components/tool-hub.css", content)
        self.assertIn("hp-tools-panel", content)
        self.assertNotIn("style-home.css", content)

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

    def _assert_modern_after(self, content, earlier_filename):
        modern_pos = content.rfind("theme-modern.css")
        earlier_pos = content.find(earlier_filename)
        self.assertGreater(modern_pos, 0, "theme-modern.css missing")
        self.assertGreater(earlier_pos, 0, f"{earlier_filename} missing")
        self.assertGreater(
            modern_pos,
            earlier_pos,
            f"theme-modern.css must load after {earlier_filename}",
        )

    def test_modern_surface_layer_loaded_last(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self._assert_modern_after(content, "theme-dark-contrast.css")
        self._assert_modern_after(content, "style-home.css")

    def test_modern_layer_follows_tools_bundle(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertEqual(response.status_code, 200)
        self._assert_modern_after(response.content.decode("utf-8"), "style-tools.css")

    def test_modern_layer_follows_companies_bundle(self):
        response = self.client.get(reverse("company_directory"))
        self.assertEqual(response.status_code, 200)
        self._assert_modern_after(response.content.decode("utf-8"), "style-companies.css")

    def test_modern_layer_follows_ai_pulse_css(self):
        response = self.client.get(reverse("ai_news_hub"))
        self.assertEqual(response.status_code, 200)
        self._assert_modern_after(response.content.decode("utf-8"), "ai_pulse.css")

    def test_theme_toggle_defaults_to_switch_to_dark(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('aria-label="Switch to dark mode"', content)
        self.assertNotIn("rgba(6, 6, 11, 0.9)", content)
        self.assertIn("--c-blue-accent: #c84b31", content)

    def test_homepage_includes_ink_inverse_tokens_in_critical_css(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("--c-ink-inverse", content)
        self.assertIn("brand-mark", content)

    def test_homepage_editorial_layout(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("nav-utilities", content)
        self.assertIn("hp-ticker-item", content)
        self.assertNotIn("hp-ticker-chip", content)
        self.assertIn("hp-editorial-list", content)
        self.assertIn("hp-editorial-featured", content)

    def test_footer_column_layout(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("footer-columns", content)
        self.assertIn("footer-col-heading", content)
        self.assertIn("footer-bottom-bar", content)
        self.assertNotIn("footer-newsletter", content)

    def test_ai_pulse_hub_loads_ai_pulse_css(self):
        response = self.client.get(reverse("ai_news_hub"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("ai_pulse.css", content)
        self.assertIn('data-theme="light"', content)
        self.assertIn("style-core.css", content)
        self.assertIn("AI Pulse · career translation", content)

    def test_salary_reality_has_explorer_language(self):
        response = self.client.get(reverse("salary_reality"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Data explorer", content)
        self.assertIn("cr-pct", content)
        self.assertIn("theme-modern.css", content)
        self.assertIn("style-tools.css", content)

    def test_ctc_decoder_has_ledger_kicker(self):
        response = self.client.get(reverse("salary_calculator"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("CTC decoder · new regime", content)
        self.assertIn("az-calc-breakdown", content)

    def test_layoff_radar_has_terminal_copy(self):
        response = self.client.get(reverse("layoff_radar"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Crowdsourced signals", content)
        self.assertIn("Report a signal", content)

    def test_company_directory_has_terminal_hero(self):
        response = self.client.get(reverse("company_directory"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Company intelligence", content)
        self.assertNotIn("Write a Review", content)

    def test_about_and_legal_pages_use_kicker(self):
        for name in ("about", "editorial", "terms", "privacy_policy", "contact"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertIn("cr-kicker", response.content.decode("utf-8"))

    def test_error_pages_use_terminal_language(self):
        from pathlib import Path

        from django.test.utils import override_settings

        server_error = Path("templates/500.html").read_text()
        self.assertIn("Back to the terminal", server_error)
        self.assertIn("#f9f8f6", server_error)
        self.assertIn("#c84b31", server_error)

        with override_settings(DEBUG=False):
            not_found = self.client.get("/this-page-does-not-exist-cr-2/")
        self.assertEqual(not_found.status_code, 404)
        body = not_found.content.decode("utf-8")
        self.assertIn("Back to the terminal", body)
        self.assertNotIn("🧮", body)