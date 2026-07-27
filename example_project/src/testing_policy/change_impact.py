"""Conservative path-to-claim change-impact suggestions."""

from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


def git_changed_paths(root: Path, base: str) -> list[str]:
    top_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )
    if top_result.returncode:
        raise ValueError("cannot determine git repository root")
    top = Path(top_result.stdout.strip()).resolve()
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD", "--", str(root)],
        cwd=top,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"cannot diff against {base}")
    prefix = root.relative_to(top)
    paths: list[str] = []
    for line in result.stdout.splitlines():
        candidate = Path(line)
        try:
            paths.append(candidate.relative_to(prefix).as_posix())
        except ValueError:
            continue
    return sorted(set(paths))


def impacted_claims(
    architecture: JsonObject,
    paths: list[str],
) -> tuple[set[str], dict[str, list[str]]]:
    components = architecture.get("components", {})
    if not isinstance(components, dict):
        raise ValueError("architecture components must be an object")
    claim_ids: set[str] = set()
    reasons: dict[str, list[str]] = {}
    for component_name, raw_component in components.items():
        if not isinstance(raw_component, dict):
            continue
        patterns = raw_component.get("paths", [])
        claims = raw_component.get("claims", [])
        if not isinstance(patterns, list) or not isinstance(claims, list):
            continue
        matched = sorted(
            path
            for path in paths
            if any(fnmatch.fnmatch(path, str(pattern)) for pattern in patterns)
        )
        if not matched:
            continue
        for claim in claims:
            claim_id = str(claim)
            claim_ids.add(claim_id)
            reasons.setdefault(claim_id, []).append(
                f"component {component_name} matched {', '.join(matched)}"
            )
    return claim_ids, reasons
