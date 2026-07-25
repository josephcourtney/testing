# Current Testing Assessment

This is a project-specific assessment example. It preserves concrete observed
values, local thresholds, commands, and conclusions so that the example remains
useful. Those values are not repository-wide defaults.

Statements below distinguish **observations**, **inferences**, **assumptions**,
and **decisions** where the difference matters.

## Applicability and decision

* **Observation:** Lifecycle profile is beta / stabilization.
* **Procedure:** L2-P3 stabilization and pre-release testing, applied after the
  L1 risk-and-evidence assessment.
* **Primary risks:** incorrect normalization, schema drift, unsafe target loading,
  misleading CLI diagnostics, packaging drift, and tests that pass only inside
  the checkout.
* **Decision:** pass for the stated beta decision.
* **Limitation:** production release remains separately gated by
  `production-readiness.md`; the beta result does not imply production readiness.

## Responsibility and invariant evidence

`testing-requirements.json` is the executable responsibility map. Every listed
responsibility has a passing test at each structural scope declared necessary by
that map; an unfiltered trusted run fails while a required mapping is incomplete.

The map covers:

* Python target loading,
* artifact portability,
* target resolution,
* deterministic merging,
* Typer observation,
* declaration enrichment,
* both schema contracts,
* the public Python API,
* CLI workflows,
* CLI diagnostics.

### Evidence by structural scope and purpose

* **Unit scope:** deterministic normalization, audit policy, rendering,
  configuration, worker-protocol parsing, output limits, and error translation.
* **Component scope:** public subsystem boundaries for acquisition, Typer
  observation, declarations, merging, configuration, target loading, and
  in-process CLI workflows.
* **Contract purpose:** public exports, schema validation, deterministic semantic
  goldens, and the versioned test-evidence document. These tests also declare
  their actual structural scope; `contract` is not treated as a fifth level.
* **System scope:** development-console smoke and regression workflows through
  the CLI boundary.
* **Installed-artifact evidence:** `just test-wheel` validates the exact built
  wheel from outside the checkout and exercises an independent consumer.

**Inference:** The responsibility map gives credible evidence for the listed
beta claims because it links obligations to tests and fails on missing mappings.
It does not prove that unlisted responsibilities or environments are covered.

## Boundary inventory

| Boundary | Evidence | Status and limitation |
| --- | --- | --- |
| Trusted Python import subprocess | Component, unit protocol, security-purpose, and system tests | Covered for the declared subprocess behavior and local platforms exercised |
| Native snapshot filesystem artifact | Component tests, contract-purpose semantic golden, and wheel-system reload | Covered for canonical artifact behavior |
| Typer/Click framework conversion | Unit normalization and public adapter component tests | Covered for declared supported conversion behavior |
| CLI process and exit diagnostics | Source system smoke and installed-wheel workflows | Covered for observed environments |
| Published Python and JSON interfaces | Contract-purpose tests plus independent installed consumer | Covered for declared versions and artifacts |
| Built wheel and source distribution | Content inspection, digests, isolated installation | Covered for generated artifacts |
| Database, network service, broker, external persistence | No such product boundary exists | Not applicable; reassess if introduced |

External-service integration tests are therefore **not applicable to the current
architecture**. This is not a phase-based deferral. Reassess immediately if a
remote runner, service protocol, production database, broker, or external
persistence boundary is introduced.

## Scope, mocking, and brittleness review

Every collected functional test has exactly one primary structural marker:
`unit`, `component`, `integration`, or `system`.

The prior component test that replaced the adapter's imported `get_command`
function was removed. Component tests now use supported subsystem boundaries.
The loader timeout test replaces the external subprocess runner because
controlled timeout behavior is the purpose and the replacement does not claim
to prove real process semantics.

Defensive worker-protocol branches are tested at unit scope. Multi-behavior
declaration validation was split into localized cases.

Whole help-text and prose snapshots remain intentionally absent. The only golden
documents are stable machine schemas, and each golden must:

* decode successfully,
* satisfy targeted semantic assertions,
* re-encode identically under the canonical serializer.

Tests use temporary paths and direct argument vectors. Network sockets are
disabled by default. Subprocess waits are bounded. No retry silently converts an
intermittent failure into trusted success.

## Health evidence

### Runtime and selection

* **Observation:** the complete trusted suite contains **112 tests**.
* **Observation:** it completes in a few seconds on the measured local machine.
* **Local budgets:** five seconds for the unit/developer loop and two minutes for
  the hard gate.
* **Observation:** the current suite has no skips, expected failures, or flaky
  quarantines.

These budgets and counts are project facts, not universal recommendations.

### History and flake evidence

Version-4 evidence stores per-test phase durations and comparable complete runs
under ignored `.cache/test-history`. `just health` reports the slowest tests and
uses a local gate of a measured flake rate of **1% or more across the latest 20
comparable runs**.

* **Observation:** no flakes were observed in the current sampled history.
* **Limitation:** there is not enough elapsed and comparable history to claim a
  precise long-term flake probability.
* **Decision:** the local threshold is retained as an operational trigger, not
  represented as a statistically universal boundary.

### Coverage

Current observed values for the declared complete selection and code cohort:

* **85.75% statement coverage**,
* **72.35% branch coverage**,
* **100% changed-line coverage**.

**Interpretation:** these values identify executed code and changed-line gaps;
they do not establish correctness or requirement coverage by themselves.

### Mutation

The maintained initial mutation cohort covers target parsing and Typer
default/type normalization:

* **81.73% mutation score** for the configured cohort and operators,
* **zero `no_tests` / untested mutants** under the declared handling rules.

Expansion of the cohort is tracked explicitly rather than hiding weak broader
results behind a baseline. The score is not comparable to another project or a
different operator, timeout, tool-version, or code-cohort definition.

### Health classification

* **Inference:** healthy for the stated beta decision.
* **Owner:** Maintainer.
* **Reassess on:** every profile promotion, material boundary change, expired
  waiver, observed flake, runtime regression, tool/configuration change, or
  evidence-integrity failure.

## Conditional and not-applicable evidence

| Category | Current decision and mitigation | Revisit trigger |
| --- | --- | --- |
| External database/service integration | Not applicable: the product has no such boundary | Introduction of a database, broker, remote service, or external persistence |
| Broad platform compatibility | Partial; production gate tracks required matrix cells | Support commitment or production release |
| Performance gate | Diagnostic history exists; production threshold remains uncalibrated | Sufficient comparable runs for calibration |
| Accessibility and usability | Limited because the product is a developer CLI and schema tool; diagnostic clarity is tested | Material interactive workflow, broader user cohort, or reported usability/accessibility issue |
| Operational resilience | Subprocess failure and artifact isolation are covered; no deployed service exists | Deployment as a service or introduction of persistent operational state |
| Flake probability | No flakes observed; precise rate not claimed | More comparable history or an intermittent failure |

## Residual uncertainty

* Limited compatibility evidence across the intended production matrix.
* Performance baseline not yet calibrated for release gating.
* Long-term flake behavior is not statistically characterized.
* The responsibility map can omit an unknown responsibility; exploratory and
  review evidence remain necessary.
* Findings apply only to the recorded artifacts, versions, configuration, and
  environments.

## Assessment result

**Decision: pass for beta / stabilization.**

The decision is supported by the responsibility map, trusted complete suite,
installed-artifact evidence, contract verification, current health evidence,
and explicit not-applicable boundary analysis. It does not satisfy the separate
production blockers documented in `production-readiness.md`.
