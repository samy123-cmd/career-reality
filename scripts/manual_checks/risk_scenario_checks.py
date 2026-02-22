import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from analyzer.logic import RiskCalculator


SCENARIOS = [
    {
        "id": "A1",
        "name": "IT Services, Manager Pressure, 90-Day Notice, No Offer",
        "inputs": {
            "company_type": "service",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "90_days",
            "current_situation": "manager_bad",
            "has_offer": "no",
        },
        "expected": "medium",
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
            "has_offer": "no",
        },
        "expected": "high",
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
            "has_offer": "yes",
        },
        "expected": "low",
    },
    {
        "id": "B1",
        "name": "Service Company, HR Escalation, Bond Unclear",
        "inputs": {
            "company_type": "service",
            "role_level": "ic",
            "bond_status": "bond_unclear",
            "notice_period": "60_days",
            "current_situation": "hr_bad",
            "has_offer": "no",
        },
        "expected": "high",
    },
    {
        "id": "B2",
        "name": "Product Startup, Offer in Hand, Manager Pressure",
        "inputs": {
            "company_type": "product",
            "role_level": "senior_ic",
            "bond_status": "no_bond",
            "notice_period": "30_days",
            "current_situation": "manager_bad",
            "has_offer": "yes",
        },
        "expected": "medium",
    },
    {
        "id": "B3",
        "name": "Small Firm, Voluntary Evaluation, No Offer",
        "inputs": {
            "company_type": "small_indian",
            "role_level": "ic",
            "bond_status": "no_bond",
            "notice_period": "30_days",
            "current_situation": "evaluating",
            "has_offer": "no",
        },
        "expected": "medium",
    },
    {
        "id": "C1",
        "name": "Contradictory Inputs: Offer + HR Warning",
        "inputs": {
            "company_type": "service",
            "role_level": "senior_ic",
            "bond_status": "no_bond",
            "notice_period": "60_days",
            "current_situation": "hr_bad",
            "has_offer": "yes",
        },
        "expected": "high",
    },
    {
        "id": "C2",
        "name": "Friendly Context But Notice > 90",
        "inputs": {
            "company_type": "product",
            "role_level": "manager",
            "bond_status": "no_bond",
            "notice_period": "more_90",
            "current_situation": "evaluating",
            "has_offer": "no",
        },
        "expected": "medium",
    },
    {
        "id": "C3",
        "name": "MNC Captive, Bond With Penalty",
        "inputs": {
            "company_type": "mnc_captive",
            "role_level": "ic",
            "bond_status": "bond_penalty",
            "notice_period": "60_days",
            "current_situation": "evaluating",
            "has_offer": "no",
        },
        "expected": "medium",
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
            "has_offer": "no",
        },
        "expected": "high",
    },
]


def run_tests():
    calc = RiskCalculator()
    passed = 0
    failed = 0

    print("--- RUNNING SCENARIO VALIDATION ---")
    for scenario in SCENARIOS:
        result = calc.calculate(scenario["inputs"])
        actual = result["level"]

        if actual == scenario["expected"]:
            print(f"PASS {scenario['id']}: {scenario['name']} -> {actual}")
            passed += 1
        else:
            print(f"FAIL {scenario['id']}: {scenario['name']}")
            print(f"  Expected: {scenario['expected']}, Got: {actual}")
            print(f"  Reason: {result['risk_reason']}")
            failed += 1

    print(f"\nResult: {passed} PASSED, {failed} FAILED")


if __name__ == "__main__":
    run_tests()
