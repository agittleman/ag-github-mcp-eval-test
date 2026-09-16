from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailedCheck:
    name: str
    summary: str
    log_url: str


def deployment_blocker(checks: tuple[FailedCheck, ...]) -> str | None:
    if not checks:
        return None
    details = "; ".join(f"{check.name}: {check.summary}" for check in checks)
    return f"deployment blocked by failing CI checks: {details}"
