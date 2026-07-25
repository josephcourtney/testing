# L3-T4 — System Testing: Design, Writing, Evaluation

## 1. Purpose

Provide evidence about the assembled product through a supported user- or operator-visible boundary.

System is a structural scope. **Smoke** describes a small critical-capability selection or purpose; **acceptance** describes stakeholder relevance; **end-to-end** describes a complete representative workflow. These terms are not interchangeable.

## 2. Applicability

Use system scope when the claim concerns:

* startup, shutdown, installation, or deployed wiring,
* behavior through a CLI, public API, browser, device, or operator interface,
* cross-component behavior visible only in the assembled artifact,
* a complete or representative workflow,
* production-like configuration or packaging.

Use lower scopes when they preserve the relevant semantics with better control or localization.

## 3. Define the system evidence

Record:

* exact assembled artifact,
* supported entrypoint,
* environment and configuration,
* dependencies retained or controlled,
* user or operator role,
* workflow and observable outcome,
* whether the selection is smoke, acceptance, compatibility, regression, or another purpose.

## 4. Design rules

* Exercise supported public boundaries.
* Assert stable user- or operator-visible behavior.
* Keep smoke selections small enough for their intended cadence.
* Do not infer stakeholder acceptance merely from system scope.
* Use readiness checks, bounded waits, isolated resources, and deterministic data.
* Retain diagnostics sufficient to distinguish product, environment, dependency, and harness failure.
* Test the installed or deployed artifact when packaging or deployment is part of the claim.

## 5. Writing procedure

1. State the system claim and purpose.
2. Identify artifact, environment, role, and entrypoint.
3. Bring up the product through supported mechanisms.
4. Drive a representative workflow.
5. Assert externally visible outcomes and critical diagnostics.
6. Verify teardown and cleanup.
7. Record controlled dependencies and residual differences from production.

## 6. Evaluation

Good system evidence:

* covers a material assembled-product claim,
* uses an appropriate public boundary,
* identifies artifact and environment,
* is stable and diagnosable,
* adds semantics unavailable at lower scope,
* remains small enough for its declared cadence.

Red flags include giant scenario matrices, hidden source-tree imports, fixed sleeps, volatile full-output assertions, unrecorded external state, and system tests used as a substitute for all localizing evidence.

## 7. Outputs

* system claim and workflow inventory,
* smoke and other purpose selections,
* artifact and environment identity,
* harness and diagnostic gaps,
* scenarios to move, split, or supplement.
