"""Validate the durable testing-policy model before resolving obligations."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from testing_policy.execution import command_for
from testing_policy.guidance import section_excerpt
from testing_policy.io import load_state, read_object
from testing_policy.resolver import PROFILES


def _strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def _records(directory: Path, kind: str) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir():
        return errors
    for path in sorted(directory.glob("*.json")):
        value = read_object(path)
        if value.get("id") != path.stem:
            errors.append(f"{kind} {path.name} id must match its filename")
        if value.get("version") != 1 or not value.get("kind", kind):
            errors.append(f"{kind} {path.name} needs version 1 and a kind")
    return errors


def validate_state(root: Path) -> list[str]:
    """Return every structural policy-state error that can be checked locally."""
    state = load_state(root)
    errors: list[str] = []
    project = state["project"]
    profiles = project.get("profiles", {}).get("active")
    if not _strings(profiles) or not profiles:
        errors.append("project profiles.active must be a non-empty string array")
    elif unknown := sorted(set(profiles) - PROFILES):
        errors.append(f"unknown profiles: {', '.join(unknown)}")
    decisions = project.get("supported_decisions")
    if not _strings(decisions) or not decisions:
        errors.append("project supported_decisions must be a non-empty string array")

    claims = state["claims"].get("claims")
    claim_ids: set[str] = set()
    if not isinstance(claims, list):
        errors.append("claims.json must contain a claims array")
        claims = []
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("each claim must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id:
            errors.append("each claim needs a non-empty id")
            continue
        if claim_id in claim_ids:
            errors.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if not claim.get("statement") or not claim.get("owner"):
            errors.append(f"claim {claim_id} needs a statement and owner")
        if not _strings(claim.get("categories")):
            errors.append(f"claim {claim_id} categories must be a non-empty string array")

    components = state["architecture"].get("components")
    if not isinstance(components, dict):
        errors.append("architecture components must be an object")
        components = {}
    for name, component in components.items():
        if not isinstance(component, dict):
            errors.append(f"component {name} must be an object")
            continue
        if not _strings(component.get("paths")):
            errors.append(f"component {name} needs path patterns")
        references = component.get("claims")
        if not _strings(references):
            errors.append(f"component {name} needs claim ids")
        else:
            for claim_id in references:
                if claim_id not in claim_ids:
                    errors.append(f"component {name} references unknown claim {claim_id}")

    rules = state["rules"]
    rule_ids: set[str] = set()
    guidance_root = (root / str(project.get("guidance_root", ".."))).resolve()
    for rule in rules:
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id:
            errors.append("each rule needs a non-empty id")
            continue
        if rule_id in rule_ids:
            errors.append(f"duplicate rule id: {rule_id}")
        rule_ids.add(rule_id)
        if rule.get("severity") not in {"blocking", "advisory"}:
            errors.append(f"rule {rule_id} has an invalid severity")
        if not isinstance(rule.get("applies_when"), dict):
            errors.append(f"rule {rule_id} applies_when must be an object")
        requirement = rule.get("requirement")
        if not isinstance(requirement, dict) or not requirement.get("kind"):
            errors.append(f"rule {rule_id} needs a requirement kind")
        elif command_id := requirement.get("command_id"):
            try:
                command_for(state["commands"], str(command_id))
            except ValueError as error:
                errors.append(f"rule {rule_id} command is invalid: {error}")
        guidance = rule.get("guidance")
        if not isinstance(guidance, dict):
            errors.append(f"rule {rule_id} needs guidance metadata")
            continue
        document = guidance.get("document")
        section = guidance.get("section")
        if not isinstance(document, str) or not isinstance(section, str):
            errors.append(f"rule {rule_id} needs a guidance document and section")
            continue
        try:
            section_excerpt(guidance_root / document, section)
        except (OSError, ValueError) as error:
            errors.append(f"rule {rule_id} guidance is invalid: {error}")

    overrides = state["policies"].get("overrides")
    if not isinstance(overrides, dict):
        errors.append("policy overrides must be an object")
    else:
        for rule_id, override in overrides.items():
            if rule_id not in rule_ids:
                errors.append(f"override references unknown rule {rule_id}")
            if (
                not isinstance(override, dict)
                or override.get("status") != "not_applicable"
                or not override.get("owner")
                or not override.get("rationale")
            ):
                errors.append(f"override {rule_id} needs status, owner, and rationale")

    additional = state["policies"].get("additional_rules")
    if not isinstance(additional, list):
        errors.append("additional_rules must be an array")
    raw_commands = state["commands"].get("commands")
    if not isinstance(raw_commands, dict):
        errors.append("commands.json must contain a commands object")
    else:
        for command_id in raw_commands:
            try:
                command_for(state["commands"], str(command_id))
            except ValueError as error:
                errors.append(str(error))
    errors.extend(_records(root / ".testing" / "decisions", "decision"))
    errors.extend(_records(root / ".testing" / "waivers", "waiver"))
    errors.extend(_records(root / ".testing" / "attestations", "attestation"))
    for path in sorted((root / ".testing" / "decisions").glob("*.json")):
        decision = read_object(path)
        if decision.get("status") not in {"draft", "accepted", "rejected", "superseded"}:
            errors.append(f"decision {path.name} has an invalid status")
        if decision.get("status") == "accepted" and (
            not decision.get("approved_by") or not decision.get("accepted_at")
        ):
            errors.append(f"accepted decision {path.name} needs approval metadata")
    for path in sorted((root / ".testing" / "waivers").glob("*.json")):
        waiver = read_object(path)
        if waiver.get("rule_id") not in rule_ids:
            errors.append(f"waiver {path.name} references an unknown rule")
        if waiver.get("status", "active") == "active":
            required = ("owner", "rationale", "mitigation", "expiry")
            if any(not waiver.get(field) for field in required):
                errors.append(f"active waiver {path.name} lacks required context")
            else:
                try:
                    if date.fromisoformat(str(waiver["expiry"])) <= date.today():
                        errors.append(f"active waiver {path.name} has expired")
                except ValueError:
                    errors.append(f"active waiver {path.name} has an invalid expiry")
    for path in sorted((root / ".testing" / "attestations").glob("*.json")):
        attestation = read_object(path)
        if attestation.get("rule_id") not in rule_ids:
            errors.append(f"attestation {path.name} references an unknown rule")
        required = ("decision", "owner", "performed_at", "limitations", "expiry")
        if any(not attestation.get(field) for field in required):
            errors.append(f"attestation {path.name} lacks required context")
        else:
            try:
                if date.fromisoformat(str(attestation["expiry"])) <= date.today():
                    errors.append(f"attestation {path.name} has expired")
            except ValueError:
                errors.append(f"attestation {path.name} has an invalid expiry")
    return errors
