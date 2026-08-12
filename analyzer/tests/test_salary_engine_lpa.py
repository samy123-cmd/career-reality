"""Salary engine LPA normalization tests."""

from django.test import SimpleTestCase

from analyzer.services.salary_engine import _ctc_to_lpa


class SalaryEngineLPATests(SimpleTestCase):
    def test_inr_to_lpa(self):
        self.assertEqual(_ctc_to_lpa(1800000), 18)

    def test_already_lpa(self):
        self.assertEqual(_ctc_to_lpa(18), 18)
