"""Installed command-line boundary for the reference project."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from testing_reference.registry import Registry


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="testing-reference")
    root.add_argument("values", nargs="*", help="values to normalize and retain")
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    registry = Registry()
    try:
        for value in args.values:
            registry.add(value)
    except ValueError as error:
        parser().error(str(error))
    print(json.dumps(registry.as_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
