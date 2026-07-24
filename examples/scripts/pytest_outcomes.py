#!/usr/bin/env python
"""Normalize pytest-json-report output into portable, versioned evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import cast

type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

STRUCTURAL_SCOPES = ("unit", "component", "integration", "system", "contract")


def _object(value: JsonValue) -> JsonObject | None:
    return value if isinstance(value, dict) else None


def _array(value: JsonValue) -> list[JsonValue]:
    return value if isinstance(value, list) else []


def _string(value: JsonValue) -> str | None:
    return value if isinstance(value, str) else None


def _number(value: JsonValue) -> float:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0.0


def _properties(item: JsonObject) -> list[JsonObject]:
    return [prop for value in _array(item.get("user_properties")) if (prop := _object(value))]


def _property_values(item: JsonObject, name: str) -> tuple[str, ...]:
    values = {
        value
        for prop in _properties(item)
        if prop.get(name) is not None and isinstance((value := prop[name]), str)
    }
    return tuple(sorted(values))


def _phase_duration(item: JsonObject, phase: str) -> float:
    value = _object(item.get(phase))
    return _number(value.get("duration")) if value else 0.0


def _test_records(report: JsonObject) -> list[JsonObject]:
    records: list[JsonObject] = []
    for raw_item in _array(report.get("tests")):
        item = _object(raw_item)
        if item is None:
            continue
        nodeid = _string(item.get("nodeid"))
        outcome = _string(item.get("outcome"))
        if nodeid is None or outcome is None:
            continue
        scopes = _property_values(item, "structural_scope")
        requirements = _property_values(item, "requirement")
        records.append({
            "nodeid": nodeid,
            "outcome": outcome,
            "scope": scopes[0] if len(scopes) == 1 else "invalid",
            "requirements": list(requirements),
            "flaky": any(prop.get("flaky") is True for prop in _properties(item)),
            "durations": {
                phase: _phase_duration(item, phase) for phase in ("setup", "call", "teardown")
            },
        })
    return sorted(records, key=lambda record: cast(str, record["nodeid"]))


def _outcomes(report: JsonObject) -> list[str]:
    values: list[str] = []
    for item in _test_records(report):
        if item["outcome"] in {"skipped", "xfailed", "xpassed"}:
            values.append(f"{item['outcome']}:{item['nodeid']}")
    return values


def _git_value(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _environment(root: Path) -> JsonObject:
    lock = root / "uv.lock"
    lock_hash = hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else "missing"
    status = _git_value(root, "status", "--porcelain")
    return {
        "revision": _git_value(root, "rev-parse", "HEAD"),
        "dirty": bool(status),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "os": platform.system(),
        "architecture": platform.machine(),
        "lock_sha256": lock_hash,
        "hostname": platform.node(),
    }


def _requirements(root: Path, tests: list[JsonObject]) -> JsonObject:
    manifest = json.loads((root / "testing-requirements.json").read_text(encoding="utf-8"))
    required = cast(dict[str, dict[str, list[str]]], manifest["requirements"])
    observed: dict[str, set[str]] = defaultdict(set)
    for test in tests:
        if test["outcome"] != "passed":
            continue
        for requirement in cast(list[str], test["requirements"]):
            observed[requirement].add(cast(str, test["scope"]))
    result: JsonObject = {}
    for name, config in sorted(required.items()):
        expected = sorted(config["scopes"])
        actual = sorted(observed[name])
        result[name] = cast(JsonValue, {
            "required_scopes": expected,
            "observed_scopes": actual,
            "complete": set(expected) <= set(actual),
        })
    unknown = sorted(set(observed) - set(required))
    if unknown:
        raise ValueError(f"unknown test requirements: {', '.join(unknown)}")
    return result


def build_evidence(report: JsonObject, *, full_suite: bool, root: Path) -> JsonObject:
    tests = _test_records(report)
    scopes = Counter(cast(str, test["scope"]) for test in tests)
    requirement_coverage = _requirements(root, tests)
    incomplete = [
        name
        for name, value in requirement_coverage.items()
        if isinstance(value, dict) and value.get("complete") is not True
    ]
    flaky = sorted(cast(str, test["nodeid"]) for test in tests if test["flaky"] is True)
    duration = _number(report.get("duration")) or sum(
        sum(cast(dict[str, float], test["durations"]).values()) for test in tests
    )
    payload = cast(JsonObject, {
        "version": 4,
        "full_suite": full_suite,
        "duration_seconds": duration,
        "environment": _environment(root),
        "tests": tests,
        "requirement_coverage": requirement_coverage,
        "scope_counts": {scope: scopes[scope] for scope in STRUCTURAL_SCOPES if scopes[scope]},
        "flaky_tests": flaky,
        "outcomes": _outcomes(report),
        "decision": "fail" if full_suite and incomplete else "pass",
    })
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["run_id"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def write_evidence(report_path: Path, output_path: Path, *, full_suite: bool, root: Path) -> None:
    raw = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("pytest report must be an object")
    evidence = build_evidence(cast(JsonObject, raw), full_suite=full_suite, root=root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if full_suite:
        history = root / ".cache" / "test-history"
        history.mkdir(parents=True, exist_ok=True)
        run_id = cast(str, evidence["run_id"])
        (history / f"{run_id}.json").write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if evidence["decision"] != "pass":
            raise ValueError("full-suite requirement coverage is incomplete")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--full-suite", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        write_evidence(args.report, args.output, full_suite=args.full_suite, root=args.root.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"test evidence error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
