# Best Practices — Automated Testing

> This is a non-normative conceptual reference. `Overview.md` defines policy,
> `glossary.md` defines terminology, `L1.md` defines assessment and routing, and
> L2/L3 define the applicable procedures.

## Purpose of this reference

Automation is valuable when repeated execution produces evidence quickly,
consistently, and with enough diagnostic detail to influence a decision. It is
not a substitute for review, exploration, usability work, accessibility work,
threat analysis, operational observation, or judgment.

This document focuses on the choices behind an automated portfolio: what to
automate, where to place the boundary, how much fidelity to buy, and how to keep
the result trustworthy. Canonical definitions are intentionally not repeated;
use `glossary.md`.

## Core tradeoffs

### Detection versus localization

A broad test may detect an assembled-product failure that narrow tests cannot,
but take longer to identify the mechanism. A narrow test may localize a logic
error immediately while remaining insensitive to packaging, protocol, or
deployment behavior.

Use the smallest boundary that preserves the failure semantics required by the
claim, then add broader evidence for material semantics that the smaller
boundary omits. The goal is neither maximal isolation nor maximal realism.

### Fidelity versus control

Real dependencies preserve behavior that doubles can erase: SQL semantics,
filesystem rules, serialization, process startup, TLS, retries, or packaging.
Doubles make rare failures, clocks, responses, and adverse sequences cheap to
control.

Choose per boundary. A controlled fake is strong evidence about the behavior it
faithfully models and weak evidence about everything it removes. Pair it with
real-boundary evidence when the removed semantics matter.

### Breadth versus oracle strength

Generated inputs, fuzz campaigns, broad workflows, and snapshots can explore or
observe a wide surface. Their value still depends on an oracle that detects a
meaningful failure. A narrow semantic assertion may support a stronger claim
than a large output comparison whose changes are routinely approved.

Prefer explicit properties and invariants. Use broad comparisons when the
artifact itself is the contract, canonicalize irrelevant variation, and make
review ownership clear.

### Speed versus decision coverage

Fast feedback is useful only for the claims it can support. Split evidence by
cadence:

* per-edit checks should be cheap, deterministic, and highly localizing;
* pre-merge checks can include real components and selected boundaries;
* scheduled checks can search larger spaces or use scarce environments;
* release checks should validate the exact artifact and required support cells;
* production observation should test safe operational claims that cannot be
  established elsewhere.

A fast or selected run is partial evidence. It must never overwrite or
masquerade as the complete selection required by another decision.

## Lifecycle use

The detailed lifecycle defaults belong in `L2_*.md`. The general pattern is:

* prototypes emphasize learning and cheap falsification;
* feature development emphasizes changed responsibilities and rapid regression
  feedback;
* stabilization adds boundary, compatibility, artifact, and stakeholder
  evidence;
* release requires fresh, comparable, enforced evidence and explicit residual
  risk;
* maintenance re-evaluates impact, evidence decay, incidents, and obsolete
  tests.

These are non-exclusive confidence profiles, not permission to postpone a
material risk. Apply `L1.md` whenever claims, architecture, exposure, support
policy, or operating conditions change.

## Classification in practice

Treat classification dimensions independently:

* assign one primary structural scope to each automated behavior test;
* add purposes such as regression, acceptance, contract, smoke, or
  compatibility when they explain why the evidence exists;
* add techniques such as property-based, fuzz, snapshot, differential, or fault
  injection when they explain how cases are produced or evaluated;
* record resources and boundaries when they affect fidelity, cost, or
  interpretation;
* record execution class and cadence for selection and operation.

Service/API, database, filesystem, message-broker, model, and data-pipeline tests
name common subjects or boundaries, not purposes by themselves. Classify an API
consumer contract test, database migration integration test, or data-quality
component test by its actual structural scope and purpose.

Use the glossary rather than inventing composite levels such as
“integration-regression-contract test.” Multiple dimensions may describe one
test without turning them into one hierarchy.

## Designing useful automation

Start with a claim and plausible failure mode. Then:

