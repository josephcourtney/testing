"""Component evidence for policy resolution and governed exceptions."""

from __future__ import annotations

import json
import shutil
from datetime import date, timedelta
from pathlib import Path

import pytest

from testing_policy.change_impact import impacted_claims
from testing_policy.cli import main
from testing_policy.execution import command_for
from testing_policy.io import load_state
from testing_policy.resolver import resolve, validate_metrics
from testing_policy.validation import validate_state

PROJECT_ROOT = Path(__file__).parents[2]


def copy_policy_project(tmp_path: Path) -> Path:
    shutil.copytree(PROJECT_ROOT / ".testing", tmp_path / ".testing")
    shutil.copy(PROJECT_ROOT / "metric-specifications.json", tmp_path)
    shutil.copy(PROJECT_ROOT / "quarantine.json", tmp_path)
    return tmp_path


@pytest.mark.component
@pytest.mark.requirement("policy-resolution")
def test_merge_plan_resolves_core_and_profile_obligations() -> None:
    obligations = {item.id: item for item in resolve(PROJECT_ROOT, "merge")}
    assert {
        "CORE-PROFILE-001",
        "CORE-TRUSTED-001",
        "CORE-QUARANTINE-001",
        "PROJECT-DOCS-001",
        "T11-METRICS-001",
    } <= obligations.keys()
    assert "P4-ARTIFACT-001" not in obligations


@pytest.mark.component
def test_release_plan_adds_production_evidence() -> None:
    rule_ids = {item.id for item in resolve(PROJECT_ROOT, "release")}
    assert {
        "P4-ARTIFACT-001",
        "P4-PERFORMANCE-001",
        "P4-RELEASE-001",
    } <= rule_ids


@pytest.mark.component
def test_unknown_decision_context_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported decision context"):
        resolve(PROJECT_ROOT, "relesae")


@pytest.mark.component
def test_policy_commands_use_a_closed_tool_interface() -> None:
    with pytest.raises(ValueError, match="unsupported tool"):
        command_for(
            {
                "commands": {
                    "unsafe": {
                        "tool": "shell",
                        "binary": "sh",
                        "arguments": ["-c"],
                        "additional_arguments": ["arbitrary input"],
                        "timeout_seconds": 10,
                    }
                }
            },
            "unsafe",
        )


@pytest.mark.component
def test_change_impact_maps_paths_to_declared_claims() -> None:
    architecture = load_state(PROJECT_ROOT)["architecture"]
    claims, reasons = impacted_claims(architecture, ["src/testing_reference/cli.py"])
    assert claims == {"INSTALLED-CLI-001", "CLI-LATENCY-001"}
    assert "INSTALLED-CLI-001" in reasons


@pytest.mark.component
def test_owned_unexpired_waiver_is_visible_in_resolution(tmp_path: Path) -> None:
    root = copy_policy_project(tmp_path)
    expiry = date.today() + timedelta(days=30)
    waiver = {
        "version": 1,
        "id": "WAIVER-WHEEL-001",
        "rule_id": "P4-ARTIFACT-001",
        "status": "active",
        "owner": "release owner",
        "rationale": "External build service is temporarily unavailable.",
        "mitigation": "Reproduce the wheel check manually before publication.",
        "expiry": expiry.isoformat(),
    }
    (root / ".testing" / "waivers" / "WAIVER-WHEEL-001.json").write_text(
        json.dumps(waiver),
        encoding="utf-8",
    )
    obligations = {item.id: item for item in resolve(root, "release")}
    assert obligations["P4-ARTIFACT-001"].status == "waived"
    assert not obligations["P4-ARTIFACT-001"].blocking


@pytest.mark.component
def test_expired_waiver_does_not_satisfy_obligation(tmp_path: Path) -> None:
    root = copy_policy_project(tmp_path)
    waiver = {
        "version": 1,
        "id": "WAIVER-WHEEL-OLD",
        "rule_id": "P4-ARTIFACT-001",
        "status": "active",
        "owner": "release owner",
        "rationale": "Historical exception.",
        "mitigation": "No longer applicable.",
        "expiry": (date.today() - timedelta(days=1)).isoformat(),
    }
    (root / ".testing" / "waivers" / "WAIVER-WHEEL-OLD.json").write_text(
        json.dumps(waiver),
        encoding="utf-8",
    )
    obligations = {item.id: item for item in resolve(root, "release")}
    assert obligations["P4-ARTIFACT-001"].status == "missing"
    assert obligations["P4-ARTIFACT-001"].blocking


@pytest.mark.component
def test_profile_change_is_applied_through_an_accepted_decision(tmp_path: Path) -> None:
    root = copy_policy_project(tmp_path)
    result = main(
        [
            "profile",
            "apply",
            "stabilization",
            "--decision-id",
            "PROFILE-STABILIZATION-001",
            "--approved-by",
            "test approver",
            "--rationale",
            "Exercise the governed transition.",
            "--root",
            str(root),
        ]
    )
    assert result == 0
    profile = load_state(root)["project"]
    assert profile["profiles"]["active"] == ["stabilization"]
    obligation = next(item for item in resolve(root, "merge") if item.id == "CORE-PROFILE-001")
    assert obligation.status == "satisfied"


@pytest.mark.component
def test_metric_threshold_change_retains_its_decision(tmp_path: Path) -> None:
    root = copy_policy_project(tmp_path)
    assert (
        main(
            [
                "metric",
                "propose",
                "cli-latency",
                "--id",
                "METRIC-CLI-LATENCY-002",
                "--threshold",
                "0.75",
                "--owner",
                "metric owner",
                "--rationale",
                "Exercise threshold governance.",
                "--root",
                str(root),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "metric",
                "apply",
                "METRIC-CLI-LATENCY-002",
                "--approved-by",
                "test approver",
                "--root",
                str(root),
            ]
        )
        == 0
    )
    assert validate_metrics(root, {"path": "metric-specifications.json"})[0] == "satisfied"


@pytest.mark.component
def test_repository_policy_state_and_guidance_anchors_are_valid() -> None:
    assert validate_state(PROJECT_ROOT) == []
