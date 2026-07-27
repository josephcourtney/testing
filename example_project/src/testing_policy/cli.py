"""Manage testing profiles, policy obligations, evidence, and human decisions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from testing_policy.change_impact import git_changed_paths
from testing_policy.execution import command_for
from testing_policy.guidance import render_guidance
from testing_policy.io import find_root, load_state, read_object, write_object
from testing_policy.resolver import (
    PROFILES,
    Obligation,
    applicability,
    resolve,
    summary,
    validate_metrics,
)
from testing_policy.validation import validate_state

JsonObject = dict[str, Any]


def now() -> str:
    return datetime.now(UTC).isoformat()


def root_for(value: Path | None) -> Path:
    return find_root(value or Path.cwd())


def selected_paths(args: argparse.Namespace, root: Path) -> list[str] | None:
    paths = list(args.changed_path or [])
    if args.base:
        paths.extend(git_changed_paths(root, args.base))
    return sorted(set(paths)) if paths else None


def print_obligations(
    obligations: list[Obligation],
    *,
    decision: str,
    changed_paths: list[str] | None,
) -> None:
    result = summary(obligations)
    print(f"Policy decision: {result['decision'].upper()}")
    print(f"Decision context: {decision}")
    if changed_paths is not None:
        print(f"Changed paths considered: {len(changed_paths)}")
    print("")
    for obligation in obligations:
        marker = "BLOCK" if obligation.blocking else obligation.status.upper()
        print(f"[{marker}] {obligation.id} — {obligation.title}")
        print(f"  {obligation.message}")
        print(f"  Why: {'; '.join(obligation.reasons)}")
        document = obligation.guidance.get("document")
        section = obligation.guidance.get("section")
        if document:
            print(f"  Guidance: {document} -> {section}")
    counts = ", ".join(f"{name}={count}" for name, count in sorted(result["counts"].items()))
    print(f"\nSummary: {counts or 'no applicable obligations'}")


def plan_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    paths = selected_paths(args, root)
    obligations = resolve(root, args.decision, changed_paths=paths)
    if args.json:
        value = summary(obligations)
        value["changed_paths"] = paths
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print_obligations(obligations, decision=args.decision, changed_paths=paths)
    return 0


def gate_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    paths = selected_paths(args, root)
    obligations = resolve(root, args.decision, changed_paths=paths)
    result = summary(obligations)
    if args.json:
        result["changed_paths"] = paths
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_obligations(obligations, decision=args.decision, changed_paths=paths)
    return 1 if result["decision"] == "fail" else 0


def explain_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    state = load_state(root)
    matches = [rule for rule in state["rules"] if rule.get("id") == args.rule_id]
    if len(matches) != 1:
        raise ValueError(f"unknown policy rule: {args.rule_id}")
    rule = matches[0]
    obligations = resolve(root, args.decision)
    current = next((item for item in obligations if item.id == args.rule_id), None)
    print(f"{rule['id']} — {rule.get('title', rule['id'])}")
    print(f"Severity: {rule.get('severity', 'blocking')}")
    if current is None:
        print(f"Status: not applicable to decision {args.decision}")
    else:
        print(f"Status: {current.status}")
        print(f"Why: {'; '.join(current.reasons)}")
        print(f"Evidence: {current.message}")
    print("")
    print(render_guidance(root, state["project"], rule))
    return 0


def review_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    obligations = resolve(root, args.decision)
    review = [
        item
        for item in obligations
        if item.status in {"manual_review", "waived", "invalid", "not_applicable"}
    ]
    if not review:
        print("No manual policy review is currently required.")
        return 0
    print(f"Manual policy work for {args.decision}:")
    for item in review:
        print(f"- {item.id} [{item.status}]: {item.title}")
        print(f"  {item.message}")
        print(f"  Guidance: {item.guidance.get('document')} -> {item.guidance.get('section')}")
    return 1 if any(item.blocking for item in review) else 0


def run_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    state = load_state(root)
    obligations = resolve(root, args.decision)
    commands: list[tuple[str, list[str], float]] = []
    seen: set[str] = set()
    for item in obligations:
        if item.status not in {"missing", "invalid"}:
            continue
        command_id = item.requirement.get("command_id")
        if not isinstance(command_id, str):
            continue
        if command_id not in seen:
            command, timeout = command_for(state["commands"], command_id)
            commands.append((command_id, command, timeout))
            seen.add(command_id)
    results: list[JsonObject] = []
    for command_id, command, timeout in commands:
        print(f"running {command_id}: {' '.join(command)}")
        completed = subprocess.run(command, cwd=root, check=False, timeout=timeout)
        results.append(
            {
                "command_id": command_id,
                "command": command,
                "timeout_seconds": timeout,
                "return_code": completed.returncode,
            }
        )
    output = root / ".cache" / "policy" / f"run-{args.decision}.json"
    write_object(
        output,
        {
            "version": 1,
            "kind": "testing-policy-run",
            "decision_context": args.decision,
            "created_at": now(),
            "results": results,
        },
        replace=True,
    )
    if any(item["return_code"] != 0 for item in results):
        return 1
    return gate_command(args)


def profile_show(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    project = load_state(root)["project"]
    print(json.dumps(project.get("profiles", {}), indent=2, sort_keys=True))
    print(f"profile decision: {project.get('profile_decision', 'missing')}")
    return 0


def obligations_for_profiles(
    state: JsonObject,
    profiles: set[str],
    decision: str,
) -> set[str]:
    raw_claims = state["claims"].get("claims", [])
    claim_tags = {
        str(category)
        for claim in raw_claims
        if isinstance(claim, dict) and isinstance(claim.get("categories"), list)
        for category in claim["categories"]
    }
    boundaries = set(state["architecture"].get("boundaries", {}))
    return {
        str(rule["id"])
        for rule in state["rules"]
        if applicability(
            rule,
            decision=decision,
            profiles=profiles,
            claim_tags=claim_tags,
            boundaries=boundaries,
        )[0]
    }


def profile_propose(args: argparse.Namespace) -> int:
    if args.profile not in PROFILES:
        raise ValueError(f"unknown profile: {args.profile}")
    root = root_for(args.root)
    state = load_state(root)
    current = {str(value) for value in state["project"]["profiles"]["active"]}
    proposed = current | {args.profile} if args.add else {args.profile}
    current_rules = obligations_for_profiles(state, current, args.decision)
    proposed_rules = obligations_for_profiles(state, proposed, args.decision)
    print(f"Current profiles: {', '.join(sorted(current))}")
    print(f"Proposed profiles: {', '.join(sorted(proposed))}")
    print("Added obligations:")
    for rule_id in sorted(proposed_rules - current_rules):
        print(f"- {rule_id}")
    print("Removed defaults:")
    for rule_id in sorted(current_rules - proposed_rules):
        print(f"- {rule_id}")
    print("No project state was changed.")
    return 0


def profile_apply(args: argparse.Namespace) -> int:
    if args.profile not in PROFILES:
        raise ValueError(f"unknown profile: {args.profile}")
    root = root_for(args.root)
    state = load_state(root)
    project = state["project"]
    current = {str(value) for value in project["profiles"]["active"]}
    proposed = sorted(current | {args.profile} if args.add else {args.profile})
    decision_path = root / ".testing" / "decisions" / f"{args.decision_id}.json"
    record = {
        "version": 1,
        "id": args.decision_id,
        "kind": "profile_change",
        "status": "accepted",
        "previous_profiles": sorted(current),
        "active_profiles": proposed,
        "rationale": args.rationale,
        "approved_by": args.approved_by,
        "accepted_at": now(),
    }
    write_object(decision_path, record)
    project["profiles"]["active"] = proposed
    project["profile_decision"] = args.decision_id
    write_object(root / ".testing" / "project.json", project, replace=True)
    print(f"Applied profiles: {', '.join(proposed)}")
    print(f"Decision: {args.decision_id}")
    return 0


def assessment_start(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    path = root / ".testing" / "decisions" / f"{args.id}.json"
    project = load_state(root)["project"]
    record = {
        "version": 1,
        "id": args.id,
        "kind": args.kind,
        "status": "draft",
        "owner": args.owner,
        "profiles": project["profiles"]["active"],
        "created_at": now(),
        "claims": [],
        "failure_modes": [],
        "selected_evidence": [],
        "residual_uncertainty": [],
        "waivers": [],
        "outcome": None,
    }
    write_object(path, record)
    print(path.relative_to(root))
    return 0


def decision_finalize(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    path = root / ".testing" / "decisions" / f"{args.id}.json"
    value = read_object(path)
    if value.get("status") != "draft":
        raise ValueError("only a draft decision can be finalized")
    required_lists = ("profiles", "claims", "failure_modes", "selected_evidence")
    if any(not isinstance(value.get(field), list) or not value[field] for field in required_lists):
        raise ValueError("assessment needs profiles, claims, failure_modes, and selected_evidence")
    if not isinstance(value.get("residual_uncertainty"), list) or not isinstance(
        value.get("waivers"), list
    ):
        raise ValueError("assessment needs residual_uncertainty and waiver arrays")
    value["status"] = "accepted"
    value["outcome"] = args.outcome
    value["rationale"] = args.rationale
    value["approved_by"] = args.approved_by
    value["accepted_at"] = now()
    write_object(path, value, replace=True)
    print(f"Finalized {args.id}: {args.outcome}")
    return 0


def waiver_create(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    expiry = date.fromisoformat(args.expiry)
    if expiry <= date.today():
        raise ValueError("waiver expiry must be in the future")
    path = root / ".testing" / "waivers" / f"{args.id}.json"
    value = {
        "version": 1,
        "id": args.id,
        "rule_id": args.rule_id,
        "status": "active",
        "owner": args.owner,
        "rationale": args.rationale,
        "mitigation": args.mitigation,
        "expiry": args.expiry,
        "created_at": now(),
    }
    write_object(path, value)
    print(path.relative_to(root))
    return 0


def attestation_create(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    expiry = date.fromisoformat(args.expiry)
    if expiry <= date.today():
        raise ValueError("attestation expiry must be in the future")
    path = root / ".testing" / "attestations" / f"{args.id}.json"
    value = {
        "version": 1,
        "id": args.id,
        "rule_id": args.rule_id,
        "decision": args.decision,
        "outcome": "accepted",
        "owner": args.owner,
        "performed_at": args.performed_at,
        "artifacts": list(args.artifact),
        "limitations": args.limitations,
        "expiry": args.expiry,
        "created_at": now(),
    }
    write_object(path, value)
    print(path.relative_to(root))
    return 0


def metric_validate(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    status, message = validate_metrics(root, {"path": "metric-specifications.json"})
    print(f"{status}: {message}")
    return 0 if status == "satisfied" else 1


def validate_command(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    errors = validate_state(root)
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    elif errors:
        print("Testing-policy state is invalid:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Testing-policy state is valid.")
    return 1 if errors else 0


def metric_propose(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    specifications = read_object(root / "metric-specifications.json")
    metrics = specifications.get("metrics", {})
    if not isinstance(metrics, dict) or args.metric not in metrics:
        raise ValueError(f"unknown metric: {args.metric}")
    current = metrics[args.metric]
    path = root / ".testing" / "decisions" / f"{args.id}.json"
    value = {
        "version": 1,
        "id": args.id,
        "kind": "metric_threshold",
        "status": "draft",
        "metric": args.metric,
        "previous_threshold": current.get("threshold"),
        "threshold": args.threshold,
        "owner": args.owner,
        "rationale": args.rationale,
        "observations": list(args.observation),
        "created_at": now(),
    }
    write_object(path, value)
    print(path.relative_to(root))
    return 0


def metric_apply(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    decision_path = root / ".testing" / "decisions" / f"{args.id}.json"
    decision = read_object(decision_path)
    if decision.get("kind") != "metric_threshold" or decision.get("status") != "draft":
        raise ValueError("metric decision must be a draft threshold change")
    specs_path = root / "metric-specifications.json"
    specifications = read_object(specs_path)
    metric = specifications["metrics"][str(decision["metric"])]
    metric["threshold"] = decision["threshold"]
    metric["threshold_decision_id"] = args.id
    decision["status"] = "accepted"
    decision["approved_by"] = args.approved_by
    decision["accepted_at"] = now()
    write_object(decision_path, decision, replace=True)
    write_object(specs_path, specifications, replace=True)
    print(f"Applied threshold decision {args.id}")
    return 0


def quarantine_add(args: argparse.Namespace) -> int:
    root = root_for(args.root)
    expiry = date.fromisoformat(args.expiry)
    if expiry <= date.today():
        raise ValueError("quarantine expiry must be in the future")
    path = root / "quarantine.json"
    manifest = read_object(path)
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("quarantine entries must be an array")
    if any(isinstance(item, dict) and item.get("nodeid") == args.nodeid for item in entries):
        raise ValueError(f"quarantine already contains {args.nodeid}")
    entries.append(
        {
            "nodeid": args.nodeid,
            "owner": args.owner,
            "rationale": args.rationale,
            "expiry": args.expiry,
        }
    )
    write_object(path, manifest, replace=True)
    print(f"Quarantined {args.nodeid} until {args.expiry}")
    return 0


def add_resolution_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path)
    parser.add_argument("--decision", default="merge")
    parser.add_argument("--base")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--json", action="store_true")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="Resolve obligations without changing state.")
    add_resolution_arguments(plan)
    plan.set_defaults(handler=plan_command)

    status = commands.add_parser("status", help="Show resolved policy status.")
    add_resolution_arguments(status)
    status.set_defaults(handler=plan_command)

    gate = commands.add_parser("gate", help="Fail when a blocking obligation is unresolved.")
    add_resolution_arguments(gate)
    gate.set_defaults(handler=gate_command)

    run = commands.add_parser("run", help="Run commands for unresolved mechanical obligations.")
    add_resolution_arguments(run)
    run.set_defaults(handler=run_command)

    explain = commands.add_parser("explain", help="Explain one rule and show its guidance.")
    explain.add_argument("rule_id")
    explain.add_argument("--decision", default="merge")
    explain.add_argument("--root", type=Path)
    explain.set_defaults(handler=explain_command)

    review = commands.add_parser("review", help="Show unresolved human and exception work.")
    review.add_argument("--decision", default="release")
    review.add_argument("--root", type=Path)
    review.set_defaults(handler=review_command)

    validate = commands.add_parser(
        "validate", help="Validate policy configuration and durable records."
    )
    validate.add_argument("--root", type=Path)
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(handler=validate_command)

    profile = commands.add_parser("profile")
    profile_commands = profile.add_subparsers(dest="profile_command", required=True)
    profile_show_parser = profile_commands.add_parser("show")
    profile_show_parser.add_argument("--root", type=Path)
    profile_show_parser.set_defaults(handler=profile_show)
    profile_propose_parser = profile_commands.add_parser("propose")
    profile_propose_parser.add_argument("profile")
    profile_propose_parser.add_argument("--add", action="store_true")
    profile_propose_parser.add_argument("--decision", default="release")
    profile_propose_parser.add_argument("--root", type=Path)
    profile_propose_parser.set_defaults(handler=profile_propose)
    profile_apply_parser = profile_commands.add_parser("apply")
    profile_apply_parser.add_argument("profile")
    profile_apply_parser.add_argument("--add", action="store_true")
    profile_apply_parser.add_argument("--decision-id", required=True)
    profile_apply_parser.add_argument("--approved-by", required=True)
    profile_apply_parser.add_argument("--rationale", required=True)
    profile_apply_parser.add_argument("--root", type=Path)
    profile_apply_parser.set_defaults(handler=profile_apply)

    assessment = commands.add_parser("assess")
    assessment_commands = assessment.add_subparsers(dest="assessment_command", required=True)
    assessment_start_parser = assessment_commands.add_parser("start")
    assessment_start_parser.add_argument("--id", required=True)
    assessment_start_parser.add_argument("--kind", required=True)
    assessment_start_parser.add_argument("--owner", required=True)
    assessment_start_parser.add_argument("--root", type=Path)
    assessment_start_parser.set_defaults(handler=assessment_start)

    decision = commands.add_parser("decision")
    decision_commands = decision.add_subparsers(dest="decision_command", required=True)
    finalize = decision_commands.add_parser("finalize")
    finalize.add_argument("id")
    finalize.add_argument(
        "--outcome",
        choices=["pass", "conditional_pass", "fail", "risk_acceptance"],
        required=True,
    )
    finalize.add_argument("--approved-by", required=True)
    finalize.add_argument("--rationale", required=True)
    finalize.add_argument("--root", type=Path)
    finalize.set_defaults(handler=decision_finalize)

    waiver = commands.add_parser("waive")
    waiver.add_argument("rule_id")
    waiver.add_argument("--id", required=True)
    waiver.add_argument("--owner", required=True)
    waiver.add_argument("--rationale", required=True)
    waiver.add_argument("--mitigation", required=True)
    waiver.add_argument("--expiry", required=True)
    waiver.add_argument("--root", type=Path)
    waiver.set_defaults(handler=waiver_create)

    attest = commands.add_parser("attest")
    attest.add_argument("rule_id")
    attest.add_argument("--id", required=True)
    attest.add_argument("--decision", required=True)
    attest.add_argument("--owner", required=True)
    attest.add_argument("--performed-at", required=True)
    attest.add_argument("--artifact", action="append", default=[])
    attest.add_argument("--limitations", required=True)
    attest.add_argument("--expiry", required=True)
    attest.add_argument("--root", type=Path)
    attest.set_defaults(handler=attestation_create)

    metric = commands.add_parser("metric")
    metric_commands = metric.add_subparsers(dest="metric_command", required=True)
    metric_validate_parser = metric_commands.add_parser("validate")
    metric_validate_parser.add_argument("--root", type=Path)
    metric_validate_parser.set_defaults(handler=metric_validate)
    metric_propose_parser = metric_commands.add_parser("propose")
    metric_propose_parser.add_argument("metric")
    metric_propose_parser.add_argument("--id", required=True)
    metric_propose_parser.add_argument("--threshold", type=float, required=True)
    metric_propose_parser.add_argument("--owner", required=True)
    metric_propose_parser.add_argument("--rationale", required=True)
    metric_propose_parser.add_argument("--observation", action="append", default=[])
    metric_propose_parser.add_argument("--root", type=Path)
    metric_propose_parser.set_defaults(handler=metric_propose)
    metric_apply_parser = metric_commands.add_parser("apply")
    metric_apply_parser.add_argument("id")
    metric_apply_parser.add_argument("--approved-by", required=True)
    metric_apply_parser.add_argument("--root", type=Path)
    metric_apply_parser.set_defaults(handler=metric_apply)

    quarantine = commands.add_parser("quarantine")
    quarantine_commands = quarantine.add_subparsers(dest="quarantine_command", required=True)
    quarantine_add_parser = quarantine_commands.add_parser("add")
    quarantine_add_parser.add_argument("nodeid")
    quarantine_add_parser.add_argument("--owner", required=True)
    quarantine_add_parser.add_argument("--rationale", required=True)
    quarantine_add_parser.add_argument("--expiry", required=True)
    quarantine_add_parser.add_argument("--root", type=Path)
    quarantine_add_parser.set_defaults(handler=quarantine_add)

    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
    ) as error:
        print(f"testpolicy error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
