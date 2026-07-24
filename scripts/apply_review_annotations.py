from __future__ import annotations

import re
import subprocess
from pathlib import Path

MARKER = "TESTING-GUIDANCE-REVIEW"
SOURCE_REF = "origin/annotate-testing-guidance-review"

TARGETS = [
    Path("README.md"),
    Path("Overview.md"),
    Path("automated_testing.md"),
    Path("L1.md"),
    Path("L2_P1_prototype.md"),
    Path("L2_P2_alpha.md"),
    Path("L2_P3_beta.md"),
    Path("L2_P4_production.md"),
    Path("L2_P5_maintenance.md"),
    Path("L3_T1_unit.md"),
    Path("L3_T2_component.md"),
    Path("L3_T3_integration.md"),
    Path("L3_T4_system.md"),
    Path("L3_T5_regression.md"),
    Path("L3_T6_property-based.md"),
    Path("L3_T7_contract.md"),
    Path("L3_T8_non-functional.md"),
    Path("L3_T9_snapshot.md"),
    Path("L3_T10_health_and_metrics.md"),
    Path("examples/current-assessment.md"),
    Path("examples/local-testing.md"),
    Path("examples/production-readiness.md"),
    Path("examples/example_pyproject.toml"),
]

MD_COMMENT = re.compile(
    rf"<!--\n{MARKER}: document-level annotation\n.*?\n-->\n?",
    re.DOTALL,
)
TOML_COMMENT = re.compile(
    rf"# {MARKER}: document-level annotation\n(?:#.*\n)+\n?",
)


def source_text(path: Path) -> str:
    source_path = path.name
    result = subprocess.run(
        ["git", "show", f"{SOURCE_REF}:{source_path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def extract_annotation(path: Path) -> str:
    source = source_text(path)
    pattern = MD_COMMENT if path.suffix == ".md" else TOML_COMMENT
    match = pattern.search(source)
    if match is None:
        raise RuntimeError(f"No annotation found for {path}")
    return match.group(0).rstrip() + "\n\n"


def insert_markdown(text: str, annotation: str) -> str:
    if MARKER in text:
        return text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            boundary = end + len("\n---\n")
            return text[:boundary] + "\n" + annotation + text[boundary:]
    return annotation + text


def main() -> None:
    subprocess.run(
        ["git", "fetch", "origin", "annotate-testing-guidance-review"],
        check=True,
    )

    for path in TARGETS:
        if not path.exists():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8")
        annotation = extract_annotation(path)
        if path.suffix == ".md":
            revised = insert_markdown(original, annotation)
        else:
            revised = original if MARKER in original else annotation + original
        path.write_text(revised, encoding="utf-8")


if __name__ == "__main__":
    main()
