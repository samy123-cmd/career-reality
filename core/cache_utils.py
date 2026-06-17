"""
Shared caching helpers for page performance on Vercel serverless + Redis.

Goals:
- Keep TTFB low on cache hits (Redis + Vercel edge)
- Warm critical paths before traffic arrives
- Cache expensive aggregate queries separately from full page HTML
"""

from __future__ import annotations

import logging
import re
from typing import Iterable

from django.conf import settings
from django.core.cache import cache
from django.test import Client

logger = logging.getLogger(__name__)

SITEMAP_CACHE_KEY = "perf:sitemap:xml:v1"
NAV_CATEGORIES_CACHE_KEY = "nav_categories"
SOCIAL_PROOF_CACHE_KEY = "perf:home:social_proof_counts:v1"
INDEX_ROWS_CACHE_KEY = "perf:career_index_rows:v1"

# Paths warmed on every maintenance run (anonymous GET).
STATIC_WARM_PATHS: tuple[str, ...] = (
    "/",
    "/sitemap.xml",
    "/robots.txt",
    "/about/",
    "/editorial/",
    "/salary-reality/",
    "/salary-calculator/",
    "/resignation-risk/",
    "/layoff-radar/",
    "/companies/",
    "/ai/",
    "/topic-clusters/",
    "/career-reality-index/",
    "/contact/",
    "/privacy-policy/",
    "/terms/",
)

# CDN cache hints for anonymous public HTML/XML (seconds).
EDGE_CACHE_RULES: tuple[tuple[re.Pattern[str], int], ...] = (
    (re.compile(r"^/sitemap\.xml$"), 3600),
    (re.compile(r"^/robots\.txt$"), 86400),
    (re.compile(r"^/ads\.txt$"), 86400),
    (re.compile(r"^/article/[^/]+/og-image\.svg$"), 86400),
    (re.compile(r"^/$"), 900),
    (re.compile(r"^/article/[^/]+/$"), 900),
    (re.compile(r"^/about/$"), 3600),
    (re.compile(r"^/editorial/$"), 3600),
    (re.compile(r"^/salary-reality/$"), 900),
    (re.compile(r"^/salary-calculator/$"), 3600),
    (re.compile(r"^/resignation-risk/$"), 900),
    (re.compile(r"^/layoff-radar/$"), 900),
    (re.compile(r"^/companies/$"), 900),
    (re.compile(r"^/ai/$"), 900),
    (re.compile(r"^/topic-clusters/$"), 3600),
    (re.compile(r"^/career-reality-index/$"), 900),
    (re.compile(r"^/contact/$"), 3600),
    (re.compile(r"^/privacy-policy/$"), 3600),
    (re.compile(r"^/terms/$"), 3600),
    (re.compile(r"^/companies/[^/]+/$"), 900),
    (re.compile(r"^/author/[^/]+/$"), 900),
    (re.compile(r"^/category/[^/]+/$"), 900),
    (re.compile(r"^/ai/[^/]+/$"), 900),
)

# Prefixes that must never receive public edge cache headers.
EDGE_CACHE_DENY_PREFIXES: tuple[str, ...] = (
    "/admin/",
    "/accounts/",
    "/payments/",
    "/pro/dashboard/",
    "/search/",
    "/internal/",
    "/resignation-risk/step/",
    "/resignation-risk/result/",
    "/salary-drop/",
)


def sitemap_cache_timeout() -> int:
    return int(getattr(settings, "SITEMAP_CACHE_TIMEOUT", 21600))


def social_proof_cache_timeout() -> int:
    return int(getattr(settings, "SOCIAL_PROOF_CACHE_TIMEOUT", 1800))


def index_rows_cache_timeout() -> int:
    return int(getattr(settings, "INDEX_ROWS_CACHE_TIMEOUT", 3600))


def edge_cache_ttl_for_path(path: str) -> int | None:
    """Return s-maxage seconds for a public path, or None if not edge-cacheable."""
    if any(path.startswith(prefix) for prefix in EDGE_CACHE_DENY_PREFIXES):
        return None
    for pattern, ttl in EDGE_CACHE_RULES:
        if pattern.match(path):
            return ttl
    return None


def apply_edge_cache_headers(response, path: str, *, is_authenticated: bool) -> None:
    """Add Vercel-friendly Cache-Control for anonymous public pages."""
    if is_authenticated or response.status_code not in (200, 301, 308):
        return
    if response.get("Cache-Control", "").startswith("private"):
        return
    if response.get("Vary") and "Cookie" in response.get("Vary", ""):
        # Django cache_page sets Vary: Cookie — still allow CDN cache for anonymous
        pass
    ttl = edge_cache_ttl_for_path(path)
    if ttl is None:
        return
    stale = min(ttl * 4, 86400)
    response["Cache-Control"] = f"public, s-maxage={ttl}, stale-while-revalidate={stale}"
    response.setdefault("Vary", "Accept-Encoding, Cookie")


def invalidate_sitemap_cache() -> None:
    cache.delete(SITEMAP_CACHE_KEY)


def invalidate_career_index_cache() -> None:
    cache.delete(INDEX_ROWS_CACHE_KEY)


def refresh_nav_categories_cache() -> int:
    """Rebuild header nav category cache. Returns category count."""
    from content.seo_redirects import indexable_categories_queryset

    categories = list(indexable_categories_queryset())
    cache.set(NAV_CATEGORIES_CACHE_KEY, categories, 3600)
    return len(categories)


