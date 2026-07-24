# Testing

This repository separates testing policy, definitions, procedures, reference material, implementation guidance, and project-specific examples.

## Document hierarchy

1. **`Overview.md`** — normative policy. It defines the required risk-and-evidence model and the dimensions used to classify tests.
2. **`glossary.md`** — canonical terminology. It defines the meanings used by the policy and procedures without imposing a language or tool.
3. **`L1.md`** — top-level assessment procedure. It selects evidence from risks, claims, system boundaries, and release context.
4. **`L2_*.md`** — lifecycle profiles. They change the required confidence and enforcement level; they do not prescribe a fixed sequence of test types.
5. **`L3_*.md`** — procedures for designing and evaluating particular forms of evidence.
6. **`automated_testing.md`** — non-normative encyclopedia of concepts, techniques, tradeoffs, and common conventions. It explains terminology but is not the canonical glossary.
7. **`python_testing.md`** — non-normative Python and pytest implementation guidance, including markers, configuration, fixtures, isolation, packaging, static analysis, and examples.
8. **`examples/`** — project-specific guides, harnesses, thresholds, and assessments. These are applications of the policy, not universal defaults.

When terminology is unclear, consult `glossary.md`; when a detailed evidence procedure is needed, consult the corresponding `L3_*.md`; when implementing the model in Python, consult `python_testing.md`.

Normative language appears only in policy and procedure documents. In those documents, **must** indicates a requirement and **should** indicates a strong recommendation that may be overridden with a documented reason.

The repository intentionally does not define one universal test pyramid, development workflow, directory layout, coverage percentage, mutation score, or CI cadence. Projects select those conventions according to their risks and operating constraints.
