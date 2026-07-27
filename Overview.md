# Testing Policy

## 1. Purpose

Testing exists to provide justified confidence in claims about a system.

A project must connect:

1. the claims it intends to make,
2. the failure modes that could invalidate those claims,
3. evidence capable of detecting those failures,
4. the confidence required for the current decision, and
5. the cost and limits of obtaining that evidence.

No test type, metric, lifecycle stage, portfolio shape, development workflow, or
tool is a substitute for this connection.

This document defines project-wide policy for selecting, designing, executing,
interpreting, and recording testing evidence. Detailed procedures for
individual test scopes, purposes, techniques, evidence forms, and lifecycle
profiles belong in the corresponding L1, L2, and L3 documents.

### 1.1 Terminology and implementation guidance

`glossary.md` is the canonical terminology reference for this policy and the
L1, L2, and L3 procedures. If a glossary definition conflicts with a normative
requirement, this policy or the applicable procedure controls.

`automated_testing.md` is non-normative conceptual reference material. It
preserves a broad range of practices, lifecycle patterns, alternatives, and
tradeoffs; those examples are not universal requirements.

`python_testing.md` is non-normative Python and pytest implementation guidance.

Project-specific commands, markers, thresholds, directory layouts, tool
configurations, runtime budgets, support matrices, and measurement cohorts
belong under `example_project/` or in the adopting project's own documentation.
Historical assessments belong under `case_study/`.

Use **must** for requirements and **should** for strong recommendations.

## 2. Core requirements

A testing strategy must:

* identify material product, technical, operational, security, privacy, data,
  accessibility, and usability risks,
* identify critical responsibilities, invariants, boundaries, contracts, user
  journeys, and operator journeys,
* select evidence that is sensitive to the relevant failure modes,
* keep feedback timely enough that the evidence is actually used,
* make failures reproducible and diagnosable,
* distinguish measured facts from assumptions, inference, exploratory findings,
  and risk acceptance,
* distinguish complete from partial or selected evidence,
* distinguish fresh from stale evidence,
* distinguish comparable from non-comparable observations,
* distinguish source-tree behavior from installed-artifact behavior where
  packaging is a claim,
* prevent selected, stale, quarantined, or non-comparable results from being
  represented as complete trusted evidence,
* record material waivers with an owner, rationale, mitigation, and expiry or
  revisit trigger,
* maintain testing, measurement, and analysis infrastructure as production
  assets when decisions depend on them.

A project must not claim confidence merely because a suite passes, a coverage
or mutation target is met, a named inventory of test levels exists, or a
preferred development workflow was followed.

## 3. Risk and evidence model

For each material change, release, deployment, continued-operation, or
risk-acceptance decision, record the following where relevant.

### 3.1 Decision

State the decision the evidence must support, such as:

* exploration or prototype continuation,
* merge,
* internal or beta use,
* production release,
* deployment or staged rollout,
* continued operation,
* explicit risk acceptance.

Evidence sufficient for one decision may be insufficient for another.

### 3.2 Claim

What must be true?

Examples include:

* a parser preserves documented semantics,
* an API remains compatible with deployed consumers,
* a migration preserves data and supports rollback,
* a CLI installed from the built artifact behaves as documented,
* a critical workflow remains within its latency objective,
* an authorization boundary fails closed,
* intended users can understand and complete a critical task,
* operators receive sufficient signals to diagnose and recover from failure.

### 3.3 Failure mode

How could the claim be false?

Consider:

* incorrect logic,
* omitted cases,
* invalid state transitions,
* boundary mismatches,
* schema or contract drift,
* configuration drift,
* dependency behavior,
* process, platform, framework, or protocol differences,
* concurrency and race conditions,
* resource exhaustion,
* hostile or malformed input,
* authentication or authorization failure,
* privacy leakage or inappropriate retention,
* data corruption, staleness, duplication, or aggregation error,
* human misunderstanding,
* inaccessible interaction,
* packaging or deployment failure,
* monitoring or diagnostic failure,
* rollback, restoration, failover, or recovery failure.

### 3.4 Consequence and exposure

Where useful, record:

* affected users, operators, consumers, systems, or data,
* impact and severity,
* likelihood or exposure,
* detectability,
* reversibility,
* containment, mitigation, and rollback options.

Risk is not reduced merely because the corresponding defect is difficult to
test. The difficulty becomes part of the residual uncertainty and decision.

