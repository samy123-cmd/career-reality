"""Tests for career taxonomy and role normalization."""

from django.test import SimpleTestCase

from analyzer.constants.career_taxonomy import normalize_role, role_search_terms


class CareerTaxonomyTests(SimpleTestCase):
    def test_normalize_sde_alias(self):
        self.assertEqual(normalize_role("sde"), "Software Engineer")

    def test_normalize_data_engineer(self):
        self.assertEqual(normalize_role("data engineer"), "Data Engineer")

    def test_normalize_hr_role(self):
        self.assertEqual(normalize_role("hr"), "HR Business Partner")

    def test_role_search_terms_includes_alias(self):
        terms = role_search_terms("Software Engineer")
        self.assertIn("software engineer", terms)
