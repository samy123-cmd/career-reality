import logging

from django.db.models import Q, Value, CharField
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

from content.models import Article
from companies.models import Company
from ainews.models import AINewsItem
from analyzer.models import SalarySubmission

logger = logging.getLogger(__name__)

MAX_QUERY_LEN = 100


def search_view(request):
    """Full-text search across articles, companies, AI news, and salary data."""
    q = request.GET.get("q", "").strip()[:MAX_QUERY_LEN]
    tab = request.GET.get("tab", "all")

    results = {"articles": [], "companies": [], "news": [], "salaries": []}
    counts = {"articles": 0, "companies": 0, "news": 0, "salaries": 0}

    if q and len(q) >= 2:
        # Articles
        articles = Article.objects.filter(
            Q(title__icontains=q) |
            Q(target_persona__icontains=q) |
            Q(actual_reality__icontains=q) |
            Q(verdict__icontains=q),
            status="published",
        ).select_related("author", "category").order_by("-published_at")
        counts["articles"] = articles.count()
        results["articles"] = articles[:20]

        # Companies
        companies = Company.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(headquarters__icontains=q)
        ).order_by("-salary_count")
        counts["companies"] = companies.count()
        results["companies"] = companies[:20]

        # AI News
        news = AINewsItem.objects.filter(
            Q(title__icontains=q) |
            Q(summary__icontains=q) |
            Q(career_angle__icontains=q),
            status="published",
        ).order_by("-published_at")
        counts["news"] = news.count()
        results["news"] = news[:20]

        # Salary data
        salaries = SalarySubmission.objects.filter(
            Q(role__icontains=q) |
            Q(city__icontains=q) |
            Q(tech_stack__icontains=q)
        ).order_by("-created_at")
        counts["salaries"] = salaries.count()
        results["salaries"] = salaries[:20]

    total = sum(counts.values())

    return render(request, "search/results.html", {
        "query": q,
        "tab": tab,
        "results": results,
        "counts": counts,
        "total": total,
        "og_title": f"Search: {q} — Career Reality India" if q else "Search — Career Reality India",
        "og_description": f"Search results for '{q}' across articles, companies, salaries, and AI news.",
        "meta_robots": "noindex, follow",
    })


def search_suggest_api(request):
    """JSON autocomplete endpoint for search bar."""
    q = request.GET.get("q", "").strip()[:MAX_QUERY_LEN]
    if len(q) < 2:
        return JsonResponse({"suggestions": []})

    suggestions = []

    # Articles
    for a in Article.objects.filter(title__icontains=q, status="published").values("title", "slug")[:3]:
        suggestions.append({"type": "article", "text": a["title"], "url": f"/article/{a['slug']}/"})

    # Companies
    for c in Company.objects.filter(name__icontains=q).values("name", "slug")[:3]:
        suggestions.append({"type": "company", "text": c["name"], "url": f"/companies/{c['slug']}/"})

    # AI News
    for n in AINewsItem.objects.filter(title__icontains=q, status="published").values("title", "slug")[:2]:
        suggestions.append({"type": "news", "text": n["title"], "url": f"/ai/{n['slug']}/"})

    return JsonResponse({"suggestions": suggestions})
