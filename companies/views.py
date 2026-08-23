import logging

from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify

from analyzer.models import SalarySubmission, LayoffReport
from analyzer.salary_access import (
    get_balance,
    get_free_previews_remaining,
    get_unlocked_ids,
    is_pro_user,
)
from accounts.models import CompanyWatchlist
from .models import Company, CompanyReview, Discussion, DiscussionReply
from .forms import CompanyReviewForm, DiscussionForm, DiscussionReplyForm
from .indexing import company_is_indexable, listable_companies_queryset

logger = logging.getLogger(__name__)


@cache_page(60 * 30)
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

    qs = listable_companies_queryset()
    if sector:
        qs = qs.filter(sector=sector)
    if q:
        qs = qs.filter(name__icontains=q)
    qs = qs.order_by(order)

    paginator = Paginator(qs, 30)
    page = paginator.get_page(request.GET.get("page", 1))

    indexed_count = listable_companies_queryset().count()

    return render(request, "companies/directory.html", {
        "page_obj": page,
        "sector_choices": Company.SECTOR_CHOICES,
        "current_sector": sector,
        "current_sort": sort,
        "search_query": q,
        "total_companies": indexed_count,
        "total_reviews": CompanyReview.objects.count(),
        "total_salaries": SalarySubmission.objects.count(),
        "pending_companies_count": Company.objects.count() - indexed_count,
        "og_title": "Company Intelligence — Career Reality India",
        "og_description": "Honest salary data, layoff alerts, and anonymous reviews for Indian tech companies. No login required.",
    })


@cache_page(60 * 15, key_prefix="company_detail_v3")
def company_detail(request, slug):
    """Deep-dive company profile with aggregated intelligence."""
    company = get_object_or_404(Company, slug=slug)

    # Salary data — match strictly by company name to avoid showing wrong-company data
    salaries = SalarySubmission.objects.filter(
        company_name__iexact=company.name
    ).order_by("-created_at")[:30]

    # Secondary loose match: company name appears in free-text tech_stack/role fields
    direct_salaries = SalarySubmission.objects.filter(
        tech_stack__icontains=company.name
    ).exclude(company_name__iexact=company.name).order_by("-created_at")[:20]

    all_salaries = list(salaries | direct_salaries)[:30]
    all_salaries.sort(
        key=lambda s: (s.verification_status != "verified", -s.created_at.timestamp())
    )

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

    # Recent discussions for this company
    company_discussions = Discussion.objects.filter(
        company=company, is_flagged=False
    ).order_by("-created_at")[:5]

    # Thin company stubs (~400 words) must stay noindex for AdSense.
    has_content = company_is_indexable(
        company,
        review_total=review_stats["total"] or 0,
        salary_records=all_salaries,
    )
    meta_robots = "index, follow" if has_content else "noindex, follow"

    is_watching = False
    if request.user.is_authenticated:
        try:
            if request.user.profile.is_pro:
                is_watching = CompanyWatchlist.objects.filter(
                    user=request.user, company=company
                ).exists()
        except Exception:
            pass

    unlocked_ids = get_unlocked_ids(request)
    user_is_pro = is_pro_user(request)

    response = render(request, "companies/detail.html", {
        "company": company,
        "salaries": all_salaries[:15],
        "salary_stats": salary_stats,
        "reviews": reviews[:20],
        "review_stats": review_stats,
        "layoff_reports": layoff_reports,
        "form": form,
        "company_discussions": company_discussions,
        "meta_robots": meta_robots,
        "is_watching": is_watching,
        "user_is_pro": user_is_pro,
        "salary_balance": get_balance(request),
        "free_previews_remaining": get_free_previews_remaining(request),
        "unlocked_salary_ids": unlocked_ids,
        "og_title": f"{company.name} — Salary, Reviews & Reality Check",
        "og_description": f"Honest salary data, anonymous reviews, and layoff alerts for {company.name}. No login required.",
    })
    if meta_robots.startswith("noindex"):
        response["X-Robots-Tag"] = "noindex, follow"
    return response


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
    """JSON API for company autocomplete / search — indexable companies only."""
    q = request.GET.get("q", "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    companies = listable_companies_queryset().filter(name__icontains=q).values(
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


# ─── Discussion Views ────────────────────────────────────────────────────────

_DISCUSSION_RATE_LIMIT = 5  # max posts per IP per hour


def _get_ip(request):
    return (
        request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        .split(",")[0]
        .strip()
    )


def discussion_list(request):
    """Browse all discussions — filterable by topic and company."""
    from django.core.cache import cache

    topic = request.GET.get("topic", "")
    company_slug = request.GET.get("company", "")
    sort = request.GET.get("sort", "recent")

    qs = Discussion.objects.filter(is_flagged=False).select_related("company")

    if topic:
        qs = qs.filter(topic=topic)
    if company_slug:
        qs = qs.filter(company__slug=company_slug)

    if sort == "top":
        qs = qs.order_by("-upvotes", "-created_at")
    else:
        qs = qs.order_by("-created_at")

    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get("page", 1))

    return render(request, "companies/discussion_list.html", {
        "page_obj": page,
        "topic_choices": Discussion.TOPIC_CHOICES,
        "current_topic": topic,
        "current_company": company_slug,
        "current_sort": sort,
        "total_discussions": Discussion.objects.filter(is_flagged=False).count(),
        "og_title": "Community Discussions — Career Reality India",
        "og_description": "Anonymous career discussions from Indian tech professionals. No corporate spin.",
        # UGC threads are thin for crawlers — keep for users, not search index.
        "meta_robots": "noindex, follow",
    })


