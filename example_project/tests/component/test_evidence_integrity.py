"""Component tests for the fail-closed evidence normalizer and gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from scripts.pytest_outcomes import build_evidence
from scripts.pytest_outcomes import test_records as normalize_records
from scripts.test_evidence import (
    comparable_runs,
    compatibility_check,
    flake_observation,
    validate_gate_evidence,
)


def report(*tests: dict[str, Any]) -> dict[str, Any]:
    return {"duration": 0.1, "summary": {}, "tests": list(tests)}


def item(nodeid: str, outcome: str, *properties: tuple[str, object]) -> dict[str, Any]:
    return {
        "nodeid": nodeid,
        "outcome": outcome,
        "user_properties": [list(value) for value in properties],
    }


def configured_root(tmp_path: Path, *, quarantine: list[dict[str, str]] | None = None) -> Path:
    (tmp_path / "testing-requirements.json").write_text(
        json.dumps({"requirements": {"evidence-integrity": {"scopes": ["component"]}}}),
        encoding="utf-8",
    )
    (tmp_path / "quarantine.json").write_text(
        json.dumps({"entries": quarantine or []}),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
    return tmp_path


@pytest.mark.component
@pytest.mark.requirement("evidence-integrity")
def test_failed_pytest_cannot_serialize_passing_evidence(tmp_path: Path) -> None:
    root = configured_root(tmp_path)
    evidence = build_evidence(
        report(
            item(
                "tests/test_gate.py::test_gate",
                "passed",
                ("structural_scope", "component"),
                ("requirement", "evidence-integrity"),
            )
        ),
        pytest_exit_code=1,
        full_suite=True,
        selection_expression="not quarantined",
        selection_arguments=[],
        root=root,
    )
    assert evidence["decision"] == "fail"
    assert "pytest exited with status 1" in evidence["findings"]


@pytest.mark.component
@pytest.mark.parametrize("outcome", ["failed", "skipped", "xfailed"])
def test_nonpassing_trusted_outcomes_fail_closed(tmp_path: Path, outcome: str) -> None:
    root = configured_root(tmp_path)
    evidence = build_evidence(
        report(
            item(
                "tests/test_gate.py::test_gate",
                outcome,
                ("structural_scope", "component"),
                ("requirement", "evidence-integrity"),
            )
        ),
        pytest_exit_code=0,
        full_suite=True,
        selection_expression="not quarantined",
        selection_arguments=[],
        root=root,
    )
    assert evidence["decision"] == "fail"


@pytest.mark.component
def test_contract_is_a_purpose_not_a_structural_scope() -> None:
    records = normalize_records(
        report(
            item(
                "tests/test_contract.py::test_consumer",
                "passed",
                ("structural_scope", "component"),
                ("purpose", "contract"),
            )
        )
    )
    assert records[0]["scope"] == "component"
    assert records[0]["purposes"] == ["contract"]


@pytest.mark.component
def test_legacy_evidence_cannot_satisfy_a_gate(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy.json"
    legacy.write_text(json.dumps({"version": 4, "decision": "pass"}), encoding="utf-8")
    with pytest.raises(ValueError, match="cannot satisfy a gate"):
        validate_gate_evidence(legacy)


@pytest.mark.component
def test_partial_evidence_cannot_satisfy_a_gate(tmp_path: Path) -> None:
    partial = tmp_path / "partial.json"
    partial.write_text(
        json.dumps({"version": 5, "decision": "pass", "full_suite": False}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="not passing complete"):
        validate_gate_evidence(partial)


@pytest.mark.component
def test_partial_run_can_retain_passing_selection_without_complete_coverage(
    tmp_path: Path,
) -> None:
    root = configured_root(tmp_path)
    (root / "testing-requirements.json").write_text(
        json.dumps(
            {
                "requirements": {
                    "selected": {"scopes": ["component"]},
                    "not-selected": {"scopes": ["system"]},
                }
            }
        ),
        encoding="utf-8",
    )
    evidence = build_evidence(
        report(
            item(
                "tests/test_gate.py::test_gate",
                "passed",
                ("structural_scope", "component"),
                ("requirement", "selected"),
            )
        ),
        pytest_exit_code=0,
        full_suite=False,
        selection_expression="not quarantined and component",
        selection_arguments=[],
        root=root,
    )
    assert evidence["decision"] == "pass"
    assert evidence["requirement_coverage"]["not-selected"]["complete"] is False


@pytest.mark.component
def test_quarantine_cannot_enter_trusted_evidence(tmp_path: Path) -> None:
    nodeid = "tests/test_gate.py::test_gate"
    root = configured_root(
        tmp_path,
        quarantine=[
            {
                "nodeid": nodeid,
                "owner": "maintainer",
                "rationale": "synthetic evidence-integrity test",
                "expiry": "2099-01-01",
            }
        ],
    )
    evidence = build_evidence(
        report(
            item(
                nodeid,
                "passed",
                ("structural_scope", "component"),
                ("quarantined", True),
                ("requirement", "evidence-integrity"),
            )
        ),
        pytest_exit_code=0,
        full_suite=True,
        selection_expression="not quarantined",
        selection_arguments=[],
        root=root,
    )
    assert evidence["decision"] == "fail"
    assert any("quarantined test entered" in finding for finding in evidence["findings"])


@pytest.mark.component
def test_flake_rate_uses_distinct_observed_cases_as_denominator() -> None:
    runs = [
        {"tests": [{"nodeid": "a", "outcome": "passed"}, {"nodeid": "b", "outcome": "passed"}]},
        {"tests": [{"nodeid": "a", "outcome": "failed"}, {"nodeid": "b", "outcome": "passed"}]},
    ]
    flaky, population, rate = flake_observation(runs)
    assert flaky == ["a"]
    assert population == 2
    assert rate == 50.0


@pytest.mark.component
def test_health_excludes_noncomparable_runs(tmp_path: Path) -> None:
    current = {
        "version": 5,
        "full_suite": True,
        "environment": {
            "revision": "current",
            "python": "3.14.0",
            "os": "Darwin",
            "architecture": "arm64",
            "lock_sha256": "lock",
            "pyproject_sha256": "project",
            "requirements_sha256": "requirements",
            "quarantine_sha256": "quarantine",
        },
    }
    comparable = {**current, "run_id": "comparable"}
    stale = {
        **current,
        "run_id": "stale",
        "environment": {**current["environment"], "revision": "old"},
    }
    (tmp_path / "comparable.json").write_text(json.dumps(comparable), encoding="utf-8")
    (tmp_path / "stale.json").write_text(json.dumps(stale), encoding="utf-8")
    assert [run["run_id"] for run in comparable_runs(tmp_path, current)] == ["comparable"]


@pytest.mark.component
def test_compatibility_rejects_stale_cells(tmp_path: Path) -> None:
    root = configured_root(tmp_path)
    evidence = build_evidence(
        report(
            item(
                "tests/test_gate.py::test_gate",
                "passed",
                ("structural_scope", "component"),
                ("requirement", "evidence-integrity"),
            )
        ),
        pytest_exit_code=0,
        full_suite=True,
        selection_expression="not quarantined",
        selection_arguments=[],
        root=root,
    )
    evidence_path = root / "evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    matrix_path = root / "matrix.json"
    matrix_path.write_text(
        json.dumps(
            {
                "required": [
                    {
                        "os": evidence["environment"]["os"],
                        "python": ".".join(evidence["environment"]["python"].split(".")[:2]),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    cells = root / "cells"
    cells.mkdir()
    (cells / "stale.json").write_text(
        json.dumps(
            {
                "kind": "testing-reference-compatibility-evidence",
                "decision": "pass",
                "os": evidence["environment"]["os"],
                "python": ".".join(evidence["environment"]["python"].split(".")[:2]),
                "revision": "different",
                "lock_sha256": evidence["environment"]["lock_sha256"],
                "pyproject_sha256": evidence["environment"]["pyproject_sha256"],
            }
        ),
        encoding="utf-8",
    )
    assert compatibility_check(cells, matrix_path, evidence_path) == 1
