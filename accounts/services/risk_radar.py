"""Career Risk Radar — multi-axis risk aggregation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskRadarResult:
    overall_label: str
    overall_score: int
    items: list[dict]
    signals: list[str]
    actions: list[str]
    labels: list[dict]
    values_json: str


def compute_risk_radar(
    *,
    career,
    salary_insight=None,
    company_score=None,
    ai_impact=None,
    stay_switch=None,
    alerts=None,
) -> RiskRadarResult:
    alerts = alerts or []
    items = []

    company_risk = 50
    if company_score:
        company_risk = max(10, min(90, int(100 - company_score.overall * 10)))
    items.append({"name": "Company", "score": company_risk, "label": _risk_label(company_risk)})

    industry_risk = 45
    items.append({"name": "Industry", "score": industry_risk, "label": _risk_label(industry_risk)})

    role_risk = 50
    if stay_switch:
        role_risk = min(85, stay_switch.market_switch_difficulty)
    items.append({"name": "Role", "score": role_risk, "label": _risk_label(role_risk)})

    skill_risk = 55
    if salary_insight and salary_insight.pay_label == "underpaid":
        skill_risk = 65
    items.append({"name": "Skill", "score": skill_risk, "label": _risk_label(skill_risk)})

    ai_risk = 50
    if ai_impact:
        ai_risk = ai_impact.ai_risk_score
    items.append({"name": "AI", "score": ai_risk, "label": _risk_label(ai_risk)})

    comp_risk = 40
    if salary_insight:
        if salary_insight.pay_label == "underpaid":
            comp_risk = 60
        elif salary_insight.pay_label == "overpaid":
            comp_risk = 30
    items.append({"name": "Compensation", "score": comp_risk, "label": _risk_label(comp_risk)})

    promo_risk = 50
    items.append({"name": "Promotion", "score": promo_risk, "label": _risk_label(promo_risk)})

    overall = int(sum(i["score"] for i in items) / len(items))
    overall_label = _risk_label(overall)

    signals = []
    for a in alerts[:5]:
        signals.append(a.message)
    if not signals and company_score and company_score.overall < 5:
        signals.append("Company Reality Score below 5/10")
    if salary_insight and salary_insight.pay_label == "underpaid":
        signals.append("Compensation below market median")

    actions = [
        "Keep resume updated with last 12 months of quantified impact",
        "Build one skill that increases market leverage",
        "Monitor jobs in your city band monthly",
    ]
    if ai_risk >= 55:
        actions.insert(0, "Complete an AI upskilling sprint in the next 90 days")
    if company_risk >= 60:
        actions.insert(0, "Add target companies to watchlist and track layoff reports")

    import json
    labels = [{"name": i["name"], "x": 120, "y": 20 + items.index(i) * 0} for i in items]
    positions = [(120, 20), (210, 75), (210, 165), (120, 220), (30, 165), (30, 75)]
    for idx, item in enumerate(items):
        if idx < len(positions):
            labels[idx] = {"name": item["name"], "x": positions[idx][0], "y": positions[idx][1]}

    return RiskRadarResult(
        overall_label=overall_label,
        overall_score=overall,
        items=items,
        signals=signals,
        actions=actions,
        labels=labels,
        values_json=json.dumps([i["score"] for i in items]),
    )


def _risk_label(score: int) -> str:
    if score >= 70:
        return "Elevated"
    if score >= 45:
        return "Moderate"
    return "Low"
