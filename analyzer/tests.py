from django.test import TestCase
from django.urls import reverse

from analyzer.models import AssessmentLog, SalarySubmission


class AnalyzerFlowTests(TestCase):
    def test_result_requires_completed_session(self):
        response = self.client.get(reverse("wizard_result"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("wizard_start"))

    def test_cannot_skip_wizard_steps(self):
        response = self.client.get(reverse("wizard_step", kwargs={"step": 2}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("wizard_step", kwargs={"step": 1}))

    def test_wizard_flow_creates_single_assessment_log(self):
        self.client.post(reverse("wizard_start"))

        self.client.post(
            reverse("wizard_step", kwargs={"step": 1}),
            {"company_type": "service", "role_level": "ic"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 2}),
            {"bond_status": "no_bond", "notice_period": "60_days"},
        )
        final_step_response = self.client.post(
            reverse("wizard_step", kwargs={"step": 3}),
            {"current_situation": "evaluating", "has_offer": "yes"},
        )

        self.assertEqual(final_step_response.status_code, 302)
        self.assertEqual(final_step_response.url, reverse("wizard_result"))

        first_result = self.client.get(reverse("wizard_result"))
        second_result = self.client.get(reverse("wizard_result"))

        self.assertEqual(first_result.status_code, 200)
        self.assertEqual(second_result.status_code, 200)
        self.assertEqual(AssessmentLog.objects.count(), 1)

    def test_submit_salary_invalid_payload_returns_error(self):
        response = self.client.post(
            reverse("submit_salary"),
            {
                "role": "Backend Engineer",
                "experience": "not-a-number",
                "company_type": "service",
                "ctc": "1800000",
                "city": "Bengaluru",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("error"), "Invalid data")
        self.assertEqual(SalarySubmission.objects.count(), 0)

    def test_salary_feed_api_returns_serialized_submissions(self):
        SalarySubmission.objects.create(
            role="Backend Engineer",
            experience_years=4.0,
            company_type="service",
            ctc=1800000,
            city="Bengaluru",
            tech_stack="Python, Django",
        )

        response = self.client.get(reverse("salary_feed_api"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["submissions"]), 1)
        self.assertEqual(payload["submissions"][0]["role"], "Backend Engineer")
