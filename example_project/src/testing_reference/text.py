"""Small deterministic behavior for unit and property examples."""


def normalize_key(value: str) -> str:
    """Return a lowercase, single-space key."""
    return " ".join(value.casefold().split())
