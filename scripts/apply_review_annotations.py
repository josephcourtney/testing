from __future__ import annotations

from pathlib import Path

MARKER = "TESTING-GUIDANCE-REVIEW"

ANNOTATIONS: dict[str, tuple[list[str], list[str]]] = {
    "README.md": (
        [
            "The repository does not define which documents are normative, explanatory, procedural, or project-specific.",
            "The phrase 'part encyclopedia, part specification, part best practices' makes conflicts between documents difficult to resolve.",
        ],
        [
            "Add a document hierarchy and precedence rule without changing the existing documents' substantive content.",
            "Label examples and local harness material as project-specific rather than universal policy.",
        ],
    ),
    "Overview.md": (
        [
            "This document combines policy, terminology, Python/pytest configuration, examples, directory conventions, lifecycle cadence, and quantitative targets in one authority level.",
            "The taxonomy treats contract as comparable to structural scopes even though contract usually describes purpose; other purposes and techniques are also mixed with scope markers.",
            "Several recommendations are framed universally despite depending on project risk, architecture, environment, and feedback constraints.",
            "Fixed coverage, mutation, runtime, flake, and performance targets are not accompanied by explicit populations, denominators, baselines, uncertainty, or decision rules.",
            "Acceptance, exploratory, usability/accessibility, and operational/recovery evidence are underrepresented.",
        ],
        [
            "Retain the detailed material, but annotate sections by authority: normative policy, definition, recommended default, example, or project-specific convention.",
            "Describe tests with orthogonal dimensions: structural scope, purpose, technique, resources/boundaries, and execution cadence.",
            "Make risk and failure modes determine evidence applicability; use lifecycle only to adjust confidence, breadth, fidelity, and enforcement.",
            "Replace universal numeric gates with a metric-specification procedure while retaining example values as explicitly illustrative.",
            "Add dedicated guidance for acceptance, exploratory, usability/accessibility, and operational/resilience evidence.",
        ],
    ),
    "automated_testing.md": (
        [
            "The document alternates between encyclopedia, prescription, and lifecycle policy without stating which statements are normative.",
            "The lifecycle sequence can be read as making test applicability depend on phase rather than current risk.",
            "TDD, isolation style, portfolio shape, and test ordering are presented more universally than the evidence supports.",
            "Property-based testing is described too narrowly, especially for stateful systems, model-based testing, differential testing, and metamorphic relations.",
            "Quantitative targets are presented without a complete measurement design.",
        ],
        [
            "Mark the document as a non-normative reference while preserving its breadth and examples.",
            "Annotate lifecycle sections as common confidence patterns rather than required sequences.",
            "Present TDD, sociable/solitary units, mocking styles, and portfolio shapes as selectable conventions with tradeoffs.",
            "Expand generative testing guidance to state machines, models, differential oracles, and metamorphic properties.",
            "Require metric definitions, baselines, uncertainty, and actions before illustrative targets become gates.",
        ],
    ),
    "L1.md": (
        [
            "The top-level routing procedure is primarily lifecycle-driven and can defer already-material risks until a later phase.",
            "It does not begin by recording the decision, claims, failure modes, architecture boundaries, affected users, and residual uncertainty.",
            "The relationship between selected evidence and the specific failure modes it can detect is not explicit enough.",
        ],
        [
            "Add a risk-and-evidence assessment before lifecycle routing.",
            "Record the decision, claims, failure modes, consequences, uncertainty, boundaries, evidence, and limitations.",
            "Use lifecycle profiles to adjust required confidence and governance, not to determine whether a material risk applies.",
        ],
    ),
    "L2_P1_prototype.md": (
        [
            "The prototype profile can be read as permitting weak evidence solely because the project is early-stage.",
            "The result vocabulary and escalation conditions are less consistent than in later lifecycle procedures.",
        ],
        [
            "State that prototype work should minimize ceremony while still addressing any already-material security, data, safety, or external-impact risk.",
            "Use the same pass, conditional pass, fail, and exploratory-finding vocabulary as the other profiles.",
        ],
    ),
    "L2_P2_alpha.md": (
        [
            "The development profile prescribes a test inventory more directly than it connects evidence to changed responsibilities and failure modes.",
            "Workflow conventions such as TDD risk being interpreted as quality requirements rather than selectable development methods.",
        ],
        [
            "Describe default confidence goals for changed behavior, interfaces, and known acceptance conditions.",
            "Select scopes and techniques from risk and architecture; keep TDD and test-after workflows as justified team conventions.",
        ],
    ),
    "L2_P3_beta.md": (
        [
            "The stabilization profile treats named test classes as a mandatory inventory even when some classes do not correspond to actual boundaries or risks.",
            "User journeys, compatibility, exploratory learning, and usability evidence are not distinguished clearly enough.",
        ],
        [
            "Frame stabilization as reducing release uncertainty across critical boundaries, compatibility obligations, and user journeys.",
            "Require explicit omissions and residual risks instead of fictitious test categories.",
        ],
    ),
    "L2_P4_production.md": (
        [
            "Production readiness is expressed mainly as pre-release automated test coverage rather than a complete operational claim.",
            "Deployment, rollback, restoration, observability, capacity, incident response, accessibility, and human operation need first-class treatment where material.",
        ],
        [
            "Add production claims and evidence for operability, recovery, security, performance, data integrity, and supported user journeys.",
            "Make each category risk-applicable and record waivers, mitigations, owners, and revisit triggers.",
        ],
    ),
    "L2_P5_maintenance.md": (
        [
            "The maintenance profile does not fully emphasize change-impact analysis, incident-derived tests, contract revalidation, or decay of operational evidence.",
            "A fixed regression inventory may miss newly introduced risks while preserving obsolete checks.",
        ],
        [
            "Start from the changed claims, affected boundaries, incidents, dependency updates, and observed production behavior.",
            "Retire stale evidence and add focused regression, contract, migration, recovery, or monitoring evidence as risks evolve.",
        ],
    ),
    "L3_T1_unit.md": (
        [
            "The unit boundary is defined too narrowly around pure logic and can imply that a unit must be one function, method, or class.",
            "The isolation rules can be read as requiring replacement of all collaborators, which encourages deep mocking and interfaces created only for tests.",
            "Dependency injection is recommended appropriately, but its purpose and limits should be stated more precisely.",
        ],
        [
            "Define a unit as the smallest useful local behavioral boundary, which may be solitary or sociable.",
            "Retain inexpensive deterministic collaborators when they are part of the chosen boundary; replace collaborators when control, substitution, observability, or fault injection is needed.",
            "Continue recommending explicit dependency injection at external-effect and variability boundaries, but do not require artificial interfaces for every internal collaborator.",
            "Pair consequential doubles with contract or integration evidence.",
        ],
    ),
    "L3_T2_component.md": (
        [
            "The component definition depends heavily on examples of lightweight infrastructure rather than a precise supported subsystem boundary.",
            "The distinction between a sociable unit, component, and integration test can be ambiguous.",
        ],
        [
            "Define the component by a coherent supported interface and state which dependencies remain inside or outside the boundary.",
            "Classify tests by the semantics actually executed, not solely by process count or the use of SQLite, temporary files, or fakes.",
        ],
    ),
    "L3_T3_integration.md": (
        [
            "Integration is equated mainly with the presence of real external services, which can obscure protocol, framework, persistence, and platform semantics.",
            "The procedure needs stronger guidance on environment identity, data isolation, failure injection, and comparability.",
        ],
        [
            "Define integration evidence by reliance on real semantics across a boundary.",
            "Require explicit boundary, environment, version, isolation, cleanup, and diagnostic records.",
        ],
    ),
    "L3_T4_system.md": (
        [
            "System, smoke, end-to-end, and acceptance testing are treated as nearly interchangeable even though they describe different dimensions.",
            "A small smoke selection cannot establish all stakeholder acceptance conditions or system risks.",
        ],
        [
            "Keep system as structural scope, smoke as selection purpose, and acceptance as stakeholder-facing purpose.",
            "State which assembled artifact, environment, user/operator boundary, and critical journeys are exercised.",
        ],
    ),
    "L3_T5_regression.md": (
        [
            "Regression is at risk of being treated as a separate structural level rather than the reason a test exists.",
            "The procedure should distinguish incident-derived regressions, characterization tests, and broad regression suites.",
        ],
        [
            "Define regression as a purpose composable with any appropriate scope and technique.",
            "Require the protected behavior or failure mode to be recorded and remove obsolete regressions when the obligation no longer exists.",
        ],
    ),
    "L3_T6_property-based.md": (
        [
            "The procedure focuses on simple pure functions and discourages stateful subjects too strongly.",
            "It omits model-based state machines, command sequences, differential comparison, and metamorphic relations.",
            "Generator validity, shrinking quality, oracle strength, and runtime budgets need more explicit evaluation.",
        ],
        [
            "Retain the pure-function examples but expand the procedure to stateful, model-based, differential, and metamorphic testing.",
            "Require domain-valid generators, interpretable shrinking, meaningful oracles, and reproducible failing examples.",
        ],
    ),
    "L3_T7_contract.md": (
        [
            "Contract testing is centered on structural schema checks and is treated too much like a structural scope.",
            "Behavioral semantics, consumer expectations, provider verification, version matrices, migrations, and artifact compatibility are underdeveloped.",
        ],
        [
            "Define contract as a purpose that may be exercised at component, integration, or system scope.",
            "Identify producer, consumer, obligations, allowed changes, compatibility policy, and verification ownership.",
            "Cover behavioral, consumer-driven, provider, persistence/migration, public API, and artifact contracts where applicable.",
        ],
    ),
    "L3_T8_non-functional.md": (
        [
            "Performance, security, data quality, and observability are grouped together despite requiring different threats, workloads, environments, and oracles.",
            "Generic percentage tolerances and thresholds can be mistaken for valid gates without measurement design.",
            "Accessibility, privacy, capacity, resilience, and recovery are not fully represented.",
        ],
        [
            "Keep the broad overview but annotate each evidence type with its own claim, workload or threat model, environment, measurement method, and uncertainty.",
            "Move threshold design into an explicit metric procedure and retain numeric examples only as illustrations.",
            "Add or cross-reference dedicated accessibility/usability and operational/resilience procedures.",
        ],
    ),
    "L3_T9_snapshot.md": (
        [
            "Snapshot tests can approve large accidental changes and may obscure the actual behavioral oracle.",
            "The procedure needs stronger canonicalization, semantic review, ownership, and update rules.",
        ],
        [
            "Require stable canonical representations and precise assertions for critical semantics alongside snapshots.",
            "Treat snapshot updates as behavior changes requiring review rather than routine regeneration.",
        ],
    ),
    "L3_T10_health_and_metrics.md": (
        [
            "Suite health and quantitative release metrics are combined even though they answer different decisions.",
            "Coverage, mutation, flake, runtime, and performance values lack a shared specification of population, denominator, environment, window, uncertainty, and response.",
        ],
        [
            "Evaluate suite health through feedback latency, determinism, diagnostic quality, maintenance burden, and critical-risk coverage.",
            "Add a separate metric-design procedure before any numerical observation becomes a gate.",
        ],
    ),
    "current-assessment.md": (
        [
            "The assessment mixes observed facts, inferred confidence, policy compliance, and project-specific thresholds.",
            "Small numbers of repeated runs cannot support a precise flake probability without an explicit statistical model and interval.",
        ],
        [
            "Label each statement as observation, inference, assumption, or accepted risk.",
            "Define the run population and uncertainty before quantifying flake rate; otherwise report only that no flakes were observed in the sampled runs.",
            "Treat local thresholds as project evidence rather than repository-wide defaults.",
        ],
    ),
    "local-testing.md": (
        [
            "This project-specific harness can be mistaken for universal policy because commands, markers, cadence, and thresholds are stated prescriptively.",
            "The marker expression `unit or component or contract and not slow` is ambiguous to readers without explicit Boolean grouping.",
        ],
        [
            "Label the entire document as a local implementation of the general guidance.",
            "Use one structural scope plus independently composable purpose, technique, and resource markers.",
            "Add explicit parentheses to compound marker expressions and document which commands produce complete versus partial evidence.",
        ],
    ),
    "production-readiness.md": (
        [
            "The checklist can be interpreted as a universal fixed inventory rather than evidence selected from the product's actual claims and risks.",
            "Operational readiness needs explicit links to deployment, observability, rollback, restoration, ownership, and residual risk.",
        ],
        [
            "Retain the checklist as a prompt, but mark each item applicable, not applicable with rationale, satisfied, waived, or unresolved.",
            "Record evidence identity, environment, owner, waiver expiry, and recovery validation for material production claims.",
        ],
    ),
    "example_pyproject.toml": (
        [
            "This configuration is useful but may be read as the repository's universal pytest, coverage, warning, and marker policy.",
            "Tool versions, warning filters, coverage collection, and marker declarations must match the adopting project's package and evidence commands.",
        ],
        [
            "Label the file as an illustrative project configuration.",
            "Require adopters to replace package names, validate filters, separate partial from complete coverage runs, and define any numeric gate through an explicit metric specification.",
        ],
    ),
}


