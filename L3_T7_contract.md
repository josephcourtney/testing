# L3-T7 — Contract and Compatibility Testing

## 1. Purpose

Verify obligations between a producer and one or more consumers, including what may change, what must remain compatible, and how compatibility is demonstrated across versions and environments.

Contract is a test purpose, not a structural scope. Contract evidence may execute at unit, component, integration, or system scope.

## 2. Contract forms

### Schema conformance

Validate required fields, types, constraints, encodings, database structure, event shape, or document format against an explicit schema.

### Behavioral protocol contract

Validate interaction semantics such as status codes, error behavior, ordering, idempotency, pagination, retries, authentication, authorization, and state transitions.

### Consumer-driven contract

Capture expectations derived from actual consumer behavior, publish versioned interactions, and verify them against provider versions before deployment.

### Provider compatibility

Verify that a producer continues to satisfy declared consumers, including supported-version and deployment compatibility rules.

### Data and migration contract

Verify schema evolution, backward and forward readability, migration preconditions, rollback limits, defaults, constraints, and retention obligations.

### Platform and artifact compatibility

Verify public Python APIs, CLI behavior, file formats, plugins, operating systems, runtimes, browsers, devices, or other supported execution cells.

## 3. Applicability

Use when:

* another component, team, version, deployment, or external user depends on an interface,
* compatibility or versioning rules matter,
* producer and consumer release independently,
* recorded examples or fakes must remain aligned with reality,
* schemas or protocols evolve,
* installed artifacts or multiple platforms are supported.

Do not use contract tests as a substitute for real-infrastructure integration tests when the risk is infrastructure semantics, or for system tests when the claim is a complete user journey.

## 4. Define the contract

Record:

* producer and consumers,
* contract artifact or source of truth,
* required and optional behavior,
* compatibility policy,
* version and deprecation rules,
* ownership and publication process,
* provider-verification process,
* environments or artifact forms in which the contract must hold.

A schema alone is insufficient when consumers depend on behavioral semantics not expressed by the schema.

## 5. Design rules

* Assert only obligations on which consumers may rely.
* Include allowed evolution, not only the current shape.
* Verify representative negative and error behavior.
* Use canonical examples only when they remain connected to real producer or consumer behavior.
* Prevent stale contracts from passing independently of the deployed participants.
* Retain versioned verification evidence when deployment safety depends on version combinations.
* Test the built or installed artifact when packaging is part of the public contract.

## 6. Writing procedure

1. Identify the boundary, producer, consumers, and independent release units.
2. Enumerate schema, behavioral, compatibility, and versioning obligations.
3. Choose an explicit artifact: schema, protocol specification, consumer interaction, migration rule, public API inventory, or compatibility matrix.
4. Select structural scope according to the semantics required.
5. Add positive, negative, and evolution cases.
6. Verify providers against actual or representative consumer expectations.
7. Record which producer/consumer versions and environments were verified.
8. Add focused integration evidence for real infrastructure behavior that the contract harness cannot establish.

## 7. Evaluation

A good contract suite:

* fails on dependency-relevant breaking change,
* tolerates changes declared compatible,
* identifies the affected obligation and consumer,
* remains connected to real producer and consumer behavior,
* supports deployment decisions across versions.

Red flags:

* whole-payload equality when only a subset is contractual,
* schemas with no behavioral or versioning policy,
* hand-maintained examples that no participant verifies,
* contract tests classified as a separate structural level regardless of execution,
* provider verification that does not run against the built artifact,
* no record of which versions are safe together.

## 8. Outputs

* boundary and consumer inventory,
* contract artifacts and ownership,
* compatibility and deprecation rules,
* producer/consumer verification matrix,
* uncovered behavioral obligations,
* required integration or system evidence.
