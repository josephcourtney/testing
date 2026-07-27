"""A coherent in-process component for the reference tests."""

from dataclasses import dataclass, field

from testing_reference.text import normalize_key


@dataclass
class Registry:
    """Store display values under normalized keys."""

    _values: dict[str, str] = field(default_factory=dict)

    def add(self, value: str) -> None:
        key = normalize_key(value)
        if not key:
            raise ValueError("value must contain a non-whitespace character")
        self._values[key] = value.strip()

    def get(self, key: str) -> str:
        return self._values[normalize_key(key)]

    def as_dict(self) -> dict[str, str]:
        return dict(sorted(self._values.items()))
