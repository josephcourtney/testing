<!--
TESTING-GUIDANCE-REVIEW: document-level annotation

Problems identified:
- This document combines policy, terminology, Python/pytest configuration, examples, directory conventions, lifecycle cadence, and quantitative targets in one authority level.
- The taxonomy treats contract as comparable to structural scopes even though contract usually describes purpose; other purposes and techniques are also mixed with scope markers.
- Several recommendations are framed universally despite depending on project risk, architecture, environment, and feedback constraints.
- Fixed coverage, mutation, runtime, flake, and performance targets are not accompanied by explicit populations, denominators, baselines, uncertainty, or decision rules.
- Acceptance, exploratory, usability/accessibility, and operational/recovery evidence are underrepresented.

Proposed fixes:
- Retain the detailed material, but annotate sections by authority: normative policy, definition, recommended default, example, or project-specific convention.
- Describe tests with orthogonal dimensions: structural scope, purpose, technique, resources/boundaries, and execution cadence.
- Make risk and failure modes determine evidence applicability; use lifecycle only to adjust confidence, breadth, fidelity, and enforcement.
- Replace universal numeric gates with a metric-specification procedure while retaining example values as explicitly illustrative.
- Add dedicated guidance for acceptance, exploratory, usability/accessibility, and operational/resilience evidence.

Review rule: preserve the original document text. Apply any proposed fix only after explicit review.
-->

# Testing Policy for Python Projects

## 1. Goals and principles

1. Tests must provide:

   * High confidence in correctness.
   * Fast feedback for most changes.
   * Clear localization of failures.
2. Test suites must be:

   * Structured by scope and intent.
   * Predictable to run (no hidden side effects).
   * Strictly configured (misconfigurations should fail, not be silently ignored).

Language conventions:
Use “must” for requirements, “should” for strong recommendations.

---

## 2. Test taxonomy

### 2.1 Scopes

Each test must declare its scope via markers:

* `unit`:

  * No real network, database, or filesystem access.
  * External dependencies are replaced with stubs/mocks/fakes.
  * Must be fast: per-test runtime should be small enough that the entire unit suite can run in a few seconds; as a rough target, keep most unit tests under ~100 ms.
* `component`:

  * Tests a coherent subsystem via its public API.
  * May use in-process fakes or lightweight real dependencies (e.g. SQLite).
* `integration`:

  * Uses real external dependencies (DB, HTTP services, message bus).
  * Tests that integration boundaries behave correctly.
* `system`:

  * End-to-end flows, treating the application as a black box.
  * Intended for smoke/acceptance-style coverage.
* `contract`:

  * Tests API or schema contracts that other systems rely on (DB schemas, event payloads, HTTP API responses).

### 2.2 Cross-cutting markers

Use additional markers to express other dimensions:

* `db`: touches a real database engine.
* `slow`: expected to be noticeably slower than typical unit tests.
* `smoke`: small set of fast, critical-path tests.
* `regression`: guards against previously reported bugs.
* `property_based`: uses property-based testing tools (e.g. Hypothesis).
* `observability`: asserts on logs, metrics, or traces.
* `security`, `performance`, `data_quality`, etc., as needed.

Example `pytest` marker configuration (in `pyproject.toml` or `pytest.ini`):

```toml
[tool.pytest.ini_options]
  minversion = "8.0"
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--cov=your_package_name",
    "--cov-branch",
    "--cov-report=xml",
  ]
  xfail_strict = true

  markers = [
    "unit: Fast, isolated tests of individual functions/classes. No real I/O.",
    "component: Tests of a subsystem via public APIs; may use local fakes or lightweight real deps.",
    "integration: Tests involving real external dependencies (DB, HTTP APIs, queues).",
    "system: End-to-end tests treating the app as a black box.",
    "contract: Tests of API or schema contracts.",
    "db: Tests that exercise database behaviour or schema.",
    "smoke: Fast, critical-path tests for quick feedback.",
    "slow: Known slow tests.",
    "regression: Guards against previously reported bugs.",
    "property_based: Property-based tests (e.g. Hypothesis).",
    "observability: Tests asserting on logs, metrics, or traces.",
    "security: Security-focused tests.",
    "performance: Performance or performance-regression tests.",
    "data_quality: Tests of data integrity or freshness.",
  ]
```

Policy:

* Every test must have at least one scope marker (`unit`, `component`, `integration`, `system`, or `contract`).
* Cross-cutting markers are optional but recommended when applicable.

