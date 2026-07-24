from pathlib import Path
import re

OVERVIEW = Path('Overview.md')
PYTHON = Path('python_testing.md')
text = OVERVIEW.read_text()

moved = []


def replace_section(number: int, title: str, destination_title: str | None = None) -> None:
    global text
    pattern = re.compile(
        rf'(?ms)^## {number}\. {re.escape(title)}\n.*?^---\n'
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f'missing section {number}: {title}')
    block = match.group(0).removesuffix('---\n').rstrip()
    moved.append((destination_title or f'{number}. {title}', block))
    replacement = (
        '<!--\n'
        'PYTHON-SPECIFIC CONTENT EXTRACTED\n\n'
        f'This section moved intact to `python_testing.md` under "{destination_title or title}".\n'
        'The move separates Python/pytest implementation guidance from the general testing policy.\n'
        '-->\n\n'
        '---\n'
    )
    text = text[:match.start()] + replacement + text[match.end():]


# Entirely Python/pytest implementation-oriented sections.
replace_section(3, 'Directory layout')
replace_section(4, 'Pytest configuration policy')
replace_section(5, 'Command-line entrypoints')
replace_section(15, 'Fixtures and test data')

# Move the pytest marker configuration example, but retain the general taxonomy and marker policy.
marker_pattern = re.compile(
    r'(?ms)^Example `pytest` marker configuration \(in `pyproject\.toml` or `pytest\.ini`\):\n\n```toml\n.*?^```\n'
)
match = marker_pattern.search(text)
if not match:
    raise RuntimeError('missing pytest marker example')
moved.append(('Pytest marker configuration', match.group(0).rstrip()))
text = text[:match.start()] + (
    '<!-- PYTHON-SPECIFIC EXAMPLE EXTRACTED: the pytest marker configuration moved to '
    '`python_testing.md`; the taxonomy and marker policy remain here. -->\n'
) + text[match.end():]

# Move Python code examples from otherwise general sections, leaving all surrounding prose unchanged.
code_pattern = re.compile(r'(?ms)^```python\n.*?^```\n')
examples = []
for idx, match in enumerate(list(code_pattern.finditer(text)), start=1):
    examples.append((f'Python example {idx}', match.group(0).rstrip()))

# Replace from the end so offsets remain valid.
for idx, match in reversed(list(enumerate(list(code_pattern.finditer(text)), start=1))):
    replacement = (
        '<!-- PYTHON-SPECIFIC EXAMPLE EXTRACTED: this code block moved to '
        f'`python_testing.md` under "Python example {idx}". -->\n'
    )
    text = text[:match.start()] + replacement + text[match.end():]
moved.extend(examples)

# Move the Python-tool-specific metric-evaluation subsection while retaining the surrounding
# advanced-technique policy.
metric_pattern = re.compile(
    r'(?ms)^### 16\.2 Coverage, mutation, and property test quality\n.*?(?=^### 16\.3 )'
)
match = metric_pattern.search(text)
if not match:
    raise RuntimeError('missing section 16.2')
moved.append(('Coverage, mutation, and property-test tooling', match.group(0).rstrip()))
text = text[:match.start()] + (
    '<!--\n'
    'PYTHON-SPECIFIC CONTENT EXTRACTED\n\n'
    'The pytest/Mutmut/Hypothesis evaluation procedure formerly in section 16.2 moved to '
    '`python_testing.md`. General metric policy remains in section 18.\n'
    '-->\n\n'
) + text[match.end():]

# Update the section-review comments whose proposed destinations are now concrete.
text = text.replace(
    'Move the pytest marker configuration example to Python/pytest implementation guidance.',
    'The pytest marker configuration example has moved to `python_testing.md`.'
)
text = text.replace(
    'Move this section to a Python/pytest implementation guide. Directory organization is a selectable project convention rather than general testing policy.',
    'This section has moved intact to `python_testing.md`; directory organization remains a selectable project convention rather than general testing policy.'
)
text = text.replace(
    'Move this entire section to Python/pytest implementation guidance. Retain strict-marker, strict-config, warning, xfail, and coverage settings as recommended defaults rather than universal cross-language policy.',
    'This entire section has moved to `python_testing.md`. Its strict-marker, strict-config, warning, xfail, and coverage settings remain Python/pytest defaults rather than cross-language policy.'
)
text = text.replace(
    'Move command names, Make examples, pytest selections, and fixed cadence tables to project-specific or Python implementation guidance.',
    'Command names, Make examples, pytest selections, and cadence tables have moved to `python_testing.md`.'
)
text = text.replace(
    'Move fixture APIs, `tests/data` conventions, and Python factory examples to Python/pytest implementation guidance.',
    'Fixture APIs, `tests/data` conventions, and Python factory examples have moved to `python_testing.md`.'
)

header = '''# Python Testing Implementation Guidance

This file contains Python-, pytest-, and Python-tool-specific material extracted verbatim from `Overview.md`.
The extraction is organizational only: the moved material has not been substantively rewritten or normalized.
General policy and non-Python guidance remain in `Overview.md`.

'''
parts = [header]
for title, block in moved:
    parts.append(f'## {title}\n\n{block}\n\n---\n\n')

OVERVIEW.write_text(text)
PYTHON.write_text(''.join(parts).rstrip() + '\n')
