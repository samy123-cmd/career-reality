from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    TIER_CHOICES = [
        ("free", "Free"),
        ("pro", "Pro — ₹299/month"),
        ("team", "Team — ₹999/month"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default="free")
    subscription_expires_at = models.DateTimeField(null=True, blank=True)

    # Engagement signals (populated from tool usage — no raw PII)
    salary_submissions_count = models.PositiveIntegerField(default=0)
    assessments_count = models.PositiveIntegerField(default=0)
    last_risk_level = models.CharField(max_length=20, blank=True)  # low/medium/high
    last_company_type = models.CharField(max_length=50, blank=True)

    # Give-to-get salary unlock credits
    # Free users earn 3 credits per salary submission; each credit unlocks 1 full salary record.
    salary_credits = models.PositiveIntegerField(
        default=0,
        help_text="Credits earned by submitting salary data. 1 credit = unlock 1 salary record.",
    )

    # Newsletter
    newsletter_subscribed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} ({self.tier})"

    @property
    def is_pro(self):
        """True if user has an active Pro or Team subscription."""
        if self.tier in ("pro", "team"):
            if self.subscription_expires_at is None:
                return True  # Lifetime / manually granted
            return self.subscription_expires_at > timezone.now()
        return False

    @property
    def days_until_expiry(self):
        if self.subscription_expires_at:
            delta = self.subscription_expires_at - timezone.now()
            return max(0, delta.days)
        return None