### 3.5 Evidence

What observation would detect or meaningfully constrain the failure with useful
sensitivity?

Evidence may include:

* automated example-based tests,
* property-based, model-based, differential, metamorphic, or fuzz testing,
* static analysis,
* formal methods,
* code or design review,
* exploratory sessions,
* usability or accessibility studies,
* simulations and emulations,
* audits and penetration testing,
* measurements and benchmarks,
* production observations and synthetic monitoring,
* incident, support, and defect history,
* demonstrations and stakeholder evaluation.

For each evidence source, identify:

* the claim and failure mode it addresses,
* structural scope, purpose, technique, resources, and cadence,
* subject revision and artifact,
* environment, platform, configuration, dependencies, and data,
* whether the result is complete or partial,
* freshness and comparability,
* assumptions and limitations.

### 3.6 Confidence

State the confidence required for the decision and why the selected evidence is
sufficient or insufficient.

Confidence is contextual. It may depend on:

* consequence and exposure,
* evidence sensitivity and independence,
* environmental fidelity,
* sample size and natural variation,
* breadth of supported users, platforms, versions, and configurations,
* reversibility and available mitigation,
* evidence age and expected rate of decay.

### 3.7 Residual uncertainty

Record important limitations, including:

* untested conditions,
* unrealistic or unverified doubles,
* missing environments or compatibility cells,
* unsupported users or assistive technologies,
* insufficient sample sizes,
* non-comparable measurements,
* ambiguous requirements,
* unexplored areas,
* assumptions about data, hardware, dependencies, scale, or operation,
* risks accepted rather than eliminated.

## 4. Classification model

Test labels describe independent dimensions. Projects must not force structural
scope, purpose, technique, resource use, execution characteristics, and cadence
into one mutually exclusive hierarchy.

### 4.1 Structural scope

When scope markers are used, an automated behavior test should identify one
primary structural scope:

* **unit** — a small chosen boundary with highly localizing failures,
* **component** — a coherent subsystem exercised through a supported interface,
* **integration** — behavior whose evidential value depends on real semantics
  across a persistence, process, protocol, platform, framework, service, or
  infrastructure boundary,
* **system** — the assembled product exercised through a user- or
  operator-visible boundary.

The primary scope is the boundary whose semantics determine how the evidence
should be interpreted. Additional resource or crossed-boundary labels may be
recorded when useful.

Scope describes the executed boundary, not the test's purpose. The size of a
unit is a project convention; it need not be a single function or class.

An **end-to-end test** is a system test that traverses a complete representative
workflow relative to a declared product boundary. It does not necessarily use
every external production dependency.

### 4.2 Resource and boundary use

Declare material resources or boundaries when they affect isolation, cost,
fidelity, selection, or interpretation, including:

* filesystem,
* process,
* database,
* network,
* broker,
* clock or scheduler,
* random source,
* external service,
* hardware or accelerator,
* operating system or platform,
* framework or runtime,
* configuration or environment,
* production-derived data,
* production environment.

Resource use does not determine structural scope by itself. A temporary file
may be inside a unit or component boundary; a process may be part of a component
contract; a database may be lightweight component state or a real integration
boundary depending on the semantics required.

### 4.3 Purpose

Purposes may be combined with any suitable structural scope:

* acceptance,
* regression,
* characterization,
* sanity,
* contract,
* schema conformance,
* smoke,
* compatibility,
* migration,
* rollback,
* security,
* privacy,
* performance,
* data quality,
* observability,
* accessibility,
* usability,
* resilience,
* recovery,
* operational readiness,
* synthetic monitoring.

For example, a contract test may be component-, integration-, or system-scoped.
Regression describes why a test exists, not how much of the system it executes.
Smoke describes a small critical-capability selection, not necessarily a system
scope. Acceptance describes a stakeholder-relevant purpose and may include
human evaluation.

### 4.4 Technique

Techniques include:

* example-based testing,
* table-driven testing,
* property-based and generative testing,
* state-machine or model-based testing,
* differential testing,
* metamorphic testing,
* fuzzing,
* mutation testing,
* snapshot or golden testing,
* fault injection,
* chaos engineering,
* simulation and emulation,
* formal verification,
* static analysis,
* exploratory testing,
* heuristic evaluation.

