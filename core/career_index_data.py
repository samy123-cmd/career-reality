"""
Editorial trend baselines for the Career Reality Index.

Blended with live crowdsourced signals when submission volume is low.
Update when market conditions shift materially (monthly review).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndexBaseline:
    salary_pressure: int
    switch_difficulty: int
    layoff_risk: int

    @property
    def overall(self) -> int:
        return int(
            self.salary_pressure * 0.35
            + self.switch_difficulty * 0.35
            + self.layoff_risk * 0.30
        )


# June 2026 — post-appraisal season, selective GCC hiring, elevated IT services risk.
JUNE_2026_BASELINE = IndexBaseline(
    salary_pressure=71,   # Compressed mid-level offers; juniors still flat
    switch_difficulty=59,   # GCC bar rising; counter-offers in senior backend
    layoff_risk=47,         # IT services + mid-tier SaaS signals; not 2023 peak
)

# July 2026 — post-appraisal disappointment, summer hiring slowdown, mid-year bench trimming.
JULY_2026_BASELINE = IndexBaseline(
    salary_pressure=74,   # Late-July: hike disappointment + clawback-heavy offers
    switch_difficulty=64,   # Notice/relieving friction offsets open reqs
    layoff_risk=50,         # Quiet bench trimming continues into August pipeline
)

# August 2026 — post-switch-wave cooling, selective H2 hiring, backlog clearance.
AUGUST_2026_BASELINE = IndexBaseline(
    salary_pressure=72,   # Slight cooling as July offer frenzy settles
    switch_difficulty=62,   # Exit queues clearing; lateral velocity slower than July
    layoff_risk=49,         # Bench trimming quieter; selective cuts continue
)

# Key: (year, month) → baseline. Add new months here each review cycle.
MONTHLY_BASELINES: dict[tuple[int, int], IndexBaseline] = {
    (2026, 6): JUNE_2026_BASELINE,
    (2026, 7): JULY_2026_BASELINE,
    (2026, 8): AUGUST_2026_BASELINE,
}


def latest_baseline_month() -> tuple[int, int]:
    """The most recent (year, month) an editor has published a baseline for."""
    return max(MONTHLY_BASELINES)


def editorial_baseline(year: int, month: int) -> IndexBaseline | None:
    """Baseline for a month, carrying the latest one forward when we run past it.

    Baselines are written by hand each review cycle, so the calendar always
    overtakes them eventually. Carrying the most recent month forward keeps the
    index showing the newest editorial view instead of silently reverting to
    whichever month happened to be hardcoded as a fallback.
    """
    baseline = MONTHLY_BASELINES.get((year, month))
    if baseline is not None:
        return baseline
    if (year, month) > latest_baseline_month():
        return MONTHLY_BASELINES[latest_baseline_month()]
    return None


def blend_with_baseline(
    computed: IndexBaseline,
    baseline: IndexBaseline,
    *,
    data_weight: float,
) -> IndexBaseline:
    """Blend computed crowdsourced scores with editorial baseline."""
    w = max(0.0, min(1.0, data_weight))
    b = 1.0 - w
    return IndexBaseline(
        salary_pressure=round(computed.salary_pressure * w + baseline.salary_pressure * b),
        switch_difficulty=round(computed.switch_difficulty * w + baseline.switch_difficulty * b),
        layoff_risk=round(computed.layoff_risk * w + baseline.layoff_risk * b),
    )
