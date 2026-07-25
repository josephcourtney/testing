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

This document defines project-wide policy for selecting, designing, executing, interpreting, and recording testing evidence. Detailed procedures for individual test scopes, purposes, and techniques belong in the corresponding L1, L2, and L3 documents.

### 1.1 Terminology and implementation guidance

`glossary.md` is the canonical terminology reference for this policy and the L1, L2, and L3 procedures. If a glossary definition conflicts with a normative requirement, this policy or the applicable procedure controls.

`automated_testing.md` is non-normative conceptual reference material.

`python_testing.md` is non-normative Python and pytest implementation guidance.

Project-specific commands, markers, thresholds, directory layouts, tool configurations, runtime budgets, and support matrices belong under `examples/` or in the adopting project's own documentation.

Use **must** for requirements and **should** for strong recommendations.

## 2. Core requirements

A testing strategy must:

* identify material product, technical, operational, security, privacy, data, accessibility, and usability risks,
* identify critical responsibilities, invariants, boundaries, contracts, and user journeys,
* select evidence that is sensitive to the relevant failure modes,
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

Consider:

* incorrect logic,
* omitted cases,
* invalid state transitions,
* boundary mismatches,
* configuration drift,
* dependency behavior,
* concurrency and race conditions,
* resource exhaustion,
* hostile or malformed input,
* human misunderstanding,
* inaccessible interaction,
* packaging or deployment failure,
* rollback or recovery failure.

### 3.3 Evidence

What observation would detect the failure with useful sensitivity?

Evidence may include:

* automated tests,
* static analysis,
* formal methods,
* code or design review,
* exploratory sessions,
* usability or accessibility studies,
* simulations,
* audits,
* measurements,
* production observations,
* incident and defect history.

### 3.4 Confidence and decision

State the decision the evidence supports, such as:

* exploration,
* merge,
* beta use,
* production release,
* deployment,
* continued operation,
* risk acceptance.

Evidence sufficient for one decision may be insufficient for another.

### 3.5 Residual uncertainty

Record important limitations, including:

* untested conditions,
* unrealistic or unverified doubles,
* missing environments,
* insufficient sample sizes,
* non-comparable measurements,
* assumptions about users, data, hardware, or dependencies,
* risks accepted rather than eliminated.


## 4. Classification model

Test labels describe independent dimensions. Projects must not force structural scope, purpose, technique, resource use, and cadence into one mutually exclusive hierarchy.

### 4.1 Structural scope

When scope markers are used, an automated functional test should identify one primary structural scope:

* **unit** â€” a small chosen boundary with highly localizing failures,
* **component** â€” a coherent subsystem exercised through a supported interface,
* **integration** â€” behavior that depends on real semantics across a system or infrastructure boundary,
* **system** â€” the assembled product exercised through a user- or operator-visible boundary.

The primary scope is the boundary whose semantics determine how the evidence should be interpreted. Additional scope or boundary labels may be recorded when a test intentionally spans multiple boundaries.

Scope describes the executed boundary, not the test's purpose. The size of a unit is a project convention; it need not be a single function or class.

### 4.2 Resource and boundary use

Declare material resources or boundaries when they affect isolation, cost, fidelity, or interpretation:

* filesystem,
* process,
* database,
* network,
* broker,
* clock or scheduler,
* random source,
* external service,
* hardware,
* operating system or platform,
* configuration or environment,
* production-derived data,
* production environment.

### 4.3 Purpose

Purposes may be combined with any suitable structural scope:

* acceptance,
* regression,
* contract,
* smoke,
* compatibility,
* security,
* privacy,
* performance,
* data quality,
* observability,
* accessibility,
* usability,
* resilience,
* recovery.

For example, a contract test may be component-, integration-, or system-scoped. Regression describes why a test exists, not how much of the system it executes.

### 4.4 Technique

Techniques include:

* example-based testing,
* property-based and generative testing,
* state-machine or model-based testing,
* differential testing,
* metamorphic testing,
* fuzzing,
* mutation testing,
* snapshot or golden testing,
* fault injection,
* chaos testing,
* simulation,
* formal verification,
* exploratory testing.

Techniques must be selected according to the failure modes they can reveal.

### 4.5 Execution and cadence

Projects may classify evidence by cost, environment, or scheduling, such as:

