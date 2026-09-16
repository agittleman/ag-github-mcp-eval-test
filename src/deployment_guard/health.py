from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseHealth:
    release: str
    error_rate: float
    p95_latency_ms: int


def regression_score(current: ReleaseHealth, baseline: ReleaseHealth) -> float:
    """Return a non-negative score where larger values indicate more risk."""
    error_delta = max(0.0, current.error_rate - baseline.error_rate) * 10_000
    latency_delta = max(0, current.p95_latency_ms - baseline.p95_latency_ms)
    return round(error_delta + latency_delta, 2)
