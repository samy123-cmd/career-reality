"""
analyzer/llm.py — OpenAI-powered personalized narrative for the risk result page.

The function is safe to call unconditionally: if OPENAI_API_KEY is not set
or the call fails, it returns None and the template falls back to the
static rule-based result text.

Using gpt-4o-mini for cost efficiency (~$0.0002 per call).
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are a no-nonsense Indian IT career advisor writing for Career Reality India.
Your job: write ONE short paragraph (3-4 sentences, max 90 words) of honest, specific advice 
for a professional based on their exact situation.

Rules:
- Use INR and India-specific context (IT service bonds, product cos, F&F settlements, relieving letters, BGV, PF).
- Be direct. No padding. No "that said" or "however". No generic advice.
- Reference their exact company type, role, notice period, and situation in the text.
- If risk is high, be urgent. If low, be calm but specific.
- Do NOT start with "I" or "You".
- Focus on what they should do in the next 7 days, not platitudes.
"""


def generate_risk_narrative(data: dict, result: dict) -> str | None:
    """
    Generate a personalized 3-4 sentence narrative for the result page.

    Args:
        data: Session data dict (company_type, role_level, bond_status, etc.)
        result: Calculated risk result dict (level, label, etc.)

    Returns:
        Personalized narrative string, or None on failure/no key.
    """
    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except ImportError:
        logger.warning("openai package not installed")
        return None

    company_map = {
        "service":      "a large Indian IT service company (TCS/Infy/Wipro/HCL tier)",
        "product":      "an Indian product company (Swiggy/Zomato/CRED tier)",
        "mnc_captive":  "an MNC captive centre / GDC",
        "startup":      "an early-stage Indian startup (Series A or earlier)",
        "small_indian": "a small Indian firm with under 100 employees",
    }
    role_map = {
        "ic":        "individual contributor (no direct reports)",
        "senior_ic": "senior IC / tech lead / team lead",
        "manager":   "manager or senior manager",
    }
    bond_map = {
        "no_bond":      "no bond",
        "bond_penalty": "a bond with a specific financial penalty",
        "bond_unclear": "an unclear / ambiguous bond clause",
    }
    notice_map = {
        "30_days": "30-day notice period",
        "60_days": "60-day notice period",
        "90_days": "90-day notice period",
        "more_90": "notice period over 90 days",
    }
    tenure_map = {
        "less_6m": "less than 6 months at this company",
        "6m_18m":  "6 to 18 months at this company",
        "18m_3y":  "18 months to 3 years at this company",
        "3y_plus": "more than 3 years at this company",
    }
    perf_map = {
        "star":        "top performer on a critical project",
        "good":        "good standing with no performance issues",
        "warning":     "received a performance warning recently",
        "pip_managed": "currently on PIP or being managed out",
    }
    ctc_map = {
        "below":    "underpaid relative to market",
        "at_market":"paid roughly at market rate",
        "above":    "above market rate",
    }

    company     = company_map.get(data.get("company_type", ""), data.get("company_type", "unknown company"))
    role        = role_map.get(data.get("role_level", ""), "professional")
    bond        = bond_map.get(data.get("bond_status", ""), "unclear bond situation")
    notice      = notice_map.get(data.get("notice_period", ""), "standard notice")
    tenure      = tenure_map.get(data.get("tenure_band", ""), "unspecified tenure")
    performance = perf_map.get(data.get("performance_status", ""), "unspecified performance")
    ctc         = ctc_map.get(data.get("ctc_vs_market", ""), "market-rate CTC")
    situation   = data.get("current_situation", "general evaluation")
    has_offer   = data.get("has_offer", "no")
    risk_label  = result.get("label", "Medium Risk")
    score       = result.get("score", 0)

    user_prompt = f"""
Profile:
- Company type: {company}
- Role: {role}
- Tenure: {tenure}
- Bond situation: {bond}
- Notice period: {notice}
- CTC vs market: {ctc}
- Performance standing: {performance}
- Current situation: {situation}
- Has competing offer: {has_offer}
- Calculated risk score: {score}/100 → {risk_label}

Write the advisory paragraph now. Be specific to this exact combination.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=150,
            temperature=0.6,
            timeout=8,
        )
        narrative = response.choices[0].message.content.strip()
        return narrative if narrative else None
    except Exception:
        logger.exception("LLM narrative generation failed")
        return None
