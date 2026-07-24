# Testing Policy

## 1. Purpose

Testing exists to provide justified confidence in claims about a system. A project must connect:

1. the claims it intends to make,
2. the failure modes that could invalidate those claims,
3. evidence capable of detecting those failures,
4. the confidence required for the current decision, and
5. the cost and limits of obtaining that evidence.

No test type, metric, lifecycle stage, or tool is a substitute for this connection.

### 1.1 Terminology and implementation guidance

`glossary.md` is the canonical terminology reference for this policy and the L1/L2/L3 procedures. If a glossary definition conflicts with a normative requirement, this policy or the applicable procedure controls.

`automated_testing.md` is non-normative conceptual reference material. `python_testing.md` is non-normative Python and pytest implementation guidance. Project-specific conventions and thresholds belong under `examples/` or in the adopting project's own documentation.

## 2. Core requirements

A testing strategy must:

* identify material product, technical, operational, security, data, and usability risks,
* identify critical responsibilities, invariants, boundaries, contracts, and user journeys,
* select evidence that is sensitive to the relevant failure modes,
* keep feedback timely enough that the evidence is actually used,
* make failures reproducible and diagnosable,
* distinguish measured facts from assumptions and risk acceptance,
* prevent partial or stale evidence from being represented as a complete result,
* record material waivers with an owner, rationale, mitigation, and expiry or revisit trigger.

A project must not claim confidence merely because a suite passes, a coverage target is met, or a named set of test levels exists.

## 3. Risk and evidence model

For each material change or release decision, record the following where relevant:

### 3.1 Claim

What must be true?

Examples:

* a parser preserves documented semantics,
* an API remains compatible with deployed consumers,
* a migration preserves data and supports rollback,
* a CLI installed from the wheel behaves as documented,
* a critical workflow remains within its latency objective,
* operators receive sufficient signals to diagnose failure.

### 3.2 Failure mode

How could the claim be false?

Consider incorrect logic, omitted cases, boundary mismatches, configuration drift, dependency behavior, race conditions, resource exhaustion, hostile input, human misunderstanding, inaccessible interaction, deployment failure, and recovery failure.

### 3.3 Evidence

What observation would detect that failure with useful sensitivity?

Evidence may include automated tests, static analysis, formal methods, reviews, exploratory sessions, usability studies, production observations, audits, simulations, measurements, and incident history.

### 3.4 Confidence and decision

State what decision the evidence supports: exploration, merge, beta use, production release, continued operation, or risk acceptance. Evidence sufficient for one decision may be insufficient for another.

### 3.5 Residual uncertainty

Record important limitations, untested conditions, unrealistic doubles, missing environments, insufficient sample sizes, and assumptions about users or dependencies.

## 4. Classification model

Test labels describe independent dimensions. Projects should not force purposes and techniques into one mutually exclusive hierarchy.

### 4.1 Structural scope

A test should declare one primary structural scope when scope markers are used:

* **unit** — a small chosen boundary with highly localizing failures,
* **component** — a coherent subsystem exercised through a supported interface,
* **integration** — behavior that depends on real semantics across a system or infrastructure boundary,
* **system** — the assembled product exercised through a user- or operator-visible boundary.

These labels describe the executed boundary, not the test's purpose. The size of a unit is a project convention; it need not be a single function or class.

### 4.2 Resource and boundary use

Declare material resources or boundaries when they affect isolation, cost, or interpretation:

* filesystem,
* process,
* database,
* network,
* broker,
* clock,
* random source,
* hardware,
* third-party service,
* production environment.

### 4.3 Purpose

Purposes may be combined with any suitable structural scope:

* acceptance,
* regression,
* contract,
* smoke,
* compatibility,
* security,
* performance,
* data quality,
* observability,
* accessibility,
* resilience,
* recovery.

For example, a contract test may be component-, integration-, or system-scoped. Regression describes why a test exists, not how much of the system it executes.

### 4.4 Technique

Techniques include:

* example-based testing,
* property-based testing,
* state-machine or model-based testing,
* differential testing,
* metamorphic testing,
* fuzzing,
* snapshot or golden testing,
* fault injection,
* simulation,
* formal verification,
* exploratory testing.

### 4.5 Execution and cadence

