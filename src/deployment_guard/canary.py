from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CanaryStage:
    traffic_percentage: int
    observation_minutes: int


def promotion_plan(
    percentages: tuple[int, ...] = (5, 25, 50, 100),
    observation_minutes: int = 15,
) -> tuple[CanaryStage, ...]:
    if not percentages or percentages[-1] != 100:
        raise ValueError("promotion plan must finish at 100 percent")
    if tuple(sorted(set(percentages))) != percentages:
        raise ValueError("promotion percentages must be unique and increasing")
    if observation_minutes < 1:
        raise ValueError("observation window must be positive")
    return tuple(
        CanaryStage(percentage, observation_minutes)
        for percentage in percentages
    )
