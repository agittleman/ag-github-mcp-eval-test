from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentPolicy:
    max_error_rate: float = 0.02
    max_p95_latency_ms: int = 500
    require_ci: bool = True
    retry_window_minutes: int = 15


@dataclass(frozen=True)
class DeploymentSignal:
    ci_passed: bool
    error_rate: float
    p95_latency_ms: int


@dataclass(frozen=True)
class DeploymentDecision:
    allowed: bool
    blockers: tuple[str, ...]


def evaluate_deployment(
    signal: DeploymentSignal,
    policy: DeploymentPolicy = DeploymentPolicy(),
) -> DeploymentDecision:
    if policy.retry_window_minutes < 1:
        raise ValueError("retry window must be at least one minute")
    blockers: list[str] = []
    if policy.require_ci and not signal.ci_passed:
        blockers.append("continuous integration is failing")
    if signal.error_rate > policy.max_error_rate:
        blockers.append(
            f"error rate {signal.error_rate:.2%} exceeds "
            f"{policy.max_error_rate:.2%}"
        )
    if signal.p95_latency_ms > policy.max_p95_latency_ms:
        blockers.append(
            f"p95 latency {signal.p95_latency_ms}ms exceeds "
            f"{policy.max_p95_latency_ms}ms"
        )
    return DeploymentDecision(allowed=not blockers, blockers=tuple(blockers))