Projects may additionally classify tests by cost or scheduling, such as fast, slow, destructive, isolated, quarantined, per-edit, pre-merge, scheduled, release, and continuous-production checks.

## 5. Evidence selection

Evidence must be selected from risk and architecture rather than from a universal inventory.

Examples:

* Pure transformation risk often favors example and property tests at unit or component scope.
* SQL, transaction, serialization, authentication, retry, and protocol risks require evidence against real semantics.
* Published interfaces require explicit compatibility obligations and provider or consumer verification where applicable.
* Packaging and deployment claims require exercising the built artifact outside the source checkout.
* User-journey claims require acceptance or system evidence.
* Ambiguous requirements require exploratory or collaborative evaluation, not only automated checks.
* Performance, security, accessibility, privacy, data quality, and operability require dedicated evidence whenever failure would be material.

A lifecycle profile may increase the required confidence, enforcement, environmental fidelity, or breadth. It must not defer an already-material risk merely because a named phase has not been reached.

## 6. Test design

Tests should:

* assert observable behavior, invariants, or explicit contracts,
* fail for a reason connected to the risk they address,
* use the smallest scope that preserves the relevant semantics,
* retain real collaborators when they are cheap, deterministic, and part of the chosen boundary,
* replace collaborators when control, speed, or fault injection is the purpose,
* pair doubles with contract or integration evidence when double fidelity is consequential,
* avoid arbitrary sleeps, hidden ordering, uncontrolled shared state, and unbounded waits,
* provide enough diagnostic context to distinguish product failure from harness failure.

Tests must not be optimized solely for low scope. Moving a test downward is beneficial only if it preserves sensitivity to the failure mode.

## 7. Development and organization conventions

The following are selectable conventions, not universal requirements:

* test-driven development,
* test-after development,
* acceptance-test-driven development,
* solitary or sociable unit testing,
* Arrange–Act–Assert or other readable structures,
* source-mirroring or behavior-oriented test directories,
* mocks, fakes, simulators, containers, or shared test environments,
* a pyramid, trophy, honeycomb, or other portfolio shape.

A project may standardize any of these when doing so improves collaboration. The standard must state its purpose and must not be treated as proof of test quality.

## 8. Tooling and execution integrity

Projects should provide named commands for common workflows and should use strict configuration where silent misconfiguration would invalidate evidence.

A testing workflow must distinguish:

* complete from selected runs,
* fresh from stale evidence,
* source-tree behavior from installed-artifact behavior,
* comparable from non-comparable environments,
* deterministic failures from suspected flakes,
* measurements from release gates.

Retries must not silently convert nondeterminism into success. Quarantine must be explicit, owned, time-bounded, and excluded from claims it cannot support.

## 9. Measurement policy

No repository-wide numeric target is universal. Coverage, mutation score, flake rate, runtime, defect escape, performance, data drift, and similar metrics may be used only after the project defines:

* the decision the metric informs,
* the population and denominator,
* the collection method and environment,
* the comparison window or baseline,
* uncertainty and known sources of bias,
* the threshold rationale,
* the action taken when the threshold is crossed.

Coverage is evidence of execution, not correctness. Mutation score is meaningful only for the declared mutant operators and code cohort. Flake rates require enough comparable observations to support the claimed precision. Performance gates require controlled comparisons and a practically meaningful effect size.

Use **L3-T11** for metric design and validation.

## 10. Lifecycle profiles

Lifecycle profiles in `L2_*.md` establish default confidence and governance expectations:

* prototype — reduce important uncertainty without unnecessary ceremony,
* development — make changed responsibilities and known acceptance conditions executable,
* stabilization — validate critical boundaries, compatibility, user journeys, and suite health,
* production — require release evidence, operational readiness, and explicit residual risk,
* maintenance — protect learned behavior, reassess changed risks, and use operational evidence.

Risk overrides these defaults in both directions. A prototype handling sensitive data may require strong security controls; a mature local utility with no external integrations does not need fictitious integration tests.

## 11. Required records

For material decisions, retain enough information to reconstruct:

* the change or release scope,
* relevant risks and claims,
* selected evidence and why it is appropriate,
* results and environment identity,
* unresolved gaps and waivers,
* the resulting pass, conditional pass, fail, or exploratory finding.

The record may be lightweight for low-risk work and more formal for high-impact, regulated, or production decisions.
