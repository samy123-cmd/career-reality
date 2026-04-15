from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from . import copy
from .models import SalarySubmission, LayoffReport


class SalarySubmissionForm(forms.Form):
    """Validates anonymous salary submissions before DB write."""
    role = forms.CharField(
        max_length=100,
        strip=True,
        label="Job Role",
    )
    experience_years = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(50.0)],
        label="Years of Experience",
    )
    company_name = forms.CharField(
        max_length=150,
        required=False,
        strip=True,
        label="Company Name (optional)",
        help_text="e.g. Infosys, Swiggy, your startup name",
    )
    company_type = forms.ChoiceField(
        choices=SalarySubmission.COMPANY_TYPES,
        label="Company Type",
    )
    ctc = forms.IntegerField(
        validators=[MinValueValidator(100_000), MaxValueValidator(100_000_000)],
        label="Annual CTC (INR)",
    )
    city = forms.CharField(
        max_length=50,
        strip=True,
        label="City",
    )
    tech_stack = forms.CharField(
        max_length=200,
        required=False,
        strip=True,
        label="Tech Stack (optional)",
    )


class LayoffReportForm(forms.Form):
    """Validates anonymous layoff/freeze reports before DB write."""
    company_name = forms.CharField(
        max_length=100,
        strip=True,
        label="Company Name",
    )
    status = forms.ChoiceField(
        choices=LayoffReport.STATUS_CHOICES,
        label="Current Status",
    )
    role_affected = forms.CharField(
        max_length=100,
        required=False,
        strip=True,
        label="Role / Team Affected (optional)",
    )
    location = forms.CharField(
        max_length=50,
        required=False,
        strip=True,
        label="Location (optional)",
    )
    details = forms.CharField(
        max_length=2000,
        required=False,
        strip=True,
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Context / Details (optional)",
    )


class Step1Form(forms.Form):
    company_type = forms.ChoiceField(
        choices=copy.COMPANY_TYPES,
        widget=forms.RadioSelect,
        label="Company type",
    )
    role_level = forms.ChoiceField(
        choices=copy.ROLE_LEVELS,
        widget=forms.RadioSelect,
        label="Your role level",
    )
    tenure_band = forms.ChoiceField(
        choices=copy.TENURE_BANDS,
        widget=forms.RadioSelect,
        label="How long have you been at this company?",
    )

class Step2Form(forms.Form):
    bond_status = forms.ChoiceField(
        choices=copy.BOND_STATUS,
        widget=forms.RadioSelect,
        label="Bond / service agreement",
    )
    notice_period = forms.ChoiceField(
        choices=copy.NOTICE_PERIODS,
        widget=forms.RadioSelect,
        label="Notice period in your contract",
    )
    ctc_vs_market = forms.ChoiceField(
        choices=copy.CTC_VS_MARKET,
        widget=forms.RadioSelect,
        label="Your CTC vs current market rate",
    )

class Step3Form(forms.Form):
    current_situation = forms.ChoiceField(
        choices=copy.CURRENT_SITUATION,
        widget=forms.RadioSelect,
        label="What is happening right now?",
    )
    performance_status = forms.ChoiceField(
        choices=copy.PERFORMANCE_STATUS,
        widget=forms.RadioSelect,
        label="Your performance standing",
    )
    has_offer = forms.ChoiceField(
        choices=copy.OFFER_STATUS,
        widget=forms.RadioSelect,
        label="Do you have an offer in hand?",
    )
