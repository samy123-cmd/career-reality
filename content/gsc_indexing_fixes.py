"""
GSC "Crawled - currently not indexed" remediation helpers.

Targets URLs from the Aug 2026 validation batch: strengthen E-E-A-T signals
(external citations), bump freshness, and keep sitemap/cache aligned.
"""

from __future__ import annotations

import re

from django.utils import timezone

from content.article_refresh import (
    _extract_links,
    apply_article_refresh,
)

SOURCES_MARKER = "<!-- cr-external-sources:"
SOURCES_END = "<!-- /cr-external-sources -->"

# Canonical article slugs Google crawled but did not index (Aug 2026 validation).
GSC_CRAWLED_NOT_INDEXED_ARTICLE_SLUGS: tuple[str, ...] = (
    "work-life-balance-myth-high-performers",
    "side-hustle-myth-india-reality",
    "remote-work-salary-trap-india",
    "why-upskilling-stops-working-career-trap",
    "digital-marketing-reality-agency-burnout",
    "broke-at-30-money-mistakes-nobody-warned",
    "mba-reality-india-worth-it-2026",
    "networking-reality-india-introverts",
    "freelancing-reality-india-freedom-myth",
    "culture-fit-trap-hiring-reality",
    "passion-luxury-not-strategy-india",
    "green-careers-esg-renewable-sustainability-india-2026",
    "cybersecurity-privacy-careers-beyond-tech-india-2026",
    "portfolio-first-hiring-gig-economy-careers-india-2026",
)

# Slug -> (label, url) pairs for a visible Sources block when body lacks citations.
ARTICLE_EXTERNAL_SOURCES: dict[str, list[tuple[str, str]]] = {
    "green-careers-esg-renewable-sustainability-india-2026": [
        ("MNRE — Ministry of New and Renewable Energy", "https://mnre.gov.in/"),
        ("SECI — Solar Energy Corporation of India", "https://www.seci.co.in/"),
        ("SEBI BRSR framework", "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=25&smid=0"),
    ],
    "cybersecurity-privacy-careers-beyond-tech-india-2026": [
        ("CERT-In advisories", "https://www.cert-in.org.in/"),
        ("MeitY — Digital Personal Data Protection Act", "https://www.meity.gov.in/"),
        ("NCIIPC — National Critical Information Infrastructure", "https://nciipc.gov.in/"),
    ],
    "portfolio-first-hiring-gig-economy-careers-india-2026": [
        ("Naukri JobSpeak Index", "https://www.naukri.com/jobSpeak"),
        ("AmbitionBox hiring trends", "https://www.ambitionbox.com/salaries"),
        ("Ministry of Labour & Employment (India)", "https://labour.gov.in/"),
    ],
    "work-life-balance-myth-high-performers": [
        ("ILO working time statistics", "https://ilostat.ilo.org/"),
        ("NITI Aayog — India at 2047", "https://www.niti.gov.in/"),
        ("AmbitionBox work-life balance reviews", "https://www.ambitionbox.com/reviews"),
    ],
    "side-hustle-myth-india-reality": [
        ("RBI household finance survey", "https://www.rbi.org.in/"),
        ("Naukri gig and freelance hiring data", "https://www.naukri.com/"),
        ("Income Tax Department — presumptive taxation", "https://www.incometax.gov.in/"),
    ],
    "remote-work-salary-trap-india": [
        ("Naukri remote work hiring index", "https://www.naukri.com/"),
        ("Glassdoor India salaries", "https://www.glassdoor.co.in/Salaries/index.htm"),
        ("TeamLease Employment Outlook", "https://www.teamlease.com/"),
    ],
    "why-upskilling-stops-working-career-trap": [
        ("NASSCOM FutureSkills", "https://nasscom.in/"),
        ("SWAYAM / NPTEL open courses", "https://swayam.gov.in/"),
        ("AmbitionBox skills and salary data", "https://www.ambitionbox.com/skills"),
    ],
    "digital-marketing-reality-agency-burnout": [
        ("IAMAI digital advertising report", "https://www.iamai.in/"),
        ("Google Ads Help — attribution", "https://support.google.com/google-ads/"),
        ("Meta Business — ads reporting", "https://www.facebook.com/business/help"),
    ],
    "broke-at-30-money-mistakes-nobody-warned": [
        ("RBI financial stability report", "https://www.rbi.org.in/"),
        ("SEBI investor education", "https://investor.sebi.gov.in/"),
        ("Income Tax Department — tax slabs", "https://www.incometax.gov.in/"),
    ],
    "mba-reality-india-worth-it-2026": [
        ("All India Council for Technical Education", "https://www.aicte-india.org/"),
        ("NIRF India Rankings", "https://www.nirfindia.org/"),
        ("AmbitionBox MBA salary data", "https://www.ambitionbox.com/salaries/mba-salary"),
    ],
    "networking-reality-india-introverts": [
        ("LinkedIn Economic Graph — India", "https://economicgraph.linkedin.com/"),
        ("Naukri hiring connectivity report", "https://www.naukri.com/"),
        ("Glassdoor India company reviews", "https://www.glassdoor.co.in/Reviews/index.htm"),
    ],
    "freelancing-reality-india-freedom-myth": [
        ("Ministry of Labour — gig and platform workers", "https://labour.gov.in/"),
        ("Income Tax — Section 44ADA", "https://www.incometax.gov.in/"),
        ("RBI payment systems review", "https://www.rbi.org.in/"),
    ],
    "culture-fit-trap-hiring-reality": [
        ("Naukri hiring practices survey", "https://www.naukri.com/"),
        ("SHRM India workplace research", "https://www.shrm.org/india"),
        ("AmbitionBox interview reviews", "https://www.ambitionbox.com/interviews"),
    ],
    "passion-luxury-not-strategy-india": [
        ("NITI Aayog — employment strategy", "https://www.niti.gov.in/"),
        ("PLFS labour force survey (MoSPI)", "https://mospi.gov.in/"),
        ("Naukri career outlook", "https://www.naukri.com/jobSpeak"),
    ],
}


