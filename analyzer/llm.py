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
Your job: write ONE short paragraph (3-4 sentences, max 80 words) of honest, specific advice 
for a professional based on their exact situation. 

Rules:
- Use INR and India-specific context (service companies, product cos, bonds, F&F, etc.)
- Be direct. No padding. No "that said" or "however". No generic advice.
- Reference their exact company type, role, notice period in the text.
- If risk is high, be urgent. If low, be calm but specific.
- Do NOT start with "I" or "You".
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
        "service": "a large Indian IT service company (TCS/Infy/HCL tier)",
        "product": "an Indian product company (Swiggy/Zomato/Flipkart tier)",
        "startup": "an early-stage startup",
        "unicorn": "a unicorn or large-scale tech company",
        "small_indian": "a small Indian company",
        "mnc": "an MNC",
    }
    role_map = {
        "junior": "junior professional (0-3 years)",
        "mid": "mid-level professional (4-7 years)",
        "senior": "senior professional (8+ years)",
        "manager": "manager or team lead",
    }
    bond_map = {
        "no_bond": "no bond",
        "bond_penalty": "a bond with financial penalty",
        "bond_unclear": "an unclear bond clause",
        "served_bond": "a bond already served",
    }
    notice_map = {
        "30_days": "30-day notice",
        "60_days": "60-day notice",
        "90_days": "90-day notice",
        "more_90": "more than 90 days notice",
    }

    company = company_map.get(data.get("company_type", ""), data.get("company_type", "unknown company"))
    role = role_map.get(data.get("role_level", ""), "professional")
    bond = bond_map.get(data.get("bond_status", ""), "unclear bond situation")
    notice = notice_map.get(data.get("notice_period", ""), "standard notice")
    situation = data.get("current_situation", "general pressure")
    has_offer = data.get("has_offer", "no")
    risk_level = result.get("level", "medium")
    risk_label = result.get("label", "Medium Risk")

    user_prompt = f"""
Situation:
- Works at: {company}
- Role: {role}  
- Bond: {bond}
- Notice period: {notice}
- Current situation: {situation}
- Has competing offer: {has_offer}
- Calculated risk: {risk_label} ({risk_level})

Write the advisory paragraph now.
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
