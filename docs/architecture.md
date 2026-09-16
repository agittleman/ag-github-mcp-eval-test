# Deployment Guard architecture

Deployment Guard evaluates release signals before promotion. The policy engine
is intentionally deterministic so an operator can explain every blocker.

## Deployment path

1. CI publishes a candidate release.
2. The service evaluates error rate and p95 latency against policy.
3. A canary receives five percent of traffic.
4. Healthy candidates advance through staged promotion.
5. Unsafe candidates invoke the precomputed rollback plan.

## Decision: deterministic rollback

We considered an adaptive rollback controller and a deterministic runbook.
Adaptive control could react faster, but would make incident behavior harder
to audit. The initial implementation uses deterministic rollback steps and
records the measurements that caused the decision.

The next iteration should compare automatic rollback against an operator
confirmation gate for database migrations.
