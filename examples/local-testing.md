# Example Local Testing Guide

This file is an illustrative project-specific implementation of the general policy. Its commands, markers, directories, and gates are not repository-wide requirements.

For normative policy see `../Overview.md`; for Python guidance see `../python_testing.md`. The adopting project's command runner remains authoritative for its implemented workflow.

## Command map

| Command | Purpose |
| --- | --- |
| `just test-dev [selection]` | Fast partial editing loop without canonical coverage. |
| `just test-fast` | Broad trusted selection excluding slow, destructive, and quarantined tests. |
| `just test-all` | Complete trusted selection; quarantined tests are excluded. |
| `just test-quarantined` | Diagnostic execution of quarantined tests. |
| `just check` | Formatting, linting, type checking, security checks, and required trusted tests. |
| `just test-wheel` | Build and test the exact wheel outside the checkout. |
| `just health` | Record comparable full-suite health evidence. |
| `just performance` | Collect performance evidence under a declared environment and workload. |
| `just release-check` | Validate fresh, complete, comparable release evidence. |

Partial selections must not overwrite canonical evidence artifacts.

## Classification

Every automated functional test has one primary structural marker:

* `unit`
* `component`
* `integration`
* `system`

Purpose markers compose independently, including `contract`, `acceptance`, `regression`, `smoke`, `compatibility`, and `security`.

Technique and resource markers also compose independently, including `property_based`, `snapshot`, `filesystem`, `process`, `db`, `network`, `slow`, and `quarantined`.

Example:

```python
@pytest.mark.component
@pytest.mark.contract
def test_export_document_matches_supported_schema(component):
    validate(component.export())
```

`component` identifies scope; `contract` identifies purpose.

## Directory layout

One possible layout is:

```text
tests/
  unit/
  component/
  integration/
  system/
  support/
  data/
```

Technique-specific tests remain under their actual structural scope. A feature-oriented layout is equally valid.

## Isolation and boundaries

Network access is disabled by default. Tests opt in only when real network semantics are part of the claim and the resource has bounded timeouts, isolation, and cleanup.

Use temporary paths for ephemeral filesystem evidence. Use the real production database engine when SQL dialect, transaction, migration, or extension semantics matter; otherwise a local implementation may remain within component scope.

System tests invoke the assembled or installed artifact through supported public entrypoints. Source-tree tests do not establish packaging correctness.

## Quarantine

Quarantined tests:

* run separately,
* do not contribute to gates or claims,
* have an owner and tracked remediation,
* expire or are revisited on a defined trigger.

Retries may collect diagnostics but do not convert an intermittent failure into a trusted pass.
