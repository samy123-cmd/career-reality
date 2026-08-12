"""Shared career context for profile prefill across new features."""

from __future__ import annotations

from analyzer.constants.career_taxonomy import normalize_city, normalize_role

SESSION_KEY = "career_context_v1"

DEFAULTS = {
    "role": "Software Engineer",
    "experience_years": 5.0,
    "city": "Bengaluru",
    "company_type": "service",
    "current_ctc": None,
    "company_name": "",
    "industry": "",
    "skills": "",
}


def get_career_context(request) -> dict:
    """Merged career context: CareerProfile → session → defaults."""
    ctx = dict(DEFAULTS)

    if request.user.is_authenticated:
        try:
            cp = request.user.career_profile
            ctx.update({
                "role": cp.role or ctx["role"],
                "experience_years": float(cp.experience_years) if cp.experience_years is not None else ctx["experience_years"],
                "city": cp.city or ctx["city"],
                "company_type": cp.company_type or ctx["company_type"],
                "current_ctc": cp.current_ctc,
                "company_name": cp.company_name or "",
                "skills": ", ".join(cp.skills) if cp.skills else "",
            })
            if cp.company_id:
                ctx["company_id"] = cp.company_id
        except Exception:
            pass

    session_ctx = request.session.get(SESSION_KEY, {})
    if isinstance(session_ctx, dict):
        for k, v in session_ctx.items():
            if v is not None and v != "":
                ctx[k] = v

    ctx["role"] = normalize_role(str(ctx.get("role", DEFAULTS["role"])))
    ctx["city"] = normalize_city(str(ctx.get("city", DEFAULTS["city"])))
    return ctx


def save_career_context(request, data: dict) -> None:
    """Persist partial inputs to session for anonymous + authenticated users."""
    existing = request.session.get(SESSION_KEY, {})
    if not isinstance(existing, dict):
        existing = {}
    for key in ("role", "experience_years", "city", "company_type", "current_ctc", "company_name", "industry", "skills"):
        if key in data and data[key] not in (None, ""):
            existing[key] = data[key]
    request.session[SESSION_KEY] = existing
    request.session.modified = True


def context_banner(ctx: dict) -> str:
    parts = [ctx.get("role", "")]
    if ctx.get("experience_years") is not None:
        parts.append(f"{ctx['experience_years']} YOE")
    if ctx.get("city"):
        parts.append(ctx["city"])
    if ctx.get("current_ctc"):
        parts.append(f"₹{ctx['current_ctc']}L")
    return " · ".join(p for p in parts if p)


def prefill_form(form_class, request, **extra):
    """Instantiate a form with career context initial data."""
    ctx = get_career_context(request)
    initial = {
        "role": ctx["role"],
        "experience_years": ctx["experience_years"],
        "city": ctx["city"],
        "company_type": ctx.get("company_type") or "service",
        "current_ctc": ctx.get("current_ctc"),
        "company_name": ctx.get("company_name", ""),
        "skills": ctx.get("skills", ""),
        "industry": ctx.get("industry", ""),
        "job_title": ctx["role"],
    }
    initial.update(extra)
    return form_class(initial=initial)


def feature_view_context(request, seo_ctx: dict) -> dict:
    ctx = get_career_context(request)
    banner = context_banner(ctx)
    return {
        **seo_ctx,
        "career_context": ctx,
        "career_context_banner": banner if any([ctx.get("role"), ctx.get("current_ctc")]) else None,
    }
