# Python and pytest Testing Guide

This document is non-normative implementation guidance for Python projects. It shows one coherent way to apply `Overview.md`, the L1/L2/L3 procedures, and `glossary.md` using pytest and common Python tooling.

Projects should adapt the examples to their risks, architecture, supported Python versions, packaging model, and operating environment. The examples are defaults to evaluate, not universal requirements.

## 1. Classification in pytest

Use markers to encode independent dimensions rather than one overloaded hierarchy.

A practical scheme is:

* one primary structural scope marker: `unit`, `component`, `integration`, or `system`,
* zero or more purpose markers: `acceptance`, `regression`, `contract`, `smoke`, `compatibility`, `security`, `performance`, `data_quality`, `observability`, `accessibility`, `resilience`, `recovery`,
* zero or more technique markers: `property_based`, `stateful`, `differential`, `metamorphic`, `fuzz`, `snapshot`, `fault_injection`,
* zero or more resource/execution markers: `filesystem`, `process`, `db`, `network`, `hardware`, `slow`, `destructive`, `quarantined`.

Example:

```python
import pytest


@pytest.mark.component
@pytest.mark.contract
def test_exported_document_matches_supported_schema(document):
    validate_document(document)
```

Here `component` states the execution boundary; `contract` states why the test exists.

A system-level compatibility test can use the same purpose:

```python
@pytest.mark.system
@pytest.mark.contract
@pytest.mark.compatibility
def test_installed_cli_emits_supported_document(installed_cli):
    result = installed_cli("inspect", "example-package")
    validate_document(result.json)
```

### Suggested marker declarations

```toml
[tool.pytest.ini_options]
markers = [
  "unit: Small local execution boundary with highly localizing failures.",
  "component: Coherent subsystem through a supported interface.",
  "integration: Real semantics across an external or infrastructure boundary.",
  "system: Assembled product through a user- or operator-visible boundary.",

  "acceptance: Stakeholder or product acceptance condition.",
  "regression: Protects learned behavior or a previous failure mode.",
  "contract: Producer-consumer or compatibility obligation.",
  "smoke: Small critical-capability selection.",
  "compatibility: Supported-version, platform, artifact, or consumer behavior.",
  "security: Threat-relevant behavior or control.",
  "performance: Latency, throughput, scalability, or resource measurement.",
  "data_quality: Data integrity, freshness, or distribution claim.",
  "observability: Logs, metrics, traces, health, or diagnostic behavior.",
  "accessibility: Accessibility or assistive-technology obligation.",
  "resilience: Degraded-operation or fault-handling claim.",
  "recovery: Rollback, restart, restoration, or failover claim.",

  "property_based: Generated invariant testing.",
  "stateful: Generated state-machine or model-based testing.",
  "differential: Comparison between implementations, versions, or modes.",
  "metamorphic: Relations across transformed inputs or outputs.",
  "fuzz: Random, adversarial, or coverage-guided input exploration.",
  "snapshot: Canonical stored-output comparison.",
  "fault_injection: Deliberately introduced dependency or runtime failure.",

  "filesystem: Uses real filesystem semantics.",
  "process: Crosses a process boundary.",
  "db: Uses a database engine.",
  "network: Uses a network boundary.",
  "hardware: Depends on specific hardware behavior.",
  "slow: Excluded from the fastest developer loop.",
  "destructive: Mutates or destroys an isolated resource.",
  "quarantined: Not trusted as gating evidence; remediation must be tracked.",
]
```

Projects may enforce one primary structural marker during collection. Purpose, technique, and resource markers should remain independently composable.

## 2. Baseline pytest configuration

A strict baseline catches misspelled markers, invalid configuration, and unexpectedly passing `xfail` cases.

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
  "--strict-markers",
  "--strict-config",
  "-ra",
]
xfail_strict = true
```

Add coverage to workflows that are intended to produce complete coverage evidence rather than to every partial developer run:

```toml
[tool.coverage.run]
source = ["your_package_name"]
branch = true
parallel = true

[tool.coverage.report]
show_missing = true
skip_covered = false
```

A project can use `pytest-cov` in its complete evidence command:

```bash
pytest --cov=your_package_name --cov-branch --cov-report=term-missing --cov-report=xml
```

Do not let a selected test run overwrite the canonical coverage artifact used by a release or quality gate.

### Warnings

Warnings from the project under test are often useful as errors, while known third-party warnings may require narrow temporary filters:

```toml
[tool.pytest.ini_options]
filterwarnings = [
  "error::DeprecationWarning:your_package_name\\.",
  "ignore:documented third-party warning:DeprecationWarning:third_party_package\\.",
]
```

Filters should be specific, justified, and removed when the underlying issue is resolved.

## 3. Directory organization

Directory layout is a navigation convention, not the full meaning of a test. Two common layouts are valid.

### Scope-oriented layout

```text
tests/
  unit/
  component/
  integration/
  system/
  property/
  data/