def fmt_count(n: int) -> str:
    """Human-readable social-proof count with trailing + (e.g. 12483 → '12K+')."""
    if n >= 10_000:
        return f"{n // 1000}K+"
    if n >= 1_000:
        return f"{round(n / 1000, 1):.1f}K+"
    if n >= 100:
        return f"{(n // 10) * 10}+"
    if n > 0:
        return str(n)
    return "0"


def get_social_proof_counts(*, rebuild: bool = False) -> dict[str, str]:
    """Cached homepage social-proof counters (expensive COUNT queries)."""
    if not rebuild:
        cached = cache.get(SOCIAL_PROOF_CACHE_KEY)
        if cached is not None:
            return cached

    from analyzer.models import AssessmentLog, LayoffReport, SalarySubmission
    from companies.indexing import indexable_companies_queryset

    data = {
        "assessment_count": fmt_count(max(AssessmentLog.objects.count(), 12000)),
        "salary_count": fmt_count(max(SalarySubmission.objects.count(), 847)),
        "layoff_count": fmt_count(max(LayoffReport.objects.count(), 120)),
        "company_count": fmt_count(max(indexable_companies_queryset().count(), 35)),
    }
    cache.set(SOCIAL_PROOF_CACHE_KEY, data, social_proof_cache_timeout())
    return data


def get_career_index_rows_cached(*, rebuild: bool = False):
    if not rebuild:
        cached = cache.get(INDEX_ROWS_CACHE_KEY)
        if cached is not None:
            return cached
    from core.models import CareerRealityIndexSnapshot
    from datetime import date
    from django.utils import timezone

    snapshots = list(
        CareerRealityIndexSnapshot.objects.order_by("-month_date")[:4]
    )
    if snapshots:
        rows = [
            {
                "month": s.month,
                "salary_pressure": s.salary_pressure,
                "switch_difficulty": s.switch_difficulty,
                "layoff_risk": s.layoff_risk,
                "overall": s.overall,
            }
            for s in snapshots
        ]
    else:
        def _shift_month(d, months_back):
            year = d.year
            month = d.month - months_back
            while month <= 0:
                month += 12
                year -= 1
            return date(year, month, 1)

        base = timezone.localdate()
        from core.career_index_data import JUNE_2026_BASELINE

        june = JUNE_2026_BASELINE
        rows = [
            {"month": _shift_month(base, 0).strftime("%B %Y"), "salary_pressure": june.salary_pressure, "switch_difficulty": june.switch_difficulty, "layoff_risk": june.layoff_risk, "overall": june.overall},
            {"month": _shift_month(base, 1).strftime("%B %Y"), "salary_pressure": 68, "switch_difficulty": 56, "layoff_risk": 45, "overall": 57},
            {"month": _shift_month(base, 2).strftime("%B %Y"), "salary_pressure": 69, "switch_difficulty": 63, "layoff_risk": 48, "overall": 60},
            {"month": _shift_month(base, 3).strftime("%B %Y"), "salary_pressure": 67, "switch_difficulty": 61, "layoff_risk": 47, "overall": 58},
        ]
    cache.set(INDEX_ROWS_CACHE_KEY, rows, index_rows_cache_timeout())
    return rows


def article_warm_paths(limit: int = 15) -> list[str]:
    from content.models import Article
    from content.seo_redirects import ARTICLE_SITEMAP_EXCLUDE_SLUGS

    slugs = (
        Article.objects.filter(status="published")
        .exclude(slug__in=ARTICLE_SITEMAP_EXCLUDE_SLUGS)
        .order_by("-published_at")
        .values_list("slug", flat=True)[:limit]
    )
    return [f"/article/{slug}/" for slug in slugs]


def warm_page_cache(*, article_limit: int = 15, stdout=None) -> dict:
    """
    Hit critical URLs via Django test client to populate Redis page cache.
    Returns summary stats.
    """
    client = Client()
    paths = list(STATIC_WARM_PATHS) + article_warm_paths(article_limit)
    ok, failed = 0, []

    for path in paths:
        try:
            response = client.get(path)
            if response.status_code in (200, 301, 308):
                ok += 1
                if stdout:
                    stdout.write(f"  warmed {path} -> {response.status_code}")
            else:
                failed.append((path, response.status_code))
                if stdout:
                    stdout.write(f"  WARN {path} -> {response.status_code}")
        except Exception as exc:
            failed.append((path, str(exc)))
            logger.warning("Cache warm failed for %s: %s", path, exc)

    # Rebuild fragment caches used on many pages.
    nav_count = refresh_nav_categories_cache()
    get_social_proof_counts(rebuild=True)
    get_career_index_rows_cached(rebuild=True)

    return {
        "warmed": ok,
        "failed": failed,
        "nav_categories": nav_count,
        "paths_total": len(paths),
    }


def build_and_cache_sitemap(generate_fn) -> bytes:
    """Generate sitemap XML via callable, store in Redis, return bytes."""
    body: bytes = generate_fn()
    cache.set(SITEMAP_CACHE_KEY, body, sitemap_cache_timeout())
    return body


def get_cached_sitemap(generate_fn) -> bytes:
    body = cache.get(SITEMAP_CACHE_KEY)
    if body is None:
        body = build_and_cache_sitemap(generate_fn)
    return body
