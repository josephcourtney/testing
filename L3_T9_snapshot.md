# L3-T9 — Snapshot and Golden Testing: Design, Writing, Evaluation

## 1. Purpose

Capture and compare a **canonical, reviewed representation** of an output or
artifact to detect unintended change when a diff is a more comprehensible and
economical oracle than an extensive set of individual assertions.

Typical subjects include JSON, HTML, rendered text, compiler output, schemas,
manifests, generated documents, render trees, public declarations, and other
large but structurally stable artifacts.

Snapshotting is a technique, not a structural scope or a primary correctness
strategy. A snapshot test may be unit-, component-, integration-, or
system-scoped and may serve regression, contract, acceptance, compatibility, or
another purpose.

## 2. Applicability

Use snapshot or golden testing when:

* output is too large or verbose for clear field-by-field assertions,
* the output has a stable, reviewable canonical form,
* diffs are meaningful and actionable,
* broad representation changes matter to a consumer or reviewer,
* the snapshot complements precise assertions for critical semantics,
* a stored artifact is itself a useful contract or characterization reference.

Avoid when:

* targeted behavioral assertions are feasible and clearer,
* output contains high-churn or environment-dependent values that cannot be
  normalized meaningfully,
* reviewers cannot realistically understand the diff,
* the snapshot would mask the intended behavior or failure mode,
* raw internal structures would couple the test to implementation details,
* updating the snapshot would become a routine substitute for investigation.

### 2.1 When not to use this technique

Do not rely on snapshots when:

* a small number of semantic assertions fully expresses the contract,
* volatile timestamps, identifiers, paths, ordering, addresses, or formatting
  dominate the artifact,
* generated output contains secrets, personal data, or environment-specific
  content that should not be retained,
* a screenshot or image diff lacks tolerances, accessibility checks, or a
  human-review process suitable for the claim,
* exact equality is stricter than the actual compatibility obligation,
* the stored baseline has no owner or source of truth.

## 3. Design rules

### 3.1 Define the snapshot claim

Record:

* what behavior, contract, representation, or compatibility obligation the
  snapshot supports,
* structural scope and purpose,
* producer and consumers where applicable,
* which fields or presentation details are meaningful,
* which variation is irrelevant and should be normalized,
* who reviews changes and under what conditions a baseline may be updated.

A snapshot failure indicates a difference. It does not by itself establish
whether the current output or stored baseline is correct.

### 3.2 Snapshot only stable, meaningful views

Prefer the minimal stable view that preserves the intended signal:

* stable field and item ordering,
* normalized whitespace and formatting,
* canonical encodings and line endings,
* redaction or replacement of volatile timestamps, identifiers, paths, ports,
  addresses, and random values,
* removal of irrelevant metadata,
* explicit selection of public or consumer-visible fields,
* deterministic rendering settings.

Prefer an explicit presentation, declaration, or serialization model over raw
private object state.

Canonicalization must not remove variation that is part of the claim. If
ordering, timestamps, identifiers, paths, or formatting are contractual, retain
and assert them deliberately.

### 3.3 Pair snapshots with semantic assertions

Add targeted assertions for critical obligations such as:

* schema or format version,
* required fields and relationships,
* safety- or security-relevant content,
* public names and compatibility guarantees,
* absence of secrets or unstable paths,
* important counts, categories, statuses, or invariants,
* successful decoding or validation,
* round-trip or deterministic re-encoding where appropriate.

A broad snapshot must not be the only oracle when a small semantic failure could
be overlooked in a large diff.

### 3.4 Treat baselines as reviewed artifacts

Snapshots should be:

* readable and diff-friendly,
* version-controlled or otherwise versioned,
* generated through a documented command or harness,
* tied to a known producer, configuration, and environment,
* reviewed like code because an update changes expected behavior,
* owned and pruned when no longer valuable.

Updating a snapshot is an acceptance decision, not a cleanup operation. Review
whether the changed behavior is intended, compatible, complete, and safe before
updating the baseline.

### 3.5 Sensitive and binary artifacts

For sensitive output:

* avoid retaining real secrets or personal data,
* use synthetic or irreversibly redacted inputs,
* validate the redaction itself,
* control access and retention where an artifact must remain restricted.

