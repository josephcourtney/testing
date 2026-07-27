"""Filesystem contracts for testing-policy state."""

from __future__ import annotations

import json
import os
import tempfile
from importlib.resources import files
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


def read_object(path: Path) -> JsonObject:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_object(path: Path, value: JsonObject, *, replace: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        raise ValueError(f"refusing to replace existing record: {path}")
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def find_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".testing" / "project.json").is_file():
            return candidate
    raise ValueError("no .testing/project.json found")


def load_catalog() -> list[JsonObject]:
    resource = files("testing_policy").joinpath("rules/catalog.json")
    value = json.loads(resource.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("rules"), list):
        raise ValueError("built-in rule catalog is invalid")
    rules = value["rules"]
    if not all(isinstance(rule, dict) for rule in rules):
        raise ValueError("built-in rules must be objects")
    return rules


def load_state(root: Path) -> JsonObject:
    policy_root = root / ".testing"
    project = read_object(policy_root / "project.json")
    claims = read_object(policy_root / "claims.json")
    architecture = read_object(policy_root / "architecture.json")
    policies = read_object(policy_root / "policies.json")
    commands = read_object(policy_root / "commands.json")
    rules = load_catalog()
    additional = policies.get("additional_rules", [])
    if not isinstance(additional, list) or not all(isinstance(rule, dict) for rule in additional):
        raise ValueError("additional_rules must be an array of objects")
    return {
        "root": root,
        "policy_root": policy_root,
        "project": project,
        "claims": claims,
        "architecture": architecture,
        "policies": policies,
        "commands": commands,
        "rules": [*rules, *additional],
    }
