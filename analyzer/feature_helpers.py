"""Related action links between CareerReality features."""

from django.urls import reverse


def tool_actions(active: str | None = None) -> list[dict]:
    actions = [
        {"key": "salary", "label": "Salary Reality", "description": "Check your percentile", "url_name": "tools:salary_reality_engine"},
        {"key": "offer", "label": "Offer Analyzer", "description": "Compare two offers", "url_name": "tools:offer_analyzer"},
        {"key": "stay", "label": "Stay vs Switch", "description": "Should you leave?", "url_name": "tools:stay_vs_switch"},
        {"key": "ai", "label": "AI Career Impact", "description": "AI exposure score", "url_name": "tools:ai_career_impact"},
        {"key": "move", "label": "Next Career Move", "description": "Highest-ROI paths", "url_name": "tools:next_career_move"},
        {"key": "ask", "label": "Ask CareerReality", "description": "Get evidence-backed advice", "url_name": "tools:ask_career_reality"},
    ]
    out = []
    for a in actions:
        if a["key"] == active:
            continue
        out.append({
            "label": a["label"],
            "description": a["description"],
            "url": reverse(a["url_name"]),
        })
    return out[:4]


METHODOLOGY_SALARY = {
    "data_sources": "Crowdsourced salary submissions and editorial salary bands from CareerReality research.",
    "assumptions": "Percentiles assume comparable role, YOE band (±1 year), and city. CTC entered in lakhs (LPA).",
    "limitations": "Sample size varies by role. Non-tech roles may use broader benchmarks when data is sparse.",
    "confidence": "High when 10+ submissions; medium when blended; low when editorial-only.",
}

METHODOLOGY_OFFER = {
    "data_sources": "Company Reality Score, salary engine, and your stated offer terms.",
    "assumptions": "Variable pay assumed at 70% expected payout; ESOP amortized over 4 years.",
    "limitations": "Benefits and culture are estimated from your inputs when not in our database.",
    "confidence": "Stronger when both companies exist in our database.",
}

METHODOLOGY_STAY = {
    "data_sources": "Salary engine, Company Reality Score, layoff reports, and Career Reality Index.",
    "assumptions": "Decision support only — not financial or legal advice.",
    "limitations": "Personal satisfaction factors rely on your optional inputs.",
    "confidence": "Higher when company is in database and salary data exists.",
}
