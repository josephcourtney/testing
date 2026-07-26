# L2-P2 — Feature Development / Alpha Confidence Profile

## 1. Profile role

This is a lifecycle confidence profile. It describes default expectations for
rapid development while interfaces and implementation are still changing. It
does not make a fixed inventory of test types universally mandatory.

Apply `L1.md` first. Select scopes, purposes, techniques, and environments from
the changed claims, failure modes, architecture, and decision. An already
material integration, security, privacy, accessibility, performance, data, or
operational risk is not deferred because the project is in development.

## 2. Profile intent

**Goal:**
Establish correctness of newly introduced or modified behavior while enabling
rapid iteration.

**Primary risks addressed:**
Incorrect core logic, misunderstood acceptance conditions, incomplete behavior,
poorly controlled effects, fragile interfaces, and tests that impede useful
refactoring.

**Risks commonly deferred only when not yet material:**
Broad compatibility matrices, complete production-operational evidence,
production-scale load, and exhaustive system scenarios.

Terminology is defined by `glossary.md`; conceptual workflows such as TDD and
test-after development are selectable conventions described in
`automated_testing.md`.

---

## 3. Applicability

This profile applies when:

* implementing new features or workflows,
* modifying core business logic,
* performing significant refactors before stabilization,
* evolving interfaces that are not yet broadly committed,
* converting prototype findings into durable behavior.

Interfaces may still be provisional. Contract evidence written here should
state whether it represents an experimental agreement or a supported
commitment.

---

## 4. Assessment inputs

Record:

* changed responsibilities and invariants,
* known acceptance conditions,
* affected public or internal interfaces,
* collaborators and external-effect boundaries,
* configuration and environment variants,
* failure modes likely to be introduced by the change,
* which evidence must remain fast enough for the editing and merge loops.

## 5. Default evidence expectations

These are profile defaults to evaluate, not categories to create without a real
claim or boundary.

### Strong defaults

* **Local behavioral evidence** for all materially changed core logic and
  invariants, commonly at unit scope.
* **Component evidence** for non-trivial subsystem collaboration through a
  supported interface.
* **Acceptance evidence** for known product or stakeholder conditions.
* **Regression evidence** for non-trivial bug fixes or learned failure modes.
* **Strict static and test configuration** where silent misconfiguration could
  invalidate development feedback.

### Conditional evidence

Use when the change or architecture makes the corresponding failure mode
material:

* contract evidence for evolving or independently consumed interfaces,
* integration evidence for real SQL, protocol, framework, process, service, or
  platform semantics,
* system evidence for installed artifacts or assembled behavior,
* property-based, stateful, differential, or metamorphic evidence for broad or
  sequential domains,
* observability evidence for diagnostics relied upon during development or
  operation,
* snapshots for large stable reviewable outputs,
* security, privacy, data-quality, accessibility, usability, performance,
  resilience, or recovery evidence.

### Workflow conventions

A team may use TDD, acceptance-test-driven development, test-after development,
or exploratory prototyping. The chosen workflow should improve learning and
feedback; it is not itself evidence that the result is correct.

### Conditional decision rule

When expected evidence is omitted, record:

* the claim and failure mode affected,
* why omission is acceptable for the current decision,
* available mitigation or substitute evidence,
* owner,
* revisit trigger, often interface stabilization, external use, L2-P3, or
  release.

---

## 6. Explicit default non-requirements

This profile does not by itself require:

* a broad end-to-end suite,
* production-scale performance testing,
* chaos or disaster-recovery exercises,
* complete compatibility matrices,
* a universal coverage or mutation target,
* TDD or any particular mocking style.

Each may nevertheless be required by L1 when it addresses a material risk.

---

## 7. Procedure

1. Identify changed responsibilities, claims, and acceptance conditions.
2. Identify affected boundaries, configurations, users, data, and operational
   behavior.
3. Choose the least costly scopes that preserve the relevant semantics.
4. Add nominal, boundary, invalid, and critical failure cases.
5. Add generated or model-based evidence where selected examples undersample
   the domain.
6. Exercise real boundaries when substitutes cannot establish the claim.
7. Keep rapid-feedback evidence deterministic and diagnostically useful.
8. Verify that tests fail when the intended behavior is removed or plausibly
   broken.
9. Record excluded semantics and the higher-scope or later-cadence evidence that
   covers them.
10. Reassess after material refactoring or interface change.

## 8. Compliance criteria

The profile is satisfied when:

1. All materially changed responsibilities have credible evidence.
2. Known acceptance conditions are executable or otherwise demonstrable.
3. Tests assert observable behavior and localize failures at a useful level.
4. External effects and variability are controlled without removing relevant
   semantics.
5. Interface commitments and provisional assumptions are distinguishable.
6. No unacknowledged high-risk gap remains.
7. Complete and partial evidence cannot be confused.

## 9. Assessment

1. Review the L1 claim and failure-mode map.
2. Map each changed responsibility to evidence.
3. Apply every relevant L3 procedure and record deviations.
4. Review rapid-loop runtime, determinism, and diagnostics.
5. Identify evidence that must be added or strengthened before stabilization.
6. Record outcome: pass, conditional pass, fail, exploratory finding, or risk
   acceptance.

## 10. Forward rules

* Durable tests written here persist as regression assets only while their
  obligation remains relevant.
* Provisional contracts must be confirmed, revised, or retired as interfaces
  stabilize.
* Documented gaps must be revisited when their trigger occurs.
* Short-term testing shortcuts must be explicit and time-bounded.
* Production-derived defects or user findings should update both the evidence
  portfolio and the risk model.

## 11. Outputs

Retain the common L1 record plus these profile-specific details:

* changed-responsibility and invariant map,
* acceptance-condition map,
* evidence by scope, purpose, and technique,
* supported interface commitments,
* rapid-feedback and merge-gate commands,
* provisional interfaces and their review triggers.
