# Testing Policy

## 1. Purpose

Testing exists to provide justified confidence in claims about a system.

A project must connect:

1. the claims it intends to make,
2. the failure modes that could invalidate those claims,
3. evidence capable of detecting those failures,
4. the confidence required for the current decision, and
5. the cost and limits of obtaining that evidence.

No test type, metric, lifecycle stage, portfolio shape, or tool is a substitute for this connection.

This document defines project-wide policy for selecting, designing, executing, interpreting, and recording testing evidence. Detailed procedures belong in the corresponding L1, L2, and L3 documents.

### 1.1 Terminology and implementation guidance

`glossary.md` is the canonical terminology reference. If a glossary definition conflicts with a normative requirement, this policy or the applicable L1, L2, or L3 procedure controls.

`automated_testing.md` is non-normative conceptual reference material.

`python_testing.md` is non-normative Python and pytest implementation guidance.

Project-specific commands, markers, thresholds, directory layouts, tool configurations, runtime budgets, and support matrices belong under `examples/` or in the adopting project's own documentation.

Use **must** for requirements and **should** for strong recommendations.

## 2. Core requirements

A testing strategy must:

* identify material product, technical, operational, security, privacy, data, accessibility, and usability risks,
* identify critical responsibilities, invariants, boundaries, contracts, and user journeys,
* select evidence sensitive to the relevant failure modes,
* keep feedback timely enough that the evidence is actually used,
* make failures reproducible and diagnosable,
* distinguish measured facts from assumptions, inference, and risk acceptance,
* distinguish complete from partial or stale evidence,
* prevent selected or non-comparable results from being represented as complete,
* record material waivers with an owner, rationale, mitigation, and expiry or revisit trigger,
* maintain testing and analysis infrastructure as production assets.

A project must not claim confidence merely because a suite passes, a coverage target is met, or a named inventory of test levels exists.

## 3. Risk and evidence model

For each material change, release, deployment, or continued-operation decision, record the following where relevant.

### 3.1 Claim

What must be true?

Examples include:

* a parser preserves documented semantics,
* an API remains compatible with deployed consumers,
* a migration preserves data and supports rollback,
* a CLI installed from the built artifact behaves as documented,
* a critical workflow remains within its latency objective,
* operators receive sufficient signals to diagnose and recover from failure.

### 3.2 Failure mode

How could the claim be false?

Consider incorrect logic, omitted cases, invalid state transitions, boundary mismatches, configuration drift, dependency behavior, concurrency, resource exhaustion, hostile input, human misunderstanding, inaccessible interaction, packaging failure, and incomplete recovery.

### 3.3 Evidence

What observation would detect the failure with useful sensitivity?

Evidence may include automated tests, static analysis, formal methods, review, exploratory sessions, usability or accessibility studies, simulations, audits, measurements, production observations, and incident history.

### 3.4 Confidence and decision

State the decision the evidence supports, such as exploration, merge, beta use, production release, deployment, continued operation, or risk acceptance.

Evidence sufficient for one decision may be insufficient for another.

### 3.5 Residual uncertainty

Record important limitations, including untested conditions, unrealistic doubles, missing environments, insufficient samples, non-comparable measurements, unsupported users, and risks accepted rather than eliminated.

## 4. Classification model

Test labels describe independent dimensions. Projects must not force structural scope, purpose, technique, resource use, and cadence into one mutually exclusive hierarchy.

### 4.1 Structural scope

When scope markers are used, an automated functional test should identify one primary structural scope:

* **unit** — a small chosen boundary with highly localizing failures,
* **component** — a coherent subsystem exercised through a supported interface,
* **integration** — behavior whose evidential value depends on real semantics across a boundary,
* **system** — the assembled product exercised through a user- or operator-visible boundary.

The primary scope is the boundary whose semantics determine how the evidence should be interpreted. Additional resource and boundary labels may be recorded.

Scope describes the executed boundary, not the test's purpose. A unit need not be a single function or class.

### 4.2 Resource and boundary use

Declare material resources or boundaries when they affect isolation, cost, fidelity, or interpretation, including filesystems, processes, databases, networks, brokers, clocks, random sources, external services, hardware, platforms, configuration, production-derived data, and production environments.

### 4.3 Purpose

