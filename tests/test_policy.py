import pytest

from deployment_guard.health import ReleaseHealth, regression_score
from deployment_guard.policy import (
    DeploymentPolicy,
    DeploymentSignal,
    evaluate_deployment,
)
from deployment_guard.rollback import build_rollback_plan


def test_healthy_deployment_is_allowed() -> None:
    decision = evaluate_deployment(
        DeploymentSignal(ci_passed=True, error_rate=0.005, p95_latency_ms=220)
    )
    assert decision.allowed
    assert decision.blockers == ()


def test_regressions_block_deployment() -> None:
    decision = evaluate_deployment(
        DeploymentSignal(ci_passed=False, error_rate=0.04, p95_latency_ms=900),
        DeploymentPolicy(max_error_rate=0.01, max_p95_latency_ms=400),
    )
    assert not decision.allowed
    assert len(decision.blockers) == 3


def test_retry_window_must_be_positive() -> None:
    with pytest.raises(ValueError):
        evaluate_deployment(
            DeploymentSignal(True, 0.0, 100),
            DeploymentPolicy(retry_window_minutes=0),
        )


def test_rollback_plan_restores_previous_release() -> None:
    plan = build_rollback_plan("v1.1.0", "v1.0.0")
    assert plan.previous_release in plan.steps[1]


def test_rollback_rejects_active_release() -> None:
    with pytest.raises(ValueError):
        build_rollback_plan("v1.1.0", "v1.1.0")


def test_regression_score_combines_errors_and_latency() -> None:
    baseline = ReleaseHealth("v1.0.0", error_rate=0.01, p95_latency_ms=200)
    current = ReleaseHealth("v1.1.0", error_rate=0.02, p95_latency_ms=250)
    assert regression_score(current, baseline) == 150
