#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import cast

from coverage import Coverage

type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]

EPSILON = 1e-9
VULTURE_PATTERN = re.compile(r"^(.*?):\d+: (.+) \((\d+)% confidence\)$")
MUTATION_FAILURE_STATUSES = {
    "check was interrupted by user",
    "not checked",
    "segfault",
    "suspicious",
    "survived",
    "timeout",
}
MUTATION_NON_FAILURE_STATUSES = {"caught by type check", "killed", "no tests", "skipped"}
KNOWN_MUTATION_STATUSES = MUTATION_FAILURE_STATUSES | MUTATION_NON_FAILURE_STATUSES


@dataclass(frozen=True)
class Thresholds:
    coverage_statement_floor: float = 80.0
    coverage_branch_floor: float = 70.0
    coverage_percentage_tolerance: float = 0.05
    coverage_missing_tolerance: int = 1
    coverage_file_min_statements: int = 20
    coverage_file_min_branches: int = 10
    duplication_percentage_ceiling: float = 5.0
    duplication_percentage_tolerance: float = 0.05
    duplication_count_tolerance: int = 1
    mutation_score_floor: float = 80.0
    mutation_score_tolerance: float = 0.1
    mutation_count_tolerance: int = 1


@dataclass(frozen=True)
class CoverageMetric:
    statements: float
    branches: float | None
    missing_statements: int
    missing_branches: int
    num_statements: int
    num_branches: int


@dataclass(frozen=True)
class DuplicationMetric:
    clones: int
    duplicated_lines: int
    duplicated_tokens: int
    percentage: float
    percentage_tokens: float
    fingerprints: tuple[str, ...]


@dataclass(frozen=True)
class MutationMetric:
    score: float
    killed: int
    no_tests: int
    total: int
    bad_mutants: tuple[str, ...]


@dataclass(frozen=True)
class Snapshot:
    coverage_global: CoverageMetric
    coverage_files: dict[str, CoverageMetric]
    dead_code: tuple[str, ...]
    duplication: dict[str, DuplicationMetric]
    outcomes: tuple[str, ...]
    mutation: MutationMetric | None


@dataclass(frozen=True)
class Baseline:
    thresholds: Thresholds
    coverage_global: CoverageMetric
    coverage_files: dict[str, CoverageMetric]
    dead_code: tuple[str, ...]
    duplication: dict[str, DuplicationMetric]
    outcomes: tuple[str, ...]
    mutation: MutationMetric | None


def _read_json(path: Path) -> JsonValue:
    return cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))


