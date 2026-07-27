#!/usr/bin/env python
"""Normalize pytest-json-report output into fail-closed version-5 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
STRUCTURAL_SCOPES = ("unit", "component", "integration", "system")
PURPOSES = ("acceptance", "regression", "contract", "smoke", "compatibility")
TECHNIQUES = ("property_based", "fuzz")


def read_object(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def git_value(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def worktree_digest(root: Path) -> str:
    difference = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--", "."],
        cwd=root,
        capture_output=True,
        check=False,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if difference.returncode or untracked.returncode:
        return "unknown"
    identity = hashlib.sha256(difference.stdout)
    for raw_name in sorted(filter(None, untracked.stdout.split(b"\0"))):
        path = root / raw_name.decode()
        if path.is_file():
            identity.update(raw_name)
            identity.update(path.read_bytes())
    return identity.hexdigest()


def properties(item: JsonObject) -> list[JsonObject]:
    raw = item.get("user_properties", [])
    if not isinstance(raw, list):
        return []
    normalized: list[JsonObject] = []
    for value in raw:
        if isinstance(value, dict):
            normalized.append(value)
        elif isinstance(value, list | tuple) and len(value) == 2 and isinstance(value[0], str):
            normalized.append({value[0]: value[1]})
    return normalized


def property_values(item: JsonObject, name: str) -> tuple[Any, ...]:
    return tuple(prop[name] for prop in properties(item) if name in prop)


def test_records(report: JsonObject) -> list[JsonObject]:
    raw_tests = report.get("tests", [])
    if not isinstance(raw_tests, list):
        raise ValueError("pytest report tests must be an array")
    records: list[JsonObject] = []
    for raw_item in raw_tests:
        if not isinstance(raw_item, dict):
            continue
        nodeid = raw_item.get("nodeid")
        outcome = raw_item.get("outcome")
        if not isinstance(nodeid, str) or not isinstance(outcome, str):
            continue
        scopes = tuple(str(value) for value in property_values(raw_item, "structural_scope"))
        requirements = sorted(str(value) for value in property_values(raw_item, "requirement"))
        purposes = sorted(str(value) for value in property_values(raw_item, "purpose"))
        techniques = sorted(str(value) for value in property_values(raw_item, "technique"))
        records.append(
            {
                "nodeid": nodeid,
                "outcome": outcome,
                "scope": scopes[0] if len(scopes) == 1 else "invalid",
                "scope_values": list(scopes),
                "purposes": purposes,
                "techniques": techniques,
                "quarantined": True in property_values(raw_item, "quarantined"),
                "requirements": requirements,
            }
        )
    return sorted(records, key=lambda item: str(item["nodeid"]))


def requirement_coverage(root: Path, tests: list[JsonObject]) -> JsonObject:
    manifest = read_object(root / "testing-requirements.json")
    required = manifest.get("requirements")
    if not isinstance(required, dict):
        raise ValueError("testing-requirements.json requires an object named requirements")
    observed: dict[str, set[str]] = defaultdict(set)
    for test in tests:
        if test["outcome"] != "passed":
            continue
        for requirement in test["requirements"]:
            observed[str(requirement)].add(str(test["scope"]))
    result: JsonObject = {}
    for name, raw_config in sorted(required.items()):
        if not isinstance(raw_config, dict) or not isinstance(raw_config.get("scopes"), list):
            raise ValueError(f"requirement {name} must declare scopes")
        expected = sorted(str(value) for value in raw_config["scopes"])
        actual = sorted(observed[name])
        result[name] = {
            "required_scopes": expected,
            "observed_scopes": actual,
            "complete": set(expected) <= set(actual),
        }
    unknown = sorted(set(observed) - set(required))
    if unknown:
        raise ValueError(f"unknown requirements: {', '.join(unknown)}")
    return result


def quarantine_entries(root: Path) -> list[JsonObject]:
    manifest = read_object(root / "quarantine.json")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not all(isinstance(item, dict) for item in entries):
        raise ValueError("quarantine.json entries must be an array of objects")
    nodeids = [str(item.get("nodeid", "")) for item in entries]
    if any(not nodeid for nodeid in nodeids) or len(nodeids) != len(set(nodeids)):
        raise ValueError("quarantine entries require unique nonempty nodeids")
    for item in entries:
        required_fields = ("owner", "rationale", "expiry")
        if not all(isinstance(item.get(field), str) and item[field] for field in required_fields):
            raise ValueError("quarantine entries require owner, rationale, and expiry")
        try:
            expiry = date.fromisoformat(str(item["expiry"]))
        except ValueError as error:
            raise ValueError("quarantine expiry must use YYYY-MM-DD") from error
        if expiry <= date.today():
            raise ValueError(f"expired quarantine entry: {item['nodeid']}")
    return sorted(entries, key=lambda item: str(item["nodeid"]))


def environment(root: Path) -> JsonObject:
    return {
        "revision": git_value(root, "rev-parse", "HEAD"),
        "dirty": bool(git_value(root, "status", "--porcelain")),
        "worktree_sha256": worktree_digest(root),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "os": platform.system(),
        "architecture": platform.machine(),
        "lock_sha256": digest(root / "uv.lock"),
        "pyproject_sha256": digest(root / "pyproject.toml"),
        "requirements_sha256": digest(root / "testing-requirements.json"),
        "quarantine_sha256": digest(root / "quarantine.json"),
    }


def build_evidence(
    report: JsonObject,
    *,
    pytest_exit_code: int,
    full_suite: bool,
    selection_expression: str,
    selection_arguments: list[str],
    root: Path,
) -> JsonObject:
    tests = test_records(report)
    requirements = requirement_coverage(root, tests)
    quarantine = quarantine_entries(root)
    quarantined_nodeids = {str(item["nodeid"]) for item in quarantine}
    findings: list[str] = []

    if pytest_exit_code != 0:
        findings.append(f"pytest exited with status {pytest_exit_code}")
    if not tests:
        findings.append("no tests were executed")
    for test in tests:
        if test["scope"] not in STRUCTURAL_SCOPES:
            findings.append(f"invalid structural scope: {test['nodeid']}")
        if full_suite and test["outcome"] != "passed":
            findings.append(f"non-passing trusted test: {test['nodeid']} ({test['outcome']})")
        if full_suite and (
            test["quarantined"] is True or str(test["nodeid"]) in quarantined_nodeids
        ):
            findings.append(f"quarantined test entered trusted evidence: {test['nodeid']}")
    if full_suite:
        for name, value in requirements.items():
            if not isinstance(value, dict) or value.get("complete") is not True:
                findings.append(f"incomplete requirement coverage: {name}")
    if full_suite and selection_expression != "not quarantined":
        findings.append("trusted selection must be exactly 'not quarantined'")

    scopes = Counter(str(test["scope"]) for test in tests)
    payload: JsonObject = {
        "version": 5,
        "kind": "testing-reference-test-evidence",
        "decision": "fail" if findings else "pass",
        "findings": findings,
        "full_suite": full_suite,
        "selection": {
            "expression": selection_expression,
            "arguments": selection_arguments,
            "excluded_quarantine": quarantine if full_suite else [],
        },
        "pytest": {
            "exit_code": pytest_exit_code,
            "duration_seconds": report.get("duration"),
            "summary": report.get("summary", {}),
        },
        "environment": environment(root),
        "tests": tests,
        "requirement_coverage": requirements,
        "scope_counts": {scope: scopes[scope] for scope in STRUCTURAL_SCOPES if scopes[scope]},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["run_id"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def write_evidence(
    report_path: Path,
    output_path: Path,
    *,
    pytest_exit_code: int,
    full_suite: bool,
    selection_expression: str,
    selection_arguments: list[str],
    root: Path,
) -> JsonObject:
    report = read_object(report_path)
    evidence = build_evidence(
        report,
        pytest_exit_code=pytest_exit_code,
        full_suite=full_suite,
        selection_expression=selection_expression,
        selection_arguments=selection_arguments,
        root=root,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if full_suite:
        history = root / ".cache" / "test-history"
        history.mkdir(parents=True, exist_ok=True)
        (history / f"{evidence['run_id']}.json").write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return evidence


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("report", type=Path)
    root.add_argument("output", type=Path)
    root.add_argument("--root", type=Path, required=True)
    root.add_argument("--pytest-exit-code", type=int, required=True)
    root.add_argument("--full-suite", action="store_true")
    root.add_argument("--selection-expression", required=True)
    root.add_argument("--selection-argument", action="append", default=[])
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        evidence = write_evidence(
            args.report,
            args.output,
            pytest_exit_code=args.pytest_exit_code,
            full_suite=args.full_suite,
            selection_expression=args.selection_expression,
            selection_arguments=args.selection_argument,
            root=args.root.resolve(),
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"evidence normalization error: {error}", file=sys.stderr)
        return 2
    return 0 if evidence["decision"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
