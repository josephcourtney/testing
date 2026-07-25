---
aliases:
  - Best Practices - Automated Testing
linter-yaml-title-alias: Best Practices - Automated Testing
status: beta
tags: []
title: Best Practices - Automated Testing
---

# Best Practices — Automated Testing

> [!important]
> This document is a **non-normative conceptual reference**. It preserves a broad
> set of practices, definitions, examples, and lifecycle patterns that may be
> useful when designing a project-specific strategy. `Overview.md` defines
> policy, `glossary.md` defines terminology, and the L1/L2/L3 procedures govern
> decisions. When this document sounds prescriptive, read the statement as a
> practice to evaluate unless a normative document independently requires it.

> [!definition] Definition: Automated Testing
> Automated testing is the use of software tools to execute checks and collect
> evidence automatically. Automated evidence may verify specified behavior,
> search for counterexamples, measure properties, inspect artifacts, or monitor
> a deployed system. It is one evidence source among testing, review, formal
> analysis, exploratory work, usability evaluation, measurement, and production
> observation.

## Core principles

The following principles are useful design prompts rather than independent proof
of quality:

* **Isolation and control** — protect results from uncontrolled shared state,
  ordering, ambient services, time, randomness, and configuration. Isolation
  does not require replacing inexpensive deterministic collaborators that belong
  inside the chosen boundary.
* **Semantic fidelity** — preserve the real behavior needed by the claim. A fast
  fake is not useful if it removes the failure mode under examination.
* **Efficiency** — keep evidence timely enough that it affects editing, merge,
  release, and operational decisions. Different evidence may belong at different
  cadences.
* **Clarity** — make the claim, inputs, oracle, boundary, and failure easy to
  understand.
* **Purpose** — know whether an item exists for acceptance, regression, contract,
  exploration, performance, security, observability, or another reason.
* **Maintainability** — avoid unnecessary coupling, hidden setup, duplicated
  scenarios, noisy snapshots, and obsolete obligations.
* **Diagnostics** — retain enough context to distinguish product, dependency,
  environment, configuration, and harness failure.
* **Diligence** — investigate failures, flakes, unexplained metric changes, and
  weak oracles rather than normalizing them.
* **Practicality** — prioritize evidence according to impact, likelihood,
  uncertainty, reversibility, and the cost of learning.
* **Evidence integrity** — distinguish complete from partial runs, fresh from
  stale results, and comparable from non-comparable measurements.

## A common lifecycle pattern

The sequence below is one common pattern, not a required project lifecycle.
Material risks apply whenever they arise. A prototype handling sensitive data
may need strong security and privacy controls; a production utility without a
network boundary does not need fictitious service integration tests.

### Always or continuously

Common recurring practices include:

* run appropriate static analysis, such as formatters, linters, and type checkers,
* run threat-relevant secret, dependency, vulnerability, license, and
  supply-chain checks,
* keep test and metric artifacts distinguishable by revision, environment,
  selection, and freshness,
* investigate flakes, degraded diagnostics, and growing feedback latency,
* revisit the risk model when users, dependencies, data, scale, threats, or
  operating conditions change.

The exact tools and cadence are project decisions.

### Exploration and prototyping

A common approach is to:

* clarify goals and reduce uncertainty,
* build a prototype from a fuzzy goal,
* iterate, evaluate, and analyze the prototype,
* formalize useful discoveries as acceptance conditions, invariants, models, or
  constraints,
* begin data validation, metric tracking, or baseline capture when feasibility
  depends on them,
* discard or deliberately promote prototype code and tests.

Exploratory scripts and measurements may be more valuable than a conventional
unit suite at this stage. Material external, security, data, or safety risks
still require credible evidence.

### Development

A common development pattern is to:

* scaffold durable production code from validated assumptions,
* define stakeholder-visible examples or acceptance conditions,
* implement local behavior with unit and component evidence,
* add contract evidence for independently consumed boundaries,
* refactor while behavior remains protected,
* add snapshots when a large stable representation benefits from reviewed diffs,
* add data freshness, referential integrity, aggregation, anomaly, backfill,
  schema-evolution, lineage, or model checks where applicable,
* add observability hooks and verify operator-critical signals,
* begin retaining test-result and metric history.

Teams may use TDD, acceptance-test-driven development, test-after development,
or mixed exploratory workflows. TDD is a development technique, not a universal
quality requirement.

### Stabilization and polishing

As interfaces and workflows stabilize, projects often increase:

* real-dependency integration evidence,
* installed-artifact and system evidence,
* contract and compatibility verification,
* exploratory evaluation of ambiguous and high-risk areas,
* usability and accessibility evaluation,
* performance measurement and capacity exploration,
* a small reliable smoke selection for frequent gating,
* suite-health assessment and diagnostic cleanup.

