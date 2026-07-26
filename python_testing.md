# Python and pytest Implementation Guidance

> This is a non-normative implementation guide. `Overview.md` defines policy,
> `glossary.md` defines terms, and L1/L2/L3 own assessment and evidence
> procedures. This document contains only Python- and pytest-specific patterns.

The runnable realization is in `example_project/`. It is intentionally more
specific than this guide: its `pyproject.toml` is the canonical marker inventory
for that project, its `justfile` is the command truth, and its JSON files own
project thresholds and support cells.

## 1. Encode independent dimensions

Pytest markers are well suited to orthogonal classification. Give each
automated behavior test exactly one structural marker:

```toml
[tool.pytest.ini_options]
addopts = ["--strict-config", "--strict-markers", "-ra"]
xfail_strict = true
markers = [
  "unit: Small local structural scope.",
  "component: Coherent subsystem structural scope.",
  "integration: Real boundary semantics structural scope.",
  "system: Assembled product structural scope.",
  "regression: Protects established behavior or a learned failure mode.",
  "contract: Producer-consumer or compatibility purpose.",
  "smoke: Small critical-capability selection.",
  "property_based: Generated invariant technique.",
  "fuzz: Generated or mutated adversarial-input technique.",
  "filesystem: Uses real filesystem semantics.",
  "process: Crosses a process boundary.",
  "slow: Excluded from a rapid selection.",
  "quarantined: Excluded from trusted evidence under an owned record.",
  "requirement(id): Links evidence to a declared responsibility.",
]
```

Do not add `contract`, `regression`, `smoke`, or `property_based` to the
structural set. They describe purpose or technique.

Enforce the structural rule during collection and report every violation
together:

```python
import pytest

SCOPES = ("unit", "component", "integration", "system")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    violations = []
    for item in items:
        found = [name for name in SCOPES if item.get_closest_marker(name)]
        if len(found) != 1:
            violations.append(f"{item.nodeid}: expected one scope, found {found}")
            continue
        item.user_properties.append(("structural_scope", found[0]))
    if violations:
        raise pytest.UsageError("\n".join(violations))
```

`item.user_properties` provides a tool-neutral path into JUnit or JSON reports.
Record purposes, techniques, requirement IDs, resource labels, and quarantine
status there when downstream evidence needs them.

## 2. Keep configuration strict and portable

Useful defaults include strict markers, strict configuration, strict xfail, and
a repository-owned warning policy:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = ["--strict-config", "--strict-markers", "-ra"]
xfail_strict = true
filterwarnings = [
  "error",
  "ignore:known upstream warning:DeprecationWarning:upstream_package",
]
```

Each warning exception should name the emitting package, owner, rationale, and
review trigger. Avoid global warning suppression.

Prefer a `src/` layout so tests do not accidentally import a package only
because the repository root is on `sys.path`:

```text
pyproject.toml
src/
  package_name/
tests/
  unit/
  component/
  integration/
  system/
```

A feature-oriented layout is equally valid when it improves ownership. Scope
comes from the exercised boundary, not the directory name; markers remain the
machine-readable contract.

## 3. Make named commands preserve evidence status

Use one wrapper to construct selections and normalize outcomes. A trusted run
should always use the declared full expression, commonly:

```console
pytest -m "not quarantined"
```

Partial workflows must write different report and coverage paths:

```console
pytest -m "not quarantined and not slow"
pytest -m "not quarantined and (unit or component)"
pytest -m "quarantined"
```

Quote marker expressions and use parentheses explicitly; shell parsing and
pytest's boolean precedence otherwise make intent hard to review.

A normalized gate artifact should derive its decision from, rather than merely
copy, all relevant facts:

* process exit status;
* selected test outcomes;
* exact full or partial selection;
* quarantine exclusion and membership;
* required scope and responsibility coverage;
* subject revision, configuration digests, environment, and artifact identity.

Downstream health, compatibility, or release code should validate those
invariants again. Selected evidence must not overwrite complete evidence.
`example_project/scripts/pytest_outcomes.py` demonstrates a version-5 contract;
legacy version-4 artifacts are diagnostic only.

## 4. Write tests around behavior

Use names that state observable behavior:

```python
@pytest.mark.unit
def test_normalize_key_collapses_whitespace() -> None:
    assert normalize_key("  A\tvalue ") == "a value"
