---
aliases:
  - L2-P4
linter-yaml-title-alias: L2-P4
tags: []
title: L2-P4
---

# L2-P4 — Release and Hardening Testing Phase

## 1. Profile role

This is the production-release confidence and governance profile. It requires
fresh, comparable, enforced evidence for the material claims of the release and
for safe operation after deployment.

It is not a universal inventory. Apply `L1.md`, determine which product,
security, privacy, data, accessibility, usability, performance, compatibility,
deployment, observability, and recovery claims are material, and record other
categories as not applicable with rationale.

## 2. Phase intent

**Goal:**
Ensure correctness, reliability, safety, compatibility, and operability for the
intended production use.

**Primary risks addressed:**
Production outages, data corruption or loss, security and privacy failure,
unacceptable performance or capacity, inaccessible or misleading workflows,
packaging and deployment defects, inadequate diagnosis, and inability to
rollback or recover.

---

## 3. Applicability

Applies when:

* preparing a production release,
* enabling a major or external user cohort,
* deploying a material change to a live system,
* operating under contractual, regulatory, safety, or service obligations,
* changing data, infrastructure, dependencies, configuration, rollout, or
  recovery behavior.

A low-impact local tool may satisfy this profile with a much smaller evidence
portfolio than a distributed or regulated service. The required confidence is
set by consequences and exposure, not by ceremony.

---

## 4. Production claim inventory

Evaluate and record the applicability of:

* functional correctness and critical acceptance conditions,
* published interface and artifact compatibility,
* supported platform, runtime, device, or consumer combinations,
* installation, deployment, startup, upgrade, and configuration,
* migration, rollback, backup, restoration, and failover,
* authentication, authorization, confidentiality, integrity, and supply chain,
* privacy purpose, retention, access, deletion, and disclosure,
* data integrity, freshness, lineage, aggregation, and drift,
* latency, throughput, responsiveness, resource use, scaling, and saturation,
* accessibility, usability, comprehension, and error recovery,
* logging, metrics, traces, health, alerting, and diagnostic quality,
* degraded operation, dependency failure, overload, and operator response.

## 5. Default evidence expectations

The following are production-readiness prompts. Evidence is required when the
associated claim is material.

### Baseline correctness and compatibility

* Unit and component evidence for critical responsibilities.
* Integration evidence for critical real boundaries.
* Contract evidence for published interfaces, schemas, data formats, plugins,
  consumers, and version commitments.
* System and acceptance evidence for key user and operator workflows.
* Regression evidence for high-severity and historically recurring failures.
* Exact built-artifact testing outside the source checkout when packaging is a
  release claim.

### Non-functional and human evidence

* Performance and capacity evidence for stated objectives and expected demand.
* Security and privacy evidence tied to a threat and data-flow model.
* Data-quality evidence for managed datasets and transformations.
* Accessibility and usability evidence for critical tasks and intended users.
* Observability evidence that critical success, degradation, and failure can be
  detected and diagnosed.

### Operational evidence

* Deployment and configuration validation.
* Readiness and synthetic transaction checks.
* Migration and rollback exercises where state changes.
* Backup restoration and data-consistency verification where backups are a
  control.
* Fault handling, degraded operation, failover, and recovery evidence where
  availability or continuity matters.
* Runbook and operator evaluation when human action is part of the control.
* Canary, staged-rollout, monitoring, stop, and rollback conditions where used.

### Evidence integrity and enforcement

* L3-T10 suite-health assessment.
* L3-T11 validation of every numeric release gate.
* Fresh artifact, revision, environment, data, dependency, and configuration
  identity.
* Separation of complete, partial, quarantined, and non-comparable results.
* CI or release tooling that enforces the declared gate rather than relying on
  an undocumented manual convention.

### Conditional decision rule

For any applicable claim that lacks sufficient evidence, record:

* the specific failure mode and affected users, operators, data, or obligations,
* why release is proposed despite the gap,
* mitigation such as limited rollout, feature flag, monitoring, containment, or
  rollback,
* owner,
* expiry or revisit trigger,
* planned remediation and evidence.

---

## 6. Explicit non-requirements

Production does not imply exhaustive testing of every theoretically possible
condition. It does not require:

* a test at every structural scope for every responsibility,
* integration tests for dependencies the product does not have,
* broad platform matrices beyond the support commitment,
* chaos experiments without a justified operational hypothesis and controlled
  blast radius,
* arbitrary coverage, mutation, flake, or performance thresholds,
* penetration testing where the threat model and consequences do not justify it.

Not-applicable decisions must be explicit for material readiness categories.

---

## 7. Procedure

1. Review release scope, audience, exposure, obligations, and change history.
2. Enumerate production claims and failure modes.
3. Map each material claim to applicable L3 procedures and evidence.
4. Verify critical behavior, contracts, boundaries, artifacts, and environment
   combinations.
5. Evaluate security, privacy, data, accessibility, usability, performance, and
   observability as applicable.
6. Exercise deployment, migration, rollback, restoration, degradation, and
   recovery controls where material.
7. Assess suite health and validate quantitative gates.
8. Confirm gate enforcement, evidence freshness, comparability, and artifact
   identity.
9. Review open defects, waivers, accepted risks, operational mitigations, stop
   conditions, and owners.
10. Record the release decision and retained evidence artifact.

## 8. Compliance criteria

The profile is satisfied when:

1. All release-critical claims have credible evidence under representative
   conditions.
2. Published contracts and supported combinations are verified.
3. Deployment and operational controls are demonstrated where applicable.
4. Operators and users receive sufficient signals and recovery paths.
5. Evidence is fresh, complete, comparable, and tied to the release artifact.
6. Gates are technically justified and actually enforced.
7. Identified risks are mitigated, blocked, or explicitly accepted by an
   authorized owner.

## 9. Decision outcomes

* **Pass** — release-critical claims are supported and no blocking gap remains.
* **Conditional pass** — release may proceed only with explicit rollout limits,
  mitigations, owners, and revisit triggers.
* **Fail** — a claim is contradicted, required evidence is invalid or missing,
  or residual risk is unacceptable.
* **Risk acceptance** — an authorized owner accepts a bounded residual risk.

## 10. Outputs

* release claim and evidence matrix,
* applicable/not-applicable readiness table,
* artifact, environment, compatibility, and dependency identity,
* security, privacy, performance, data, accessibility, and usability findings,
* deployment, monitoring, rollback, restoration, and recovery evidence,
* suite-health and metric-validation results,
* blockers, waivers, mitigations, owners, and expiry dates,
* release decision and rationale.

## 11. Forward rules

* Release evidence that can decay must have a recurrence or revalidation trigger.
* Operational failures, near misses, user findings, and incidents feed into
  L2-P5 and the regression portfolio.
* Supported contracts and compatibility cells remain explicit obligations until
  deprecated or removed.
* Waivers expire; they do not become undocumented permanent policy.
