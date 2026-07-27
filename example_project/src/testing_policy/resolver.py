"""Resolve applicable testing-policy rules and validate their evidence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from testing_policy.change_impact import impacted_claims
from testing_policy.io import JsonObject, load_state, read_object

BLOCKING_STATUSES = {"missing", "invalid", "manual_review"}
PROFILES = {"prototype", "development", "stabilization", "production", "maintenance"}


@dataclass(frozen=True)
class Obligation:
    id: str
    title: str
    severity: str
    status: str
    reasons: tuple[str, ...]
    message: str
    requirement: JsonObject
    guidance: JsonObject

    @property
    def blocking(self) -> bool:
        return self.severity == "blocking" and self.status in BLOCKING_STATUSES

    def as_dict(self) -> JsonObject:
        value = asdict(self)
        value["blocking"] = self.blocking
        return value


def decision_record(root: Path, decision_id: str) -> JsonObject | None:
    path = root / ".testing" / "decisions" / f"{decision_id}.json"
    if not path.is_file():
        return None
    value = read_object(path)
    if value.get("id") != decision_id or value.get("status") != "accepted":
        return None
    return value


def active_waiver(root: Path, rule_id: str) -> JsonObject | None:
    directory = root / ".testing" / "waivers"
    if not directory.is_dir():
        return None
    today = date.today()
    for path in sorted(directory.glob("*.json")):
        value = read_object(path)
        if value.get("rule_id") != rule_id or value.get("status", "active") != "active":
            continue
        required = ("owner", "rationale", "mitigation", "expiry")
        if not all(isinstance(value.get(field), str) and value[field] for field in required):
            continue
        try:
            expiry = date.fromisoformat(str(value["expiry"]))
        except ValueError:
            continue
        if expiry > today:
            return value
    return None


def project_claims(
    state: JsonObject,
    changed_paths: list[str] | None,
) -> tuple[list[JsonObject], list[str]]:
    raw_claims = state["claims"].get("claims", [])
    if not isinstance(raw_claims, list) or not all(isinstance(claim, dict) for claim in raw_claims):
        raise ValueError("claims.json must contain an array named claims")
    if changed_paths is None:
        return raw_claims, []
    claim_ids, impact_reasons = impacted_claims(state["architecture"], changed_paths)
    selected = [claim for claim in raw_claims if str(claim.get("id")) in claim_ids]
    reasons = [
        f"{claim_id}: {reason}"
        for claim_id, values in sorted(impact_reasons.items())
        for reason in values
    ]
    return selected, reasons


def applicability(
    rule: JsonObject,
    *,
    decision: str,
    profiles: set[str],
    claim_tags: set[str],
    boundaries: set[str],
) -> tuple[bool, list[str]]:
    conditions = rule.get("applies_when", {})
    if not isinstance(conditions, dict):
        raise ValueError(f"rule {rule.get('id')} applies_when must be an object")
    reasons: list[str] = []
    decisions = {str(value) for value in conditions.get("decisions_any", [])}
    if decisions:
        if decision not in decisions:
            return False, []
        reasons.append(f"decision is {decision}")
    profiles_any = {str(value) for value in conditions.get("profiles_any", [])}
    if profiles_any:
        matched = profiles & profiles_any
        if not matched:
            return False, []
        reasons.append(f"active profile includes {', '.join(sorted(matched))}")
    profiles_all = {str(value) for value in conditions.get("profiles_all", [])}
    if profiles_all:
        if not profiles_all <= profiles:
            return False, []
        reasons.append(f"active profiles include {', '.join(sorted(profiles_all))}")
    claims_any = {str(value) for value in conditions.get("claims_any", [])}
    if claims_any:
        matched = claim_tags & claims_any
        if not matched:
            return False, []
        reasons.append(f"declared claim category includes {', '.join(sorted(matched))}")
    boundaries_any = {str(value) for value in conditions.get("boundaries_any", [])}
    if boundaries_any:
        matched = boundaries & boundaries_any
        if not matched:
            return False, []
        reasons.append(f"declared boundary includes {', '.join(sorted(matched))}")
    if not reasons:
        reasons.append("core policy applies")
    return True, reasons


def validate_trusted(root: Path, requirement: JsonObject) -> tuple[str, str]:
    path = root / str(requirement.get("path", ".cache/evidence/full.json"))
    if not path.is_file():
        return "missing", f"missing trusted evidence: {path.relative_to(root)}"
    value = read_object(path)
    if (
        value.get("version") != 5
        or value.get("full_suite") is not True
        or value.get("decision") != "pass"
    ):
        return "invalid", "trusted evidence is not a passing version-5 complete run"
    pytest = value.get("pytest")
    selection = value.get("selection")
    tests = value.get("tests")
    coverage = value.get("requirement_coverage")
    if not isinstance(pytest, dict) or pytest.get("exit_code") != 0:
        return "invalid", "trusted evidence records an unsuccessful test process"
    if not isinstance(selection, dict) or selection.get("expression") != "not quarantined":
        return "invalid", "trusted evidence does not use the declared selection"
    if not isinstance(tests, list) or not tests:
        return "invalid", "trusted evidence has no test records"
    if any(
        not isinstance(test, dict)
        or test.get("outcome") != "passed"
        or test.get("quarantined") is True
        or test.get("scope") not in {"unit", "component", "integration", "system"}
        for test in tests
    ):
        return "invalid", "trusted evidence contains an unacceptable test record"
    if not isinstance(coverage, dict) or any(
        not isinstance(item, dict) or item.get("complete") is not True for item in coverage.values()
    ):
        return "invalid", "trusted evidence has incomplete requirement coverage"
    return "satisfied", f"passing trusted evidence: {path.relative_to(root)}"


def validate_quarantine(root: Path, requirement: JsonObject) -> tuple[str, str]:
    path = root / str(requirement.get("path", "quarantine.json"))
    if not path.is_file():
        return "missing", f"missing quarantine manifest: {path.relative_to(root)}"
    value = read_object(path)
    entries = value.get("entries")
    if not isinstance(entries, list):
        return "invalid", "quarantine entries must be an array"
    today = date.today()
    nodeids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            return "invalid", "quarantine entries must be objects"
        required = ("nodeid", "owner", "rationale", "expiry")
        if not all(isinstance(entry.get(field), str) and entry[field] for field in required):
            return "invalid", "quarantine entry lacks nodeid, owner, rationale, or expiry"
        nodeid = str(entry["nodeid"])
        if nodeid in nodeids:
            return "invalid", f"duplicate quarantine nodeid: {nodeid}"
        nodeids.add(nodeid)
        try:
            expiry = date.fromisoformat(str(entry["expiry"]))
        except ValueError:
            return "invalid", f"invalid quarantine expiry: {nodeid}"
        if expiry <= today:
            return "invalid", f"expired quarantine entry: {nodeid}"
    return "satisfied", f"{len(entries)} valid quarantine entries"


def validate_metrics(root: Path, requirement: JsonObject) -> tuple[str, str]:
    path = root / str(requirement.get("path", "metric-specifications.json"))
    if not path.is_file():
        return "missing", f"missing metric specifications: {path.relative_to(root)}"
    value = read_object(path)
    metrics = value.get("metrics")
    if not isinstance(metrics, dict):
        return "invalid", "metric specifications require an object named metrics"
    fields = {
        "decision",
        "claim",
        "population",
        "denominator",
        "method",
        "response",
        "owner",
        "review_trigger",
    }
    for name, metric in metrics.items():
        if not isinstance(metric, dict) or any(not metric.get(field) for field in fields):
            return "invalid", f"metric {name} lacks an L3-T11 field"
        if metric.get("threshold") is not None:
            decision_id = metric.get("threshold_decision_id")
            decision = decision_record(root, decision_id) if isinstance(decision_id, str) else None
            if (
                decision is None
                or decision.get("kind") != "metric_threshold"
                or decision.get("metric") != name
                or decision.get("threshold") != metric.get("threshold")
            ):
                return "invalid", f"metric {name} threshold lacks an accepted decision"
    return "satisfied", f"{len(metrics)} complete metric specifications"


def validate_file_pass(root: Path, requirement: JsonObject) -> tuple[str, str]:
    path = root / str(requirement.get("path", ""))
    if not path.is_file():
        return "missing", f"missing evidence file: {path.relative_to(root)}"
    value = read_object(path)
    if value.get("decision") != "pass":
        return "invalid", f"{path.relative_to(root)} does not record decision=pass"
    expected_kind = requirement.get("kind_value")
    if expected_kind is not None and value.get("kind") != expected_kind:
        return "invalid", f"{path.relative_to(root)} has the wrong evidence kind"
    return "satisfied", f"passing evidence: {path.relative_to(root)}"


def validate_file_exists(root: Path, requirement: JsonObject) -> tuple[str, str]:
    path = root / str(requirement.get("path", ""))
    if not path.is_file():
        return "missing", f"missing required file: {path.relative_to(root)}"
    return "satisfied", f"required file exists: {path.relative_to(root)}"


def validate_profile(root: Path, project: JsonObject) -> tuple[str, str]:
    profiles = project.get("profiles", {}).get("active", [])
    if not isinstance(profiles, list) or not profiles:
        return "invalid", "project must declare at least one active profile"
    unknown = sorted({str(profile) for profile in profiles} - PROFILES)
    if unknown:
        return "invalid", f"unknown active profiles: {', '.join(unknown)}"
    decision_id = project.get("profile_decision")
    decision = decision_record(root, decision_id) if isinstance(decision_id, str) else None
    if (
        decision is None
        or decision.get("kind") != "profile_change"
        or decision.get("active_profiles") != profiles
    ):
        return "invalid", "active profiles lack an accepted profile decision"
    return "satisfied", f"active profiles are governed by {decision_id}"


def validate_manual(
    root: Path,
    rule_id: str,
    decision: str,
) -> tuple[str, str]:
    directory = root / ".testing" / "attestations"
    if not directory.is_dir():
        return "manual_review", "required human attestation has not been recorded"
    today = date.today()
    for path in sorted(directory.glob("*.json")):
        value = read_object(path)
        if value.get("rule_id") != rule_id or value.get("decision") != decision:
            continue
        if value.get("outcome") != "accepted":
            continue
        required = ("owner", "performed_at", "limitations", "expiry")
        if not all(value.get(field) for field in required):
            return "invalid", f"attestation {path.name} lacks required context"
        try:
            expiry = date.fromisoformat(str(value["expiry"]))
        except ValueError:
            return "invalid", f"attestation {path.name} has invalid expiry"
        if expiry <= today:
            return "manual_review", f"attestation {path.name} has expired"
        return "satisfied", f"accepted human attestation: {path.name}"
    return "manual_review", "required human attestation has not been accepted"


def validate_requirement(
    root: Path,
    project: JsonObject,
    rule: JsonObject,
    decision: str,
) -> tuple[str, str]:
    requirement = rule.get("requirement", {})
    if not isinstance(requirement, dict):
        return "invalid", "rule requirement is not an object"
    kind = requirement.get("kind")
    if kind == "project_profile":
        return validate_profile(root, project)
    if kind == "trusted_evidence":
        return validate_trusted(root, requirement)
    if kind == "quarantine":
        return validate_quarantine(root, requirement)
    if kind == "metric_specifications":
        return validate_metrics(root, requirement)
    if kind == "file_pass":
        return validate_file_pass(root, requirement)
    if kind == "file_exists":
        return validate_file_exists(root, requirement)
    if kind == "human_attestation":
        return validate_manual(root, str(rule["id"]), decision)
    return "invalid", f"unknown requirement kind: {kind}"


def resolve(
    root: Path,
    decision: str,
    *,
    changed_paths: list[str] | None = None,
) -> list[Obligation]:
    state = load_state(root)
    project = state["project"]
    supported = project.get("supported_decisions", [])
    if not isinstance(supported, list) or decision not in supported:
        raise ValueError(f"unsupported decision context: {decision}")
    raw_profiles = project.get("profiles", {}).get("active", [])
    if not isinstance(raw_profiles, list):
        raise ValueError("project profiles.active must be an array")
    profiles = {str(value) for value in raw_profiles}
    claims, _ = project_claims(state, changed_paths)
    claim_tags = {
        str(category)
        for claim in claims
        for category in claim.get("categories", [])
        if isinstance(claim.get("categories"), list)
    }
    raw_boundaries = state["architecture"].get("boundaries", {})
    if not isinstance(raw_boundaries, dict):
        raise ValueError("architecture boundaries must be an object")
    boundaries = {str(value) for value in raw_boundaries}
    overrides = state["policies"].get("overrides", {})
    if not isinstance(overrides, dict):
        raise ValueError("policy overrides must be an object")
    seen: set[str] = set()
    obligations: list[Obligation] = []
    for rule in state["rules"]:
        rule_id = str(rule.get("id", ""))
        if not rule_id or rule_id in seen:
            raise ValueError(f"duplicate or empty policy rule id: {rule_id}")
        seen.add(rule_id)
        applicable, reasons = applicability(
            rule,
            decision=decision,
            profiles=profiles,
            claim_tags=claim_tags,
            boundaries=boundaries,
        )
        if not applicable:
            continue
        override = overrides.get(rule_id)
        if override is not None:
            if (
                not isinstance(override, dict)
                or override.get("status") != "not_applicable"
                or not override.get("rationale")
                or not override.get("owner")
            ):
                status, message = "invalid", "project override is incomplete"
            else:
                status = "not_applicable"
                message = f"not applicable: {override['rationale']}"
        else:
            waiver = active_waiver(root, rule_id)
            if waiver is not None:
                status = "waived"
                message = (
                    f"waived by {waiver['owner']} until {waiver['expiry']}: {waiver['rationale']}"
                )
            else:
                status, message = validate_requirement(root, project, rule, decision)
        requirement = rule.get("requirement", {})
        guidance = rule.get("guidance", {})
        obligations.append(
            Obligation(
                id=rule_id,
                title=str(rule.get("title", rule_id)),
                severity=str(rule.get("severity", "blocking")),
                status=status,
                reasons=tuple(reasons),
                message=message,
                requirement=requirement if isinstance(requirement, dict) else {},
                guidance=guidance if isinstance(guidance, dict) else {},
            )
        )
    return sorted(obligations, key=lambda item: item.id)


def summary(obligations: list[Obligation]) -> JsonObject:
    counts: dict[str, int] = {}
    for obligation in obligations:
        counts[obligation.status] = counts.get(obligation.status, 0) + 1
    return {
        "decision": "fail" if any(item.blocking for item in obligations) else "pass",
        "counts": counts,
        "blocking": [item.id for item in obligations if item.blocking],
        "obligations": [item.as_dict() for item in obligations],
    }


def dump_summary(obligations: list[Obligation]) -> str:
    return json.dumps(summary(obligations), indent=2, sort_keys=True)
