"""Stay vs Switch — decision framework with category breakdown."""

from __future__ import annotations

from dataclasses import dataclass, field

from analyzer import logic
from analyzer.services.salary_engine import get_salary_reality
from companies.models import Company
from companies.scoring import compute_company_reality_score
from core.models import CareerRealityIndexSnapshot


@dataclass
class StayVsSwitchResult:
    recommendation: str
    recommendation_label: str
    confidence: str
    confidence_pct: int
    financial_reasons: list[str]
    career_reasons: list[str]
    risk_score: int
    salary_percentile: int | None
    company_stability: str
    market_switch_difficulty: int
    categories: list[dict] = field(default_factory=list)
    timeline: str = ""
    improvements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in (
            "recommendation", "recommendation_label", "confidence", "confidence_pct",
            "financial_reasons", "career_reasons", "risk_score", "salary_percentile",
            "company_stability", "market_switch_difficulty", "categories", "timeline", "improvements",
        )}


def _latest_switch_difficulty() -> int:
    snap = CareerRealityIndexSnapshot.objects.order_by("-month_date").first()
    return snap.switch_difficulty if snap else 55


def analyze_stay_vs_switch(
    *,
    role: str,
    yoe: float,
    city: str,
    company_type: str,
    current_ctc: int,
    company: Company | None = None,
    has_offer: bool = False,
    offer_ctc: int | None = None,
    wizard_data: dict | None = None,
) -> StayVsSwitchResult:
    wizard_data = wizard_data or {}
    wizard_data.setdefault("company_type", company_type)
    wizard_data.setdefault("has_offer", "yes" if has_offer else "no")
    wizard_data.setdefault("ctc_vs_market", "at_market")

    risk = logic.RiskCalculator().calculate(wizard_data)
    risk_score = risk["score"]

    salary = get_salary_reality(role, yoe, city, company_type, current_ctc=current_ctc)
    stability_label = "unknown"
    company_score = 5.0
    if company:
        crs = compute_company_reality_score(company)
        company_score = crs.overall
        stability_label = crs.stability_label

    switch_difficulty = _latest_switch_difficulty()
    financial = []
    career = []

    comp_label = "At market"
    if salary.pay_label == "underpaid":
        comp_label = "Below market"
        financial.append(f"Underpaid ~{abs(salary.pay_delta_pct or 0)}% vs median ₹{salary.p50}L")
        financial.append(f"Realistic switch target: ₹{salary.realistic_next}L")
    elif salary.pay_label == "overpaid":
        comp_label = "Above market"
        financial.append("Above market — switching may mean a pay cut")
    else:
        financial.append(f"Near market median ₹{salary.p50}L")

    growth_label = "Steady"
    if wizard_data.get("current_situation") in ("stagnant", "burned_out"):
        growth_label = "Slowing"
    elif wizard_data.get("performance_status") == "high_performer":
        growth_label = "Strong"

    if offer_ctc and offer_ctc > current_ctc:
        hike = int((offer_ctc - current_ctc) / current_ctc * 100)
        financial.append(f"Offer ₹{offer_ctc}L is a {hike}% hike")

    if company_score < 5:
        career.append(f"Company score low ({company_score:.1f}/10)")
    elif company_score >= 7:
        career.append(f"Strong company ({company_score:.1f}/10) — internal growth viable")

    if stability_label in ("layoff_active", "at_risk", "freeze"):
        career.append(f"Stability: {stability_label}")
    if switch_difficulty >= 70:
        career.append(f"High switch difficulty ({switch_difficulty}/100)")
    elif switch_difficulty <= 40:
        career.append(f"Favourable market ({switch_difficulty}/100 difficulty)")

    switch_score = 0
    if salary.pay_label == "underpaid":
        switch_score += 2
    if offer_ctc and offer_ctc > current_ctc * 1.15:
        switch_score += 3
    elif has_offer:
        switch_score += 1
    if company_score < 5:
        switch_score += 2
    if stability_label in ("layoff_active", "at_risk"):
        switch_score += 3

    stay_score = 0
    if salary.pay_label == "overpaid":
        stay_score += 2
    if company_score >= 7:
        stay_score += 2
    if risk_score >= 60 and not has_offer:
        stay_score += 1

    readiness = "High" if (has_offer or switch_difficulty <= 45) else "Moderate" if switch_difficulty <= 65 else "Low"

    if switch_score >= stay_score + 2:
        rec, label = "switch", "Switch"
        confidence_pct = min(92, 65 + switch_score * 5)
    elif stay_score > switch_score + 1:
        rec, label = "stay", "Stay"
        confidence_pct = min(88, 60 + stay_score * 5)
    else:
        rec, label = "wait", "Wait"
        confidence_pct = 55

    confidence = "high" if confidence_pct >= 75 else "medium" if confidence_pct >= 60 else "low"

    categories = [
        {"name": "Compensation", "value": comp_label},
        {"name": "Career growth", "value": growth_label},
        {"name": "Market demand", "value": "Healthy" if switch_difficulty <= 55 else "Tight"},
        {"name": "Company risk", "value": stability_label.replace("_", " ").title()},
        {"name": "Switch readiness", "value": readiness},
    ]

    timeline = {
        "switch": "Begin interviewing within 1–3 months",
        "stay": "Revisit in 6 months — focus on internal scope",
        "wait": "Build leverage (offer, savings, skills) over 2–4 months",
    }[rec]

    improvements = []
    if salary.pay_label == "underpaid":
        improvements.append("Benchmark offers at ₹{}–{}L before resigning".format(salary.p50, salary.p75))
    if not has_offer:
        improvements.append("Secure at least one written offer before giving notice")
    improvements.append("Update resume with quantified impact from last 12 months")
    if switch_difficulty >= 65:
        improvements.append("Expand target companies beyond top-tier — market is selective")

    return StayVsSwitchResult(
        recommendation=rec,
        recommendation_label=label,
        confidence=confidence,
        confidence_pct=confidence_pct,
        financial_reasons=financial[:3],
        career_reasons=career[:3],
        risk_score=risk_score,
        salary_percentile=salary.percentile,
        company_stability=stability_label,
        market_switch_difficulty=switch_difficulty,
        categories=categories,
        timeline=timeline,
        improvements=improvements[:3],
    )
