import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from analyzer.logic import RiskCalculator

# SCENARIO DATA
SCENARIOS = [
    # SET A — COMMON, HIGH-FREQUENCY CASES
    {
        "id": "A1",
        "name": "IT Services, Manager Pressure, 90-Day Notice, No Offer",
        "inputs": {
            "company_type": "service",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "90_days",
            "current_situation": "manager_bad",
            "has_offer": "no"
        },
        "expected": "medium"
    },
    {
        "id": "A2",
        "name": "Startup (<100), HR Warning, Bond With Penalty",
        "inputs": {
            "company_type": "small_indian",
            "role_level": "senior_ic",
            "bond_status": "bond_penalty",
            "notice_period": "60_days",
            "current_situation": "hr_bad",
            "has_offer": "no"
        },
        "expected": "high"
    },
    {
        "id": "A3",
        "name": "MNC Captive, No Pressure, Offer in Hand",
        "inputs": {
            "company_type": "mnc_captive",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "60_days",
            "current_situation": "evaluating",
            "has_offer": "yes"
        },
        "expected": "low"
    },

    # SET B — BORDERLINE / CONFUSING CASES
    {
        "id": "B1",
        "name": "Service Company, HR CC’d Email, Bond Unclear",
        "inputs": {
            "company_type": "service",
            "role_level": "ic",
            "bond_status": "bond_unclear",
            "notice_period": "60_days",
            "current_situation": "hr_bad",
            "has_offer": "no"
        },
        "expected": "high"
    },
    {
        "id": "B2",
        "name": "Product Startup, Offer in Hand, Manager Pressure Only",
        "inputs": {
            "company_type": "product",
            "role_level": "senior_ic",
            "bond_status": "no_bond",
            "notice_period": "30_days",
            "current_situation": "manager_bad",
            "has_offer": "yes"
        },
        "expected": "medium"
    },
    {
        "id": "B3",
        "name": "Small Firm, Voluntary Resignation, No Pressure Yet",
        "inputs": {
            "company_type": "small_indian",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "30_days",
            "current_situation": "evaluating", # mapped approximate 'voluntary' to evaluating/eval-risk if strictly distinct? 
            # Re-reading prompt: "current_situation: voluntary_resign_risk"
            # My current copy.py doesn't have 'voluntary_resign_risk', it has 'evaluating'.
            # I should map 'evaluating' close to it or update copy logic. 
            # Prompt says "voluntary_resign_risk" -> likely means 'evaluating' or 'unsafe'.
            # Let's assume 'evaluating' for "No pressure yet".
            # Wait, prompt B3 says "current_situation: voluntary_resign_risk". 
            # I must check my form choices. 
            # copy.py: ['manager_bad', 'hr_bad', 'unsafe', 'offer_hand', 'evaluating']
            # I will treat "voluntary_resign_risk" as 'evaluating' or add logic mapping.
            # But the logic expects exact keys from copy.py. 
            # I will use 'evaluating' but expect Medium for Small Firm even if evaluating?
            # Prompt B3 says "Expected Risk: Medium". 
            "current_situation": "evaluating",
            "has_offer": "no"
        },
        "expected": "medium"
    },

    # SET C — EDGE CASE STRESS TESTS
    {
        "id": "C1",
        "name": "Contradictory Inputs: Offer + HR Warning",
        "inputs": {
            "company_type": "service",
            "role_level": "senior_ic",
            "bond_status": "no_bond",
            "notice_period": "60_days",
            "current_situation": "hr_bad",
            "has_offer": "yes"
        },
        "expected": "high"
    },
    {
        "id": "C2",
        "name": "Manager Is Friendly, But Notice Is 120 Days",
        "inputs": {
            "company_type": "product",
            "role_level": "manager",
            "bond_status": "no_bond",
            "notice_period": "more_90",
            "current_situation": "evaluating",
            "has_offer": "no"
        },
        "expected": "medium"
    },
    {
        "id": "C3",
        "name": "MNC Captive, Bond With Penalty (Rare but Real)",
        "inputs": {
            "company_type": "mnc_captive",
            "role_level": "ic",
            "bond_status": "bond_penalty",
            "notice_period": "60_days",
            "current_situation": "evaluating",
            "has_offer": "no"
        },
        "expected": "medium"
    },
    {
        "id": "C4",
        "name": "HR Warning, Short Notice, No Bond",
        "inputs": {
            "company_type": "product",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "30_days",
            "current_situation": "hr_bad",
            "has_offer": "no"
        },
        "expected": "high"
    }
]

def run_tests():
    calc = RiskCalculator()
    passed = 0
    failed = 0

    print("--- RUNNING SCENARIO VALIDATION ---")
    for s in SCENARIOS:
        result = calc.calculate(s['inputs'])
        actual_level = result['level']
        
        if actual_level == s['expected']:
            print(f"✅ {s['id']}: PASS ({s['name']}) -> {actual_level}")
            passed += 1
        else:
            print(f"❌ {s['id']}: FAIL ({s['name']})")
            print(f"   Expected: {s['expected']}, Got: {actual_level}")
            print(f"   Reason: {result['risk_reason']}")
            failed += 1
            
    print(f"\nResult: {passed} PASSED, {failed} FAILED")

if __name__ == "__main__":
    run_tests()
