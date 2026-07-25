# Example Production Readiness Assessment

This is an illustrative project-specific assessment applying L1, L2-P4, and the relevant L3 procedures. It is not a universal checklist.

## Decision scope

Record:

* release revision and artifact digests,
* supported platforms and runtimes,
* deployment environment and configuration,
* user and operator populations,
* rollout and rollback plan.

## Risk-driven evidence

| Claim or risk | Evidence | Status |
| --- | --- | --- |
| Functional and contract behavior | Complete trusted tests, installed-artifact verification, provider and consumer checks | Pass / fail / conditional |
| Packaging and installation | Archive inspection and clean-environment system tests | Pass / fail |
| Security and supply chain | Threat-relevant tests, dependency and secret scans, artifact verification | Pass / fail / waived |
| Compatibility | Same-revision evidence for each supported matrix cell | Pass / fail / not applicable |
| Performance and capacity | L3-T11 metric specification and comparable measurements | Pass / conditional / fail |
| Data integrity and migration | Migration, rollback, backfill, and consistency evidence | Pass / not applicable |
| Accessibility and usability | Automated and human evidence for critical tasks | Pass / conditional / not applicable |
| Observability and operability | Signals, alert path, runbooks, deployment diagnostics | Pass / fail |
| Resilience and recovery | Fault, rollback, backup restoration, failover, and recovery evidence | Pass / conditional / not applicable |

Each not-applicable result requires rationale. Each waiver identifies scope, mitigation, owner, expiry, and removal condition.

## Evidence validity

Release evidence must be:

* fresh for the release artifact,
* complete for its declared selection,
* comparable under documented rules,
* independent of source-tree leakage where packaging matters,
* separated from quarantined evidence,
* retained with environment and configuration identity.

## Operational controls

Record:

* deployment stop conditions,
* canary or staged-rollout criteria,
* alert and diagnosis expectations,
* rollback trigger and tested procedure,
* backup restoration status,
* recovery time and data-consistency observations,
* incident owner and escalation path.

## Release decision

Classify the result as pass, conditional pass, fail, or risk acceptance.

A conditional pass must state rollout limits, compensating controls, owner, and revisit trigger. Missing material compatibility, recovery, security, or operational evidence is a failure unless explicitly accepted by an authorized owner.