Techniques must be selected according to the failure modes they can reveal.
No technique is confined to one structural scope unless its required semantics
make that restriction explicit.

### 4.5 Execution and cadence

Projects may classify evidence by execution properties or scheduling, such as:

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
* hermetic,
* isolated,
* privileged,
* environment-specific,
* quarantined.

Cadence must be selected according to evidence value, cost, rate of decay, and
required feedback latency. No test type or check is universally required at
every cadence.

## 5. Evidence selection

Evidence must be selected from risk and architecture rather than from a
universal inventory.

Examples:

* Pure transformation risk often favors example and property tests at unit or
  component scope.
* Stateful stores, protocols, schedulers, and workflows may require generated
  action sequences and reference models.
* SQL, transaction, serialization, authentication, retry, and protocol risks
  require evidence against real semantics.
* Published interfaces require explicit compatibility obligations and provider
  or consumer verification where applicable.
* Packaging and deployment claims require exercising the built artifact outside
  the source checkout.
* User-journey claims require acceptance or system evidence.
* Ambiguous requirements require exploratory or collaborative evaluation, not
  only automated checks.
* Performance, security, privacy, accessibility, usability, data quality, and
  operability require dedicated evidence whenever failure would be material.
* Recovery claims require evidence for restart, rollback, failover, restoration,
  degraded operation, data consistency, and observability where applicable.
* Human judgment must be retained when automation would discard essential
  comprehension, usability, accessibility, or operational information.

A lifecycle profile may increase required confidence, enforcement,
environmental fidelity, breadth, cadence, ownership, or recordkeeping. It must
not defer an already-material risk merely because a named profile has not been
reached.

A project must not rely on one scope, technique, metric, portfolio shape, or
automation percentage as a substitute for risk-appropriate evidence.

## 6. Test design

Tests should:

* assert observable behavior, invariants, state transitions, or explicit
  contracts,
* fail for a reason connected to the risk they address,
* use the least costly scope that preserves the relevant semantics,
* provide enough diagnostic context to distinguish product, dependency,
  environment, configuration, and harness failure,
* identify relevant input, state, environment, resource, and boundary
  conditions,
* avoid incidental assertions that do not increase failure sensitivity,
* state or reveal the oracle independently of the implementation where
  practical,
* retain minimized counterexamples and traces for generated failures,
* remain understandable enough that future maintainers can interpret failure.

Tests must not be optimized solely for low scope. Moving a test downward is
beneficial only if it preserves sensitivity to the targeted failure mode.
Moving a test upward is beneficial only if the broader boundary adds semantics
needed by the claim.

### 6.1 Isolation and realism

Isolation and realism must be balanced according to the claim and risk being
tested.

Tests should:

* retain real collaborators when they are cheap, deterministic, and part of the
  chosen boundary,
* replace collaborators when control, speed, determinism, rare-state creation,
  or fault injection is needed,
* use controlled substitutes when they improve evidence without removing the
  semantics under examination,
* prefer simple fakes and stubs when interaction verification adds no value,
* use mocks when the interaction itself is contractual,
* pair consequential doubles with contract, integration, or compatibility
  evidence,
* use real dependencies or representative environments when substitutes cannot
  provide valid evidence,
* document differences between simulations, test environments, and production.

A fake, mock, simulator, emulator, stub, recorded response, or in-memory
implementation must not be treated as proof of behavior that depends on the
real system it replaces.

### 6.2 Assertions and diagnostics

Assertions should target stable, externally meaningful behavior.

Avoid assertions on:

* private state,
* incidental call sequences,
* unstable formatting,
* non-contractual log text,
* implementation-specific ordering,
* environment-specific paths or identifiers,

unless those details are the explicit subject of the test.

Failures must provide enough context to identify:

* the violated claim or obligation,
* relevant inputs and state,
* subject artifact and version,
* environment and dependency identity,
* exercised boundary,
* whether the failure likely belongs to the subject, dependency, environment,
  configuration, or harness.

### 6.3 Configuration and environment

Behavior that varies across supported configuration, environment, platform,
feature flags, deployment modes, hardware, runtime, locale, timezone, or
compatibility versions must have representative evidence.

The selected combinations should be justified by support commitments, usage,
architecture, and risk. Exhaustive matrices are not required unless the
combinations are themselves contractual.

