from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    deployment_id: str
    action: str
    reason: str
    occurred_at: datetime


def deployment_event(
    deployment_id: str,
    action: str,
    reason: str,
    *,
    occurred_at: datetime | None = None,
) -> AuditEvent:
    if action not in {"allow", "block", "rollback"}:
        raise ValueError(f"unsupported deployment action: {action}")
    return AuditEvent(
        deployment_id=deployment_id,
        action=action,
        reason=reason,
        occurred_at=occurred_at or datetime.now(timezone.utc),
    )
