<!--
TESTING-GUIDANCE-REVIEW: document-level annotation

Problems identified:
- This document combines policy, terminology, lifecycle cadence, and quantitative targets in one authority level.
- The taxonomy treats contract as comparable to structural scopes even though contract usually describes purpose; other purposes and techniques are also mixed with scope markers.
- Several recommendations are framed universally despite depending on project risk, architecture, environment, and feedback constraints.
- Fixed coverage, mutation, runtime, flake, and performance targets are not accompanied by explicit populations, denominators, baselines, uncertainty, or decision rules.
- Acceptance, exploratory, usability/accessibility, and operational/recovery evidence are underrepresented.

Proposed fixes:
- Retain the detailed material, but annotate sections by authority: normative policy, definition, recommended default, example, or project-specific convention.
- Describe tests with orthogonal dimensions: structural scope, purpose, technique, resources/boundaries, and execution cadence.
- Make risk and failure modes determine evidence applicability; use lifecycle only to adjust confidence, breadth, fidelity, and enforcement.
- Replace universal numeric gates with a metric-specification procedure while retaining example values as explicitly illustrative.
- Add dedicated guidance for acceptance, exploratory, usability/accessibility, and operational/resilience evidence.
-->

# Testing Policy

## 1. Goals and principles

1. Tests must provide:

   * High confidence in correctness.
   * Fast feedback for most changes.
   * Clear localization of failures.
2. Test suites must be:

   * Structured by scope and intent.
   * Predictable to run (no hidden side effects).
   * Strictly configured (misconfigurations should fail, not be silently ignored).

Language conventions:
Use “must” for requirements, “should” for strong recommendations.

---

<!--
SECTION REVIEW — SPLIT AND MOVE MOST CONTENT

Keep in Overview.md only a concise normative statement that tests are classified along independent dimensions.
Remove the rule that `contract` is an alternative structural scope; contract should be an independently composable purpose.
-->
## 2. Test taxonomy

### 2.1 Scopes

Each test must declare its scope via markers:

### 2.2 Cross-cutting markers

Use additional markers to express other dimensions:

Policy:

* Every test must have at least one scope marker (`unit`, `component`, `integration`, `system`, or `contract`).
* Cross-cutting markers are optional but recommended when applicable.

---

<!--
SECTION REVIEW — SPLIT

Keep the tool-independent behavioral and invariant-oriented principles in Overview.md.
-->
## 6. Test design guidelines

### 6.1 Design around behaviour and invariants

For each module or component:

* Identify responsibilities in plain language.
* Identify invariants (“this can never happen”) and state transitions.
* Write tests that reflect these, not just line coverage.

### 6.2 Naming and structure

* Test function names must describe behaviour, not implementation details:

  * `test_parse_header_handles_missing_fields` instead of `test_parser_case3`.
* Each test should assert one conceptual behaviour; multiple small tests are preferred over one large one.
* Arrange test body roughly as:

  * Arrange (set up),
  * Act (call),
  * Assert (checks).

---

<!--
SECTION REVIEW — MOVE DETAILED MATERIAL; KEEP ONLY POLICY SUMMARY

Move the collaborator strategy, dependency-injection guidance, and mocking/fake guidance to the unit-testing procedure.
Keep a short policy statement that unit scope is a small chosen boundary providing localizing evidence.
Preserve dependency injection as a selective recommendation at external-effect and variability boundaries; do not remove it or require replacement of every collaborator.
Remove the universal ~100 ms threshold from core policy and retain it only as an illustrative project budget.
-->
## 7. Unit tests

Guidelines:

* Aim for unit tests to be very fast; most should complete in under ~100 ms, and the entire unit suite should be runnable on every save or commit.
* Use dependency injection and small interfaces to avoid mocking deep internals.
* When mocking, mock at integration boundaries (`requests` layer, repository interface), not internals.
* Use simple, explicit fakes when possible.
* Avoid asserting on private attributes or unstable implementation details; prefer observable behaviour.

---

<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the definition and resource guidance to the component-testing procedure.
Overview.md should name component scope only as one available evidence boundary.
-->
## 8. Component tests

Guidelines:

* Use temporary resources (temp directories, SQLite in a temp file, etc.).
* Test through public APIs; avoid reaching into internal implementation details.
* Only mock or fake at the boundaries of the component under test.

---

<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the infrastructure guidance to the integration-testing procedure.
Retain only the policy principle that real external semantics require evidence that executes those semantics.
-->
## 9. Integration tests

Guidelines:

* Mark tests as `integration` and any relevant cross-cutting markers (`db`, `slow`, `security`, `performance`).
* Use dedicated test resources (test databases, stub services) to avoid affecting production data/settings.
* Ensure tests are repeatable and can be run in CI.
* Prefer containerized or isolated test instances of infrastructure where possible.

