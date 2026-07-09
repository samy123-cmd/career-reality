"""Shared salary ticker feed data for API and server-rendered homepage."""

from __future__ import annotations

from analyzer.models import SalarySubmission

COMPANY_TYPE_LABELS = dict(SalarySubmission.COMPANY_TYPES)


def get_salary_ticker_items(*, limit: int = 20) -> list[dict[str, str]]:
    """Return recent salary submissions formatted for the homepage ticker."""
    verified = list(
        SalarySubmission.objects.filter(verification_status="verified")
        .values("role", "company_type", "experience_years", "ctc", "city")
        .order_by("-created_at")[:limit]
    )
    pending_limit = max(0, limit - len(verified))
    pending = list(
        SalarySubmission.objects.exclude(verification_status="verified")
        .values("role", "company_type", "experience_years", "ctc", "city")
        .order_by("-created_at")[:pending_limit]
    )
    rows = verified + pending
    return [
        {
            "role": row["role"],
            "company": COMPANY_TYPE_LABELS.get(row["company_type"], row["company_type"]),
            "exp": f"{row['experience_years']}y",
            "ctc": f"{row['ctc'] / 100000:.1f} LPA",
            "city": row["city"],
        }
        for row in rows
    ]
