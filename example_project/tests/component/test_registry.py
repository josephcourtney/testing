"""Component evidence for the in-process registry."""

import pytest

from testing_reference import Registry


@pytest.mark.component
@pytest.mark.requirement("registry")
def test_registry_normalizes_keys_and_preserves_display_values() -> None:
    registry = Registry()
    registry.add("  Alpha Value ")
    assert registry.get("ALPHA   VALUE") == "Alpha Value"
    assert registry.as_dict() == {"alpha value": "Alpha Value"}


@pytest.mark.component
@pytest.mark.regression
def test_registry_rejects_empty_values() -> None:
    registry = Registry()
    with pytest.raises(ValueError, match="non-whitespace"):
        registry.add(" \t ")