* per-edit,
* local development,
* pre-commit,
* pre-merge,
* scheduled,
* release,
* pre-deployment,
* post-deployment,
* continuous production,
* fast,
* slow,
* destructive,
* isolated,
* quarantined.

Cadence must be selected according to evidence value, cost, and required feedback latency. No test type or check is universally required at every cadence.

## 5. Evidence selection

Evidence must be selected from risk and architecture rather than from a universal inventory.

Examples:

* Pure transformation risk often favors example and property tests at unit or component scope.
* SQL, transaction, serialization, authentication, retry, and protocol risks require evidence against real semantics.
* Published interfaces require explicit compatibility obligations and provider or consumer verification where applicable.
* Packaging and deployment claims require exercising the built artifact outside the source checkout.
* User-journey claims require acceptance or system evidence.
* Ambiguous requirements require exploratory or collaborative evaluation, not only automated checks.
* Performance, security, privacy, accessibility, usability, data quality, and operability require dedicated evidence whenever failure would be material.
* Recovery claims require evidence for restart, rollback, failover, restoration, degraded operation, and observability where applicable.

A lifecycle profile may increase required confidence, enforcement, environmental fidelity, or breadth. It must not defer an already-material risk merely because a named phase has not been reached.

A project must not rely on one scope, technique, metric, or portfolio shape as a substitute for risk-appropriate evidence.

## 6. Test design

Tests should:

* assert observable behavior, invariants, state transitions, or explicit contracts,
* fail for a reason connected to the risk they address,
* use the smallest scope that preserves the relevant semantics,
* provide enough diagnostic context to distinguish product failure from harness failure,
* identify relevant input, environment, resource, and boundary conditions,
* avoid incidental assertions that do not increase failure sensitivity.

Tests must not be optimized solely for low scope. Moving a test downward is beneficial only if it preserves sensitivity to the targeted failure mode.

### 6.1 Isolation and realism

Isolation and realism must be balanced according to the claim and risk being tested.

Tests should:

* retain real collaborators when they are cheap, deterministic, and part of the chosen boundary,
* replace collaborators when control, speed, determinism, or fault injection is the purpose,
* use controlled substitutes when they improve evidence without removing the semantics under examination,
* pair consequential doubles with contract, integration, or compatibility evidence,
* use real dependencies or representative environments when substitutes cannot provide valid evidence.

A fake, mock, simulator, emulator, stub, or recorded response must not be treated as proof of behavior that depends on the real system it replaces.

### 6.2 Assertions and diagnostics

Assertions should target stable, externally meaningful behavior.

Avoid assertions on:

* private state,
* incidental call sequences,
* unstable formatting,
* non-contractual log text,
* implementation-specific ordering,

unless those details are the explicit subject of the test.

Failures must provide enough context to identify the violated claim, relevant inputs, environment, and exercised boundary.

### 6.3 Configuration and environment

Behavior that varies across supported configuration, environment, platform, feature flags, deployment modes, hardware, or compatibility versions must have representative evidence.

The selected combinations should be justified by support commitments, usage, architecture, and risk. Exhaustive matrices are not required unless the combinations are themselves contractual.

## 7. Development and organization conventions

The following are selectable conventions, not universal requirements:

* test-driven development,
* test-after development,
* acceptance-test-driven development,
* solitary or sociable unit testing,
* Arrangeâ€“Actâ€“Assert or another readable structure,
* source-mirroring or behavior-oriented test directories,
* mocks, fakes, simulators, containers, or shared test environments,
* a pyramid, trophy, honeycomb, or another portfolio shape.

A project may standardize any of these when doing so improves collaboration. The standard must state its purpose and must not be treated as proof of test quality.

## 8. Tooling and execution integrity

Projects should provide named commands for common workflows and should use strict configuration where silent misconfiguration would invalidate evidence.

A testing workflow must distinguish:

* complete from selected runs,
* fresh from stale evidence,
* source-tree behavior from installed-artifact behavior,
* comparable from non-comparable environments,
* deterministic failures from suspected flakes,
* measurements from release gates,
* product failures from harness or infrastructure failures.

Retries must not silently convert nondeterminism into success.

Quarantine must be:

* explicit,
* owned,
* time-bounded,
* excluded from claims it cannot support.

