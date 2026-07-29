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

# Key: (year, month) → baseline. Add new months here each review cycle.
MONTHLY_BASELINES: dict[tuple[int, int], IndexBaseline] = {
    (2026, 6): JUNE_2026_BASELINE,
    (2026, 7): JULY_2026_BASELINE,
}


def editorial_baseline(year: int, month: int) -> IndexBaseline | None:
    return MONTHLY_BASELINES.get((year, month))


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
