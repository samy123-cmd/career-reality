import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from analyzer.logic import RiskCalculator


def test_guards():
    calc = RiskCalculator()
    print(f"Testing Risk Engine Version: {calc.RISK_ENGINE_VERSION}")

    # Guard 1: 90 Day Notice + Offer + MNC (Usually Low, but Guard should force Medium)
    s1 = {
        "company_type": "mnc_captive",
        "role_level": "ic",
        "bond_status": "no_bond",
        "notice_period": "90_days",
        "current_situation": "evaluating",
        "has_offer": "yes",
    }
    r1 = calc.calculate(s1)
    print(f"Test 1: 90d + Offer + MNC -> Expected: medium, Got: {r1['level']}")
    if r1["level"] == "low":
        print("FAILED: 90-day guard missed.")
    else:
        print("PASSED")

    # Guard 2: Small Firm + Bond (Any) should never be low.
    s2 = {
        "company_type": "small_indian",
        "role_level": "ic",
        "bond_status": "bond_unclear",
        "notice_period": "30_days",
        "current_situation": "evaluating",
        "has_offer": "yes",
    }
    r2 = calc.calculate(s2)
    print(f"Test 2: Small Firm + Bond + Offer -> Expected: medium/high, Got: {r2['level']}")
    if r2["level"] == "low":
        print("FAILED: Small+Bond guard missed.")
    else:
        print("PASSED")


if __name__ == "__main__":
    test_guards()
