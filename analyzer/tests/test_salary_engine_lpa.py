"""Salary engine LPA normalization tests."""

from django.test import SimpleTestCase

from analyzer.services.salary_engine import _ctc_to_lpa, _salary_reality_cache_key


class SalaryEngineLPATests(SimpleTestCase):
    def test_inr_to_lpa(self):
        self.assertEqual(_ctc_to_lpa(1800000), 18)

    def test_already_lpa(self):
        self.assertEqual(_ctc_to_lpa(18), 18)


class SalaryEngineCacheKeyTests(SimpleTestCase):
    def test_cache_key_has_no_whitespace(self):
        key = _salary_reality_cache_key("Software Engineer", 5.0, "Bengaluru", "service", 18)
        self.assertNotRegex(key, r"\s")
        self.assertLessEqual(len(key), 250)

    def test_same_inputs_same_key(self):
        a = _salary_reality_cache_key("Software Engineer", 5.0, "Bengaluru", "service", 18)
        b = _salary_reality_cache_key("Software Engineer", 5.0, "Bengaluru", "service", 18)
        self.assertEqual(a, b)

    def test_different_inputs_different_keys(self):
        a = _salary_reality_cache_key("Software Engineer", 5.0, "Bengaluru", "service", 18)
        b = _salary_reality_cache_key("Software Engineer", 6.0, "Bengaluru", "service", 18)
        self.assertNotEqual(a, b)

