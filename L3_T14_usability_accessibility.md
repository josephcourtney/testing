# L3-T14 — Usability and Accessibility Testing

## 1. Purpose

Evaluate whether intended users can perceive, understand, navigate, and complete important tasks, including users with disabilities and users operating under realistic constraints.

Automated conformance checks are useful evidence but do not by themselves establish usability or accessibility.

## 2. Applicability

Use when:

* people interact with a UI, CLI, documentation, API, device, report, or workflow,
* misunderstanding or error would cause material cost or harm,
* accessibility standards or organizational obligations apply,
* a new or changed workflow affects task completion,
* user populations, locales, devices, assistive technologies, or environmental conditions vary.

## 3. Evidence types

* task-based moderated or unmoderated usability sessions,
* expert or heuristic review,
* accessibility conformance checks,
* keyboard-only and focus-order evaluation,
* screen-reader and assistive-technology evaluation,
* contrast, scaling, motion, localization, and reflow checks,
* comprehension testing for messages, documentation, and diagnostics,
* telemetry or support evidence interpreted with appropriate privacy controls.

## 4. Define users and tasks

Record:

* intended user groups and relevant abilities or constraints,
* critical tasks and unacceptable failure outcomes,
* devices, environments, assistive technologies, and locales,
* prior knowledge and terminology assumptions,
* success, error, recovery, and comprehension criteria.

Do not use a generic persona as a substitute for the actual population whose needs determine acceptance.

## 5. Procedure

1. Select critical tasks from the acceptance and risk map.
2. Identify user groups and accessibility conditions relevant to those tasks.
3. Run automated checks for mechanically detectable violations.
4. Perform keyboard, focus, scaling, screen-reader, contrast, motion, and localization evaluation where applicable.
5. Observe representative users or qualified evaluators completing tasks.
6. Capture completion, errors, hesitation, recovery, comprehension, and qualitative findings.
7. Separate defects, standards violations, design tradeoffs, and training or documentation gaps.
8. Prioritize findings by user impact and task criticality.
9. Convert stable mechanical obligations into regression checks while retaining human reevaluation for experiential claims.

## 6. Evaluation

Good usability and accessibility evidence:

* evaluates real tasks rather than isolated controls only,
* covers relevant user variation and assistive technology,
* distinguishes conformance from practical usability,
* records the observed environment and limitations,
* leads to testable design or content changes.

Red flags:

* claiming accessibility from an automated scanner alone,
* evaluating only the happy path,
* using internal staff as the sole proxy for unfamiliar users without acknowledging the limitation,
* measuring clicks or duration without examining errors and comprehension,
* treating documentation as a remedy for avoidable interaction defects.

## 7. Outputs

* user and task matrix,
* automated conformance results,
* manual and assistive-technology findings,
* task outcomes and observed failure modes,
* prioritized remediation,
* regression candidates and required future human reevaluation.
