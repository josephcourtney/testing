# L3-T3 — Integration Testing: Design, Writing, Evaluation

## 1. Purpose

Validate behavior whose evidential value depends on **real semantics across a
boundary**, such as a database engine, process, operating-system facility,
framework integration, protocol, broker, deployed service, hardware platform,
or separately versioned component.

Integration scope is defined by semantic fidelity, not merely by the number of
modules, the presence of a container, or whether a dependency is “external” in
an organizational sense.

## 2. Applicability

Use integration scope when correctness depends on real behavior such as:

* SQL dialect, constraints, indexing, transactions, isolation, or migrations,
* request serialization, protocol framing, status and error semantics,
* authentication, authorization, identity, certificates, or credentials,
* retry, timeout, backoff, idempotency, ordering, and partial failure,
* process boundaries, signals, environment, startup, shutdown, or exit behavior,
* framework lifecycle, plugin loading, runtime discovery, or platform behavior,
* broker delivery, acknowledgement, duplication, or ordering,
* filesystem or operating-system semantics not represented by a local substitute,
* real provider behavior needed to validate a contract or fake.

Do not use integration tests to:

* exhaustively repeat local business logic already covered at unit or component
  scope,
* simulate complete user workflows when the assembled product is the claim,
* establish stakeholder acceptance merely because a real dependency is present,
* claim production equivalence when the integration environment is materially
  different.

### 2.1 When not to use integration scope

Prefer another scope when:

* the behavior is fully local and a smaller boundary preserves the semantics,
* a controlled fake or lightweight implementation models the relevant risk
  adequately,
* the purpose is only schema or interface shape and provider behavior is not
  required,
* the test spans a full assembled workflow whose oracle belongs at system scope.

## 3. Design rules

### 3.1 Name the boundary and semantic claim

Identify:

* the subject on each side of the boundary,
* the actual implementation or artifact being exercised,
* the specific real semantics that make integration evidence necessary,
* producer, consumer, protocol, schema, or platform versions,
* expected nominal and failure behavior,
* semantics deliberately excluded from the environment.

A test that happens to start a database or container is not useful integration
evidence unless the assertions depend on behavior supplied by that real
implementation.

### 3.2 Use a controlled, representative environment

Integration resources should be:

* isolated from production data, settings, and credentials,
* dedicated or explicitly coordinated,
* provisioned in a known state,
* reset predictably per test, group, or suite,
* identified by implementation, version, image or artifact digest, schema,
  configuration, and important feature flags,
* bounded by startup, readiness, operation, and teardown timeouts,
* cleaned up even after failure,
* reproducible in CI or in a documented equivalent environment,
* representative of the semantics being claimed.

Containers are often useful because they provide a real implementation cheaply,
but containerization alone does not determine scope or fidelity.

Shared environments may be appropriate when dedicated environments are too
costly, but ownership, contention, state isolation, reset, version drift, and
comparability must be explicit.

### 3.3 Test data and state

Use the smallest state that preserves the boundary behavior. Record:

* migrations and initialization applied,
* seed data and identity,
* cleanup or rollback strategy,
* concurrency and isolation assumptions,
* whether tests may run in parallel,
* data retained for diagnosis.

Never rely on undocumented pre-existing shared state.

### 3.4 Assertions

Assert boundary-visible behavior such as:

* persisted values, constraints, transactions, or rollback,
* request and response semantics,
* schema and migration behavior,
* authorization and permission outcomes,
* message acknowledgement, ordering, duplication, and redelivery,
* timeout, retry, cancellation, and partial-failure behavior,
* process exit, signal, startup, shutdown, and resource cleanup,
* compatibility between declared versions,
* diagnostic context needed to distinguish subject, dependency, environment,
  and harness failure.

Avoid:

* fine-grained internal call sequences,
* exact incidental logs unless observability is the purpose,
* broad multi-system user journeys unless intentionally classified as system
  scope,
* assertions that could pass equally against a simplistic fake.

### 3.5 Failure injection and adverse behavior

Add negative cases where they materially increase confidence, including:

