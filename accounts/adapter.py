from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    """Custom allauth adapter — redirects new sign-ups to the onboarding page."""

    def get_signup_redirect_url(self, request):
        return reverse("onboarding")
