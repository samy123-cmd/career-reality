from django import forms
from . import copy

class Step1Form(forms.Form):
    company_type = forms.ChoiceField(
        choices=copy.COMPANY_TYPES, 
        widget=forms.RadioSelect, 
        label="Company type"
    )
    role_level = forms.ChoiceField(
        choices=copy.ROLE_LEVELS, 
        widget=forms.RadioSelect, 
        label="Your role level"
    )

class Step2Form(forms.Form):
    bond_status = forms.ChoiceField(
        choices=copy.BOND_STATUS, 
        widget=forms.RadioSelect, 
        label="Bond status"
    )
    notice_period = forms.ChoiceField(
        choices=copy.NOTICE_PERIODS, 
        widget=forms.RadioSelect, 
        label="Notice period"
    )

class Step3Form(forms.Form):
    current_situation = forms.ChoiceField(
        choices=copy.CURRENT_SITUATION, 
        widget=forms.RadioSelect, 
        label="What is happening right now?"
    )
    has_offer = forms.ChoiceField(
        choices=copy.OFFER_STATUS, 
        widget=forms.RadioSelect, 
        label="Offer in hand?"
    )