Purposes may be combined with any suitable structural scope, including acceptance, regression, characterization, sanity, contract, smoke, compatibility, migration, rollback, security, privacy, performance, data quality, observability, accessibility, usability, resilience, recovery, and operational readiness.

For example, a contract test may be component-, integration-, or system-scoped. Regression describes why a test exists, not how much of the system it executes.

### 4.4 Technique

Techniques include example-based, property-based, state-machine, model-based, differential, metamorphic, fuzz, mutation, snapshot, fault-injection, chaos, simulation, formal-verification, static-analysis, and exploratory techniques.

Select techniques according to the failure modes they can reveal.

### 4.5 Execution and cadence

Projects may classify evidence by execution properties or scheduling, such as per-edit, pre-commit, pre-merge, scheduled, release, post-deployment, continuous, fast, slow, destructive, hermetic, isolated, or quarantined.

Cadence must be selected according to evidence value, cost, and required feedback latency. No test type or check is universally required at every cadence.

## 5. Evidence selection

Evidence must be selected from risk and architecture rather than from a universal inventory.

Examples:

* Pure transformation risk often favors example and property evidence at unit or component scope.
* SQL, transaction, serialization, authentication, retry, and protocol risks require evidence against real semantics.
* Published interfaces require explicit compatibility obligations and provider or consumer verification where applicable.
* Packaging claims require exercising the built artifact outside the source checkout.
* User-journey claims require acceptance or system evidence.
* Ambiguous requirements require exploratory or collaborative evaluation.
* Performance, security, privacy, accessibility, usability, data quality, and operability require dedicated evidence whenever failure would be material.
* Recovery claims require evidence for restart, rollback, failover, restoration, degraded operation, and observability where applicable.

A lifecycle profile may increase required confidence, enforcement, environmental fidelity, breadth, or recordkeeping. It must not defer an already-material risk merely because a named phase has not been reached.

A project must not rely on one scope, technique, metric, or portfolio shape as a substitute for risk-appropriate evidence.

## 6. Test design

Tests should:

* assert observable behavior, invariants, state transitions, or explicit contracts,
* fail for a reason connected to the risk they address,
* use the least costly scope that preserves the relevant semantics,
* provide enough context to distinguish product, dependency, environment, and harness failure,
* identify relevant input, environment, resource, and boundary conditions,
* avoid incidental assertions that do not increase failure sensitivity.

Tests must not be optimized solely for low scope. Moving a test downward is beneficial only when it preserves sensitivity to the targeted failure mode.

### 6.1 Isolation and realism

Isolation and realism must be balanced according to the claim and risk.

Tests should retain real collaborators when they are cheap, deterministic, and part of the chosen boundary; replace collaborators when control or fault injection is needed; pair consequential doubles with contract, integration, or compatibility evidence; and use representative real environments when substitutes cannot provide valid evidence.

A fake, mock, simulator, emulator, stub, or recorded response must not be treated as proof of behavior that depends on the real system it replaces.

### 6.2 Assertions and diagnostics

Assertions should target stable, externally meaningful behavior. Avoid private state, incidental call sequences, unstable formatting, non-contractual log text, and implementation-specific ordering unless those details are the explicit subject of the test.

Failures must identify the violated claim, relevant inputs, environment, and exercised boundary.

### 6.3 Configuration and environment

Behavior that varies across supported configuration, environment, platform, feature flags, deployment modes, hardware, or compatibility versions must have representative evidence.

Selected combinations should be justified by support commitments, usage, architecture, and risk. Exhaustive matrices are required only when the combinations are themselves contractual.

## 7. Development and organization conventions

The following are selectable conventions, not universal requirements:

* test-driven, test-after, acceptance-test-driven, or exploratory development,
* solitary or sociable unit testing,
* Arrange–Act–Assert, Given–When–Then, or another readable structure,
* source-mirroring, scope-oriented, feature-oriented, or colocated directories,
* mocks, fakes, simulators, containers, or shared environments,
* a pyramid, trophy, honeycomb, or another portfolio shape.

A project may standardize a convention when doing so improves collaboration. The standard must state its purpose and must not be treated as proof of test quality.

## 8. Tooling and execution integrity

Projects should provide named commands for common workflows and use strict configuration where silent misconfiguration would invalidate evidence.

A workflow must distinguish:

