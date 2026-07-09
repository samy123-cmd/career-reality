"""Detect and remove duplicated editorial padding from article bodies."""

from __future__ import annotations

import re

# Generic word-count padding injected by legacy expansion scripts.
SAFETY_PAD_TEXT = (
    "Indian IT compensation decisions in 2026 should always be stress-tested with "
    "in-hand cash flow, not headline CTC alone. Use structured comparison tools, talk "
    "to three people who made the same choice last year, and write down your "
    "assumptions before committing — ambiguity favors employers and coaching "
    "marketers, not candidates."
)

_SAFETY_PAD_HTML = re.compile(
    r"<p>\s*Indian IT compensation decisions in 2026 should always be stress-tested.*?</p>\s*",
    re.IGNORECASE | re.DOTALL,
)


def strip_safety_pad(html: str | None) -> str:
    """Remove repeated generic padding paragraphs from article HTML fields."""
    if not html:
        return html or ""
    cleaned = html
    while _SAFETY_PAD_HTML.search(cleaned):
        cleaned = _SAFETY_PAD_HTML.sub("", cleaned, count=1)
    return cleaned.strip()