For binary or visual artifacts:

* retain a reviewable derivative or metadata where practical,
* define tolerances and comparison method,
* distinguish meaningful changes from renderer, font, platform, or compression
  noise,
* supplement image equality with semantic and accessibility assertions when
  those matter.

### 3.6 Baseline provenance and comparability

Record:

* producer revision and artifact,
* tool and serializer versions,
* configuration, locale, timezone, platform, and rendering environment,
* canonicalization version,
* input data or fixture identity,
* whether comparisons across environments are valid.

Do not accept churn caused only by an uncontrolled or non-comparable environment.

## 4. Writing procedure

1. State the claim and why a snapshot is a useful oracle.
2. Select structural scope and purpose independently.
3. Identify the minimal public or consumer-visible representation.
4. Define canonicalization:
   * stable sorting,
   * volatile-field redaction,
   * path and environment normalization,
   * whitespace, encoding, and formatting normalization.
5. Add targeted assertions for critical semantics before broad comparison.
6. Produce the baseline from a known artifact, input, configuration, and
   environment.
7. Store it in a readable, diff-friendly, appropriately protected form.
8. Verify that a plausible semantic change produces a clear failure.
9. Define the update command and review process.
10. Record ownership, provenance, and conditions for pruning or regeneration.

## 5. Evaluating an existing snapshot test

A good snapshot test:

* uses a snapshot where diff review is genuinely the clearest oracle,
* snapshots a canonical, stable, public or consumer-relevant representation,
* includes targeted semantic assertions,
* produces small, interpretable diffs tied to intended changes,
* records provenance and comparison conditions,
* treats updates as reviewed behavior changes,
* avoids secrets and uncontrolled environment data,
* fails only on meaningful representation or contract changes,
* has a clear owner and maintenance purpose.

Red flags:

* frequent churn with no semantic relevance,
* volatile timestamps, UUIDs, paths, ports, addresses, or ordering without
  canonicalization,
* snapshots used as a one-test-to-cover-everything escape hatch,
* very large baselines reviewers cannot realistically validate,
* raw private object dumps coupled to implementation details,
* unconditional or bulk update commands used after failures,
* important semantic changes hidden in noisy diffs,
* exact equality imposed where compatibility permits variation,
* missing baseline provenance,
* real sensitive data committed to the repository.

## 6. Evaluating the snapshot suite

Check:

* **Necessity** — each snapshot materially improves the oracle or review process.
* **Signal** — diffs are meaningful, localized, and actionable.
* **Canonicalization** — irrelevant variation is removed without erasing
  contractual behavior.
* **Semantic coverage** — critical obligations also have focused assertions.
* **Contract fit** — exact equality does not overstate the compatibility promise.
* **Provenance** — producer, input, environment, tool, and canonicalization
  identity are known.
* **Security and privacy** — no inappropriate sensitive content is retained.
* **Maintenance** — update frequency, ownership, review quality, and snapshot
  size remain reasonable.
* **Obsolescence** — stale, redundant, unreadable, or low-value snapshots are
  removed or replaced.
* **Scope and purpose** — snapshots are not treated as a separate structural
  level.

## 7. Scope and technique adjustment

* Replace a snapshot with targeted assertions when a compact semantic oracle is
  clearer.
* Reduce a broad snapshot to a smaller presentation model when noise dominates.
* Retain the snapshot but add **contract (L3-T7)** evidence when the artifact is
  a published interface.
* Add **regression (L3-T5)** context when the baseline protects a learned failure
  mode.
* Add **system (L3-T4)** or installed-artifact evidence when source-tree output
  does not establish packaged behavior.
* Use dedicated visual, usability, or accessibility evaluation when image or UI
  correctness cannot be reduced to a stable serialized representation.

## 8. Outputs

* snapshot and golden-artifact inventory,
* claim, scope, purpose, owner, and consumer for each baseline,
* canonicalization and redaction specification,
* targeted semantic assertions to add,
* provenance and comparability information,
* snapshots to shrink, replace, split, regenerate, or remove,
* update and review workflow,
* security, privacy, contract, compatibility, or installed-artifact follow-up.
