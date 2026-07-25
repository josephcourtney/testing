# L3-T2 — Component Testing: Design, Writing, Evaluation

## 1. Purpose

Validate a **coherent subsystem** through a supported interface, exercising real
collaboration among the code inside the chosen component boundary while
controlling dependencies outside it.

Component scope sits between a small local unit and evidence whose value depends
on real external or infrastructure semantics. Process count, temporary files,
SQLite, containers, or fakes do not determine scope by themselves; classify the
test by the semantics actually exercised.

## 2. Applicability

Use component scope when:

* multiple units must collaborate to deliver meaningful behavior,
* correctness depends on orchestration, internal adapters, or subsystem state,
* a supported module, package, service object, or in-process interface can serve
  as the boundary,
* unit evidence is too narrow but real production infrastructure is not required
  for the claim,
* a lightweight real implementation preserves the component semantics more
  clearly than a large network of mocks.

Do not use component evidence as a substitute for:

* contract evidence at published or independently consumed boundaries,
* integration evidence when real SQL, protocol, platform, framework, process, or
  service semantics are the risk,
* system evidence for complete assembled user or operator workflows,
* acceptance, usability, accessibility, security, performance, or operational
  evidence when those are the actual purposes.

### 2.1 When not to use component scope

Prefer another scope when:

* the behavior is fully local and a smaller unit gives clearer localization,
* the test's evidential value depends on a real external boundary,
* the oracle is available only through the assembled product,
* an unrealistic fake would make a passing result misleading.

## 3. Design rules

### 3.1 Define the component boundary

Identify:

* the supported entrypoint,
* the coherent responsibilities being validated together,
* code and collaborators considered **inside** the component,
* dependencies and semantics considered **outside**,
* resource use, such as filesystem, process, database, clock, configuration, or
  random source,
* excluded semantics that require contract, integration, or system evidence.

Code inside the component boundary should normally collaborate through its real
implementation. Replacing an internal collaborator is justified when deliberate
control, fault injection, or rare-state construction is necessary and the
replacement does not remove the semantics the component test is intended to
exercise.

Dependencies outside the boundary may be replaced, simulated, recorded, or
provided through lightweight real implementations.

### 3.2 Choose substitutes and lightweight dependencies deliberately

Prefer simple, comprehensible options such as:

* in-memory repositories,
* fake clients,
* stub servers,
* controlled clocks and random sources,
* temporary directories,
* temporary SQLite databases,
* lightweight local implementations of an external interface.

Temporary directories or SQLite databases are appropriate when they remain
inside the declared component boundary, preserve the needed semantics, and have
deterministic setup and cleanup.

Avoid:

* extensive mock graphs that reproduce the component's internal call structure,
* fakes whose behavior is assumed rather than validated,
* substitutions that eliminate the failure mode under examination,
* hidden shared fixtures or ambient state.

Pair consequential fakes with contract or integration evidence where fidelity
matters.

### 3.3 Assertions

Assert behavior observable through the component boundary, including:

* returned values and objects,
* supported state transitions,
* persisted records in a controlled store,
* emitted events captured through a supported interface,
* externally meaningful error categories and rejection behavior,
* stable serialization or artifact properties,
* critical invariants across a representative workflow.

Avoid:

* verifying internal method-call graphs,
* private attributes and incidental intermediate state,
* exact logging prose unless wording is contractual,
* snapshots without targeted assertions for critical semantics.

### 3.4 Determinism and diagnostics

Component tests should:

* control external effects and variability,
* avoid hidden ordering and shared mutable state,
* bound waits and subprocesses,
* identify setup, input, component boundary, and failed obligation,
* distinguish component failure from fixture, fake, environment, or harness
  failure.

## 4. Writing procedure

1. State the claim and failure mode the test should detect.
2. Pick a supported component entrypoint.
3. Declare what is inside and outside the component boundary.
4. Choose real collaborators, controlled substitutes, and lightweight resources.
5. Set up representative nominal state with minimal implicit fixture behavior.
6. Exercise a meaningful workflow:
   * happy path,
   * important boundary or variation,
   * critical rejection or error path.
7. Assert outcomes visible at the component boundary.
8. Verify that the test fails when the behavior is plausibly broken.
9. Record excluded real-world semantics and the higher-scope evidence that covers
   them.
10. After the interface stabilizes, consider a canonical snapshot for a large
    stable output only when it improves reviewability.

## 5. Evaluating an existing component test

A component test is good when:

* it uses supported component interfaces,
* it exercises collaboration that unit tests alone do not establish,
* internal implementations normally remain real,
* any internal replacement is justified and preserves the semantics under
  review,
* outside dependencies are controlled without making the oracle unrealistic,
* assertions target boundary-visible behavior,
* it is deterministic and diagnostically useful,
* its resource and purpose classifications are explicit where useful.

Red flags:

* a test labeled component but exercising only one pure function,
* a component test that has become an ungoverned miniature system suite,
* fragile or opaque “god fixtures,”
* deep interaction mocking coupled to implementation details,
* fakes treated as proof of real dependency behavior,
* tests passing while incorrect behavior remains possible because the fake is
  too weak,
* hidden filesystem, process, clock, configuration, or database dependencies,
* duplicated exhaustive logic matrices already covered more clearly at unit
  scope.

## 6. Evaluating the component suite

Check:

* **Boundary coverage** — critical supported component entrypoints and workflows.
* **Risk coverage** — the actual failure modes the component suite can detect.
* **Fidelity** — whether substitutes preserve needed behavior and are verified.
* **Duplication** — avoid repeating every unit path without added subsystem
  semantics.
* **Execution time** — keep appropriate component evidence usable in merge
  workflows; move only genuinely expensive campaigns to another cadence.
* **Isolation** — resource reset, cleanup, ordering independence, and bounded
  waits.
* **Diagnostics** — failures should implicate a component behavior or a clearly
  identified harness problem.
* **Confidence gaps** — real boundary semantics should be queued for integration,
  contract, compatibility, or system evidence.

## 7. Scope adjustment guidance

* Downscope to **unit (L3-T1)** when the meaningful behavior is local and a
  smaller boundary preserves the failure mode.
* Keep component scope when a coherent subsystem must collaborate but real
  external semantics are not required.
* Upscope to **integration (L3-T3)** when correctness depends on real database,
  protocol, service, process, framework, or platform behavior.
* Upscope to **system (L3-T4)** when only assembled user- or operator-visible
  behavior provides the required oracle.
* Add **contract (L3-T7)** evidence when a substitute or interface must remain
  compatible with an independently changing producer or consumer.

## 8. Outputs

* component boundary and supported-entrypoint inventory,
* collaborator and resource strategy,
* map of component workflows to evidence,
* fake and lightweight-dependency fidelity assumptions,
* missing workflows or error behavior,
* tests to downscope, upscope, split, remove, or supplement,
* required contract, integration, system, or non-functional follow-up.
