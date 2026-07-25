# L3-T4 — System Testing: Design, Writing, Evaluation

## 1. Purpose

Validate the **assembled product** through a supported user- or operator-visible
boundary, such as an installed CLI, public API, browser interface, packaged
application, deployed service, or complete processing workflow.

System is a structural scope. It is not synonymous with acceptance,
end-to-end, regression, or smoke testing:

* **end-to-end** describes a complete representative workflow within the
  relevant product boundary,
* **smoke** describes a small critical-capability selection,
* **acceptance** describes why evidence matters to a stakeholder,
* **regression** describes protection of established behavior or a learned
  failure mode.

A system test may carry any of those purposes when appropriate.

## 2. Applicability

Use system scope when confidence depends on:

* startup, shutdown, wiring, packaging, or deployment of the assembled product,
* critical behavior through the same public entrypoint used by a user or
  operator,
* collaboration across several internal components or services,
* source-tree versus installed-artifact differences,
* configuration or routing that only exists in the assembled system,
* a cross-service failure that lower-scope evidence cannot represent,
* user-visible output, artifacts, state, or error handling.

Do not use system tests to:

* exhaustively repeat every unit, component, or integration case,
* claim stakeholder acceptance without explicit acceptance conditions,
* replace dedicated contract, performance, security, accessibility, usability,
  or operational evidence,
* hide a poorly controlled environment behind repeated retries.

### 2.1 When not to use system scope

Prefer a lower scope when:

* the failure mode is local and a smaller boundary improves localization,
* the risk is one real dependency's semantics rather than complete wiring,
* the intended oracle is a contract or schema independent of the assembled
  product,
* the system harness adds cost or nondeterminism without adding relevant
  semantics.

## 3. Define the system boundary

Record:

* the assembled artifact or deployment under test,
* revision, package, image, executable, or distribution identity,
* user- or operator-visible entrypoint,
* services, dependencies, and controlled substitutes inside the test boundary,
* supported configuration and environment,
* real and simulated external systems,
* critical workflow and expected result,
* semantics or environments deliberately excluded.

End-to-end is relative to this declared product and decision boundary. A system
test may use controlled external dependencies when they preserve the semantics
needed by the claim.

## 4. Design rules

### 4.1 Select high-value workflows

Prefer a curated set of workflows such as:

* startup and shutdown,
* installation or first-run behavior,
* one representative happy path per top-tier user journey,
* critical rejection and recovery paths,
* cross-service flows whose failures appear only in the assembled system,
* configuration and upgrade paths that change public behavior,
* production-like diagnostic or operator workflows.

Avoid comprehensive scenario matrices at system scope when detail can be tested
more cheaply and clearly at unit, component, integration, contract, or
property-based scope.

### 4.2 Black-box assertions

Assert externally visible behavior, including:

* exit status, HTTP status, or public result,
* stable output fields and error categories,
* files, records, events, or reports produced,
* externally visible state transitions,
* user-visible rejection and recovery behavior,
* startup readiness and shutdown completion,
* correlation identifiers or operational signals when observability is a
  declared purpose.

Avoid:

* private state and internal call graphs,
* incidental logs unless operationally contractual,
* exact volatile UI or serialization details without need,
* broad snapshots used in place of semantic assertions.

### 4.3 Installed-artifact fidelity

When packaging is part of the claim:

1. build the exact artifact intended for release,
2. inspect required metadata and included files,
3. install it in a clean environment outside the source checkout,
4. clear source-tree import paths and undeclared development dependencies,
5. invoke public interfaces as an independent consumer,
6. retain artifact digest, runtime, platform, and dependency identity.

Source-tree system tests cannot establish that entry points, package metadata,
included data, dependency declarations, or isolated installation are correct.

### 4.4 Determinism and isolation

Use:

* ephemeral ports and directories,
* isolated accounts, schemas, queues, or containers,
* deterministic or explicitly versioned data,
* readiness probes rather than startup sleeps,
* bounded polling, subprocess timeouts, and explicit stop conditions,
* cleanup that runs after failure,
* captured logs, traces, screenshots, or artifacts needed for diagnosis.

