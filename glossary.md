# Testing Glossary

This document is the canonical terminology reference for this repository. It defines the meanings intended by `Overview.md` and the L1/L2/L3 procedures without imposing a particular tool, language, directory layout, or development workflow.

Testing terminology varies across organizations. A project may adopt narrower or broader local definitions, but it should state them explicitly. When this glossary conflicts with a normative requirement in `Overview.md` or an L1/L2/L3 procedure, the normative document controls.

## Contents

1. Risk, claims, and decisions
2. Classification dimensions
3. Test purposes
4. Evidence and test-design techniques
5. Test doubles and controlled dependencies
6. Test artifacts and organization
7. Execution and result integrity
8. Development workflows
9. Static and supply-chain checks
10. Measurements

## 1. Risk, claims, and decisions

### Claim

A statement that must be true for a product, change, release, deployment, or operating decision to be justified.

Examples include correctness of a transformation, compatibility of an interface, preservation of data during migration, acceptable task completion by users, or recovery within an operational objective.

### Failure mode

A way in which a claim could be false. Failure modes include incorrect logic, missing cases, incompatible schemas, dependency mismatch, race conditions, hostile input, misleading interaction, deployment failure, and incomplete recovery.

### Risk

The combination of uncertainty about a failure mode and the consequences if it occurs. Risk analysis may consider likelihood, impact, detectability, reversibility, exposure, affected users, and available mitigations.

### Evidence

An observation capable of increasing or decreasing confidence in a claim. Evidence may be automated or manual and may include tests, static analysis, formal proof, review, measurement, exploratory work, usability evaluation, production observation, audit, simulation, or incident history.

### Evidence artifact

A retained output used to support a decision, such as a report, log, trace, coverage file, benchmark result, contract-verification record, screenshot, exploratory-session note, or signed attestation.

### Oracle

The rule or source used to determine whether an observed result is acceptable. An oracle may be an explicit expected value, invariant, reference model, independent implementation, schema, stakeholder judgment, standard, baseline, or operational objective.

### Confidence

The degree of justified belief that a claim holds for the decision and conditions under consideration. Confidence is contextual; evidence sufficient for experimentation may be insufficient for broad production use.

### Residual uncertainty

Important uncertainty remaining after the available evidence is considered. Examples include untested environments, unrealistic doubles, limited samples, ambiguous requirements, unsupported user groups, or unexercised recovery paths.

### Risk acceptance

An explicit decision to proceed despite a known residual risk. Risk acceptance should identify the failure mode, rationale, impact, mitigation, owner, and revisit trigger.

### Waiver

A documented, bounded exception to a stated requirement or gate. A waiver should name its scope, owner, rationale, mitigation, and expiration or revisit condition.

### Gate

A rule that blocks or permits a defined decision based on specified evidence. A gate is meaningful only when its inputs, comparability rules, threshold rationale, and response are explicit.

### Pass

The required claims are supported to the confidence level needed for the stated decision, with no unresolved blocking gaps.

### Conditional pass

The decision may proceed only with explicitly accepted conditions, mitigations, owners, and revisit triggers.

### Fail

The available evidence contradicts a required claim, is invalid, or leaves an unaccepted material gap.

### Exploratory finding

A result intended to reduce uncertainty rather than make a pass/fail decision. It may include learned behavior, rejected assumptions, new risks, or questions requiring further evidence.

## 2. Classification dimensions

### Structural scope

The chosen execution boundary whose behavior the test exercises. Structural scope is independent of purpose and technique.

A test may cross several boundaries, but its primary structural scope identifies the boundary whose semantics determine how the evidence should be interpreted. Additional resource, boundary, purpose, and execution classifications may also be recorded.

### Unit test

A test of a small chosen boundary that provides highly localizing feedback. A unit may be a function, class, module, cluster of collaborating objects, or other locally understandable boundary.

