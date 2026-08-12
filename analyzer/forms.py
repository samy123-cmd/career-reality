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
    confirm_payslip = forms.BooleanField(
        required=False,
        label="I confirm this matches my offer letter or payslip",
    )
    source = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())


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


# ─── New Career Tools Forms ───────────────────────────────────────────────────

class SalaryRealityEngineForm(forms.Form):
    role = forms.CharField(max_length=100, label="Job Role", initial="Software Engineer")
    experience_years = forms.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        label="Years of Experience",
    )
    city = forms.CharField(max_length=50, label="City", initial="Bengaluru")
    company_type = forms.ChoiceField(
        choices=[("", "Any")] + list(SalarySubmission.COMPANY_TYPES),
        required=False,
        label="Company Type",
    )
    current_ctc = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(500)],
        label="Your Current CTC (LPA, optional)",
        help_text="Enter in lakhs, e.g. 18 for ₹18L",
    )


class OfferAnalyzerForm(forms.Form):
    role = forms.CharField(max_length=100, label="Role")
    experience_years = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])

    offer_a_company = forms.CharField(max_length=150, label="Offer A — Company")
    offer_a_ctc = forms.IntegerField(label="Offer A — CTC (LPA)")
    offer_a_city = forms.CharField(max_length=50, required=False)
    offer_a_fixed_pct = forms.IntegerField(initial=70, min_value=40, max_value=100)
    offer_a_variable_pct = forms.IntegerField(initial=10, min_value=0, max_value=50)
    offer_a_commute = forms.IntegerField(required=False, label="Commute (minutes)")
    offer_a_wlb = forms.IntegerField(required=False, min_value=1, max_value=5, label="WLB rating 1-5")

    offer_b_company = forms.CharField(max_length=150, label="Offer B — Company")
    offer_b_ctc = forms.IntegerField(label="Offer B — CTC (LPA)")
    offer_b_city = forms.CharField(max_length=50, required=False)
    offer_b_fixed_pct = forms.IntegerField(initial=70, min_value=40, max_value=100)
    offer_b_variable_pct = forms.IntegerField(initial=10, min_value=0, max_value=50)
    offer_b_commute = forms.IntegerField(required=False, label="Commute (minutes)")
    offer_b_wlb = forms.IntegerField(required=False, min_value=1, max_value=5, label="WLB rating 1-5")


class StayVsSwitchForm(forms.Form):
    role = forms.CharField(max_length=100, initial="Software Engineer")
    experience_years = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    city = forms.CharField(max_length=50, initial="Bengaluru")
    company_type = forms.ChoiceField(choices=copy.COMPANY_TYPES)
    company_name = forms.CharField(max_length=150, required=False)
    current_ctc = forms.IntegerField(label="Current CTC (LPA)")
    has_offer = forms.ChoiceField(choices=copy.OFFER_STATUS, required=False, initial="no")
    offer_ctc = forms.IntegerField(required=False, label="Offer CTC (LPA)")
    company_type_wizard = forms.ChoiceField(choices=copy.COMPANY_TYPES, required=False)
    role_level = forms.ChoiceField(choices=copy.ROLE_LEVELS, required=False, initial="ic")
    tenure_band = forms.ChoiceField(choices=copy.TENURE_BANDS, required=False, initial="18m_3y")
    bond_status = forms.ChoiceField(choices=copy.BOND_STATUS, required=False, initial="no_bond")
    notice_period = forms.ChoiceField(choices=copy.NOTICE_PERIODS, required=False, initial="90_days")
    ctc_vs_market = forms.ChoiceField(choices=copy.CTC_VS_MARKET, required=False, initial="at_market")
    current_situation = forms.ChoiceField(choices=copy.CURRENT_SITUATION, required=False, initial="evaluating")
    performance_status = forms.ChoiceField(choices=copy.PERFORMANCE_STATUS, required=False, initial="good")


class AICareerImpactForm(forms.Form):
    job_title = forms.CharField(max_length=100, label="Your Job Title")


class NextCareerMoveForm(forms.Form):
    role = forms.CharField(max_length=100, initial="Software Engineer")
    experience_years = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    city = forms.CharField(max_length=50, initial="Bengaluru")
    company_type = forms.ChoiceField(choices=copy.COMPANY_TYPES)
    current_ctc = forms.IntegerField(label="Current CTC (LPA)")
    skills = forms.CharField(required=False, label="Skills (comma-separated)")


class AskCareerRealityForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "I make ₹18L at TCS with 6 YOE — should I take ₹23L at a startup?"}),
        max_length=1000,
        label="Your question",
    )


class CareerProfileForm(forms.Form):
    role = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100, required=False)
    experience_years = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    city = forms.CharField(max_length=50)
    company_type = forms.ChoiceField(choices=copy.COMPANY_TYPES)
    current_ctc = forms.IntegerField(label="Current CTC (LPA)")
    company_name = forms.CharField(max_length=150, required=False)
    skills = forms.CharField(required=False, label="Skills (comma-separated)")


class CareerSnapshotForm(forms.Form):
    recorded_at = forms.DateField()
    title = forms.CharField(max_length=100)
    ctc = forms.IntegerField(label="CTC (LPA)")
    company_name = forms.CharField(max_length=150, required=False)
    skills = forms.CharField(required=False)
