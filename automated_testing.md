# Automated Testing: Concepts and Tradeoffs

This document is non-normative conceptual reference material. It discusses common approaches and tradeoffs; it does not establish repository policy, lifecycle requirements, tool choices, portfolio ratios, or numeric gates.

Use `Overview.md` for policy, `glossary.md` for terminology, and the applicable L1/L2/L3 procedures for normative decisions.

## 1. Automated evidence in context

Automated tests are one form of evidence. They are especially useful when behavior can be executed repeatedly with a stable oracle. Review, formal analysis, exploratory work, usability evaluation, audits, measurement, and production observation may be more appropriate for other claims.

A passing suite supports only the claims, conditions, and environments it actually exercises.

## 2. Scope is not quality

Unit, component, integration, and system describe execution boundaries. None is intrinsically superior.

Lower scope often improves speed and localization. Higher or real-boundary scope may be required when correctness depends on framework, protocol, persistence, platform, packaging, deployment, or assembled-product semantics.

Choose the least costly boundary that preserves the failure mode.

## 3. Purposes and techniques compose

Acceptance, regression, contract, smoke, security, performance, and other purposes can occur at several structural scopes.

Example-based, property-based, state-machine, differential, metamorphic, fuzz, snapshot, mutation, and fault-injection techniques address different failure classes. A project normally combines several dimensions rather than choosing one taxonomy.

## 4. Solitary and sociable units

A solitary style replaces collaborators outside a focal unit. It can improve control and localization but may couple tests to interactions or rely on unrealistic doubles.

A sociable style retains inexpensive deterministic collaborators. It can provide stronger collaboration evidence with less mocking but may broaden failure localization.

Projects may use either or both. The relevant question is whether the chosen boundary and collaborator strategy preserve the semantics needed by the claim.

## 5. Test doubles

Dummies, stubs, spies, mocks, fakes, simulators, emulators, and record/replay systems provide different control and fidelity.

Doubles are valuable for rare states, fault injection, determinism, and speed. They cannot establish real behavior that they do not reproduce. Consequential doubles should be paired with contract, integration, compatibility, or production evidence.

## 6. Development workflows

TDD, acceptance-test-driven development, behavior-driven development, test-after development, and exploratory prototyping are workflows, not quality proofs.

TDD can clarify design and create rapid feedback. Test-after work may be more efficient during discovery or when the interface is unstable. Acceptance examples can improve stakeholder alignment. Teams should standardize workflows only where the collaboration benefit justifies the constraint.

## 7. Portfolio heuristics

Pyramids, trophies, honeycombs, and similar diagrams are planning metaphors. They emphasize different costs and risks but do not prescribe universal ratios.

Portfolio shape should follow architecture, failure modes, environment cost, and required feedback latency. A local library, database adapter, browser application, distributed service, and hardware controller need different evidence distributions.

## 8. Generative testing

Property-based testing checks invariants over generated domains. Stateful and model-based testing explore action sequences and transitions. Differential testing compares implementations or versions. Metamorphic testing checks relations when exact outputs are unavailable. Fuzzing emphasizes malformed, adversarial, random, or coverage-guided inputs.

Useful generative evidence requires a representative domain, independent oracle, reproducible counterexamples, and controlled cost.

## 9. Snapshots

Snapshots are useful when a canonical diff is the clearest oracle for a stable artifact. They become weak when outputs are noisy, too broad to review, or used to avoid stating critical semantics.

Snapshot updates are behavior approvals and should receive semantic review.

## 10. Performance and metrics

Coverage, mutation, runtime, flake observations, and performance measurements can reveal gaps or regressions. Their meaning depends on population, denominator, environment, baseline, uncertainty, and response.

No percentage or duration is portable without a metric specification. Use L3-T11 before converting a measurement into a gate.

## 11. Lifecycle

Projects often move from exploration to development, stabilization, production, and maintenance, but evidence applicability does not wait for a phase.

A prototype may need strong security or recovery evidence. A mature local tool may need no external integration tests. Lifecycle profiles adjust confidence, fidelity, cadence, and governance rather than supplying a fixed inventory.

## 12. Automation limits

Automation is weak when:

* the requirement is ambiguous,
* human comprehension or usability is intrinsic,
* the environment cannot be represented credibly,
* the oracle merely repeats the implementation,
* evidence can be gamed or silently contaminated,
* maintenance cost exceeds the confidence gained.

In those cases, combine automation with review, exploration, measurement, user evaluation, or operational observation.
