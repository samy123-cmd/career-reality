import logging

from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

from analyzer.models import SalarySubmission, LayoffReport
from .models import Company, CompanyReview
from .forms import CompanyReviewForm

logger = logging.getLogger(__name__)


@cache_page(60 * 10)
def company_directory(request):
    """Browsable directory of all companies with intelligence data."""
    sector = request.GET.get("sector", "")
    sort = request.GET.get("sort", "-salary_count")
    q = request.GET.get("q", "").strip()

    allowed_sorts = {
        "-salary_count": "-salary_count",
        "-review_count": "-review_count",
        "-overall_score": "-overall_score",
        "name": "name",
    }
    order = allowed_sorts.get(sort, "-salary_count")

    qs = Company.objects.all()
    if sector:
        qs = qs.filter(sector=sector)
    if q:
        qs = qs.filter(name__icontains=q)
    qs = qs.order_by(order)

    paginator = Paginator(qs, 30)
    page = paginator.get_page(request.GET.get("page", 1))

    return render(request, "companies/directory.html", {
        "page_obj": page,
        "sector_choices": Company.SECTOR_CHOICES,
        "current_sector": sector,
        "current_sort": sort,
        "search_query": q,
        "total_companies": Company.objects.count(),
        "total_reviews": CompanyReview.objects.count(),
        "total_salaries": SalarySubmission.objects.count(),
        "og_title": "Company Intelligence — Career Reality India",
        "og_description": "Honest salary data, layoff alerts, and anonymous reviews for Indian tech companies. No login required.",
    })


def company_detail(request, slug):
    """Deep-dive company profile with aggregated intelligence."""
    company = get_object_or_404(Company, slug=slug)

    # Salary data linked by company name
    salaries = SalarySubmission.objects.filter(
        Q(company_type__iexact=company.sector) |
        Q(role__icontains=company.name[:20])  # Fuzzy match for now
    ).order_by("-created_at")[:30]

    # If we can match salaries by company name stored as keyword in tech_stack/role
    direct_salaries = SalarySubmission.objects.filter(
        tech_stack__icontains=company.name
    ).order_by("-created_at")[:20]

    all_salaries = list(salaries | direct_salaries)[:30]

    # Salary stats
    if all_salaries:
        ctcs = sorted([s.ctc for s in all_salaries])
        salary_stats = {
            "count": len(ctcs),
            "median": ctcs[len(ctcs) // 2],
            "p25": ctcs[max(0, len(ctcs) // 4)],
            "p75": ctcs[min(len(ctcs) - 1, (3 * len(ctcs)) // 4)],
            "min": ctcs[0],
            "max": ctcs[-1],
        }
    else:
        salary_stats = None

    # Reviews
    reviews = company.reviews.filter(is_flagged=False).order_by("-created_at")[:50]
    review_stats = reviews.aggregate(
        avg_overall=Avg("rating_overall"),
        avg_salary=Avg("rating_salary"),
        avg_culture=Avg("rating_culture"),
        avg_growth=Avg("rating_growth"),
        avg_worklife=Avg("rating_worklife"),
        avg_management=Avg("rating_management"),
        total=Count("id"),
        would_rejoin_count=Count("id", filter=Q(would_rejoin=True)),
    )
    if review_stats["total"] and review_stats["total"] > 0:
        review_stats["rejoin_pct"] = round(
            review_stats["would_rejoin_count"] / review_stats["total"] * 100
        )
    else:
        review_stats["rejoin_pct"] = None

    # Layoff reports for this company
    layoff_reports = LayoffReport.objects.filter(
        company_name__iexact=company.name
    ).order_by("-created_at")[:20]

    # Review form
    form = CompanyReviewForm()

    return render(request, "companies/detail.html", {
        "company": company,
        "salaries": all_salaries[:15],
        "salary_stats": salary_stats,
        "reviews": reviews[:20],
        "review_stats": review_stats,
        "layoff_reports": layoff_reports,
        "form": form,
        "og_title": f"{company.name} — Salary, Reviews & Reality Check",
        "og_description": f"Honest salary data, anonymous reviews, and layoff alerts for {company.name}. No login required.",
    })


@require_POST
def submit_review(request, slug):
    """Submit an anonymous company review."""
    company = get_object_or_404(Company, slug=slug)

    # Rate limit: 3 reviews per IP per hour
    from django.core.cache import cache
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0].strip()
    rate_key = f"review_{ip}"
    count = cache.get(rate_key, 0)
    if count >= 3:
        messages.error(request, "Too many submissions. Please try again later.")
        return redirect("company_detail", slug=slug)
    cache.set(rate_key, count + 1, timeout=3600)

    form = CompanyReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.company = company
        review.save()

        # Update denormalized counts
        company.review_count = company.reviews.filter(is_flagged=False).count()
        avg = company.reviews.filter(is_flagged=False).aggregate(avg=Avg("rating_overall"))
        company.overall_score = avg["avg"]
        company.save(update_fields=["review_count", "overall_score", "updated_at"])

        messages.success(request, "Review submitted. Thanks for keeping it real.")
        return redirect("company_detail", slug=slug)

    messages.error(request, "Please fix the errors below.")
    return redirect("company_detail", slug=slug)


def company_search_api(request):
    """JSON API for company autocomplete / search."""
    q = request.GET.get("q", "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    companies = Company.objects.filter(name__icontains=q).values(
        "name", "slug", "sector", "salary_count", "overall_score"
    )[:10]

    return JsonResponse({
        "results": [
            {
                "name": c["name"],
                "slug": c["slug"],
                "sector": c["sector"],
                "salary_count": c["salary_count"],
                "score": float(c["overall_score"]) if c["overall_score"] else None,
            }
            for c in companies
        ]
    })
