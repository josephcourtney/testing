"""System evidence for the installed testing-policy command interface."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[2]


def invoke(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "testing_policy.cli", *arguments],
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
        text=True,
    )


@pytest.mark.system
@pytest.mark.process
def test_policy_plan_is_machine_readable() -> None:
    result = invoke("plan", "--root", str(PROJECT_ROOT), "--decision", "merge", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["decision"] in {"pass", "fail"}
    assert any(item["id"] == "CORE-PROFILE-001" for item in payload["obligations"])


@pytest.mark.system
@pytest.mark.process
def test_policy_explain_surfaces_the_canonical_guidance_section() -> None:
    result = invoke(
        "explain",
        "CORE-TRUSTED-001",
        "--root",
        str(PROJECT_ROOT),
        "--decision",
        "merge",
    )
    assert result.returncode == 0
    assert "Overview.md -> Tooling and execution integrity" in result.stdout
    assert "## 8. Tooling and execution integrity" in result.stdout