Do not postpone a material integration, usability, security, or performance risk
until this stage merely because it appears here in the common sequence.

### Hardening and release

Common hardening activities include:

* focused regression tests for learned failure modes,
* migration and rollback testing,
* supported-version and platform compatibility testing,
* mutation testing to evaluate suite sensitivity,
* fuzzing and malformed-input campaigns,
* security and privacy assessment tied to threats and data flows,
* fault injection and controlled resilience testing,
* deployment, observability, restoration, and recovery exercises,
* validation of quantitative gates, baselines, and comparability rules.

These activities are selected from release claims and risk. They are not a
mandatory checklist for every product.

### Maintenance and operation

Common maintenance practices include:

* synthetic monitoring of critical deployed transactions,
* change-impact and incident-derived regression analysis,
* contract and compatibility revalidation after dependency or platform change,
* performance, capacity, data, and model drift monitoring,
* periodic rollback, restoration, failover, and runbook exercises,
* test-suite health, flake, latency, defect, and maintenance-cost review,
* retiring stale evidence and updating obsolete baselines,
* returning to development or stabilization practices when requirements or
  threats change.

A bug fix may begin with a narrow sanity check and result in durable regression,
contract, property, integration, monitoring, or operational evidence.

## Classification dimensions

Tests should not be forced into one hierarchy that combines scope, purpose,
technique, resources, and cadence.

### Structural scope

* **Unit tests** exercise a small chosen boundary and provide highly localizing
  feedback. A unit may be a function, class, module, or cluster of collaborating
  objects. Solitary tests replace outside collaborators; sociable tests retain
  inexpensive deterministic collaborators inside the unit.
* **Component tests** exercise a coherent subsystem through a supported
  interface. Internal implementation normally collaborates for real, while
  outside dependencies may be controlled or represented by lightweight real
  implementations.
* **Integration tests** depend for their evidential value on real semantics
  across a persistence, process, protocol, platform, framework, service, or
  infrastructure boundary.
* **System tests** exercise the assembled product through a user- or
  operator-visible boundary.
* **End-to-end tests** are system tests that traverse a complete representative
  workflow relative to a declared product boundary. They need not use every
  external production dependency.

Static analysis is an evidence technique rather than a structural test scope.
Contract, acceptance, regression, smoke, performance, and security describe
purposes rather than structural levels.

### Purpose

* **Acceptance tests** demonstrate concrete conditions that matter to a user,
  operator, stakeholder, regulator, or dependent system.
* **Regression tests** protect established behavior or a learned failure mode.
* **Characterization tests** record existing behavior before modification without
  automatically endorsing it.
* **Sanity tests** provide narrow plausibility checks for a change or fix before
  broader evaluation.
* **Smoke tests** provide a small critical-capability selection indicating that a
  build, deployment, or environment is suitable for further testing or use.
* **Compatibility tests** evaluate supported versions, platforms, devices,
  browsers, consumers, data formats, or environments.
* **Contract tests** verify producer-consumer obligations, including structure,
  semantics, errors, ordering, versioning, timing, and artifact identity.
* **Schema tests** verify structural constraints but do not by themselves prove
  behavioral compatibility.
* **Migration tests** verify intended state transitions for data, configuration,
  schema, or platform changes.
* **Rollback tests** verify return to a previous acceptable state and any limits
  on reversibility.
* **Performance tests** evaluate latency, throughput, responsiveness, capacity,
  scalability, or resource use under a defined workload and environment.
* **Performance regression tests** compare against a valid baseline or objective
  and require practically meaningful thresholds.
* **Load tests** exercise expected or specified demand.
* **Stress tests** exceed expected capacity to reveal saturation, failure, and
  recovery behavior.
* **Soak tests** run for long durations to reveal leaks, accumulation, and
  degradation.
* **Security tests** evaluate threat-relevant properties including authentication,
  authorization, unsafe parsing, injection, confidentiality, integrity,
  availability, and supply-chain risk.
* **Vulnerability scans** search source, dependencies, artifacts, or deployed
  systems for known or rule-defined security issues.
* **Secret scans** detect credentials, keys, tokens, or sensitive values in code,
  history, configuration, and artifacts.
* **Privacy-impact tests and reviews** evaluate data purpose, minimization,
  consent, access, retention, deletion, disclosure, anonymization, and privacy
  mechanisms such as differential-privacy budgets where applicable.
* **Supply-chain verification** evaluates dependency provenance, integrity,
  signatures, builds, allowed sources, licensing, and known vulnerabilities.
