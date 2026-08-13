"""Views for CareerReality career tools (Top 10 features)."""

import json

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.cache import patch_cache_control
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone

from accounts.career_context import feature_view_context, prefill_form, save_career_context
from accounts.models import AdvisorConversation, AdvisorMessage, JobOffer
from analyzer import forms
from analyzer.feature_helpers import (
    METHODOLOGY_OFFER,
    METHODOLOGY_SALARY,
    METHODOLOGY_STAY,
    tool_actions,
)
from analyzer.services.salary_engine import get_salary_reality
from analyzer.services.offer_analyzer import OfferInput, compare_offers, DEFAULT_WEIGHTS
from analyzer.services.stay_vs_switch import analyze_stay_vs_switch
from analyzer.services.ai_career_impact import analyze_ai_career_impact
from analyzer.services.next_career_move import recommend_next_moves
from analyzer.services.career_advisor import answer_career_question
from companies.models import Company
from core.seo_pages import (
    SALARY_REALITY_ENGINE,
    OFFER_ANALYZER,
    STAY_VS_SWITCH,
    AI_CAREER_IMPACT,
    NEXT_CAREER_MOVE,
    ASK_CAREER_REALITY,
    TOOL_FAQS,
)

ASK_MONTHLY_LIMIT = 3


def _seo_ctx(seo, faq_key: str):
    return {
        "og_title": seo.title,
        "og_description": seo.description,
        "twitter_title": seo.title,
        "twitter_description": seo.description,
        "page_h1": seo.h1,
        "page_keywords": seo.keywords,
        "tool_faq": TOOL_FAQS.get(faq_key, ()),
        "tool_schema_name": seo.h1,
    }


def _ask_limit_state(request):
    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)
    month_key = timezone.now().strftime("%Y-%m")
    session_key = f"ask_count_{month_key}"
    ask_count = request.session.get(session_key, 0)
    return is_pro, session_key, ask_count


def _check_ask_rate_limit(request, *, increment=False):
    is_pro, session_key, ask_count = _ask_limit_state(request)
    if is_pro:
        return True, is_pro, session_key, ask_count
    if ask_count >= ASK_MONTHLY_LIMIT:
        return False, is_pro, session_key, ask_count
    ip = (
        request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        .split(",")[0]
        .strip()
    )
    ip_key = f"ask_api:{timezone.now().strftime('%Y-%m')}:{ip}"
    ip_count = cache.get(ip_key, 0)
    if ip_count >= ASK_MONTHLY_LIMIT:
        return False, is_pro, session_key, ask_count
    if increment:
        request.session[session_key] = ask_count + 1
        cache.set(ip_key, ip_count + 1, timeout=60 * 60 * 24 * 32)
    return True, is_pro, session_key, ask_count


def _company_lookup(name: str):
    return Company.objects.filter(name__icontains=name).first() if name else None


def salary_reality_engine(request):
    result = None
    form = prefill_form(forms.SalaryRealityEngineForm, request)
    if request.method == "POST":
        form = forms.SalaryRealityEngineForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            save_career_context(request, d)
            result = get_salary_reality(
                role=d["role"],
                yoe=d["experience_years"],
                city=d["city"],
                company_type=d.get("company_type") or "",
                current_ctc=d.get("current_ctc"),
            )
    ctx = feature_view_context(request, _seo_ctx(SALARY_REALITY_ENGINE, "salary_reality_engine"))
    return render(request, "analyzer/tools/salary_reality_engine.html", {
        "form": form,
        "result": result,
        "chart_data": result.chart_payload() if result else None,
        "methodology": METHODOLOGY_SALARY,
        "related_actions": tool_actions("salary"),
        "preview_items": ["Salary percentile", "Market range P25–P90", "Under/overpaid estimate", "Realistic next salary", "Confidence indicator"],
        **ctx,
    })


@require_GET
def salary_reality_api(request):
    role = request.GET.get("role", "").strip()
    if not role:
        return JsonResponse({"error": "role required"}, status=400)
    try:
        yoe = float(request.GET.get("yoe", 5))
        city = request.GET.get("city", "Bengaluru")
        company_type = request.GET.get("company_type", "")
        current_ctc = request.GET.get("current_ctc")
        current_ctc = int(current_ctc) if current_ctc else None
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid parameters"}, status=400)
    result = get_salary_reality(role, yoe, city, company_type, current_ctc=current_ctc)
    response = JsonResponse(result.to_dict())
    patch_cache_control(response, public=True, max_age=300, stale_while_revalidate=120)
    response["X-Robots-Tag"] = "noindex"
    return response


