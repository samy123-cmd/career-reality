from django.shortcuts import redirect, render
from django.utils import timezone
from analyzer.models import SalarySubmission
from accounts.decorators import pro_required


@pro_required
def pro_dashboard(request):
    """Pro subscriber dashboard — salary intelligence + tools."""
    profile = request.user.profile

    # Salary intelligence: top 20 recent verified submissions
    recent_salaries = SalarySubmission.objects.order_by("-created_at")[:20]

    # Percentile buckets for the logged-in user's last submission (if any)
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

    return render(
        request,
        "accounts/pro_dashboard.html",
        {
            "profile": profile,
            "recent_salaries": recent_salaries,
            "role_benchmarks": role_benchmarks,
            "subscription_expires_at": profile.subscription_expires_at,
            "days_until_expiry": profile.days_until_expiry,
            "og_title": "Pro Dashboard — Career Reality India",
            "og_description": "Your salary intelligence dashboard.",
        },
    )
