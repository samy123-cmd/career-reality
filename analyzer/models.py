from django.db import models

class AssessmentLog(models.Model):
    """
    Tracks anonymous usage of the Resignation Risk Analyzer.
    PRIVACY NOTICE: NO raw user inputs (bond, company type, etc.) are stored.
    Only derived signals and metadata are persisted for analytics.
    """
    risk_level = models.CharField(max_length=20, help_text="Calculated Risk (Low/Medium/High)")
    scenario_type = models.CharField(max_length=100, help_text="Primary driver (e.g. manager_pressure)")
    has_offer = models.BooleanField(default=False)
    tool_version = models.CharField(max_length=20, default="v1.0")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.risk_level} - {self.created_at.strftime('%Y-%m-%d')}"

class SalarySubmission(models.Model):
    """
    Crowdsourced anonymous salary data.
    "Glassdoor Killer" - Verified by community patterns, not intrusive logins.
    """
    COMPANY_TYPES = [
        ('service', 'Service Based (TCS/Infy/Wipro)'),
        ('product', 'Product Based (Swiggy/Zomato/Flipkart)'),
        ('startup', 'Early Stage Startup'),
        ('unicorn', 'Unicorn / Big Tech'),
    ]

    role = models.CharField(max_length=100, help_text="e.g. Senior Backend Engineer")
    experience_years = models.FloatField(help_text="Years of Experience")
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    ctc = models.IntegerField(help_text="Annual CTC in INR")
    in_hand = models.IntegerField(help_text="Monthly In-Hand (Optional)", null=True, blank=True)
    city = models.CharField(max_length=50)
    tech_stack = models.CharField(max_length=200, help_text="e.g. Java, React, AWS", blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.role} ({self.experience_years}y) - ₹{self.ctc}"

class LayoffReport(models.Model):
    """
    Crowdsourced anonymous reports on company stability.
    """
    STATUS_CHOICES = [
        ('hiring', 'Hiring Aggressively (Safe)'),
        ('freeze', 'Hiring Freeze'),
        ('rumor', 'Rumors of Layoffs'),
        ('layoff', 'Active Layoffs (Danger)'),
    ]

    company_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    role_affected = models.CharField(max_length=100, blank=True, help_text="e.g. Sales, Engineering")
    location = models.CharField(max_length=50, blank=True)
    details = models.TextField(blank=True, help_text="Context (optional)")
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.get_status_display()}"
