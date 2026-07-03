from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q

from analyzer.models import SalarySubmission, LayoffReport
from companies.models import Company
from accounts.decorators import pro_required
from accounts.models import CompanyWatchlist


@login_required
def onboarding(request):
    """Post-signup onboarding page for new free users."""
    if request.user.profile.is_pro:
        return redirect("pro_dashboard")
    return render(request, "accounts/onboarding.html")


@pro_required
def pro_dashboard(request):
    """Pro subscriber dashboard — salary intelligence + tools."""
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
