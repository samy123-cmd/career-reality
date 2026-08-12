from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from companies.models import Company
from accounts.models import UserProfile


class UserProfileDefaultsTests(TestCase):
    """Ensure newly created users have correct default profile values."""

    def setUp(self):
        self.user = User.objects.create_user("newuser", password="pass")

    def test_profile_auto_created_on_user_save(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_salary_credits_default_zero(self):
        self.assertEqual(self.user.profile.salary_credits, 0)

    def test_tier_default_free(self):
        self.assertEqual(self.user.profile.tier, "free")

    def test_assessments_count_default_zero(self):
        self.assertEqual(self.user.profile.assessments_count, 0)

    def test_salary_submissions_count_default_zero(self):
        self.assertEqual(self.user.profile.salary_submissions_count, 0)


class UserProfileIsProTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("prouser", password="pass")
        self.profile = self.user.profile

    def test_free_tier_is_not_pro(self):
        self.assertFalse(self.profile.is_pro)

    def test_pro_tier_without_expiry_is_pro(self):
        self.profile.tier = "pro"
        self.profile.subscription_expires_at = None
        self.profile.save()
        self.assertTrue(self.profile.is_pro)

    def test_pro_tier_with_future_expiry_is_pro(self):
        self.profile.tier = "pro"
        self.profile.subscription_expires_at = timezone.now() + timezone.timedelta(days=30)
        self.profile.save()
        self.assertTrue(self.profile.is_pro)

    def test_pro_tier_with_past_expiry_is_not_pro(self):
        self.profile.tier = "pro"
        self.profile.subscription_expires_at = timezone.now() - timezone.timedelta(days=1)
        self.profile.save()
        self.assertFalse(self.profile.is_pro)

    def test_team_tier_without_expiry_is_pro(self):
        self.profile.tier = "team"
        self.profile.subscription_expires_at = None
        self.profile.save()
        self.assertTrue(self.profile.is_pro)


class SalaryCreditsTests(TestCase):
    """Test that salary submissions award credits to authenticated users."""

    def setUp(self):
        self.user = User.objects.create_user("tester", password="pass")

    def test_credits_increment_from_salary_submission(self):
        from django.urls import reverse
        self.client.login(username="tester", password="pass")
        self.client.post(reverse("submit_salary"), {
            "role": "Software Engineer",
            "experience_years": "3",
            "company_type": "product",
            "ctc": "2000000",
            "city": "Pune",
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.salary_credits, 3)

    def test_credits_accumulate_across_submissions(self):
        from django.urls import reverse
        self.client.login(username="tester", password="pass")
        payload = {
            "role": "Backend Developer",
            "experience_years": "2",
            "company_type": "service",
            "ctc": "1200000",
            "city": "Chennai",
        }
        self.client.post(reverse("submit_salary"), payload)
        self.client.post(reverse("submit_salary"), payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.salary_credits, 6)


class OnboardingPageTests(TestCase):
    """Tests for the post-signup onboarding page."""

    def setUp(self):
        self.user = User.objects.create_user("onboard_user", password="pass",
                                             email="onboard@example.com")

    def test_onboarding_page_renders_for_free_user(self):
        """Authenticated free user sees the onboarding page."""
        self.client.login(username="onboard_user", password="pass")
        response = self.client.get(reverse("onboarding"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You're in.")

    def test_onboarding_page_contains_key_tools(self):
        """Onboarding page links to the three main free tools."""
        self.client.login(username="onboard_user", password="pass")
        response = self.client.get(reverse("onboarding"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Risk Analyzer")
        self.assertContains(response, "CTC Decoder")
        self.assertContains(response, "Layoff Radar")

    def test_onboarding_page_contains_pro_upsell(self):
        """Onboarding page includes the Pro upgrade call to action."""
        self.client.login(username="onboard_user", password="pass")
        response = self.client.get(reverse("onboarding"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "See Pro Plans")

    def test_onboarding_redirects_anonymous_to_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(reverse("onboarding"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_onboarding_redirects_pro_user_to_dashboard(self):
        """Pro users are skipped past onboarding to the dashboard."""
        self.user.profile.tier = "pro"
        self.user.profile.save()
        self.client.login(username="onboard_user", password="pass")
        response = self.client.get(reverse("onboarding"))

        self.assertRedirects(response, reverse("pro_dashboard"),
                             fetch_redirect_response=False)

    def test_adapter_signup_redirect_points_to_onboarding(self):
        """Custom allauth adapter must redirect new sign-ups to /pro/onboarding/."""
        from accounts.adapter import AccountAdapter
        from unittest.mock import MagicMock
        adapter = AccountAdapter()
        mock_request = MagicMock()
        url = adapter.get_signup_redirect_url(mock_request)
        self.assertEqual(url, reverse("onboarding"))


class WatchlistTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("watchuser", password="pass", email="watch@example.com")
        self.user.profile.tier = "pro"
        self.user.profile.save()
        self.company = Company.objects.create(name="WatchCo", slug="watchco", sector="product")

    def test_pro_user_can_toggle_watchlist(self):
        self.client.login(username="watchuser", password="pass")
        response = self.client.post(reverse("toggle_watchlist", args=[self.company.slug]))
        self.assertEqual(response.status_code, 302)
        from accounts.models import CompanyWatchlist
        self.assertTrue(CompanyWatchlist.objects.filter(user=self.user, company=self.company).exists())

        self.client.post(reverse("toggle_watchlist", args=[self.company.slug]))
        self.assertFalse(CompanyWatchlist.objects.filter(user=self.user, company=self.company).exists())

    def test_free_user_redirected_from_watchlist(self):
        free_user = User.objects.create_user("freeuser", password="pass")
        self.client.login(username="freeuser", password="pass")
        response = self.client.post(reverse("toggle_watchlist", args=[self.company.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("pricing", response.url)


class CareerContextTests(TestCase):
    def setUp(self):
        from accounts.models import CareerProfile
        self.user = User.objects.create_user("ctx", password="pass")
        CareerProfile.objects.create(
            user=self.user,
            role="Data Engineer",
            experience_years=7,
            city="Pune",
            current_ctc=16,
            company_type="product",
        )

    def test_authenticated_profile_in_context(self):
        from accounts.career_context import get_career_context
        from django.test import RequestFactory
        request = RequestFactory().get("/")
        request.user = self.user
        request.session = {}
        ctx = get_career_context(request)
        self.assertEqual(ctx["role"], "Data Engineer")
        self.assertEqual(ctx["city"], "Pune")
