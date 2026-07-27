"""Unit evidence for normalization."""

import pytest

from testing_reference import normalize_key


@pytest.mark.unit
@pytest.mark.requirement("normalization")
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  Mixed CASE  ", "mixed case"),
        ("two\twords", "two words"),
        ("Straße", "strasse"),
    ],
)
def test_normalize_key(value: str, expected: str) -> None:
    assert normalize_key(value) == expected


@pytest.mark.unit
@pytest.mark.quarantined
def test_unicode_normalization_future_obligation() -> None:
    """Illustrate an owned quarantine entry without contributing trusted evidence."""
    assert normalize_key(" café ") == "café"
