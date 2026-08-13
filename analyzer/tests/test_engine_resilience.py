"""Engines must fail without taking the page down.

A career tool is a computation over crowdsourced data. One malformed row should
cost the user a single result — with their answers intact and an honest message
— not a 500 and a lost session. These tests simulate that failure directly.
"""

import logging
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import CareerProfile
from analyzer.engine_guard import ENGINE_ERROR_MESSAGE, run_engine, safe_engine

TOOL_FAILURE_CASES = (
    ("analyzer.views_tools.get_salary_reality", "tools:salary_reality_engine",
     {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru", "current_ctc": "18"}),
    ("analyzer.views_tools.analyze_stay_vs_switch", "tools:stay_vs_switch",
     {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru",
      "company_type": "service", "current_ctc": "18"}),
    ("analyzer.views_tools.analyze_ai_career_impact", "tools:ai_career_impact",
     {"job_title": "Software Engineer", "experience_years": "5", "seniority": "mid"}),
    ("analyzer.views_tools.recommend_next_moves", "tools:next_career_move",
     {"role": "Software Engineer", "experience_years": "5", "city": "Bengaluru",
      "company_type": "service", "current_ctc": "18"}),
    ("analyzer.views_tools.answer_career_question", "tools:ask_career_reality",
     {"question": "Am I underpaid?"}),
    ("analyzer.views_tools.compare_offers", "tools:offer_analyzer",
     {"role": "Software Engineer", "experience_years": "5",
      "offer_a_company": "A", "offer_a_ctc": "20", "offer_a_fixed_pct": "70",
      "offer_a_variable_pct": "10", "offer_a_work_mode": "hybrid", "offer_a_growth": "3",
      "offer_b_company": "B", "offer_b_ctc": "25", "offer_b_fixed_pct": "70",
      "offer_b_variable_pct": "10", "offer_b_work_mode": "hybrid", "offer_b_growth": "3"}),
)


class EngineGuardUnitTests(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.addCleanup(logging.disable, logging.NOTSET)

    def test_run_engine_returns_result_on_success(self):
        result, error = run_engine("demo", lambda value: value * 2, 21)
        self.assertEqual(result, 42)
        self.assertIsNone(error)

    def test_run_engine_converts_failure_to_message(self):
        def boom():
            raise RuntimeError("downstream exploded")

        result, error = run_engine("demo", boom)
        self.assertIsNone(result)
        self.assertEqual(error, ENGINE_ERROR_MESSAGE)

    def test_run_engine_logs_with_engine_name(self):
        logging.disable(logging.NOTSET)

        def boom():
            raise ValueError("bad row")

        with self.assertLogs("analyzer.engine_guard", level="ERROR") as captured:
            run_engine("salary_reality", boom, _context={"role": "SDE"})
        joined = "\n".join(captured.output)
        self.assertIn("salary_reality", joined)
        self.assertIn("role", joined)

    def test_safe_engine_returns_none_on_failure(self):
        def boom():
            raise RuntimeError("nope")

        self.assertIsNone(safe_engine("demo", boom))

    def test_error_message_tells_the_user_what_to_do(self):
        self.assertIn("try again", ENGINE_ERROR_MESSAGE.lower())


class ToolDegradationTests(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.addCleanup(logging.disable, logging.NOTSET)

    def test_tools_survive_engine_failure(self):
        for target, url_name, payload in TOOL_FAILURE_CASES:
            with self.subTest(tool=url_name):
                with patch(target, side_effect=RuntimeError("simulated failure")):
                    response = self.client.post(reverse(url_name), payload)
                self.assertEqual(response.status_code, 200, msg=f"{url_name} returned a server error")

    def test_failure_is_explained_to_the_user(self):
        for target, url_name, payload in TOOL_FAILURE_CASES:
            with self.subTest(tool=url_name):
                with patch(target, side_effect=RuntimeError("simulated failure")):
                    response = self.client.post(reverse(url_name), payload)
                self.assertContains(response, "Analysis unavailable")

    def test_user_input_is_not_lost_on_failure(self):
        target, url_name, payload = TOOL_FAILURE_CASES[0]
        with patch(target, side_effect=RuntimeError("simulated failure")):
            response = self.client.post(reverse(url_name), payload)
        self.assertContains(response, "Software Engineer")

    def test_failed_answer_does_not_consume_ask_quota(self):
        """A failure must not bill the user for an answer they never got."""
        from analyzer.views_tools import _ask_limit_state

        with patch("analyzer.views_tools.answer_career_question", side_effect=RuntimeError("x")):
            self.client.post(reverse("tools:ask_career_reality"), {"question": "Am I underpaid?"})
        request = type("R", (), {"user": type("U", (), {"is_authenticated": False})(), "session": self.client.session})()
        _, _, count = _ask_limit_state(request)
        self.assertEqual(count, 0)


class DashboardDegradationTests(TestCase):
    """One broken panel must cost that panel, never the whole dashboard."""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.addCleanup(logging.disable, logging.NOTSET)
        self.user = User.objects.create_user("resilient", password="pw", email="r@example.com")
        profile = self.user.profile
        profile.tier = "pro"
        profile.save()
        CareerProfile.objects.create(
            user=self.user, role="Software Engineer", title="SDE II",
            experience_years=5, city="Bengaluru", company_type="service", current_ctc=18,
        )
        self.client.login(username="resilient", password="pw")

    def test_dashboards_survive_engine_failure(self):
        cases = (
            ("accounts.views.get_salary_reality", "my_career_reality"),
            ("accounts.views.compute_career_health", "my_career_reality"),
            ("accounts.views.compute_risk_radar", "career_risk_radar"),
            ("accounts.views.get_salary_reality", "career_risk_radar"),
            ("accounts.views.analyze_ai_career_impact", "my_career_reality"),
        )
        for target, url_name in cases:
            with self.subTest(page=url_name, engine=target):
                with patch(target, side_effect=RuntimeError("simulated failure")):
                    response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)


class HostileInputTests(TestCase):
    """Untrusted input must never escape or crash a tool."""

    def test_script_payload_is_escaped(self):
        response = self.client.post(reverse("tools:salary_reality_engine"), {
            "role": "<script>alert(1)</script>", "experience_years": "5",
            "city": "Bengaluru", "current_ctc": "18",
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("<script>alert(1)</script>", response.content.decode())

    def test_extreme_values_do_not_crash(self):
        cases = (
            {"role": "Software Engineer", "experience_years": "0", "city": "Bengaluru", "current_ctc": "1"},
            {"role": "Software Engineer", "experience_years": "50", "city": "Bengaluru", "current_ctc": "500"},
            {"role": "Software Engineer", "experience_years": "-5", "city": "Bengaluru", "current_ctc": "18"},
        )
        for payload in cases:
            with self.subTest(payload=payload):
                response = self.client.post(reverse("tools:salary_reality_engine"), payload)
                self.assertEqual(response.status_code, 200)

    def test_long_and_unicode_questions_are_handled(self):
        for question in ("a" * 5000, "मैं underpaid हूँ? 🤔💰"):
            with self.subTest(question=question[:20]):
                response = self.client.post(reverse("tools:ask_career_reality"), {"question": question})
                self.assertEqual(response.status_code, 200)
