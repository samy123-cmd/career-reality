"""Next Career Move — cross-discipline path recommendations."""

from __future__ import annotations

from dataclasses import dataclass, field

from analyzer.constants.career_taxonomy import normalize_role
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
    salary_potential: str = ""
    market_demand: str = "Moderate"
    difficulty: str = "Moderate"
    transferable_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    ai_durability: str = "Moderate"
    confidence: str = "Medium"


@dataclass
class NextCareerMoveResult:
    paths: list[CareerPath]
    top_path: CareerPath | None
    best_fit_reason: str = ""


PATH_LIBRARY: dict[str, list[dict]] = {
    "Software Engineer": [
        {"id": "product_engineer", "title": "Product Engineer", "timeline": "6–12 months", "skills": ["product sense", "full-stack depth"]},
        {"id": "engineering_manager", "title": "Engineering Manager", "timeline": "12–18 months", "skills": ["people leadership", "hiring"]},
        {"id": "staff_architecture", "title": "Staff / Architect", "timeline": "12–24 months", "skills": ["system design", "ADR ownership"]},
    ],
    "Data Engineer": [
        {"id": "data_architect", "title": "Data Architect", "timeline": "12–18 months", "skills": ["data modeling", "platform design"]},
        {"id": "ml_engineer", "title": "ML Engineer", "timeline": "9–15 months", "skills": ["ML pipelines", "feature stores"]},
    ],
    "Data Analyst": [
        {"id": "data_engineer", "title": "Data Engineer", "timeline": "9–12 months", "skills": ["SQL", "Python", "ETL"]},
        {"id": "business_analyst", "title": "Business Analyst", "timeline": "6–9 months", "skills": ["stakeholder mgmt", "requirements"]},
    ],
    "QA Engineer": [
        {"id": "sdet", "title": "SDET / Automation Engineer", "timeline": "6–9 months", "skills": ["test automation", "CI/CD"]},
        {"id": "product_analyst", "title": "Product / Business Analyst", "timeline": "9–12 months", "skills": ["analytics", "user research"]},
    ],
    "Business Analyst": [
        {"id": "product_manager", "title": "Product Manager", "timeline": "12–18 months", "skills": ["roadmap", "metrics"]},
        {"id": "program_manager", "title": "Program Manager", "timeline": "9–15 months", "skills": ["cross-team delivery"]},
    ],
    "Financial Analyst": [
        {"id": "fintech_pm", "title": "FinTech Product Analyst", "timeline": "12–18 months", "skills": ["payments", "compliance basics"]},
    ],
    "HR Business Partner": [
        {"id": "people_analytics", "title": "People Analytics", "timeline": "9–12 months", "skills": ["HRIS data", "SQL"]},
    ],
    "default": [
        {"id": "company_switch", "title": "Strategic Company Switch", "timeline": "3–6 months", "skills": ["interview prep", "offer negotiation"]},
        {"id": "promotion", "title": "Internal Promotion", "timeline": "6–12 months", "skills": ["scope expansion", "visibility"]},
        {"id": "gcc", "title": "Move to GCC / Captive", "timeline": "4–8 months", "skills": ["system design", "ownership stories"]},
        {"id": "management", "title": "Management Track", "timeline": "12–18 months", "skills": ["mentoring", "hiring"]},
        {"id": "ai_upskill", "title": "AI / GenAI Upskill", "timeline": "3–9 months", "skills": ["AI workflows", "automation"]},
    ],
}


def _paths_for_role(role: str) -> list[dict]:
    role = normalize_role(role)
    for key, paths in PATH_LIBRARY.items():
        if key.lower() in role.lower() or role.lower() in key.lower():
            return paths + PATH_LIBRARY["default"][:2]
    return PATH_LIBRARY["default"]


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
    role = normalize_role(role)
    salary = get_salary_reality(role, yoe, city, company_type, current_ctc=current_ctc)
    ai = analyze_ai_career_impact(role, experience_years=yoe)

    gap = max(0, salary.p75 - current_ctc)
    underpaid = salary.pay_label == "underpaid"
    paths: list[CareerPath] = []

    for spec in _paths_for_role(role):
        pid = spec["id"]
        if pid == "company_switch":
            roi = min(10, 5 + gap / 5) if underpaid else 4.0
            fit = 8.0 if underpaid else 5.0
            summary = f"Target ₹{salary.realistic_next}L via lateral move"
        elif pid == "gcc":
            roi = 7.5 if company_type == "service" else 5.5
            fit = 7.5 if yoe >= 3 else 5.0
            summary = "GCC roles often pay 20–40% premium over IT services"
        elif pid == "ai_upskill":
            roi = 8.0 if ai.ai_risk_score >= 50 else 5.0
            fit = 7.0
            summary = f"Reduce AI exposure (current risk {ai.ai_risk_score}/100)"
        elif pid == "promotion":
            roi = 6.0 if company_type in ("product", "unicorn", "mnc_captive") else 4.5
            fit = 7.0 if yoe >= 4 else 5.0
            summary = "Build scope evidence for next level"
        else:
            roi = 6.5
            fit = 6.0 + min(2, len(set(skills) & set(spec.get("skills", []))))
            summary = f"Transition toward {spec['title']} using transferable skills"

        transfer = [s for s in spec.get("skills", []) if any(s.lower() in sk.lower() for sk in skills)] or spec.get("skills", [])[:2]
        missing = [s for s in spec.get("skills", []) if s not in transfer][:2]

        paths.append(CareerPath(
            id=pid,
            title=spec["title"],
            roi_score=roi,
            fit_score=fit,
            timeline=spec["timeline"],
            summary=summary,
            actions=[
                f"Build proof of {spec.get('skills', ['scope'])[0]}",
                "Update LinkedIn and resume for this path",
                "Target 3 informational interviews in this track",
            ],
            salary_potential=f"₹{salary.p50}–{salary.p90}L band",
            market_demand="Strong" if roi >= 7 else "Moderate",
            difficulty="High" if fit < 5 else "Moderate",
            transferable_skills=transfer,
            missing_skills=missing,
            ai_durability="High" if ai.ai_risk_score < 40 else "Moderate",
            confidence="High" if fit >= 7 else "Medium",
        ))

    paths.sort(key=lambda p: p.roi_score * 0.6 + p.fit_score * 0.4, reverse=True)
    top = paths[0] if paths else None
    reason = ""
    if top:
        reason = f"Best ROI × fit for your profile ({role}, {yoe} YOE). {top.summary}"
    return NextCareerMoveResult(paths=paths[:5], top_path=top, best_fit_reason=reason)
