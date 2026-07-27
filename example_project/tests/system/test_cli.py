"""System evidence for the assembled command boundary."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.system
@pytest.mark.smoke
@pytest.mark.process
@pytest.mark.requirement("installed-cli")
def test_cli_emits_normalized_registry() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "testing_reference.cli", "  Alpha ", "BETA"],
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(Path.cwd() / "src")},
        text=True,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout) == {"alpha": "Alpha", "beta": "BETA"}
