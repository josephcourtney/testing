# L2-P2 — Development / Alpha Confidence Profile

## 1. Intent

Make changed responsibilities, known invariants, and acceptance conditions executable while preserving rapid feedback.

## 2. Default confidence posture

For each change:

* identify affected claims and failure modes,
* provide localizing evidence for changed logic,
* exercise collaboration at component scope when the subsystem boundary matters,
* add real-boundary evidence when correctness depends on infrastructure, framework, protocol, packaging, or platform semantics,
* record known acceptance conditions,
* protect material bug fixes with regression evidence,
* use exploratory work where behavior remains uncertain.

Unit or component scope is common but not mandatory when it would remove the relevant semantics.

## 3. Development conventions

TDD, test-after development, acceptance-test-driven development, solitary or sociable units, and directory layout are team conventions rather than confidence requirements.

## 4. Governance defaults

Expected controls include:

* a fast trusted developer workflow,
* strict test and tool configuration,
* clear separation of partial and complete evidence,
* no hidden quarantines or retries,
* explicit ownership of deferred evidence,
* provisional contract artifacts labeled as provisional.

## 5. Escalation

Apply stabilization or production-level fidelity early when a change affects a stable consumer, sensitive data, deployment behavior, security boundary, critical user journey, or operational obligation.

## 6. Outcome

Pass requires credible evidence for changed claims and no unacknowledged material gap. A conditional pass must identify unsupported claims, mitigation, owner, and revisit trigger.
