from django.db import models
from django.utils.text import slugify


class Company(models.Model):
    """
    Structured company profile — aggregates salary data, layoff reports,
    and community-sourced intelligence into one canonical entity.
    """

    SECTOR_CHOICES = [
        ("service", "IT Services / Consulting"),
        ("product", "Product Company"),
        ("startup", "Startup (< 3 years)"),
        ("unicorn", "Unicorn / Big Tech"),
        ("mnc_captive", "MNC Captive Centre"),
        ("bfsi", "BFSI / Fintech"),
        ("ecommerce", "E-Commerce"),
        ("edtech", "EdTech"),
        ("healthtech", "HealthTech"),
        ("other", "Other"),
    ]

    SIZE_CHOICES = [
        ("1-50", "1–50 employees"),
        ("51-200", "51–200 employees"),
        ("201-1000", "201–1,000 employees"),
        ("1001-5000", "1,001–5,000 employees"),
        ("5001-10000", "5,001–10,000 employees"),
        ("10001+", "10,001+ employees"),
    ]

    WORK_MODE_CHOICES = [
        ("office", "Office-first"),
        ("hybrid", "Hybrid"),
        ("remote", "Remote-first"),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    logo_url = models.URLField(blank=True, help_text="URL to company logo (Clearbit/brand)")
    website = models.URLField(blank=True)
    sector = models.CharField(max_length=30, choices=SECTOR_CHOICES, db_index=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)
    headquarters = models.CharField(max_length=100, blank=True, help_text="e.g. Bangalore, India")
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief company description")

    # Work culture signals
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, blank=True)
    glassdoor_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    ambitionbox_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    # Aggregated stats (denormalized for performance — updated by signals/cron)
    avg_ctc = models.IntegerField(null=True, blank=True, help_text="Average CTC from submissions")
    salary_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    layoff_report_count = models.PositiveIntegerField(default=0)
    overall_score = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        help_text="Composite score 0-10 based on salary, culture, stability"
    )

    is_verified = models.BooleanField(default=False, help_text="Manually verified by editorial team")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["-salary_count", "name"]
        indexes = [
            models.Index(fields=["sector", "-salary_count"]),
            models.Index(fields=["-overall_score"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("company_detail", kwargs={"slug": self.slug})

    @property
    def stability_label(self):
        """Derive stability from recent layoff reports."""
        if self.layoff_report_count == 0:
            return "unknown"
        from analyzer.models import LayoffReport
        recent = LayoffReport.objects.filter(
            company_name__iexact=self.name
        ).order_by("-created_at").first()
        if recent:
            return recent.status
        return "unknown"


class CompanyReview(models.Model):
    """Anonymous company review — the career reality take on Glassdoor."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    ROLE_LEVEL_CHOICES = [
        ("intern", "Intern"),
        ("junior", "Junior (0–2 yrs)"),
        ("mid", "Mid (3–5 yrs)"),
        ("senior", "Senior (6–10 yrs)"),
        ("lead", "Lead / Manager"),
        ("director", "Director+"),
    ]

    EMPLOYMENT_STATUS = [
        ("current", "Current Employee"),
        ("former", "Former Employee"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="reviews")
    role_title = models.CharField(max_length=100)
    role_level = models.CharField(max_length=20, choices=ROLE_LEVEL_CHOICES)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS)
    tenure_months = models.PositiveIntegerField(help_text="Months at company")

    # Structured ratings (1–5 scale)
    rating_overall = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_salary = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_culture = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_growth = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_worklife = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_management = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    # Free text
    pros = models.TextField(help_text="What's good about working here?")
    cons = models.TextField(help_text="What's bad? Be honest.")
    advice_to_management = models.TextField(blank=True)

    # Career Reality signature: the question nobody else asks
    would_rejoin = models.BooleanField(help_text="Would you join this company again?")
    biggest_lie = models.CharField(
        max_length=300, blank=True,
        help_text="What did the company promise but never delivered?"
    )

    is_verified = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False, help_text="Flagged for moderation")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company", "-created_at"]),
            models.Index(fields=["company", "rating_overall"]),
        ]

    def __str__(self):
        return f"{self.company.name} — {self.role_title} ({self.rating_overall}★)"

    @property
    def avg_rating(self):
        ratings = [
            self.rating_salary, self.rating_culture, self.rating_growth,
            self.rating_worklife, self.rating_management,
        ]
        return round(sum(ratings) / len(ratings), 1)


class Discussion(models.Model):
    """
    Anonymous peer discussion thread — the Fishbowl/Blind killer.
    No account required. Authenticated users can attach a verified badge.
    Company is optional: discussions can be company-specific or general career topics.
    """
    TOPIC_CHOICES = [
        ("salary", "Salary & Compensation"),
        ("culture", "Work Culture"),
        ("layoff", "Layoffs & Stability"),
        ("switching", "Job Switching"),
        ("career", "Career Growth"),
        ("interview", "Interview Experience"),
        ("wlb", "Work-Life Balance"),
        ("other", "Other"),
    ]

    company = models.ForeignKey(
        Company, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="discussions",
        help_text="Company this discussion is about (optional)",
    )
    # Anonymous identity — auto-generated handle like "Engineer#4821"
    anonymous_handle = models.CharField(max_length=50, blank=True)
    # Optional verified user link (null for truly anonymous posts)
    user = models.ForeignKey(
        "auth.User", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="discussions",
    )

    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, default="other", db_index=True)
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="The full question or discussion post")
    role = models.CharField(max_length=100, blank=True, help_text="e.g. Senior Engineer at a product company")

    upvotes = models.PositiveIntegerField(default=0, db_index=True)
    is_pinned = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company", "-created_at"]),
            models.Index(fields=["topic", "-upvotes"]),
            models.Index(fields=["-upvotes", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title[:60]} [{self.topic}]"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("discussion_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.anonymous_handle:
            import random
            handles = ["Engineer", "Manager", "Designer", "Analyst", "Developer", "PM", "SDE", "Lead"]
            self.anonymous_handle = f"{random.choice(handles)}#{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)


class DiscussionReply(models.Model):
    """A reply to a Discussion thread."""

    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name="replies"
    )
    anonymous_handle = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(
        "auth.User", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="discussion_replies",
    )
    body = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["discussion", "created_at"]),
        ]

    def __str__(self):
        return f"Reply to '{self.discussion.title[:40]}' by {self.anonymous_handle}"

    def save(self, *args, **kwargs):
        if not self.anonymous_handle:
            import random
            handles = ["Engineer", "Manager", "Designer", "Analyst", "Developer", "PM", "SDE", "Lead"]
            self.anonymous_handle = f"{random.choice(handles)}#{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
