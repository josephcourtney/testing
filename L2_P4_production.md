---
aliases:
  - L2-P4
linter-yaml-title-alias: L2-P4
tags: []
title: L2-P4
---

# L2-P4 — Production Release and Hardening Confidence Profile

## 1. Intent

Determine whether evidence supports production use under the stated audience, workload, trust, compatibility, availability, recovery, and compliance conditions.

## 2. Applicability

Use for production releases, major rollouts, materially changed operational conditions, and systems subject to SLA, security, privacy, safety, or regulatory obligations.

## 3. Required release evidence

The release assessment must address every material claim in the L1 risk and evidence map. Relevant evidence commonly includes:

* correctness of critical responsibilities and invariants,
* real integration and protocol semantics,
* consumer and provider compatibility,
* critical acceptance and system journeys,
* built-artifact, installation, configuration, migration, and deployment behavior,
* supported platform and dependency combinations,
* performance and capacity under justified workloads,
* threat-model-driven security and privacy checks,
* data integrity and quality checks,
* accessibility obligations,
* observability and diagnostic sufficiency,
* rollback, restoration, failover, and degraded-mode behavior,
* production monitoring, canary, or staged-rollout controls.

No item is automatically required when it has no corresponding material claim or risk. Conversely, a material risk cannot be waived merely because its test type is described as optional elsewhere.

## 4. Procedure

1. Freeze the release scope, artifact identity, environment matrix, and intended operating conditions.
2. Confirm that evidence is fresh, complete, and comparable to those conditions.
3. Verify critical contracts, integrations, journeys, and operational controls.
4. Apply **L3-T11** to every metric used as a release gate.
5. Apply **L3-T15** to deployment, monitoring, rollback, recovery, and resilience claims.
6. Review unresolved incidents, regressions, quarantines, and waivers.
7. Record residual uncertainty, rollout limits, monitoring, and stop/rollback conditions.
8. Return the release decision.

## 5. Exit criteria

Return pass, conditional pass, or fail to L1.

A production pass requires evidence sufficient for the declared operating envelope and explicit treatment of residual risk. Missing material evidence is a fail unless a responsible authority accepts a bounded, time-limited risk with concrete mitigation and detection.

## 6. Common L3 procedures

All L3 procedures may be relevant. Frequently used procedures include:

* **L3-T3:** Integration Testing
* **L3-T4:** System and Smoke Testing
* **L3-T7:** Contract and Compatibility Testing
* **L3-T8:** Non-Functional Testing
* **L3-T10:** Suite Health
* **L3-T11:** Metric Design
* **L3-T12:** Acceptance Testing
* **L3-T14:** Usability and Accessibility
* **L3-T15:** Operational and Resilience Testing
