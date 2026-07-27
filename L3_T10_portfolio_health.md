# L3-T10 — Evidence Portfolio Health

## 1. Purpose

Assess whether a test portfolio remains trustworthy and usable as a socio-technical system. This procedure evaluates feedback latency, determinism, diagnostic quality, maintenance cost, and coverage of material risks.

Metric definitions and thresholds are governed separately by **L3-T11**.

## 2. Applicability

Apply:

* during stabilization, production, and maintenance assessments,
* when runtime, flakiness, quarantine, or maintenance burden changes,
* after large test or architecture refactors,
* before relying on an evidence portfolio or one of its suites as a release
  gate.

## 3. Health dimensions

### Feedback latency

Assess whether each workflow receives evidence soon enough to affect the decision: editing, merge, scheduled verification, release, and production operation.

### Determinism and reproducibility

Assess intermittent outcomes, shared state, hidden ordering, uncontrolled time or randomness, environment sensitivity, retries, and inability to reproduce failures.

### Signal and localization

Assess whether failures distinguish product behavior, dependency behavior, environment problems, and harness defects; whether assertions are legible; and whether retained diagnostics are sufficient.

### Fidelity and control

Assess whether doubles, simulations, fixtures, and test environments preserve the semantics required by the risk, and whether rare or adverse conditions remain controllable.

### Maintainability

Assess churn under behavior-preserving refactors, fixture complexity, obsolete regressions, duplicated scenario coverage, snapshot noise, and ownership of infrastructure.

### Risk coverage

Assess whether critical responsibilities, boundaries, contracts, user journeys, security properties, data behavior, accessibility obligations, and operational claims have credible evidence. Do not infer this solely from line coverage or test counts.

### Evidence integrity

Assess whether complete and partial runs are separated, evidence is fresh, artifact and environment identities are recorded, quarantines are excluded from unsupported claims, and incompatible measurements are not combined.

## 4. Assessment procedure

1. Identify the decisions and cadences the portfolio and its suites are
   intended to support.
2. Collect comparable run histories, failure classifications, runtimes, quarantines, and maintenance observations.
3. Review a sample of tests at each important scope and purpose for oracle quality and fidelity.
4. Map critical risks to existing evidence and identify gaps or redundant portfolios.
5. Diagnose root causes rather than classifying every symptom as “flaky” or “slow.”
6. Recommend scope changes, harness improvements, contract alignment, fixture reduction, selective removal, or cadence changes.
7. Apply L3-T11 before using any quantitative metric as a gate.
8. Record health status, owners, and remediation triggers.

## 5. Classification

* **Healthy** — evidence is trusted, timely, sufficiently localizing, and aligned with the risks it supports.
* **Degraded** — bounded issues exist, but their effects and mitigations are explicit and the remaining evidence supports the stated decisions.
* **Unhealthy** — results are unreliable, routinely ignored, materially stale, non-reproducible, or too weakly connected to the required claims to support decisions.

## 6. Gating guidance

Fail a decision when portfolio-health problems invalidate the evidence needed
for that decision, for example:

* retries or nondeterminism make a critical gate untrustworthy,
* the complete suite cannot be distinguished from a selected run,
* evidence was produced for a different artifact or non-comparable environment,
* a critical boundary is represented only by an unvalidated fake,
* failures are so opaque that pass/fail status cannot be interpreted reliably.

Use conditional pass only when the effect is bounded, the unsupported claims are identified, mitigation is active, and remediation is owned and time-limited.

## 7. Outputs

* health classification and supported decisions,
* diagnosed causes of flake, slowness, brittleness, or weak fidelity,
* critical risk-to-evidence gaps,
* tests to remove, rewrite, move, or supplement,
* harness and evidence-integrity improvements,
* metric definitions requiring L3-T11 review.
