#!/usr/bin/env python
"""Validate, export, aggregate, and summarize local test evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import cast

type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


def read_object(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return cast(JsonObject, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_evidence(path: Path, *, require_full: bool = True) -> JsonObject:
    value = read_object(path)
    if value.get("version") != 4:
        raise ValueError(f"{path} is not version 4 test evidence")
    if require_full and value.get("full_suite") is not True:
        raise ValueError(f"{path} is partial test evidence")
    run_id = value.get("run_id")
    if not isinstance(run_id, str) or len(run_id) != 64:
        raise ValueError(f"{path} has an invalid run_id")
    environment = value.get("environment")
    tests = value.get("tests")
    requirements = value.get("requirement_coverage")
    if not isinstance(environment, dict) or not isinstance(tests, list) or not isinstance(requirements, dict):
        raise ValueError(f"{path} is missing required evidence fields")
    if value.get("decision") != "pass":
        raise ValueError(f"{path} does not contain passing evidence")
    return value


def environment_key(evidence: JsonObject) -> tuple[str, ...]:
    environment = cast(JsonObject, evidence["environment"])
    return tuple(
        str(environment.get(name, "unknown"))
        for name in ("revision", "lock_sha256", "os", "python", "architecture", "hostname")
    )


def comparable_runs(history: Path, current: JsonObject) -> list[JsonObject]:
    key = environment_key(current)
    runs: list[JsonObject] = []
    for path in sorted(history.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            candidate = validate_evidence(path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if environment_key(candidate) == key:
            runs.append(candidate)
    return runs[:20]


def health(evidence_path: Path, history: Path) -> int:
    current = validate_evidence(evidence_path)
    runs = comparable_runs(history, current)
    outcomes: dict[str, set[str]] = defaultdict(set)
    durations: dict[str, list[float]] = defaultdict(list)
    for run in runs:
        for raw_test in cast(list[JsonValue], run["tests"]):
            if not isinstance(raw_test, dict):
                continue
            nodeid = raw_test.get("nodeid")
            outcome = raw_test.get("outcome")
            phases = raw_test.get("durations")
            if isinstance(nodeid, str) and isinstance(outcome, str):
                outcomes[nodeid].add(outcome)
            if isinstance(nodeid, str) and isinstance(phases, dict):
                values = [value for value in phases.values() if isinstance(value, (int, float))]
                durations[nodeid].append(float(sum(values)))
    flaky = sorted(nodeid for nodeid, values in outcomes.items() if len(values) > 1)
    observations = sum(len(values) for values in outcomes.values())
    flake_rate = (len(flaky) / observations * 100) if observations else 0.0
    slowest = sorted(
        ((max(values), nodeid) for nodeid, values in durations.items()), reverse=True
    )[:10]
    print(f"Comparable full runs: {len(runs)}/20")
    print(f"Observed flaky tests: {len(flaky)} ({flake_rate:.2f}%)")
    print("Slowest tests:")
    for duration, nodeid in slowest:
        print(f"  {duration:.3f}s  {nodeid}")
    if flaky:
        for nodeid in flaky:
            print(f"flake: {nodeid}", file=sys.stderr)
    return 1 if flake_rate >= 1.0 else 0


def compatibility(evidence_path: Path, destination: Path) -> Path:
    evidence = validate_evidence(evidence_path)
    environment = cast(JsonObject, evidence["environment"])
    python_minor = ".".join(str(environment["python"]).split(".")[:2])
    cell: JsonObject = {
        "version": 1,
        "kind": "package_name-compatibility-evidence",
        "os": environment["os"],
        "python": python_minor,
        "architecture": environment["architecture"],
        "revision": environment["revision"],
        "lock_sha256": environment["lock_sha256"],
        "test_run_id": evidence["run_id"],
        "test_evidence_sha256": digest(evidence_path),
        "decision": "pass",
    }
    destination.mkdir(parents=True, exist_ok=True)
    name = f"{cell['os']}-py{python_minor}-{cell['architecture']}.json"
    output = destination / name
    output.write_text(json.dumps(cell, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return output


def compatibility_check(directory: Path, matrix_path: Path, evidence_path: Path) -> int:
    current = validate_evidence(evidence_path)
    environment = cast(JsonObject, current["environment"])
    matrix = read_object(matrix_path)
    required = matrix.get("required")
    if not isinstance(required, list):
        raise ValueError("compatibility matrix required must be an array")
    found: dict[tuple[str, str], JsonObject] = {}
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        cell = read_object(path)
        if cell.get("kind") != "package_name-compatibility-evidence" or cell.get("decision") != "pass":
            continue
        if cell.get("revision") != environment["revision"] or cell.get("lock_sha256") != environment["lock_sha256"]:
            errors.append(f"stale compatibility evidence: {path}")
            continue
        os_name, python = cell.get("os"), cell.get("python")
        if isinstance(os_name, str) and isinstance(python, str):
            found[os_name, python] = cell
    missing: list[str] = []
    for raw in required:
        if not isinstance(raw, dict) or not isinstance(raw.get("os"), str) or not isinstance(raw.get("python"), str):
            raise ValueError("compatibility matrix cells require os and python strings")
        key = cast(str, raw["os"]), cast(str, raw["python"])
        if key not in found:
            missing.append(f"{key[0]} Python {key[1]}")
    for message in (*errors, *(f"missing compatibility evidence: {cell}" for cell in missing)):
        print(message, file=sys.stderr)
    print(f"Compatibility cells: {len(found)}/{len(required)} required")
    return 1 if errors or missing else 0


def export_evidence(evidence_path: Path, destination: Path) -> None:
    evidence = validate_evidence(evidence_path)
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / evidence_path.name
    shutil.copyfile(evidence_path, output)
    manifest = {
        "version": 1,
        "files": {output.name: digest(output)},
        "revision": cast(JsonObject, evidence["environment"])["revision"],
        "lock_sha256": cast(JsonObject, evidence["environment"])["lock_sha256"],
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def import_evidence(bundle: Path, destination: Path) -> None:
    manifest = read_object(bundle / "manifest.json")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("evidence bundle manifest files must be an object")
    destination.mkdir(parents=True, exist_ok=True)
    for name, expected in files.items():
        if not isinstance(name, str) or not isinstance(expected, str) or Path(name).name != name:
            raise ValueError("evidence bundle contains an invalid file entry")
        source = bundle / name
        validate_evidence(source)
        if digest(source) != expected:
            raise ValueError(f"evidence digest mismatch: {name}")
        shutil.copyfile(source, destination / name)


def record_defect(
    ledger: Path,
    *,
    defect_id: str,
    affected_version: str,
    context: str,
    fix_revision: str,
    regression_test: str,
) -> None:
    if any(not value.strip() for value in (defect_id, affected_version, context, fix_revision, regression_test)):
        raise ValueError("defect fields must be nonempty")
    data: JsonObject = {"version": 1, "defects": []}
    if ledger.exists():
        data = read_object(ledger)
    defects = data.get("defects")
    if not isinstance(defects, list):
        raise ValueError("defect ledger defects must be an array")
    if any(isinstance(item, dict) and item.get("id") == defect_id for item in defects):
        raise ValueError(f"duplicate defect id: {defect_id}")
    defects.append({
        "id": defect_id,
        "affected_version": affected_version,
        "context": context,
        "fix_revision": fix_revision,
        "regression_test": regression_test,
    })
    defects.sort(key=lambda item: str(item.get("id")) if isinstance(item, dict) else "")
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    health_parser = commands.add_parser("health")
    health_parser.add_argument("evidence", type=Path)
    health_parser.add_argument("history", type=Path)
    compat = commands.add_parser("compatibility")
    compat.add_argument("evidence", type=Path)
    compat.add_argument("destination", type=Path)
    check = commands.add_parser("compatibility-check")
    check.add_argument("directory", type=Path)
    check.add_argument("matrix", type=Path)
    check.add_argument("evidence", type=Path)
    export = commands.add_parser("export")
    export.add_argument("evidence", type=Path)
    export.add_argument("destination", type=Path)
    import_parser = commands.add_parser("import")
    import_parser.add_argument("bundle", type=Path)
    import_parser.add_argument("destination", type=Path)
    defect = commands.add_parser("record-defect")
    defect.add_argument("ledger", type=Path)
    defect.add_argument("--id", required=True)
    defect.add_argument("--affected-version", required=True)
    defect.add_argument("--context", required=True)
    defect.add_argument("--fix-revision", required=True)
    defect.add_argument("--regression-test", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "health":
            return health(args.evidence, args.history)
        if args.command == "compatibility":
            compatibility(args.evidence, args.destination)
        elif args.command == "compatibility-check":
            return compatibility_check(args.directory, args.matrix, args.evidence)
        elif args.command == "export":
            export_evidence(args.evidence, args.destination)
        elif args.command == "import":
            import_evidence(args.bundle, args.destination)
        elif args.command == "record-defect":
            record_defect(
                args.ledger,
                defect_id=args.id,
                affected_version=args.affected_version,
                context=args.context,
                fix_revision=args.fix_revision,
                regression_test=args.regression_test,
            )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"test evidence error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
