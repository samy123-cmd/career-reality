"""
Salary Reality Engine — role + YOE + city + company type → percentile, market range, under/overpaid flag.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from django.core.cache import cache

from analyzer.constants.career_taxonomy import normalize_role, role_search_terms
from analyzer.models import SalarySubmission
from content.article_market_data import SALARY_CLUSTERS


CITY_ALIASES = {
    "bengaluru": "bengaluru",
    "bangalore": "bengaluru",
    "blr": "bengaluru",
    "hyderabad": "hyderabad",
    "hyd": "hyderabad",
    "pune": "pune",
    "mumbai": "mumbai",
    "delhi": "delhi",
    "ncr": "delhi",
    "gurgaon": "delhi",
    "gurugram": "delhi",
    "noida": "delhi",
    "chennai": "chennai",
    "remote": "remote",
    "wfh": "remote",
}

MIN_SAMPLE_SIZE = 5


@dataclass
class SalaryRealityResult:
    role: str
    experience_years: float
    city: str
    company_type: str
    sample_size: int
    p10: int
    p25: int
    p50: int
    p75: int
    p90: int
    realistic_next: int
    current_ctc: int | None
    percentile: int | None
    pay_label: str | None  # underpaid | at_market | overpaid
    pay_delta_pct: int | None
    confidence: str  # high | medium | low
    data_source: str  # crowdsourced | editorial | blended
    gap_lpa: float | None = None
    limitation: str | None = None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "experience_years": self.experience_years,
            "city": self.city,
            "company_type": self.company_type,
            "sample_size": self.sample_size,
            "percentiles": {
                "p10": self.p10,
                "p25": self.p25,
                "p50": self.p50,
                "p75": self.p75,
                "p90": self.p90,
            },
            "market_range": {"low": self.p25, "median": self.p50, "high": self.p75},
            "realistic_next": self.realistic_next,
            "current_ctc": self.current_ctc,
            "percentile": self.percentile,
            "pay_label": self.pay_label,
            "pay_delta_pct": self.pay_delta_pct,
            "confidence": self.confidence,
            "data_source": self.data_source,
            "gap_lpa": self.gap_lpa,
            "limitation": self.limitation,
            "chart": self.chart_payload(),
        }

    def chart_payload(self) -> dict:
        user_marker = None
        if self.percentile is not None:
            user_marker = {
                "percentile": self.percentile,
                "position_pct": min(95, max(5, self.percentile)),
            }
        return {
            "p10": self.p10,
            "p25": self.p25,
            "p50": self.p50,
            "p75": self.p75,
            "p90": self.p90,
            "p25_pos": 25,
            "p75_pos": 75,
            "user_marker": user_marker,
        }


def _ctc_to_lpa(raw: int) -> int:
    """Normalize SalarySubmission CTC (INR or LPA) to lakhs."""
    if raw >= 100000:
        return max(1, int(round(raw / 100000)))
    return raw


def _normalize_city(city: str) -> str:
    key = city.strip().lower()
    return CITY_ALIASES.get(key, key)


def _percentile_value(sorted_values: list[int], pct: float) -> int:
    if not sorted_values:
        return 0
    idx = int((len(sorted_values) - 1) * pct)
    return sorted_values[idx]


def _compute_percentile(sorted_values: list[int], value: int) -> int:
    if not sorted_values:
        return 50
    below = sum(1 for v in sorted_values if v < value)
    return min(99, max(1, int(below / len(sorted_values) * 100)))


def _parse_lpa_range(text: str) -> tuple[int, int] | None:
    """Parse '14–23 LPA' or '14-23 LPA' into (14, 23) lakhs."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*[–\-]\s*(\d+(?:\.\d+)?)", text)
    if m:
        return int(float(m.group(1))), int(float(m.group(2)))
    return None


