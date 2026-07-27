"""Resolve policy rules to short and authoritative guidance."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


def guidance_path(root: Path, project: JsonObject, rule: JsonObject) -> Path:
    guidance = rule.get("guidance", {})
    if not isinstance(guidance, dict) or not isinstance(guidance.get("document"), str):
        raise ValueError(f"rule {rule.get('id')} has no guidance document")
    configured = project.get("guidance_root", ".")
    if not isinstance(configured, str):
        raise ValueError("guidance_root must be a string")
    return (root / configured / guidance["document"]).resolve()


def section_excerpt(path: Path, section: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    wanted = re.sub(r"[^a-z0-9]+", " ", section.casefold()).strip()
    start: int | None = None
    level = 0
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if not match:
            continue
        normalized = re.sub(r"[^a-z0-9]+", " ", match.group(2).casefold()).strip()
        if start is None and (wanted == normalized or wanted in normalized):
            start = index
            level = len(match.group(1))
            continue
        if start is not None and len(match.group(1)) <= level:
            return "\n".join(lines[start:index]).strip()
    if start is None:
        raise ValueError(f"section {section!r} not found in {path}")
    return "\n".join(lines[start:]).strip()


def render_guidance(root: Path, project: JsonObject, rule: JsonObject) -> str:
    guidance = rule.get("guidance", {})
    if not isinstance(guidance, dict):
        return ""
    path = guidance_path(root, project, rule)
    section = str(guidance.get("section", ""))
    summary = str(guidance.get("summary", ""))
    relative = path.relative_to((root / str(project.get("guidance_root", "."))).resolve())
    parts = [summary, f"Source: {relative} -> {section}"]
    if path.is_file() and section:
        parts.extend(["", section_excerpt(path, section)])
    return "\n".join(part for part in parts if part is not None)
