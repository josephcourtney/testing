#!/usr/bin/env python
"""Measure the packaged command against its project-specific latency specification."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path


def invoke(root: Path) -> tuple[int, float]:
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, "-m", "testing_reference.cli", "Alpha", "Beta", "Gamma"],
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(root / "src")},
        text=True,
    )
    return result.returncode, time.monotonic() - started


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(".cache/evidence/performance.json"))
    args = parser.parse_args(argv)
    root = args.root.resolve()
    specifications = json.loads((root / "metric-specifications.json").read_text(encoding="utf-8"))
    threshold = specifications["metrics"]["cli-latency"]["threshold"]
    for _ in range(2):
        return_code, _ = invoke(root)
        if return_code:
            print("performance workload failed during warmup", file=sys.stderr)
            return 2
    measurements: list[float] = []
    for _ in range(7):
        return_code, duration = invoke(root)
        if return_code:
            print("performance workload failed", file=sys.stderr)
            return 2
        measurements.append(duration)
    median = statistics.median(measurements)
    payload = {
        "version": 1,
        "kind": "testing-reference-performance-evidence",
        "decision": "pass" if median <= threshold else "fail",
        "metric": "cli-latency",
        "measurements_seconds": measurements,
        "median_seconds": median,
        "threshold_seconds": threshold,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"median {median:.4f}s; threshold {threshold:.4f}s")
    return 0 if payload["decision"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
