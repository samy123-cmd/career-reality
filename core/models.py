from django.db import models


class NewsletterSubscriber(models.Model):
    """Store newsletter subscriber emails."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class CareerRealityIndexSnapshot(models.Model):
    """
    Monthly computed snapshot of the Career Reality Index.
    Replaces the hardcoded numbers in views.py.
    Populated by management command: python manage.py refresh_career_index
    """
    month = models.CharField(max_length=20, help_text="e.g. 'April 2026'")
    month_date = models.DateField(unique=True, help_text="First day of the month — used for ordering")

    # All scores are 0–100
    salary_pressure = models.PositiveSmallIntegerField(
        help_text="% of submissions reporting stagnant/declining CTC"
    )
    switch_difficulty = models.PositiveSmallIntegerField(
        help_text="Index of switching friction based on notice + bond signals"
    )
    layoff_risk = models.PositiveSmallIntegerField(
        help_text="% of layoff reports (freeze/rumor/layoff) in last 30 days"
    )
    overall = models.PositiveSmallIntegerField(
        help_text="Composite score — weighted average of the three signals"
    )

    # Metadata
    total_salary_submissions = models.PositiveIntegerField(default=0)
    total_layoff_reports = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-month_date"]
        verbose_name = "Career Reality Index Snapshot"
        verbose_name_plural = "Career Reality Index Snapshots"

    def __str__(self):
        return f"{self.month} — Overall: {self.overall}"
