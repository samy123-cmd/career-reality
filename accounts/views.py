from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone

from analyzer.models import SalarySubmission, LayoffReport
from analyzer import forms as analyzer_forms
from analyzer.services.salary_engine import get_salary_reality
from analyzer.services.stay_vs_switch import analyze_stay_vs_switch
from analyzer.services.ai_career_impact import analyze_ai_career_impact
from companies.models import Company
from companies.scoring import compute_company_reality_score
from analyzer.engine_guard import safe_engine
from accounts.decorators import pro_required
from accounts.models import (
    CareerAlert,
    CareerProfile,
    CareerSnapshot,
    CompanyWatchlist,
)
from accounts.services.career_health import compute_career_health
from accounts.services.risk_radar import compute_risk_radar


@login_required
def onboarding(request):
    """Post-signup onboarding — capture career profile for new free users."""
    profile = request.user.profile
    # Pro users are onboarded through the dashboard, never this page.
    if profile.is_pro:
        return redirect("pro_dashboard")
    # Anyone who already has a profile has nothing left to fill in.
    if CareerProfile.objects.filter(user=request.user).exists():
        return redirect("pro_dashboard")

    if request.method == "POST":
        form = analyzer_forms.CareerProfileForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            company = None
            if d.get("company_name"):
                company = Company.objects.filter(name__icontains=d["company_name"]).first()
            skills = [s.strip() for s in d.get("skills", "").split(",") if s.strip()]
            CareerProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    "role": d["role"],
                    "title": d.get("title") or d["role"],
                    "experience_years": d["experience_years"],
                    "city": d["city"],
                    "company_type": d["company_type"],
                    "current_ctc": d["current_ctc"],
                    "company": company,
                    "company_name": d.get("company_name", ""),
                    "skills": skills,
                },
            )
            return redirect("pro_dashboard")
    else:
        form = analyzer_forms.CareerProfileForm()

    return render(request, "accounts/onboarding.html", {"form": form})


@login_required
def my_career_reality(request):
    """Personalized dashboard — underpaid? progressing? switch? company risk?"""
    user_profile = request.user.profile
    career = CareerProfile.objects.filter(user=request.user).first()
    if career is None:
        return redirect("career_profile_edit")

    is_pro = user_profile.is_pro
    salary_insight = None
    stay_switch = None
    company_score = None
    ai_impact = None
    alerts = []

    if career.role and career.current_ctc:
        salary_insight = safe_engine(
            "salary_reality", get_salary_reality,
            career.role,
            float(career.experience_years or 5),
            career.city or "Bengaluru",
            career.company_type or "",
            current_ctc=career.current_ctc,
        )

    if is_pro:
        stay_switch = safe_engine(
            "stay_vs_switch", analyze_stay_vs_switch,
            role=career.role,
            yoe=float(career.experience_years or 5),
            city=career.city or "Bengaluru",
            company_type=career.company_type or "service",
            current_ctc=career.current_ctc or 15,
            company=career.company,
        )
        if career.title or career.role:
            ai_impact = safe_engine("ai_career_impact", analyze_ai_career_impact, career.title or career.role)
        alerts = list(CareerAlert.objects.filter(user=request.user, is_read=False)[:10])

    if career.company:
        company_score = safe_engine("company_reality_score", compute_company_reality_score, career.company)

    snapshots = list(CareerSnapshot.objects.filter(user=request.user).order_by("-recorded_at")[:5])
    latest_snapshot = snapshots[0] if snapshots else None

    career_health = safe_engine(
        "career_health", compute_career_health,
        salary_insight=salary_insight,
        company_score=company_score,
        stay_switch=stay_switch if is_pro else None,
        ai_impact=ai_impact if is_pro else None,
        latest_snapshot=latest_snapshot,
    )

    return render(
        request,
        "accounts/my_career_reality.html",
        {
            "profile": user_profile,
            "career": career,
            "is_pro": is_pro,
            "salary_insight": salary_insight,
            "stay_switch": stay_switch,
            "company_score": company_score,
            "ai_impact": ai_impact,
            "alerts": alerts,
            "snapshots": snapshots,
            "latest_snapshot": latest_snapshot,
            "career_health": career_health,
            "og_title": "My Career Reality — Career Reality India",
            "og_description": "Your personalized career dashboard.",
        },
    )


@pro_required
def pro_dashboard(request):
    """Redirect Pro users to My Career Reality when profile exists."""
    if CareerProfile.objects.filter(user=request.user).exists():
        return redirect("my_career_reality")
    return _legacy_pro_dashboard(request)


