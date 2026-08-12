"""
Stay vs Switch Analyzer — current job + market → Stay / Switch / Wait recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass

from analyzer import logic
from analyzer.services.salary_engine import get_salary_reality
from companies.models import Company
from companies.scoring import compute_company_reality_score
from core.models import CareerRealityIndexSnapshot


@dataclass
class StayVsSwitchResult:
    recommendation: str  # stay | switch | wait
    recommendation_label: str
    confidence: str
    financial_reasons: list[str]
    career_reasons: list[str]
    risk_score: int
    salary_percentile: int | None
    company_stability: str
    market_switch_difficulty: int

    def to_dict(self) -> dict:
        return {
            "recommendation": self.recommendation,
            "recommendation_label": self.recommendation_label,
            "confidence": self.confidence,
            "financial_reasons": self.financial_reasons,
            "career_reasons": self.career_reasons,
            "risk_score": self.risk_score,
            "salary_percentile": self.salary_percentile,
            "company_stability": self.company_stability,
            "market_switch_difficulty": self.market_switch_difficulty,
        }


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
    """Combine salary, company, market, and risk signals into a career decision."""
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

    if salary.pay_label == "underpaid":
        financial.append(
            f"You appear underpaid by ~{abs(salary.pay_delta_pct or 0)}% vs market median (₹{salary.p50}L)."
        )
        financial.append(f"Realistic switch target: ₹{salary.realistic_next}L (p75 for your band).")
    elif salary.pay_label == "overpaid":
        financial.append(f"You're above market median — switching may mean a pay cut unless role changes.")
    else:
        financial.append(f"Compensation is near market median (₹{salary.p50}L).")

    if offer_ctc and offer_ctc > current_ctc:
        hike = int((offer_ctc - current_ctc) / current_ctc * 100)
        financial.append(f"Offer on table: ₹{offer_ctc}L is a {hike}% hike — strong financial case to switch.")
    elif has_offer and not offer_ctc:
        financial.append("You have an offer — quantify the hike before deciding.")

    if company_score < 5:
        career.append(f"Company Reality Score is low ({company_score:.1f}/10) — limited growth or stability.")
    elif company_score >= 7:
        career.append(f"Company scores well ({company_score:.1f}/10) — internal growth may beat a risky switch.")

    if stability_label in ("layoff_active", "at_risk", "freeze"):
        career.append(f"Company stability signal: {stability_label} — prioritize exit planning.")
    else:
        career.append("No acute layoff signals for your company in recent reports.")

    if switch_difficulty >= 70:
        career.append(f"Market switch difficulty is high ({switch_difficulty}/100) — secure offer before resigning.")
    elif switch_difficulty <= 40:
        career.append(f"Market is relatively open ({switch_difficulty}/100 switch difficulty) — good window to move.")

    if risk_score >= 65:
        career.append("Resignation risk is elevated — document everything and avoid hostile exits.")

    # Decision logic
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
    if switch_difficulty >= 75:
        switch_score -= 1

    stay_score = 0
    if salary.pay_label == "overpaid":
        stay_score += 2
    if company_score >= 7:
        stay_score += 2
    if stability_label in ("stable", "hiring"):
        stay_score += 1
    if risk_score >= 60 and not has_offer:
        stay_score += 1  # risky to leave without offer

    if switch_score >= stay_score + 2:
        rec, label = "switch", "Switch — financial and risk signals favour moving"
        confidence = "high" if switch_score >= 4 else "medium"
    elif stay_score > switch_score + 1:
        rec, label = "stay", "Stay — current position has more upside than risk"
        confidence = "medium"
    else:
        rec, label = "wait", "Wait — build leverage (offer, skills, savings) before deciding"
        confidence = "medium"

    return StayVsSwitchResult(
        recommendation=rec,
        recommendation_label=label,
        confidence=confidence,
        financial_reasons=financial[:3],
        career_reasons=career[:3],
        risk_score=risk_score,
        salary_percentile=salary.percentile,
        company_stability=stability_label,
        market_switch_difficulty=switch_difficulty,
    )
