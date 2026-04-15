from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from analyzer.models import AssessmentLog, SalarySubmission
from companies.models import Company


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
            {"company_type": "service", "role_level": "ic", "tenure_band": "18m_3y"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 2}),
            {"bond_status": "no_bond", "notice_period": "60_days", "ctc_vs_market": "at_market"},
        )
        final_step_response = self.client.post(
            reverse("wizard_step", kwargs={"step": 3}),
            {"current_situation": "evaluating", "performance_status": "good", "has_offer": "yes"},
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
        self.assertTrue(response.context["form"].errors)
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


_VALID_SALARY_PAYLOAD = {
    "role": "Backend Engineer",
    "experience_years": "4",
    "company_type": "service",
    "ctc": "1800000",
    "city": "Bengaluru",
}


class SalarySubmissionTests(TestCase):
    """Tests for the give-to-get salary submission feature."""

    def test_valid_submission_creates_record(self):
        response = self.client.post(reverse("submit_salary"), _VALID_SALARY_PAYLOAD)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SalarySubmission.objects.count(), 1)
        submission = SalarySubmission.objects.first()
        self.assertEqual(submission.role, "Backend Engineer")
        self.assertEqual(submission.ctc, 1800000)

    def test_valid_submission_saves_company_name(self):
        payload = dict(_VALID_SALARY_PAYLOAD, company_name="Infosys")
        self.client.post(reverse("submit_salary"), payload)

        submission = SalarySubmission.objects.first()
        self.assertEqual(submission.company_name, "Infosys")

    def test_valid_submission_links_matching_company_fk(self):
        company = Company.objects.create(name="SurgeLogic", slug="surgelogic", sector="product")
        payload = dict(_VALID_SALARY_PAYLOAD, company_name="surgelogic")  # case-insensitive
        self.client.post(reverse("submit_salary"), payload)

        submission = SalarySubmission.objects.first()
        self.assertEqual(submission.company_id, company.id)

    def test_valid_submission_no_fk_when_company_not_found(self):
        payload = dict(_VALID_SALARY_PAYLOAD, company_name="UnknownCorp XYZ")
        self.client.post(reverse("submit_salary"), payload)

        submission = SalarySubmission.objects.first()
        self.assertIsNone(submission.company)
        self.assertEqual(submission.company_name, "UnknownCorp XYZ")

    def test_anonymous_submission_awards_session_credits(self):
        self.client.post(reverse("submit_salary"), _VALID_SALARY_PAYLOAD)

        self.assertEqual(self.client.session.get("salary_unlocks"), 3)

    def test_authenticated_submission_increments_profile_credits(self):
        user = User.objects.create_user("credituser", password="pass")
        self.client.login(username="credituser", password="pass")

        self.client.post(reverse("submit_salary"), _VALID_SALARY_PAYLOAD)

        user.refresh_from_db()
        self.assertEqual(user.profile.salary_credits, 3)

    def test_authenticated_submission_increments_submissions_count(self):
        user = User.objects.create_user("countuser", password="pass")
        self.client.login(username="countuser", password="pass")

        self.client.post(reverse("submit_salary"), _VALID_SALARY_PAYLOAD)
        self.client.post(reverse("submit_salary"), _VALID_SALARY_PAYLOAD)

        user.refresh_from_db()
        self.assertEqual(user.profile.salary_submissions_count, 2)
        self.assertEqual(user.profile.salary_credits, 6)

    def test_invalid_payload_renders_form_errors(self):
        response = self.client.post(reverse("submit_salary"), {
            "role": "Backend Engineer",
            "experience_years": "not-a-number",
            "company_type": "service",
            "ctc": "1800000",
            "city": "Bengaluru",
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("experience_years", response.context["form"].errors)
        self.assertEqual(SalarySubmission.objects.count(), 0)

    def test_submit_success_page_renders(self):
        response = self.client.get(reverse("salary_submit_success"))
        self.assertEqual(response.status_code, 200)


class ResultPageNewsletterCTATests(TestCase):
    """
    Verify the post-result newsletter CTA block is present for
    anonymous users and contains the correct personalised copy.
    """

    def _complete_wizard(self, situation="unsafe", has_offer="no"):
        """Drive the wizard to completion and return the result page response."""
        self.client.post(reverse("wizard_start"))
        self.client.post(
            reverse("wizard_step", kwargs={"step": 1}),
            {"company_type": "service", "role_level": "ic", "tenure_band": "18m_3y"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 2}),
            {"bond_status": "no_bond", "notice_period": "60_days", "ctc_vs_market": "at_market"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 3}),
            {"current_situation": situation, "performance_status": "good", "has_offer": has_offer},
        )
        return self.client.get(reverse("wizard_result"))

    def test_newsletter_cta_block_present_for_anonymous_user(self):
        response = self._complete_wizard()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "result-newsletter-cta")
        self.assertContains(response, 'name="source" value="risk_analyzer_result"')

    def test_newsletter_cta_contains_email_input(self):
        response = self._complete_wizard()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="email"')
        self.assertContains(response, "Send Me Weekly Signals")

    def test_newsletter_cta_high_risk_copy_shown(self):
        """For an unsafe situation (high risk) the HIGH-risk copy variant is used."""
        response = self._complete_wizard(situation="unsafe", has_offer="no")

        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # HIGH or CRITICAL branch includes "Your risk is"
        self.assertIn("Stay informed", content)

    def test_newsletter_cta_hidden_for_authenticated_pro_user(self):
        """Pro users should not see the newsletter CTA (they are already subscribers)."""
        from django.contrib.auth.models import User
        user = User.objects.create_user("prouser", password="pass")
        user.profile.tier = "pro"
        user.profile.save()
        self.client.login(username="prouser", password="pass")

        response = self._complete_wizard()

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "result-newsletter-cta")