A **solitary unit test** replaces collaborators outside the focal unit boundary. A **sociable unit test** retains inexpensive, deterministic collaborators inside the chosen unit boundary.

### Component test

A test of a coherent subsystem through a supported interface. Code inside the component boundary generally collaborates normally; dependencies outside the boundary may be replaced, simulated, or supplied through lightweight real implementations.

### Integration test

A test whose evidential value depends on real semantics across a process, infrastructure, platform, protocol, service, or persistence boundary. Integration scope is about semantic fidelity, not merely the number of modules involved.

### System test

A test of the assembled product through a user-visible or operator-visible boundary, such as an installed CLI, public API, browser interface, deployed service, or packaged application.

### End-to-end test

A system test that traverses a complete workflow across the boundaries necessary to represent real use.

End-to-end is relative to the product and decision boundary. Controlled dependencies may still be used when they do not remove the semantics needed by the claim, and the term does not necessarily imply every external production dependency.

### Resource or boundary classification

A label identifying material resources whose use affects isolation, cost, fidelity, or interpretation. Common examples include filesystem, process, database, network, broker, clock, random source, hardware accelerator, third-party service, configuration, platform, and production environment.

### Execution class

A label describing execution properties rather than test meaning. Examples include fast, slow, destructive, hermetic, isolated, quarantined, privileged, or environment-specific.

### Cadence

The event or schedule at which evidence is collected, such as per-edit, pre-commit, pre-merge, scheduled, pre-release, post-deployment, or continuous.

## 3. Test purposes

### Acceptance testing

Testing intended to demonstrate a concrete condition that matters to a stakeholder, user, operator, regulator, or dependent system. Acceptance is a purpose and may be implemented at component, integration, or system scope, or through human evaluation.

### Regression testing

Testing intended to prevent loss of previously established behavior or reintroduction of a known defect. Regression is a reason a test exists, not a structural scope.

### Characterization testing

Testing that records existing behavior of a poorly understood or legacy system before modification. Characterization evidence describes what the system currently does and is not automatically a statement that the behavior is desirable.

### Sanity testing

A narrow check that a specific change, fix, or capability behaves plausibly before broader evaluation proceeds.

### Smoke testing

A small, fast set of checks indicating that critical capabilities are available and the system is suitable for further testing or use.

### Contract testing

Testing intended to verify obligations between a producer and one or more consumers. Contract obligations may include structure, semantics, error behavior, ordering, versioning, compatibility, timing, or artifact identity.

### Consumer-driven contract testing

Contract testing in which consumer expectations are captured as executable interactions and verified by the provider.

### Provider verification

Execution of consumer or shared contract expectations against a provider implementation or artifact.

### Schema testing

Testing that data, messages, APIs, databases, or documents conform to structural constraints such as required fields, types, nullability, relationships, and allowed values. Schema conformance is one form of contract evidence but does not establish full behavioral compatibility.

### Compatibility testing

Testing that behavior remains acceptable across supported versions, consumers, platforms, devices, environments, data formats, or deployment combinations.

### Migration testing

Testing that a schema, data, configuration, or platform transition produces the intended state and preserves required information and behavior.

### Rollback testing

Testing that a system, release, configuration, or migration can return to a previous acceptable state within defined constraints.

### Performance testing

Testing or measurement of latency, throughput, scalability, resource use, responsiveness, or other time- and capacity-related properties under a specified workload and environment.

### Performance regression testing

Comparison intended to detect practically meaningful degradation relative to a valid baseline or objective.

### Load testing

Performance testing under expected or specified demand.

### Stress testing

Testing beyond expected capacity to identify saturation behavior, failure modes, and recovery characteristics.

### Soak testing

Long-duration testing intended to reveal leaks, accumulation, degradation, or instability over time.

### Security testing

Testing intended to evaluate threat-relevant properties, abuse cases, authorization, confidentiality, integrity, availability, unsafe parsing, supply-chain exposure, or other security claims.

