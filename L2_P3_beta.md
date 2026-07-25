---
aliases:
  - L2-P3
linter-yaml-title-alias: L2-P3
tags: []
title: L2-P3
---

# L2-P3 — Stabilization and Pre-Release Testing Phase

## 1. Profile role

This is a lifecycle confidence profile for beta, stabilization, and pre-release
work. It increases confidence, breadth, environmental fidelity, enforcement,
and recordkeeping relative to ordinary feature development.

It is not a universal inventory of test classes. Apply `L1.md` first, select
evidence from the product's actual claims and risks, and mark a category not
applicable when no corresponding boundary or obligation exists.

## 2. Phase intent

**Goal:**
Stabilize behavior, validate critical boundaries and user journeys, and reduce
release uncertainty.

**Primary risks addressed:**
Integration failures, regressions, contract drift, packaging defects,
incomplete acceptance conditions, unrealistic test environments, inaccessible
or confusing workflows, and a suite that cannot support release decisions.

**Risks sometimes deferred only when not material to the intended release:**
Long-duration capacity optimization, rare disaster scenarios, or broad platform
matrices beyond the declared support commitment.

---

## 3. Applicability

Applies when:

* the feature set is largely complete,
* preparing for beta, external evaluation, or release,
* APIs and data models are becoming commitments,
* built artifacts and deployment forms must be validated,
* critical user or operator workflows need representative evaluation.

This profile assumes important interfaces are stable enough that compatibility,
development, and deprecation decisions can be made explicitly.

---

## 4. Assessment inputs

Record:

* intended release or beta audience,
* critical responsibilities and user/operator journeys,
* public interfaces, schemas, artifacts, and supported versions,
* real persistence, protocol, process, platform, and service boundaries,
* configuration and environment matrix,
* known incidents, regressions, and unresolved ambiguity,
* suite-health status and release feedback budget,
* residual risks and available rollback or containment.

## 5. Default evidence expectations

These are strong stabilization prompts. Each must be evaluated, but only
applicable items require evidence.

### Baseline behavioral evidence

* Unit and component evidence for critical logic and subsystem behavior.
* Regression evidence for learned failure modes and escaped defects.
* Acceptance evidence for critical user, stakeholder, or operator conditions.

### Boundary and compatibility evidence

* Integration evidence for critical real external semantics.
* Contract and compatibility evidence for stable APIs, schemas, data formats,
  consumers, platforms, and artifact forms.
* Migration and rollback evidence when data or configuration evolves.
* Installed-artifact testing when packaging, entry points, included data, or
  isolated installation are claims.

### Assembled-product and human evidence

* System evidence for critical assembled workflows.
* A small smoke selection suitable for frequent gating where useful.
* Exploratory evaluation of changed, ambiguous, or high-risk areas.
* Usability and accessibility evidence when people interact with the system and
  those outcomes are material.

### Non-functional and operational evidence

* Performance, security, privacy, data-quality, observability, resilience, and
  recovery evidence whenever the corresponding failure is material.
* Suite-health assessment through L3-T10 before relying on the portfolio as a
  release gate.
* Metric design and validation through L3-T11 before quantitative gating.

### Conditional decision rule

For an applicable category that lacks sufficient evidence, record:

* affected claim and failure mode,
* explicit scope of the gap or waiver,
* current mitigation, rollout control, monitoring, or rollback plan,
* owner and expiry or revisit date,
* planned evidence or remediation.

---

## 6. Explicit default non-requirements

This profile does not require evidence for nonexistent boundaries or unsupported
combinations. It does not automatically require:

* every test scope for every feature,
* exhaustive system scenario matrices,
* production-scale load when scale is not a release claim,
* chaos experiments without an operational hypothesis,
* full penetration testing where the threat model does not warrant it,
* universal coverage, mutation, flake, or runtime percentages.

A material risk overrides these defaults.

---

## 7. Procedure

1. Enumerate critical claims, user journeys, operator workflows, and boundaries.
2. Identify supported interfaces, versions, artifacts, platforms, and data
   transitions.
3. Map each material failure mode to credible evidence.
4. Verify real boundary semantics for critical dependencies.
5. Verify provider/consumer compatibility and artifact identity.
6. Exercise representative assembled-product workflows and a curated smoke set.
7. Perform exploratory, usability, accessibility, security, and non-functional
   evaluation where applicable.
8. Assess suite health, flakiness, runtime, diagnostics, and evidence integrity.
9. Validate every metric used as a release gate.
10. Record omitted evidence, residual uncertainty, waivers, mitigations, and
    owners.
11. Produce the beta or pre-release decision.

## 8. Compliance criteria

The profile is satisfied when:

1. Critical behavior and journeys have credible evidence at appropriate scopes.
2. Real external semantics and stable interfaces are verified where applicable.
3. The built artifact and supported environment combinations are represented.
4. Applicable usability, accessibility, security, privacy, performance, data,
   observability, and recovery claims are addressed.
5. The suite is reliable, repeatable, sufficiently localizing, and usable as a
   gate.
6. Missing or weak evidence is explicit rather than hidden by a named test
   inventory.
7. Residual risk is accepted only by an authorized owner with conditions.

## 9. Assessment outputs

* release claim and critical-journey map,
* boundary and compatibility matrix,
* applicable/not-applicable evidence table with rationale,
* installed-artifact and environment identities,
* exploratory, usability, accessibility, and non-functional findings,
* suite-health and metric-validation results,
* waivers, blockers, mitigations, and owners,
* pass, conditional pass, fail, exploratory finding, or risk-acceptance result.

## 10. Forward rules

* Stable contracts become explicit compatibility obligations.
* Release regressions and exploratory findings become durable evidence where
  useful.
* Provisional tests, snapshots, and fixtures should be pruned or hardened before
  they become permanent maintenance cost.
* Evidence that decays with dependencies, platforms, users, scale, or operating
  conditions must receive a recurrence cadence.
* Unresolved release gaps flow into L2-P4 or block promotion.
