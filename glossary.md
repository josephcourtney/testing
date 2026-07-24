# Testing Glossary

This glossary collects terminology currently defined in `Overview.md`. It is descriptive rather than normative: policy requirements remain in `Overview.md` unless and until they are separately revised.

## Test scope

### Unit test

A test of a small, deliberately chosen unit of behavior. The unit boundary may include inexpensive, deterministic collaborators, but excludes real external systems such as network services and production databases. Persistent filesystem access, real-time sleeps, and uncontrolled timing are normally outside the unit boundary.

### Component test

A test of a coherent subsystem through its public API using real internal code paths. External systems may be replaced with in-process fakes, or lightweight local implementations such as SQLite may be used when they are part of the intended component boundary.

### Integration test

A test that exercises interaction with a real external dependency or infrastructure boundary, such as a database server, HTTP service, message broker, operating-system facility, or separately deployed component.

### System test

An end-to-end test that treats the application or service as a black box and exercises a complete user- or system-visible workflow through production-like entry points.

## Test purpose

### Contract test

A test that validates an interface or compatibility obligation relied upon by another component, service, consumer, data store, artifact, or deployment environment. Contracts may include API schemas, database schemas, event payloads, behavioral expectations, versioning rules, and migration compatibility.

### Regression test

A test added or retained to prevent recurrence of a previously observed defect or failure mode.

### Smoke test

A small, fast set of tests covering critical paths to establish that a build, deployment, or environment is basically usable before broader testing proceeds.

### Observability test

A test that verifies required logs, metrics, traces, identifiers, or other operational signals. Such signals should be tested as contracts only when their presence or shape is relied upon operationally.

### Security test

A test whose primary purpose is to identify or prevent security failures, including authorization errors, unsafe input handling, secret exposure, vulnerable dependencies, and other explicitly modeled threats.

### Performance test

A test that measures latency, throughput, resource consumption, scalability, or another performance characteristic under a defined workload and environment.

### Data-quality test

A test that checks properties of data such as validity, completeness, consistency, freshness, uniqueness, referential integrity, or conformance to an expected schema.

## Test techniques

### Property-based test

A generative test that checks stated properties over many generated examples rather than enumerating only selected cases. Properties may include invariants, round trips, bounds, algebraic laws, state-machine rules, differential equivalence, or metamorphic relations.

### Fuzz test

A test that supplies large numbers of generated, mutated, malformed, adversarial, or unexpected inputs to discover crashes, hangs, assertion failures, unsafe behavior, or other violations.

### Mutation testing

A method for evaluating test-suite sensitivity by making systematic small changes to production code and checking whether the tests detect them. A surviving mutation indicates that the changed behavior was not distinguished by the executed tests.

### Chaos test

A test that deliberately introduces failures or degraded conditions—such as latency, dependency errors, resource loss, or network interruption—to evaluate resilience, degraded behavior, observability, and recovery.

### Snapshot test

A test that compares a current serialized output against a reviewed stored baseline. Snapshot tests are most useful for large, stable outputs and do not replace precise behavioral assertions when those are practical.

## Resources and execution characteristics

### Database test (`db`)

A test that exercises database behavior, schema, persistence, transactions, or database-specific integration. The marker does not by itself determine whether the test is unit, component, integration, or system scope.

### Slow test (`slow`)

A test whose expected execution cost is materially higher than the project's normal fast feedback set. The threshold is project-specific and should be defined by the workflow that uses the marker.

### Test fixture

Prepared state, data, resources, or collaborators supplied to a test. Fixtures may be inline values, factories, files, temporary resources, fakes, or managed external systems.

### Test double

A replacement for a collaborator used to control behavior, observe interaction, isolate an external effect, or inject a failure. Common forms include stubs, fakes, spies, and mocks.

### Stub

A test double that returns controlled responses to calls made by the subject under test.

### Fake

A working but simplified implementation of a collaborator, such as an in-memory repository or local service substitute.

### Spy

A test double or wrapper that records interactions for later inspection while optionally retaining real behavior.

### Mock

A test double configured with interaction expectations that are verified by the test.

### Dependency injection

Supplying a collaborator explicitly rather than constructing or locating it implicitly. It is useful when behavior must be controlled, substituted, observed, or fault-injected, especially at external-effect and variability boundaries. It need not be introduced solely to isolate inexpensive, deterministic collaborators within the chosen unit boundary.

## Metrics

### Line coverage

The proportion of executable source lines reported as executed by a test run for a defined code population.

### Branch coverage

The proportion of measured control-flow branches reported as executed by a test run for a defined code population.

### Mutation score

The proportion of executed, non-equivalent mutations detected by the test suite, using a stated treatment of timeouts, invalid mutants, and excluded code.

### Flake rate

The frequency with which a test produces inconsistent outcomes without a relevant change to the tested behavior, measured over a specified population, environment, and time window.

### Performance regression

A statistically or operationally meaningful degradation in a defined performance metric relative to an explicit baseline under comparable conditions.