### Privacy testing

Testing or review intended to evaluate data minimization, consent, retention, disclosure, anonymization, access, and other privacy obligations.

### Data-quality testing

Testing intended to evaluate data integrity, validity, uniqueness, completeness, freshness, referential consistency, lineage, aggregation correctness, anomaly, or distribution claims.

### Observability testing

Testing intended to verify that logs, metrics, traces, events, health signals, and diagnostics support detection and diagnosis of important behavior and failure.

### Accessibility testing

Evaluation of whether people with relevant disabilities can perceive, understand, navigate, and operate the product under applicable standards and real assistive-technology conditions.

### Usability testing

Evaluation of whether intended users can understand and complete important tasks effectively, including errors, hesitation, recovery, and comprehension.

### Resilience testing

Testing intended to evaluate behavior under dependency degradation, partial failure, overload, interruption, or other adverse conditions.

### Recovery testing

Testing intended to evaluate restoration of service and data after failure, including rollback, restart, failover, backup restoration, and return to a known-good state.

### Operational-readiness testing

Evaluation of deployment, configuration, monitoring, alerting, diagnosis, runbooks, rollback, recovery, and operator action required to operate the system safely.

### Synthetic monitoring

Scheduled or continuous execution of representative transactions against a deployed environment to detect loss of capability, latency degradation, or other production failures.

## 4. Evidence and test-design techniques

### Example-based testing

Testing selected inputs or scenarios against explicit expected outcomes.

### Table-driven testing

Example-based testing in which multiple cases share one test structure and are represented as data.

### Property-based testing

Generation of inputs to evaluate invariants over a broad domain, with shrinking or minimization of failing examples where supported.

### Stateful or state-machine testing

Generation of action sequences against a stateful subject while checking invariants, preconditions, postconditions, or a reference state model.

### Model-based testing

Generation or evaluation of tests from an explicit model of allowed states, transitions, outputs, or behavior.

### Differential testing

Comparison of independent implementations, versions, modes, platforms, or tools using the same inputs to detect disagreement.

### Metamorphic testing

Testing relations between transformed inputs and outputs when a direct expected result is unavailable or expensive to compute.

### Fuzzing

Systematic generation or mutation of malformed, adversarial, random, or coverage-guided inputs to discover crashes, hangs, memory errors, security defects, or invariant violations.

### Snapshot or golden testing

Comparison of a canonicalized output or artifact with a reviewed stored baseline. Snapshot approval is a semantic review, not merely an update operation.

### Mutation testing

Deliberate alteration of implementation behavior to evaluate whether the selected test suite detects the change.

### Fault injection

Controlled introduction of errors, delays, unavailable resources, corrupted responses, or other failures to evaluate handling and recovery.

### Chaos engineering

Hypothesis-driven fault experimentation on a running system, with defined blast radius, stop conditions, observability, and recovery checks.

### Simulation

Use of an executable approximation of a system, dependency, environment, or physical process to generate evidence under controlled conditions.

### Formal verification

Mathematical demonstration that specified properties hold under an explicit formal model and assumptions.

### Static analysis

Analysis of source code, bytecode, configuration, or artifacts without executing the target behavior in the usual runtime environment.

### Abstract interpretation

Static analysis that approximates possible program states using an abstract domain to reason about properties such as ranges, nullability, taint, or reachability.

### Dataflow analysis

Analysis of how values or facts propagate through a program, often used to detect uninitialized values, tainted input, dead code, or resource misuse.

### Exploratory testing

Simultaneous learning, test design, and execution guided by a charter rather than only predefined cases.

### Heuristic evaluation

Review of a system using established principles or prompts to identify likely usability, accessibility, security, or operational problems.

### Counterexample

An input, state, sequence, or condition demonstrating that a claimed property does not hold.

### Shrinking or minimization

Reduction of a failing generated case or execution trace to a smaller reproduction that preserves the failure.

