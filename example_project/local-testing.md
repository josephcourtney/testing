# Local Testing Guide

This page describes one **project-specific implementation** of the general
policy in `Overview.md`, the assessment procedure in `L1.md`, the L2/L3
procedures, and the Python guidance in `python_testing.md`.

`just help` is the authoritative command reference for the adopting project.
The command names, marker enforcement, test directories, thresholds, and tool
choices below are concrete examples rather than repository-wide requirements.

## Command map

| Command | Purpose and evidence status |
| --- | --- |
| `just test` | Run the unfiltered complete trusted suite with coverage and refresh canonical test artifacts. Quarantined tests must be excluded or reported separately rather than counted as trusted evidence. |
| `just test --fast` | Run every trusted test except those marked `slow`; this is a broad partial selection rather than the canonical complete artifact. |
| `just test --marker "unit and not slow"` | Run an explicit pytest marker expression without remembering raw pytest syntax; the result is partial evidence. |
| `just test --durations 25` | Run the selected suite and report the 25 slowest setup, call, or teardown phases. |
| `just test --dev [selection]` | Use testmon and conditional xdist for an editing loop; coverage is disabled and the result is partial. |
| `just test tests/path.py::test_name` | Run a path or node-id selection; the result is partial evidence. |
| `just test --failing` | Re-run pytest's last-failed selection for diagnosis; this does not replace a fresh complete run. |
| `just check` | Run the hard local regression gate: formatting, linting, type checking, security/static checks, and the declared trusted test selection. |
| `just measure` | Refresh complete-suite evidence and print detailed metrics and uncovered lines. |
| `just summary` | Read fresh standard artifacts and report coverage, runtime, structural-scope counts, quarantines, and other tracked quality signals. |
| `just test-wheel` | Build and inspect the distributions, then test the exact wheel outside the checkout. |
| `just health` | Record a comparable complete-suite health run in ignored local history. |
| `just performance` | Measure fixed local performance cases and apply the calibrated gate when available. |
| `just compatibility` | Export evidence for the current operating-system and Python matrix cell. |
| `just compatibility-check <directory>` | Validate and aggregate portable compatibility evidence. |
| `just mutation` | Run the maintained high-risk mutation cohort and enforce the project-specific mutation gate. |
| `just release-check <directory>` | Produce a complete release decision from all required local and imported evidence. |

`--quiet`, `--logs`, and `--debug` are mutually exclusive output modes. Options
may be combined, for example:

```bash
just test --marker "(contract or system) and not slow" --durations 10 --logs
```

The parentheses make the intended Boolean grouping explicit.

## Classification markers

Every collected functional test has exactly one primary structural marker:

* `unit`,
* `component`,
* `integration`, or
* `system`.

Collection fails with all violating node IDs when a primary structural marker is
missing or more than one primary scope is declared without an explicit project
exception.

Purpose markers compose independently, including:

* `contract`,
* `acceptance`,
* `regression`,
* `sanity`,
* `smoke`,
* `compatibility`,
* `security`,
* `performance`,
* `data_quality`,
* `observability`,
* `accessibility`,
* `usability`,
* `resilience`,
* `recovery`.

Technique markers may include `property_based`, `stateful`, `model_based`,
`differential`, `metamorphic`, `fuzz`, `snapshot`, and `fault_injection`.
Resource and execution markers may include `filesystem`, `process`, `db`,
`network`, `clock`, `configuration`, `environment`, `hardware`, `slow`,
`destructive`, and `quarantined`.

`contract` is not a structural marker. A contract check also declares the scope
at which it executes, such as `component + contract` or `system + contract`.

## Directory organization

The project's directories are navigation aids rather than the complete
classification source. A taxonomy-consistent layout is:

| Directory | Typical structural marker | Current role |
| --- | --- | --- |
| `tests/unit` | `unit` | Deterministic normalization, audit policy, rendering, configuration, model, and protocol logic. |
| `tests/component` | `component` | Typer acquisition, target loading, declaration enrichment, merging, and in-process CLI workflows. |
| `tests/integration` | `integration` | Real external or infrastructure semantics, added only when the product has such a boundary. |
| `tests/system` | `system` | Development-console and installed-artifact workflows treating `package_name` as a black box. |
| `tests/support` | none by itself | Shared helpers, factories, and harness code. |
| `tests/data` | none by itself | Static fixtures and reviewed artifacts. |

Property, snapshot, regression, and contract tests remain under their actual
structural scope, for example:

```text
tests/unit/test_codec_properties.py
tests/component/test_declaration_contract.py
tests/system/test_cli_schema_contract.py
```

Module-level markers remain the enforced source of truth for collected cases.

## Complete, partial, and quarantined evidence

The local harness must prevent selected or diagnostic runs from overwriting the
canonical complete artifacts.

* `just test` and the required release command write canonical complete evidence.
* `--fast`, `--dev`, marker, path, node-id, and last-failed selections write
  separate partial artifacts or no canonical artifacts.
* Quarantined tests run through a separate diagnostic command. They do not
  contribute to supported claims or cause a passing quarantine retry to be
  represented as trusted success.
* Imported compatibility and performance evidence is accepted only when revision,
  lockfile, configuration, workload, tool, and platform comparability rules hold.

## Isolation and process boundaries

Network sockets are disabled by default through `pytest-socket`. A test that
genuinely exercises real network semantics must opt in narrowly with
`socket_enabled`, declare an appropriate structural and resource classification,
and own the isolation and cleanup of its external resource.

Component CLI tests invoke the Typer application in process and assert exit
codes plus captured stdout and stderr. Source-tree system tests invoke the
current development console with direct argument vectors, bounded timeouts, and
captured output.

`just test-wheel` separately:

1. builds the package,
2. inspects the exact wheel and source distribution,
3. installs the reported wheel and an unrelated target distribution into a
   temporary clean environment,
4. changes outside the checkout,
5. clears repository import paths,
6. exercises the installed CLI and an independent public-API consumer,
7. retains artifact digests and environment identity.

Loader component tests retain the product's subprocess boundary because process
isolation is part of that component's contract. The use of a process resource
does not automatically make the test integration- or system-scoped.

Use `tmp_path` for ephemeral configuration, generated documentation, SQLite
files, and snapshot artifacts. Small real files can make path resolution,
encoding, atomic replacement, and artifact portability clearer than a mocked
filesystem. Add a `filesystem` resource marker when this distinction supports
selection or interpretation.

The current product has no concurrent runtime workflow under test, so the suite
does not carry speculative thread or async coordination fixtures. If concurrency
is introduced, tests must:

* assert causality with events, barriers, queues, or explicit hooks,
* deadline every wait,
* propagate background exceptions,
* clean up tasks and threads,
* avoid raw sleeps and scheduler luck,
* add repeated or systematic schedule exploration when race risk is material.

Introduce shared helpers only with the first concrete consumer.

## Project-specific metric and gate policy

The adopting project may retain exact thresholds, histories, and calibrated
rules in its implementation. Each gate must still satisfy L3-T11:

* define the decision,
* define population and denominator,
* identify workload, artifact, environment, and tool versions,
* separate natural variation from a practical regression,
* prevent partial or non-comparable data from contaminating the result,
* state the response, owner, and recalibration trigger.

The concrete coverage, mutation, flake, performance, and compatibility values in
the assessment examples are facts about that example project, not defaults for
other repositories.
