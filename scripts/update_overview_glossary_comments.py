from pathlib import Path

path = Path("Overview.md")
text = path.read_text()

replacements = {
    "- Retain the detailed material, but annotate sections by authority: normative policy, definition, recommended default, example, or project-specific convention.": "- Retain the detailed material, but annotate sections by authority: normative policy, definition, recommended default, example, or project-specific convention. Definitions have now been copied into `glossary.md`; remove the duplicated definitions from this file only after separate review.",
    "Move detailed definitions of unit, component, integration, system, contract, purposes, techniques, and resource markers to the terminology/reference material.": "Definitions of unit, component, integration, system, contract, purposes, techniques, and resource markers have been extracted into `glossary.md`. Remove the duplicated definitions from this section only after separate review.",
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"expected text not found: {old}")
    text = text.replace(old, new, 1)

heading_notes = {
    "## 7. Unit tests": "Definition status: the unit-test and dependency-injection terminology has been extracted into `glossary.md`; this section still contains the original text pending separate removal or relocation.",
    "## 8. Component tests": "Definition status: the component-test definition has been extracted into `glossary.md`; this section still contains the original text pending separate removal or relocation.",
    "## 9. Integration tests": "Definition status: the integration-test definition has been extracted into `glossary.md`; this section still contains the original text pending separate removal or relocation.",
    "## 10. System tests": "Definition status: the system-test definition has been extracted into `glossary.md`; this section still contains the original text pending separate removal or relocation.",
    "## 11. Contract tests": "Definition status: the contract-test definition has been extracted into `glossary.md`; this section still contains the original text pending separate removal or relocation.",
    "## 13. Property-based testing": "Definition status: the property-based-testing definition has been extracted into `glossary.md`; this section still contains the original policy, guidance, and example pending separate relocation.",
    "## 14. Observability tests": "Definition status: the observability-test definition has been extracted into `glossary.md`; this section still contains the original policy, guidance, and example pending separate relocation.",
    "## 15. Fixtures and test data": "Definition status: fixture terminology has been extracted into `glossary.md`; this section still contains the original guidance and example pending separate relocation.",
    "## 16. Advanced testing techniques": "Definition status: mutation testing, fuzz testing, chaos testing, and snapshot testing have been extracted into `glossary.md`; this section still contains the original guidance pending separate relocation.",
    "## 18. Metrics and targets": "Definition status: line coverage, branch coverage, mutation score, flake rate, and performance regression have been extracted into `glossary.md`; this section still contains the original targets pending separate review.",
}

for heading, note in heading_notes.items():
    pos = text.find(heading)
    if pos < 0:
        raise SystemExit(f"heading not found: {heading}")
    comment_start = text.rfind("<!--", 0, pos)
    comment_end = text.find("-->", comment_start, pos)
    if comment_start < 0 or comment_end < 0:
        raise SystemExit(f"review comment not found before: {heading}")
    block = text[comment_start:comment_end]
    if note in block:
        continue
    insert_at = comment_end
    text = text[:insert_at] + note + "\n" + text[insert_at:]

path.write_text(text)
