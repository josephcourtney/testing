# L3-T5 — Regression Testing: Design, Writing, Evaluation

## 1. Purpose

Prevent loss of previously established behavior or reintroduction of a learned failure mode.

Regression is a purpose composable with any structural scope and technique. A **sanity check** is a separate narrow plausibility check used before broader evaluation; it is not synonymous with regression.

## 2. Applicability

Use regression evidence when:

* a defect or incident revealed a failure mode worth preserving,
* a compatibility, migration, or operational obligation was learned,
* characterization of legacy behavior is needed before change,
* a high-impact behavior requires a durable guardrail.

Do not add a regression merely to duplicate existing evidence without identifying a distinct protected obligation.

## 3. Define the protected obligation

Record:

* trigger and observed symptom,
* intended behavior,
* root cause as understood,
* affected claim, user, boundary, and environment,
* structural scope required to preserve the original failure mechanism,
* incident or issue reference where useful,
* conditions under which the regression can be retired.

Characterization evidence records current behavior but does not automatically declare it desirable.

## 4. Design rules

* Use the least costly scope that preserves the failure mechanism, not merely the visible symptom.
* Make the test fail on the defective behavior where practical.
* Avoid overfitting to the implementation of the fix.
* Add contract, integration, system, or operational evidence when the failure arose from those semantics.
* Keep important minimized counterexamples visible.
* Remove or revise obsolete regressions when the protected obligation changes.

## 5. Writing procedure

1. Reproduce and minimize the failure.
2. State the protected claim and failure mode.
3. Select scope, technique, and resources.
4. Verify the evidence distinguishes defective from corrected behavior.
5. Add diagnostic context and relevant identifiers.
6. Link related contract, compatibility, monitoring, or recovery evidence.
7. Define ownership and retirement conditions.

## 6. Evaluation

Good regression evidence:

* would detect a plausible recurrence,
* preserves the relevant semantics,
* remains stable under behavior-preserving refactoring,
* localizes the protected failure sufficiently,
* records why it exists,
* remains relevant to a current obligation.

Red flags include large reproductions without need, tests that only verify implementation details, indefinite accumulation, flaky incident tests, and “regression suites” defined only as every existing test.

## 7. Outputs

* protected-obligation and incident map,
* minimized reproductions,
* missing regressions for important learned failures,
* obsolete or redundant regressions,
* scope and complementary-evidence recommendations.
