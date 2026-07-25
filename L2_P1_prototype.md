---
aliases:
  - L2-P1
linter-yaml-title-alias: L2-P1
tags: []
title: L2-P1
---

# L2-P1 — Exploratory / Prototype Testing Phase

## Procedure L2-P1: Exploratory / Prototype Testing Phase

## 1. Profile role

This is a lifecycle **confidence and governance profile**, not a universal test
inventory. It minimizes ceremony while reducing the uncertainty that matters to
the current decision.

Material security, privacy, safety, data, accessibility, external-impact, or
irreversibility risks are not deferred merely because the project is a
prototype. Apply L1 first and invoke whatever L3 procedures those risks require.

## 2. Phase intent

**Goal:**
Reduce uncertainty and validate feasibility with minimal friction.

**Primary risks addressed:**
Building the wrong thing; misunderstanding domain constraints; committing to an
architecture or interface before important assumptions are tested.

**Risks commonly deferred when they are not yet material:**
Long-term regression protection, broad compatibility, sustained performance,
production operations, and complete non-functional evidence.

Deferral is a recorded decision, not an automatic property of the phase.

Terminology is defined by `glossary.md`; general policy is defined by
`Overview.md`.

---

## 3. Applicability

Applies when:

* exploring new ideas, algorithms, workflows, or architectures,
* validating assumptions,
* building throwaway or experimental code,
* evaluating data, tools, dependencies, or feasibility,
* deciding whether a concept should advance into durable development.

This profile may also apply to a bounded experimental branch inside a mature
project. The surrounding production system may still require stronger evidence.

---

## 4. Assessment inputs

Record:

* the decision the prototype supports,
* assumptions and questions being investigated,
* users, operators, data, and systems exposed to the prototype,
* irreversible or expensive consequences,
* expected lifetime and whether the code may be promoted,
* evidence needed to distinguish useful learning from a misleading result.

## 5. Default evidence expectations

These are defaults to evaluate after L1, not mandatory categories that must be
created when they do not fit the risk.

### Required by the profile itself

No particular automated test scope is universally mandatory.

The assessment record, important assumptions, material risks, observations, and
limitations are required.

### Commonly useful

* **Unit tests** for critical logic or surprising behavior.
* **Property-based or differential tests** for core invariants,
  transformations, numeric behavior, parsers, or competing implementations.
* **Exploratory tests or scripts** used as executable experiments.
* **Acceptance examples** that make a fuzzy goal concrete.
* **Measurements or baseline capture** where feasibility depends on performance,
  data behavior, model quality, capacity, or resource use.
* **Contract or integration evidence** when the prototype's claim depends on a
  real interface or dependency.
* **Security, privacy, accessibility, or usability evaluation** when people,
  sensitive data, or external systems are materially exposed.

### Conditional decision rule

If evidence is omitted for a critical assumption or material failure mode,
record:

* the assumption, claim, or failure mode,
* why the omission is acceptable for the current decision,
* compensating observation, containment, or mitigation,
* owner,
* revisit trigger, often promotion to L2-P2, external use, handling real data,
  or an architecture commitment.

---

## 6. Explicit default non-requirements

Unless L1 identifies a corresponding material claim, this profile does not by
itself require:

* repository-wide coverage targets,
* a complete unit/component/integration/system portfolio,
* broad regression guarantees,
* full CI enforcement,
* production-scale performance testing,
* production operational-readiness exercises,
* compatibility matrices for unsupported platforms.

These are defaults only. A real risk overrides them.

---

## 7. Procedure

1. State the question, decision, and assumptions.
2. Select the smallest credible experiment or evidence source.
3. Define what observation would support, weaken, or reject the assumption.
4. Exercise representative, boundary, and failure conditions where they affect
   feasibility.
5. Record environment, data, versions, and important uncontrolled variables.
6. Capture exploratory findings, counterexamples, measurements, and unanswered
   questions.
7. Distinguish disposable scaffolding from evidence or code intended for
   promotion.
8. Decide whether to continue, revise, stop, or promote the work.
9. Convert durable discoveries into requirements, acceptance conditions,
   regression tests, contracts, or design constraints as appropriate.

## 8. Compliance and outcome

The profile is satisfied when:

* important assumptions and material risks are explicit,
* the selected evidence is capable of changing the decision,
* observations and limitations are recorded,
* no material exposure is dismissed solely because the work is early-stage,
* promotion conditions and unresolved risks have owners or triggers.

Record one of:

* **pass** — sufficient evidence supports the prototype decision,
* **conditional pass** — continuation is bounded by explicit conditions,
* **fail** — the evidence rejects a required assumption or leaves an
  unacceptable gap,
* **exploratory finding** — useful learning was produced without a pass/fail
  conclusion,
* **risk acceptance** — an authorized owner accepts a documented residual risk.

## 9. Outputs

* assumption and question inventory,
* prototype environment and data identity,
* experiments, tests, measurements, or review artifacts,
* findings and counterexamples,
* limitations and unexplored areas,
* promotion, discard, or continuation decision,
* follow-up evidence and revisit triggers.
