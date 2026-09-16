from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RollbackPlan:
    release: str
    previous_release: str
    steps: tuple[str, ...]


def build_rollback_plan(release: str, previous_release: str) -> RollbackPlan:
    if not release or not previous_release:
        raise ValueError("release names must be non-empty")
    if release == previous_release:
        raise ValueError("rollback target must differ from the active release")

    return RollbackPlan(
        release=release,
        previous_release=previous_release,
        steps=(
            "pause deployment promotion",
            f"restore application image {previous_release}",
            "verify database compatibility",
            "run smoke checks",
            "confirm error rate and latency recovery",
        ),
    )
