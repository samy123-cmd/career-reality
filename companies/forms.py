from django import forms
from .models import Company, CompanyReview


class CompanyReviewForm(forms.ModelForm):
    """Structured review form for anonymous company reviews."""

    class Meta:
        model = CompanyReview
        fields = [
            "role_title", "role_level", "employment_status", "tenure_months",
            "rating_overall", "rating_salary", "rating_culture",
            "rating_growth", "rating_worklife", "rating_management",
            "pros", "cons", "advice_to_management",
            "would_rejoin", "biggest_lie",
        ]
        widgets = {
            "role_title": forms.TextInput(attrs={"placeholder": "e.g. Senior Software Engineer", "class": "cr-input"}),
            "tenure_months": forms.NumberInput(attrs={"placeholder": "e.g. 18", "min": 1, "max": 600, "class": "cr-input"}),
            "pros": forms.Textarea(attrs={"rows": 4, "placeholder": "What did you genuinely like?", "class": "cr-input"}),
            "cons": forms.Textarea(attrs={"rows": 4, "placeholder": "What made you want to leave?", "class": "cr-input"}),
            "advice_to_management": forms.Textarea(attrs={"rows": 3, "placeholder": "What should leadership change?", "class": "cr-input"}),
            "biggest_lie": forms.TextInput(attrs={"placeholder": "e.g. 'We value work-life balance'", "class": "cr-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if "rating_" in field_name:
                self.fields[field_name].widget = forms.RadioSelect(
                    choices=CompanyReview.RATING_CHOICES,
                )
