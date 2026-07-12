"""Recalculate denormalized company intelligence stats from live submissions."""

from django.db.models import Avg, Q

from analyzer.models import LayoffReport, SalarySubmission


def sync_company_stats(company, *, save=True):
    """Refresh salary_count, avg_ctc, review_count, overall_score, layoff_report_count."""
    salaries = SalarySubmission.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name)
    )
    salary_count = salaries.count()
    avg_ctc = salaries.aggregate(v=Avg("ctc"))["v"]

    reviews = company.reviews.filter(is_flagged=False)
    review_count = reviews.count()
    overall = reviews.aggregate(v=Avg("rating_overall"))["v"]

    layoff_count = LayoffReport.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name)
    ).count()

    company.salary_count = salary_count
    company.avg_ctc = int(avg_ctc) if avg_ctc else company.avg_ctc
    company.review_count = review_count
    company.overall_score = round(overall, 1) if overall is not None else company.overall_score
    company.layoff_report_count = layoff_count

    if save:
        company.save(
            update_fields=[
                "salary_count",
                "avg_ctc",
                "review_count",
                "overall_score",
                "layoff_report_count",
                "updated_at",
            ]
        )
    return company


def sync_all_company_stats():
    from companies.models import Company

    updated = 0
    for company in Company.objects.all():
        sync_company_stats(company)
        updated += 1
    return updated