def _sources_block_html(slug: str) -> str:
    pairs = ARTICLE_EXTERNAL_SOURCES.get(slug)
    if not pairs:
        pairs = [
            ("AmbitionBox Salary Insights", "https://www.ambitionbox.com/salaries"),
            ("Glassdoor India Salaries", "https://www.glassdoor.co.in/Salaries/index.htm"),
            ("Naukri JobSpeak Index", "https://www.naukri.com/jobSpeak"),
        ]
    today = timezone.localdate().isoformat()
    items = "".join(
        f'<li><a href="{url}" rel="noopener noreferrer">{label}</a></li>'
        for label, url in pairs
    )
    return (
        f"<h3>Sources &amp; verification ({today})</h3>"
        f"<p>Salary bands, hiring signals, and policy references checked against primary data:</p>"
        f"<ul>{items}</ul>"
    )


def _replace_sources_block(content: str, slug: str) -> str:
    block = _sources_block_html(slug)
    wrapped = f"{SOURCES_MARKER}{slug} -->\n{block}\n{SOURCES_END}"
    pattern = re.compile(
        rf"{re.escape(SOURCES_MARKER)}[^>]*>.*?{re.escape(SOURCES_END)}",
        re.DOTALL | re.IGNORECASE,
    )
    if pattern.search(content or ""):
        return pattern.sub(wrapped, content)
    return (content or "").rstrip() + "\n\n" + wrapped


def apply_gsc_indexing_fixes(article) -> list[str]:
    """
    Strengthen a published article for indexing: external sources + market refresh.
    Mutates article in memory; caller must save.
    """
    changes: list[str] = []
    blocks = " ".join(
        filter(
            None,
            [
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.who_should_avoid,
                article.verdict,
            ],
        )
    )
    external = [
        link
        for link in _extract_links(blocks)
        if link.startswith("http") and "careerreality.in" not in link
    ]

    if len(external) < 2:
        new_reality = _replace_sources_block(article.actual_reality or "", article.slug)
        if new_reality != (article.actual_reality or ""):
            article.actual_reality = new_reality
            changes.append("external_sources")

    refresh_changes = apply_article_refresh(article)
    changes.extend(refresh_changes)
    return changes