### Reference model

A simpler or independently specified representation of expected behavior used as an oracle.

## 5. Test doubles and controlled dependencies

### Test double

A general term for a controlled replacement or representation of a collaborator used during testing.

### Dummy

A value supplied only to satisfy an interface and not used meaningfully by the behavior under test.

### Stub

A replacement that returns controlled responses to calls made by the subject.

### Spy

A collaborator or wrapper that records interactions for later inspection while optionally retaining real behavior.

### Mock

A replacement configured with interaction expectations that are verified by the test.

### Fake

A simplified but functional implementation of an interface, such as an in-memory repository.

### Simulator

A substitute that attempts to reproduce externally observable behavior or protocols of another system.

### Emulator

A substitute intended to reproduce a platform, device, or execution environment closely enough to run software designed for the original.

### Record/replay

Capture of real interactions followed by deterministic reuse of the captured responses.

### Containerized dependency

A real dependency implementation run in an isolated container or ephemeral environment.

### Shared test environment

A coordinated environment used by multiple tests or teams. It may provide high fidelity but introduces contention, state-management, and comparability risks.

### Dependency injection

Supplying a collaborator, resource, configuration value, clock, or other dependency explicitly rather than constructing or locating it implicitly.

Dependency injection enables control, substitution, observation, and fault injection, especially at external-effect and variability boundaries. It need not be introduced solely to replace inexpensive, deterministic collaborators that remain inside the chosen test boundary.

### Hermetic test

A test whose result depends only on explicitly controlled inputs and resources rather than ambient services, state, time, or ordering.

## 6. Test artifacts and organization

### Fixture

Test setup data, objects, state, or resources supplied to one or more tests. A fixture may be inline, generated, file-backed, or environment-backed.

### Factory

A helper that creates test objects or data with explicit defaults and controlled variation.

### Builder

A composable helper for incrementally constructing complex test objects or scenarios.

### Test data

Inputs, reference outputs, captured artifacts, generated examples, datasets, or environment state used to execute or evaluate tests.

### Canonicalization

Transformation of output into a stable representation by removing or normalizing irrelevant variation before comparison.

### Test harness

The code, configuration, commands, fixtures, environments, collectors, and reporting mechanisms used to execute tests and produce evidence.

### Test suite

A maintained collection of tests selected or grouped for a purpose or workflow.

### Portfolio

The overall combination of evidence types, scopes, techniques, environments, and cadences used by a project.

### Testability

The degree to which a system permits important inputs, states, failures, outputs, and effects to be controlled or observed well enough to obtain useful evidence.

### Test pyramid, trophy, and honeycomb

Heuristic portfolio shapes emphasizing different distributions of test scopes. They are planning metaphors, not universal quality laws.

## 7. Execution and result integrity

### Isolation

The degree to which one test is protected from uncontrolled effects of other tests, shared state, ambient environment, or execution order.

### Determinism

The property that equivalent controlled inputs and conditions produce the same test result.

### Flaky test

A test that produces different pass/fail outcomes without a relevant change in the subject or declared inputs.

Infrastructure, dependency, and harness failures should be distinguished from test nondeterminism where possible.

### Infrastructure failure

A failure of the environment, runner, network, dependency provisioning, credential system, storage, or test platform that prevents valid evidence from being collected without demonstrating that the subject claim is false.

### Harness failure

A defect or invalid state in test setup, control, instrumentation, cleanup, collection, or reporting that makes the resulting evidence incomplete, misleading, or uninterpretable.

### Retry

Re-execution after failure. Retry may collect diagnostic evidence but must not silently redefine an intermittent failure as success.

### Quarantine

Explicit exclusion of unreliable evidence from a gate while remediation is tracked. Quarantined tests cannot support claims that depend on them.

### Complete run

Execution of the full declared selection required for a particular evidence artifact or decision.

### Partial run

