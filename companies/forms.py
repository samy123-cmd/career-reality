from django import forms
from .models import Company, CompanyReview, Discussion, DiscussionReply


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
                self.fields[field_name].choices = CompanyReview.RATING_CHOICES
        # Override would_rejoin as TypedChoiceField so "False" is valid (BooleanField rejects it)
        self.fields["would_rejoin"] = forms.TypedChoiceField(
            choices=[(True, "Yes"), (False, "No")],
            coerce=lambda x: x == "True" or x is True,
            widget=forms.RadioSelect,
            required=True,
        )


class DiscussionForm(forms.ModelForm):
    """Form for starting a new anonymous discussion thread."""

    class Meta:
        model = Discussion
        fields = ["topic", "title", "body", "role"]
        widgets = {
            "topic": forms.Select(attrs={"class": "cr-input"}),
            "title": forms.TextInput(attrs={
                "placeholder": "What's the real story? Be specific.",
                "class": "cr-input",
                "maxlength": 200,
            }),
            "body": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Share your honest experience or question. No company names in the title — use the company filter instead.",
                "class": "cr-input",
            }),
            "role": forms.TextInput(attrs={
                "placeholder": "e.g. 3yr SDE at product company (optional)",
                "class": "cr-input",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].required = False
        self.fields["body"].label = "Details"
        self.fields["title"].label = "Your question or topic"


class DiscussionReplyForm(forms.ModelForm):
    """Form for replying to a discussion thread."""

    class Meta:
        model = DiscussionReply
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Add your honest take. Anonymous, no login required.",
                "class": "cr-input",
            }),
        }
        labels = {"body": "Your reply"}
