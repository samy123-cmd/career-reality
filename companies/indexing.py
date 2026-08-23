"""Helpers for company page indexability — shared by views and sitemap logic."""

from django.db.models import Q, QuerySet

from .models import Company

# Directory / search: any community signal is enough to show the card.
# Indexation: AdSense thin-content safe bar — short template pages with 1 review
# or 1 salary were flooding GSC/sitemap as near-duplicate ~400-word stubs.
MIN_INDEXABLE_REVIEWS = 3
MIN_INDEXABLE_SALARIES = 5
MIN_DESCRIPTION_WORDS = 120


def _description_word_count(company) -> int:
    return len((company.description or "").split())


def listable_companies_queryset() -> QuerySet[Company]:
    """Companies shown in the directory / search (have any community data)."""
    return Company.objects.filter(
        Q(review_count__gte=1) | Q(salary_count__gte=1)
    )


def indexable_companies_queryset() -> QuerySet[Company]:
    """
    Companies with enough community data to *candidate* for index,follow.
    Callers that need the full AdSense gate should also check
    ``company_is_indexable`` (description length).
    """
    return Company.objects.filter(
        review_count__gte=MIN_INDEXABLE_REVIEWS,
        salary_count__gte=MIN_INDEXABLE_SALARIES,
    ).exclude(description="")


def company_is_indexable(company, *, review_total=0, salary_records=None) -> bool:
    """
    True when a company detail page should be indexable.

    Uses live review/salary queries first, then denormalized counts so sitemap
    and detail meta_robots stay aligned.
    """
    if _description_word_count(company) < MIN_DESCRIPTION_WORDS:
        return False
    reviews = max(review_total or 0, company.review_count or 0)
    live_salaries = len(salary_records) if salary_records is not None else 0
    salaries = max(live_salaries, company.salary_count or 0)
    return reviews >= MIN_INDEXABLE_REVIEWS and salaries >= MIN_INDEXABLE_SALARIES


def indexable_companies_for_sitemap():
    """Companies that pass the full index gate (for sitemap generation)."""
    return [
        c
        for c in indexable_companies_queryset().order_by("-salary_count", "name")
        if company_is_indexable(c)
    ]
