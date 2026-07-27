#!/usr/bin/env python
"""Run a trusted or explicitly partial pytest selection and retain separate evidence."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from scripts.pytest_outcomes import write_evidence


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--root", type=Path, default=Path.cwd())
    root.add_argument("--fast", action="store_true")
    root.add_argument("--marker")
    root.add_argument("--quarantined", action="store_true")
    root.add_argument("selection", nargs="*")
    return root


def marker_expression(args: argparse.Namespace) -> str:
    if args.quarantined:
        return "quarantined"
    clauses = ["not quarantined"]
    if args.fast:
        clauses.append("not slow")
    if args.marker:
        clauses.append(f"({args.marker})")
    return " and ".join(clauses)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    full_suite = not (args.fast or args.marker or args.quarantined or args.selection)
    expression = marker_expression(args)
    evidence_dir = root / ".cache" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    stem = "full" if full_suite else "partial"
    report_path = evidence_dir / f"pytest-{stem}.json"
    evidence_path = evidence_dir / f"{stem}.json"
    coverage_path = root / (".coverage" if full_suite else ".cache/coverage-partial")

    command = [
        sys.executable,
        "-m",
        "pytest",
        "-m",
        expression,
        "--json-report",
        "--json-report-file",
        str(report_path),
    ]
    if full_suite:
        command.extend(
            [
                "--cov=testing_reference",
                "--cov-branch",
                "--cov-report=term-missing",
            ]
        )
    command.extend(args.selection or ["tests"])
    result = subprocess.run(
        command,
        cwd=root,
        env={**os.environ, "COVERAGE_FILE": str(coverage_path)},
        check=False,
    )
    if not report_path.exists():
        print("pytest did not produce its JSON report", file=sys.stderr)
        return result.returncode or 2
    evidence = write_evidence(
        report_path,
        evidence_path,
        pytest_exit_code=result.returncode,
        full_suite=full_suite,
        selection_expression=expression,
        selection_arguments=list(args.selection),
        root=root,
    )
    print(f"evidence: {evidence_path}")
    return result.returncode or (0 if evidence["decision"] == "pass" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