def offer_analyzer(request):
    result = None
    form = prefill_form(forms.OfferAnalyzerForm, request)
    if request.method == "POST":
        form = forms.OfferAnalyzerForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            save_career_context(request, {"role": d["role"], "experience_years": d["experience_years"], "current_ctc": d.get("current_ctc")})
            yoe = d["experience_years"]
            role = d["role"]
            # Sliders are optional, so an omitted value must fall back rather
            # than reach the engine as None.
            weights = {
                "salary": d.get("priority_salary") or DEFAULT_WEIGHTS["salary"],
                "stability": d.get("priority_stability") or DEFAULT_WEIGHTS["stability"],
                "growth": d.get("priority_growth") or DEFAULT_WEIGHTS["growth"],
                "wlb": d.get("priority_wlb") or DEFAULT_WEIGHTS["wlb"],
            }
            offer_a = OfferInput(
                label="Offer A",
                company_name=d["offer_a_company"],
                company=_company_lookup(d["offer_a_company"]),
                role=d.get("offer_a_role") or role,
                ctc=d["offer_a_ctc"],
                fixed_pct=d["offer_a_fixed_pct"],
                variable_pct=d["offer_a_variable_pct"],
                esop_value=d.get("offer_a_esop") or 0,
                joining_bonus=d.get("offer_a_joining_bonus") or 0,
                city=d.get("offer_a_city") or "",
                commute_minutes=d.get("offer_a_commute"),
                wlb_rating=d.get("offer_a_wlb"),
                work_mode=d.get("offer_a_work_mode") or "hybrid",
                growth_potential=d.get("offer_a_growth") or 3,
            )
            offer_b = OfferInput(
                label="Offer B",
                company_name=d["offer_b_company"],
                company=_company_lookup(d["offer_b_company"]),
                role=d.get("offer_b_role") or role,
                ctc=d["offer_b_ctc"],
                fixed_pct=d["offer_b_fixed_pct"],
                variable_pct=d["offer_b_variable_pct"],
                esop_value=d.get("offer_b_esop") or 0,
                joining_bonus=d.get("offer_b_joining_bonus") or 0,
                city=d.get("offer_b_city") or "",
                commute_minutes=d.get("offer_b_commute"),
                wlb_rating=d.get("offer_b_wlb"),
                work_mode=d.get("offer_b_work_mode") or "hybrid",
                growth_potential=d.get("offer_b_growth") or 3,
            )
            result = compare_offers(offer_a, offer_b, yoe, weights=weights)
            if request.user.is_authenticated and request.POST.get("save_offer"):
                for label, inp in [("A", offer_a), ("B", offer_b)]:
                    JobOffer.objects.create(
                        user=request.user,
                        label=f"Offer {label}",
                        company_name=inp.company_name,
                        company=inp.company,
                        role=inp.role,
                        ctc=inp.ctc,
                        fixed_pct=inp.fixed_pct,
                        variable_pct=inp.variable_pct,
                        esop_value=inp.esop_value,
                        city=inp.city,
                        commute_minutes=inp.commute_minutes or 0,
                        wlb_rating=inp.wlb_rating or 3,
                        work_mode=inp.work_mode,
                    )

    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)
    ctx = feature_view_context(request, _seo_ctx(OFFER_ANALYZER, "offer_analyzer"))
    return render(request, "analyzer/tools/offer_analyzer.html", {
        "form": form,
        "result": result,
        "is_pro": is_pro,
        "methodology": METHODOLOGY_OFFER,
        "related_actions": tool_actions("offer"),
        "default_weights": DEFAULT_WEIGHTS,
        "preview_items": ["Weighted verdict", "Dimension breakdown", "Trade-offs", "2-year outlook", "5-year outlook"],
        **ctx,
    })


def stay_vs_switch(request):
    result = None
    form = prefill_form(forms.StayVsSwitchForm, request)
    if request.method == "POST":
        form = forms.StayVsSwitchForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            save_career_context(request, d)
            company = _company_lookup(d.get("company_name", ""))
            wizard_data = {k: d[k] for k in (
                "company_type", "role_level", "tenure_band", "bond_status",
                "notice_period", "ctc_vs_market", "current_situation",
                "performance_status", "has_offer",
            ) if d.get(k)}
            result = analyze_stay_vs_switch(
                role=d["role"], yoe=d["experience_years"], city=d["city"],
                company_type=d["company_type"], current_ctc=d["current_ctc"],
                company=company, has_offer=d.get("has_offer") == "yes",
                offer_ctc=d.get("offer_ctc"), wizard_data=wizard_data,
            )
    ctx = feature_view_context(request, _seo_ctx(STAY_VS_SWITCH, "stay_vs_switch"))
    return render(request, "analyzer/tools/stay_vs_switch.html", {
        "form": form, "result": result,
        "methodology": METHODOLOGY_STAY,
        "related_actions": tool_actions("stay"),
        "preview_items": ["Stay / Switch / Wait verdict", "Category breakdown", "Recommended timeline", "Improvement checklist"],
        **ctx,
    })