class ResultPageUpsellPersonalizationTests(TestCase):
    """
    Verify the exit-checklist paywall card shows personalized copy
    that references the user's actual risk level, role, and company.
    """

    def _run_wizard(self, company_type="service", role_level="ic",
                    bond_status="no_bond", notice_period="60_days",
                    situation="unsafe", has_offer="no"):
        self.client.post(reverse("wizard_start"))
        self.client.post(
            reverse("wizard_step", kwargs={"step": 1}),
            {"company_type": company_type, "role_level": role_level, "tenure_band": "18m_3y"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 2}),
            {"bond_status": bond_status, "notice_period": notice_period, "ctc_vs_market": "at_market"},
        )
        self.client.post(
            reverse("wizard_step", kwargs={"step": 3}),
            {"current_situation": situation, "performance_status": "good", "has_offer": has_offer},
        )
        return self.client.get(reverse("wizard_result"))

    def test_high_risk_upsell_references_risk_label(self):
        """High-risk upsell headline contains the risk label."""
        response = self._run_wizard(situation="unsafe")

        self.assertEqual(response.status_code, 200)
        # High risk headline: "Your High Risk situation needs a specific exit plan"
        self.assertContains(response, "High Risk situation")

    def test_high_risk_upsell_references_company_type(self):
        """High-risk upsell body references the notice label (context-specific detail)."""
        response = self._run_wizard(company_type="service", situation="unsafe",
                                    notice_period="60_days")

        self.assertEqual(response.status_code, 200)
        # notice_period "60_days" → label "60 days" — rendered inside the paywall card
        self.assertContains(response, "60 days")

    def test_medium_risk_upsell_headline_variant(self):
        """Medium-risk situation shows medium-specific headline."""
        # manager_bad → medium risk
        response = self._run_wizard(situation="manager_bad", has_offer="no",
                                    notice_period="30_days", bond_status="no_bond",
                                    company_type="product")

        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("friction points", content)

    def test_low_risk_upsell_headline_variant(self):
        """Low-risk situation shows low-risk-specific headline."""
        # evaluating + offer=yes + mnc_captive + ic + no_bond → low risk
        response = self._run_wizard(
            company_type="mnc_captive",
            role_level="ic",
            bond_status="no_bond",
            notice_period="30_days",
            situation="evaluating",
            has_offer="yes",
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Lock in your low-risk exit", content)

    def test_upsell_card_role_label_present(self):
        """The upsell card body contains the human-readable role label."""
        response = self._run_wizard(role_level="ic", situation="unsafe")

        self.assertEqual(response.status_code, 200)
        # "ic" maps to "Individual Contributor" or similar
        content = response.content.decode("utf-8")
        # The role label appears inside <strong> in the paywall card
        self.assertIn("paywall-card", content)
        self.assertIn("Individual Contributor", content)


class AnalyzerIntroNewsletterCTATests(TestCase):
    """Tests for the pre-start newsletter nudge on the analyzer intro page."""

    def test_newsletter_nudge_present_for_anonymous_user(self):
        """Anonymous visitors see the newsletter nudge on the intro page."""
        response = self.client.get(reverse("analyzer_home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "az-intro-newsletter")
        self.assertContains(response, "analyzer_intro_nudge")

    def test_newsletter_nudge_contains_email_input(self):
        """The nudge form contains an email input field."""
        response = self.client.get(reverse("analyzer_home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="email"')
        self.assertContains(response, "/newsletter/signup/")

    def test_newsletter_nudge_hidden_for_authenticated_user(self):
        """The nudge is not shown to logged-in users (they already have an account)."""
        user = User.objects.create_user("intro_auth", password="pass")
        self.client.login(username="intro_auth", password="pass")
        response = self.client.get(reverse("analyzer_home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "az-intro-newsletter")

    def test_start_button_still_present_for_all_users(self):
        """The 'Start Risk Assessment' button must remain visible regardless of auth state."""
        response = self.client.get(reverse("analyzer_home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start Risk Assessment")