def _legacy_pro_dashboard(request):
    """Legacy Pro dashboard — salary intelligence + tools."""
    profile = request.user.profile

    recent_salaries = SalarySubmission.objects.order_by("-is_verified", "-created_at")[:20]

    role_benchmarks = []
    top_roles = (
        SalarySubmission.objects.values("role")
        .order_by("role")
        .distinct()[:10]
    )
    for r in top_roles:
        role_subs = SalarySubmission.objects.filter(role=r["role"])
        if role_subs.exists():
            ctcs = sorted([s.ctc for s in role_subs])
            median = ctcs[len(ctcs) // 2]
            role_benchmarks.append(
                {
                    "role": r["role"],
                    "median_ctc": median,
                    "sample_size": len(ctcs),
                    "p25": ctcs[max(0, len(ctcs) // 4)],
                    "p75": ctcs[min(len(ctcs) - 1, (3 * len(ctcs)) // 4)],
                }
            )

    watchlist_entries = []
    for entry in CompanyWatchlist.objects.filter(user=request.user).select_related("company"):
        company = entry.company
        latest_report = LayoffReport.objects.filter(
            Q(company=company) | Q(company_name__iexact=company.name)
        ).order_by("-created_at").first()
        watchlist_entries.append({
            "entry": entry,
            "company": company,
            "latest_report": latest_report,
        })

    return render(
        request,
        "accounts/pro_dashboard.html",
        {
            "profile": profile,
            "recent_salaries": recent_salaries,
            "role_benchmarks": role_benchmarks,
            "watchlist_entries": watchlist_entries,
            "subscription_expires_at": profile.subscription_expires_at,
            "days_until_expiry": profile.days_until_expiry,
            "og_title": "Pro Dashboard — Career Reality India",
            "og_description": "Your salary intelligence dashboard.",
        },
    )


@login_required
@pro_required
def career_progression(request):
    """Career progression tracker."""
    snapshots = CareerSnapshot.objects.filter(user=request.user).order_by("-recorded_at")
    form = analyzer_forms.CareerSnapshotForm()

    if request.method == "POST":
        form = analyzer_forms.CareerSnapshotForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            career = getattr(request.user, "career_profile", None)
            role = career.role if career else "Software Engineer"
            yoe = float(career.experience_years) if career else 5
            city = career.city if career else "Bengaluru"
            salary = safe_engine("salary_reality", get_salary_reality, role, yoe, city, current_ctc=d["ctc"])
            peer = "on_track"
            if salary.percentile and salary.percentile >= 70:
                peer = "ahead"
            elif salary.percentile and salary.percentile < 40:
                peer = "behind"
            skills = [s.strip() for s in d.get("skills", "").split(",") if s.strip()]
            CareerSnapshot.objects.create(
                user=request.user,
                recorded_at=d["recorded_at"],
                title=d["title"],
                ctc=d["ctc"],
                company_name=d.get("company_name", ""),
                skills=skills,
                salary_percentile=salary.percentile,
                peer_comparison=peer,
            )
            return redirect("career_progression")

    return render(request, "accounts/career_progression.html", {
        "snapshots": snapshots,
        "form": form,
        "trajectory": _build_trajectory(snapshots),
        "narrative": _progression_narrative(snapshots, getattr(request.user, "career_profile", None)),
        "og_title": "Career Progression Tracker",
    })


def _build_trajectory(snapshots):
    """Build SVG trajectory data from snapshots."""
    snaps = list(snapshots.order_by("recorded_at"))
    if len(snaps) < 2:
        return None
    ctcs = [s.ctc for s in snaps]
    mn, mx = min(ctcs), max(ctcs)
    span = max(mx - mn, 1)
    points = []
    markers = []
    for i, s in enumerate(snaps):
        x = 40 + (i / max(len(snaps) - 1, 1)) * 320
        y = 160 - ((s.ctc - mn) / span) * 120
        points.append(f"{x},{y}")
        markers.append({"x": x, "y": y, "label": f"₹{s.ctc}L"})
    return {
        "points": " ".join(points),
        "markers": markers,
        "snapshots": [{"date": s.recorded_at.isoformat(), "ctc": s.ctc, "title": s.title} for s in snaps],
    }


def _progression_narrative(snapshots, career=None):
    snaps = list(snapshots.order_by("recorded_at"))
    if len(snaps) < 2:
        return "Add two or more snapshots to see your salary trajectory story."
    first, last = snaps[0], snaps[-1]
    growth = last.ctc - first.ctc
    years = max(0.5, (last.recorded_at - first.recorded_at).days / 365)
    cagr = int(growth / years) if years else growth
    peer = last.peer_comparison or "on_track"
    return (
        f"Your CTC grew from ₹{first.ctc}L to ₹{last.ctc}L "
        f"(~₹{cagr}L/year). Latest peer comparison: {peer.replace('_', ' ')}."
    )


@login_required
@pro_required
def career_risk_radar(request):
    """Personalized career risk alerts."""
    alert_qs = CareerAlert.objects.filter(user=request.user)
    # Counted before slicing; a sliced queryset cannot be filtered again.
    unread_count = alert_qs.filter(is_read=False).count()
    alerts = list(alert_qs.order_by("-created_at")[:50])
    watchlist = CompanyWatchlist.objects.filter(user=request.user).select_related("company")

    career = getattr(request.user, "career_profile", None)
    salary_insight = company_score = ai_impact = stay_switch = None
    if career and career.role and career.current_ctc:
        salary_insight = safe_engine(
            "salary_reality", get_salary_reality,
            career.role, float(career.experience_years or 5),
            career.city or "Bengaluru", career.company_type or "", current_ctc=career.current_ctc,
        )
        if career.company:
            company_score = safe_engine("company_reality_score", compute_company_reality_score, career.company)
        if is_pro := request.user.profile.is_pro:
            ai_impact = safe_engine("ai_career_impact", analyze_ai_career_impact, career.title or career.role)
            stay_switch = safe_engine(
                "stay_vs_switch", analyze_stay_vs_switch,
                role=career.role, yoe=float(career.experience_years or 5),
                city=career.city or "Bengaluru", company_type=career.company_type or "service",
                current_ctc=career.current_ctc or 15, company=career.company,
            )

    radar = safe_engine(
        "risk_radar", compute_risk_radar,
        career=career,
        salary_insight=salary_insight,
        company_score=company_score,
        ai_impact=ai_impact,
        stay_switch=stay_switch,
        alerts=alerts[:10],
    )

    return render(request, "accounts/career_risk_radar.html", {
        "alerts": alerts,
        "watchlist": watchlist,
        "unread_count": unread_count,
        "radar": radar,
        "og_title": "Career Risk Radar",
    })


@login_required
def career_profile_edit(request):
    """Create or edit the career profile that powers every personalized view.

    This must work for users who have no profile yet; it is the only route
    Pro members have to build one, since onboarding sends them to the dashboard.
    """
    career = CareerProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = analyzer_forms.CareerProfileForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            company = Company.objects.filter(name__icontains=d["company_name"]).first() if d.get("company_name") else None
            skills = [s.strip() for s in d.get("skills", "").split(",") if s.strip()]
            CareerProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    "role": d["role"],
                    "title": d.get("title") or d["role"],
                    "experience_years": d["experience_years"],
                    "city": d["city"],
                    "company_type": d["company_type"],
                    "current_ctc": d["current_ctc"],
                    "company": company,
                    "company_name": d.get("company_name", ""),
                    "skills": skills,
                },
            )
            messages.success(
                request,
                "Career profile saved. Your tools and dashboard now use it." if career
                else "Career profile created. Your dashboard is ready.",
            )
            return redirect("my_career_reality")
    elif career:
        form = analyzer_forms.CareerProfileForm(initial={
            "role": career.role,
            "title": career.title,
            "experience_years": career.experience_years,
            "city": career.city,
            "company_type": career.company_type,
            "current_ctc": career.current_ctc,
            "company_name": career.company_name,
            "skills": ", ".join(career.skills or []),
        })
    else:
        form = analyzer_forms.CareerProfileForm()

    return render(request, "accounts/career_profile_edit.html", {"form": form, "career": career})


@login_required
@pro_required
@require_POST
def mark_alert_read(request, alert_id):
    alert = get_object_or_404(CareerAlert, pk=alert_id, user=request.user)
    alert.is_read = True
    alert.save(update_fields=["is_read"])
    return redirect("career_risk_radar")


@pro_required
@require_POST
def toggle_watchlist(request, slug):
    """Add or remove a company from the Pro user's watchlist."""
    company = get_object_or_404(Company, slug=slug)
    existing = CompanyWatchlist.objects.filter(user=request.user, company=company).first()
    if existing:
        existing.delete()
    else:
        CompanyWatchlist.objects.create(user=request.user, company=company)
    return redirect("company_detail", slug=slug)
