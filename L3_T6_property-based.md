# L3-T6 — Generative, Property, Model, and Differential Testing

## 1. Purpose

Explore a broad or sequential input space using generated cases and compact oracles. Generative testing complements selected examples by searching for counterexamples, invalid transitions, implementation disagreements, and relations that should hold when a direct expected value is difficult to enumerate.

## 2. Applicable techniques

### Property-based testing

Generate inputs and assert invariants such as idempotence, round trips, bounds, monotonicity, conservation, symmetry, normalization, or compatibility.

### Stateful or model-based testing

Generate action sequences, maintain a reference model, and compare the system state or outputs after each transition. This is appropriate for stores, protocols, workflows, parsers with modes, caches, schedulers, and other stateful behavior.

### Differential testing

Run the same input against independent implementations, versions, backends, execution modes, or a trusted reference and investigate disagreements.

### Metamorphic testing

Transform an input or environment and assert an expected relation between results when an exact oracle is unavailable. Examples include permutation invariance, scale relations, translation invariance, and behavior-preserving serialization changes.

### Generated contract or integration testing

Generate values or interaction sequences at a boundary when real infrastructure remains affordable and deterministic enough. Generative testing is not limited to pure functions or unit scope.

## 3. Applicability

Use when:

* edge cases are numerous or difficult to anticipate,
* behavior can be expressed as properties or model transitions,
* several implementations or modes should agree,
* exact expected values are costly but relational oracles exist,
* failures depend on action order or accumulated state,
* parsers, protocols, numeric transformations, serialization, data structures, or workflow engines accept rich input domains.

Avoid when the only available property merely restates the implementation, the generator cannot represent the relevant domain, or the execution cost prevents useful exploration without a better harness.

## 4. Design rules

### Define the domain

Specify valid, invalid, boundary, adversarial, and out-of-scope regions. A generator should reflect domain structure rather than produce unconstrained noise unless arbitrary bytes are the actual interface.

### Define the oracle independently

Prefer:

* domain invariants,
* a simpler reference model,
* an independently implemented algorithm,
* a compatibility specification,
* a metamorphic relation,
* safety properties that must hold after every transition.

Avoid computing the expected result through the same logic used by the system under test.

### Preserve diagnostics

* Keep generated examples small enough to shrink or minimize.
* Record seeds or counterexamples when the framework does not reproduce them automatically.
* Include the action trace and relevant state for sequential failures.
* Convert important discovered cases into targeted regressions when a named failure mode should remain visible.

### Control cost without destroying coverage

Bound sizes, sequence lengths, deadlines, and infrastructure use according to cadence. Use a small generated portfolio for rapid feedback and broader campaigns in scheduled workflows when appropriate.

## 5. Writing procedure

1. State the failure class and input or action domain.
2. Choose property, state-machine, differential, metamorphic, or mixed technique.
3. Define the oracle independently in plain language.
4. Build generators that cover ordinary, boundary, invalid, and structurally diverse cases.
5. Verify that shrinking or trace minimization produces actionable failures.
6. Seed the test with known difficult examples when useful.
7. Run a deliberate fault or mutation to confirm the oracle detects plausible defects.
8. Record discovered counterexamples and clarify the specification when results are ambiguous.

## 6. Evaluation

A good generative test:

* explores a domain wider than the example suite,
* has a comprehensible and independent oracle,
* produces reproducible minimal failures,
* exercises meaningful state or boundary behavior,
* remains within its declared cost budget.

Red flags:

* generators exclude the difficult parts of the domain,
* assertions are tautologies,
* generated tests merely repeat a few constants,
* sequential tests lack a reference model or invariant,
* differential tests assume one implementation is correct without justification,
* timeouts are treated as flaky noise rather than a harness or complexity signal.

## 7. Outputs

* property and model inventory,
* generator-domain description,
* counterexamples and regression candidates,
* unmodeled states or unsupported domains,
* recommended scope and cadence changes.
