from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class DeploymentMarker:
    release: str
    environment: str
    commit_sha: str
    deployed_at: datetime


def create_marker(
    release: str,
    environment: str,
    commit_sha: str,
    *,
    deployed_at: datetime | None = None,
) -> DeploymentMarker:
    if not release or not environment:
        raise ValueError("release and environment are required")
    if len(commit_sha) < 7:
        raise ValueError("commit SHA must contain at least seven characters")
    return DeploymentMarker(
        release=release,
        environment=environment,
        commit_sha=commit_sha,
        deployed_at=deployed_at or datetime.now(timezone.utc),
    )
