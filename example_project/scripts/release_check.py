#!/usr/bin/env python
"""Run every release obligation, retain all outcomes, and fail closed."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--compatibility-evidence",
        type=Path,
        default=Path(".cache/compatibility"),
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    python = sys.executable
    steps = [
        ("lint", ["uv", "run", "ruff", "check", "."]),
        ("trusted-tests", [python, "-m", "scripts.run_tests"]),
        ("build", ["uv", "build"]),
        ("wheel", [python, "-m", "scripts.test_wheel"]),
        ("performance", [python, "-m", "scripts.performance_check"]),
        (
            "compatibility",
            [
                python,
                "-m",
                "scripts.test_evidence",
                "compatibility-check",
                str(args.compatibility_evidence),
                "compatibility-matrix.json",
                ".cache/evidence/full.json",
            ],
        ),
    ]
    results: list[dict[str, object]] = []
    for name, command in steps:
        started = time.monotonic()
        completed = subprocess.run(command, cwd=root, check=False)
        results.append(
            {
                "name": name,
                "command": command,
                "return_code": completed.returncode,
                "duration_seconds": time.monotonic() - started,
            }
        )
    decision = "pass" if all(item["return_code"] == 0 for item in results) else "fail"
    output = root / ".cache" / "release.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"version": 1, "decision": decision, "steps": results}, indent=2) + "\n",
        encoding="utf-8",
    )
    for item in results:
        print(f"{item['name']}: {item['return_code']}")
    print(f"release evidence: {output}")
    return 0 if decision == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
