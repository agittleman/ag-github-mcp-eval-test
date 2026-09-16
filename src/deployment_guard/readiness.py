from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RollbackReadiness:
    previous_image_available: bool
    policy_snapshot_available: bool
    smoke_checks_configured: bool

    @property
    def ready(self) -> bool:
        return all(
            (
                self.previous_image_available,
                self.policy_snapshot_available,
                self.smoke_checks_configured,
            )
        )

    def missing_requirements(self) -> tuple[str, ...]:
        requirements = {
            "previous deployment image": self.previous_image_available,
            "policy snapshot": self.policy_snapshot_available,
            "smoke checks": self.smoke_checks_configured,
        }
        return tuple(name for name, present in requirements.items() if not present)