Distinguish product failure from dependency, environment, configuration, and
harness failure.

### 4.5 Environment and compatibility

Record the platform, runtime, artifact, configuration, data, service versions,
and important external conditions. Exercise representative support cells
selected from actual commitments and risk; do not imply compatibility beyond
the observed combinations.

## 5. Smoke selection

A smoke selection is a small, fast, highly reliable subset of critical
capabilities used to decide whether a build, deployment, or environment is
suitable for further testing or use.

A smoke test should:

* use system scope only when it actually exercises the assembled system,
* cover the minimum critical capability needed by the gate,
* have short bounded setup and execution,
* fail with actionable boundary context,
* not be treated as complete acceptance or regression evidence.

Smoke may also describe a small selection at another structural scope. The
purpose does not determine the boundary.

## 6. Writing procedure

1. State the system claim, failure mode, and decision.
2. Identify the exact assembled artifact and environment.
3. Select a critical workflow and define observable pass/fail criteria.
4. Provision dependencies and data with controlled isolation.
5. Bring up the product through its supported startup or installation path.
6. Drive inputs through the user or operator entrypoint.
7. Assert outcomes at the public boundary.
8. Capture diagnostics and artifacts needed to reproduce failure.
9. Shut down and clean up with bounded waits.
10. If the test belongs to a smoke selection, minimize it to the critical signal
    without implying broader coverage.
11. Record excluded support cells, real dependencies, and residual uncertainty.

## 7. Evaluating an existing system test

A good system test:

* exercises the assembled product through a supported public boundary,
* identifies the artifact and environment,
* covers a material workflow or assembled failure mode,
* uses stable semantic assertions,
* is isolated and bounded,
* fails with actionable user- or operator-visible context,
* does not duplicate lower-scope detail without adding assembled semantics,
* states whether it is smoke, acceptance, regression, contract, compatibility,
  or another purpose.

Red flags:

* broad suites duplicating lower-level scenario matrices,
* source-tree execution presented as proof that the built artifact works,
* arbitrary sleeps, port collisions, hidden state, or unbounded processes,
* repeated retries that hide nondeterminism,
* volatile snapshots or exact prose assertions without a contract,
* system scope treated as automatic acceptance evidence,
* a smoke check used to claim complete release confidence,
* environment and dependency identity omitted,
* a black-box test that reaches into private internals for its oracle.

## 8. Evaluating the system suite

Check:

* **Flow selection** — alignment with critical user and operator journeys.
* **Assembled semantics** — evidence that cannot be obtained more credibly at a
  lower scope.
* **Smoke set** — small enough for its intended cadence and clearly distinguished
  from the broader suite.
* **Artifact fidelity** — exact installed, packaged, or deployed artifact where
  relevant.
* **Environment and support coverage** — representative configurations and
  declared compatibility cells.
* **Runtime and flake rate** — diagnose harness and environment causes rather
  than merely moving tests later.
* **Isolation and cleanup** — ports, processes, accounts, data, services, and
  temporary resources.
* **Diagnostics** — retained boundary symptoms, logs, traces, screenshots, and
  reproduction context.
* **Redundancy** — logic and boundary cases remain at the clearest credible
  scope.

## 9. Scope adjustment guidance

* Downscope local logic checks to **unit (L3-T1)** or **component (L3-T2)**.
* Downscope a single real dependency's semantics to **integration (L3-T3)**.
* Retain system scope when assembled wiring, packaging, deployment, or a complete
  public workflow is essential to the claim.
* Add **acceptance (L3-T12)** when stakeholder conditions determine completion.
* Add **contract (L3-T7)** for published interface obligations.
* Add **operational evidence (L3-T15)** for deployment, readiness, monitoring,
  degradation, rollback, or recovery claims.

## 10. Outputs

* assembled-artifact and system-boundary definition,
* critical user/operator workflow inventory,
* curated smoke selection,
* artifact, environment, configuration, data, and dependency identity,
* system tests to split, downscope, remove, or strengthen,
* harness improvements for readiness, isolation, cleanup, and diagnostics,
* support and compatibility gaps,
* required acceptance, contract, non-functional, usability, accessibility, or
  operational follow-up.
