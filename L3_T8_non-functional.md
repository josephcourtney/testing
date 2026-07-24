<!--
TESTING-GUIDANCE-REVIEW: document-level annotation

Problems identified:
- Performance, security, data quality, and observability are grouped together despite requiring different threats, workloads, environments, and oracles.
- Generic percentage tolerances and thresholds can be mistaken for valid gates without measurement design.
- Accessibility, privacy, capacity, resilience, and recovery are not fully represented.

Proposed fixes:
- Keep the broad overview but annotate each evidence type with its own claim, workload or threat model, environment, measurement method, and uncertainty.
- Move threshold design into an explicit metric procedure and retain numeric examples only as illustrations.
- Add or cross-reference dedicated accessibility/usability and operational/resilience procedures.

Review rule: preserve the original document text. Apply any proposed fix only after explicit review.
-->

# L3-T8 — Non-Functional Tests (Risk-Driven): Design, Writing, Evaluation

## 1. Purpose

Validate properties other than functional correctness, selected based on **risk profile**:

* **Performance** (latency/throughput/resource)
* **Security** (vulnerability/abuse resistance)
* **Data quality** (freshness/integrity/anomaly)
* **Observability** (logs/metrics/traces as contract)

These tests are typically gating in release/hardening phases for relevant systems.

## 2. Applicability

Use when:

* non-functional failure would cause material harm (SLA breach, data corruption, incident response failure),
* the system is customer-facing or compliance-constrained,
* the risk profile explicitly requires it (L2-P4).

Configuration-dependent behavior also requires representative evidence. Test
supported runtime profiles, feature flags, cache toggles, environment-variable
combinations, and other settings where a configuration change can alter
behavior or risk.

Configuration tests may occur at unit, component, integration, or system scope.
Choose the lowest scope that executes the semantics at risk, and include
realistic environment or infrastructure semantics when a local substitute is
not sufficient.

### 2.1 When not to use this test type

Avoid non-functional tests that:

* have no explicit measurable contract (threshold, invariant, required signal),
* are too noisy to be actionable (uncontrolled variance),
* are run at an inappropriate cadence (e.g., heavy perf gates on every save).

## 3. Design rules (common)

* Define the **measurable contract** (threshold, invariant, required signal).
* Prefer repeatable harnesses; isolate environmental noise where feasible.
* Keep assertions robust to small variance; avoid brittle micro-benchmarks.
* Separate “diagnostic measurement” from “gating thresholds” where necessary.

## 4. Sub-procedures by category

### 4.1 Performance tests

**Design**

* Identify critical endpoints/operations and the metric (p50/p95 latency, throughput, memory).
* Establish a baseline and acceptable band (e.g., ±5–10% where appropriate).
* Control data sizes and warmup; avoid conflating functional and perf assertions.

**Evaluate a test**

* Does it measure something stable and meaningful?
* Is variance controlled (warmup, fixed dataset, pinned environment)?
* Are thresholds justified and not arbitrary?

**Evaluate the suite**

* Coverage of top critical paths.
* Trend tracking and regression detection strategy.
* Runtime placement (PR vs nightly) aligned to cost.

---

### 4.2 Security tests

**Design**

* Include static security scanning and dependency checks as baseline.
* Add targeted dynamic tests where abuse cases are known (authZ, injection boundaries, unsafe deserialization).
* Prefer boundary-focused tests over deep internal mocking.

Static, security, and supply-chain checks should be selected according to the
project's risk and support policy. A typical automated check set includes:

* a formatter,
* a linter,
* a type checker,
* a dependency vulnerability scanner, and
* a repository-level secret scanner.

Projects should explicitly select which checks run on commits, pull requests,
scheduled workflows, and releases. CI should fail on lint or type errors when
those checks are designated gates, and on blocker security findings unless an
explicitly documented waiver has been reviewed. The selected checks should be
available through the project's normal aggregate check command and CI
pipelines.

**Evaluate a test**

* Does it reflect a realistic threat model?
* Does it fail closed with actionable diagnostics?
* Is it maintained as dependencies and attack surface evolve?

**Evaluate the suite**

* Coverage of authentication/authorization and data-handling boundaries.
* Handling of known CVEs and secret scanning hygiene.
* Regular cadence and gating rules.

---

### 4.3 Data quality tests

**Design**

* Define invariants: referential integrity, uniqueness, null bounds, freshness windows, distribution constraints.
* Place checks near ingestion/transformation boundaries.
* Include backfill and aggregation accuracy checks when relevant.

**Evaluate a test**

* Does it detect the failure mode early (before consumers are harmed)?
* Are thresholds justified (not overly sensitive)?
* Does it localize which dataset/transform broke?

**Evaluate the suite**

* Coverage across critical datasets and transforms.
* Handling of drift/anomaly over time (alerting vs gating).
* Runtime strategy (CI vs scheduled validation).

---

### 4.4 Observability tests

For critical flows, logs, metrics, and traces may be part of the public or
operational contract. Focus assertions on:

* presence and structure of key signals,
* correct signals for error conditions, and
* identifiers needed for diagnosis, such as request or entity IDs.

In pytest projects, `caplog` may be used for log assertions. Tests should carry
an observability classification in addition to their structural scope.

**Design**

* Treat key logs/metrics/traces as a contract for critical flows.
* Assert on presence/shape of signals (event emitted, fields included), not full text unless explicitly contractual.

**Evaluate a test**

* Does it test what operators need (IDs, error codes, key metrics)?
* Is it robust to log phrasing changes (prefer structured fields)?

**Evaluate the suite**

* Coverage of critical flows and error paths.
* Signals are sufficient to diagnose failures without guesswork.

---

### 4.5 Mutation testing

Projects with high-criticality code may use mutation testing to assess whether
the suite detects plausible defects. Run mutation analysis in dedicated
workflows because it is expensive, and use surviving mutants to identify weakly
tested paths rather than imposing a universal hard gate.

Prioritize core business logic, pure or mostly pure functions, and
security-sensitive paths.

---

### 4.6 Fuzz testing

Use fuzzing where inputs are complex, adversarial, or security-relevant, such as
parsers, protocol handlers, and API boundaries. Begin with property-based
generators when they provide adequate exploration before adding external
fuzzers.

Look specifically for crashes, assertion failures, unexpected exceptions, and
timeouts.

---

### 4.7 Chaos, resilience, and recovery testing

Distributed systems and services require evidence about behavior under partial
failure. Select a small set of risk-driven scenarios such as database latency,
dependency errors, intermittent network failures, restart, failover, rollback,
backup restoration, and degraded operation.

Automate these scenarios at integration or system scope where feasible. Verify
that logs, metrics, and traces clearly identify degraded modes and recovery, and
that the resulting evidence supports applicable recovery objectives and
runbooks.

---

### 4.8 Snapshot testing

Use snapshots sparingly for outputs that are large but structurally stable.
Keep snapshots readable and review them like code. Do not use snapshots as a
substitute for precise behavioral assertions when those assertions are
feasible; see L3-T9 for the full procedure.

---

## 5. Assessment outputs

For each non-functional category in scope:

* coverage map (critical path → test coverage)
* thresholds/baselines and justification
* flakiness/noise analysis
* recommendation: PR gating vs nightly vs pre-release

### 6. Scope adjustment guidance (downscope / upscope)

* If non-functional checks are stable and low-cost, move them earlier (PR gating).
* If checks are expensive or noisy, move them to scheduled runs while improving harness fidelity and observability.