* complete from selected runs,
* fresh from stale evidence,
* source-tree behavior from installed-artifact behavior,
* comparable from non-comparable environments,
* deterministic failures from suspected flakes,
* measurements from release gates,
* product failures from dependency, harness, or infrastructure failures.

Retries must not silently convert nondeterminism into success.

Quarantine must be explicit, owned, time-bounded, and excluded from claims it cannot support.

Static, security, and supply-chain checks must be selected according to language, dependencies, threat model, and support policy. Every required check must have a documented cadence, failure policy, owner, and triage and waiver process.

## 9. Measurement policy

No repository-wide numeric target is universal.

Before a metric is used as a target or gate, define the decision, claim, population, denominator, collection method, environment, baseline or window, uncertainty, threshold rationale, response, owner, and review trigger.

Coverage is evidence of execution, not correctness. Mutation score is meaningful only for the declared cohort, operators, exclusions, and outcome treatment. Flake observations require a defined unit and sufficient comparable history. Performance gates require controlled comparisons and practically meaningful effect sizes.

Improving a metric must not be pursued through tests or assertions that add no meaningful defect-detection value.

Use **L3-T10** for suite-health assessment and **L3-T11** for metric design, validation, and interpretation.

## 10. Lifecycle profiles

Lifecycle profiles in `L2_*.md` establish default confidence and governance expectations:

* **prototype (L2-P1)** — reduce important uncertainty without unnecessary ceremony,
* **development / alpha (L2-P2)** — make changed responsibilities and known acceptance conditions executable,
* **stabilization / beta (L2-P3)** — validate critical boundaries, compatibility, user journeys, and suite health,
* **production (L2-P4)** — require release evidence, operational readiness, and explicit residual risk,
* **maintenance (L2-P5)** — protect learned behavior, reassess changed risks, and use operational evidence.

Risk overrides these defaults in both directions.

## 11. Exceptions and waivers

A policy exception or waiver must record:

* the requirement being waived,
* why it is not currently appropriate or feasible,
* the affected claim, scope, and risk,
* compensating evidence or controls,
* the owner,
* the expiry date or revisit trigger,
* the conditions for removal.

Temporary disabling of evidence must have tracked follow-up. Blocking findings must not be suppressed without documented review.

## 12. Prohibited practices

Tests and testing workflows must not:

* rely on arbitrary sleeps when explicit synchronization or bounded polling is available,
* depend on hidden execution order or undocumented shared mutable state,
* use unbounded waits,
* access or mutate production resources without explicit authorization and controls,
* silently ignore failures,
* allow retries to conceal nondeterminism,
* leave known flakes untriaged indefinitely,
* represent selected, partial, stale, or non-comparable evidence as complete,
* chase numeric targets with trivial assertions,
* use broad snapshots as a substitute for practical semantic assertions,
* assert unstable implementation details without reason,
* treat doubles as proof of real integration semantics,
* casually suppress test, static-analysis, vulnerability, or secret-scanner failures,
* disable required evidence without a documented waiver.

Where a prohibition cannot be followed, Section 11 applies.

## 13. Required records

For material decisions, retain enough information to reconstruct:

* the change, release, deployment, or operating scope,
* relevant claims and risks,
* selected evidence and why it is appropriate,
* commands, configurations, versions, artifacts, and environment identity,
* results and measurement conditions,
* unresolved gaps and residual uncertainty,
* waivers and compensating controls,
* the resulting pass, conditional pass, fail, exploratory finding, or risk-acceptance decision.

The record may be lightweight for low-risk work and more formal for high-impact, regulated, safety-critical, or production decisions.

## 14. Detailed procedures

The L3 procedures are:

* **L3-T1** — unit testing,
* **L3-T2** — component testing,
* **L3-T3** — integration testing,
* **L3-T4** — system testing,
* **L3-T5** — regression testing,
* **L3-T6** — generative, property, model, and differential testing,
* **L3-T7** — contract and compatibility testing,
* **L3-T8** — non-functional testing,
* **L3-T9** — snapshot and golden testing,
* **L3-T10** — test-suite health,
* **L3-T11** — metric design and validation,
* **L3-T12** — acceptance testing,
* **L3-T13** — exploratory testing,
* **L3-T14** — usability and accessibility testing,
* **L3-T15** — operational, resilience, and recovery testing.

This policy controls when a procedure conflicts with a project convention or non-normative implementation guide.
