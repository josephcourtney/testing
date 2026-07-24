# Testing Policy

## 1. Purpose

This document defines the project-wide policy for selecting, designing, executing, and evaluating testing evidence.

Detailed procedures for individual test scopes and techniques are defined in the corresponding `L3_T*.md` documents. Language- and tool-specific implementation guidance belongs in the relevant implementation guide rather than in this policy.

## 2. Goals and principles

Tests must provide:

* Confidence proportionate to the consequences and likelihood of failure.
* Fast feedback for most changes.
* Clear localization and diagnosis of failures.
* Evidence that the system satisfies its functional and non-functional obligations.

Test suites must be:

* Structured by explicit scope and intent.
* Predictable to run, without hidden side effects.
* Strictly configured so that invalid configuration fails rather than being silently ignored.
* Repeatable within the limits of the system and environment being tested.
* Maintained as production assets rather than treated as disposable scaffolding.

Use **must** for requirements and **should** for strong recommendations.

## 3. Risk-driven evidence

Testing must be selected from identified claims, risks, and failure modes.

For each material risk, determine:

* What claim must be supported.
* Which failure modes could invalidate that claim.
* What evidence can detect those failures.
* Which environment, resources, data, and system boundaries the evidence must exercise.
* How frequently the evidence must be collected.
* What result blocks progression, requires follow-up, or is informational.

Lifecycle stage may change the breadth, fidelity, cadence, and enforcement of evidence, but it does not determine which test types are intrinsically applicable.

A project must not rely on one test scope, technique, or metric as a substitute for a risk-appropriate evidence portfolio.

## 4. Test classification

Tests must be described using independent dimensions rather than a single flat taxonomy.

### 4.1 Structural scope

Each automated functional test must identify the structural boundary it exercises:

* **Unit** â€” a small local behavioral boundary.
* **Component** â€” a coherent subsystem exercised through a supported interface.
* **Integration** â€” behavior that depends on real semantics across a boundary.
* **System** â€” an assembled system exercised at an external user or operator boundary.

The selected scope must reflect the semantics actually executed, not merely the directory, process count, fixture type, or tool used.

### 4.2 Purpose

A test may serve one or more purposes, including:

* Regression detection.
* Acceptance.
* Contract verification.
* Smoke verification.
* Compatibility.
* Resilience or recovery.
* Security.
* Performance.
* Data quality.
* Observability.
* Accessibility or usability.

Purpose does not replace structural scope. For example, a contract test may execute at component, integration, or system scope.

### 4.3 Technique

Techniques include:

* Example-based testing.
* Property-based and generative testing.
* Model-based or state-machine testing.
* Differential and metamorphic testing.
* Fuzzing.
* Mutation testing.
* Snapshot testing.
* Static analysis.
* Exploratory testing.
* Fault-injection and chaos testing.

Techniques must be selected according to the failure modes they can reveal.

### 4.4 Resources and boundaries

Tests should identify material resources and boundaries when relevant, including:

* Databases and persistent storage.
* Filesystems.
* Networks and external services.
* Message brokers.
* Clocks and schedulers.
* Processes and containers.
* Hardware or platform dependencies.
* Configuration and environment.
* Production-derived or synthetic data.

### 4.5 Execution cadence

Cadence must be selected according to evidence value, cost, and required feedback latency.

Common cadences include:

* Local development.
* Pre-commit.
* Pull request.
* Scheduled or nightly.
* Pre-release.
* Post-deployment.
* Continuous operational monitoring.

No test type or check is universally required at every cadence.

## 5. Test design

### 5.1 Design around behavior and invariants

For each tested boundary:

* Identify responsibilities in plain language.
* Identify invariants, state transitions, and externally observable obligations.
* Write tests that support those claims rather than merely executing lines of code.
* Exercise real external semantics when correctness depends on those semantics.
* Prefer the lowest-cost scope that can validly detect the targeted failure mode.

### 5.2 Assertions and observability

Tests should assert stable, externally meaningful behavior.

Avoid assertions on private state, incidental call sequences, unstable formatting, or non-contractual log text unless those details are the explicit subject of the test.

Failures must provide enough context to identify the violated claim, relevant inputs, environment, and boundary.

### 5.3 Isolation and realism

Isolation and realism must be balanced according to the risk being tested.

Use controlled substitutes when they improve determinism, fault injection, or feedback speed without removing the semantics under examination.