---

## 3. Directory layout

All tests must live under a top-level `tests/` directory.

Recommended structure:

```text
tests/
  unit/
    package_a/
    package_b/
    test_misc.py
  component/
  integration/
  system/
  property/
  data/         # static test fixtures (JSON, YAML, HTML, etc.)
```

Guidelines:

* Unit tests should roughly mirror the source tree but do not need a 1:1 mapping.
* Property-based tests that are conceptually about correctness invariants may live under `tests/property/`.
* Large or reusable fixtures should go in `tests/data/` or be generated by fixtures, not hard-coded in many tests.

---

## 4. Pytest configuration policy

### 4.1 Core settings

Use pytest as the default test runner with the following baseline configuration:

```toml
[tool.pytest.ini_options]
  minversion = "8.0"
  testpaths = ["tests"]
  python_files = ["test_*.py"]

  addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--cov=your_package_name",
    "--cov-branch",
    "--cov-report=xml",
  ]

  xfail_strict = true

  log_cli       = true
  log_cli_level = "INFO"
  log_cli_format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
  log_cli_date_format = "%Y-%m-%d %H:%M:%S"

  filterwarnings = [
    "error::DeprecationWarning:your_package_name\\.",
    "ignore::DeprecationWarning:some_known_third_party",
  ]
```

Policies:

* Unknown markers must fail the test run (`--strict-markers`).
* Unknown config keys must fail the test run (`--strict-config`).
* Deprecation warnings from the main package should be treated as errors.
* `xfail` must be strict: if an xfailed test unexpectedly passes, the run should fail.

### 4.2 Coverage

* Branch coverage must be enabled (`--cov-branch`).
* XML coverage reports must be generated for CI systems.
* Projects may set `fail_under` in `[tool.coverage.report]` once a stable baseline is established.

Example (in `pyproject.toml`):

```toml
[tool.coverage.run]
  source   = ["your_package_name"]
  branch   = true
  parallel = true

[tool.coverage.report]
  show_missing = false
  skip_covered = true
  # Optionally:
  # fail_under = 80
```

---

## 5. Command-line entrypoints

Projects should provide ergonomic commands (via `Makefile`, `justfile`, or scripts) to standardize usage.

Recommended targets:

* `test-fast`: run all tests except those marked `slow`.
* `test-all`: run the full test suite.
* `test`: default to “CI-equivalent” suite (often same as `test-all`).
* `check`: run linting, type checking, security checks, and tests, as a pre-commit/CI pipeline.

Example using `make`:

```make
test-fast:
	pytest -m "not slow"

test-all:
	pytest

test:
	pytest

check:
	flake8 your_package_name tests
	mypy your_package_name tests
	pytest
```

Policy:

* Developers must be able to run a fast subset locally (`test-fast`) and a full suite (`test-all`) without remembering complex filter expressions.

### 5.1 Recommended testing cadence

Recommended mapping from workflow events to commands/markers:

| Trigger      | Command / selection                                            | Expected duration |
| ------------ | -------------------------------------------------------------- | ----------------- |
| Every save   | `pytest tests/unit -q`                                         | < 5 s             |
| Every commit | `pytest -m "unit and not slow" -q`                             | ≤ 2 min           |
| Pull request | `pytest -m "unit or component or contract and not slow"`       | ≤ 10–15 min       |
| Nightly      | `pytest` (full suite, incl. `integration`, `system`, `slow`)   | up to ~60 min     |
| Pre-release  | Nightly suite + `-m "performance or security or data_quality"` | project-specific  |

Projects may adjust details and budgets, but the pattern (fast per-save / per-commit checks, broader PR checks, and full nightly/pre-release runs) should be preserved.

---

## 6. Test design guidelines

### 6.1 Design around behaviour and invariants

For each module or component:

* Identify responsibilities in plain language.
* Identify invariants (“this can never happen”) and state transitions.
* Write tests that reflect these, not just line coverage.

Example invariant tests:

```python
import pytest

from your_package_name.normalize import normalize_whitespace

@pytest.mark.unit
def test_normalize_whitespace_idempotent():
    original = "  Foo   bar \n baz  "
    once = normalize_whitespace(original)
    twice = normalize_whitespace(once)
    assert once == twice

@pytest.mark.unit
def test_normalize_whitespace_strips_edges():
    assert normalize_whitespace("  a  ") == "a"
```

### 6.2 Naming and structure