* **Service/API tests** evaluate the functionality, reliability, errors,
  authorization, and contract compliance of a public service interface; their
  structural scope depends on the real boundary exercised.
* **Data-quality tests** evaluate validity, completeness, consistency, freshness,
  uniqueness, referential integrity, lineage, aggregation, anomaly, and
  distribution claims.
* **Database tests** evaluate query, schema, constraint, transaction, indexing,
  trigger, migration, integrity, or performance behavior. `database` is also a
  useful resource classification; the structural scope depends on the boundary.
* **Queries and schema tests** verify expected tables, indexes, constraints,
  query results, plans, and schema evolution.
* **Usability tests** evaluate whether intended users can understand and complete
  tasks, including error and recovery behavior.
* **Accessibility tests** evaluate whether people with relevant disabilities can
  perceive, navigate, understand, and operate the product. Automated conformance
  scans are partial evidence, not complete accessibility evaluation.
* **Internationalization and localization tests** evaluate locales, encodings,
  text expansion, formats, translation, layout, and culturally dependent
  behavior.
* **Observability tests** verify that logs, metrics, traces, health signals, and
  diagnostics support detection and diagnosis.
* **Resilience tests** evaluate behavior under partial failure, overload,
  interruption, and dependency degradation.
* **Recovery tests** evaluate restart, rollback, failover, restoration, and
  return to a known-good state.
* **Synthetic monitoring** repeatedly executes representative deployed
  transactions to detect loss of capability, latency degradation, or downtime.
* **Model and data drift detection** observes changes in input distributions,
  output distributions, calibration, or predictive performance. Generic PSI,
  KS, or accuracy thresholds are not portable defaults.

### Techniques

* **Example-based testing** checks selected scenarios against explicit expected
  outcomes.
* **Table-driven testing** represents several examples as data under one test
  structure.
* **Property-based testing** generates inputs and checks invariants, with
  shrinking or minimization where supported.
* **Stateful or state-machine testing** generates action sequences and checks
  state models, preconditions, postconditions, and invariants.
* **Model-based testing** derives or evaluates behavior from an explicit model of
  states, transitions, or outputs.
* **Differential testing** compares independent implementations, versions,
  backends, modes, or platforms using the same inputs.
* **Metamorphic testing** checks expected relations between transformed inputs and
  outputs when exact expected values are unavailable.
* **Fuzzing** generates or mutates malformed, adversarial, random, or
  coverage-guided inputs to find crashes, hangs, security defects, and invariant
  violations.
* **Mutation testing** deliberately changes implementation behavior to evaluate
  whether the selected suite detects the change.
* **Snapshot or golden testing** compares canonicalized output with a reviewed
  stored baseline.
* **Fault injection** deliberately introduces controlled failures, errors,
  corruption, or latency.
* **Chaos engineering** performs hypothesis-driven fault experiments with
  controlled blast radius, stop conditions, observability, and recovery checks.
* **Simulation and emulation** provide controlled approximations of systems,
  devices, protocols, environments, or physical processes.
* **Formal verification** proves specified properties under an explicit model and
  assumptions.
* **Exploratory testing** combines learning, test design, and execution under a
  charter.

## Static and build-time checks

* **Linting** detects selected correctness, maintainability, stylistic, and
  suspicious-code patterns.
* **Formatting** rewrites code into a consistent layout without intending to
  change behavior.
* **Type checking** evaluates declared or inferred type relationships. It may be
  static or dynamic, but the repository's static-analysis policy should state
  the actual tool, scope, and failure handling.
* **Dependency scanning** evaluates declared or resolved dependencies for known
  vulnerabilities, unsupported versions, provenance, policy, or licensing
  concerns.
* **Artifact validation** verifies package metadata, contents, signatures,
  digests, entry points, dependency declarations, and installability.

These checks are valuable evidence about their configured rules and inputs. A
passing tool does not establish properties it does not analyze.

## Development and portfolio conventions

The following choices can be useful when a project states why it adopted them:

* test-driven, test-after, or acceptance-test-driven development,
* solitary or sociable unit testing,
* Arrange–Act–Assert, Given–When–Then, or domain-specific structures,
* source-mirroring, scope-oriented, feature-oriented, or colocated directories,
* test pyramids, trophies, honeycombs, or other portfolio heuristics,
* mocks, fakes, simulators, emulators, containers, or shared environments,
* per-edit, pre-commit, pre-merge, scheduled, release, or production cadence.

No workflow, directory layout, portfolio shape, marker, or tool is a substitute
for connecting claims, failure modes, evidence, uncertainty, and decisions.
