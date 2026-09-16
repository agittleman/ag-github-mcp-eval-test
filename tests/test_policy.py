import pytest

from deployment_guard.audit import deployment_event
from deployment_guard.canary import promotion_plan
from deployment_guard.health import ReleaseHealth, regression_score
from deployment_guard.marker import create_marker
from deployment_guard.performance import (
    PerformanceBudget,
    exceeds_performance_budget,
)
from deployment_guard.policy import (
    DeploymentPolicy,
    DeploymentSignal,
    evaluate_deployment,
)
from deployment_guard.rollback import build_rollback_plan
from deployment_guard.status import DeploymentStatus


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


def test_status_response_includes_rollback_readiness() -> None:
    baseline = ReleaseHealth("v1.0.0", error_rate=0.01, p95_latency_ms=200)
    current = ReleaseHealth("v1.1.0", error_rate=0.02, p95_latency_ms=250)
    response = DeploymentStatus("production", current, baseline, True).as_response()
    assert response["rollback_ready"] is True
    assert response["regression_score"] == 150


def test_audit_event_rejects_unknown_action() -> None:
    with pytest.raises(ValueError):
        deployment_event("deploy-42", "retry", "transient failure")


def test_canary_plan_finishes_at_full_traffic() -> None:
    stages = promotion_plan()
    assert stages[0].traffic_percentage == 5
    assert stages[-1].traffic_percentage == 100


def test_latency_regression_exceeds_performance_budget() -> None:
    budget = PerformanceBudget(
        p95_latency_ms=500,
        maximum_regression_percent=20,
    )
    assert exceeds_performance_budget(300, 450, budget)


def test_deployment_marker_requires_commit_identity() -> None:
    with pytest.raises(ValueError):
        create_marker("v0.3.0", "production", "abc")
