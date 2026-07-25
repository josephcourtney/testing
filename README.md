# Testing Guidance

This repository defines a risk-driven framework for selecting, producing, and evaluating software-testing evidence.

## Document hierarchy

1. **`Overview.md` — normative policy.** Defines repository-wide requirements and precedence.
2. **`glossary.md` — canonical terminology.** Defines terms used by the policy and procedures.
3. **`L1.md` — assessment and routing procedure.** Starts from a decision, claims, failure modes, and residual uncertainty.
4. **`L2_*.md` — lifecycle confidence profiles.** Adjust confidence, fidelity, cadence, and governance expectations without deciding which material risks apply.
5. **`L3_*.md` — evidence procedures.** Define how to design, collect, evaluate, and record particular forms of evidence.
6. **`automated_testing.md` — non-normative conceptual reference.**
7. **`python_testing.md` — non-normative Python and pytest implementation guidance.**
8. **`examples/` — project-specific or illustrative implementations and assessments.**

When documents conflict, `Overview.md` controls, followed by the applicable L1, L2, or L3 procedure. The glossary controls terminology unless a normative document explicitly defines a narrower requirement.

## Using the repository

Begin with `Overview.md`, then apply `L1.md` to the decision at hand. Use the relevant lifecycle profile and only those L3 procedures needed by the identified claims, risks, and boundaries.

Projects should copy or adapt implementation examples rather than treating commands, markers, thresholds, directory layouts, or tool choices as universal requirements.
