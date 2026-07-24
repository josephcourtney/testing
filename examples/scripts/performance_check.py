#!/usr/bin/env python
"""Measure stable CLI operations and gate calibrated performance regressions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable, cast

type JsonObject = dict[str, object]


def invoke(argv: list[str], *, cwd: Path, env: dict[str, str]) -> float:
    started = time.perf_counter()
    result = subprocess.run(
        argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=10, check=False
    )
    elapsed = time.perf_counter() - started
    if result.returncode not in {0, 3}:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"performance command failed ({result.returncode}): {detail}")
    return elapsed


def fingerprint(root: Path) -> JsonObject:
    lock = root / "uv.lock"
    return {
        "os": platform.system(),
        "python": ".".join(platform.python_version().split(".")[:2]),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
    }


def measure(root: Path, executable: Path) -> JsonObject:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory(prefix="package_name-performance-") as raw:
        work = Path(raw)
        capture_argv = [
            str(executable), "describe", "python:tests.fixtures.target_app:app",
            "--program", "fixture", "--format", "json",
        ]
        captured = subprocess.run(
            capture_argv, cwd=root, env=env, capture_output=True, text=True, timeout=10, check=False
        )
        if captured.returncode != 0:
            raise ValueError(f"could not prepare performance artifact: {captured.stderr.strip()}")
        artifact = work / "snapshot.json"
        artifact.write_text(captured.stdout, encoding="utf-8")
        operations: dict[str, tuple[list[str], Path]] = {
            "cli-startup": ([str(executable), "--help"], work),
            "snapshot-capture": (capture_argv, root),
            "artifact-reload": (
                [str(executable), "describe", f"artifact:{artifact}", "--format", "json"], work
            ),
            "failed-import": (
                [str(executable), "describe", "python:missing.module:app", "--program", "missing", "--format", "json"], work
            ),
        }
        results: dict[str, list[float]] = {}
        for name, (argv, cwd) in operations.items():
            for _ in range(2):
                invoke(argv, cwd=cwd, env=env)
            results[name] = [invoke(argv, cwd=cwd, env=env) for _ in range(7)]
    return {
        "version": 1,
        "fingerprint": fingerprint(root),
        "operations": {
            name: {
                "samples_seconds": values,
                "median_seconds": statistics.median(values),
                "coefficient_of_variation": statistics.stdev(values) / statistics.mean(values),
            }
            for name, values in sorted(results.items())
        },
    }


def comparable(history: Path, report: JsonObject) -> list[JsonObject]:
    expected = report["fingerprint"]
    records: list[JsonObject] = []
    for path in sorted(history.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and value.get("fingerprint") == expected:
            records.append(cast(JsonObject, value))
    return records


def calibrate(history: Path, report: JsonObject, baseline_path: Path) -> None:
    records = comparable(history, report)
    if len(records) < 10:
        raise ValueError(f"performance calibration requires 10 comparable runs; found {len(records)}")
    operation_names = cast(dict[str, object], report["operations"]).keys()
    baselines: dict[str, object] = {}
    for name in operation_names:
        medians = [
            float(cast(dict[str, dict[str, float]], record["operations"])[name]["median_seconds"])
            for record in records[:10]
        ]
        coefficient = statistics.stdev(medians) / statistics.mean(medians)
        if coefficient > 0.10:
            raise ValueError(f"performance calibration for {name} is noisy: CV={coefficient:.3f}")
        baselines[name] = {"median_seconds": statistics.median(medians), "calibration_cv": coefficient}
    baseline = {
        "version": 1,
        "status": "calibrated",
        "fingerprint": report["fingerprint"],
        "thresholds": {"absolute_allowance_seconds": 0.1, "relative_multiplier": 1.15},
        "operations": baselines,
    }
    baseline_path.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def gate(report: JsonObject, baseline_path: Path, *, strict: bool) -> tuple[str, list[str]]:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if not isinstance(baseline, dict) or baseline.get("status") != "calibrated":
        return ("fail" if strict else "conditional-pass", ["performance baseline is uncalibrated"])
    if baseline.get("fingerprint") != report["fingerprint"]:
        return ("fail" if strict else "conditional-pass", ["performance baseline fingerprint differs"])
    thresholds = cast(dict[str, float], baseline["thresholds"])
    errors: list[str] = []
    for name, raw in cast(dict[str, dict[str, float]], report["operations"]).items():
        expected = cast(dict[str, dict[str, float]], baseline["operations"])[name]["median_seconds"]
        current = raw["median_seconds"]
        if current > expected * thresholds["relative_multiplier"] and current > expected + thresholds["absolute_allowance_seconds"]:
            errors.append(f"{name} regressed from {expected:.3f}s to {current:.3f}s")
    return ("fail" if errors else "pass", errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--history", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--update-baseline", action="store_true")
    args = parser.parse_args()
    try:
        report = measure(args.root.resolve(), args.executable.resolve())
        args.history.mkdir(parents=True, exist_ok=True)
        canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
        report["run_id"] = hashlib.sha256(canonical.encode()).hexdigest()
        history_path = args.history / f"{report['run_id']}.json"
        history_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.update_baseline:
            calibrate(args.history, report, args.baseline)
        decision, errors = gate(report, args.baseline, strict=args.strict)
        report["decision"] = decision
        report["findings"] = errors
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        for error in errors:
            print(error, file=sys.stderr)
        return 1 if decision == "fail" else 0
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"performance error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
