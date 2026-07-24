# Current Testing Assessment

This is a project-specific example of applying L1 and L2-P3. Its commands, evidence formats, measurements, and thresholds are not general policy.

## Decision context

* Decision: beta/stabilization readiness.
* Primary risks: incorrect normalization, schema drift, unsafe target loading, misleading CLI diagnostics, packaging drift, and tests that pass only inside the source checkout.
* Outcome: pass for the stated beta decision. Production remains separately gated in `production-readiness.md`.

## Risk and evidence map

`testing-requirements.json` maps declared responsibilities to executable evidence. An unfiltered run fails when a required mapping is incomplete.

| Claim or risk | Evidence |
|---|---|
| Normalization and policy behavior are deterministic | Unit examples and generated invariants |
| Subsystems collaborate through supported interfaces | Component tests |
| Published Python and JSON behavior remains compatible | Component/system tests marked `contract`, semantic goldens, independent consumer |
| CLI behavior and diagnostics work through the process boundary | System smoke and regression tests |
| Built distributions work outside the checkout | Exact-wheel isolated installation and consumer workflow |
| Unsafe or failed target loading is bounded and diagnostic | Unit protocol, component process-boundary, security-purpose, and system evidence |

The product has no database, network service, broker, remote persistence, or other real external-system boundary. Integration scope is therefore not applicable to the current risk map. Reassess if such a boundary is introduced.

## Classification and fidelity

Each test has one structural scope (`unit`, `component`, or `system` in the current portfolio) and may have independent purpose or technique markers such as `contract`, `regression`, `smoke`, `security`, `snapshot`, or `property_based`.

Component tests use supported subsystem entrypoints and retain the subprocess boundary when process isolation is part of the component's behavior. Doubles are limited to external control points where deliberate fault injection is required. Contract-purpose tests include both local schema/public-API checks and installed-artifact system checks.

Whole help and prose snapshots are intentionally absent. Machine-document goldens decode, satisfy semantic assertions, and re-encode identically. Temporary paths, direct argument vectors, disabled network sockets, bounded waits, and the absence of retry-as-success support determinism.

## Suite health

The full suite contains 112 tests and completes within the project's declared editing and hard-gate budgets. It currently has no skips, expected failures, or quarantines. Comparable run history records per-phase durations and suspected flakes.

The available history is insufficient to claim a precise long-term flake probability. Current observations support “no known flake” rather than a statistically established rate.

## Project-specific metrics

* Statement coverage: 85.75%.
* Branch coverage: 72.35%.
* Changed-line coverage: 100%.
* Maintained mutation cohort: 81.73%, with zero `no_tests` mutants.

These values are descriptive evidence for the declared code and mutation cohorts. Their gates are defined in `local-testing.md` and must satisfy `L3_T11_metrics.md`; they are not universal quality targets.

## Residual uncertainty and revisit triggers

| Gap or non-applicable class | Revisit trigger |
|---|---|
| Real external integration semantics | Add a service, database, broker, remote runner, or persistence dependency. |
| Human-facing prose compatibility | Make prose or help output a supported compatibility contract. |
| Managed data-quality behavior | Add persistent observation corpora, learned behavior, or production datasets. |
| Operational resilience and privacy | Add a live service, sensitive data, authentication, recovery objectives, or multi-system operation. |
| Long-term flake estimate | Accumulate enough comparable runs for a defensible estimate. |

Reassess on phase promotion, material boundary or audience change, expired waiver, incident, or measured suite-health degradation.
