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
