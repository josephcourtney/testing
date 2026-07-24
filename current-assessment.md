# Current Testing Assessment

## Applicability and decision

- Lifecycle stage: beta.
- Applicable procedure: L2-P3 stabilization and pre-release testing.
- Primary risks: incorrect normalization, schema drift, unsafe target loading, misleading CLI
  diagnostics, packaging drift, and tests that pass only inside the checkout.
- Outcome: pass for L2-P3. Production remains separately gated as described in
  `production-readiness.md`.

## Responsibility and invariant evidence

`testing-requirements.json` is the executable responsibility map. Every listed responsibility has a
passing test at every required structural scope; an unfiltered run fails while any mapping is
incomplete. It covers Python loading, artifact portability, target resolution, merge determinism,
Typer observation, declaration enrichment, both schema contracts, the public API, CLI workflows,
and CLI diagnostics.

Unit tests cover deterministic normalization, audit policy, rendering, configuration, worker
protocol parsing, output limits, and error translation. Component tests exercise public subsystem
boundaries for acquisition, Typer observation, declarations, merging, configuration, and in-process
CLI workflows. Contract tests cover public exports, schema validation, deterministic semantic
goldens, and the versioned test-evidence document. System smoke tests exercise the console boundary.
`just test-wheel` separately validates the exact built wheel from outside the checkout.

## Boundary inventory

| Boundary | Evidence | Status |
| --- | --- | --- |
| Trusted Python import subprocess | Component, unit protocol, security, and system tests | Covered |
| Native snapshot filesystem artifact | Component, contract golden, and wheel-system reload | Covered |
| Typer/Click framework conversion | Unit normalization and public adapter component tests | Covered |
| CLI process and exit diagnostics | Source smoke and installed-wheel workflows | Covered |
| Published Python and JSON interfaces | Contract tests plus independent installed consumer | Covered |
| Built wheel and source distribution | Content inspection, digests, isolated install | Covered |
| Database, network service, broker, external persistence | No such product boundary exists | Not applicable |

External integration tests are therefore not applicable. Reassess immediately if a remote runner,
service protocol, database, broker, or external persistence boundary is introduced.

## Scope, mocking, and brittleness review

Every collected test has exactly one structural marker. The prior component test that replaced the
adapter's imported `get_command` function was removed; component tests now use public boundaries and
only the loader timeout test replaces the external subprocess runner. Defensive worker protocol
branches are tested at unit scope. Multi-behavior declaration validation was split into localized
cases.

Whole help/prose snapshots remain intentionally absent. The only golden documents are stable machine
schemas, and each golden must decode, satisfy semantic assertions, and re-encode identically. Tests
use temporary paths and direct argument vectors, network sockets are disabled by default, subprocess
waits are bounded, and no retry hides nondeterminism.

## Health evidence

The current full suite contains 112 tests and completes in a few seconds locally, within the five
second unit/developer-loop and two-minute hard-gate budgets. It has no skips, expected failures, or
flaky quarantines. Version-4 evidence stores per-test phase durations and comparable full runs under
ignored `.cache/test-history`; `just health` reports the slowest tests and fails at a measured flake
rate of 1% or more across the latest 20 comparable runs. There is not yet enough elapsed history to
claim a statistically meaningful long-term flake rate.

Current coverage is 85.75% statements and 72.35% branches, with 100% changed-line coverage. The
initial maintained mutation cohort covers target parsing and Typer default/type normalization at
81.73% with zero untested mutants. Expanding mutation scope is tracked explicitly rather than
hiding weak broader results in a baseline.

Health classification: healthy for beta. Owner: Maintainer. Reassess on every phase promotion,
material boundary change, expired waiver, or observed flake/runtime regression.

## Conditional classes

| Class | Decision and mitigation | Revisit trigger |
| --- | --- | --- |
| Integration | Not applicable; no external-system boundary exists. | Add a service, database, broker, remote runner, or persistence dependency. |
| Broad snapshots | Not applicable to human prose; targeted semantic machine-document goldens are used. | Human output becomes a compatibility contract. |
| Data quality | Not applicable; no managed dataset exists. | Add persistent observation corpora or learned/statistical behavior. |
| Chaos/privacy | Not applicable to the current local library/CLI risk profile. | Add a live service, sensitive data, authentication, or multi-system recovery behavior. |
