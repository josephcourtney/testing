"""Enforce the reference project's test-classification contract."""

from __future__ import annotations

from collections.abc import Iterable

import pytest

STRUCTURAL_SCOPES = ("unit", "component", "integration", "system")
PURPOSES = ("acceptance", "regression", "contract", "smoke", "compatibility")
TECHNIQUES = ("property_based", "fuzz")


def marker_names(item: pytest.Item, names: Iterable[str]) -> list[str]:
    return [name for name in names if item.get_closest_marker(name) is not None]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    violations: list[str] = []
    for item in items:
        scopes = marker_names(item, STRUCTURAL_SCOPES)
        if len(scopes) != 1:
            violations.append(
                f"{item.nodeid}: expected exactly one structural scope, found {scopes or 'none'}"
            )
            continue
        item.user_properties.append(("structural_scope", scopes[0]))
        for purpose in marker_names(item, PURPOSES):
            item.user_properties.append(("purpose", purpose))
        for technique in marker_names(item, TECHNIQUES):
            item.user_properties.append(("technique", technique))
        if item.get_closest_marker("quarantined") is not None:
            item.user_properties.append(("quarantined", True))
        for marker in item.iter_markers("requirement"):
            if len(marker.args) != 1 or not isinstance(marker.args[0], str):
                violations.append(f"{item.nodeid}: requirement marker needs one string argument")
            else:
                item.user_properties.append(("requirement", marker.args[0]))
    if violations:
        raise pytest.UsageError("\n".join(violations))
