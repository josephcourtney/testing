# L3-T3 — Integration Testing: Design, Writing, Evaluation

## 1. Purpose

Provide evidence whose value depends on real semantics across a process, persistence, protocol, framework, service, platform, or infrastructure boundary.

Integration scope is defined by semantic fidelity, not merely by the number of modules or the presence of a container.

## 2. Applicability

Use when correctness depends on behavior such as:

* SQL dialect, constraints, transactions, or migrations,
* serialization, wire protocols, authentication, or authorization,
* framework or operating-system integration,
* retries, timeouts, partial failure, or resource behavior,
* externally versioned services or deployed components.

Do not use integration scope merely to retest local business logic or full user journeys.

## 3. Evidence identity

Record:

* boundary and claim,
* dependency implementation and version,
* artifact under test,
* operating system, runtime, configuration, and feature flags,
* schema or migration state,
* test data identity,
* provisioning, readiness, reset, and cleanup method,
* network and credential assumptions,
* comparability rules.

## 4. Environment and isolation

Integration resources must be dedicated or safely partitioned, bounded by timeouts, isolated from production, and reset predictably.

Containers may provide reproducibility but do not by themselves establish representativeness. Shared environments require ownership, contention controls, and state identity.

Use readiness probes or explicit synchronization rather than arbitrary sleeps.

## 5. Assertions and faults

Assert boundary-observable behavior, including data, protocol responses, authorization, errors, retries, and recovery where relevant.

Include representative negative or degraded cases when they materially increase confidence. Distinguish product, dependency, environment, and harness failure in diagnostics.

## 6. Writing procedure

1. State the claim and real semantic required.
2. Select a representative dependency and environment.
3. Provision and verify a known state.
4. Exercise the boundary through production code paths.
5. Assert boundary-visible outcomes.
6. Introduce a plausible fault or incompatibility where practical.
7. Verify cleanup and evidence identity.
8. Record limitations and unsupported production differences.

## 7. Evaluation

Good integration evidence:

* would lose value if replaced by a fake,
* uses sufficiently representative real semantics,
* is repeatable and isolated,
* records artifact and environment identity,
* localizes failures to a boundary,
* remains comparable across the decision it supports.

Red flags include undocumented dependency drift, shared mutable state, arbitrary sleeps, excessive internal mocking, uncontrolled external services, and measurements combined across incompatible environments.

## 8. Outputs

* boundary and risk inventory,
* environment and dependency specification,
* covered positive, negative, and degraded behavior,
* comparability and residual-uncertainty record,
* harness and scope recommendations.
