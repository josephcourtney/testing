#!/usr/bin/env python
"""Install the built wheel in isolation and retain artifact evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(command, cwd=cwd, env=env, check=False)
    if result.returncode:
        raise RuntimeError(f"command failed with status {result.returncode}: {' '.join(command)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    wheels = sorted((root / "dist").glob("*.whl"))
    if len(wheels) != 1:
        print("expected exactly one wheel in dist", file=sys.stderr)
        return 2
    wheel = wheels[0]
    try:
        with tempfile.TemporaryDirectory(prefix="testing-reference-wheel-") as directory:
            sandbox = Path(directory)
            environment = sandbox / "venv"
            run(
                [
                    "uv",
                    "venv",
                    "--no-project",
                    "--python",
                    sys.executable,
                    str(environment),
                ],
                cwd=sandbox,
            )
            python = environment / "bin" / "python"
            command = environment / "bin" / "testing-reference"
            policy_command = environment / "bin" / "testpolicy"
            clean_env = dict(os.environ)
            clean_env.pop("PYTHONPATH", None)
            run(
                [
                    "uv",
                    "pip",
                    "install",
                    "--python",
                    str(python),
                    "--no-deps",
                    str(wheel),
                ],
                cwd=sandbox,
                env=clean_env,
            )
            run(
                [
                    str(python),
                    "-c",
                    (
                        "from importlib.resources import files; "
                        "import testing_policy, testing_reference; "
                        "assert files('testing_policy').joinpath("
                        "'rules/catalog.json').is_file()"
                    ),
                ],
                cwd=sandbox,
                env=clean_env,
            )
            run([str(command), " Alpha ", "BETA"], cwd=sandbox, env=clean_env)
            run([str(policy_command), "--help"], cwd=sandbox, env=clean_env)
    except (OSError, RuntimeError) as error:
        print(f"wheel validation failed: {error}", file=sys.stderr)
        return 1
    payload = {
        "version": 1,
        "kind": "testing-reference-wheel-evidence",
        "decision": "pass",
        "artifact": wheel.name,
        "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "os": platform.system(),
        "architecture": platform.machine(),
    }
    output = root / ".cache" / "evidence" / "wheel.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
