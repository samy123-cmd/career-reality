"""AI Career Impact — expanded role analysis with action plan."""

from __future__ import annotations

from dataclasses import dataclass, field

from analyzer.constants.career_taxonomy import normalize_role

TITLE_RISK_MAP: dict[str, dict] = {
    "data entry": {"risk": 85, "demand": "declining"},
    "manual tester": {"risk": 78, "demand": "declining"},
    "qa": {"risk": 65, "demand": "stable"},
    "content writer": {"risk": 72, "demand": "declining"},
    "customer support": {"risk": 68, "demand": "stable"},
    "business analyst": {"risk": 55, "demand": "stable"},
    "financial analyst": {"risk": 48, "demand": "stable"},
    "operations": {"risk": 52, "demand": "stable"},
    "hr": {"risk": 45, "demand": "stable"},
    "recruiter": {"risk": 58, "demand": "declining"},
    "sales": {"risk": 40, "demand": "stable"},
    "marketing": {"risk": 50, "demand": "stable"},
    "frontend": {"risk": 45, "demand": "stable"},
    "backend": {"risk": 35, "demand": "growing"},
    "software engineer": {"risk": 38, "demand": "growing"},
    "devops": {"risk": 30, "demand": "growing"},
    "data engineer": {"risk": 32, "demand": "growing"},
    "ml engineer": {"risk": 25, "demand": "growing"},
    "data scientist": {"risk": 40, "demand": "stable"},
    "product manager": {"risk": 35, "demand": "stable"},
    "project manager": {"risk": 42, "demand": "stable"},
    "architect": {"risk": 22, "demand": "growing"},
    "security": {"risk": 25, "demand": "growing"},
    "supply chain": {"risk": 48, "demand": "stable"},
    "healthcare": {"risk": 35, "demand": "growing"},
}


@dataclass
class AICareerImpactResult:
    job_title: str
    ai_risk_score: int
    risk_label: str
    automation_exposure: int
    augmentation_opportunity: int
    future_demand: str
    skill_durability: int
    vulnerable_tasks: list[str]
    resistant_tasks: list[str]
    skills_gaining: list[str]
    skills_declining: list[str]
    action_plan_12mo: list[str]
    outlook_3y: str
    data_sources: list[str]
    skills_to_learn: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {f.name: getattr(self, f.name) for f in self.__dataclass_fields__.values()}


def _match_title(title: str, industry: str = "", seniority: str = "mid") -> tuple[int, str]:
    t = title.lower()
    for key, meta in TITLE_RISK_MAP.items():
        if key in t:
            risk = meta["risk"]
            if seniority in ("lead", "staff", "director", "manager") and "manager" not in key:
                risk = max(15, risk - 15)
            if industry == "finance":
                risk = max(20, risk - 5)
            return risk, meta["demand"]
    if any(k in t for k in ("intern", "trainee")):
        return 60, "stable"
    if any(k in t for k in ("lead", "staff", "principal", "architect", "director")):
        return 22, "growing"
    if any(k in t for k in ("senior", "sr")):
        return 35, "stable"
    return 50, "stable"


def analyze_ai_career_impact(
    job_title: str,
    *,
    experience_years: float = 5,
    industry: str = "",
    seniority: str = "mid",
    is_manager: bool = False,
    tech_stack: str = "",
    job_description: str = "",
) -> AICareerImpactResult:
    title = normalize_role(job_title)
    if is_manager or seniority in ("manager", "director"):
        seniority = "lead"

    risk_score, demand = _match_title(title, industry, seniority)
    jd = (job_description or "").lower()
    if any(w in jd for w in ("repetitive", "data entry", "manual testing", "copy paste")):
        risk_score = min(95, risk_score + 10)
    if any(w in jd for w in ("strategy", "stakeholder", "architecture", "leadership")):
        risk_score = max(15, risk_score - 12)

    if risk_score >= 65:
        tier, label = "high", "High Exposure"
    elif risk_score >= 40:
        tier, label = "moderate", "Moderate Exposure"
    else:
        tier, label = "low", "Low Exposure"

    automation = min(100, risk_score + 5)
    augmentation = max(20, 100 - risk_score)
    durability = max(30, 100 - risk_score // 2)

    vulnerable = {
        "high": ["Routine reporting and documentation", "Template-based analysis", "First-line ticket triage", "Standard test case writing"],
        "moderate": ["Boilerplate implementation", "Basic research summaries", "Standard dashboard builds", "Screening coordination"],
        "low": ["Architecture trade-offs", "Incident ownership under ambiguity", "Stakeholder negotiation", "Org-level technical direction"],
    }[tier]

    resistant = {
        "high": ["Client relationship ownership", "Domain-specific judgment calls", "Cross-team coordination"],
        "moderate": ["System design decisions", "Production debugging", "Requirements ambiguity resolution"],
        "low": ["Multi-year technical strategy", "Hiring and team building", "Budget and roadmap ownership"],
    }[tier]

    gaining = {
        "high": ["AI workflow design", "Domain expertise", "Process automation ownership"],
        "moderate": ["LLM/RAG fundamentals", "System design", "Data engineering"],
        "low": ["Technical strategy", "AI product judgment", "Executive communication"],
    }[tier]

    declining = {
        "high": ["Manual data entry", "Copy-paste reporting", "Script-less manual QA"],
        "moderate": ["Boilerplate-only coding", "Generic content production"],
        "low": ["Pure ticket routing without judgment"],
    }[tier]

    plan = [
        f"Month 1–3: Map which weekly tasks are automatable vs judgment-heavy",
        f"Month 4–6: Ship one AI-assisted workflow that saves measurable hours",
        f"Month 7–12: Build visible outcome tied to {gaining[0].lower()}",
    ]

    outlook = {
        "declining": "Role demand may shrink for execution-heavy work — upskill toward oversight and domain judgment.",
        "stable": "Role evolves with AI augmentation — winners combine domain depth with AI fluency.",
        "growing": "Strong demand expected — focus on leverage and scope, not competing with automation on volume.",
    }[demand]

    return AICareerImpactResult(
        job_title=title,
        ai_risk_score=risk_score,
        risk_label=label,
        automation_exposure=automation,
        augmentation_opportunity=augmentation,
        future_demand=demand,
        skill_durability=durability,
        vulnerable_tasks=vulnerable,
        resistant_tasks=resistant,
        skills_gaining=gaining,
        skills_declining=declining,
        action_plan_12mo=plan,
        outlook_3y=outlook,
        data_sources=["editorial", "ai_pulse", "role_taxonomy"],
        skills_to_learn=gaining,
    )
