---
aliases:
  - L2-P2
linter-yaml-title-alias: L2-P2
tags: []
title: L2-P2
---

# L2-P2 — Feature Development Confidence Profile

## 1. Intent

Provide rapid, localizing evidence that changed responsibilities behave as intended while interfaces and design may still evolve.

## 2. Applicability

Use for new features, refactors, behavior changes, and defect corrections during active development.

## 3. Default evidence expectations

For each changed responsibility:

* identify the intended behavior, invariants, and acceptance conditions,
* add executable evidence at a scope that preserves the relevant semantics,
* add a regression purpose when correcting a distinct failure mode,
* exercise a real boundary early when its semantics are a material source of uncertainty,
* define contract obligations when another consumer already relies on the interface,
* include security, data, performance, usability, or accessibility evidence when those risks affect the design.

Unit and component evidence are common because they usually provide fast localization. They are not mandatory categories when another form of evidence is more direct and credible.

## 4. Development workflow

Test-driven, acceptance-first, test-after, characterization, and exploratory workflows are all permitted. Select the workflow according to how well the behavior is understood and the cost of obtaining an oracle.

Mocking is not required. Retain inexpensive real collaborators within the chosen boundary when they improve confidence. Use doubles where control, speed, or deliberate fault injection is valuable, and add alignment evidence when fidelity matters.

## 5. Procedure

1. Identify changed responsibilities and affected consumers.
2. Update the L1 risk and evidence map.
3. Select structural scope, purpose, technique, and resources independently.
4. Add or update evidence that fails when the intended behavior is absent.
5. Run the fastest relevant feedback loop during implementation.
6. Run the complete pre-merge evidence set before declaring the change complete.
7. Record any material risk intentionally deferred to stabilization.

## 6. Exit criteria

Return pass, conditional pass, or fail to L1.

A pass requires:

* executable evidence for material changed behavior,
* no known high-impact gap concealed by a double or omitted boundary,
* acceptance conditions that are either demonstrated or explicitly deferred,
* evidence that remains readable and sufficiently localizing for continued development.

## 7. Common L3 procedures

* **L3-T1:** Unit Testing
* **L3-T2:** Component Testing
* **L3-T3:** Integration Testing
* **L3-T5:** Regression Testing
* **L3-T6:** Generative Testing
* **L3-T7:** Contract Testing
* **L3-T12:** Acceptance Testing
* **L3-T13:** Exploratory Testing

Use other L3 procedures whenever the risk map calls for them.
