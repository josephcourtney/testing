#!/usr/bin/env python
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def command(executable: str, exclusions: Path) -> list[str]:
    return [
        executable,
        "--no-update",
        "--fail",
        "--fail-on-scan-errors",
        "filesystem",
        ".",
        "--exclude-paths",
        str(exclusions),
    ]


def describe_failure(returncode: int) -> str | None:
    if returncode == 0:
        return None
    if returncode == 183:
        return "repository secrets were detected"
    return f"scanner setup or execution failed with exit code {returncode}"


def main() -> int:
    executable = shutil.which("trufflehog")
    if executable is None:
        print("[sec-secrets] ERROR: trufflehog not found on PATH", file=sys.stderr)
        return 1
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as exclusions:
        exclusions.write(
            "^\\.venv/\n^build/\n^dist/\n^\\.cache/\n"
            "^references/pulsecode/nan/.*/fid$\n"
            "^references/pulsecode/nan/.*\\.zip$\n"
        )
        exclusions.flush()
        result = subprocess.run(command(executable, Path(exclusions.name)), check=False)
    failure = describe_failure(result.returncode)
    if failure is not None:
        print(f"[sec-secrets] ERROR: {failure}", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
