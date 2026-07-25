# L2-P5 — Maintenance Confidence Profile

## 1. Intent

Safely evolve a live system using changed claims, incident history, production observations, and decaying operational evidence.

## 2. Change-impact assessment

For every maintenance change, identify:

* changed responsibilities and user-visible behavior,
* affected boundaries, consumers, artifacts, data, and migrations,
* dependency, platform, configuration, or infrastructure changes,
* related incidents, defects, support findings, and telemetry,
* operational evidence that may have become stale,
* obsolete tests or controls whose underlying obligation no longer exists.

## 3. Default confidence posture

Use:

* focused regression evidence for learned failure modes,
* localizing evidence for changed logic,
* contract and compatibility revalidation when interfaces or versions change,
* integration or system evidence when real boundaries or assembled behavior change,
* migration, rollback, recovery, and monitoring evidence when operational state changes,
* exploratory work for surprising or poorly understood behavior,
* suite-health review when runtime, flake, maintenance burden, or fidelity changes.

Regression tests should not accumulate indefinitely without ownership or continued relevance.

## 4. Governance defaults

* Every change links to the claims and risks it affects.
* Incident-derived evidence records the trigger, symptom, and protected obligation.
* Quarantines, waivers, and temporary controls remain time-bounded.
* Operational and compatibility evidence is repeated when its validity decays.
* Stale, redundant, or misleading evidence is removed or revised.

## 5. Outcome

Pass requires evidence appropriate to the actual impact of the change. Conditional pass and risk acceptance require explicit unsupported claims, mitigation, owner, and revisit trigger.
