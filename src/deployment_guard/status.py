from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .health import ReleaseHealth, regression_score


@dataclass(frozen=True)
class DeploymentStatus:
    environment: str
    current: ReleaseHealth
    baseline: ReleaseHealth
    rollback_ready: bool

    def as_response(self) -> dict[str, Any]:
        return {
            "environment": self.environment,
            "current": asdict(self.current),
            "baseline": asdict(self.baseline),
            "regression_score": regression_score(self.current, self.baseline),
            "rollback_ready": self.rollback_ready,
        }
