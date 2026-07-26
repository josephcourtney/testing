# Running the reference project

This directory is a small runnable demonstration of the repository's testing
contracts. It is intentionally separate from the dated case study in
`../case_study/`.

The exact command and marker tables are generated in `generated-reference.md`
from the `justfile` and `pyproject.toml`; `just docs-check` fails if they drift.

## Setup and trusted evidence

Install `uv` and `just`, then run:

```console
just setup
just check
```

`just test` always selects `not quarantined`, writes the raw pytest report to
`.cache/evidence/pytest-full.json`, and writes normalized version-5 evidence to
`.cache/evidence/full.json`. A nonzero pytest exit, an invalid structural scope,
an incomplete requirement, a quarantined test, an altered full selection, or a
non-passing test makes that evidence fail.

Partial runs use `.cache/evidence/partial.json` and cannot overwrite trusted
evidence:

```console
just test-fast
just test-marker "unit and regression"
just test-quarantined
```

Every test has exactly one structural scope: `unit`, `component`, `integration`,
or `system`. Purpose markers such as `regression`, `contract`, and `smoke`, and
technique markers such as `property_based` and `fuzz`, are independent
dimensions.

## Artifact and release evidence

```console
just test-wheel
just performance
just compatibility
just release-check /path/to/compatibility-evidence
```

The wheel check installs the built artifact in an isolated virtual environment
outside the source tree. Compatibility evidence is accepted only when every
required matrix cell has the same revision and configuration digests as the
current trusted run. `release-check` runs every obligation and records all step
outcomes in `.cache/release.json`; it does not stop after the first failure.

The numeric latency budget belongs to `metric-specifications.json`. The
repository-wide guidance defines what a metric specification must contain but
does not prescribe this example project's number.

Legacy version-4 evidence can be inspected with
`uv run python -m scripts.test_evidence describe FILE`, but cannot satisfy a
gate.
