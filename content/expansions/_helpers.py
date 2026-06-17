"""Shared helpers for core article expansions."""

from __future__ import annotations

import re
from typing import Any

TEXT_FIELDS = (
    "target_persona",
    "who_should_avoid",
    "common_expectation",
    "actual_reality",
    "salary_reality",
    "stuck_point",
    "verdict",
)


def _strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value or "")


def expansion_word_count(data: dict[str, Any]) -> int:
    return len(_strip_html(" ".join(data.get(f, "") or "" for f in TEXT_FIELDS)).split())


def expansion_salary_words(data: dict[str, Any]) -> int:
    return len(_strip_html(data.get("salary_reality", "")).split())


def resolve_slugs(primary: str, data: dict[str, Any]) -> list[str]:
    """Primary slug plus optional aliases that should receive the same body."""
    aliases = data.get("aliases") or []
    return [primary, *aliases]
