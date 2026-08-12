"""Views for CareerReality career tools (Top 10 features)."""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone

from accounts.decorators import pro_required
from accounts.models import (
    AdvisorConversation,
    AdvisorMessage,
    CareerAlert,
    CareerProfile,
    CareerSnapshot,
)
from analyzer import forms
from analyzer.services.salary_engine import get_salary_reality
from analyzer.services.offer_analyzer import OfferInput, compare_offers
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
)


def _seo_ctx(seo):
    return {
        "og_title": seo.title,
        "og_description": seo.description,
        "page_h1": seo.h1,
        "page_keywords": seo.keywords,
    }


@cache_page(60 * 30)
def salary_reality_engine(request):
    """Interactive Salary Reality Engine tool."""
    result = None
    form = forms.SalaryRealityEngineForm()
    if request.method == "POST":
        form = forms.SalaryRealityEngineForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            result = get_salary_reality(
                role=d["role"],
                yoe=d["experience_years"],
                city=d["city"],
                company_type=d.get("company_type") or "",
                current_ctc=d.get("current_ctc"),
            )
    ctx = {
        "form": form,
        "result": result,
        **_seo_ctx(SALARY_REALITY_ENGINE),
    }
    return render(request, "analyzer/tools/salary_reality_engine.html", ctx)


@require_GET
def salary_reality_api(request):
    """JSON API for salary reality lookups."""
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
    response["X-Robots-Tag"] = "noindex"
    return response


def offer_analyzer(request):
    """Compare two job offers."""
    result = None
    form = forms.OfferAnalyzerForm()
    if request.method == "POST":
        form = forms.OfferAnalyzerForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            yoe = d["experience_years"]

            def _company(name):
                return Company.objects.filter(name__icontains=name).first()

            offer_a = OfferInput(
                label="Offer A",
                company_name=d["offer_a_company"],
                company=_company(d["offer_a_company"]),
                role=d["role"],
                ctc=d["offer_a_ctc"],
                fixed_pct=d["offer_a_fixed_pct"],
                variable_pct=d["offer_a_variable_pct"],
                city=d.get("offer_a_city") or "",
                commute_minutes=d.get("offer_a_commute"),
                wlb_rating=d.get("offer_a_wlb"),
            )
            offer_b = OfferInput(
                label="Offer B",
                company_name=d["offer_b_company"],
                company=_company(d["offer_b_company"]),
                role=d["role"],
                ctc=d["offer_b_ctc"],
                fixed_pct=d["offer_b_fixed_pct"],
                variable_pct=d["offer_b_variable_pct"],
                city=d.get("offer_b_city") or "",
                commute_minutes=d.get("offer_b_commute"),
                wlb_rating=d.get("offer_b_wlb"),
            )
            result = compare_offers(offer_a, offer_b, yoe)

    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)
    return render(request, "analyzer/tools/offer_analyzer.html", {
        "form": form,
        "result": result,
        "is_pro": is_pro,
        **_seo_ctx(OFFER_ANALYZER),
    })


def stay_vs_switch(request):
    """Stay vs Switch career decision tool."""
    result = None
    form = forms.StayVsSwitchForm()
    if request.method == "POST":
        form = forms.StayVsSwitchForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            company = None
            if d.get("company_name"):
                company = Company.objects.filter(name__icontains=d["company_name"]).first()
            wizard_data = {
                k: d[k] for k in (
                    "company_type", "role_level", "tenure_band", "bond_status",
                    "notice_period", "ctc_vs_market", "current_situation",
                    "performance_status", "has_offer",
                ) if d.get(k)
            }
            result = analyze_stay_vs_switch(
                role=d["role"],
                yoe=d["experience_years"],
                city=d["city"],
                company_type=d["company_type"],
                current_ctc=d["current_ctc"],
                company=company,
                has_offer=d.get("has_offer") == "yes",
                offer_ctc=d.get("offer_ctc"),
                wizard_data=wizard_data,
            )
    return render(request, "analyzer/tools/stay_vs_switch.html", {
        "form": form,
        "result": result,
        **_seo_ctx(STAY_VS_SWITCH),
    })


def ai_career_impact(request):
    """AI career impact assessment."""
    result = None
    form = forms.AICareerImpactForm()
    if request.method == "POST":
        form = forms.AICareerImpactForm(request.POST)
        if form.is_valid():
            result = analyze_ai_career_impact(form.cleaned_data["job_title"])
            from analyzer.llm import generate_ai_impact_narrative
            llm_narrative = generate_ai_impact_narrative(result)
    else:
        llm_narrative = None

    return render(request, "analyzer/tools/ai_career_impact.html", {
        "form": form,
        "result": result,
        "llm_narrative": llm_narrative if form.is_bound and form.is_valid() else None,
        **_seo_ctx(AI_CAREER_IMPACT),
    })


def next_career_move(request):
    """Next career move recommendations."""
    result = None
    form = forms.NextCareerMoveForm()
    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)
    if request.method == "POST":
        form = forms.NextCareerMoveForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            skills = [s.strip() for s in d.get("skills", "").split(",") if s.strip()]
            result = recommend_next_moves(
                role=d["role"],
                yoe=d["experience_years"],
                city=d["city"],
                company_type=d["company_type"],
                current_ctc=d["current_ctc"],
                skills=skills,
            )
            if not is_pro and result.paths:
                result.paths = result.paths[:1]
    return render(request, "analyzer/tools/next_career_move.html", {
        "form": form,
        "result": result,
        "is_pro": is_pro,
        **_seo_ctx(NEXT_CAREER_MOVE),
    })


def ask_career_reality(request):
    """Conversational career advisor."""
    answer = None
    form = forms.AskCareerRealityForm()
    is_pro = request.user.is_authenticated and getattr(request.user.profile, "is_pro", False)

    # Rate limit free users
    month_key = timezone.now().strftime("%Y-%m")
    session_key = f"ask_count_{month_key}"
    ask_count = request.session.get(session_key, 0)
    limit_reached = not is_pro and ask_count >= 3

    if request.method == "POST" and not limit_reached:
        form = forms.AskCareerRealityForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]
            answer = answer_career_question(question)
            request.session[session_key] = ask_count + 1

            conv = AdvisorConversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or "",
            )
            AdvisorMessage.objects.create(conversation=conv, role="user", content=question)
            AdvisorMessage.objects.create(
                conversation=conv,
                role="assistant",
                content=answer.answer,
                citations=[c.__dict__ for c in answer.citations],
            )

    return render(request, "analyzer/tools/ask_career_reality.html", {
        "form": form,
        "answer": answer,
        "is_pro": is_pro,
        "limit_reached": limit_reached,
        "asks_remaining": max(0, 3 - ask_count) if not is_pro else None,
        **_seo_ctx(ASK_CAREER_REALITY),
    })


@require_POST
def ask_career_reality_api(request):
    """JSON API for Ask CareerReality."""
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid_json"}, status=400)
    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "question required"}, status=400)
    answer = answer_career_question(question)
    return JsonResponse(answer.to_dict())