Use real dependencies or representative environments when substitutes cannot provide valid evidence.

A fake, mock, emulator, or recorded response must not be treated as proof of behavior that depends on the real system it replaces.

### 5.4 Configuration and environment

Behavior that varies across supported configuration, environment, platform, feature flags, deployment modes, or compatibility versions must have representative evidence.

The selected combinations should be justified by support commitments, usage, architecture, and risk. Exhaustive matrices are not required unless the combinations are themselves contractual.

## 6. Evidence portfolio

A project should maintain a portfolio that may include:

* Localizing functional tests across appropriate structural scopes.
* Contract and compatibility evidence for depended-upon interfaces.
* Acceptance evidence for stakeholder-visible obligations.
* Exploratory evidence for poorly understood or rapidly changing risks.
* Static, security, and supply-chain analysis where justified.
* Performance, capacity, accessibility, data-quality, privacy, and observability evidence where failure would be material.
* Operational evidence for startup, shutdown, deployment, rollback, restart, failover, backup restoration, degraded operation, and recovery where applicable.

The portfolio shape must follow project risks and architecture. A fixed testing pyramid or universal ratio between scopes is not required.

## 7. Static analysis and security checks

Projects must define the static, security, and supply-chain checks required by their languages, dependencies, threat model, and support policy.

Required checks may include:

* Formatting and linting.
* Type checking.
* Dependency and vulnerability analysis.
* Secret scanning.
* License or policy checks.
* Configuration validation.
* Artifact integrity or provenance checks.

Each required check must have:

* A documented execution cadence.
* A defined failure policy.
* An owner.
* A process for triage, waiver, expiration, and follow-up.

Blocking findings must not be suppressed without documented review.

## 8. Metrics and targets

Metrics are evidence about the testing system; they are not substitutes for test quality or risk coverage.

Before a metric is used for comparison or gating, define:

* The claim or decision it informs.
* Population and denominator.
* Tool and configuration.
* Environment and data.
* Measurement window.
* Baseline and expected variability.
* Threshold rationale.
* Required response.
* Owner.

Relevant metrics may include:

* Feedback latency and suite runtime.
* Flake rate and retry rate.
* Failure localization and diagnostic quality.
* Coverage of identified risks, responsibilities, boundaries, and contracts.
* Code coverage.
* Mutation results.
* Snapshot churn.
* Maintenance burden.
* Performance or resource regressions.

Projects may establish quantitative targets, but values must be project-specific, justified, and periodically reviewed. Improving a metric must not be pursued through tests or assertions that add no defect-detection value.

## 9. Exceptions and waivers

A policy exception must record:

* The requirement being waived.
* The reason the requirement is not currently appropriate or feasible.
* The affected scope and risk.
* Compensating evidence or controls.
* The owner.
* The review or expiration condition.

Temporary disabling of tests, static analysis, or security checks must have a tracked follow-up and must not become an undocumented permanent state.

## 10. Prohibited practices

Tests and test suites must not:

* Rely on arbitrary sleeps to stabilize behavior when explicit synchronization, readiness checks, bounded polling, hooks, or events are available.
* Depend on hidden execution order or undocumented shared mutable state.
* Access production data or mutate production resources unless the test is explicitly designed, authorized, and controlled for that environment.
* Silently ignore failures.
* Leave known flaky tests untriaged indefinitely.
* Chase coverage or other numeric targets with trivial assertions that add no meaningful defect-detection value.
* Use broad snapshots as a substitute for practical semantic assertions.
* Assert unstable implementation details without a documented reason.
* Treat a mocked, faked, or emulated dependency as proof of real integration semantics.
* Casually suppress secret-scanner, vulnerability, static-analysis, or test failures.
* Disable required evidence without a documented exception and follow-up.

Where a prohibition cannot be followed, the exception process in Section 9 applies.

## 11. Detailed procedures

Detailed design, writing, and evaluation guidance is defined in:

* `L3_T1_unit.md`
* `L3_T2_component.md`
* `L3_T3_integration.md`
* `L3_T4_system.md`
* `L3_T5_regression.md`
* `L3_T6_property-based.md`
* `L3_T7_contract.md`
* `L3_T8_non-functional.md`
* `L3_T9_snapshot.md`
* `L3_T10_health_and_metrics.md`

Project-specific commands, tools, directory layouts, markers, thresholds, and runtime budgets belong in project configuration or implementation guidance.