---
<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the scenario list to the system-testing procedure.
Do not equate system scope with acceptance purpose; acceptance evidence may exist at several structural scopes.
-->
## 10. System tests

Guidelines:

* Mark as `system` and usually `slow`.
* Prefer a small set of critical scenarios:

  * Startup and shutdown behaviour.
  * Happy-path workflows.
  * Critical error handling paths.
  * Cross-service flows in a distributed system.

---

<!--
SECTION REVIEW — MOVE AND EXPAND

Move the detailed material to the contract-testing procedure.
Reclassify contract as a purpose that can be exercised at component, integration, or system scope.
Expand beyond schema shape to behavioral obligations, producer/consumer expectations, version compatibility, migrations, and allowed versus breaking changes.
-->
## 11. Contract tests

Guidelines:

* Mark as `contract`.
* For databases:

  * Assert column presence, nullability, types, and relationships.
* For APIs:

  * Assert that responses match a schema (e.g. via JSON Schema or Pydantic models).
* For events/messages:

  * Assert payload structure, required fields, and versioning rules.

---

<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Retain only the general policy that behavior varying by supported configuration or environment requires representative evidence.
-->
## 12. Configuration and environment testing

Policy:

* Behaviour that depends on configuration or environment variables must have tests.

Examples:

* Different runtime profiles (dev vs prod).
* Feature flags.
* Cache toggles.

---

<!--
SECTION REVIEW — MOVE AND EXPAND

Move the detailed guidance to the generative/property-testing procedure.
Remove the implication that property-based testing primarily belongs to pure functions. Expand the reference material to stateful, model-based, differential, and metamorphic testing.
-->
## 13. Property-based testing

Policy:

* Property-based tests should be used for:

  * Normalization functions.
  * Parsers and formatters.
  * Comparators and similarity functions.
  * Simple but critical transformations.

Guidelines:

* Place such tests under `tests/property/` and mark them `property_based` (plus a scope marker).
* Properties should be simple and easy to understand (idempotence, round-trip, bounds, symmetry).
* Prefer pure, side-effect-free functions as subjects of property-based tests.

---

<!--
SECTION REVIEW — MOVE AND SPLIT

Move test-design guidance for logs, metrics, traces, and diagnostics to the non-functional/observability procedure.
Separate instrumentation-contract checks from operational evidence that alerts and diagnostics work under realistic failure conditions.
-->
## 14. Observability tests

Policy:

* For critical flows, log messages and metrics are part of the public contract and may be tested.

Guidelines:

* Use the `caplog` fixture for log assertions.
* Mark tests with `observability`.
* Focus on:

  * Presence and shape of key log messages.
  * Correct logging of error conditions.
  * Inclusion of identifiers (e.g. request IDs, entity IDs) needed for debugging.

---

<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD AND DISTRIBUTE

Distribute mutation testing, fuzzing, chaos/resilience testing, and snapshot testing to their corresponding procedures and reference sections.
Keep the detailed information; do not compress these techniques into a short list.
-->
## 16. Advanced testing techniques

### 16.1 Mutation testing (optional)

Projects with high criticality may adopt mutation testing tools to assess test suite strength.

Guidelines:

* Run mutation tests only in dedicated workflows (they are slow).
* Use them to identify weakly tested code paths, not as a hard gate for all changes.
* Focus mutation testing on:

  * Core business logic.
  * Pure or mostly pure functions.
  * Security-sensitive code paths.

<!--
SECTION REVIEW — MOVE; REMOVE UNSUPPORTED UNIVERSAL TARGETS

Move metric interpretation to a dedicated metric-design procedure and project-specific examples.
Remove universal coverage and mutation targets unless their population, denominator, tool configuration, baseline, uncertainty, decision, and response are explicitly defined.
Retain the practical workflow for investigating uncovered code and surviving mutants as implementation guidance.
-->

### 16.3 Fuzz testing

Use fuzzing where inputs are complex, adversarial, or security-relevant (parsers, protocol handlers, API boundaries).

Guidelines:

* Start with property-based generators (e.g. Hypothesis) before introducing external fuzzers.
* Focus on:

  * Crashing behaviours.
  * Assertion failures.
  * Unexpected exceptions or timeouts.

<!--
SECTION REVIEW — MOVE AND EXPAND

Move this material to a first-class operational/resilience procedure.
Expand it to deployment, rollback, restart, failover, backup restoration, recovery objectives, degraded modes, runbooks, and observability validation.
-->
### 16.4 Chaos and resilience testing

For distributed systems and services, resilience under partial failure is critical.

Guidelines:

* Design a small set of chaos scenarios (e.g. DB latency, dependency returning errors, intermittent network failures).
* Automate these in integration/system tests where feasible.
* Ensure observability (logs/metrics/traces) clearly indicate degraded modes and recovery.

