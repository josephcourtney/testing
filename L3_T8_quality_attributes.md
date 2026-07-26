# L3-T8 — Performance, Security, Privacy, Data, and Observability Evidence

## 1. Purpose

Evaluate material performance, security, privacy, data-quality, and
observability claims.

The phrase **quality-attribute evidence** is used here only as a convenient
umbrella. These categories remain distinct purposes and evidence forms selected
from the risk profile; they are not a structural scope and are not deferred
automatically to a late lifecycle profile.

## 2. Common design rules

For every quality-attribute claim:

* identify the failure mode and affected user, operator, data, or obligation,
* define an observable property or measurement,
* select a harness that preserves the relevant environment and workload semantics,
* separate diagnostic measurement from a release gate,
* apply **L3-T11** before adopting any numeric threshold,
* record environmental noise, exclusions, and residual uncertainty,
* choose cadence according to cost and the time at which evidence can still affect the decision.

## 3. Performance

Define the operation, workload, data shape, concurrency, resource limits, environment, warmup, sample method, statistic, and practically meaningful regression.

Evaluate:

* latency distributions rather than isolated timings where appropriate,
* throughput, memory, CPU, I/O, or capacity relevant to the claim,
* scaling behavior and saturation points,
* comparability of artifacts and environments,
* whether the harness detects a deliberate material slowdown.

Do not use a generic percentage band as a portable default.

## 4. Security and privacy

Start from a threat and data-flow model. Evidence may include:

* static analysis and dependency or secret scanning,
* authorization and authentication checks,
* injection, deserialization, path, command, and protocol abuse cases,
* fuzzing and malformed-input handling,
* least-privilege and failure-closed behavior,
* privacy purpose, retention, deletion, access, and disclosure obligations,
* supply-chain and artifact verification,
* expert review or penetration testing where the threat warrants it.

A scanner result is evidence about its ruleset, not proof of security.

## 5. Data quality

Define invariants and service expectations for relevant datasets and transformations:

* schema and type,
* uniqueness and referential integrity,
* null and range constraints,
* freshness and completeness,
* aggregation and backfill correctness,
* lineage and version compatibility,
* distribution or model-input drift.

Use L3-T11 for statistical thresholds. Distinguish conditions that should block processing from those that should alert or trigger investigation.

## 6. Observability

Treat operator-critical signals as contracts. Evaluate whether critical success, degradation, and failure paths provide:

* stable event or metric identity,
* relevant entity and correlation identifiers,
* severity and error classification,
* actionable context without sensitive-data leakage,
* enough information to distinguish product, dependency, environment, and configuration failures.

Prefer structured fields and semantic assertions over complete log-message equality.

## 7. Procedure

1. Select material quality-attribute claims from the L1 risk map.
2. Define the environment, workload, threat, dataset, or operator scenario.
3. Identify an observable contract and evidence source.
4. Build or select a repeatable harness.
5. Validate the measurement or detector with a known fault where practical.
6. Apply L3-T11 to gates and thresholds.
7. Run at the cadence appropriate to cost and risk.
8. Record results, limitations, and required action.

## 8. Evaluation

Good quality-attribute evidence:

* corresponds to a material claim,
* exercises realistic semantics,
* controls or reports important variance,
* has an actionable oracle,
* remains comparable across the decisions for which it is used.

Red flags:

* arbitrary thresholds,
* uncontrolled microbenchmarks,
* security tests unrelated to a threat model,
* drift alarms with no operational interpretation,
* logs tested only for wording,
* measurements used as gates before baseline stability is established.

## 9. Outputs

* claim and failure-mode inventory,
* harness and environment specification,
* validated metrics or invariants,
* cadence and gating decision,
* uncertainty and comparability limits,
* remediation and ownership.