```

Parameterization is useful when the cases share one decision and oracle:

```python
@pytest.mark.unit
@pytest.mark.parametrize(
    ("raw", "expected"),
    [("", ""), (" A ", "a"), ("two\twords", "two words")],
)
def test_normalize_key(raw: str, expected: str) -> None:
    assert normalize_key(raw) == expected
```

Split cases when they require different setup, failure diagnosis, or
requirements. Do not hide the behavior behind a large fixture or helper.

Test exceptions with the narrowest meaningful contract:

```python
with pytest.raises(ValueError, match="non-whitespace"):
    registry.add(" ")
```

Avoid asserting every implementation call. Interaction assertions are useful
when the interaction itself is the contract: transaction order, idempotency
keys, audit emission, or a required protocol sequence.

## 5. Fixtures and state

Prefer function-scoped fixtures. Broader scopes save setup cost but increase
state coupling and make failures harder to reproduce:

```python
@pytest.fixture
def registry() -> Registry:
    return Registry()
```

Factories keep variation visible:

```python
@pytest.fixture
def make_user():
    def factory(*, role: str = "reader", active: bool = True) -> User:
        return User(role=role, active=active)
    return factory
```

Use pytest's controlled resources:

* `tmp_path` for real ephemeral filesystem behavior;
* `monkeypatch` for environment, attributes, and process-local configuration;
* `capsys` or `capfd` for stream behavior;
* `caplog` for structured logging assertions;
* `pytester` for testing pytest plugins and collection behavior.

A test using `tmp_path` may still be unit-scoped when the filesystem is inside
the chosen local boundary and platform semantics are not the claim. Mark
resource use separately.

## 6. Doubles and patching

Patch where the subject looks up a name, not where the object was originally
defined:

```python
def test_client_reports_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*args, **kwargs):
        raise TimeoutError

    monkeypatch.setattr("package.client.transport.send", fail)
    assert Client().fetch().status == "unavailable"
```

Prefer small fakes when stateful behavior matters. Use autospecced mocks when an
interface mismatch should fail immediately:

```python
from unittest.mock import create_autospec

transport = create_autospec(Transport, instance=True)
```

Pair doubles with real-boundary evidence whenever framework, SQL, protocol,
serialization, packaging, or operating-system behavior supports the claim.

## 7. Processes, CLIs, and built artifacts

Use `subprocess.run` with explicit input, captured output, timeout, environment,
and return-code assertions:

```python
result = subprocess.run(
    [sys.executable, "-m", "package.cli", "inspect", str(path)],
    capture_output=True,
    check=False,
    text=True,
    timeout=10,
)
assert result.returncode == 0
assert json.loads(result.stdout)["status"] == "ok"
```

For packaging claims:

1. build the sdist and wheel once;
2. retain their names and digests;
3. install the wheel into an isolated environment;
4. run imports, entry points, metadata, and critical workflows outside the
   source tree with `PYTHONPATH` removed;
5. publish exactly the tested artifact.

Do not rebuild between artifact verification and publication.

## 8. Time, randomness, and concurrency

Inject clocks rather than waiting:

```python
class FixedClock:
    def now(self) -> datetime:
        return datetime(2030, 1, 1, tzinfo=UTC)
```

Pass a local `random.Random(seed)` or framework-managed generator instead of
changing process-global randomness. Retain failing seeds and minimized
counterexamples.

For threads and async tasks, synchronize on events, queues, barriers, or
observable state. A timeout should bound a test, not serve as its primary
coordination mechanism. Use framework-specific helpers such as AnyIO's pytest
plugin where they preserve the relevant scheduler semantics.

## 9. Generative techniques

Hypothesis can encode invariants and shrink failures:

```python
from hypothesis import given, strategies as st


@pytest.mark.unit
@pytest.mark.property_based
@given(st.text())
def test_normalization_is_idempotent(value: str) -> None:
    once = normalize_key(value)
    assert normalize_key(once) == once