def _editorial_fallback(role: str, yoe: float, city: str) -> tuple[int, int, int, int, int] | None:
    """Return p10,p25,p50,p75,p90 from editorial SALARY_CLUSTERS."""
    norm_city = _normalize_city(city)
    city_col = {
        "bengaluru": "bengaluru",
        "hyderabad": "hyderabad",
        "remote": "remote_india",
    }.get(norm_city, "bengaluru")

    role_lower = normalize_role(role).lower()
    search_terms = role_search_terms(role)
    best_band = None
    best_score = 0

    for cluster_bands in SALARY_CLUSTERS.values():
        for band in cluster_bands:
            score = 0
            band_lower = band.role.lower()
            if any(term in band_lower or band_lower in term for term in search_terms):
                score += 5
            if any(kw in role_lower for kw in band.role.lower().split("/")):
                score += 3
            if band_lower in role_lower or role_lower in band_lower:
                score += 5
            # YOE band match
            yoe_str = band.experience
            nums = re.findall(r"\d+", yoe_str)
            if len(nums) >= 2:
                lo, hi = int(nums[0]), int(nums[-1])
                if lo <= yoe <= hi:
                    score += 4
            if score > best_score:
                best_score = score
                best_band = band

    if not best_band:
        bands = SALARY_CLUSTERS.get("general", ())
        best_band = bands[0] if bands else None

    if not best_band:
        return None

    city_text = getattr(best_band, city_col, best_band.bengaluru)
    parsed = _parse_lpa_range(city_text)
    if not parsed:
        return None

    lo, hi = parsed
    median = (lo + hi) // 2
    spread = max(2, (hi - lo) // 4)
    return (
        max(1, lo - spread),
        lo,
        median,
        hi,
        hi + spread,
    )


def get_salary_reality(
    role: str,
    yoe: float,
    city: str,
    company_type: str = "",
    current_ctc: int | None = None,
) -> SalaryRealityResult:
    """
    Compute salary reality for a role + experience + city combination.
    Falls back to editorial bands when crowdsourced n < MIN_SAMPLE_SIZE.
    """
    cache_key = (
        f"salary_reality:v1:{role.lower()}:{yoe}:{_normalize_city(city)}:"
        f"{company_type}:{current_ctc or 0}"
    )
    cached = cache.get(cache_key)
    if cached:
        return SalaryRealityResult(**cached)

    result = _compute_salary_reality(role, yoe, city, company_type, current_ctc)
    cache.set(cache_key, result.__dict__, timeout=3600)
    return result


def _compute_salary_reality(
    role: str,
    yoe: float,
    city: str,
    company_type: str = "",
    current_ctc: int | None = None,
) -> SalaryRealityResult:
    role = normalize_role(role)
    norm_city = _normalize_city(city)
    yoe_lo = max(0, yoe - 1)
    yoe_hi = yoe + 1

    from django.db.models import Q
    role_q = Q()
    for term in role_search_terms(role)[:3]:
        role_q |= Q(role__icontains=term)

    qs = SalarySubmission.objects.exclude(verification_status="flagged").filter(
        role_q,
        experience_years__gte=yoe_lo,
        experience_years__lte=yoe_hi,
    )
    if company_type:
        qs = qs.filter(company_type=company_type)
    if norm_city and norm_city != "remote":
        qs = qs.filter(city__icontains=norm_city[:4])

    ctcs = sorted(_ctc_to_lpa(s.ctc) for s in qs[:500])
    data_source = "crowdsourced"
    confidence = "high"
    limitation = None

    if len(ctcs) < MIN_SAMPLE_SIZE:
        editorial = _editorial_fallback(role, yoe, city)
        if editorial and ctcs:
            e_p10, e_p25, e_p50, e_p75, e_p90 = editorial
            c_median = ctcs[len(ctcs) // 2] if ctcs else e_p50
            p10 = (e_p10 + _percentile_value(ctcs, 0.1)) // 2 if ctcs else e_p10
            p25 = (e_p25 + _percentile_value(ctcs, 0.25)) // 2 if ctcs else e_p25
            p50 = (e_p50 + c_median) // 2
            p75 = (e_p75 + _percentile_value(ctcs, 0.75)) // 2 if ctcs else e_p75
            p90 = (e_p90 + _percentile_value(ctcs, 0.9)) // 2 if ctcs else e_p90
            sample_size = len(ctcs)
            data_source = "blended"
            confidence = "medium"
        elif editorial:
            p10, p25, p50, p75, p90 = editorial
            sample_size = 0
            data_source = "editorial"
            confidence = "low"
        elif ctcs:
            p10 = _percentile_value(ctcs, 0.1)
            p25 = _percentile_value(ctcs, 0.25)
            p50 = _percentile_value(ctcs, 0.5)
            p75 = _percentile_value(ctcs, 0.75)
            p90 = _percentile_value(ctcs, 0.9)
            sample_size = len(ctcs)
            confidence = "medium" if sample_size < 10 else "high"
        else:
            p10, p25, p50, p75, p90 = 8, 12, 18, 25, 35
            sample_size = 0
            data_source = "editorial"
            confidence = "low"
    else:
        p10 = _percentile_value(ctcs, 0.1)
        p25 = _percentile_value(ctcs, 0.25)
        p50 = _percentile_value(ctcs, 0.5)
        p75 = _percentile_value(ctcs, 0.75)
        p90 = _percentile_value(ctcs, 0.9)
        sample_size = len(ctcs)

    realistic_next = p75
    percentile = None
    pay_label = None
    pay_delta_pct = None
    gap_lpa = None

    if sample_size < MIN_SAMPLE_SIZE and data_source == "editorial":
        limitation = (
            "Limited crowdsourced data for this role and location. "
            "Showing editorial benchmarks — try a broader role or national data."
        )
        confidence = "low"

    if current_ctc:
        all_values = ctcs if ctcs else [p10, p25, p50, p75, p90]
        percentile = _compute_percentile(all_values, current_ctc)
        delta_pct = int((current_ctc - p50) / p50 * 100) if p50 else 0
        pay_delta_pct = delta_pct
        gap_lpa = round(current_ctc - p50, 1)
        if delta_pct < -10:
            pay_label = "underpaid"
        elif delta_pct > 10:
            pay_label = "overpaid"
        else:
            pay_label = "at_market"

    return SalaryRealityResult(
        role=role,
        experience_years=yoe,
        city=city,
        company_type=company_type,
        sample_size=sample_size,
        p10=p10,
        p25=p25,
        p50=p50,
        p75=p75,
        p90=p90,
        realistic_next=realistic_next,
        current_ctc=current_ctc,
        percentile=percentile,
        pay_label=pay_label,
        pay_delta_pct=pay_delta_pct,
        confidence=confidence,
        data_source=data_source,
        gap_lpa=gap_lpa,
        limitation=limitation,
    )