```

### Feature-oriented layout

```text
tests/
  accounts/
    test_domain.py
    test_api_contract.py
    test_checkout_flow.py
  reporting/
  support/
  data/
```

Markers remain the source of classification when directories mix purposes or techniques. A project may also colocate tests with implementation where its tooling and team practices support that arrangement.

## 4. Named commands and evidence integrity

Provide stable commands so developers and CI do not need to remember complex selections.

Typical commands include:

* `test-dev` — narrow, fast editing loop; may use test-impact selection and omit coverage,
* `test-fast` — broad deterministic selection excluding declared expensive tests,
* `test-all` — complete declared test selection,
* `check` — formatting, linting, type checking, security checks, and required tests,
* `test-installed` — build and test the actual wheel or distribution outside the checkout,
* `test-integration` — provision and exercise real external dependencies,
* `test-system` — assembled-product workflows,
* `test-performance` — controlled performance measurements,
* `test-mutation` — declared mutation cohort,
* `release-check` — validate all required fresh and comparable evidence.

Example `justfile` fragments:

```just
test-dev *args:
    uv run pytest --no-cov {{args}}

test-fast:
    uv run pytest -m "not slow and not destructive and not quarantined"

test-all:
    uv run pytest

check:
    uv run ruff format --check .
    uv run ruff check .
    uv run basedpyright
    uv run pytest
```

The exact names and selections are project conventions. The important properties are that complete and partial runs are distinguishable and that stale or incompatible artifacts cannot silently satisfy a gate.

### Marker-expression parentheses

Use explicit parentheses around Boolean marker groups:

```bash
pytest -m "(unit or component or contract) and not slow"
```

Do not rely on readers remembering operator precedence in expressions such as:

```bash
pytest -m "unit or component or contract and not slow"
```

## 5. Test design and naming

Tests should describe observable behavior, conditions, and outcomes.

Prefer:

```python
def test_parse_header_rejects_missing_identifier(): ...
```

over:

```python
def test_parser_case_3(): ...
```

Arrange–Act–Assert is a useful default when it improves readability:

```python
@pytest.mark.unit
def test_calculate_price_applies_discount():
    base_price = 100

    result = calculate_price(base=base_price, discount_percent=10)

    assert result == 90
```

Given–When–Then, table-driven tests, helper assertions, or domain-specific test languages may be clearer for other cases.

A test may contain several assertions when they express one conceptual behavior. Splitting every assertion into a separate test is not inherently better.

## 6. Unit tests

Choose a small boundary that provides useful localization. A unit need not be a single function or class.

Good unit-test subjects include:

* calculations and transformations,
* parsers and formatters,
* local state transitions,
* validation and decision logic,
* invariants and error rules.

Unit tests should avoid uncontrolled network, database, process, clock, randomness, or persistent-state dependencies. Small real collaborators and ephemeral files are acceptable when they are part of the chosen local boundary and improve clarity.

### Pure example

```python
@pytest.mark.unit
def test_normalize_whitespace_is_idempotent():
    original = "  Foo   bar \n baz  "

    once = normalize_whitespace(original)
    twice = normalize_whitespace(once)

    assert once == twice
```

### Sociable unit example

```python
@pytest.mark.unit
def test_invoice_total_uses_domain_tax_policy():
    invoice = Invoice(lines=[LineItem(price=100)])
    tax_policy = StandardTaxPolicy(rate=Decimal("0.06"))

    assert invoice.total(tax_policy) == Decimal("106.00")
```

Both collaborators remain real because they are inexpensive, deterministic, and within the chosen unit boundary.

### Solitary unit example

```python
@pytest.mark.unit
def test_notification_service_reports_rejected_delivery():
    gateway = StubGateway(result=DeliveryResult.rejected("blocked"))
    service = NotificationService(gateway=gateway)

    result = service.send(message)

    assert result == SendResult.failed("blocked")