Execution of only a subset of the declared selection. A partial result must not overwrite or masquerade as complete evidence.

### Fresh evidence

Evidence collected from the relevant current revision, artifact, configuration, data, and environment within the required time window.

### Comparable evidence

Evidence whose workload, environment, tool configuration, cohort, and collection method satisfy the rules required for valid comparison.

### Failure localization

The degree to which a failing result identifies a narrow behavior, boundary, or cause.

### Diagnostic quality

The usefulness of failure messages, logs, artifacts, context, and reproduction information in distinguishing subject failure from harness, dependency, or environment failure.

### False positive

A result indicating that a failure, violation, or condition exists when the relevant claim is actually satisfied under the defined conditions.

### False negative

A result failing to indicate a failure, violation, or condition that actually exists under the defined conditions.

The meanings of false positive and false negative depend on a sufficiently explicit reference condition or adjudication process.

## 8. Development workflows

### Test-driven development

A development workflow that alternates a failing test, minimal implementation, and refactoring.

### Acceptance-test-driven development

A workflow that establishes concrete stakeholder-facing examples or conditions before or during implementation.

### Behavior-driven development

A collaboration and specification style that describes behavior using domain-oriented examples, often expressed as Givenâ€“Whenâ€“Then scenarios.

### Test-after development

A workflow in which implementation or exploration precedes encoding stable behavior as tests.

### Exploratory prototyping

Use of disposable or promotable experiments, measurements, and observations to reduce uncertainty before committing to a durable implementation.

## 9. Static and supply-chain checks

### Formatter

A tool that rewrites source text into a consistent layout without intending to change behavior.

### Linter

A tool that detects selected stylistic, correctness, maintainability, or suspicious-code patterns.

### Type checker

A tool that evaluates whether values and operations conform to declared or inferred type relationships.

### Dependency scan

Analysis of declared or resolved dependencies for known vulnerabilities, policy violations, unsupported versions, provenance concerns, or licensing constraints.

### Secret scan

Analysis intended to detect credentials, tokens, private keys, or other sensitive values in source, history, configuration, or artifacts.

### Supply-chain verification

Evidence about dependency provenance, integrity, signatures, build process, artifact identity, and allowed sources.

## 10. Measurements

### Line coverage

The proportion of instrumented executable lines observed during a specified test selection for a declared code population.

### Branch coverage

The proportion of instrumented branch outcomes observed during a specified test selection for a declared code population.

### Path coverage

The proportion of paths through a defined path model that are exercised. For general programs, the number of possible paths may be unbounded or computationally impractical, so the denominator must be explicit.

### Requirement or case coverage

The proportion of declared responsibilities, requirements, risks, or logical cases linked to acceptable evidence.

### Mutation score

The proportion of mutants counted in the declared denominator that are detected by the selected evidence.

The definition must state the code cohort, mutation operators, and treatment of invalid, equivalent, uncovered, timed-out, and untested mutants.

### Flake rate

A rate of suspected nondeterministic failures over a defined unit, population, environment, and observation window.

### Defect escape

A defect discovered after the stage at which the organization intended to detect it. Severity, attribution, reporting behavior, exposure, and observation period affect interpretation.

### Baseline

A declared reference distribution, revision, environment, workload, or cohort used for comparison.

### Threshold

A boundary associated with a defined action. A threshold requires technical or product rationale and must account for measurement uncertainty and practical effect.

### Population stability index

A binned measure of distribution difference between a reference and comparison population. Its meaning depends on binning, sample size, reference selection, and operational context.

### Kolmogorovâ€“Smirnov statistic

The maximum difference between two empirical cumulative distributions. Interpretation depends on sample size, independence, multiple comparisons, and the decision being made.

Population stability index and the Kolmogorovâ€“Smirnov statistic are included as examples of statistical comparison measures used in data-quality and drift analysis; they are not universal defaults.

See `L3_T11_metrics.md` before treating any measurement as a gate.