* constraint violations,
* permission or authentication failure,
* unavailable or slow dependencies,
* malformed or incompatible responses,
* interrupted transactions,
* duplicate or reordered messages,
* startup or migration failure.

Use controlled mechanisms and bounded timeouts. Verify handling and resulting
state, not merely that a fault was introduced.

### 3.6 Evidence identity and comparability

Retain enough information to identify:

* subject revision and built artifact,
* dependency implementation and version,
* configuration, schema, migrations, and data,
* platform, runtime, container image, or hardware,
* test selection and command,
* whether the run was complete or partial,
* known differences from production.

Do not compare or aggregate results from incompatible environments without an
explicit comparability rule.

## 4. Writing procedure

1. Select the boundary and state the claim and failure mode.
2. Explain why a fake or lower-scope test cannot establish the claim.
3. Provision the real implementation in a known, isolated state.
4. Record implementation, artifact, version, configuration, schema, and data
   identity.
5. Exercise the interaction through the production client, repository, adapter,
   process, or protocol path.
6. Assert boundary-observable outcomes and state.
7. Add representative negative or disruption cases where risk warrants them.
8. Verify readiness, deadlines, teardown, cleanup, and background-exception
   handling.
9. Capture diagnostics sufficient to classify subject, dependency, environment,
   or harness failure.
10. Record excluded semantics and any required system, compatibility,
    performance, security, or operational follow-up.

## 5. Evaluating an existing integration test

A good integration test:

* validates behavior that would be easy to model incorrectly with a fake,
* uses the real implementation or artifact relevant to the claim,
* records versions and environment identity,
* is isolated, repeatable, and cleans up after itself,
* uses readiness checks and bounded waits rather than arbitrary sleeps,
* asserts meaningful boundary semantics,
* includes important error behavior where feasible,
* produces actionable diagnostics,
* states differences from production and residual uncertainty.

Red flags:

* a real service is started but no implementation-specific behavior is asserted,
* tests depend on mutable shared state or execution order,
* environment or dependency versions are unknown,
* setup is manual or irreproducible,
* retries hide intermittent failure,
* arbitrary sleeps and unbounded waits,
* excessive mocking that removes the boundary semantics,
* tests that are actually system workflows without a suitable harness,
* successful results from different environments combined as one comparable
  series,
* production data or credentials used without explicit authorization and
  controls.

## 6. Evaluating the integration suite

Check:

* **Boundary coverage** — each critical real boundary and semantic obligation.
* **Risk coverage** — SQL, protocol, auth, transaction, process, failure, and
  compatibility behavior selected from actual risks.
* **Environment identity** — implementations, versions, artifacts, schemas,
  configuration, and data.
* **Isolation and reset** — dedicated resources, cleanup, ordering independence,
  and parallel-safety rules.
* **Runtime and cadence** — high-value boundary evidence remains usable; heavier
  campaigns may move to scheduled or release workflows with explicit coverage.
* **Failure localization** — results implicate a specific boundary, contract,
  environment, or harness issue.
* **Fidelity gaps** — known differences from production and required higher-
  fidelity evidence.
* **Redundancy** — local business rules are not needlessly repeated.

## 7. Scope adjustment guidance

* Downscope to **component (L3-T2)** when the result no longer depends on real
  boundary semantics.
* Keep integration scope when real implementation behavior is the essential
  source of evidence.
* Add **contract (L3-T7)** evidence for stable producer-consumer obligations and
  version compatibility.
* Upscope to **system (L3-T4)** when the claim is an assembled user- or
  operator-visible workflow across multiple boundaries.
* Add **operational evidence (L3-T15)** when deployment, readiness, degradation,
  recovery, or operator action is the claim.

## 8. Outputs

* boundary-to-claim-to-test inventory,
* real dependency and environment specification,
* versions, artifacts, schemas, configuration, and data identity,
* setup, readiness, reset, cleanup, and timeout strategy,
* nominal and adverse cases covered,
* flaky tests and diagnosed causes,
* fidelity and production-representativeness limitations,
* tests to downscope, upscope, split, remove, or supplement,
* required contract, compatibility, system, security, performance, or
  operational follow-up.