```

The gateway is replaced because external delivery is outside the boundary and controlled failure is the purpose.

## 7. Component tests

Component tests exercise a coherent subsystem through supported interfaces. Internal collaborators generally remain real.

```python
@pytest.mark.component
@pytest.mark.filesystem
def test_store_persists_and_loads_entities(tmp_path):
    store = SqliteStore(tmp_path / "store.sqlite")

    store.save_user(User(id=1, name="Alice"))

    assert store.get_user(1) == User(id=1, name="Alice")
```

Using a temporary SQLite database is appropriate when the component contract includes persistence behavior but the risk does not depend on the production database engine. If SQL dialect, transaction isolation, extensions, migrations, or production indexing matter, add integration evidence using the actual engine.

## 8. Integration tests

Use integration scope when the claim depends on real semantics across an external boundary.

```python
@pytest.mark.integration
@pytest.mark.db
@pytest.mark.slow
def test_repository_transaction_rolls_back_on_conflict(postgres_repository):
    with pytest.raises(VersionConflict):
        postgres_repository.apply_conflicting_updates()

    assert postgres_repository.current_state() == EXPECTED_ORIGINAL_STATE
```

Integration resources should be:

* isolated from production,
* provisioned or reset predictably,
* identified in the evidence,
* bounded by timeouts,
* cleaned up even after failure,
* representative of the semantics being claimed.

Containers are useful when they supply the real implementation cheaply, but containerization alone does not make a test integration-scoped. The evidential question is whether real boundary semantics matter.

## 9. System and installed-artifact tests

System tests exercise the assembled product through a supported user or operator boundary.

```python
@pytest.mark.system
@pytest.mark.process
@pytest.mark.smoke
def test_cli_can_generate_report(tmp_path):
    completed = subprocess.run(
        ["your-cli", "report", "--output", str(tmp_path / "report.json")],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert completed.returncode == 0, completed.stderr
    assert (tmp_path / "report.json").exists()
```

For packaged tools, test the exact wheel or distribution intended for release:

1. build the artifact,
2. inspect expected files and metadata,
3. install it into a clean environment outside the source checkout,
4. clear source-tree import paths,
5. invoke public interfaces as an independent consumer,
6. retain artifact identity and environment details with the result.

Source-tree tests cannot establish that packaging metadata, entry points, included data, or isolated installation are correct.

## 10. Configuration and environment testing

Behavior controlled by configuration, environment variables, feature flags, locale, timezone, or runtime profiles needs evidence at a scope appropriate to the risk.

Prefer configuration objects that can be constructed explicitly:

```python
@pytest.mark.unit
@pytest.mark.parametrize(
    ("environment", "expected_cache"),
    [("development", True), ("production", False)],
)
def test_cache_default_depends_on_environment(environment, expected_cache):
    settings = Settings.from_mapping({"APP_ENV": environment})

    assert settings.cache_enabled is expected_cache
```

When import-time environment behavior is itself the contract, isolate module loading carefully:

```python
@pytest.mark.component
@pytest.mark.process
def test_invalid_production_configuration_fails_at_startup(run_module):
    result = run_module(
        "your_package_name",
        env={"APP_ENV": "production", "DATABASE_URL": ""},
    )

    assert result.returncode != 0
    assert "DATABASE_URL is required" in result.stderr
```

Reloading modules inside one process can leak state between tests. A subprocess is often clearer for import-time configuration and startup claims.

## 11. Fixtures and test data

Prefer the simplest representation that keeps the behavior legible.

* Inline small scalar values and compact dictionaries.
* Use factories or builders for complex domain objects.
* Store large static payloads under `tests/data/` when file identity matters.
* Generate data when broad variation is useful.
* Keep fixtures focused and composable.
* Avoid fixtures that hide the behavior under test behind extensive implicit setup.

Example factory:

```python
@pytest.fixture
def user_factory():
    def make_user(
        *,
        user_id: int = 1,
        name: str = "Alice",
        email: str = "alice@example.com",
    ) -> User:
        return User(id=user_id, name=name, email=email)

    return make_user
```

Use session-scoped expensive fixtures only when isolation and reset semantics are explicit. Shared mutable fixtures are a common source of order dependence.

## 12. Filesystem testing

Use `tmp_path` when real path, encoding, permission, atomic-write, rename, or serialization behavior matters.

```python
@pytest.mark.unit
@pytest.mark.filesystem
def test_configuration_round_trips(tmp_path):
    path = tmp_path / "config.toml"
    original = Config(enabled=True)

    original.write(path)

    assert Config.read(path) == original
```

This can still be a unit test when the file is local to the chosen boundary, ephemeral, and deterministic. Do not define unit scope solely as “no filesystem.”

Use pyfakefs or an explicit filesystem abstraction when control over faults or large virtual structures matters. Pair the double with real-filesystem evidence when platform semantics are consequential.

## 13. Time, randomness, and concurrency

### Time

Inject a clock or use framework-supported time control when business behavior depends on time. Use real monotonic time only when the test is specifically evaluating timing or scheduling semantics.

Avoid raw sleeps as synchronization:

```python
# Fragile
worker.start()
time.sleep(0.5)
assert worker.finished
```

Prefer an event, barrier, queue, callback, or bounded polling condition:

```python
worker.start()
assert finished.wait(timeout=2), "worker did not finish"
```

### Randomness

Seeded pseudorandomness is reproducible only when the generator, seed, version, and generation process are stable. Record failing generated examples and use shrinking where available.

Do not make a deterministic test depend on the ambient global random generator.

### Threads and async tasks

Tests involving concurrency should:

* assert causality rather than elapsed time,
* deadline every wait,
* propagate background exceptions,
* clean up tasks and threads,
* avoid dependence on scheduler luck,
* repeat or systematically explore schedules when race risk is material.

For asyncio, use framework-supported async fixtures and ensure pending tasks are detected at teardown.

## 14. Property-based and generative testing

Property-based testing is not limited to pure functions.

### Invariant example

```python
import hypothesis.strategies as st
from hypothesis import given


@given(st.text())
@pytest.mark.unit
@pytest.mark.property_based
def test_normalize_id_is_idempotent(value):
    assert normalize_id(normalize_id(value)) == normalize_id(value)
```

### Stateful example

```python
import hypothesis.strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule


class StackMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.stack = Stack()
        self.model = []

    @rule(value=st.integers())
    def push(self, value):
        self.stack.push(value)
        self.model.append(value)

    @rule()
    def pop_when_present(self):
        if self.model:
            assert self.stack.pop() == self.model.pop()

    @invariant()
    def sizes_match(self):
        assert len(self.stack) == len(self.model)
```

Useful properties include idempotence, round-trip behavior, bounds, conservation, monotonicity, equivalence, order independence, model agreement, and valid state transitions.

Constrain generators to the intended domain and runtime budget. A property that simply restates the implementation is not an independent oracle.

## 15. Differential and metamorphic testing

Differential testing is useful during refactoring, migration, parser replacement, optimization, or cross-platform support:

```python
@given(valid_documents())
@pytest.mark.component
@pytest.mark.differential
def test_new_parser_matches_reference(document):
    assert new_parser(document) == reference_parser(document)
```

Metamorphic testing is useful when exact expected outputs are unavailable:

```python
@given(valid_rows())
@pytest.mark.unit
@pytest.mark.metamorphic
def test_order_independent_aggregation(rows):
    assert aggregate(rows) == aggregate(list(reversed(rows)))
```

Disagreement identifies a question; it does not automatically identify which implementation is correct. Minimize the example and consult the intended contract.

## 16. Contract and compatibility testing

Contract tests should identify the producer, consumer, obligations, allowed change, and version rules.

### Schema check

```python
@pytest.mark.component
@pytest.mark.contract
def test_response_conforms_to_schema(api_component):
    response = api_component.get_user(1)

    UserResponse.model_validate(response)
```

### Behavioral contract

```python
@pytest.mark.component
@pytest.mark.contract
def test_unknown_user_has_stable_error_semantics(api_component):
    response = api_component.get_user(999)

    assert response.status == 404
    assert response.body["code"] == "user_not_found"
```

### Provider verification

Consumer-driven contracts should be versioned, published, and verified against the provider artifact. A passing consumer-side mock test is not provider verification.

Compatibility evidence may need to cover:

* old consumer against new provider,
* new consumer against old provider,
* old data read by new code,
* new data rejected or tolerated by old code,
* migration and rollback paths,
* packaged artifacts rather than source-tree objects.

## 17. Snapshot and golden testing

Snapshots are appropriate when output is large, reviewable, structurally stable, and expensive to assert field by field.

Before comparison:

* canonicalize irrelevant ordering,
* remove unstable timestamps, identifiers, or paths unless contractual,
* decode structured snapshots and assert critical semantics,
* keep snapshots small enough to review.

```python
@pytest.mark.component
@pytest.mark.snapshot
def test_manifest_matches_reviewed_golden(manifest, snapshot):
    canonical = canonicalize_manifest(manifest)

    assert canonical["schema_version"] == 3
    assert canonical == snapshot
```

Updating a snapshot means accepting a behavior change. Review the semantic diff rather than running an unconditional update command.

## 18. Observability testing

Prefer structured fields over exact prose unless wording is itself contractual.

```python
@pytest.mark.component
@pytest.mark.observability
def test_failed_job_emits_diagnostic_context(caplog, worker):
    with caplog.at_level("ERROR"):
        worker.process(Job(id="job-123", invalid=True))

    records = [record for record in caplog.records if record.name == "worker"]
    assert any(getattr(record, "job_id", None) == "job-123" for record in records)
```

For metrics and traces, validate names, dimensions, correlation identifiers, and error-path emission. System and operational tests should also establish that signals reach the actual collector or alert path when that boundary matters.

## 19. Performance testing

Separate measurement from gating until the harness is demonstrated to be stable.

A performance definition should include:

* operation or user journey,
* workload and data sizes,
* warmup,
* sample count,
* hardware and platform identity,
* dependency and configuration identity,
* statistic such as median or p95,
* natural variation,
* baseline comparability rules,
* relative and practically meaningful absolute thresholds,
* action on regression.

Use `pytest-benchmark`, a dedicated runner, or a project-specific harness where appropriate. Do not compare results from incompatible machines or workloads as though they were one series.

See `L3_T11_metrics.md` before creating a performance gate.

## 20. Coverage and mutation testing

Coverage identifies executed instrumented code. Use it to find unexamined responsibilities and suspicious gaps, not as proof of correctness.

When reviewing coverage:

* inspect missing branches and responsibilities,
* separate generated, defensive, platform-specific, and unreachable code,
* consider changed-code or risk-focused views,
* keep the code cohort and exclusions explicit,
* prevent partial runs from overwriting complete coverage.

Mutation testing evaluates whether selected implementation changes are detected. Define:

* code cohort,
* operators,
* test selection,
* timeout behavior,
* treatment of equivalent and invalid mutants,
* treatment of `no_tests` mutants,
* comparison rules across tool versions.

Use survivors as prompts for missing assertions, weak oracles, ambiguous requirements, or equivalent behavior. Do not impose a universal mutation-score target.

## 21. Static analysis and supply-chain checks

A Python `check` workflow commonly includes:

* formatter validation, such as `ruff format --check`,
* linting, such as `ruff check`,
* type checking, such as basedpyright, pyright, mypy, or ty,
* dependency vulnerability scanning,
* secret scanning across the repository and relevant history,
* package metadata and build validation,
* tests required for the decision.

Example:

```bash
uv run ruff format --check .
uv run ruff check .
uv run basedpyright
uv run pip-audit
uv run pytest
```

Select tools and gates according to the language features, threat model, deployment context, false-positive handling, and available remediation process. Security findings require triage rather than blanket suppression.

## 22. Security testing

Static and dependency scanning are baseline evidence, not complete security testing.

Add targeted tests for relevant threats such as:

* authentication and authorization boundaries,
* injection and unsafe parsing,
* path traversal,
* deserialization,
* secret handling,
* permission and role transitions,
* denial-of-service inputs,
* insecure defaults,
* failure-open behavior,
* supply-chain or artifact substitution.

Use controlled doubles for difficult fault cases and real boundary evidence for security semantics that doubles cannot establish.

## 23. Common anti-patterns

Avoid:

* arbitrary sleeps used to hide missing synchronization,
* unbounded subprocess, network, or task waits,
* deep mocks of internal call graphs,
* fakes treated as proof of production dependency behavior,
* giant end-to-end suites duplicating every lower-level case,
* low-level tests that omit the real semantics behind the risk,
* exact log-string assertions when structured fields are the contract,
* broad snapshots replacing deliberate assertions,
* test order dependence,
* shared mutable fixtures without reset guarantees,
* retries that silently convert intermittent failure into success,
* selected runs overwriting complete evidence,
* coverage or mutation percentages treated as correctness,
* permanent skips, `xfail`, warning filters, or quarantines without ownership and review,
* source-tree tests presented as evidence that the built package works,
* Python-specific conventions presented as universal testing definitions.

## 24. Relationship to repository documents

* `Overview.md` defines normative policy.
* `glossary.md` defines repository terminology.
* `L1.md` selects evidence from risk and decision context.
* `L2_*.md` define lifecycle confidence profiles.
* `L3_*.md` define procedures for particular forms of evidence.
* `automated_testing.md` discusses broader concepts and tradeoffs.
* `examples/` contains project-specific implementations and assessments.
