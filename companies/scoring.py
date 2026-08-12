"""
Company Reality Score — 360° composite view of compensation, stability,
growth, WLB, culture, promotion, and work mode clarity.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from django.db.models import Avg, Count, Q
from django.utils import timezone

from analyzer.models import LayoffReport, SalarySubmission


@dataclass
class DimensionScore:
    name: str
    score: float  # 0-10
    weight: float
    label: str
    detail: str


@dataclass
class CompanyRealityScore:
    company_id: int
    company_name: str
    overall: float  # 0-10
    dimensions: list[DimensionScore]
    stability_label: str
    sample_salaries: int
    sample_reviews: int
    layoff_reports: int

    def to_dict(self) -> dict:
        return {
            "company_name": self.company_name,
            "overall": round(self.overall, 1),
            "stability_label": self.stability_label,
            "dimensions": [
                {
                    "name": d.name,
                    "score": round(d.score, 1),
                    "weight": d.weight,
                    "label": d.label,
                    "detail": d.detail,
                }
                for d in self.dimensions
            ],
            "sample_salaries": self.sample_salaries,
            "sample_reviews": self.sample_reviews,
            "layoff_reports": self.layoff_reports,
        }


def _clamp(val: float, lo: float = 0, hi: float = 10) -> float:
    return max(lo, min(hi, val))


def _stability_from_layoffs(company) -> tuple[float, str]:
    """Score stability from recent layoff reports."""
    cutoff = timezone.now() - timedelta(days=90)
    reports = LayoffReport.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name),
        created_at__gte=cutoff,
    ).order_by("-created_at")

    if not reports.exists():
        return 7.5, "stable"

    latest = reports.first()
    status_scores = {
        "hiring": (9.0, "hiring"),
        "freeze": (5.5, "freeze"),
        "rumor": (4.0, "at_risk"),
        "layoff": (2.0, "layoff_active"),
    }
    return status_scores.get(latest.status, (5.0, "unknown"))


def _compensation_score(company) -> tuple[float, str]:
    salaries = SalarySubmission.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name)
    ).exclude(verification_status="flagged")
    count = salaries.count()
    if count == 0:
        return 5.0, "No salary data yet"

    median = sorted(s.ctc for s in salaries[:200])
    med = median[len(median) // 2]

    sector_medians = {
        "service": 12,
        "product": 22,
        "startup": 18,
        "unicorn": 28,
        "mnc_captive": 24,
        "bfsi": 20,
        "ecommerce": 20,
    }
    sector_med = sector_medians.get(company.sector, 18)
    ratio = med / sector_med if sector_med else 1.0
    score = _clamp(5 + (ratio - 1) * 5)
    return score, f"Median ₹{med}L vs sector ~₹{sector_med}L (n={count})"


def compute_company_reality_score(company) -> CompanyRealityScore:
    """Compute full 360° Company Reality Score."""
    reviews = company.reviews.filter(is_flagged=False)
    review_count = reviews.count()

    avg = reviews.aggregate(
        culture=Avg("rating_culture"),
        growth=Avg("rating_growth"),
        worklife=Avg("rating_worklife"),
        salary=Avg("rating_salary"),
        overall=Avg("rating_overall"),
        rejoin=Count("id", filter=Q(would_rejoin=True)),
        total=Count("id"),
    )

    stability_score, stability_label = _stability_from_layoffs(company)
    comp_score, comp_detail = _compensation_score(company)

    culture_score = _clamp(float(avg["culture"] or 5) * 2)
    growth_score = _clamp(float(avg["growth"] or 5) * 2)
    wlb_score = _clamp(float(avg["worklife"] or 5) * 2)
    salary_review_score = _clamp(float(avg["salary"] or 5) * 2)

    rejoin_pct = 0
    if avg["total"]:
        rejoin_pct = (avg["rejoin"] or 0) / avg["total"] * 100
    sentiment_score = _clamp(rejoin_pct / 10)

    # Promotion proxy: tenure distribution — longer tenure = better promotion path
    tenures = list(reviews.exclude(tenure_months__isnull=True).values_list("tenure_months", flat=True))
    if tenures:
        avg_tenure_y = sum(tenures) / len(tenures) / 12
        promotion_score = _clamp(4 + avg_tenure_y * 0.8)
        promo_detail = f"Avg tenure {avg_tenure_y:.1f}y among reviewers"
    else:
        promotion_score = 5.0
        promo_detail = "Insufficient tenure data"

    work_mode_score = 7.0 if company.work_mode else 5.0
    work_mode_detail = company.get_work_mode_display() if company.work_mode else "Work mode not specified"

    layoff_count = LayoffReport.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name)
    ).count()

    dimensions = [
        DimensionScore("compensation", comp_score, 0.20, "Compensation", comp_detail),
        DimensionScore("stability", stability_score, 0.20, "Stability", f"Status: {stability_label}"),
        DimensionScore("growth", growth_score, 0.15, "Growth", "Career growth from reviews"),
        DimensionScore("work_life", wlb_score, 0.15, "Work-Life Balance", "WLB rating from reviews"),
        DimensionScore("culture", sentiment_score, 0.15, "Culture & Sentiment", f"{rejoin_pct:.0f}% would rejoin"),
        DimensionScore("promotion", promotion_score, 0.10, "Promotion Path", promo_detail),
        DimensionScore("work_mode", work_mode_score, 0.05, "Work Mode", work_mode_detail),
    ]

    overall = sum(d.score * d.weight for d in dimensions)

    salary_count = SalarySubmission.objects.filter(
        Q(company=company) | Q(company_name__iexact=company.name)
    ).count()

    return CompanyRealityScore(
        company_id=company.id,
        company_name=company.name,
        overall=overall,
        dimensions=dimensions,
        stability_label=stability_label,
        sample_salaries=salary_count,
        sample_reviews=review_count,
        layoff_reports=layoff_count,
    )


def reality_score_from_dict(data: dict) -> CompanyRealityScore:
    """Reconstruct CompanyRealityScore from denormalized JSON."""
    dimensions = [
        DimensionScore(
            name=d["name"],
            score=float(d["score"]),
            weight=float(d["weight"]),
            label=d["label"],
            detail=d["detail"],
        )
        for d in data.get("dimensions", [])
    ]
    return CompanyRealityScore(
        company_id=data.get("company_id", 0),
        company_name=data.get("company_name", ""),
        overall=float(data.get("overall", 0)),
        dimensions=dimensions,
        stability_label=data.get("stability_label", "unknown"),
        sample_salaries=data.get("sample_salaries", 0),
        sample_reviews=data.get("sample_reviews", 0),
        layoff_reports=data.get("layoff_reports", 0),
    )


def get_company_reality_score(company) -> CompanyRealityScore:
    """Read denormalized score when available; compute on miss."""
    if company.reality_score_json:
        try:
            return reality_score_from_dict(company.reality_score_json)
        except (TypeError, KeyError, ValueError):
            pass
    return compute_company_reality_score(company)