Import-time configuration and startup behavior may require a subprocess or
installed-artifact harness to prevent state leakage and to preserve the real
semantics.

### 6.4 Time, randomness, and concurrency

Tests should:

* use explicit clocks or framework-supported time control for business-time
  behavior,
* use monotonic real time only when timing or scheduling semantics are the
  subject,
* avoid arbitrary sleeps when events, barriers, queues, readiness checks,
  callbacks, or bounded polling are available,
* record seeds or minimized examples when generated randomness is involved,
* avoid dependence on ambient global random state,
* deadline every wait,
* propagate background exceptions,
* clean up threads, tasks, processes, and resources,
* repeat or systematically explore schedules when race risk is material.

### 6.5 Test data and fixtures

Use the simplest representation that keeps the behavior legible.

* Inline compact values when they make the case clearer.
* Use factories or builders for complex domain objects.
* Store large static payloads when file identity matters.
* Generate data when broad variation is useful.
* Keep fixtures focused and composable.
* Avoid fixtures that hide the behavior behind extensive implicit setup.
* Make shared mutable fixture reset and ownership explicit.
* Protect sensitive or production-derived data with authorization, minimization,
  redaction, and retention controls.

## 7. Development and organization conventions

The following are selectable conventions, not universal requirements:

* test-driven development,
* test-after development,
* acceptance-test-driven development,
* behavior-driven collaboration,
* exploratory prototyping,
* solitary or sociable unit testing,
* Arrange–Act–Assert, Given–When–Then, or another readable structure,
* source-mirroring, scope-oriented, feature-oriented, or colocated test
  directories,
* mocks, fakes, simulators, emulators, containers, or shared test environments,
* a pyramid, trophy, honeycomb, or another portfolio shape,
* one test per assertion or several assertions for one conceptual behavior.

A project may standardize any of these when doing so improves collaboration.
The standard must state its purpose and must not be treated as proof of test
quality.

Directory layout is a navigation aid, not the complete meaning of a test.
Markers or metadata may encode independent dimensions when projects need
selection, reporting, or governance.

## 8. Tooling and execution integrity

Projects should provide named commands for common workflows and should use
strict configuration where silent misconfiguration would invalidate evidence.

Common workflows may include:

* narrow editing-loop tests,
* broad fast tests,
* complete trusted tests,
* integration and system tests,
* exact installed-artifact tests,
* performance measurement,
* mutation campaigns,
* compatibility-cell export and aggregation,
* portfolio-health recording,
* release checks.

A testing workflow must distinguish:

* complete from selected or partial runs,
* fresh from stale evidence,
* source-tree behavior from installed-artifact behavior,
* comparable from non-comparable environments,
* deterministic failures from suspected flakes,
* measurements from release gates,
* product failures from dependency, harness, configuration, or infrastructure
  failures,
* diagnostic reruns from trusted gate results,
* quarantined tests from evidence supporting a claim.

Retries may collect diagnostic evidence but must not silently convert
nondeterminism into success.

Quarantine must be:

* explicit,
* owned,
* time-bounded,
* excluded from claims it cannot support,
* run separately when useful for diagnosis,
* removed when the evidence is repaired or no longer relevant.

Static, security, and supply-chain checks must be selected according to
language, dependencies, threat model, deployment context, and support policy.
Required checks may include:

* formatting and linting,
* type checking,
* import or architecture checks,
* dead-code or complexity analysis,
* dependency and vulnerability analysis,
* secret scanning,
* license or policy checks,
* configuration validation,
* build and package validation,
* artifact integrity or provenance checks.

Each required check must have:

* a documented scope and cadence,
* a defined failure policy,
* an owner,
* a triage and waiver process,
* explicit handling for false positives and unsupported conditions.

## 9. Measurement policy

No repository-wide numeric target is universal. A metric may influence a
decision only after it has the complete specification required by **L3-T11**:
decision, claim, population, denominator, method, identity and comparability,
uncertainty, threshold rationale, response, owner, and review trigger.

Coverage establishes execution, not correctness. Mutation, flake, performance,
defect, incident, drift, and maintenance measures are meaningful only for their
declared cohorts and conditions. Generic thresholds are not portable defaults.

Improving a metric must not be pursued through tests or assertions that add no
meaningful defect-detection value or that distort behavior to satisfy the
measurement.

Use **L3-T10** for evidence-portfolio health and **L3-T11** for metric design,
validation, thresholds, and interpretation.

