<!--
TESTING-GUIDANCE-REVIEW: document-level annotation

Problems identified:
- This project-specific harness can be mistaken for universal policy because commands, markers, cadence, and thresholds are stated prescriptively.
- The marker expression `unit or component or contract and not slow` is ambiguous to readers without explicit Boolean grouping.

Proposed fixes:
- Label the entire document as a local implementation of the general guidance.
- Use one structural scope plus independently composable purpose, technique, and resource markers.
- Add explicit parentheses to compound marker expressions and document which commands produce complete versus partial evidence.

Review rule: preserve the original document text. Apply any proposed fix only after explicit review.
-->
# Local Testing Guide

This page describes the implemented local workflow for the broader policy in
`notes/TESTING.md` and the procedures in `notes/testing/README.md`. `just help`
is the authoritative command reference.

## Command map

| Command | Purpose |
| --- | --- |
| `just test` | Run the unfiltered full suite with coverage and refresh canonical test artifacts. |
| `just test --fast` | Run every test except those marked `slow`. |
| `just test --marker "unit and not slow"` | Run a pytest marker expression without remembering raw pytest syntax. |
| `just test --durations 25` | Run the suite and report the 25 slowest setup, call, or teardown phases. |
| `just test --dev [selection]` | Use testmon and conditional xdist for an editing loop; coverage is disabled. |
| `just test tests/path.py::test_name` | Run a path or node-id selection. |
| `just test --failing` | Re-run pytest's last-failed selection. |
| `just check` | Run the hard local regression gate. |
| `just measure` | Refresh full-suite evidence and print detailed metrics and uncovered lines. |
| `just summary` | Read fresh standard artifacts and report coverage, runtime, scope counts, flaky quarantines, and other tracked quality signals. |
| `just test-wheel` | Build and inspect the distributions, then test the exact wheel outside the checkout. |
| `just health` | Record a comparable full-suite health run in ignored local history. |
| `just performance` | Measure the fixed local performance cases and apply the calibrated gate when available. |
| `just compatibility` | Export evidence for the current OS and Python matrix cell. |
| `just compatibility-check <directory>` | Validate and aggregate portable compatibility evidence. |
| `just mutation` | Run the maintained high-risk mutation cohort and enforce the mutation quality gate. |
| `just release-check <directory>` | Produce a complete release decision from all local and imported evidence. |

`--quiet`, `--logs`, and `--debug` are mutually exclusive output modes. Options
may be combined, for example:

```bash
just test --marker "contract or system" --durations 10 --logs
```

## Scope markers

Every collected test must have exactly one structural marker: `unit`,
`component`, `integration`, `system`, or `contract`. Collection fails with all
violating node IDs when a marker is missing or multiple structural markers are
present. Cross-cutting markers such as `property_based`, `snapshot`, `smoke`,
`regression`, and `slow` may be added independently.

Test modules are organized under scope-aligned `tests/unit`, `tests/component`,
`tests/property`, `tests/contract`, and `tests/system` directories:

| Directory | Structural marker | Current role |
| --- | --- | --- |
| `tests/unit` | `unit` | Pure normalization, audit policy, rendering, configuration, and model behavior. |
| `tests/property` | `unit` plus `property_based` | Bounded generated checks for deterministic codec and normalization invariants. |
| `tests/component` | `component` | Typer acquisition, target loading, declaration enrichment, and in-process CLI workflows. |
| `tests/contract` | `contract` | Public Python exports and versioned snapshot/declaration document contracts. |
| `tests/system` | `system` | Fast development-console smoke and regression workflows treating `clinspect` as a black box. |

Add `tests/integration` only when the product gains a genuine external
integration boundary. Module-level markers remain the enforced source of truth
for collected cases.

## Isolation and process boundaries

Network sockets are disabled by default through `pytest-socket`. A test that
genuinely exercises a real network boundary must use an appropriate structural
scope, opt in narrowly with `socket_enabled`, and own the isolation and cleanup
of its external resource.

Component CLI tests invoke the Typer application in process and assert exit
codes plus captured stdout/stderr. Source-tree system tests invoke the current
development console with direct argument vectors, bounded timeouts, and
captured output. `just test-wheel` separately builds the package, installs the
exact reported wheel and an unrelated target distribution into a temporary
environment, changes outside the checkout, clears repository import paths, and
exercises the installed CLI plus an independent public-API consumer. Loader
component tests retain the product's subprocess boundary because process
isolation is part of that component's contract.

Use `tmp_path` for ephemeral configuration, generated documentation, and
snapshot artifacts. These small real files make path resolution and artifact
portability clearer than a mocked filesystem.

The current product has no concurrent runtime workflow under test, so the suite
does not carry speculative thread or async coordination fixtures. If concurrency
is introduced, tests must assert causality with events, barriers, or queues;
deadline every wait; propagate background exceptions; and avoid raw sleeps.
Introduce shared helpers only with the first concrete consumer.

## Test artifacts

Only an unfiltered `just test` run refreshes `.coverage` and the canonical
full-suite pytest outcome artifact used by quality gates. Marker expressions,
path selections, `--fast`, `--failing`, and `--dev` are partial runs; their
reports and coverage data are written under `.cache/quality/` so they cannot
overwrite authoritative full-suite evidence.

The version-4 evidence document records the repository and environment
fingerprint, per-test outcomes and durations, structural scopes, requirement
IDs, artifact digests, and the final decision. Full comparable runs are copied
to ignored `.cache/test-history/` storage; partial runs cannot contaminate that
history. `just summary` reports requirement coverage, slow tests, trends,
quarantines, compatibility cells, and release-evidence freshness.

Compatibility reports are portable. Run `just compatibility` in each required
environment, copy the resulting report directory to the release host, and pass
the aggregate directory to `just compatibility-check` or `just release-check`.
Reports with a different revision, lock hash, platform cell, invalid schema, or
artifact digest are rejected.

Performance remains measurement-first. The harness warms up twice and records
seven samples for each fixed case. A baseline is calibrated only after ten
comparable clean runs with coefficient of variation at most 10%. Thereafter a
release regression requires both a median above 115% of baseline and an
absolute increase above 100 ms. Unlike environment fingerprints are never
combined.

The maintained mutation cohort currently covers target parsing/resolution and
Typer default/type normalization. It must retain at least an 80% score and zero
`no_tests` mutants. Expanding the cohort is tracked separately so the gate
describes the code it actually mutates.

Routine evidence and defect records remain ignored local state. Portable
compatibility reports are the supported evidence-transfer boundary for the
current release workflow. Committed waivers must name their scope, owner,
reason, mitigation, and expiry or revisit trigger; expired or unowned waivers
fail the release decision.
