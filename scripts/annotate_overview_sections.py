from pathlib import Path

path = Path("Overview.md")
text = path.read_text()

comments = {
    "## 2. Test taxonomy": """<!--
SECTION REVIEW — SPLIT AND MOVE MOST CONTENT

Keep in Overview.md only a concise normative statement that tests are classified along independent dimensions.
Move detailed definitions of unit, component, integration, system, contract, purposes, techniques, and resource markers to the terminology/reference material.
Move the pytest marker configuration example to Python/pytest implementation guidance.
Remove the rule that `contract` is an alternative structural scope; contract should be an independently composable purpose.
-->
""",
    "## 3. Directory layout": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move this section intact to Python/pytest implementation guidance or project-specific examples.
Directory organization is a selectable convention, not core testing policy. Retain several viable layouts and their tradeoffs rather than prescribing one universal tree.
-->
""",
    "## 4. Pytest configuration policy": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the pytest and coverage configuration examples to Python/pytest implementation guidance.
Retain in Overview.md only tool-independent evidence-integrity requirements such as rejecting unknown configuration and distinguishing complete from partial evidence.
-->
""",
    "## 5. Command-line entrypoints": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move command names, Make/just examples, pytest selections, and concrete cadence budgets to Python/pytest implementation guidance or project-specific examples.
Retain in Overview.md only the general requirement for reproducible named evidence-producing commands and clearly distinguished complete versus partial runs.
-->
""",
    "### 5.1 Recommended testing cadence": """<!--
SECTION REVIEW — MOVE; REMOVE UNIVERSAL CADENCE PRESCRIPTION

Move the table to implementation guidance as an illustrative workflow.
Remove the claim that this exact save/commit/PR/nightly progression should be preserved universally. Cadence should follow risk, cost, feedback needs, and available infrastructure.
-->
""",
    "## 6. Test design guidelines": """<!--
SECTION REVIEW — SPLIT

Keep the tool-independent behavioral and invariant-oriented principles in Overview.md.
Move Python examples, naming conventions, and Arrange–Act–Assert guidance to implementation/reference material, explicitly labeling them as useful conventions rather than universal requirements.
-->
""",
    "## 7. Unit tests": """<!--
SECTION REVIEW — MOVE DETAILED MATERIAL; KEEP ONLY POLICY SUMMARY

Move the definition, examples, collaborator strategy, dependency-injection guidance, and mocking/fake guidance to the unit-testing procedure and Python guide.
Keep a short policy statement that unit scope is a small chosen boundary providing localizing evidence.
Preserve dependency injection as a selective recommendation at external-effect and variability boundaries; do not remove it or require replacement of every collaborator.
Remove the universal ~100 ms threshold from core policy and retain it only as an illustrative project budget.
-->
""",
    "## 8. Component tests": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the definition, resource guidance, and Python example to the component-testing procedure and Python implementation guide.
Overview.md should name component scope only as one available evidence boundary.
-->
""",
    "## 9. Integration tests": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the detailed definition, infrastructure guidance, markers, and example to the integration-testing procedure and Python implementation guide.
Retain only the policy principle that real external semantics require evidence that executes those semantics.
-->
""",
    "## 10. System tests": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the definition, scenario list, marker advice, and subprocess example to the system-testing procedure and Python guide.
Do not equate system scope with acceptance purpose; acceptance evidence may exist at several structural scopes.
-->
""",
    "## 11. Contract tests": """<!--
SECTION REVIEW — MOVE AND EXPAND

Move the detailed material to the contract-testing procedure and Python guide.
Reclassify contract as a purpose that can be exercised at component, integration, or system scope.
Expand beyond schema shape to behavioral obligations, producer/consumer expectations, version compatibility, migrations, and allowed versus breaking changes.
-->
""",
    "## 12. Configuration and environment testing": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move the Python-specific environment-variable and module-reload examples to the Python guide.
Retain only the general policy that behavior varying by supported configuration or environment requires representative evidence.
-->
""",
    "## 13. Property-based testing": """<!--
SECTION REVIEW — MOVE AND EXPAND

Move the detailed guidance and Hypothesis example to the generative/property-testing procedure and Python guide.
Remove the implication that property-based testing primarily belongs to pure functions. Expand the reference material to stateful, model-based, differential, and metamorphic testing.
-->
""",
    "## 14. Observability tests": """<!--
SECTION REVIEW — MOVE AND SPLIT

Move Python `caplog` guidance and examples to the Python guide.
Move test-design guidance for logs, metrics, traces, and diagnostics to the non-functional/observability procedure.
Separate instrumentation-contract checks from operational evidence that alerts and diagnostics work under realistic failure conditions.
-->
""",
    "## 15. Fixtures and test data": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD

Move fixture, factory, test-data, and pytest examples to Python implementation guidance and the terminology/reference material.
These are maintainability techniques rather than top-level policy.
-->
""",
    "## 16. Advanced testing techniques": """<!--
SECTION REVIEW — MOVE OUT OF OVERVIEW.MD AND DISTRIBUTE

Distribute mutation testing, fuzzing, chaos/resilience testing, and snapshot testing to their corresponding procedures and reference sections.
Keep the detailed information; do not compress these techniques into a short list.
-->
""",
    "### 16.2 Coverage, mutation, and property test quality": """<!--
SECTION REVIEW — MOVE; REMOVE UNSUPPORTED UNIVERSAL TARGETS

Move metric interpretation to a dedicated metric-design procedure and project-specific examples.
Remove universal coverage and mutation targets unless their population, denominator, tool configuration, baseline, uncertainty, decision, and response are explicitly defined.
Retain the practical workflow for investigating uncovered code and surviving mutants as implementation guidance.
-->
""",
    "### 16.4 Chaos and resilience testing": """<!--
SECTION REVIEW — MOVE AND EXPAND

Move this material to a first-class operational/resilience procedure.
Expand it to deployment, rollback, restart, failover, backup restoration, recovery objectives, degraded modes, runbooks, and observability validation.
-->
""",
    "## 17. Static analysis and security checks": """<!--
SECTION REVIEW — SPLIT AND MOVE DETAILS

Move Python tool examples and command wiring to implementation guidance.
Keep tool-independent requirements for required static, security, and supply-chain evidence only where justified by project risk and support policy.
Replace the universal every-commit/every-PR cadence with explicit project-selected gates and documented waivers.
-->
""",
    "## 18. Metrics and targets": """<!--
SECTION REVIEW — MOVE; REMOVE UNIVERSAL NUMERIC TARGETS

Move metric definitions and examples to a dedicated metric-design procedure.
Remove the generic 80% line coverage, 70% branch coverage, 70% mutation, and ±5–10% performance recommendations as universal guidance.
Retain values only as clearly labeled examples after defining population, denominator, environment, baseline, uncertainty, threshold rationale, action, and owner.
-->
""",
    "## 19. Prohibited practices and anti-patterns": """<!--
SECTION REVIEW — SPLIT

Keep genuinely tool-independent evidence-integrity prohibitions in Overview.md, such as arbitrary sleeps, hidden failures, and unreviewed suppression.
Move scope-specific red flags to the relevant L3 procedures and Python-specific advice to the Python guide.
Remove the universal claim that lower-level tests must carry most of the load; portfolio shape should follow risks and architecture.
-->
""",
    "### 16.5 Snapshot tests (optional)": """<!--
SECTION REVIEW — REMOVE THIS DUPLICATE SECTION

This is a duplicate of section 16.5 above and follows stray Markdown fences. Remove the duplicate and malformed fences after review; preserve the earlier complete snapshot-testing section and move it to the snapshot procedure/reference material.
-->
""",
}

for heading, comment in comments.items():
    marker = comment + heading
    if marker in text:
        continue
    count = text.count(heading)
    if heading == "### 16.5 Snapshot tests (optional)":
        # Annotate only the second, duplicated occurrence.
        first = text.find(heading)
        second = text.find(heading, first + len(heading))
        if second == -1:
            raise RuntimeError(f"duplicate heading not found: {heading}")
        text = text[:second] + comment + text[second:]
        continue
    if count != 1:
        raise RuntimeError(f"expected one occurrence of {heading!r}, found {count}")
    text = text.replace(heading, marker, 1)

path.write_text(text)
