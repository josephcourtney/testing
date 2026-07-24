# L3-T15 — Operational, Resilience, and Recovery Testing

## 1. Purpose

Evaluate whether a system can be deployed, observed, operated, degraded, recovered, rolled back, and restored under the conditions that matter to its operators and users.

This procedure covers operational readiness, fault injection, resilience, disaster recovery, rollback, synthetic monitoring, and production verification.

## 2. Applicability

Use when:

* a service or deployed system has availability or recovery obligations,
* releases involve migrations, configuration, infrastructure, or distributed dependencies,
* operators must diagnose and mitigate failure,
* partial failure, overload, retry, failover, rollback, or restoration is material,
* production monitoring or staged rollout supports release confidence.

## 3. Operational claims

Identify relevant claims such as:

* deployment and startup succeed from a clean environment,
* configuration errors fail safely and diagnostically,
* health and readiness signals reflect actual service capability,
* alerts detect user-impacting conditions with acceptable delay and noise,
* degraded dependencies produce defined behavior,
* retries, queues, and circuit breakers do not amplify failure,
* rollback is possible within stated limits,
* backups restore usable and consistent state,
* failover meets recovery time and recovery point objectives,
* operators can diagnose and execute the runbook,
* canary or staged rollout detects regressions before broad impact.

## 4. Evidence types

* deployment and installation tests,
* migration and rollback exercises,
* backup restoration tests,
* readiness and synthetic transaction checks,
* targeted fault injection,
* controlled chaos experiments,
* load, saturation, and resource-exhaustion tests,
* failover and disaster-recovery exercises,
* game days and runbook rehearsals,
* canary analysis and post-deployment verification,
* incident and near-miss review.

## 5. Design rules

* Start from an explicit operational claim and failure mode.
* Use the lowest-risk environment that preserves the required semantics.
* Define blast radius, stop conditions, cleanup, and responsible operators before fault injection.
* Verify recovery, not only detection of failure.
* Assert observable service and data outcomes, not merely that a fault was injected.
* Include operators and runbooks when human response is part of the control.
* Treat monitoring and alerts as contracts with measurable detection and diagnostic requirements.
* Do not perform uncontrolled production chaos to compensate for missing lower-environment evidence.

## 6. Procedure

1. Define the operating envelope, critical dependencies, state, and recovery objectives.
2. Inventory deployment, migration, monitoring, rollback, backup, and incident-response controls.
3. Select representative failure and recovery scenarios from the risk map.
4. Establish environment, blast radius, stop conditions, and data protection.
5. Exercise detection, degradation, operator response, rollback or recovery, and return to a known-good state.
6. Verify data consistency and user-visible behavior after recovery.
7. Capture timelines, signals, missing diagnostics, manual errors, and unmet assumptions.
8. Update tests, alerts, runbooks, architecture, and release controls.
9. Define cadence for repeating evidence that can decay.

## 7. Evaluation

Good operational evidence:

* demonstrates a specific operating or recovery claim,
* uses realistic dependencies and state where semantics matter,
* verifies both failure handling and recovery,
* records artifact, environment, workload, and timing,
* exposes whether operators can act on the available signals,
* has controlled risk and repeatable cleanup.

Red flags:

* checking only process liveness rather than user capability,
* chaos without a hypothesis or stop condition,
* backup success without restoration testing,
* rollback documentation that has never been exercised,
* alerts that fire but do not identify an actionable condition,
* successful recovery that leaves inconsistent or silently lost data,
* production verification whose results are not connected to release decisions.

## 8. Outputs

* operational claim and scenario inventory,
* deployment, monitoring, rollback, and recovery evidence,
* recovery time and data-consistency observations,
* runbook and diagnostic gaps,
* release stop and rollback conditions,
* recurrence schedule and ownership.