1. choose the boundary whose semantics could expose that failure;
2. choose an oracle independent enough to detect it;
3. control irrelevant variability without deleting relevant behavior;
4. arrange representative ordinary, boundary, invalid, and adverse cases;
5. make failure output identify inputs, state, environment, and artifact;
6. confirm the test fails under a deliberate relevant fault where practical;
7. decide the selection, cadence, owner, and retention needed by the decision;
8. record omitted semantics and route broader follow-up through L3.

Prefer behavior-oriented assertions over private call sequences. Avoid
time-based sleeps when an observable condition can be awaited. Keep test data
small enough to understand unless scale itself is part of the claim.

## Common subjects and boundaries

### Processes and installed artifacts

When packaging, entry points, imports, startup, generated metadata, or
installation are claims, build once and test the exact artifact outside the
source tree. Source-tree imports do not establish installed behavior.

### Persistence and data

Use real persistence semantics when constraints, transactions, isolation,
migrations, encoding, collation, or query behavior matter. Separate schema
conformance from semantic contract and data-quality claims.

### Networks and services

Use doubles for controlled client behavior and rare responses; use real or
representative protocols for serialization, headers, status handling, timeouts,
TLS, retries, and compatibility. Record which side of the boundary is under
test.

### Time, randomness, and concurrency

Inject clocks and random sources where control matters, retain seeds and
counterexamples, and synchronize on state rather than elapsed time.
Concurrency evidence needs enough repetitions and environment identity to
support its claim; a single pass does not establish absence of races.

### Human-facing behavior

Automation can check syntax, rules, focus order, contrast, labels, and stable
interaction contracts. It cannot by itself establish usability, comprehension,
or accessibility for intended users and assistive technologies. Combine it
with L3-T12 through L3-T14 where those claims matter.

## Trustworthy execution

The harness is part of the evidence system. It should:

* fail when the subject, setup, collection, normalization, or reporting fails;
* keep complete and partial artifacts separate;
* record subject revision, built artifact, environment, selection, exclusions,
  tool configuration, and outcome;
* exclude quarantined tests from claims they cannot support while retaining
  owned, expiring diagnostic records;
* distinguish product, dependency, infrastructure, and harness failures;
* preserve enough context to reproduce a result;
* reject stale or non-comparable inputs at gates.

Retries can collect diagnostic observations but must not silently redefine an
intermittent failure as success. A quarantine is an explicit evidence gap, not
a synonym for a suspected flake.

## Static and build-time evidence

Formatting, linting, type checking, architecture checks, vulnerability scans,
secret scans, license checks, configuration validation, and supply-chain
verification do not execute ordinary product behavior. They remain valuable
evidence selected by language, threat model, dependency model, and deployment
context.

Give every enforced check a scope, cadence, failure policy, owner, triage path,
and waiver policy. A scanner supports claims about its rules, configuration,
inputs, and freshness; it does not prove the absence of defects outside that
model.

## Portfolio maintenance

More tests are not automatically more confidence. Review the portfolio for:

* duplicated scenarios that add no distinct sensitivity;
* assertions tied to implementation rather than behavior;
* obsolete regressions and snapshots;
* boundaries represented only by unvalidated doubles;
* slow tests that belong at a different cadence or scope;
* failures that cannot be localized or reproduced;
* critical claims without credible evidence.

Use `L3_T10_portfolio_health.md` for this assessment and
`L3_T11_metrics.md` before turning any measurement into a gate. Numeric targets
belong in project-owned specifications, not this conceptual reference.

## Procedure map

Use:

* `L3_T1_unit.md` through `L3_T4_system.md` for structural boundaries;
* `L3_T5_regression.md`, `L3_T7_contract.md`, and `L3_T12_acceptance.md` for
  purposes;
* `L3_T6_generative_and_fuzz.md`, `L3_T9_snapshot.md`, and
  `L3_T13_exploratory.md` for techniques and evidence forms;
* `L3_T8_quality_attributes.md`, `L3_T14_usability_accessibility.md`, and
  `L3_T15_operational_resilience.md` for specialized claims;
* `L3_T10_portfolio_health.md` and `L3_T11_metrics.md` for evidence-system
  health and quantitative decisions.
