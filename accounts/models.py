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
    salary_previews_used = models.PositiveIntegerField(default=0)
    salary_previews_month = models.CharField(max_length=7, blank=True, default="")

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


class CompanyWatchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_watchlist"
    )
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "company")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} watches {self.company.name}"


class LayoffAlertLog(models.Model):
    """Dedup: one alert per user per layoff report."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    layoff_report = models.ForeignKey("analyzer.LayoffReport", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "layoff_report")]

    def __str__(self):
        return f"Alert to {self.user.email} for report #{self.layoff_report_id}"


class CareerProfile(models.Model):
    """User career context for personalized dashboards and alerts."""

    COMPANY_TYPE_CHOICES = [
        ("service", "IT Services"),
        ("product", "Product Company"),
        ("mnc_captive", "MNC Captive / GCC"),
        ("startup", "Startup"),
        ("small_indian", "Small Indian Firm"),
        ("unicorn", "Unicorn / Big Tech"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="career_profile")
    role = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, blank=True)
    current_ctc = models.IntegerField(null=True, blank=True, help_text="Annual CTC in lakhs")
    company = models.ForeignKey(
        "companies.Company", null=True, blank=True, on_delete=models.SET_NULL
    )
    company_name = models.CharField(max_length=150, blank=True)
    skills = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CareerProfile: {self.user.email}"


class CareerSnapshot(models.Model):
    """Point-in-time career progression record."""

    PEER_COMPARISON = [
        ("ahead", "Ahead of peers"),
        ("on_track", "On track"),
        ("behind", "Falling behind"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="career_snapshots")
    recorded_at = models.DateField()
    title = models.CharField(max_length=100)
    ctc = models.IntegerField(help_text="Annual CTC in lakhs")
    company_name = models.CharField(max_length=150, blank=True)
    skills = models.JSONField(default=list, blank=True)
    salary_percentile = models.IntegerField(null=True, blank=True)
    peer_comparison = models.CharField(max_length=20, choices=PEER_COMPARISON, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.user.email} @ {self.recorded_at}: ₹{self.ctc}L"


class JobOffer(models.Model):
    """Saved job offer for comparison (Offer Analyzer)."""

    WORK_MODE = [
        ("office", "Office"),
        ("hybrid", "Hybrid"),
        ("remote", "Remote"),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="job_offers")
    session_key = models.CharField(max_length=64, blank=True)
    label = models.CharField(max_length=50, default="Offer")
    company_name = models.CharField(max_length=150)
    company = models.ForeignKey("companies.Company", null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=100)
    ctc = models.IntegerField()
    fixed_pct = models.IntegerField(default=70)
    variable_pct = models.IntegerField(default=10)
    esop_value = models.IntegerField(default=0)
    city = models.CharField(max_length=50, blank=True)
    commute_minutes = models.IntegerField(null=True, blank=True)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE, default="hybrid")
    wlb_rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class CareerAlert(models.Model):
    """Personalized career risk alerts."""

    ALERT_TYPES = [
        ("layoff", "Layoff Risk"),
        ("freeze", "Hiring Freeze"),
        ("salary_stagnation", "Salary Stagnation"),
        ("ai_disruption", "AI Disruption"),
        ("industry_decline", "Industry Decline"),
    ]
    SEVERITY = [
        ("info", "Info"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="career_alerts")
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY, default="info")
    message = models.TextField()
    source_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]


class AdvisorConversation(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="advisor_conversations")
    session_key = models.CharField(max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class AdvisorMessage(models.Model):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant")]

    conversation = models.ForeignKey(AdvisorConversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    citations = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
