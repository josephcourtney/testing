# L3-T1 — Unit Testing: Design, Writing, Evaluation

## 1. Purpose

Provide fast, deterministic, highly localizing evidence about behavior inside a small chosen boundary.

A unit is an operational testing boundary, not necessarily a single function, method, or class. Projects may use solitary units with replaced collaborators, sociable units with inexpensive real collaborators, or both.

## 2. Applicability

Use unit scope when:

* the relevant semantics are local to a small boundary,
* failures can be diagnosed without exercising external infrastructure,
* the test can remain fast and deterministic,
* replacing or retaining collaborators does not remove the failure mode being tested.

Do not use unit tests to claim confidence in SQL dialects, wire protocols, authentication systems, framework integration, deployment behavior, or other semantics that the unit boundary does not execute.

## 3. Define the boundary

Before writing the test, identify:

* the public or supported entrypoint,
* the behavior or invariant under test,
* collaborators inside the chosen unit,
* dependencies outside the unit,
* the external semantics deliberately excluded.

The boundary may contain multiple objects when their collaboration is cheap, stable, and central to the behavior.

## 4. Collaborator strategy

### Retain real collaborators when

* they are deterministic and inexpensive,
* their behavior is part of the chosen unit,
* retaining them improves confidence without harming localization.

### Replace collaborators when

* deliberate fault injection or rare responses are required,
* the real collaborator is slow, nondeterministic, destructive, or unavailable,
* the dependency lies outside the chosen unit boundary.

Prefer simple fakes or stubs when interaction verification adds no value. Use mocks when the interaction itself is contractual. Do not reproduce an internal call graph merely to make the test pass.

When double fidelity is consequential, pair the unit tests with contract or integration evidence.

## 5. Assertions

Prefer:

* explicit outputs and state transitions,
* specified exceptions and error categories,
* domain events or observable effects,
* invariants, algebraic properties, and idempotence.

Avoid:

* private attributes and incidental intermediate values,
* internal call sequences that are not contractual,
* tautological assertions derived from the implementation,
* broad snapshots used instead of a comprehensible oracle.

## 6. Writing procedure

1. State the behavior and the failure mode the test should detect.
2. Choose the unit boundary and collaborator strategy.
3. Select representative nominal, boundary, and invalid cases.
4. Add properties or generated cases where examples undersample the domain.
5. Assert observable behavior.
6. Verify that the test fails when the behavior is removed or plausibly broken.
7. Record excluded semantics that require higher-scope evidence.

Arrange–Act–Assert is a useful convention, not a requirement. Use another structure when it communicates the behavior more clearly.

## 7. Evaluation

A good unit test:

* detects a meaningful local failure,
* is deterministic and independent of test order,
* remains stable under behavior-preserving refactoring,
* has a comprehensible oracle,
* runs within the project's intended rapid-feedback budget.

Red flags:

* deep stacks of mocks,
* fixtures larger than the behavior being tested,
* interaction assertions that mirror implementation,
* hidden global state,
* real-time waits,
* tests labeled unit despite depending on semantics they do not execute.

## 8. Scope adjustment

* Move to component scope when the meaningful behavior is collaboration across a coherent subsystem.
* Move to integration scope when correctness depends on real external semantics.
* Move to system scope when only assembled user-visible behavior provides the required oracle.
* Do not move downward merely to obtain a preferred portfolio shape if doing so removes sensitivity to the risk.