```

State machines work well for stores, caches, protocols, and workflows. A
reference model should be simpler and independent from the subject.

Fuzz runners such as Atheris or external native fuzzers need a stable entry
point, seed corpus, resource bounds, crash artifact retention, minimization, and
reproduction instructions. Route design and evaluation through
`L3_T6_generative_and_fuzz.md`.

## 10. Contracts, snapshots, and schemas

Schema validation establishes structure, not full compatibility:

```python
jsonschema.validate(instance=payload, schema=EVENT_SCHEMA)
```

Provider verification should run against the provider revision or artifact that
will actually be released. Record consumer/provider versions and interaction
identity.

For snapshots:

* canonicalize irrelevant timestamps, paths, ordering, or generated IDs;
* keep semantic fields under ordinary assertions when they deserve focused
  diagnostics;
* review diffs as behavior changes, not formatting chores;
* retain provenance for generated golden files.

Use `L3_T7_contract.md` and `L3_T9_snapshot.md` for the procedure; the choice of
pytest plugin does not change the evidence contract.

## 11. Integration resources

Prefer fixtures that explicitly provision, verify readiness, reset, and clean
up real resources. Container startup alone is not readiness. Test the adverse
semantics that motivate integration scope: transaction rollback, encoding,
timeout, protocol error, migration, restart, or permission behavior.

Record image or service versions and configuration. Parallel tests need unique
namespaces or isolated instances. If teardown fails, report that as a harness
failure rather than silently accepting leaked state.

## 12. Performance and quantitative gates

Python tools such as `pytest-benchmark`, `pyperf`, `coverage.py`, mutation
runners, and profiling libraries collect observations; they do not supply a
portable decision threshold.

Keep the complete L3-T11 metric specification in a versioned project artifact.
For performance, include workload, environment, warmup, sample method,
statistic, natural variation, and both practically meaningful absolute and
relative effects. For coverage and mutation, preserve code cohort, test
selection, exclusions, operators, and denominator treatment.

Never combine partial coverage data with a complete-run artifact unless the
aggregation contract explicitly proves equivalence.

## 13. Static, security, and supply-chain tools

Common Python choices include:

| Concern | Example tools |
| --- | --- |
| format and lint | Ruff, Black |
| types | mypy, pyright, ty |
| security rules | Bandit, Semgrep |
| dependencies | pip-audit, osv-scanner |
| secrets | TruffleHog, Gitleaks |
| builds | `python -m build`, `uv build`, Twine checks |
| provenance | hashes, signatures, attestations, SBOM tools |

Pin or otherwise identify decision-critical tool versions and configuration.
Treat tool errors, unsupported inputs, stale advisory data, and incomplete scans
as invalid evidence rather than clean results.

## 14. Acceptance, accessibility, and operations

Pytest can encode automated portions of acceptance, accessibility, and
operational claims, but the corresponding L3 procedure controls the overall
evidence:

* `L3_T12_acceptance.md` for stakeholder conditions;
* `L3_T14_usability_accessibility.md` for automated checks plus human and
  assistive-technology evidence;
* `L3_T15_operational_resilience.md` for deployment, monitoring, backup,
  restore, rollback, degradation, and recovery.

A command that completes is not proof that restored data is usable, a rollback
preserves compatibility, or operators can diagnose the failure.

## 15. Quarantine, reruns, and harness tests

An owned quarantine record should contain node ID, rationale, affected claim,
owner, expiry, and remediation link. The trusted marker expression excludes
quarantined tests; a separate command runs them diagnostically.

Rerun plugins may collect observations but must not turn fail-then-pass into a
clean complete run. Store raw attempts if flake analysis depends on them.

Test the harness itself with synthetic pass, failure, skip, xfail, quarantine,
partial-selection, stale-evidence, and non-comparable-evidence cases. In
particular, verify that:

* a nonzero pytest exit cannot serialize a passing decision;
* every behavior test has exactly one structural scope;
* contract remains a purpose;
* partial evidence cannot satisfy a full gate;
* compatibility cells match the current revision and configuration digests.

The runnable examples are in
`example_project/tests/component/test_evidence_integrity.py`.

## 16. Project workflow

The reference project's executable workflow is documented in
`example_project/local-testing.md`. Use `just --list` for commands and
`example_project/pyproject.toml` for the project marker inventory. Do not copy
its numeric budget or compatibility matrix without a project-specific L1 and
L3-T11 decision.