## 10. Lifecycle profiles

Lifecycle profiles in `L2_*.md` establish default confidence and governance
expectations:

* **prototype (L2-P1)** — reduce important uncertainty without unnecessary
  ceremony while addressing already-material risk,
* **development / alpha (L2-P2)** — make changed responsibilities and known
  acceptance conditions executable while preserving rapid feedback,
* **stabilization / beta (L2-P3)** — validate critical boundaries,
  compatibility, user journeys, artifacts, and portfolio health,
* **production (L2-P4)** — require release evidence, operational readiness,
  enforcement, and explicit residual risk,
* **maintenance (L2-P5)** — protect learned behavior, reassess changed claims,
  revalidate affected boundaries, and use operational evidence.

Risk overrides these defaults in both directions.

A prototype handling sensitive data may require production-strength security
controls. A mature local utility with no external integrations does not need
fictitious integration tests. More than one profile may apply to a decision,
such as a production hotfix during maintenance.

## 11. Exceptions and waivers

A policy exception or waiver must record:

* the requirement being waived,
* the reason it is not currently appropriate or feasible,
* the affected claim, scope, and risk,
* affected users, operators, data, systems, or obligations,
* compensating evidence or controls,
* rollout, monitoring, containment, rollback, or recovery conditions,
* the owner,
* the expiry date or revisit trigger,
* the conditions for removal.

Temporary disabling of tests, static analysis, security checks, or required
evidence must have a tracked follow-up and must not become an undocumented
permanent state.

Blocking findings must not be suppressed without documented review.

## 12. Prohibited practices

Tests and testing workflows must not:

* rely on arbitrary sleeps when explicit synchronization, readiness checks,
  bounded polling, hooks, events, barriers, or queues are available,
* depend on hidden execution order or undocumented shared mutable state,
* use unbounded waits,
* access production data or mutate production resources unless explicitly
  designed, authorized, minimized, and controlled for that environment,
* silently ignore failures,
* allow retries to conceal nondeterministic behavior,
* leave known flaky tests untriaged indefinitely,
* represent selected, partial, stale, quarantined, or non-comparable evidence as
  complete trusted evidence,
* chase coverage, mutation, or other numeric targets with trivial assertions,
* use broad snapshots as a substitute for practical semantic assertions,
* assert unstable implementation details without a documented reason,
* treat doubles as proof of real integration semantics,
* treat source-tree tests as proof that the built package works,
* compare measurements from incompatible workloads or environments as one
  series,
* casually suppress secret-scanner, vulnerability, static-analysis, warning, or
  test failures,
* disable required evidence without a documented waiver and follow-up,
* claim accessibility from an automated scanner alone,
* claim recovery because a backup or rollback command completed without
  validating usable state.

Where a prohibition cannot be followed, the exception process in Section 11
applies.

## 13. Required records

For material decisions, retain the assessment record defined by **L1 Section
9**, supplemented by the outputs required by each invoked L3 procedure. That
record is the canonical schema for decision, identity, selection, results,
limitations, waivers, and residual uncertainty. Its form may be lightweight for
low-risk work and more formal for high-impact or regulated work.

## 14. Detailed procedures

Detailed design, writing, execution, evaluation, and output guidance belongs in:

* **L1** — assessment and routing,
* **L2-P1** — prototype profile,
* **L2-P2** — development / alpha profile,
* **L2-P3** — stabilization / beta profile,
* **L2-P4** — production profile,
* **L2-P5** — maintenance profile,
* **L3-T1** — unit testing,
* **L3-T2** — component testing,
* **L3-T3** — integration testing,
* **L3-T4** — system testing,
* **L3-T5** — regression testing,
* **L3-T6** — generative, property, model, differential, and fuzz testing,
* **L3-T7** — contract and compatibility testing,
* **L3-T8** — performance, security, privacy, data, and observability evidence,
* **L3-T9** — snapshot and golden testing,
* **L3-T10** — evidence-portfolio health,
* **L3-T11** — metric design and validation,
* **L3-T12** — acceptance testing,
* **L3-T13** — exploratory testing,
* **L3-T14** — usability and accessibility testing,
* **L3-T15** — operational, resilience, and recovery testing.

This policy controls when a procedure conflicts with a project convention,
non-normative conceptual reference, implementation guide, or example.