def _require_dict(value: JsonValue, label: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _number(value: JsonValue, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    return float(value)


def _integer(value: JsonValue, label: str) -> int:
    number = _number(value, label)
    if not number.is_integer():
        raise ValueError(f"{label} must be an integer")
    return int(number)


def _strings(value: JsonValue, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be an array of strings")
    return tuple(item for item in value if isinstance(item, str))


def _coverage_metric(value: JsonValue, label: str) -> CoverageMetric:
    data = _require_dict(value, label)
    branches_value = data.get("branches")
    branches = None if branches_value is None else _number(branches_value, f"{label}.branches")
    return CoverageMetric(
        statements=_number(data.get("statements"), f"{label}.statements"),
        branches=branches,
        missing_statements=_integer(data.get("missing_statements"), f"{label}.missing_statements"),
        missing_branches=_integer(data.get("missing_branches"), f"{label}.missing_branches"),
        num_statements=_integer(data.get("num_statements"), f"{label}.num_statements"),
        num_branches=_integer(data.get("num_branches"), f"{label}.num_branches"),
    )


def _duplication_metric(value: JsonValue, label: str) -> DuplicationMetric:
    data = _require_dict(value, label)
    return DuplicationMetric(
        clones=_integer(data.get("clones"), f"{label}.clones"),
        duplicated_lines=_integer(data.get("duplicated_lines"), f"{label}.duplicated_lines"),
        duplicated_tokens=_integer(data.get("duplicated_tokens"), f"{label}.duplicated_tokens"),
        percentage=_number(data.get("percentage"), f"{label}.percentage"),
        percentage_tokens=_number(data.get("percentage_tokens"), f"{label}.percentage_tokens"),
        fingerprints=_strings(data.get("fingerprints"), f"{label}.fingerprints"),
    )


def _mutation_metric(value: JsonValue, label: str) -> MutationMetric:
    data = _require_dict(value, label)
    return MutationMetric(
        score=_number(data.get("score"), f"{label}.score"),
        killed=_integer(data.get("killed"), f"{label}.killed"),
        no_tests=_integer(data.get("no_tests"), f"{label}.no_tests"),
        total=_integer(data.get("total"), f"{label}.total"),
        bad_mutants=_strings(data.get("bad_mutants"), f"{label}.bad_mutants"),
    )


def _coverage_from_summary(summary: dict[str, JsonValue], label: str) -> CoverageMetric:
    num_branches = _integer(summary.get("num_branches"), f"{label}.num_branches")
    covered_branches = _integer(summary.get("covered_branches"), f"{label}.covered_branches")
    branches = covered_branches * 100 / num_branches if num_branches else None
    return CoverageMetric(
        statements=_number(summary.get("percent_statements_covered"), f"{label}.percent_statements_covered"),
        branches=branches,
        missing_statements=_integer(summary.get("missing_lines"), f"{label}.missing_lines"),
        missing_branches=num_branches - covered_branches,
        num_statements=_integer(summary.get("num_statements"), f"{label}.num_statements"),
        num_branches=num_branches,
    )


def collect_coverage(coverage_path: Path) -> tuple[CoverageMetric, dict[str, CoverageMetric]]:
    if not coverage_path.exists():
        raise ValueError(f"coverage data does not exist: {coverage_path}")
    coverage = Coverage(data_file=str(coverage_path))
    coverage.load()
    with tempfile.NamedTemporaryFile(suffix=".json") as report_file:
        coverage.json_report(outfile=report_file.name)
        report = _require_dict(_read_json(Path(report_file.name)), "coverage report")

    totals = _require_dict(report.get("totals"), "coverage totals")
    files = _require_dict(report.get("files"), "coverage files")
    per_file: dict[str, CoverageMetric] = {}
    for path, value in files.items():
        if not path.startswith("src/"):
            continue
        label = f"coverage file {path}"
        file_data = _require_dict(value, label)
        summary = _require_dict(file_data.get("summary"), f"{label}.summary")
        per_file[path] = _coverage_from_summary(summary, label)
    return _coverage_from_summary(totals, "coverage totals"), per_file


def collect_dead_code(vulture: Path, source: Path, tests: Path) -> tuple[str, ...]:
    result = subprocess.run(
        [str(vulture), "--min-confidence", "80", str(source), str(tests)],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode not in {0, 3}:
        raise ValueError(f"vulture failed with exit code {result.returncode}: {result.stderr.strip()}")
    findings: list[str] = []
    for line in result.stdout.splitlines():
        match = VULTURE_PATTERN.match(line)
        if match is None:
            raise ValueError(f"unrecognized vulture output: {line}")
        path, message, confidence = match.groups()
        findings.append(f"{Path(path).as_posix()}:{message}:{confidence}")
    return tuple(sorted(findings))


def collect_duplication(path: Path) -> DuplicationMetric:
    data = _require_dict(_read_json(path), f"duplication report {path}")
    statistics = _require_dict(data.get("statistics"), "duplication statistics")
    total = _require_dict(statistics.get("total"), "duplication total")
    duplicates = data.get("duplicates")
    if not isinstance(duplicates, list):
        raise ValueError("duplication duplicates must be an array")
    fingerprints: list[str] = []
    for index, duplicate_value in enumerate(duplicates):
        duplicate = _require_dict(duplicate_value, f"duplicate {index}")
        first = _require_dict(duplicate.get("firstFile"), f"duplicate {index}.firstFile")
        second = _require_dict(duplicate.get("secondFile"), f"duplicate {index}.secondFile")
        first_name = first.get("name")
        second_name = second.get("name")
        fragment = duplicate.get("fragment")
        if (
            not isinstance(first_name, str)
            or not isinstance(second_name, str)
            or not isinstance(fragment, str)
        ):
            raise ValueError(f"duplicate {index} has invalid file names or fragment")
        digest = hashlib.sha256(fragment.strip().encode()).hexdigest()[:16]
        names = sorted((Path(first_name).as_posix(), Path(second_name).as_posix()))
        fingerprints.append(f"{names[0]}|{names[1]}|{digest}")
    return DuplicationMetric(
        clones=_integer(total.get("clones"), "duplication clones"),
        duplicated_lines=_integer(total.get("duplicatedLines"), "duplicated lines"),
        duplicated_tokens=_integer(total.get("duplicatedTokens"), "duplicated tokens"),
        percentage=_number(total.get("percentage"), "duplication percentage"),
        percentage_tokens=_number(total.get("percentageTokens"), "duplication token percentage"),
        fingerprints=tuple(sorted(fingerprints)),
    )


def collect_outcomes(path: Path) -> tuple[str, ...]:
    data = _require_dict(_read_json(path), "pytest outcomes")
    if data.get("version") != 4:
        raise ValueError("pytest outcomes must have version 4")
    if data.get("full_suite") is not True:
        raise ValueError("pytest outcomes are partial; run the full test suite")
    return _strings(data.get("outcomes"), "pytest outcomes")


def collect_mutation(stats_path: Path, results_path: Path) -> MutationMetric:
    stats = _require_dict(_read_json(stats_path), "mutation stats")
    status_counts: Counter[str] = Counter()
    bad_mutants: list[str] = []
    for line in results_path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if not value:
            continue
        name, separator, status = value.rpartition(": ")
        if not separator:
            raise ValueError(f"unrecognized mutation result: {line}")
        if status not in KNOWN_MUTATION_STATUSES:
            raise ValueError(f"unrecognized mutation status: {status}")
        status_counts[status] += 1
        if status in MUTATION_FAILURE_STATUSES:
            bad_mutants.append(f"{name}:{status}")
    killed = status_counts["killed"]
    no_tests = status_counts["no tests"]
    total = sum(status_counts.values())
    if killed != _integer(stats.get("killed"), "mutation killed"):
        raise ValueError("mutation killed count disagrees with mutation results")
    if no_tests != _integer(stats.get("no_tests"), "mutation no tests"):
        raise ValueError("mutation no-tests count disagrees with mutation results")
    if total != _integer(stats.get("total"), "mutation total"):
        raise ValueError("mutation total disagrees with mutation results")
    evaluated = killed + sum(status_counts[status] for status in MUTATION_FAILURE_STATUSES)
    score = killed * 100 / evaluated if evaluated else 0.0
    return MutationMetric(
        score=score,
        killed=killed,
        no_tests=no_tests,
        total=total,
        bad_mutants=tuple(sorted(bad_mutants)),
    )


def require_fresh(artifact: Path, roots: tuple[Path, ...], label: str) -> None:
    if not artifact.exists():
        raise ValueError(f"{label} does not exist: {artifact}")
    newest_input = max(
        (path.stat().st_mtime for root in roots for path in root.rglob("*.py")),
        default=0.0,
    )
    if artifact.stat().st_mtime < newest_input:
        raise ValueError(f"{label} is stale; rerun the producing recipe: {artifact}")


def collect_snapshot(args: argparse.Namespace) -> Snapshot:
    roots = (args.source, args.tests)
    require_fresh(args.coverage_data, roots, "coverage data")
    require_fresh(args.pytest_outcomes, roots, "pytest outcomes")
    if args.mutation:
        require_fresh(args.mutation_stats, roots, "mutation stats")
        require_fresh(args.mutation_results, roots, "mutation results")
    coverage_global, coverage_files = collect_coverage(args.coverage_data)
    mutation = collect_mutation(args.mutation_stats, args.mutation_results) if args.mutation else None
    return Snapshot(
        coverage_global=coverage_global,
        coverage_files=coverage_files,
        dead_code=collect_dead_code(args.vulture, args.source, args.tests),
        duplication={
            "source": collect_duplication(args.duplication_source),
            "tests": collect_duplication(args.duplication_tests),
        },
        outcomes=collect_outcomes(args.pytest_outcomes),
        mutation=mutation,
    )


def build_baseline(snapshot: Snapshot, thresholds: Thresholds, previous: Baseline | None) -> Baseline:
    coverage_files = {
        path: metric
        for path, metric in snapshot.coverage_files.items()
        if metric.num_statements >= thresholds.coverage_file_min_statements
        and (
            metric.statements < thresholds.coverage_statement_floor
            or (
                metric.num_branches >= thresholds.coverage_file_min_branches
                and metric.branches is not None
                and metric.branches < thresholds.coverage_branch_floor
            )
        )
    }
    mutation = snapshot.mutation
    if mutation is None and previous is not None:
        mutation = previous.mutation
    return Baseline(
        thresholds=thresholds,
        coverage_global=snapshot.coverage_global,
        coverage_files=coverage_files,
        dead_code=snapshot.dead_code,
        duplication=snapshot.duplication,
        outcomes=snapshot.outcomes,
        mutation=mutation,
    )


def _compare_higher(
    label: str,
    current: float | int,
    expected: float | int,
    *,
    ratchet: bool,
    tolerance: float | int = 0,
) -> list[str]:
    if current > expected + tolerance + EPSILON:
        return [f"{label} regressed from {expected} to {current} beyond tolerance {tolerance}"]
    if ratchet and current < expected - tolerance - EPSILON:
        return [f"{label} improved from {expected} to {current} beyond tolerance {tolerance}; refresh the baseline"]
    return []


def _compare_lower(
    label: str,
    current: float,
    expected: float,
    *,
    ratchet: bool,
    tolerance: float = 0.0,
) -> list[str]:
    if current < expected - tolerance - EPSILON:
        return [f"{label} regressed from {expected} to {current} beyond tolerance {tolerance}"]
    if ratchet and current > expected + tolerance + EPSILON:
        return [f"{label} improved from {expected} to {current} beyond tolerance {tolerance}; refresh the baseline"]
    return []


def _compare_sets(
    label: str, current: tuple[str, ...], expected: tuple[str, ...], *, stale: bool = True
) -> list[str]:
    errors = [f"{label}: new finding: {item}" for item in sorted(set(current) - set(expected))]
    if stale:
        errors.extend(
            f"{label}: removed finding: {item}; refresh the baseline"
            for item in sorted(set(expected) - set(current))
        )
    return errors


def check_snapshot(
    snapshot: Snapshot, baseline: Baseline, *, mutation: bool, ratchet: bool = False
) -> list[str]:
    thresholds = baseline.thresholds
    errors: list[str] = []
    errors.extend(
        _compare_lower(
            "global statement coverage",
            snapshot.coverage_global.statements,
            baseline.coverage_global.statements,
            ratchet=ratchet,
            tolerance=thresholds.coverage_percentage_tolerance,
        )
    )
    if snapshot.coverage_global.branches is not None and baseline.coverage_global.branches is not None:
        errors.extend(
            _compare_lower(
                "global branch coverage",
                snapshot.coverage_global.branches,
                baseline.coverage_global.branches,
                ratchet=ratchet,
                tolerance=thresholds.coverage_percentage_tolerance,
            )
        )
    errors.extend(
        _compare_higher(
            "missing statements",
            snapshot.coverage_global.missing_statements,
            baseline.coverage_global.missing_statements,
            ratchet=ratchet,
            tolerance=thresholds.coverage_missing_tolerance,
        )
    )
    errors.extend(
        _compare_higher(
            "missing branches",
            snapshot.coverage_global.missing_branches,
            baseline.coverage_global.missing_branches,
            ratchet=ratchet,
            tolerance=thresholds.coverage_missing_tolerance,
        )
    )
    if snapshot.coverage_global.statements < thresholds.coverage_statement_floor:
        errors.append(
            f"global statement coverage is below {thresholds.coverage_statement_floor}: "
            f"{snapshot.coverage_global.statements}"
        )
    if (
        snapshot.coverage_global.branches is not None
        and snapshot.coverage_global.branches < thresholds.coverage_branch_floor
    ):
        errors.append(
            f"global branch coverage is below {thresholds.coverage_branch_floor}: "
            f"{snapshot.coverage_global.branches}"
        )

    current_debt = build_baseline(snapshot, thresholds, baseline).coverage_files
    for path in sorted(current_debt.keys() | baseline.coverage_files.keys()):
        current = current_debt.get(path)
        expected = baseline.coverage_files.get(path)
        if current is None:
            if ratchet:
                errors.append(f"per-file coverage improved or file was removed: {path}; refresh the baseline")
        elif expected is None:
            errors.append(f"new low-coverage file: {path}")
        else:
            errors.extend(
                _compare_lower(
                    f"{path} statement coverage",
                    current.statements,
                    expected.statements,
                    ratchet=ratchet,
                    tolerance=thresholds.coverage_percentage_tolerance,
                )
            )
            if current.branches is not None and expected.branches is not None:
                errors.extend(
                    _compare_lower(
                        f"{path} branch coverage",
                        current.branches,
                        expected.branches,
                        ratchet=ratchet,
                        tolerance=thresholds.coverage_percentage_tolerance,
                    )
                )

    errors.extend(_compare_sets("dead code", snapshot.dead_code, baseline.dead_code, stale=ratchet))
    for scope in ("source", "tests"):
        current_dup = snapshot.duplication[scope]
        expected_dup = baseline.duplication[scope]
        count_fields = (
            "clones",
            "duplicated_lines",
            "duplicated_tokens",
        )
        for field in count_fields:
            errors.extend(
                _compare_higher(
                    f"{scope} duplication {field}",
                    getattr(current_dup, field),
                    getattr(expected_dup, field),
                    ratchet=ratchet,
                    tolerance=thresholds.duplication_count_tolerance,
                )
            )
        for field in ("percentage", "percentage_tokens"):
            errors.extend(
                _compare_higher(
                    f"{scope} duplication {field}",
                    getattr(current_dup, field),
                    getattr(expected_dup, field),
                    ratchet=ratchet,
                    tolerance=thresholds.duplication_percentage_tolerance,
                )
            )
        errors.extend(
            _compare_sets(
                f"{scope} duplication",
                current_dup.fingerprints,
                expected_dup.fingerprints,
                stale=ratchet,
            )
        )
        if current_dup.percentage >= thresholds.duplication_percentage_ceiling:
            errors.append(
                f"{scope} duplication exceeds {thresholds.duplication_percentage_ceiling}%: "
                f"{current_dup.percentage}%"
            )

    errors.extend(_compare_sets("pytest outcome", snapshot.outcomes, baseline.outcomes, stale=ratchet))

    if mutation:
        if snapshot.mutation is None or baseline.mutation is None:
            errors.append("mutation results or mutation baseline are missing")
        else:
            errors.extend(
                _compare_lower(
                    "mutation score",
                    snapshot.mutation.score,
                    baseline.mutation.score,
                    ratchet=ratchet,
                    tolerance=thresholds.mutation_score_tolerance,
                )
            )
            errors.extend(
                _compare_higher(
                    "mutation no-tests",
                    snapshot.mutation.no_tests,
                    baseline.mutation.no_tests,
                    ratchet=ratchet,
                    tolerance=thresholds.mutation_count_tolerance,
                )
            )
            errors.extend(
                _compare_sets(
                    "mutation",
                    snapshot.mutation.bad_mutants,
                    baseline.mutation.bad_mutants,
                    stale=ratchet,
                )
            )
            if snapshot.mutation.score < thresholds.mutation_score_floor:
                errors.append(
                    f"mutation score is below {thresholds.mutation_score_floor}: {snapshot.mutation.score}"
                )
    return errors


def print_report(snapshot: Snapshot) -> None:
    global_cov = snapshot.coverage_global
    branch_text = "n/a" if global_cov.branches is None else f"{global_cov.branches:.2f}%"
    print(
        f"Coverage: statements={global_cov.statements:.2f}% branches={branch_text} "
        f"missing_statements={global_cov.missing_statements} "
        f"missing_branches={global_cov.missing_branches}"
    )
    print(f"Dead code: findings={len(snapshot.dead_code)}")
    for scope, metric in snapshot.duplication.items():
        print(
            f"Duplication ({scope}): clones={metric.clones} lines={metric.duplicated_lines} "
            f"tokens={metric.duplicated_tokens} percentage={metric.percentage:.2f}%"
        )
    print(f"Pytest outcomes: skips_or_xfails={len(snapshot.outcomes)}")
    if snapshot.mutation is not None:
        print(
            f"Mutation: score={snapshot.mutation.score:.2f}% killed={snapshot.mutation.killed} "
            f"no_tests={snapshot.mutation.no_tests} total={snapshot.mutation.total} "
            f"bad={len(snapshot.mutation.bad_mutants)}"
        )


def _baseline_json(baseline: Baseline) -> dict[str, JsonValue]:
    return cast(dict[str, JsonValue], {"version": 1, **asdict(baseline)})


def write_baseline(path: Path, baseline: Baseline) -> None:
    path.write_text(
        json.dumps(_baseline_json(baseline), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_baseline(path: Path) -> Baseline:
    data = _require_dict(_read_json(path), "quality baseline")
    if data.get("version") != 1:
        raise ValueError("quality baseline must have version 1")
    threshold_data = _require_dict(data.get("thresholds"), "thresholds")
    defaults = Thresholds()
    thresholds = Thresholds(
        coverage_statement_floor=_number(
            threshold_data.get("coverage_statement_floor"), "coverage_statement_floor"
        ),
        coverage_branch_floor=_number(threshold_data.get("coverage_branch_floor"), "coverage_branch_floor"),
        coverage_percentage_tolerance=_number(
            threshold_data.get("coverage_percentage_tolerance", defaults.coverage_percentage_tolerance),
            "coverage_percentage_tolerance",
        ),
        coverage_missing_tolerance=_integer(
            threshold_data.get("coverage_missing_tolerance", defaults.coverage_missing_tolerance),
            "coverage_missing_tolerance",
        ),
        coverage_file_min_statements=_integer(
            threshold_data.get("coverage_file_min_statements"), "coverage_file_min_statements"
        ),
        coverage_file_min_branches=_integer(
            threshold_data.get("coverage_file_min_branches"), "coverage_file_min_branches"
        ),
        duplication_percentage_ceiling=_number(
            threshold_data.get("duplication_percentage_ceiling"), "duplication_percentage_ceiling"
        ),
        duplication_percentage_tolerance=_number(
            threshold_data.get(
                "duplication_percentage_tolerance", defaults.duplication_percentage_tolerance
            ),
            "duplication_percentage_tolerance",
        ),
        duplication_count_tolerance=_integer(
            threshold_data.get("duplication_count_tolerance", defaults.duplication_count_tolerance),
            "duplication_count_tolerance",
        ),
        mutation_score_floor=_number(threshold_data.get("mutation_score_floor"), "mutation_score_floor"),
        mutation_score_tolerance=_number(
            threshold_data.get("mutation_score_tolerance", defaults.mutation_score_tolerance),
            "mutation_score_tolerance",
        ),
        mutation_count_tolerance=_integer(
            threshold_data.get("mutation_count_tolerance", defaults.mutation_count_tolerance),
            "mutation_count_tolerance",
        ),
    )
    coverage_files_data = _require_dict(data.get("coverage_files"), "coverage_files")
    duplication_data = _require_dict(data.get("duplication"), "duplication")
    mutation_value = data.get("mutation")
    return Baseline(
        thresholds=thresholds,
        coverage_global=_coverage_metric(data.get("coverage_global"), "coverage_global"),
        coverage_files={
            path: _coverage_metric(value, f"coverage_files.{path}")
            for path, value in coverage_files_data.items()
        },
        dead_code=_strings(data.get("dead_code"), "dead_code"),
        duplication={
            scope: _duplication_metric(duplication_data.get(scope), f"duplication.{scope}")
            for scope in ("source", "tests")
        },
        outcomes=_strings(data.get("outcomes"), "outcomes"),
        mutation=None if mutation_value is None else _mutation_metric(mutation_value, "mutation"),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report and ratchet test and quality metrics.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--tests", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--coverage-data", type=Path, required=True)
    parser.add_argument("--pytest-outcomes", type=Path, required=True)
    parser.add_argument("--duplication-source", type=Path, required=True)
    parser.add_argument("--duplication-tests", type=Path, required=True)
    parser.add_argument("--vulture", type=Path, required=True)
    parser.add_argument("--mutation-stats", type=Path, default=Path("mutants/mutmut-cicd-stats.json"))
    parser.add_argument("--mutation-results", type=Path, default=Path(".cache/quality/mutmut-results.txt"))
    parser.add_argument("--mutation", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--ratchet", action="store_true")
    mode.add_argument("--update-baseline", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        previous = read_baseline(args.baseline) if args.baseline.exists() else None
        snapshot = collect_snapshot(args)
        if args.update_baseline:
            thresholds = previous.thresholds if previous is not None else Thresholds()
            baseline = build_baseline(snapshot, thresholds, previous)
            write_baseline(args.baseline, baseline)
            print(f"updated quality baseline: {args.baseline}")
            return 0
        if previous is None:
            raise ValueError(f"quality baseline does not exist: {args.baseline}")
        print_report(snapshot)
        if args.strict or args.ratchet:
            errors = check_snapshot(snapshot, previous, mutation=args.mutation, ratchet=args.ratchet)
            if errors:
                label = "Quality ratchet failed" if args.ratchet else "Quality gate failed"
                print(f"{label}:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            if args.ratchet:
                print("Quality ratchet passed: baseline is current and no regressions were found.")
            else:
                print("Quality gate passed: no regressions or unreviewed findings.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"quality metrics error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
