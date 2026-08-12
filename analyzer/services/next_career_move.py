"""
Next Career Move — recommend highest-ROI paths based on skills, experience, and salary.
"""

from __future__ import annotations

from dataclasses import dataclass

from analyzer.services.ai_career_impact import analyze_ai_career_impact
from analyzer.services.salary_engine import get_salary_reality


@dataclass
class CareerPath:
    id: str
    title: str
    roi_score: float
    fit_score: float
    timeline: str
    summary: str
    actions: list[str]


@dataclass
class NextCareerMoveResult:
    paths: list[CareerPath]
    top_path: CareerPath | None

    def to_dict(self) -> dict:
        def _path(p: CareerPath) -> dict:
            return {
                "id": p.id,
                "title": p.title,
                "roi_score": round(p.roi_score, 1),
                "fit_score": round(p.fit_score, 1),
                "timeline": p.timeline,
                "summary": p.summary,
                "actions": p.actions,
            }

        return {
            "paths": [_path(p) for p in self.paths],
            "top_path": _path(self.top_path) if self.top_path else None,
        }


def recommend_next_moves(
    *,
    role: str,
    yoe: float,
    city: str,
    company_type: str,
    current_ctc: int,
    skills: list[str] | None = None,
) -> NextCareerMoveResult:
    skills = skills or []
    salary = get_salary_reality(role, yoe, city, company_type, current_ctc=current_ctc)
    ai = analyze_ai_career_impact(role)

    gap_to_p75 = max(0, salary.p75 - current_ctc)
    underpaid = salary.pay_label == "underpaid"

    paths: list[CareerPath] = []

    # Company switch
    switch_roi = min(10, 5 + gap_to_p75 / 5) if underpaid else 4.0
    paths.append(CareerPath(
        id="company_switch",
        title="Company Switch",
        roi_score=switch_roi,
        fit_score=8.0 if underpaid else 5.0,
        timeline="3–6 months",
        summary=f"Target ₹{salary.realistic_next}L (p75) via lateral move to product/GCC.",
        actions=[
            "Update resume with quantified impact metrics",
            "Target 15–25% hike companies in your sector",
            "Line up 2–3 offers before resigning",
        ],
    ))

    # Internal promotion
    promo_roi = 6.0 if company_type in ("product", "unicorn", "mnc_captive") else 4.5
    paths.append(CareerPath(
        id="promotion",
        title="Internal Promotion",
        roi_score=promo_roi,
        fit_score=7.0 if yoe >= 4 else 5.0,
        timeline="6–12 months",
        summary="Build scope evidence for next level calibration.",
        actions=[
            "Own a cross-team initiative with measurable outcome",
            "Document Staff/Lead scope in writing with manager",
            "Get peer endorsements before appraisal cycle",
        ],
    ))

    # GCC move
    gcc_roi = 7.5 if company_type == "service" else 5.5
    paths.append(CareerPath(
        id="gcc",
        title="Move to GCC / Captive",
        roi_score=gcc_roi,
        fit_score=7.5 if yoe >= 3 else 5.0,
        timeline="4–8 months",
        summary="GCC roles often pay 20–40% premium over IT services at same YOE.",
        actions=[
            "Target platform, security, or data roles in captives",
            "Prepare system design + ownership stories",
            "Factor 3–4 day RTO into commute/rent math",
        ],
    ))

    # Management track
    mgmt_fit = 6.0 if yoe >= 6 else 3.0
    paths.append(CareerPath(
        id="management",
        title="Management Track",
        roi_score=5.5,
        fit_score=mgmt_fit,
        timeline="12–18 months",
        summary="People leadership path — comp ceiling higher but IC optionality reduces.",
        actions=[
            "Take on informal mentoring and hiring loop participation",
            "Run a team ritual (standup, retro, planning)",
            "Read management craft — not just tech blogs",
        ],
    ))

    # Staff / Architecture
    arch_fit = 8.0 if yoe >= 7 else 4.0
    paths.append(CareerPath(
        id="staff_architecture",
        title="Staff / Architecture",
        roi_score=7.0,
        fit_score=arch_fit,
        timeline="12–24 months",
        summary="Highest IC ceiling — requires multi-team scope and system design depth.",
        actions=[
            "Lead an architecture decision record (ADR) for a real trade-off",
            "Present tech strategy to leadership",
            "Build T-shaped depth in one domain + breadth in adjacent systems",
        ],
    ))

    # AI upskill
    ai_roi = 8.0 if ai.ai_risk_score >= 50 else 5.0
    paths.append(CareerPath(
        id="ai_upskill",
        title="AI / GenAI Upskill",
        roi_score=ai_roi,
        fit_score=7.0,
        timeline="3–9 months",
        summary=f"AI risk score {ai.ai_risk_score}/100 — upskilling reduces exposure and opens premium roles.",
        actions=ai.skills_to_learn[:3],
    ))

    paths.sort(key=lambda p: p.roi_score * 0.6 + p.fit_score * 0.4, reverse=True)
    return NextCareerMoveResult(paths=paths, top_path=paths[0] if paths else None)
