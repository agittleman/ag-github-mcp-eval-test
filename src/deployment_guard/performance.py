from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceBudget:
    p95_latency_ms: int
    maximum_regression_percent: float


def exceeds_performance_budget(
    baseline_p95_ms: int,
    candidate_p95_ms: int,
    budget: PerformanceBudget,
) -> bool:
    if baseline_p95_ms <= 0:
        raise ValueError("baseline latency must be positive")
    regression = ((candidate_p95_ms - baseline_p95_ms) / baseline_p95_ms) * 100
    return (
        candidate_p95_ms > budget.p95_latency_ms
        or regression > budget.maximum_regression_percent
    )