def ai_career_impact(request):
    result = None
    form = prefill_form(forms.AICareerImpactForm, request)
    if request.method == "POST":
        form = forms.AICareerImpactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            save_career_context(request, {"role": d["job_title"], "experience_years": d["experience_years"]})
            result = analyze_ai_career_impact(
                d["job_title"],
                experience_years=d["experience_years"],
                industry=d.get("industry") or "",
                seniority=d.get("seniority") or "mid",
                is_manager=d.get("is_manager") or False,
                tech_stack=d.get("tech_stack") or "",
                job_description=d.get("job_description") or "",
            )
    ctx = feature_view_context(request, _seo_ctx(AI_CAREER_IMPACT, "ai_career_impact"))
    return render(request, "analyzer/tools/ai_career_impact.html", {
        "form": form, "result": result,
        "related_actions": tool_actions("ai"),
        "preview_items": ["AI impact level", "Task exposure analysis", "Skills gaining vs declining", "12-month action plan"],
        **ctx,
    })


def next_career_move(request):
    result = None
    form = prefill_form(forms.NextCareerMoveForm, request)
    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)
    if request.method == "POST":
        form = forms.NextCareerMoveForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            save_career_context(request, d)
            skills = [s.strip() for s in d.get("skills", "").split(",") if s.strip()]
            result = recommend_next_moves(
                role=d["role"], yoe=d["experience_years"], city=d["city"],
                company_type=d["company_type"], current_ctc=d["current_ctc"], skills=skills,
            )
            if not is_pro and result.paths:
                result.paths = result.paths[:1]
    ctx = feature_view_context(request, _seo_ctx(NEXT_CAREER_MOVE, "next_career_move"))
    return render(request, "analyzer/tools/next_career_move.html", {
        "form": form, "result": result, "is_pro": is_pro,
        "related_actions": tool_actions("move"),
        "preview_items": ["3–5 career paths", "Salary potential", "Difficulty & timeline", "Best-fit recommendation"],
        **ctx,
    })


def ask_career_reality(request):
    answer = None
    form = forms.AskCareerRealityForm()
    is_pro, session_key, ask_count = _ask_limit_state(request)
    limit_reached = not is_pro and ask_count >= ASK_MONTHLY_LIMIT
    history = []

    if request.user.is_authenticated:
        convs = AdvisorConversation.objects.filter(user=request.user).order_by("-created_at")[:3]
        for c in convs:
            msgs = list(c.messages.order_by("created_at"))
            if msgs:
                history.append({"question": msgs[0].content, "answer": msgs[-1].content if len(msgs) > 1 else ""})

    if request.method == "POST" and not limit_reached:
        allowed, is_pro, session_key, ask_count = _check_ask_rate_limit(request, increment=False)
        if allowed:
            form = forms.AskCareerRealityForm(request.POST)
            if form.is_valid():
                question = form.cleaned_data["question"]
                answer = answer_career_question(question)
                _check_ask_rate_limit(request, increment=True)
                conv = AdvisorConversation.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_key=request.session.session_key or "",
                )
                AdvisorMessage.objects.create(conversation=conv, role="user", content=question)
                AdvisorMessage.objects.create(
                    conversation=conv, role="assistant", content=answer.answer,
                    citations=[{"type": c.type, "label": c.label, "url": c.url} for c in answer.citations],
                )

    ctx = feature_view_context(request, _seo_ctx(ASK_CAREER_REALITY, "ask_career_reality"))
    return render(request, "analyzer/tools/ask_career_reality.html", {
        "form": form, "answer": answer, "is_pro": is_pro,
        "limit_reached": limit_reached,
        "asks_remaining": max(0, ASK_MONTHLY_LIMIT - ask_count) if not is_pro else None,
        "history": history,
        "related_actions": tool_actions("ask"),
        "preview_items": ["Evidence-backed answer", "CareerReality data citations", "Assumptions stated", "Recommended next steps"],
        **ctx,
    })


@require_POST
def ask_career_reality_api(request):
    allowed, _, _, _ = _check_ask_rate_limit(request, increment=False)
    if not allowed:
        return JsonResponse({"error": "rate_limit_exceeded"}, status=429)
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid_json"}, status=400)
    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "question required"}, status=400)
    answer = answer_career_question(question)
    _check_ask_rate_limit(request, increment=True)
    response = JsonResponse(answer.to_dict())
    response["X-Robots-Tag"] = "noindex"
    return response
