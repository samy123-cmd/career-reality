"""
Offer Analyzer — compare two job offers across salary, variable, commute, WLB, stability, growth, risk.
"""

from __future__ import annotations

from dataclasses import dataclass

from companies.models import Company
from companies.scoring import compute_company_reality_score
from analyzer.services.salary_engine import get_salary_reality


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
    city: str = ""
    commute_minutes: int | None = None
    work_mode: str = "hybrid"
    wlb_rating: int | None = None  # 1-5 user estimate


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


@dataclass
class OfferComparisonResult:
    offer_a: OfferScore
    offer_b: OfferScore
    verdict: str  # offer_a | offer_b | too_close
    verdict_label: str
    reasoning: list[str]

    def to_dict(self) -> dict:
        def _score_dict(s: OfferScore) -> dict:
            return {
                "label": s.label,
                "total_comp": s.total_comp,
                "overall": round(s.overall, 1),
                "stability": round(s.stability_score, 1),
                "market_fit": round(s.market_fit_score, 1),
                "wlb": round(s.wlb_score, 1),
                "commute": round(s.commute_score, 1),
                "growth": round(s.growth_score, 1),
                "details": s.details,
            }

        return {
            "offer_a": _score_dict(self.offer_a),
            "offer_b": _score_dict(self.offer_b),
            "verdict": self.verdict,
            "verdict_label": self.verdict_label,
            "reasoning": self.reasoning,
        }


def _effective_comp(offer: OfferInput) -> int:
    fixed = offer.ctc * offer.fixed_pct // 100
    variable = offer.ctc * offer.variable_pct // 100 * 70 // 100  # 70% expected payout
    esop_annual = offer.esop_value // 4 if offer.esop_value else 0
    return fixed + variable + esop_annual


def _score_offer(offer: OfferInput, yoe: float = 5) -> OfferScore:
    details = []
    total_comp = _effective_comp(offer)
    details.append(f"Effective annual comp ~₹{total_comp}L (fixed + expected variable + ESOP)")

    stability_score = 5.0
    growth_score = 5.0
    if offer.company:
        crs = compute_company_reality_score(offer.company)
        for dim in crs.dimensions:
            if dim.name == "stability":
                stability_score = dim.score
            if dim.name == "growth":
                growth_score = dim.score
        details.append(f"Company Reality Score: {crs.overall:.1f}/10")
    else:
        details.append("Company not in database — stability estimated conservatively")

    market = get_salary_reality(offer.role, yoe, offer.city or "Bengaluru", current_ctc=offer.ctc)
    if market.pay_label == "underpaid":
        market_fit = 8.0
    elif market.pay_label == "at_market":
        market_fit = 6.5
    elif market.pay_label == "overpaid":
        market_fit = 9.0
    else:
        market_fit = 6.0
    details.append(f"Market position: {market.pay_label or 'unknown'} (p50 ₹{market.p50}L)")

    wlb_score = (offer.wlb_rating or 3) * 2
    if offer.work_mode == "remote":
        wlb_score = min(10, wlb_score + 1)
        details.append("Remote work mode bonus")
    elif offer.work_mode == "office":
        wlb_score = max(1, wlb_score - 1)

    commute = offer.commute_minutes or 45
    if commute <= 30:
        commute_score = 9.0
    elif commute <= 60:
        commute_score = 7.0
    elif commute <= 90:
        commute_score = 5.0
    else:
        commute_score = 3.0
    details.append(f"Commute: {commute} min → score {commute_score:.0f}/10")

    overall = (
        total_comp / 50 * 0.30
        + stability_score * 0.20
        + market_fit * 0.15
        + wlb_score * 0.15
        + commute_score * 0.10
        + growth_score * 0.10
    )
    overall = min(10, overall)

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
    )


def compare_offers(offer_a: OfferInput, offer_b: OfferInput, yoe: float = 5) -> OfferComparisonResult:
    score_a = _score_offer(offer_a, yoe)
    score_b = _score_offer(offer_b, yoe)

    diff = abs(score_a.overall - score_b.overall)
    reasoning = []

    if score_a.total_comp != score_b.total_comp:
        higher = offer_a.label if score_a.total_comp > score_b.total_comp else offer_b.label
        reasoning.append(
            f"{higher} wins on effective compensation "
            f"(₹{max(score_a.total_comp, score_b.total_comp)}L vs ₹{min(score_a.total_comp, score_b.total_comp)}L)."
        )

    if abs(score_a.stability_score - score_b.stability_score) >= 1.5:
        safer = offer_a.label if score_a.stability_score > score_b.stability_score else offer_b.label
        reasoning.append(f"{safer} has stronger company stability signals.")

    if diff < 0.5:
        verdict = "too_close"
        verdict_label = "Too close to call — weigh non-financial factors"
        reasoning.append("Scores are within 0.5 points. Visit both teams, check manager quality, and validate ESOP terms.")
    elif score_a.overall > score_b.overall:
        verdict = "offer_a"
        verdict_label = f"Take {offer_a.label}"
        reasoning.append(f"{offer_a.label} scores {score_a.overall:.1f} vs {score_b.overall:.1f} overall.")
    else:
        verdict = "offer_b"
        verdict_label = f"Take {offer_b.label}"
        reasoning.append(f"{offer_b.label} scores {score_b.overall:.1f} vs {score_a.overall:.1f} overall.")

    return OfferComparisonResult(
        offer_a=score_a,
        offer_b=score_b,
        verdict=verdict,
        verdict_label=verdict_label,
        reasoning=reasoning,
    )
