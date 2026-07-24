---
aliases:
  - L2-P1
linter-yaml-title-alias: L2-P1
tags: []
title: L2-P1
---

# L2-P1 — Exploratory and Prototype Confidence Profile

## 1. Intent

Reduce the uncertainties that determine whether an idea, requirement, architecture, model, or dependency is viable. Avoid creating durable process or test assets before their value is understood.

## 2. Applicability

Use for spikes, prototypes, feasibility studies, architecture experiments, uncertain requirements, and early model or data exploration.

## 3. Required evidence

No structural test scope is universally mandatory. The prototype must nevertheless address each assumption whose failure would invalidate the conclusion.

Suitable evidence may include:

* executable examples or small unit/component checks,
* property, differential, or metamorphic experiments,
* integration probes against uncertain external semantics,
* performance or capacity measurements where architecture depends on them,
* threat or privacy analysis where sensitive data or trust boundaries are involved,
* exploratory sessions, user observation, or usability evaluation,
* data validation and baseline measurement,
* written analysis where execution is not yet possible.

## 4. Procedure

1. State the decision the prototype is intended to inform.
2. List the critical assumptions and unknowns.
3. Identify the cheapest credible evidence for each.
4. Run the experiments and record contradictory or inconclusive results.
5. Distinguish demonstrated facts from assumptions that remain open.
6. Decide whether code and tests are disposable, reusable as characterization evidence, or suitable for promotion after reevaluation.

## 5. Exit criteria

Return a **finding** to L1. The finding must state:

* which uncertainties were reduced,
* which remain material,
* what evidence was collected,
* whether the prototype may be promoted and under what reevaluation,
* what evidence is required before the next decision.

Do not describe a prototype as production-ready merely because its demonstration succeeds.

## 6. Relevant L3 procedures

Commonly relevant:

* **L3-T6:** Generative Testing
* **L3-T11:** Metric Design
* **L3-T12:** Acceptance Testing
* **L3-T13:** Exploratory Testing
* **L3-T14:** Usability and Accessibility

Invoke integration, security, performance, contract, or operational procedures whenever those risks are already material.
