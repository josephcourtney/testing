# Local Testing Guide

This page is a project-specific example of applying the repository policy. It is not a universal command layout, marker scheme, cadence, or threshold set. `just help` is the authoritative command reference for the project it describes.

## Command map

| Command | Purpose |
|---|---|
| `just test` | Run the unfiltered full suite with coverage and refresh canonical test artifacts. |
| `just test --fast` | Run every test except those marked `slow`. |
| `just test --marker "unit and not slow"` | Run a pytest marker expression. |
| `just test --durations 25` | Report the slowest setup, call, or teardown phases. |
| `just test --dev [selection]` | Use test-impact selection for an editing loop; coverage is disabled. |
| `just test tests/path.py::test_name` | Run a path or node-id selection. |
| `just test --failing` | Re-run pytest's last-failed selection. |
| `just check` | Run the hard local regression gate. |
| `just measure` | Refresh full-suite evidence and print detailed measurements. |
| `just summary` | Report coverage, runtime, classifications, quarantines, and freshness. |
| `just test-wheel` | Build, inspect, install, and test the exact wheel outside the checkout. |
| `just health` | Record a comparable full-suite health run. |
| `just performance` | Measure the declared local performance cases and apply a calibrated gate when valid. |
| `just compatibility` | Export evidence for the current environment cell. |
| `just compatibility-check <directory>` | Validate and aggregate portable compatibility evidence. |
| `just mutation` | Run the maintained mutation cohort. |
| `just release-check <directory>` | Produce a release decision from local and imported evidence. |

## Classification

Every collected test has one primary structural scope marker:

* `unit`,
* `component`,
* `integration`, or
* `system`.

Purpose and technique markers are independent and may be combined with any appropriate scope:

* `contract`,
* `acceptance`,
* `regression`,
* `smoke`,
* `property_based`,
* `snapshot`,
* `security`,
* `performance`,
* `observability`,
* `slow`.

For example, a local schema compatibility check may be `component` plus `contract`; an installed-CLI compatibility check may be `system` plus `contract`; a generated normalization invariant may be `unit` plus `property_based`.

Directories organize the project for navigation but do not define the complete test meaning:

| Directory | Typical scope and purposes |
|---|---|
| `tests/unit` | Local behavior and invariants. |
| `tests/property` | Unit or component scope plus generative techniques. |
| `tests/component` | Public subsystem behavior. |
| `tests/contract` | Contract-purpose tests with an explicit structural scope. |
| `tests/system` | Black-box smoke, acceptance, regression, and contract checks. |
| `tests/integration` | Added only when real external semantics are part of the product boundary. |

Collection validates the structural scope independently from purpose and technique markers.

## Isolation and process boundaries

Network sockets are disabled by default through `pytest-socket`. A test that exercises a real network boundary opts in narrowly, declares integration or system scope, and owns isolation and cleanup.

Component CLI tests invoke the Typer application in process. Source-tree system tests invoke the development console with direct argument vectors, bounded timeouts, and captured output. `just test-wheel` builds the package, installs the exact reported wheel and an unrelated target distribution into a temporary environment, changes outside the checkout, clears repository import paths, and exercises the installed CLI plus an independent public-API consumer.

Use `tmp_path` for ephemeral configuration and artifacts when real filesystem semantics are part of the chosen boundary. These files are preferable to a mocked filesystem when path resolution and portability are the risk.

The current product has no concurrent runtime workflow under test, so it does not carry speculative coordination fixtures. If concurrency is introduced, tests should assert causality with events, barriers, or queues; deadline every wait; propagate background exceptions; and avoid raw sleeps.

## Evidence integrity

Only an unfiltered `just test` run refreshes `.coverage` and the canonical full-suite outcome artifact. Partial selections write under `.cache/quality/` and cannot overwrite authoritative evidence.

The evidence document records repository and environment identity, per-test outcomes and durations, classifications, requirement IDs, artifact digests, and the final decision. Comparable full runs are retained separately; partial runs cannot contaminate history.

Compatibility reports are portable and reject mismatched revisions, lock hashes, platform cells, schemas, or artifact digests.

## Project-specific metric definitions

The following are not general recommendations; they are local gates defined for this project's current harness and risk map.

### Performance

The harness warms up twice and records seven samples for each fixed case. A baseline is calibrated only after ten comparable clean runs with coefficient of variation at most 10%. A release regression then requires both a median above 115% of baseline and an absolute increase above 100 ms. Unlike environment fingerprints are never combined.

### Mutation

The maintained cohort covers target parsing/resolution and Typer default/type normalization. Its gate applies only to that declared cohort and operator configuration: at least 80% mutation score and zero `no_tests` mutants. Expanding the cohort is tracked independently.

These definitions must be reviewed under `../L3_T11_metrics.md` whenever the workload, cohort, environment, tool configuration, or release decision changes.

## Waivers

Committed waivers name their scope, owner, reason, mitigation, and expiry or revisit trigger. Expired or unowned waivers fail the decision whose evidence they weaken.