### 16.5 Snapshot tests (optional)

Guidelines:

* Use sparingly, when outputs are large but structurally stable.
* Keep snapshots readable and reviewed like code.
* Avoid using snapshots as a substitute for precise behavioural assertions when those are feasible.

---

<!--
SECTION REVIEW — SPLIT AND MOVE DETAILS

Keep tool-independent requirements for required static, security, and supply-chain evidence only where justified by project risk and support policy.
Replace the universal every-commit/every-PR cadence with explicit project-selected gates and documented waivers.
-->
## 17. Static analysis and security checks

Some checks must run regularly regardless of project specifics.

Policy:

* On every commit and every PR, run:

  * Formatter (e.g. `ruff format`, `black`).
  * Linter (e.g. `ruff check`).
  * Type checker (e.g. `mypy`, `pyright`, `ty`).
  * Dependency scanner (e.g. `pip-audit`, `safety`, or platform SCA).
  * Secret scanner (e.g. `gitleaks`, `trufflehog`, or platform equivalent) at the repository level.

Guidelines:

* CI must fail on:

  * Lint or type errors.
  * Blocker security findings (critical/high CVEs, leaked secrets), unless explicitly triaged with a documented waiver.

These checks should be wired into the `check` command and CI pipelines.

---

<!--
SECTION REVIEW — MOVE; REMOVE UNIVERSAL NUMERIC TARGETS

Move metric definitions and examples to a dedicated metric-design procedure.
Remove the generic 80% line coverage, 70% branch coverage, 70% mutation, and ±5–10% performance recommendations as universal guidance.
Retain values only as clearly labeled examples after defining population, denominator, environment, baseline, uncertainty, threshold rationale, action, and owner.
-->
## 18. Metrics and targets

Quantitative metrics help keep the test suite effective and healthy. Targets are guidelines, not rigid laws, but deviations should be explicit and justified.

Recommended targets:

* Coverage:

  * Line coverage: target ≥ 80% for backend Python code.
  * Branch coverage: target ≥ 70%.
  * For critical modules, higher targets are encouraged.
* Mutation score (where used):

  * Target ≥ 70% for core business logic.
* Flake rate:

  * Flaky tests should be rare; if the same test flakes multiple times in a short window, it must be investigated, fixed, or quarantined.
* Performance regression:

  * For performance tests, new versions should remain within an agreed band (e.g. ±5–10%) of baseline latency/throughput for key endpoints, unless an intentional change has been documented.

Projects may adopt stricter or looser thresholds, but they should be explicit.

---

<!--
SECTION REVIEW — SPLIT

Keep genuinely tool-independent evidence-integrity prohibitions in Overview.md, such as arbitrary sleeps, hidden failures, and unreviewed suppression.
Move scope-specific red flags to the relevant L3 procedures.
Remove the universal claim that lower-level tests must carry most of the load; portfolio shape should follow risks and architecture.
-->
## 19. Prohibited practices and anti-patterns

To maintain isolation, efficiency, clarity, purpose, and maintainability, the following are explicitly disallowed:

* Unit tests must not:

  * Hit real network endpoints.
  * Use real databases or queues.
  * Read from or write to persistent files or directories.
  * Depend on real-time sleeps or non-deterministic timing.

* Test suites must not:

  * Rely on arbitrary `time.sleep` calls to “stabilize” behaviour; use proper synchronization (e.g. polling, hooks, events) instead.
  * Treat large, slow end-to-end suites as the primary safety net; lower levels must carry most of the load.

* Tests must not:

  * Chase 100% line coverage with trivial assertions that add no defect-detection value.
  * Assert on unstable implementation details (private attributes, log strings that are not part of the contract) without a clear reason.
  * Silently ignore failing tests or leave known flaky tests untriaged for long periods.

* Security/tooling:

  * Secret-scanner and vulnerability-scan warnings must not be casually suppressed; waivers must be documented and reviewed.
  * Disabling static analysis or test suites “temporarily” without an issue/ticket and clear follow-up is not acceptable.

If these constraints are too tight for a specific case, the exception and rationale must be documented in code comments and, where relevant, in project docs.

```
```
<!--
SECTION REVIEW — REMOVE THIS DUPLICATE SECTION

This is a duplicate of section 16.5 above and follows stray Markdown fences. Remove the duplicate and malformed fences after review; preserve the earlier complete snapshot-testing section and move it to the snapshot procedure/reference material.
-->
### 16.5 Snapshot tests (optional)

Snapshot tests capture a serialized representation (e.g. JSON, HTML) and compare against a baseline.

Guidelines:

* Use sparingly, when outputs are large but structurally stable.
* Keep snapshots readable and reviewed like code.
* Avoid using snapshots as a substitute for precise behavioural assertions when those are feasible.
