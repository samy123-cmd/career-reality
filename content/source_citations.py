"""Article-specific source citation helpers."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from django.utils import timezone

_EXTERNAL_LINK_RE = re.compile(
    r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)

_CATEGORY_DEFAULTS: dict[str, list[tuple[str, str]]] = {
    "data": [
        ("Kaggle State of Data/AI", "https://www.kaggle.com/"),
    ],
    "design": [
        ("Dribbble Salary Guide", "https://dribbble.com/resources"),
    ],
    "product": [
        ("Product Management Salary Benchmarks", "https://www.productledalliance.com/"),
    ],
}

_BASE_SOURCES = [
    ("AmbitionBox Salary Insights", "https://www.ambitionbox.com/salaries"),
    ("Glassdoor India Salaries", "https://www.glassdoor.co.in/Salaries/index.htm"),
    ("Naukri JobSpeak Index", "https://www.naukri.com/jobSpeak"),
]


def _checked_on(article):
    checked_on = article.last_reality_check
    if checked_on is None and article.updated_at:
        checked_on = timezone.localtime(article.updated_at).date()
    return checked_on or timezone.localdate()


def _name_from_url(url: str) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    mapping = {
        "ambitionbox.com": "AmbitionBox Salary Insights",
        "glassdoor.co.in": "Glassdoor India Salaries",
        "naukri.com": "Naukri Jobs (India)",
        "linkedin.com": "LinkedIn Jobs (India)",
        "labour.gov.in": "Ministry of Labour & Employment (India)",
        "kaggle.com": "Kaggle State of Data/AI",
    }
    for key, label in mapping.items():
        if key in host:
            return label
    return host.replace(".", " ").title()


def extract_body_sources(article) -> list[dict]:
    """Pull external citations already referenced in article body HTML."""
    checked_on = _checked_on(article)
    blocks = [
        article.common_expectation,
        article.actual_reality,
        article.salary_reality,
        article.stuck_point,
        article.who_should_avoid,
        article.verdict,
    ]
    combined = " ".join(blocks)
    seen: set[str] = set()
    sources: list[dict] = []
    for match in _EXTERNAL_LINK_RE.finditer(combined):
        url = match.group(1).strip()
        if "careerreality.in" in url or url in seen:
            continue
        seen.add(url)
        anchor_text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        name = anchor_text if anchor_text and len(anchor_text) < 80 else _name_from_url(url)
        sources.append({"name": name, "url": url, "checked_on": checked_on})
    return sources


def article_source_references(article) -> list[dict]:
    """Prefer article-body citations; fall back to category-aware defaults."""
    body_sources = extract_body_sources(article)
    if len(body_sources) >= 3:
        return body_sources[:6]

    checked_on = _checked_on(article)
    category_name = (article.category.name or "").lower()
    extras: list[tuple[str, str]] = []
    for key, items in _CATEGORY_DEFAULTS.items():
        if key in category_name:
            extras.extend(items)

    merged: list[dict] = []
    seen_urls: set[str] = set()
    for name, url in [(n, u) for n, u in _BASE_SOURCES] + extras:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        merged.append({"name": name, "url": url, "checked_on": checked_on})
    for item in body_sources:
        if item["url"] not in seen_urls:
            seen_urls.add(item["url"])
            merged.append(item)
    return merged[:6]
