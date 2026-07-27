# L3-T5 — Regression Testing: Design, Writing, Evaluation

## 1. Purpose

Protect previously established behavior and prevent reintroduction of a learned
failure mode.

Regression is a **purpose**, not a structural scope. A regression test may be
unit-, component-, integration-, or system-scoped and may use example-based,
property-based, contract, snapshot, differential, or other techniques.

A regression obligation may arise from:

* a reported or escaped defect,
* an incident or near miss,
* a compatibility break,
* a previously ambiguous behavior that has now been specified,
* characterization of legacy behavior that must remain stable,
* a performance, data, accessibility, usability, security, or operational
  degradation that must not recur.

## 2. Regression, characterization, and sanity

These related purposes should remain distinct:

* **Regression testing** protects established desirable behavior or a learned
  failure mode over time.
* **Characterization testing** records current behavior before change; it does
  not automatically endorse that behavior.
* **Sanity testing** is a narrow plausibility check that a specific change, fix,
  or capability behaves as expected before broader evaluation proceeds.

A sanity check may later become a durable regression test when the protected
obligation and failure mechanism are made explicit.

## 3. Applicability

Use regression evidence when:

* a non-trivial bug is fixed,
* a failure mode is subtle, high-impact, or likely to recur,
* an incident revealed a missing obligation or weak oracle,
* a public behavior, contract, data property, or workflow must remain stable,
* a refactor or replacement must preserve established semantics,
* a high-blast-radius change warrants a focused guardrail,
* a historical defect class should remain visible in the suite.

Do not add regression tests that:

* merely duplicate existing evidence without a distinct protected obligation,
* reproduce only implementation details of the fix,
* require a broad harness when a smaller scope preserves the failure mechanism,
* are so noisy, flaky, or opaque that future failures will be ignored,
* freeze behavior that is obsolete, accidental, or no longer supported.

## 4. Define the protected obligation

Record:

* what behavior must remain true,
* the trigger or conditions under which it matters,
* the previous wrong outcome or failure mode,
* affected users, consumers, operators, data, or systems,
* root cause as currently understood,
* the scope and semantics required to reproduce it,
* issue, incident, support case, or compatibility context where useful,
* conditions under which the regression test may be revised or removed.

A short test name, docstring, issue reference, or nearby comment may carry this
context. Avoid comments that merely narrate implementation mechanics.

## 5. Design rules

### 5.1 Preserve the failure mechanism

Prefer the least costly scope that still reproduces the material mechanism:

* **unit** when the defect is local logic or an invariant,
* **component** when subsystem collaboration is required,
* **integration** when real boundary semantics caused the failure,
* **system** when only assembled wiring, packaging, deployment, or a public
  workflow can reproduce it.

Do not downscope so aggressively that the test reproduces only the symptom while
omitting the boundary or environment that made the defect possible.

### 5.2 Minimize the reproduction

Reduce inputs, state, timing, action sequence, configuration, and environment to
the smallest case that preserves the failure. For generated or stateful
failures, retain the minimized counterexample or action trace.

A minimal reproduction should remain understandable without erasing the real
semantics behind the defect.

### 5.3 Choose a durable oracle

Assert:

* the correct output or state,
* absence of the prior corrupt, unsafe, or invalid outcome,
* a specified exception or rejection,
* a contract or compatibility obligation,
* an invariant that the prior defect violated,
* user-visible or operator-visible recovery,
* a practically meaningful quality attribute when that was the failure.

Avoid:

* incidental internal call sequences,
* private state selected only because it changed during the fix,
* exact unstable output that is not part of the obligation,
* assertions that pass while the original failure can recur in another form.

### 5.4 Validate the regression

Where practical, verify that the test:

* fails on the pre-fix implementation or an equivalent deliberate fault,
* passes after the fix,
* continues to pass through behavior-preserving refactors,
* distinguishes the intended defect from unrelated harness failure.

### 5.5 Add complementary evidence when needed

