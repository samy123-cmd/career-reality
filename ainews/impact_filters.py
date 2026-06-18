"""Filters for IT workplace-impact AI news only (AdSense / crawl hygiene)."""

from __future__ import annotations

import re

# Skip research / benchmark / model-release noise.
SKIP_KEYWORDS: tuple[str, ...] = (
    "benchmark",
    "leaderboard",
    "sota",
    "state-of-the-art",
    "arxiv",
    "preprint",
    "research paper",
    "parameter count",
    "training run",
    "fine-tune benchmark",
    "model roundup",
    "daily model roundup",
    "huggingface trending",
    "open weights release",
    "gpu cluster",
)

# Require at least one signal of day-to-day IT / workplace impact.
IMPACT_KEYWORDS: tuple[str, ...] = (
    "enterprise",
    "copilot",
    "workplace",
    "productivity",
    "developer",
    "engineering",
    "hiring",
    "layoff",
    "workforce",
    "job",
    "security",
    "compliance",
    "gdpr",
    "soc2",
    "policy",
    "regulation",
    "india",
    "outsourc",
    "it services",
    "gcc",
    "remote work",
    "salary",
    "automation",
    "workflow",
    "github",
    "jira",
    "microsoft 365",
    "google workspace",
    "slack",
    "data breach",
    "privacy",
    "ban",
    "visa",
    "h1b",
    "reskill",
    "upskill",
    "performance review",
    "manager",
    "team",
    "deploy",
    "production",
    "incident",
    "on-call",
    "cost cut",
    "restructur",
)

_BUNDLE_TITLE_RE = re.compile(r"daily model roundup|trending feed|papers feed", re.I)


def _haystack(title: str, summary: str, source: str = "") -> str:
    return f"{title} {summary} {source}".lower()


def is_research_noise(title: str, summary: str = "", source: str = "") -> bool:
    text = _haystack(title, summary, source)
    if _BUNDLE_TITLE_RE.search(title):
        return True
    return any(kw in text for kw in SKIP_KEYWORDS)


def has_it_workplace_impact(title: str, summary: str = "", source: str = "", career_angle: str = "") -> bool:
    text = _haystack(title, summary, source) + " " + (career_angle or "").lower()
    if is_research_noise(title, summary, source):
        return False
    return any(kw in text for kw in IMPACT_KEYWORDS)


def passes_ingest_filter(title: str, summary: str = "", source: str = "") -> bool:
    """RSS triage: keep only likely IT workplace items."""
    if is_research_noise(title, summary, source):
        return False
    return has_it_workplace_impact(title, summary, source)