* Test function names must describe behaviour, not implementation details:

  * `test_parse_header_handles_missing_fields` instead of `test_parser_case3`.
* Each test should assert one conceptual behaviour; multiple small tests are preferred over one large one.
* Arrange test body roughly as:

  * Arrange (set up),
  * Act (call),
  * Assert (checks).

---

## 7. Unit tests

Definition:

* No real network calls.
* No real databases.
* No reads or writes of persistent files or directories.
* No reliance on actual files unless they are tiny, ephemeral temporary files.
* No sleeps or non-deterministic timing.

Guidelines:

* Aim for unit tests to be very fast; most should complete in under ~100 ms, and the entire unit suite should be runnable on every save or commit.
* Use dependency injection and small interfaces to avoid mocking deep internals.
* When mocking, mock at integration boundaries (`requests` layer, repository interface), not internals.
* Use simple, explicit fakes when possible.
* Avoid asserting on private attributes or unstable implementation details; prefer observable behaviour.

Example:

```python
import pytest

from your_package_name.core import calculate_price

@pytest.mark.unit
def test_calculate_price_applies_discount():
    price = calculate_price(base=100, discount_percent=10)
    assert price == 90
```

---

## 8. Component tests

Definition:

* Test a bounded subsystem with real code paths.
* May use:

  * In-process fakes for external systems, or
  * Lightweight real services (e.g. SQLite, in-memory cache).

Guidelines:

* Use temporary resources (temp directories, SQLite in a temp file, etc.).
* Test through public APIs; avoid reaching into internal implementation details.
* Only mock or fake at the boundaries of the component under test.

Example:

```python
import pytest
from sqlalchemy import create_engine

from your_package_name.store import SqlAlchemyStore

@pytest.mark.component
@pytest.mark.db
def test_store_persists_and_loads_entities(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    store = SqlAlchemyStore(engine=engine)

    store.save_user({"id": 1, "name": "Alice"})
    user = store.get_user(1)

    assert user["name"] == "Alice"
```

---

## 9. Integration tests

Definition:

* Exercises integration with real external systems: a real DB server, HTTP API, message broker, etc.

Guidelines:

* Mark tests as `integration` and any relevant cross-cutting markers (`db`, `slow`, `security`, `performance`).
* Use dedicated test resources (test databases, stub services) to avoid affecting production data/settings.
* Ensure tests are repeatable and can be run in CI.
* Prefer containerized or isolated test instances of infrastructure where possible.

Example:

```python
import pytest

@pytest.mark.integration
@pytest.mark.db
@pytest.mark.slow
def test_api_can_write_to_real_database(api_client, real_db):
    response = api_client.post("/users", json={"name": "Bob"})
    assert response.status_code == 201

    user = real_db.query_user_by_name("Bob")
    assert user is not None
```

---

## 10. System tests

Definition:

* End-to-end tests that approximate real usage habits (e.g. HTTP requests, CLI invocations).

Guidelines:

* Mark as `system` and usually `slow`.
* Prefer a small set of critical scenarios:

  * Startup and shutdown behaviour.
  * Happy-path workflows.
  * Critical error handling paths.
  * Cross-service flows in a distributed system.

Example:

```python
import pytest
import subprocess

@pytest.mark.system
@pytest.mark.slow
def test_cli_end_to_end(tmp_path):
    out = subprocess.check_output(["your-cli", "--output", str(tmp_path)])
    assert b"Completed successfully" in out
    # Additional assertions on generated output
```

---

## 11. Contract tests

Definition:

* Validates contracts that other systems rely on (e.g. API schemas, DB schemas, event formats).

Guidelines:

* Mark as `contract`.
* For databases:

  * Assert column presence, nullability, types, and relationships.
* For APIs:

  * Assert that responses match a schema (e.g. via JSON Schema or Pydantic models).
* For events/messages:

  * Assert payload structure, required fields, and versioning rules.

Example:

```python
import pytest

@pytest.mark.contract
@pytest.mark.db
def test_user_table_schema(db_inspector):
    cols = {c["name"]: c for c in db_inspector.get_columns("users")}
    assert cols["id"]["nullable"] is False
    assert cols["email"]["nullable"] is False
    assert cols["email"]["type"].__class__.__name__.lower().startswith("varchar")
```

---

## 12. Configuration and environment testing

Policy:

* Behaviour that depends on configuration or environment variables must have tests.

Examples:

* Different runtime profiles (dev vs prod).
* Feature flags.
* Cache toggles.

