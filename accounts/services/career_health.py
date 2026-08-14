"""Career Health composite score for My Career Reality dashboard."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CareerHealthResult:
    overall: int
    indicators: list[dict]
    biggest_opportunity: str
    biggest_risk: str
    recommended_move: str


def compute_career_health(
    *,
    salary_insight,
    company_score=None,
    stay_switch=None,
    ai_impact=None,
    latest_snapshot=None,
) -> CareerHealthResult | None:
    if not salary_insight:
        return None

    scores = {}
    indicators = []

    # Salary position (0-100)
    pct = salary_insight.percentile or 50
    sal_score = min(100, max(20, pct))
    scores["salary"] = sal_score
    indicators.append({"name": "Salary Position", "score": sal_score, "label": salary_insight.pay_label or "Unknown"})

    # Company risk
    if company_score:
        comp_risk = int(company_score.overall * 10)
        scores["company"] = comp_risk
        indicators.append({"name": "Company Stability", "score": comp_risk, "label": company_score.stability_label})
    else:
        scores["company"] = 55
        indicators.append({"name": "Company Stability", "score": 55, "label": "Unknown"})

    # AI exposure (invert — lower risk = higher score)
    if ai_impact:
        ai_score = max(20, 100 - ai_impact.ai_risk_score)
        scores["ai"] = ai_score
        indicators.append({"name": "AI Resilience", "score": ai_score, "label": ai_impact.risk_label})
    else:
        scores["ai"] = 60
        indicators.append({"name": "AI Exposure", "score": 60, "label": "Not assessed"})

    # Momentum
    if latest_snapshot:
        mom = {"ahead": 80, "on_track": 65, "behind": 45}.get(latest_snapshot.peer_comparison, 60)
        scores["momentum"] = mom
        indicators.append({"name": "Career Momentum", "score": mom, "label": latest_snapshot.peer_comparison.title()})
    else:
        scores["momentum"] = 55
        indicators.append({"name": "Career Momentum", "score": 55, "label": "No snapshots"})

    # Switch readiness
    if stay_switch:
        sw = {"switch": 75, "wait": 55, "stay": 65}.get(stay_switch.recommendation, 60)
        scores["switch"] = sw
        indicators.append({"name": "Switch Readiness", "score": sw, "label": stay_switch.recommendation_label})
    else:
        scores["switch"] = 50
        indicators.append({"name": "Switch Readiness", "score": 50, "label": "Run analysis"})

    # Market demand proxy
    market = 70 if salary_insight.confidence in ("high", "medium") else 50
    scores["market"] = market
    indicators.append({"name": "Market Demand", "score": market, "label": salary_insight.data_source})

    overall = int(sum(scores.values()) / len(scores))

    opportunity = "You're positioned well — focus on scope and visibility for the next hike."
    if salary_insight.pay_label == "underpaid":
        opportunity = "You're below the estimated market range — a switch or strong appraisal case could add ₹{}–{}L.".format(
            salary_insight.p50, salary_insight.realistic_next
        )

    risk = "No acute risks detected from available data."
    if ai_impact and ai_impact.ai_risk_score >= 55:
        risk = "Your role has moderate-to-high AI exposure — prioritize {}.".format(ai_impact.skills_gaining[0].lower())
    elif company_score and company_score.overall < 5:
        risk = "Company stability is below average — monitor layoff signals and keep options open."

    move = "Run Stay vs Switch for a personalised timeline."
    if stay_switch:
        move = stay_switch.timeline
    elif salary_insight.pay_label == "underpaid":
        move = "Begin interviewing while building two higher-value skills."

    return CareerHealthResult(
        overall=overall,
        indicators=indicators[:6],
        biggest_opportunity=opportunity,
        biggest_risk=risk,
        recommended_move=move,
    )
