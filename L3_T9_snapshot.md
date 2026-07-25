# L3-T9 — Snapshot and Golden Testing: Design, Writing, Evaluation

## 1. Purpose

Compare a canonicalized output or artifact with a reviewed stored baseline when a semantic diff is a more comprehensible and economical oracle than extensive individual assertions.

Snapshotting is a convenience technique, not a structural scope or a substitute for understanding expected behavior.

## 2. Applicability

Use when:

* output is large but structurally stable,
* a reviewer can realistically interpret the diff,
* stored representation is part of the useful oracle,
* targeted assertions alone would be less clear or maintainable.

Avoid when output is highly volatile, reviewers cannot validate changes, or a small set of direct assertions expresses the contract more clearly.

## 3. Canonical representation

Snapshot the minimal meaningful view:

* normalize irrelevant ordering,
* redact or replace nondeterministic identifiers, timestamps, and paths,
* normalize formatting and platform variation,
* prefer explicit presentation or interchange models over private structures,
* keep artifacts readable and diff-friendly.

## 4. Semantic obligations

Add targeted assertions for critical semantics that could be obscured by a large diff, such as schema version, required fields, safety properties, or compatibility obligations.

A broad snapshot must not replace practical direct assertions.

## 5. Update policy

Updating a snapshot means accepting a behavior change.

Snapshot changes must:

* be intentional,
* be reviewed like code,
* explain relevant semantic changes,
* avoid unconditional bulk regeneration,
* preserve ownership and provenance where consequential.

## 6. Writing procedure

1. State the claim and why a snapshot is the appropriate oracle.
2. Define canonicalization.
3. Produce the minimal stable artifact.
4. Add critical semantic assertions.
5. Verify that a relevant change produces an interpretable failure.
6. Define review and update workflow.
7. Record platform or environment limitations.

## 7. Evaluation

Good snapshot evidence:

* produces small, interpretable diffs,
* compares canonical public or supported representations,
* complements semantic assertions,
* changes only for meaningful behavior,
* remains reviewable at its actual update frequency.

Red flags include snapshot churn, unreadable artifacts, hidden volatile fields, private implementation dumps, and approvals performed without semantic review.

## 8. Outputs

* snapshot inventory and ownership,
* canonicalization rules,
* semantic assertions paired with each artifact,
* snapshots to narrow, replace, or remove,
* update and review policy.