Static, security, and supply-chain checks must be selected according to language, dependencies, threat model, and support policy. Required checks may include:

* formatting and linting,
* type checking,
* dependency and vulnerability analysis,
* secret scanning,
* license or policy checks,
* configuration validation,
* artifact integrity or provenance checks.

Each required check must have:

* a documented cadence,
* a defined failure policy,
* an owner,
* a triage and waiver process.

## 9. Measurement policy

No repository-wide numeric target is universal.

Coverage, mutation score, flake rate, runtime, defect escape, performance, capacity, resource use, data drift, snapshot churn, maintenance burden, and similar metrics may be used only after the project defines:

* the decision the metric informs,
* the population and denominator,
* the collection method and environment,
* the comparison window or baseline,
* uncertainty and known sources of bias,
* the threshold rationale,
* the action taken when the threshold is crossed,
* the owner.

Coverage is evidence of execution, not correctness.

Mutation score is meaningful only for the declared mutant operators, exclusions, and code cohort.

Flake rates require enough comparable observations to support the claimed precision.

Performance gates require controlled comparisons, an explicit baseline, and a practically meaningful effect size.

Improving a metric must not be pursued through tests or assertions that add no meaningful defect-detection value.

Use the applicable health-and-metrics procedure for metric design, validation, and interpretation.

## 10. Lifecycle profiles

Lifecycle profiles in `L2_*.md` establish default confidence and governance expectations:

* **prototype** â€” reduce important uncertainty without unnecessary ceremony,
* **development** â€” make changed responsibilities and known acceptance conditions executable,
* **stabilization** â€” validate critical boundaries, compatibility, user journeys, and suite health,
* **production** â€” require release evidence, operational readiness, and explicit residual risk,
* **maintenance** â€” protect learned behavior, reassess changed risks, and use operational evidence.

Risk overrides these defaults in both directions.

A prototype handling sensitive data may require strong security controls. A mature local utility with no external integrations does not need fictitious integration tests.

## 11. Exceptions and waivers

A policy exception or waiver must record:

* the requirement being waived,
* the reason it is not currently appropriate or feasible,
* the affected claim, scope, and risk,
* compensating evidence or controls,
* the owner,
* the expiry date or revisit trigger,
* the conditions for removal.

Temporary disabling of tests, static analysis, security checks, or required evidence must have a tracked follow-up and must not become an undocumented permanent state.

Blocking findings must not be suppressed without documented review.

## 12. Prohibited practices

Tests and testing workflows must not:

* rely on arbitrary sleeps when explicit synchronization, readiness checks, bounded polling, hooks, or events are available,
* depend on hidden execution order or undocumented shared mutable state,
* use unbounded waits,
* access production data or mutate production resources unless explicitly designed, authorized, and controlled for that environment,
* silently ignore failures,
* allow retries to conceal nondeterministic behavior,
* leave known flaky tests untriaged indefinitely,
* represent selected, partial, stale, or non-comparable evidence as complete,
* chase coverage or other numeric targets with trivial assertions,
* use broad snapshots as a substitute for practical semantic assertions,
* assert unstable implementation details without a documented reason,
* treat doubles as proof of real integration semantics,
* casually suppress secret-scanner, vulnerability, static-analysis, or test failures,
* disable required evidence without a documented waiver and follow-up.

Where a prohibition cannot be followed, the exception process in Section 11 applies.

## 13. Required records

For material decisions, retain enough information to reconstruct:

* the change, release, deployment, or operating scope,
* relevant risks and claims,
* selected evidence and why it is appropriate,
* commands, configurations, versions, and environment identity,
* results and measurement conditions,
* unresolved gaps and residual uncertainty,
* waivers and compensating controls,
* the resulting pass, conditional pass, fail, exploratory finding, or risk-acceptance decision.

The record may be lightweight for low-risk work and more formal for high-impact, regulated, safety-critical, or production decisions.

## 14. Detailed procedures

Detailed design, writing, execution, and evaluation guidance belongs in the applicable L1, L2, and L3 procedures, including procedures for:

* unit testing,
* component testing,
* integration testing,
* system testing,
* regression testing,
* property-based and generative testing,
* contract testing,
* non-functional and operational evidence,
* snapshot testing,
* suite health and metric design.

This policy controls when a procedure conflicts with a project convention or non-normative implementation guide.
