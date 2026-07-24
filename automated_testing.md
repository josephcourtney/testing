---
aliases:
  - Automated Testing Reference
linter-yaml-title-alias: Automated Testing Reference
status: reference
tags: []
title: Automated Testing Reference
---

# Automated Testing Reference

This document is a non-normative encyclopedia. It discusses common concepts, techniques, conventions, and tradeoffs. Canonical terminology is defined in `glossary.md`; requirements are defined in `Overview.md` and the L1/L2/L3 procedures; Python implementation guidance is in `python_testing.md`.

Testing terminology is not standardized across organizations. The definitions in `glossary.md` state the meanings used within this repository. External sources and project-specific guides may use the same labels differently.

## Core concerns

Automated testing usually attempts to balance:

* **confidence** — sensitivity to relevant failures,
* **feedback latency** — how soon useful evidence arrives,
* **localization** — how narrowly a failure identifies the problem,
* **fidelity** — how closely the exercised semantics match the deployed system,
* **control** — ability to create inputs and failures deliberately,
* **repeatability** — ability to reproduce results,
* **maintenance cost** — effort required to keep evidence useful.

No technique maximizes all of these simultaneously.

## Classification dimensions

This section is an overview. Consult `glossary.md` for the canonical definitions and distinctions used by the policy and procedures.

### Structural scope

* **Unit** — a small chosen execution boundary. Some teams use solitary units with replaced collaborators; others use sociable units with inexpensive real collaborators.
* **Component** — a coherent subsystem exercised through a supported interface while dependencies outside the boundary are controlled.
* **Integration** — evidence that depends on real behavior across a process, infrastructure, protocol, service, or platform boundary.
* **System** — the assembled product exercised through a user- or operator-visible boundary.

### Purpose

* **Acceptance** — demonstrates a concrete stakeholder or product condition.
* **Regression** — protects a learned behavior or previous failure mode.
* **Contract** — verifies obligations between producers and consumers.
* **Smoke** — provides a small, fast indication that critical capabilities are available.
* **Compatibility** — checks supported versions, platforms, data formats, or consumers.
* **Performance** — measures latency, throughput, resource use, or scalability.
* **Security** — evaluates threat-relevant properties and abuse cases.
* **Data quality** — evaluates integrity, freshness, uniqueness, distribution, or lineage claims.
* **Observability** — evaluates whether logs, metrics, traces, and diagnostics meet operational needs.
* **Accessibility and usability** — evaluates whether intended users can perceive, understand, and complete tasks.
* **Resilience and recovery** — evaluates degraded behavior, rollback, failover, restoration, and incident response.

Purposes are orthogonal to structural scope. A regression, contract, security, or acceptance test may execute at several scopes.

### Techniques

* **Example-based testing** checks selected cases with explicit expected results.
* **Property-based testing** generates inputs and evaluates invariants.
* **State-machine/model-based testing** generates action sequences and compares resulting state with a model or invariant.
* **Differential testing** compares independent implementations, versions, or execution modes.
* **Metamorphic testing** checks relations between transformed inputs and outputs when a direct oracle is difficult.
* **Fuzzing** explores malformed, adversarial, or coverage-guided inputs.
* **Snapshot/golden testing** compares a canonical representation with a reviewed baseline.
* **Mutation testing** alters implementation behavior to evaluate whether the selected tests detect the change.
* **Fault injection and chaos engineering** introduce controlled failures to evaluate resilience and recovery.
* **Exploratory testing** combines learning, test design, and execution without relying only on predefined cases.
* **Formal verification** proves specified properties under an explicit model.

See `glossary.md` for complete definitions and additional terms.

## Test doubles and real dependencies

Common options include:

* **stub** — returns controlled responses,
* **mock** — records or constrains interactions,
* **fake** — implements a simplified but usable substitute,
* **simulator** — approximates externally observable behavior,
* **record/replay** — reuses captured interactions,
* **containerized dependency** — runs a real implementation in an isolated environment,
* **shared test environment** — provides realistic integration at higher coordination cost.

Mocks and fakes provide control and speed but may diverge from real semantics. Real dependencies provide fidelity but may reduce control and repeatability. A common portfolio uses doubles for exhaustive logic and fault cases, contract evidence for alignment, and focused real-dependency tests for semantic fidelity.

## Development workflows

Common workflows include:

* **test-driven development** — alternate failing test, implementation, and refactoring,
* **acceptance-test-driven development** — establish stakeholder-facing examples before implementation,
* **test-after development** — implement or explore first, then encode stable behavior,
* **characterization testing** — capture current behavior before changing poorly understood code,
* **property discovery** — alternate implementation, examples, generated counterexamples, and specification refinement,
* **exploratory prototyping** — use experiments and measurements before committing to a durable design.

None is universally required. The appropriate workflow depends on how well the behavior is understood, the cost of mistakes, and the available oracle.

## Test organization conventions

Common directory organizations include:

* mirroring the source tree,
* grouping by structural scope,
* grouping by feature or user capability,
* colocating tests with implementation,
* separating expensive, destructive, compatibility, or deployment suites.

Common code structures include Arrange–Act–Assert, Given–When–Then, table-driven cases, fixtures, factories, builders, and domain-specific test languages. These are readability conventions, not definitions of correctness.

For a concrete pytest implementation, see `python_testing.md`.

## Feedback portfolios

Many projects maintain multiple feedback loops:

* edit-time checks for local logic,
* pre-commit or pre-merge checks for broad deterministic evidence,
* scheduled checks for expensive integrations, compatibility, mutation, fuzzing, or performance,
* release checks against built artifacts and deployment environments,
* production monitoring and synthetic transactions.

The exact cadence should follow cost, change frequency, failure impact, and the time at which evidence can still affect the decision.

## Metrics

Common metrics include line or branch coverage, requirement or case coverage, mutation score, runtime, flake observations, defect escape, compatibility cells, performance distributions, and data-drift statistics.

These metrics have no universal target. Their interpretation depends on the population, tool, code cohort, environment, sample size, and decision. See `L3_T11_metrics.md` for the required design procedure before using a metric as a gate.

## Common failure modes

* Tests assert implementation details rather than stable behavior.
* Doubles model the implementation instead of the external obligation.
* Large system suites duplicate lower-scope checks and produce poor localization.
* Lower-scope tests omit real semantics that caused the actual risk.
* Arbitrary sleeps conceal missing synchronization.
* Partial runs overwrite complete evidence.
* Retries conceal nondeterminism.
* Snapshots are updated without reviewing semantic changes.
* Coverage or mutation percentages are treated as proof of correctness.
* Manual, exploratory, usability, or operational evidence is omitted because it is not easily automated.

## Related documents

* `glossary.md` — canonical repository terminology
* `python_testing.md` — Python and pytest implementation guidance
* `L3_T1_unit.md` — unit test design
* `L3_T2_component.md` — component test design
* `L3_T3_integration.md` — integration test design
* `L3_T4_system.md` — system and smoke testing
* `L3_T5_regression.md` — regression testing
* `L3_T6_property-based.md` — generative testing
* `L3_T7_contract.md` — contract and compatibility testing
* `L3_T8_non-functional.md` — performance, security, data quality, and observability
* `L3_T9_snapshot.md` — snapshot testing
* `L3_T10_health_and_metrics.md` — suite health
* `L3_T11_metrics.md` — metric design
* `L3_T12_acceptance.md` — acceptance testing
* `L3_T13_exploratory.md` — exploratory testing
* `L3_T14_usability_accessibility.md` — usability and accessibility testing
* `L3_T15_operational_resilience.md` — operational, resilience, and recovery testing
