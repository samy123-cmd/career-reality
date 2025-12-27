import random
from . import copy

class RiskCalculator:
    """
    Refined Rule-Based Risk Engine.
    Implements 3-Layer Logic: Baseline -> Escalation -> Buffer.
    Output: Risk Level (Low/Medium/High) + Human-readable Reason (Rotational).
    """
    RISK_ENGINE_VERSION = "v1.0"

    def calculate(self, data):
        # 1. Unpack Inputs
        company = data.get('company_type')
        role = data.get('role_level')
        bond = data.get('bond_status')
        notice = data.get('notice_period')
        situation = data.get('current_situation')
        offer = data.get('has_offer') # 'yes' or 'no'

        # Mutable State for Layered Logic
        risk_level = 'low' # Default
        
        # Helper map for relative severity
        LEVEL_ORDER = {'low': 1, 'medium': 2, 'high': 3}
        
        def set_risk(new_level):
            nonlocal risk_level
            if LEVEL_ORDER[new_level] > LEVEL_ORDER[risk_level]:
                risk_level = new_level

        # --- LAYER 1: BASELINE RISK (Structural) ---
        if notice in ['90_days', 'more_90']:
            set_risk('medium')
        
        if company == 'small_indian':
             set_risk('medium')

        if company == 'service' and notice in ['90_days', 'more_90']:
             set_risk('medium')

        # --- LAYER 2: ESCALATION SIGNALS (Active Friction) ---
        # Bond Logic
        if bond == 'bond_penalty':
            if company == 'small_indian':
                set_risk('high')
            else:
                set_risk('medium')     
        elif bond == 'bond_unclear':
            set_risk('medium')

        # Situation Logic
        if situation == 'hr_bad':
            set_risk('high')
        elif situation == 'manager_bad':
            set_risk('medium')
        elif situation == 'unsafe':
            set_risk('high')

        # --- LAYER 3: BUFFERING FACTORS (Stabilizers) ---
        # Offer Buffer
        if offer == 'yes':
            if risk_level == 'medium' and situation not in ['manager_bad', 'hr_bad', 'unsafe'] and bond == 'no_bond':
                 risk_level = 'low'
        
        # Role Buffer
        if role == 'ic' and company == 'mnc_captive' and risk_level == 'medium' and situation == 'evaluating' and bond == 'no_bond':
             risk_level = 'low'
             
        # --- FINAL SAFETY GUARDS ---
        if situation == 'hr_bad' and risk_level == 'low':
             risk_level = 'medium'

        # Guard 2: 90-Day Notice can NEVER be Low
        if notice in ['90_days', 'more_90'] and risk_level == 'low':
             risk_level = 'medium'

        # Guard 3: Small Firm + Bond can NEVER be Low
        if company == 'small_indian' and bond != 'no_bond' and risk_level == 'low':
             risk_level = 'medium'

        # --- ROTATIONAL REASON SELECTION ---
        variants = copy.RISK_REASON_VARIANTS[risk_level]
        reason = random.choice(variants)

        # --- OUTPUT GENERATION ---
        result_meta = copy.RISK_LABELS[risk_level]
        expansion_text = copy.EXPANSION_TEXT[risk_level]
        
        # Generator warnings
        warnings = []
        if bond != 'no_bond': warnings.append(copy.WARNINGS['bond_pressure'])
        if notice in ['90_days', 'more_90']: warnings.append(copy.WARNINGS['market_risk'])
        if situation in ['manager_bad', 'hr_bad']: warnings.append(copy.WARNINGS['hr_escalation'])
        if company == 'small_indian': warnings.append(copy.WARNINGS['relieving_delay'])
        if situation == 'manager_bad': warnings.append(copy.WARNINGS['manager_hostility'])
        
        return {
            'level': risk_level,
            'label': result_meta['label'],
            'color': result_meta['color'],
            'summary': result_meta['summary'],
            'risk_reason': reason,
            'expansion_text': expansion_text, # Layer 2
            'warnings': list(set(warnings))[:5],
            'next_steps_intro': copy.NEXT_STEPS_INTRO,
            'disclaimer': copy.DISCLAIMER_TEXT
        }
