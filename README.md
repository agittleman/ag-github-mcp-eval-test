# Deployment Guard

Deployment Guard is a small Python service used to evaluate GitHub search,
summarization, and repository-understanding workflows. It models a deployment
control plane with explicit safety checks, rollback planning, and release
health scoring.

The project is intentionally realistic but contains no production data.

## Capabilities

- evaluate deployment readiness from CI, error-rate, and latency signals;
- produce deterministic rollback plans;
- rank release health regressions;
- document deployment ownership and operational decisions;
- exercise pull-request, issue, branch, commit, review, and release queries.

## Repository layout

- `src/deployment_guard/`: policy, rollback, and health-scoring logic;
- `tests/`: unit tests for safety-critical behavior;
- `config/`: example deployment policy;
- `docs/`: architecture decisions and operational runbooks;
- `.github/`: CI and code-ownership configuration.

## Development

```bash
python -m pip install -e '.[test]'
pytest
```

## Safety model

A deployment is allowed only when CI is healthy, error rate is within budget,
and p95 latency is below the configured threshold. Rollback plans are generated
before a release is promoted.
