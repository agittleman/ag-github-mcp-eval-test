# Rollback runbook

Use this runbook when deployment health checks fail or the release exceeds its
error budget.

1. Pause promotion and record the active release.
2. Restore the previous application image.
3. Confirm database compatibility before shifting traffic.
4. Run smoke checks against health, login, and deployment endpoints.
5. Compare error rate and p95 latency with the pre-deployment baseline.
6. Open a follow-up issue with the failed signal and rollback timeline.

Do not retry deployment until the triggering regression is understood.
