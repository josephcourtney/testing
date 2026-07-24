from pathlib import Path

python_path = Path('python_testing.md')
overview_path = Path('Overview.md')

python_text = python_path.read_text()
for heading in (
    '## 3. Directory layout',
    '## 4. Pytest configuration policy',
    '## 5. Command-line entrypoints',
    '## 15. Fixtures and test data',
):
    python_text = python_text.replace(f'{heading}\n\n{heading}\n', f'{heading}\n')
python_path.write_text(python_text)

overview = overview_path.read_text()
replacements = {
    'Move this section intact to Python/pytest implementation guidance or project-specific examples.\nDirectory organization is a selectable convention, not core testing policy. Retain several viable layouts and their tradeoffs rather than prescribing one universal tree.':
        'This section has moved intact to `python_testing.md`.\nDirectory organization remains a selectable convention, not core testing policy; the extracted material should retain viable layouts and their tradeoffs rather than prescribe one universal tree.',
    'Move the pytest and coverage configuration examples to Python/pytest implementation guidance.\nRetain in Overview.md only tool-independent evidence-integrity requirements such as rejecting unknown configuration and distinguishing complete from partial evidence.':
        'The pytest and coverage configuration material has moved intact to `python_testing.md`.\nOverview.md now retains only the surrounding tool-independent policy and review direction.',
    'Move command names, Make/just examples, pytest selections, and concrete cadence budgets to Python/pytest implementation guidance or project-specific examples.\nRetain in Overview.md only the general requirement for reproducible named evidence-producing commands and clearly distinguished complete versus partial runs.':
        'Command names, Make/just examples, pytest selections, and concrete cadence budgets have moved intact to `python_testing.md`.\nA later policy edit should retain here only the general requirement for reproducible named evidence-producing commands and clearly distinguished complete versus partial runs.',
    'Move fixture APIs, `tests/data` conventions, and Python factory examples to Python/pytest implementation guidance.\nRetain only tool-independent principles about representative, minimal, comprehensible test data.':
        'Fixture APIs, `tests/data` conventions, and Python factory examples have moved intact to `python_testing.md`.\nA later policy edit should retain here only tool-independent principles about representative, minimal, comprehensible test data.',
}
for old, new in replacements.items():
    overview = overview.replace(old, new)
overview_path.write_text(overview)
