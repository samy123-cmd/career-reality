"""Helpers for company page indexability — shared by views and sitemap logic."""

from django.db.models import Q

from .models import Company


def indexable_companies_queryset():
    """
    Companies with enough community data to earn index,follow on detail pages.
    Matches the has_content gate in company_detail.
    """
    return Company.objects.filter(
        Q(review_count__gte=1) | Q(salary_count__gte=1)
    )


def company_is_indexable(company, *, review_total=0, salary_records=None) -> bool:
    """
    True when a company detail page should be indexable.

    Uses live review/salary queries first, then denormalized counts so sitemap
    and detail meta_robots stay aligned when either signal is present.
    """
    if review_total and review_total > 0:
        return True
    if salary_records:
        return True
    return company.review_count >= 1 or company.salary_count >= 1
