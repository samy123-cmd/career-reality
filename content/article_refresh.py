"""
Audit and refresh utilities for published articles.

Designed for daily cron runs: detect stale content, append idempotent market/salary
blocks, add external sources, and bump last_reality_check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

from django.utils import timezone

from content.article_market_data import (
    EXTERNAL_SOURCES_HTML,
    MARKET_LABEL,
    MARKET_PERIOD,
    market_update_html,
    role_cluster_for_article,
    salary_table_html,
)

MARKET_MARKER = "<!-- cr-market-update:"
SALARY_MARKER = "<!-- cr-salary-refresh:"
SOURCES_MARKER = "<!-- cr-source-refs -->"
SOURCES_END = "<!-- /cr-source-refs -->"

YEAR_RE = re.compile(r"\b(20\d{2})\b")


def _strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value or "")


def _extract_links(value: str) -> list[str]:
    return re.findall(r"<a\s+[^>]*href=['\"]([^'\"]+)['\"]", value or "", flags=re.I)


def _replace_marked_block(content: str, marker_prefix: str, end_marker: str, new_block: str) -> str:
    """Replace or append a marked HTML block."""
    pattern = re.compile(
        rf"{re.escape(marker_prefix)}[^>]*>.*?{re.escape(end_marker)}",
        re.DOTALL | re.IGNORECASE,
    )
    wrapped = f"{marker_prefix}{MARKET_PERIOD} -->\n{new_block}\n{end_marker}"
    if pattern.search(content or ""):
        return pattern.sub(wrapped, content)
    return (content or "").rstrip() + "\n\n" + wrapped


def _replace_sources_block(content: str) -> str:
    pattern = re.compile(
        rf"{re.escape(SOURCES_MARKER)}.*?{re.escape(SOURCES_END)}",
        re.DOTALL | re.IGNORECASE,
    )
    wrapped = f"{SOURCES_MARKER}\n{EXTERNAL_SOURCES_HTML}\n{SOURCES_END}"
    if pattern.search(content or ""):
        return pattern.sub(wrapped, content)
    if "ambitionbox.com" in (content or "").lower():
        return content
    return (content or "").rstrip() + "\n\n" + wrapped


def _has_external_links(content: str) -> bool:
    for link in _extract_links(content):
        if link.startswith("http") and "careerreality.in" not in link:
            return True
    return False


def _word_count(article) -> int:
    blocks = [
        article.common_expectation,
        article.actual_reality,
        article.salary_reality,
        article.stuck_point,
        article.who_should_avoid,
        article.verdict,
    ]
    return len(_strip_html(" ".join(blocks)).split())


def _salary_words(article) -> int:
    return len(_strip_html(article.salary_reality).split())


def _current_market_marker(content: str) -> str | None:
    match = re.search(r"<!-- cr-market-update:([\d-]+) -->", content or "")
    return match.group(1) if match else None


def refresh_meta_years(meta: str, current_year: int) -> str:
    """Bump stale year references in meta strings (2024/2025 → current year)."""
    if not meta:
        return meta

    def replacer(m: re.Match) -> str:
        year = int(m.group(1))
        if year < current_year - 1:
            return str(current_year)
        return m.group(1)

    return YEAR_RE.sub(replacer, meta)


@dataclass
class ArticleAudit:
    slug: str
    title: str
    word_count: int
    salary_words: int
    internal_links: int
    external_links: int
    last_reality_check: date | None
    updated_at: date
    market_period: str | None
    cluster: str
    stale: bool
    needs_refresh: bool
    issues: list[str] = field(default_factory=list)


def audit_article(article, *, today: date | None = None, stale_days: int = 30) -> ArticleAudit:
    today = today or timezone.localdate()
    blocks = " ".join(
        filter(
            None,
            [
                article.target_persona,
                article.common_expectation,
                article.actual_reality,
                article.salary_reality,
                article.stuck_point,
                article.who_should_avoid,
                article.verdict,
            ],
        )
    )
    links = _extract_links(blocks)
    internal = [l for l in links if l.startswith("/") or "careerreality.in" in l]
    external = [l for l in links if l.startswith("http") and "careerreality.in" not in l]
    cluster = role_cluster_for_article(article.slug, getattr(article.category, "name", ""))
    market_period = _current_market_marker(article.actual_reality)

    issues: list[str] = []
    if _word_count(article) < 900:
        issues.append(f"low_word_count:{_word_count(article)}")
    if _salary_words(article) < 150:
        issues.append(f"thin_salary_section:{_salary_words(article)}")
    if len(internal) < 2:
        issues.append(f"low_internal_links:{len(internal)}")
    if len(external) < 2:
        issues.append("missing_external_sources")
    if not article.last_reality_check:
        issues.append("missing_last_reality_check")
    elif article.last_reality_check < today - timedelta(days=stale_days):
        issues.append(f"stale_reality_check:{article.last_reality_check.isoformat()}")

    if market_period != MARKET_PERIOD:
        issues.append(f"market_block_outdated:{market_period or 'none'}")

    meta = article.meta_description or ""
    for match in YEAR_RE.finditer(meta):
        if int(match.group(1)) < today.year - 1:
            issues.append(f"stale_meta_year:{match.group(1)}")
            break

    stale = bool(issues)
    needs_refresh = any(
        i.startswith(("missing_", "stale_", "market_block", "missing_external", "thin_salary"))
        for i in issues
    )

    return ArticleAudit(
        slug=article.slug,
        title=article.title,
        word_count=_word_count(article),
        salary_words=_salary_words(article),
        internal_links=len(internal),
        external_links=len(external),
        last_reality_check=article.last_reality_check,
        updated_at=article.updated_at.date(),
        market_period=market_period,
        cluster=cluster,
        stale=stale,
        needs_refresh=needs_refresh,
        issues=issues,
    )


def apply_article_refresh(article, *, today: date | None = None) -> list[str]:
    """
    Apply idempotent refresh blocks to an article. Returns list of change labels.
    Mutates article in memory; caller must save.
    """
    today = today or timezone.localdate()
    changes: list[str] = []
    cluster = role_cluster_for_article(article.slug, getattr(article.category, "name", ""))
    current_year = today.year

    new_reality = _replace_marked_block(
        article.actual_reality,
        MARKET_MARKER,
        "<!-- /cr-market-update -->",
        market_update_html(cluster),
    )
    if new_reality != (article.actual_reality or ""):
        article.actual_reality = new_reality
        changes.append("market_update")

    if _salary_words(article) < 200 or SALARY_MARKER not in (article.salary_reality or ""):
        salary_block = (
            f"<h3>Updated median bands ({MARKET_LABEL})</h3>\n{salary_table_html(cluster)}"
        )
        new_salary = _replace_marked_block(
            article.salary_reality,
            SALARY_MARKER,
            "<!-- /cr-salary-refresh -->",
            salary_block,
        )
        if new_salary != (article.salary_reality or ""):
            article.salary_reality = new_salary
            changes.append("salary_bands")

    if not _has_external_links(article.actual_reality):
        new_reality = _replace_sources_block(article.actual_reality)
        if new_reality != article.actual_reality:
            article.actual_reality = new_reality
            changes.append("external_sources")

    new_meta = refresh_meta_years(article.meta_description, current_year)
    if new_meta != article.meta_description:
        article.meta_description = new_meta[:160]
        changes.append("meta_year")

    new_title = refresh_meta_years(article.meta_title, current_year)
    if new_title != article.meta_title:
        article.meta_title = new_title[:60]
        changes.append("title_year")

    article.last_reality_check = today
    changes.append("last_reality_check")

    return changes


def build_audit_report_markdown(audits: list[ArticleAudit], *, period: str = MARKET_PERIOD) -> str:
    today = timezone.localdate()
    total = len(audits)
    stale = [a for a in audits if a.needs_refresh]
    clean = [a for a in audits if not a.stale]

    lines = [
        "# Article Freshness Audit",
        "",
        f"Generated: {today.isoformat()}",
        f"Market period: {period} ({MARKET_LABEL})",
        f"Published articles: {total}",
        f"Needs refresh: {len(stale)}",
        f"Up to date: {len(clean)}",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| Needs refresh | {len(stale)} |",
        f"| Minor issues only | {len([a for a in audits if a.stale and not a.needs_refresh])} |",
        f"| Clean | {len(clean)} |",
        "",
    ]

    if stale:
        lines.extend(["## Articles updated / needing update", ""])
        for a in sorted(stale, key=lambda x: x.slug):
            lines.append(f"### {a.title} (`{a.slug}`)")
            lines.append("")
            lines.append(
                f"- Cluster: **{a.cluster}** | Words: {a.word_count} | "
                f"Salary words: {a.salary_words} | External links: {a.external_links}"
            )
            lines.append(f"- Last reality check: {a.last_reality_check or 'never'}")
            lines.append(f"- Market block: {a.market_period or 'none'} → target **{period}**")
            lines.append(f"- Issues: {', '.join(a.issues)}")
            lines.append("")

    lines.extend(["## All articles", ""])
    lines.append("| Slug | Cluster | Words | Last check | Market period | Issues |")
    lines.append("|------|---------|-------|------------|---------------|--------|")
    for a in sorted(audits, key=lambda x: x.slug):
        issues = "; ".join(a.issues) if a.issues else "—"
        lines.append(
            f"| `{a.slug}` | {a.cluster} | {a.word_count} | "
            f"{a.last_reality_check or '—'} | {a.market_period or '—'} | {issues} |"
        )
    lines.append("")
    return "\n".join(lines)