def discussion_detail(request, pk):
    """Single discussion thread with replies."""
    discussion = get_object_or_404(Discussion, pk=pk, is_flagged=False)
    replies = discussion.replies.filter(is_flagged=False).order_by("created_at")
    reply_form = DiscussionReplyForm()

    return render(request, "companies/discussion_detail.html", {
        "discussion": discussion,
        "replies": replies,
        "reply_count": replies.count(),
        "reply_form": reply_form,
        "og_title": f"{discussion.title} — Career Reality Discussions",
        "og_description": discussion.body[:160],
        "meta_robots": "noindex, follow",
    })


def discussion_create(request, slug=None):
    """Create a new discussion thread — optionally attached to a company."""
    company = None
    if slug:
        company = get_object_or_404(Company, slug=slug)

    if request.method == "POST":
        from django.core.cache import cache

        ip = _get_ip(request)
        rate_key = f"disc_post_{ip}"
        count = cache.get(rate_key, 0)
        if count >= _DISCUSSION_RATE_LIMIT:
            messages.error(request, "You're posting too fast. Please wait an hour before posting again.")
            return redirect("discussion_list")

        form = DiscussionForm(request.POST)
        if form.is_valid():
            disc = form.save(commit=False)
            disc.company = company
            if request.user.is_authenticated:
                disc.user = request.user
            disc.save()

            cache.set(rate_key, count + 1, timeout=3600)
            messages.success(request, "Discussion posted. Every honest voice counts.")
            return redirect("discussion_detail", pk=disc.pk)
    else:
        form = DiscussionForm()

    return render(request, "companies/discussion_create.html", {
        "form": form,
        "company": company,
        "og_title": "Start a Discussion — Career Reality India",
        "og_description": "Ask anonymously. Get honest answers from real professionals.",
    })


@require_POST
def discussion_reply(request, pk):
    """Submit a reply to a discussion thread."""
    from django.core.cache import cache

    discussion = get_object_or_404(Discussion, pk=pk, is_flagged=False)

    ip = _get_ip(request)
    rate_key = f"disc_reply_{ip}"
    count = cache.get(rate_key, 0)
    if count >= _DISCUSSION_RATE_LIMIT:
        messages.error(request, "Too many replies. Please wait an hour.")
        return redirect("discussion_detail", pk=pk)

    form = DiscussionReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.discussion = discussion
        if request.user.is_authenticated:
            reply.user = request.user
        reply.save()
        cache.set(rate_key, count + 1, timeout=3600)
        messages.success(request, "Reply posted.")

    return redirect("discussion_detail", pk=pk)


@require_POST
def discussion_upvote(request, pk):
    """Upvote a discussion thread — session-gated to prevent spam."""
    discussion = get_object_or_404(Discussion, pk=pk, is_flagged=False)
    voted_key = f"upvoted_disc_{pk}"

    if request.session.get(voted_key):
        return JsonResponse({"ok": False, "error": "already_voted", "upvotes": discussion.upvotes})

    Discussion.objects.filter(pk=pk).update(upvotes=discussion.upvotes + 1)
    request.session[voted_key] = True
    return JsonResponse({"ok": True, "upvotes": discussion.upvotes + 1})



def write_review(request):
    """Standalone review page - works for any company, listed or not."""
    from django.core.cache import cache

    # Pre-fill company if coming from a company detail page
    prefill_slug = request.GET.get("company", "")
    prefill_company = None
    if prefill_slug:
        prefill_company = Company.objects.filter(slug=prefill_slug).first()

    form = CompanyReviewForm()

    if request.method == "POST":
        company_name = request.POST.get("company_name", "").strip()
        sector = request.POST.get("company_sector", "other")

        if not company_name:
            messages.error(request, "Please enter your company name.")
            return render(request, "companies/write_review.html", {
                "form": form,
                "sector_choices": Company.SECTOR_CHOICES,
                "og_title": "Write a Company Review � Career Reality India",
            })

        # Rate limit: 3 reviews per IP per hour
        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0].strip()
        rate_key = f"review_{ip}"
        count = cache.get(rate_key, 0)
        if count >= 3:
            messages.error(request, "Too many submissions. Please try again later.")
            return render(request, "companies/write_review.html", {
                "form": form,
                "sector_choices": Company.SECTOR_CHOICES,
                "og_title": "Write a Company Review � Career Reality India",
            })
        cache.set(rate_key, count + 1, timeout=3600)

        # Get or create the company
        base_slug = slugify(company_name)
        candidate_slug = base_slug
        counter = 1
        while Company.objects.filter(slug=candidate_slug).exclude(name__iexact=company_name).exists():
            candidate_slug = f"{base_slug}-{counter}"
            counter += 1

        company, created = Company.objects.get_or_create(
            name__iexact=company_name,
            defaults={
                "name": company_name,
                "slug": candidate_slug,
                "sector": sector if sector in dict(Company.SECTOR_CHOICES) else "other",
            }
        )

        form = CompanyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.company = company
            review.save()

            company.review_count = company.reviews.filter(is_flagged=False).count()
            avg = company.reviews.filter(is_flagged=False).aggregate(avg=Avg("rating_overall"))
            company.overall_score = avg["avg"]
            company.save(update_fields=["review_count", "overall_score", "updated_at"])

            messages.success(request, "Review submitted. Thanks for keeping it real.")
            return redirect("company_detail", slug=company.slug)

        messages.error(request, "Please fix the errors below.")

    return render(request, "companies/write_review.html", {
        "form": form,
        "prefill_company": prefill_company,
        "sector_choices": Company.SECTOR_CHOICES,
        "og_title": "Write a Company Review � Career Reality India",
        "og_description": "Share your anonymous, honest experience. No login required. Any company � listed or not.",
    })
