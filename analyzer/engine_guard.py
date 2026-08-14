"""Failure boundary between the career tools and their analysis engines.

An engine is a pure computation over crowdsourced and editorial data. When one
raises — bad data, a downstream lookup, an arithmetic edge case — the user must
still get their page back with their input intact, and the failure must reach
monitoring with enough context to identify the engine and the inputs involved.

Without this boundary a single malformed row turns every affected tool into a
500, which is both a lost session and an invisible outage.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)

#: Shown in place of a result. States what happened and what to do next.
ENGINE_ERROR_MESSAGE = (
    "We could not complete this analysis just now. Your answers are saved below — "
    "try again in a moment, and if it keeps happening the data team is already notified."
)


def run_engine(
    engine: str,
    fn: Callable[..., Any],
    *args: Any,
    _context: dict | None = None,
    **kwargs: Any,
) -> tuple[Any, str | None]:
    """Run an analysis engine, converting failure into a user-facing message.

    Returns ``(result, error)``. Exactly one is ever non-None.

    Args:
        engine: Stable identifier used for log filtering and alerting.
        fn: The engine callable.
        _context: Extra detail to log (never rendered to the user).
    """
    try:
        return fn(*args, **kwargs), None
    except Exception:
        logger.exception(
            "Career engine failed | engine=%s context=%s",
            engine,
            _context or {},
        )
        return None, ENGINE_ERROR_MESSAGE


def safe_engine(engine: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run a supporting engine whose failure should not block the page.

    Used for dashboard panels: a broken salary lookup should cost the user that
    one card, not the whole dashboard. Returns None on failure.
    """
    result, _ = run_engine(engine, fn, *args, **kwargs)
    return result