Example:

```python
import importlib
import pytest

@pytest.mark.unit
def test_cache_default_enabled_in_dev(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    module = importlib.import_module("your_package_name.settings")
    importlib.reload(module)
    assert module.CACHE_ENABLED is True

@pytest.mark.unit
def test_cache_default_disabled_in_prod(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    module = importlib.import_module("your_package_name.settings")
    importlib.reload(module)
    assert module.CACHE_ENABLED is False
```

---

## 13. Property-based testing

Policy:

* Property-based tests should be used for:

  * Normalization functions.
  * Parsers and formatters.
  * Comparators and similarity functions.
  * Simple but critical transformations.

Guidelines:

* Place such tests under `tests/property/` and mark them `property_based` (plus a scope marker).
* Properties should be simple and easy to understand (idempotence, round-trip, bounds, symmetry).
* Prefer pure, side-effect-free functions as subjects of property-based tests.

Example:

```python
import hypothesis.strategies as st
from hypothesis import given
import pytest

from your_package_name.normalize import normalize_id

@given(st.text())
@pytest.mark.unit
@pytest.mark.property_based
def test_normalize_id_is_idempotent(s: str):
    once = normalize_id(s)
    twice = normalize_id(once)
    assert once == twice
```

---

## 14. Observability tests

Policy:

* For critical flows, log messages and metrics are part of the public contract and may be tested.

Guidelines:

* Use the `caplog` fixture for log assertions.
* Mark tests with `observability`.
* Focus on:

  * Presence and shape of key log messages.
  * Correct logging of error conditions.
  * Inclusion of identifiers (e.g. request IDs, entity IDs) needed for debugging.

Example:

```python
import logging
import pytest

from your_package_name.worker import process_job

logger = logging.getLogger("your_package_name.worker")

@pytest.mark.unit
@pytest.mark.observability
def test_process_job_logs_success(caplog):
    with caplog.at_level("INFO", logger=logger.name):
        process_job({"id": 1})

    assert "processed job id=1" in caplog.text
```

---

## 15. Fixtures and test data

Guidelines:

* Prefer inline data for small examples (strings, small dicts).
* Use files in `tests/data/` for larger payloads (HTML, JSON, etc.).
* Build reusable factories/helpers for complex domain objects instead of duplicating literals.
* Keep fixtures focused and composable; avoid “god fixtures” that do too much.

Example fixture factory:

```python
import pytest

from your_package_name.models import User

@pytest.fixture
def user_factory():
    def _make_user(id=1, name="Alice", email="alice@example.com"):
        return User(id=id, name=name, email=email)
    return _make_user
```

---

## 16. Advanced testing techniques

### 16.1 Mutation testing (optional)

Projects with high criticality may adopt mutation testing tools to assess test suite strength.

Guidelines:

* Run mutation tests only in dedicated workflows (they are slow).
* Use them to identify weakly tested code paths, not as a hard gate for all changes.
* Focus mutation testing on:

  * Core business logic.
  * Pure or mostly pure functions.
  * Security-sensitive code paths.

### 16.2 Coverage, mutation, and property test quality

- **Coverage evaluation** – rely on the pytest-generated XML/HTML reports (`--cov`, `--cov-branch`, `--cov-report=xml`) and aim for the targets described in `Automated Testing.md:143-167` (line ≥80% backend, branch ≥70%, case/path coverage as applicable). Use `showcov` or similar tools to highlight missing lines and modules; if a critical module is below target, add focused unit/component tests or refactor to reduce dead branches so the coverage metrics better reflect exercised behaviour.
- **Mutation evaluation** – treat Mutmut results as a mutation score, targeting >85% for safety-critical or >70% for general code per `Automated Testing.md:145-157`. Run `just mutation`/`mutmut results` to surface survivors, translate each survivor into a concrete assertion or property (possibly adding new tests or tightening invariants), and confirm that rerunning the mutation suite kills the previous survivors.
- **Property-testing evaluation** – property suites should codify deterministics invariants (e.g., idempotent normalizers, filter sorting, capability state transitions, queue-overflow responses). Measure their effectiveness by whether Hypothesis finds counterexamples when an invariant is violated and whether coverage/mutation metrics improve after adding the property. Extend property tests by enumerating invariants from design notes (e.g., `DESIGN.md:369-380`) or from mutation survivors and adding new test functions under `tests/property/` marked with `property_based`.

