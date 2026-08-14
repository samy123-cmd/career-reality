"""
Offer Analyzer — compare two job offers with weighted priorities and outlook.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from companies.models import Company
from companies.scoring import compute_company_reality_score
from analyzer.services.salary_engine import get_salary_reality

DEFAULT_WEIGHTS = {
    "salary": 30,
    "stability": 20,
    "growth": 10,
    "wlb": 15,
    "commute": 10,
    "remote": 5,
    "brand": 5,
    "learning": 5,
}


@dataclass
class OfferInput:
    label: str
    company_name: str
    company: Company | None
    role: str
    ctc: int
    fixed_pct: int = 70
    variable_pct: int = 10
    esop_value: int = 0
    joining_bonus: int = 0
    retention_bonus: int = 0
    city: str = ""
    commute_minutes: int | None = None
    work_mode: str = "hybrid"
    office_days: int = 3
    wlb_rating: int | None = None
    notice_period_days: int = 90
    growth_potential: int = 3  # 1-5
    expected_hours: int | None = None


@dataclass
class OfferScore:
    label: str
    total_comp: int
    stability_score: float
    market_fit_score: float
    wlb_score: float
    commute_score: float
    growth_score: float
    overall: float
    details: list[str]
    dimensions: list[dict] = field(default_factory=list)


@dataclass
class OfferComparisonResult:
    offer_a: OfferScore
    offer_b: OfferScore
    verdict: str
    verdict_label: str
    reasoning: list[str]
    tradeoffs: dict
    outlook_2y: str
    outlook_5y: str
    score_a_display: int
    score_b_display: int

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "verdict_label": self.verdict_label,
            "reasoning": self.reasoning,
            "tradeoffs": self.tradeoffs,
            "outlook_2y": self.outlook_2y,
            "outlook_5y": self.outlook_5y,
            "score_a": self.score_a_display,
            "score_b": self.score_b_display,
        }


def _effective_comp(offer: OfferInput) -> int:
    fixed = offer.ctc * offer.fixed_pct // 100
    variable = offer.ctc * offer.variable_pct // 100 * 70 // 100
    esop_annual = offer.esop_value // 4 if offer.esop_value else 0
    bonus = (offer.joining_bonus + offer.retention_bonus) // 2
    return fixed + variable + esop_annual + bonus


def _score_offer(offer: OfferInput, yoe: float = 5) -> OfferScore:
    details = []
    total_comp = _effective_comp(offer)
    details.append(f"Predictable annual cash ~₹{total_comp}L")

    stability_score = 5.0
    growth_score = float(offer.growth_potential) * 2
    if offer.company:
        crs = compute_company_reality_score(offer.company)
        for dim in crs.dimensions:
            if dim.name == "stability":
                stability_score = dim.score
            if dim.name == "growth":
                growth_score = max(growth_score, dim.score)
        details.append(f"Company Reality Score {crs.overall:.1f}/10")

    market = get_salary_reality(offer.role, yoe, offer.city or "Bengaluru", current_ctc=offer.ctc)
    market_fit = {"underpaid": 8.0, "at_market": 6.5, "overpaid": 9.0}.get(market.pay_label or "", 6.0)

    wlb_score = (offer.wlb_rating or 3) * 2
    if offer.work_mode == "remote":
        wlb_score = min(10, wlb_score + 1.5)
    elif offer.work_mode == "office":
        wlb_score = max(1, wlb_score - 0.5)
    if offer.office_days <= 2:
        wlb_score = min(10, wlb_score + 0.5)

    commute = offer.commute_minutes or 45
    commute_score = 9.0 if commute <= 30 else 7.0 if commute <= 60 else 5.0 if commute <= 90 else 3.0

    dimensions = [
        {"label": "Comp", "score": min(10, total_comp / 5), "max": 10},
        {"label": "Stability", "score": stability_score, "max": 10},
        {"label": "Market fit", "score": market_fit, "max": 10},
        {"label": "WLB", "score": wlb_score, "max": 10},
        {"label": "Commute", "score": commute_score, "max": 10},
        {"label": "Growth", "score": growth_score, "max": 10},
    ]
    overall = sum(d["score"] for d in dimensions) / len(dimensions)

    return OfferScore(
        label=offer.label,
        total_comp=total_comp,
        stability_score=stability_score,
        market_fit_score=market_fit,
        wlb_score=wlb_score,
        commute_score=commute_score,
        growth_score=growth_score,
        overall=overall,
        details=details,
        dimensions=dimensions,
    )


def compare_offers(
    offer_a: OfferInput,
    offer_b: OfferInput,
    yoe: float = 5,
    weights: dict | None = None,
) -> OfferComparisonResult:
    score_a = _score_offer(offer_a, yoe)
    score_b = _score_offer(offer_b, yoe)
    w = weights or DEFAULT_WEIGHTS

    def weighted(s: OfferScore, o: OfferInput) -> float:
        comp_norm = min(100, s.total_comp * 2)
        return (
            comp_norm * w.get("salary", 30) / 100
            + s.stability_score * 10 * w.get("stability", 20) / 100
            + s.growth_score * 10 * w.get("growth", 10) / 100
            + s.wlb_score * 10 * w.get("wlb", 15) / 100
            + s.commute_score * 10 * w.get("commute", 10) / 100
            + (10 if o.work_mode == "remote" else 5) * w.get("remote", 5) / 100
            + s.market_fit_score * 10 * w.get("brand", 5) / 100
            + s.growth_score * 10 * w.get("learning", 5) / 100
        )

    wa = weighted(score_a, offer_a)
    wb = weighted(score_b, offer_b)
    display_a = min(99, max(40, int(wa)))
    display_b = min(99, max(40, int(wb)))

    reasoning = []
    tradeoffs = {"offer_a": [], "offer_b": []}

    if score_a.total_comp != score_b.total_comp:
        winner = offer_a.label if score_a.total_comp > score_b.total_comp else offer_b.label
        diff = abs(score_a.total_comp - score_b.total_comp)
        reasoning.append(f"₹{diff}L more predictable annual cash with {winner}")

    if score_a.stability_score > score_b.stability_score + 1:
        reasoning.append(f"{offer_a.label} has stronger stability signals")
        tradeoffs["offer_b"].append("Lower company stability score")
    elif score_b.stability_score > score_a.stability_score + 1:
        reasoning.append(f"{offer_b.label} has stronger stability signals")
        tradeoffs["offer_a"].append("Lower company stability score")

    if score_a.commute_score > score_b.commute_score + 1:
        tradeoffs["offer_b"].append("Longer commute")
    elif score_b.commute_score > score_a.commute_score + 1:
        tradeoffs["offer_a"].append("Longer commute")

    if score_a.growth_score > score_b.growth_score + 1:
        reasoning.append(f"{offer_a.label} offers stronger growth trajectory")
    elif score_b.growth_score > score_a.growth_score + 1:
        reasoning.append(f"{offer_b.label} offers stronger growth trajectory")

    diff = abs(display_a - display_b)
    if diff < 3:
        verdict, label = "too_close", "Too close to call — weigh team fit and learning"
        reasoning.append("Scores within 3 points — validate manager quality and ESOP terms in person.")
    elif display_a > display_b:
        verdict, label = "offer_a", f"{offer_a.label} wins"
        reasoning.append(f"Overall {display_a} vs {display_b} based on your priorities.")
    else:
        verdict, label = "offer_b", f"{offer_b.label} wins"
        reasoning.append(f"Overall {display_b} vs {display_a} based on your priorities.")

    winner_comp = max(score_a.total_comp, score_b.total_comp)
    outlook_2y = f"Expect ₹{winner_comp + 2}–{winner_comp + 5}L with typical annual hikes if you perform at median."
    outlook_5y = f"5-year ceiling ~₹{winner_comp + 12}–{winner_comp + 20}L depending on promotion velocity and sector."

    return OfferComparisonResult(
        offer_a=score_a,
        offer_b=score_b,
        verdict=verdict,
        verdict_label=label,
        reasoning=reasoning[:5],
        tradeoffs=tradeoffs,
        outlook_2y=outlook_2y,
        outlook_5y=outlook_5y,
        score_a_display=display_a,
        score_b_display=display_b,
    )
