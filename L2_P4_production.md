# L2-P4 — Production Confidence Profile

## 1. Intent

Justify production release, deployment, and operation with evidence for correctness, compatibility, security, privacy, performance, data integrity, accessibility, operability, and recovery wherever those claims are material.

## 2. Required assessment

Apply L1 to the actual release and identify:

* release artifacts and supported environments,
* critical user and operator journeys,
* dependencies, data, migrations, and configuration,
* threat and privacy obligations,
* capacity and performance objectives,
* monitoring, alerting, rollback, backup, restoration, and incident response,
* residual risks and rollout controls.

## 3. Default confidence posture

Production evidence should normally include:

* complete trusted functional evidence for release-critical claims,
* installed-artifact and packaging verification,
* contract and compatibility matrices for supported cells,
* non-functional evidence designed through L3-T8 and L3-T11,
* acceptance, usability, and accessibility evidence where interaction matters,
* operational, resilience, rollback, and recovery evidence through L3-T15,
* suite-health assessment through L3-T10,
* fresh and comparable evidence tied to the release artifact.

Not-applicable categories require rationale. Material omissions require a waiver or risk acceptance.

## 4. Governance defaults

* Gates are explicit, reproducible, and actionable.
* Required evidence has owners and documented cadence.
* Waivers are scoped, mitigated, approved, and expiring.
* Deployment stop, rollback, and recovery conditions are defined.
* Production verification does not overwrite pre-release evidence.
* Incidents and near misses feed back into L1 and L2-P5.

## 5. Outcome

A production pass requires sufficient evidence for all release-blocking claims and no unaccepted material gap. A conditional pass requires an authorized bounded rollout, compensating controls, owner, and revisit trigger.
