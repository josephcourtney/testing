---
aliases:
  - L2-P5
linter-yaml-title-alias: L2-P5
tags: []
title: L2-P5
---

# L2-P5 — Maintenance and Change Testing Phase

## 1. Profile role

This is the lifecycle confidence profile for safely changing or continuing to
operate a live system. It emphasizes change-impact analysis, incident learning,
contract revalidation, evidence decay, suite health, and operational feedback.

It does not require a fixed regression inventory for every change. Apply
`L1.md`, identify the claims and boundaries affected by the change or operating
observation, and select evidence accordingly.

## 2. Phase intent

**Goal:**
Safely evolve a live system while preventing regressions and preserving the
ability to deploy, diagnose, operate, and recover it.

**Primary risks addressed:**
Silent breakage, reintroduction of learned defects, contract drift, migration or
rollback failure, dependency incompatibility, stale operational evidence,
cumulative test debt, and erosion of suite trustworthiness.

---

## 3. Applicability

Applies when:

* fixing bugs in production code,
* responding to incidents or near misses,
* making incremental improvements or refactors,
* upgrading dependencies, runtimes, platforms, or infrastructure,
* changing configuration, data, migrations, deployment, or monitoring,
* reassessing continued operation after evidence, scale, users, threats, or
  environments change.

---

## 4. Change-impact assessment

Record:

* the changed claim, behavior, or operating assumption,
* affected responsibilities and user/operator journeys,
* affected interfaces, consumers, schemas, data, artifacts, and environments,
* the trigger, symptom, and root cause of any defect or incident,
* relevant production observations, support reports, telemetry, or near misses,
* evidence that may have become stale or non-comparable,
* rollout, monitoring, rollback, and recovery implications.

## 5. Default evidence expectations

These are prompts to evaluate for each maintenance decision, not a universal
inventory.

### Changed behavior and learned failures

* Regression evidence for non-trivial bug fixes and material escaped defects.
* Unit or component evidence for changed local logic and subsystem behavior.
* Characterization evidence before modifying poorly understood legacy behavior.
* Acceptance evidence when a stakeholder-visible condition changes.
* Removal or revision of regressions whose underlying obligation no longer
  exists.

### Boundaries and compatibility

* Integration evidence when real persistence, protocol, service, framework,
  process, or platform semantics change.
* Contract and compatibility revalidation when interfaces, consumers, versions,
  schemas, formats, or artifacts change.
* Migration and rollback evidence for data or configuration transitions.
* Exact installed-artifact evidence when packaging, dependencies, entry points,
  or included files change.

### Operational and non-functional change

* Security and privacy reassessment for new threats, dependencies, permissions,
  or data flows.
* Performance and capacity comparison for changes likely to affect resource use
  or demand.
* Data-quality and drift evidence for changed sources, transformations, models,
  or populations.
* Accessibility and usability reevaluation for changed user workflows.
* Observability, alerting, deployment, rollback, restoration, resilience, and
  recovery evidence when operating controls change.

### Portfolio health

* L3-T10 review before and after changes that materially affect runtime,
  flakiness, fixtures, snapshots, test infrastructure, or ownership.
* L3-T11 validation when metrics, baselines, environments, cohorts, or threshold
  decisions change.
* Removal, repair, or quarantine of stale and unreliable evidence with explicit
  ownership and time bounds.

### Conditional decision rule

If evidence is omitted despite a material affected claim or boundary, record:

* the impacted claim, interface, user, operator, or data,
* why omission is acceptable,
* compensating monitoring, canary, feature flag, containment, or rollback,
* owner,
* time-bounded remediation or revisit trigger.

---

## 6. Explicit default non-requirements

Maintenance does not automatically require:

* full revalidation of demonstrably unchanged behavior,
* broad exploratory testing unrelated to the change,
* a new regression test for every trivial edit,
* retention of obsolete tests solely because they already exist,
* every structural scope for each change,
* universal numeric thresholds.

Change-impact analysis must justify what is not rerun or revalidated.

---

## 7. Procedure

1. Identify the change, operating observation, incident, or continued-operation
   decision.
2. Map affected claims, responsibilities, boundaries, consumers, environments,
   data, and operational controls.
3. Reproduce and minimize defects or incidents where applicable.
4. Select evidence that preserves the original failure mechanism, not merely its
   symptom.
5. Revalidate contracts, integrations, migrations, artifacts, and supported
   combinations affected by the change.
6. Evaluate non-functional and operational effects where material.
7. Run the required trusted regression and release selections without allowing
   quarantined or partial results to masquerade as complete evidence.
8. Compare suite health, performance, compatibility, and other metrics only
   under valid comparability rules.
9. Retire or rewrite obsolete, duplicated, brittle, or misleading tests.
10. Record outcome, residual risk, mitigation, owner, and revisit trigger.

## 8. Compliance criteria

The profile is satisfied when:

1. The change-impact analysis covers affected claims and boundaries.
2. Evidence would detect the material failure modes introduced or learned.
3. Relevant contracts, integrations, migrations, artifacts, and operational
   controls are revalidated.
4. Existing tests remain stable, meaningful, and trustworthy.
5. No new unacknowledged flakiness, excessive delay, or evidence-integrity defect
   is introduced.
6. Stale or obsolete evidence is repaired, bounded, or removed.
7. Continued-operation risk is explicit.

## 9. Assessment outputs

* change-impact and affected-boundary map,
* defect or incident reproduction and root-cause context,
* added, updated, removed, or reclassified evidence,
* contract, compatibility, migration, and artifact revalidation,
* operational and non-functional findings,
* before/after suite-health observations,
* waivers, mitigations, owners, and recurrence triggers,
* pass, conditional pass, fail, exploratory finding, or risk-acceptance result.

## 10. Forward rules

* Regression tests remain assets only while they protect a real obligation or
  failure class.
* Incidents and near misses update claims, runbooks, monitoring, architecture,
  and evidence—not only a single test.
* Dependency and platform support commitments receive recurring compatibility
  evidence.
* Operational evidence is repeated according to how quickly it can decay.
* Test debt and brittleness are addressed incrementally rather than normalized
  as permanent maintenance cost.
