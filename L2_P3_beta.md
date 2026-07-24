---
aliases:
  - L2-P3
linter-yaml-title-alias: L2-P3
tags: []
title: L2-P3
---

# L2-P3 — Stabilization and Pre-Release Confidence Profile

## 1. Intent

Increase confidence that the assembled behavior, important boundaries, published obligations, supported environments, and critical user journeys are stable enough for beta or release-candidate use.

## 2. Applicability

Use when interfaces are becoming commitments, the feature set is largely complete, or a broader audience will depend on the system.

## 3. Default evidence expectations

The evidence map should now address:

* critical responsibilities and invariants,
* real semantics at every material external boundary,
* published and consumed contracts, including compatibility rules,
* critical user and operator journeys,
* packaging, installation, configuration, and deployment behavior,
* representative supported environments,
* known regressions and high-severity failure classes,
* accessibility, usability, security, data quality, performance, and resilience where material,
* suite health and evidence freshness.

A category is required because a risk or claim needs it, not merely because the project is called beta. A local library with no external system boundary need not invent integration tests; a beta service with authentication and persistence normally does.

## 4. Procedure

1. Enumerate critical user, operator, and system flows.
2. Inventory external boundaries, consumers, deployment artifacts, and supported environments.
3. Confirm that selected evidence exercises real semantics where doubles are insufficient.
4. Verify compatibility obligations and negative/error behavior.
5. Perform targeted exploratory and usability work for behavior not adequately covered by predefined automation.
6. Assess suite health with **L3-T10** and metric validity with **L3-T11**.
7. Record residual uncertainty and any time-bounded mitigation.

## 5. Exit criteria

Return pass, conditional pass, or fail to L1.

A pass requires evidence sufficient for the stated beta or pre-release audience, reliable execution of the selected gates, and no unacknowledged material boundary, compatibility, user-journey, or operational gap.

## 6. Common L3 procedures

* **L3-T2:** Component Testing
* **L3-T3:** Integration Testing
* **L3-T4:** System and Smoke Testing
* **L3-T7:** Contract and Compatibility Testing
* **L3-T10:** Suite Health
* **L3-T11:** Metric Design
* **L3-T12:** Acceptance Testing
* **L3-T13:** Exploratory Testing
* **L3-T14:** Usability and Accessibility
* **L3-T15:** Operational and Resilience Testing