def markdown_comment(problems: list[str], fixes: list[str]) -> str:
    lines = [
        "<!--",
        f"{MARKER}: document-level annotation",
        "",
        "Problems identified:",
    ]
    lines.extend(f"- {item}" for item in problems)
    lines.extend(["", "Proposed fixes:"])
    lines.extend(f"- {item}" for item in fixes)
    lines.extend(
        [
            "",
            "Review rule: preserve the original document text. Apply any proposed fix only after explicit review.",
            "-->",
            "",
        ]
    )
    return "\n".join(lines)


def toml_comment(problems: list[str], fixes: list[str]) -> str:
    lines = [
        f"# {MARKER}: document-level annotation",
        "#",
        "# Problems identified:",
    ]
    lines.extend(f"# - {item}" for item in problems)
    lines.extend(["#", "# Proposed fixes:"])
    lines.extend(f"# - {item}" for item in fixes)
    lines.extend(
        [
            "#",
            "# Review rule: preserve the original configuration. Apply any proposed fix only after explicit review.",
            "",
        ]
    )
    return "\n".join(lines)


def insert_markdown_annotation(text: str, annotation: str) -> str:
    if MARKER in text:
        return text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            boundary = end + len("\n---\n")
            return text[:boundary] + "\n" + annotation + text[boundary:]
    return annotation + text


def main() -> None:
    missing: list[str] = []
    for filename, (problems, fixes) in ANNOTATIONS.items():
        path = Path(filename)
        if not path.exists():
            missing.append(filename)
            continue
        original = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            revised = insert_markdown_annotation(original, markdown_comment(problems, fixes))
        elif path.suffix == ".toml":
            revised = original if MARKER in original else toml_comment(problems, fixes) + original
        else:
            raise ValueError(f"Unsupported annotation target: {path}")
        path.write_text(revised, encoding="utf-8")

    if missing:
        raise FileNotFoundError(f"Annotation targets missing: {', '.join(missing)}")


if __name__ == "__main__":
    main()
