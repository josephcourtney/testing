---
aliases:
  - L2-P5
linter-yaml-title-alias: L2-P5
tags: []
title: L2-P5
---

# L2-P5 — Maintenance and Live-System Change Confidence Profile

## 1. Intent

Safely evolve a live system, preserve learned behavior, and incorporate evidence from incidents, users, operators, dependencies, and production measurements.

## 2. Applicability

Use for defect corrections, dependency and platform upgrades, migrations, incremental features, configuration or deployment changes, scaling changes, and operational remediations.

## 3. Default evidence expectations

For each change:

* reproduce and protect distinct escaped failure modes where practical,
* identify affected responsibilities, consumers, boundaries, environments, and operational procedures,
* rerun the existing evidence needed to support unchanged release claims,
* add new evidence only where the change or learned failure exposes a gap,
* reassess performance, security, compatibility, accessibility, data, or recovery evidence when the corresponding assumptions change,
* use production history to revise risk priorities and metric baselines.

“Do not fully revalidate unchanged functionality” means that new tests need not be invented for unrelated behavior. It does not mean that the existing regression or release gate may be skipped when it remains necessary to support the release claim.

## 4. Procedure

1. Identify the trigger, symptom, impact, and known root cause.
2. Update the L1 risk and evidence map with newly learned information.
3. Select the lowest scope that reproduces the symptom without discarding the responsible semantics.
4. Add or strengthen contract, integration, system, operational, or monitoring evidence when the failure crossed those boundaries.
5. Run affected fast checks and the complete release evidence required for the resulting deployment decision.
6. Compare suite health and relevant measurements before and after the change using L3-T10 and L3-T11.
7. Update runbooks, alerts, rollback conditions, or recovery exercises when operational learning requires it.

## 5. Exit criteria

Return pass, conditional pass, or fail to L1.

A pass requires evidence that the change addresses its intended condition, protects material learned behavior, preserves the release claims affected by the change, and introduces no unacknowledged degradation in test or operational evidence.

## 6. Common L3 procedures

* **L3-T5:** Regression Testing
* **L3-T7:** Contract and Compatibility Testing
* **L3-T10:** Suite Health
* **L3-T11:** Metric Design
* **L3-T13:** Exploratory Testing
* **L3-T15:** Operational and Resilience Testing

Use unit, component, integration, system, security, performance, usability, or data procedures according to the affected risk rather than by default.
