"""
AI Career Impact — job title → AI Risk Score, vulnerable tasks, future demand, skills to learn.
"""

from __future__ import annotations

from dataclasses import dataclass


TITLE_RISK_MAP: dict[str, dict] = {
    "data entry": {"risk": 85, "demand": "declining"},
    "manual tester": {"risk": 78, "demand": "declining"},
    "qa manual": {"risk": 75, "demand": "declining"},
    "content writer": {"risk": 72, "demand": "declining"},
    "customer support": {"risk": 68, "demand": "stable"},
    "business analyst": {"risk": 55, "demand": "stable"},
    "frontend": {"risk": 45, "demand": "stable"},
    "backend": {"risk": 35, "demand": "growing"},
    "full stack": {"risk": 38, "demand": "growing"},
    "devops": {"risk": 30, "demand": "growing"},
    "sre": {"risk": 28, "demand": "growing"},
    "data engineer": {"risk": 32, "demand": "growing"},
    "ml engineer": {"risk": 25, "demand": "growing"},
    "data scientist": {"risk": 40, "demand": "stable"},
    "product manager": {"risk": 35, "demand": "stable"},
    "staff engineer": {"risk": 20, "demand": "growing"},
    "architect": {"risk": 22, "demand": "growing"},
    "security": {"risk": 25, "demand": "growing"},
    "cybersecurity": {"risk": 22, "demand": "growing"},
}

VULNERABLE_BY_TIER = {
    "high": [
        "Repetitive documentation and status reporting",
        "Basic code generation from well-defined specs",
        "Routine data transformation and report building",
        "First-line troubleshooting with known playbooks",
    ],
    "moderate": [
        "Boilerplate implementation without architectural decisions",
        "Standard test case authoring",
        "Competitive analysis summaries",
        "Interview screening coordination",
    ],
    "low": [
        "Cross-team system design and trade-off decisions",
        "Production incident ownership under ambiguity",
        "Stakeholder negotiation and roadmap prioritization",
        "Mentoring and org-level technical direction",
    ],
}

SKILLS_BY_TIER = {
    "high": [
        "AI-assisted workflow design (not just prompting)",
        "Domain expertise that AI cannot replicate",
        "Cross-functional communication and stakeholder management",
    ],
    "moderate": [
        "LLM evaluation, RAG pipelines, and cost-aware inference",
        "System design and distributed systems fundamentals",
        "Data engineering and observability tooling",
    ],
    "low": [
        "Staff-level architecture and technical strategy",
        "AI product sense — knowing when NOT to use AI",
        "People leadership and org design",
    ],
}


@dataclass
class AICareerImpactResult:
    job_title: str
    ai_risk_score: int
    risk_label: str
    vulnerable_tasks: list[str]
    future_demand: str
    skills_to_learn: list[str]
    data_sources: list[str]

    def to_dict(self) -> dict:
        return {
            "job_title": self.job_title,
            "ai_risk_score": self.ai_risk_score,
            "risk_label": self.risk_label,
            "vulnerable_tasks": self.vulnerable_tasks,
            "future_demand": self.future_demand,
            "skills_to_learn": self.skills_to_learn,
            "data_sources": self.data_sources,
        }


def _match_title(title: str) -> tuple[int, str]:
    t = title.lower()
    for key, meta in TITLE_RISK_MAP.items():
        if key in t:
            return meta["risk"], meta["demand"]
    # Default by keywords
    if any(k in t for k in ("intern", "trainee", "associate")):
        return 60, "stable"
    if any(k in t for k in ("lead", "staff", "principal", "architect", "director")):
        return 22, "growing"
    if any(k in t for k in ("senior", "sr")):
        return 35, "stable"
    return 50, "stable"


def analyze_ai_career_impact(job_title: str) -> AICareerImpactResult:
    risk_score, demand = _match_title(job_title)

    if risk_score >= 65:
        tier = "high"
        label = "High Exposure"
    elif risk_score >= 40:
        tier = "moderate"
        label = "Moderate Exposure"
    else:
        tier = "low"
        label = "Low Exposure"

    return AICareerImpactResult(
        job_title=job_title,
        ai_risk_score=risk_score,
        risk_label=label,
        vulnerable_tasks=VULNERABLE_BY_TIER[tier][:4],
        future_demand=demand,
        skills_to_learn=SKILLS_BY_TIER[tier],
        data_sources=["editorial", "ai_pulse"],
    )