When any metric falls short, schedule follow-up work: add targeted tests for the failing module (coverage), write assertions that detect the mutated behaviour (mutation), or describe the missing invariant (property testing). Repeat the measurement cycle so automated runs report regained targets before the next release.

### 16.3 Fuzz testing

Use fuzzing where inputs are complex, adversarial, or security-relevant (parsers, protocol handlers, API boundaries).

Guidelines:

* Start with property-based generators (e.g. Hypothesis) before introducing external fuzzers.
* Focus on:

  * Crashing behaviours.
  * Assertion failures.
  * Unexpected exceptions or timeouts.

### 16.4 Chaos and resilience testing

For distributed systems and services, resilience under partial failure is critical.

Guidelines:

* Design a small set of chaos scenarios (e.g. DB latency, dependency returning errors, intermittent network failures).
* Automate these in integration/system tests where feasible.
* Ensure observability (logs/metrics/traces) clearly indicate degraded modes and recovery.

### 16.5 Snapshot tests (optional)

Snapshot tests capture a serialized representation (e.g. JSON, HTML) and compare against a baseline.

Guidelines:

* Use sparingly, when outputs are large but structurally stable.
* Keep snapshots readable and reviewed like code.
* Avoid using snapshots as a substitute for precise behavioural assertions when those are feasible.

---

## 17. Static analysis and security checks

Some checks must run regularly regardless of project specifics.

Policy:

* On every commit and every PR, run:

  * Formatter (e.g. `ruff format`, `black`).
  * Linter (e.g. `ruff check`).
  * Type checker (e.g. `mypy`, `pyright`, `ty`).
  * Dependency scanner (e.g. `pip-audit`, `safety`, or platform SCA).
  * Secret scanner (e.g. `gitleaks`, `trufflehog`, or platform equivalent) at the repository level.

Guidelines:

* CI must fail on:

  * Lint or type errors.
  * Blocker security findings (critical/high CVEs, leaked secrets), unless explicitly triaged with a documented waiver.

These checks should be wired into the `check` command and CI pipelines.

---

## 18. Metrics and targets

Quantitative metrics help keep the test suite effective and healthy. Targets are guidelines, not rigid laws, but deviations should be explicit and justified.

Recommended targets:

* Coverage:

  * Line coverage: target ≥ 80% for backend Python code.
  * Branch coverage: target ≥ 70%.
  * For critical modules, higher targets are encouraged.
* Mutation score (where used):

  * Target ≥ 70% for core business logic.
* Flake rate:

  * Flaky tests should be rare; if the same test flakes multiple times in a short window, it must be investigated, fixed, or quarantined.
* Performance regression:

  * For performance tests, new versions should remain within an agreed band (e.g. ±5–10%) of baseline latency/throughput for key endpoints, unless an intentional change has been documented.

Projects may adopt stricter or looser thresholds, but they should be explicit.

---

## 19. Prohibited practices and anti-patterns

To maintain isolation, efficiency, clarity, purpose, and maintainability, the following are explicitly disallowed:

* Unit tests must not:

  * Hit real network endpoints.
  * Use real databases or queues.
  * Read from or write to persistent files or directories.
  * Depend on real-time sleeps or non-deterministic timing.

* Test suites must not:

  * Rely on arbitrary `time.sleep` calls to “stabilize” behaviour; use proper synchronization (e.g. polling, hooks, events) instead.
  * Treat large, slow end-to-end suites as the primary safety net; lower levels must carry most of the load.

* Tests must not:

  * Chase 100% line coverage with trivial assertions that add no defect-detection value.
  * Assert on unstable implementation details (private attributes, log strings that are not part of the contract) without a clear reason.
  * Silently ignore failing tests or leave known flaky tests untriaged for long periods.

* Security/tooling:

  * Secret-scanner and vulnerability-scan warnings must not be casually suppressed; waivers must be documented and reviewed.
  * Disabling static analysis or test suites “temporarily” without an issue/ticket and clear follow-up is not acceptable.

If these constraints are too tight for a specific case, the exception and rationale must be documented in code comments and, where relevant, in project docs.

```
```
### 16.5 Snapshot tests (optional)

Snapshot tests capture a serialized representation (e.g. JSON, HTML) and compare against a baseline.

Guidelines:

* Use sparingly, when outputs are large but structurally stable.
* Keep snapshots readable and reviewed like code.
* Avoid using snapshots as a substitute for precise behavioural assertions when those are feasible.

