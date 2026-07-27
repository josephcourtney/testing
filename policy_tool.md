# Executable testing-policy reference

`testpolicy` is the runnable reference for turning this repository’s guidance
into project-owned state, explainable obligations, and enforceable gates. It is
implemented in `example_project/`; projects may reuse the model with different
language and test runners.

## Durable state

A policy-enabled project has a `.testing/` directory:

| Location | Canonical responsibility |
| --- | --- |
| `project.json` | Project identity, active lifecycle profiles, supported decision contexts, owners, and the accepted profile decision. |
| `claims.json` | Owned product claims and policy categories. |
| `architecture.json` | Components and path patterns mapped to claims, plus material boundaries. |
| `commands.json` | Named project-native commands through a closed supported-tool interface, with binary, arguments, and timeout. |
| `policies.json` | Project-specific rules and reviewed not-applicable overrides. |
| `decisions/` | Immutable proposals and accepted profile, threshold, assessment, and risk decisions. |
| `waivers/` | Owned, mitigated, expiring exceptions to identified rules. |
| `attestations/` | Current records of human evaluation for a rule and decision context. |

Metric definitions remain in the project’s metric-specification file. Numeric
thresholds must point to an accepted decision record. Quarantined tests remain
in the quarantine manifest and require a node identifier, owner, rationale, and
future expiry.

Policy identifiers are stable review handles. Built-in rules live in the tool’s
catalog; project additions live in `policies.json`. Every rule declares:

- applicability by decision, lifecycle profile, claim category, or boundary;
- blocking or advisory severity;
- a machine validator or explicit human attestation;
- a canonical guidance document, section, and short summary.

`testpolicy validate` checks the structure, references, unique identifiers,
command interface, project overrides, durable record filenames, and guidance
anchors before policy resolution. Rules refer to command IDs; they cannot embed
arbitrary command arrays.

## Resolution and explanation

`plan`, `status`, and `gate` use the same resolver. This keeps local output, CI,
and developer explanations consistent. Resolution combines:

1. the decision context;
2. accepted active profiles;
3. declared claim categories;
4. architectural boundaries and optional change impact;
5. project additions and justified not-applicable overrides;
6. active waivers;
7. validated machine evidence or current human attestations.

`--json` provides stable machine-readable output. `--base REVISION` or repeated
`--changed-path PATH` narrows claim-dependent rules through the architecture
map. Core governance still applies.

`explain` prints the applicability trace, evidence result, summary, and exact
guidance section. `review` filters the plan to human work and exceptions so a
developer does not need to browse the entire guidance set during a decision.

## Managed changes

The command groups make policy changes visible and reviewable:

- `profile show`, `profile propose`, and `profile apply` manage lifecycle stage;
- `assess start` and `decision finalize` retain decision reasoning;
- `metric validate`, `metric propose`, and `metric apply` govern thresholds;
- `quarantine add` creates an owned, expiring test exception;
- `waive` creates an owned, mitigated, expiring policy exception;
- `attest` records a performed human evaluation and its limitations.

New records are created without overwriting an existing identifier. JSON writes
use a same-directory temporary file followed by atomic replacement. Accepted
state changes name the approver and rationale.

## Automation boundary

The reference automates deterministic work: applicability, configuration
validation, change impact, test selection integrity, requirement coverage,
quarantine expiry, evidence shape, artifact execution, performance thresholds,
compatibility aggregation, release aggregation, and blocking gates.

It deliberately does not claim that automation can decide:

- whether a claim or failure mode is materially complete;
- whether a lifecycle transition is justified;
- whether users understand or can operate a system;
- whether a recovery result is usable;
- whether residual uncertainty or a waiver is acceptable.

For those questions, automation requires an owned record, checks its required
context and expiry, and surfaces the relevant section at the decision point.
The human remains responsible for the substantive judgment.

## CI integration

Run `testpolicy validate` before evidence collection and `testpolicy gate` after
it. Use the actual decision context: `merge` for ordinary integration,
`release` after artifact, performance, compatibility, and aggregate release
evidence. CI should retain the JSON plan and evidence artifacts needed to
diagnose a failure.

The reference project exposes these steps through stable `just` recipes and
demonstrates a production release matrix on macOS and Ubuntu.
