# Testing

This repository separates testing policy, procedures, reference material, and project-specific examples.

## Document hierarchy

1. **`Overview.md`** — normative policy. It defines the required risk-and-evidence model and the dimensions used to classify tests.
2. **`L1.md`** — top-level assessment procedure. It selects evidence from risks, claims, system boundaries, and release context.
3. **`L2_*.md`** — lifecycle profiles. They change the required confidence and enforcement level; they do not prescribe a fixed sequence of test types.
4. **`L3_*.md`** — procedures for designing and evaluating particular forms of evidence.
5. **`automated_testing.md`** — non-normative encyclopedia of terms, techniques, tradeoffs, and common conventions.
6. **Project-specific guides and assessments** — examples of applying the policy to a particular project. They are not universal defaults.

Normative language appears only in policy and procedure documents. In those documents, **must** indicates a requirement and **should** indicates a strong recommendation that may be overridden with a documented reason.

The repository intentionally does not define one universal test pyramid, development workflow, directory layout, coverage percentage, mutation score, or CI cadence. Projects select those conventions according to their risks and operating constraints.
