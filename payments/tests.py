from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from payments.models import Order, Product, Subscription


def _make_pro_monthly():
    return Product.objects.create(
        name="Career Reality Pro",
        slug="pro-monthly",
        price_paise=29900,
        product_type="subscription_monthly",
        is_active=True,
    )


def _make_pro_annual():
    return Product.objects.create(
        name="Career Reality Pro — Annual",
        slug="pro-annual",
        price_paise=249900,
        product_type="subscription_annual",
        is_active=True,
    )


class PricingPageTests(TestCase):
    """Tests for the public pricing page."""

    def test_pricing_page_renders(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertEqual(response.status_code, 200)

    def test_pricing_page_contains_roi_callout(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "plan-roi")
        self.assertContains(response, "667x ROI")

    def test_pricing_page_contains_billing_toggle(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "billing-toggle")
        self.assertContains(response, "btn-annual-toggle")

    def test_pricing_page_contains_annual_price(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "2,499")

    def test_pricing_page_contains_trust_line(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "Cancel anytime")

    def test_pricing_page_hides_zero_proof_counters(self):
        response = self.client.get(reverse("payments:pricing"))
        content = response.content.decode()
        self.assertNotIn(">0<small>salary data points</small>", content)
        self.assertNotIn('default:"0"', content)

    def test_pricing_free_cta_goes_to_calculator(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "Try free tools")
        self.assertContains(response, reverse("salary_calculator"))

    def test_pricing_pro_cta_copy(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "Unlock Pro")
        self.assertContains(response, "Unlimited salary benchmarks")

    def test_pro_button_default_product_is_monthly(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, 'data-product="pro-monthly"')

    def test_annual_save_badge_present(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, "Save 30%")

    def test_pro_inline_email_form_present(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, 'id="pro-email-wrap"')
        self.assertContains(response, 'id="pro-email-input"')
        self.assertContains(response, 'id="btn-pro-confirm"')

    def test_checklist_inline_email_form_present(self):
        response = self.client.get(reverse("payments:pricing"))
        self.assertContains(response, 'id="checklist-email-wrap"')
        self.assertContains(response, 'id="checklist-email-input"')
        self.assertContains(response, 'id="btn-checklist-confirm"')

    def test_no_window_prompt_in_pricing_js(self):
        """Ensure the jarring browser prompt() dialog has been replaced."""
        response = self.client.get(reverse("payments:pricing"))
        content = response.content.decode()
        self.assertNotIn("window.prompt", content)
        self.assertNotIn("= prompt(", content)


class AnnualSubscriptionActivationTests(TestCase):
    """Tests for _activate_subscription with annual product type."""

    def _make_order(self, product, user):
        return Order.objects.create(
            razorpay_order_id=f"test_order_{product.slug}",
            amount_paise=product.price_paise,
            product=product,
            user=user,
            status="paid",
        )

    def test_annual_subscription_grants_365_days(self):
        from payments.views import _activate_subscription

        user = User.objects.create_user("annualuser", password="pass")
        product = _make_pro_annual()
        order = self._make_order(product, user)

        before = timezone.now()
        _activate_subscription(order)
        after = timezone.now()

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.tier, "pro")
        self.assertTrue(user.profile.is_pro)

        sub = Subscription.objects.get(user=user)
        expected_min = before + timedelta(days=364)
        expected_max = after + timedelta(days=366)
        self.assertGreater(sub.expires_at, expected_min)
        self.assertLess(sub.expires_at, expected_max)

    def test_monthly_subscription_still_grants_30_days(self):
        from payments.views import _activate_subscription

        user = User.objects.create_user("monthlyuser", password="pass")
        product = _make_pro_monthly()
        order = self._make_order(product, user)

        before = timezone.now()
        _activate_subscription(order)
        after = timezone.now()

        sub = Subscription.objects.get(user=user)
        expected_min = before + timedelta(days=29)
        expected_max = after + timedelta(days=31)
        self.assertGreater(sub.expires_at, expected_min)
        self.assertLess(sub.expires_at, expected_max)

    def test_annual_subscription_sets_profile_tier(self):
        from payments.views import _activate_subscription

        user = User.objects.create_user("tieruser", password="pass")
        product = _make_pro_annual()
        order = self._make_order(product, user)

        _activate_subscription(order)

        user.refresh_from_db()
        self.assertEqual(user.profile.tier, "pro")