A focused regression does not replace broader evidence for the underlying class
of risk. Consider:

* property or model tests for a broad input or state space,
* contract tests for producer-consumer drift,
* integration tests for real dependency behavior,
* system tests for assembled workflows,
* monitoring or operational checks for conditions best observed after
  deployment,
* usability, accessibility, security, performance, or data-quality evidence when
  the defect arose in those areas.

## 6. Writing procedure

1. Identify the trigger, symptom, impact, and root cause as known.
2. State the durable behavior or failure mode being protected.
3. Reproduce the defect on the pre-fix code or with a deliberate equivalent
   fault when practical.
4. Minimize the input, state, sequence, and environment without removing the
   failure mechanism.
5. Select the structural scope and technique independently.
6. Assert a stable externally meaningful obligation.
7. Add issue or incident context where it improves future interpretation.
8. Pair the focused test with contract, integration, generative, system,
   quality-attribute or operational evidence when the broader risk warrants it.
9. Record removal or review conditions when the obligation is temporary.
10. Verify evidence freshness and artifact/environment identity when the
    regression depends on a particular platform, dependency, or deployment.

## 7. Evaluating an existing regression test

A good regression test:

* would fail if the learned failure mode plausibly returned,
* states or reveals the protected obligation,
* preserves the relevant failure mechanism,
* is minimal enough to diagnose,
* is stable under behavior-preserving refactoring,
* uses an appropriate structural scope,
* is deterministic or makes unavoidable uncertainty explicit,
* remains relevant to a supported behavior, contract, or risk.

Red flags:

* large fixtures or action sequences when a smaller reproduction exists,
* tests overfit to implementation details of one fix,
* a unit test used for a defect caused by real integration semantics,
* a system test used for local logic that could be localized,
* no record of what behavior is being protected,
* duplicate regressions for the same failure mode without additional sensitivity,
* permanent retention of obsolete characterization behavior,
* flaky timing or concurrency reproductions without a controlled harness,
* a test that passes even when the original defect is deliberately restored.

## 8. Evaluating the regression portfolio

Check:

* **Incident coverage** — high-severity incidents, escaped defects, and repeated
  defect classes.
* **Failure-class coverage** — focused examples supplemented by broader
  properties or contracts where useful.
* **Scope fit** — defects live at the scope that preserves their mechanism and
  localizes failure.
* **Redundancy** — overlapping tests add distinct sensitivity or are merged.
* **Obsolescence** — unsupported behavior, retired compatibility obligations, and
  superseded implementation details are removed or revised.
* **Diagnostics** — failures identify the protected obligation and relevant
  context.
* **Cost and cadence** — important regressions run early enough to affect the
  corresponding decision.
* **Operational feedback** — incidents, support reports, monitoring, and user
  findings feed the portfolio.

## 9. Scope adjustment and maintenance

* Downscope when a smaller boundary preserves the original failure mechanism and
  improves diagnostics.
* Upscope when real dependency, artifact, platform, or assembled behavior was
  essential to the failure.
* Add **contract (L3-T7)** and **integration (L3-T3)** evidence for boundary or
  compatibility defects.
* Add **system (L3-T4)** evidence for packaging, deployment, wiring, and complete
  workflow defects.
* Add **generative evidence (L3-T6)** when the incident is one member of a broad
  input or sequence class.
* Add **operational evidence (L3-T15)** when recurrence must also be detected or
  mitigated in a deployed environment.
* Remove or revise a regression when its obligation is intentionally retired,
  but retain the decision context where historical understanding matters.

## 10. Outputs

* protected behavior and failure-mode inventory,
* issue, incident, or compatibility links,
* minimized reproductions and generated counterexamples,
* regressions missing for important learned failures,
* tests to downscope, upscope, merge, rewrite, or remove,
* broader contract, generative, integration, system, quality-attribute, or
  operational follow-up,
* review and retirement conditions for temporary obligations.
