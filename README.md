# Testing

These files are part encyclopedia, part specification, and part best practices
based on my current thinking. Do not take the non-normative material as gospel;
if you think it is wrong, challenge it.

The repository now makes the roles and precedence of the different documents
explicit so that explanatory material and project examples cannot silently
become universal policy.

## Document hierarchy

1. **`Overview.md` — normative policy.** Defines repository-wide requirements,
   evidence principles, and precedence.
2. **`glossary.md` — canonical terminology.** Defines the meanings used by the
   policy and procedures.
3. **`L1.md` — assessment and routing procedure.** Starts from the decision,
   claims, failure modes, architecture, and residual uncertainty.
4. **`L2_*.md` — lifecycle confidence profiles.** Adjust confidence, fidelity,
   breadth, cadence, enforcement, ownership, and recordkeeping without deciding
   whether an already-material risk applies.
5. **`L3_*.md` — evidence procedures.** Define how to design, collect, evaluate,
   and record particular scopes, purposes, techniques, and evidence forms.
6. **`automated_testing.md` — non-normative conceptual reference.** Discusses
   common practices, terminology, alternatives, and tradeoffs.
7. **`python_testing.md` — non-normative Python and pytest guidance.** Shows one
   coherent implementation of the general framework.
8. **`example_project/` — runnable reference implementation.** Demonstrates the
   classification, evidence-integrity, artifact, metric, and release contracts.
9. **`case_study/` — dated historical assessment.** Preserves concrete findings
   from a separate project without presenting them as current or reproducible
   from the reference implementation.

When documents conflict, `Overview.md` controls, followed by the applicable L1,
L2, or L3 procedure. The glossary controls terminology unless a normative
document explicitly defines a narrower requirement.

## Using the repository

Begin with `Overview.md`, then apply `L1.md` to the decision at hand. Use the
relevant lifecycle profile and only those L3 procedures needed by the identified
claims, risks, and boundaries.

Use `example_project/local-testing.md` to run the reference implementation. Its
package names, tools, marker inventory, support matrix, and numeric latency
budget are deliberately project-specific. `case_study/` is background evidence,
not another source of policy.
