#!/usr/bin/env python
"""Validate, summarize, export, and aggregate version-5 test evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


def read_object(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_gate_evidence(path: Path) -> JsonObject:
    value = read_object(path)
    if value.get("version") != 5:
        raise ValueError(f"{path} is not version-5 evidence and cannot satisfy a gate")
    if value.get("full_suite") is not True or value.get("decision") != "pass":
        raise ValueError(f"{path} is not passing complete trusted evidence")
    pytest = value.get("pytest")
    selection = value.get("selection")
    tests = value.get("tests")
    requirements = value.get("requirement_coverage")
    if not isinstance(pytest, dict) or pytest.get("exit_code") != 0:
        raise ValueError(f"{path} does not record a successful pytest run")
    if not isinstance(selection, dict) or selection.get("expression") != "not quarantined":
        raise ValueError(f"{path} does not record the trusted selection")
    if not isinstance(tests, list) or not tests:
        raise ValueError(f"{path} has no test records")
    for test in tests:
        if not isinstance(test, dict) or test.get("outcome") != "passed":
            raise ValueError(f"{path} contains a non-passing trusted test")
        if test.get("quarantined") is True:
            raise ValueError(f"{path} contains quarantined evidence")
        if test.get("scope") not in {"unit", "component", "integration", "system"}:
            raise ValueError(f"{path} contains an invalid structural scope")
    if not isinstance(requirements, dict) or any(
        not isinstance(item, dict) or item.get("complete") is not True
        for item in requirements.values()
    ):
        raise ValueError(f"{path} has incomplete requirement coverage")
    return value


def environment_key(evidence: JsonObject) -> tuple[str, ...]:
    environment = evidence.get("environment")
    if not isinstance(environment, dict):
        raise ValueError("evidence is missing environment identity")
    names = (
        "revision",
        "worktree_sha256",
        "python",
        "os",
        "architecture",
        "lock_sha256",
        "pyproject_sha256",
        "requirements_sha256",
        "quarantine_sha256",
    )
    return tuple(str(environment.get(name, "missing")) for name in names)


def comparable_runs(history: Path, current: JsonObject) -> list[JsonObject]:
    key = environment_key(current)
    runs: list[JsonObject] = []
    for path in sorted(
        history.glob("*.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    ):
        try:
            candidate = read_object(path)
            if candidate.get("version") != 5 or candidate.get("full_suite") is not True:
                continue
            if environment_key(candidate) == key:
                runs.append(candidate)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return runs[:20]


def flake_observation(runs: list[JsonObject]) -> tuple[list[str], int, float]:
    outcomes: dict[str, set[str]] = defaultdict(set)
    for run in runs:
        tests = run.get("tests", [])
        if not isinstance(tests, list):
            continue
        for test in tests:
            if isinstance(test, dict) and isinstance(test.get("nodeid"), str):
                outcomes[test["nodeid"]].add(str(test.get("outcome", "unknown")))
    flaky = sorted(
        nodeid
        for nodeid, values in outcomes.items()
        if "passed" in values and any(value != "passed" for value in values)
    )
    population = len(outcomes)
    rate = len(flaky) / population * 100 if population else 0.0
    return flaky, population, rate


def health(evidence_path: Path, history: Path) -> int:
    current = read_object(evidence_path)
    if current.get("version") != 5 or current.get("full_suite") is not True:
        raise ValueError("health requires version-5 complete evidence")
    runs = comparable_runs(history, current)
    flaky, population, rate = flake_observation(runs)
    print(f"Comparable complete runs: {len(runs)}/20")
    print(f"Observed test cases: {population}")
    print(f"Cases with passing and failing outcomes: {len(flaky)} ({rate:.2f}%)")
    for nodeid in flaky:
        print(f"flake: {nodeid}", file=sys.stderr)
    return 1 if flaky else 0


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compatibility(evidence_path: Path, destination: Path) -> Path:
    evidence = validate_gate_evidence(evidence_path)
    environment = evidence["environment"]
    python_minor = ".".join(str(environment["python"]).split(".")[:2])
    cell = {
        "version": 1,
        "kind": "testing-reference-compatibility-evidence",
        "os": environment["os"],
        "python": python_minor,
        "architecture": environment["architecture"],
        "revision": environment["revision"],
        "worktree_sha256": environment["worktree_sha256"],
        "lock_sha256": environment["lock_sha256"],
        "pyproject_sha256": environment["pyproject_sha256"],
        "requirements_sha256": environment["requirements_sha256"],
        "quarantine_sha256": environment["quarantine_sha256"],
        "test_run_id": evidence["run_id"],
        "test_evidence_sha256": digest(evidence_path),
        "decision": "pass",
    }
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / f"{cell['os']}-py{python_minor}-{cell['architecture']}.json"
    output.write_text(json.dumps(cell, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return output


def compatibility_check(
    directory: Path,
    matrix_path: Path,
    evidence_path: Path,
) -> int:
    current = validate_gate_evidence(evidence_path)
    environment = current["environment"]
    matrix = read_object(matrix_path)
    required = matrix.get("required")
    if not isinstance(required, list):
        raise ValueError("compatibility matrix requires an array named required")
    found: set[tuple[str, str]] = set()
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        cell = read_object(path)
        if cell.get("kind") != "testing-reference-compatibility-evidence":
            continue
        if (
            cell.get("decision") != "pass"
            or cell.get("revision") != environment["revision"]
            or cell.get("worktree_sha256") != environment["worktree_sha256"]
            or cell.get("lock_sha256") != environment["lock_sha256"]
            or cell.get("pyproject_sha256") != environment["pyproject_sha256"]
            or cell.get("requirements_sha256") != environment["requirements_sha256"]
            or cell.get("quarantine_sha256") != environment["quarantine_sha256"]
        ):
            errors.append(f"invalid or stale compatibility evidence: {path}")
            continue
        found.add((str(cell.get("os")), str(cell.get("python"))))
    expected = {
        (str(item.get("os")), str(item.get("python")))
        for item in required
        if isinstance(item, dict)
    }
    missing = sorted(expected - found)
    for item in missing:
        errors.append(f"missing compatibility evidence: {item[0]} Python {item[1]}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Compatibility cells: {len(found & expected)}/{len(expected)} required")
    return 1 if errors else 0


def describe(path: Path) -> int:
    value = read_object(path)
    print(f"version: {value.get('version', 'unknown')}")
    print(f"decision: {value.get('decision', 'unknown')}")
    print(f"full_suite: {value.get('full_suite', 'unknown')}")
    if value.get("version") != 5:
        print("legacy evidence is diagnostic only and cannot satisfy a gate")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    health_parser = commands.add_parser("health")
    health_parser.add_argument("evidence", type=Path)
    health_parser.add_argument("history", type=Path)
    export = commands.add_parser("compatibility")
    export.add_argument("evidence", type=Path)
    export.add_argument("destination", type=Path)
    check = commands.add_parser("compatibility-check")
    check.add_argument("directory", type=Path)
    check.add_argument("matrix", type=Path)
    check.add_argument("evidence", type=Path)
    show = commands.add_parser("describe")
    show.add_argument("evidence", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "health":
            return health(args.evidence, args.history)
        if args.command == "compatibility":
            compatibility(args.evidence, args.destination)
            return 0
        if args.command == "compatibility-check":
            return compatibility_check(args.directory, args.matrix, args.evidence)
        if args.command == "describe":
            return describe(args.evidence)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"test evidence error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
