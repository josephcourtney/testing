# Production Testing Readiness

This is a project-specific production-readiness assessment. It applies L1,
L2-P4, and the relevant L3 procedures without treating the checklist or numeric
values as universal policy.

Each readiness area is classified as applicable, not applicable with rationale,
satisfied, conditional, waived, unresolved, or blocking. Concrete thresholds
and measured values are retained because they are part of this example
project's evidence.

## Decision scope

* **Decision:** production release of the current built artifact.
* **Profile:** L2-P4 release and hardening.
* **Current result:** **fail for production release**.
* **Active waiver:** none.
* **Primary blockers:** incomplete compatibility matrix and uncalibrated
  performance baseline.

A beta pass in `current-assessment.md` does not override these production
blockers.

## Risk-driven evidence

| Risk or claim | Implemented evidence | Current decision | Identity or limitation |
| --- | --- | --- | --- |
| Functional and contract regression | Unit, component, contract-purpose, smoke-purpose system tests, executable requirement map, and coverage ratchets | Pass | Applies to the current revision and declared trusted complete selection |
| Installed behavior and packaging | Exact-wheel outside-checkout suite, independent consumer, archive inspection, and SHA-256 digests | Pass | Applies to the exact generated wheel and source distribution |
| Import/subprocess trust boundary | Direct argv, bounded timeout, environment sanitization, output bound, malformed/crash diagnostics | Pass | Covers the declared loader and subprocess protocol behavior |
| Security and supply chain | Secret scan in `just check`; dependency audit and distribution verification in `just release-check` | Required gate | A passing scan establishes only the configured rules and databases |
| Mutation sensitivity | Maintained cohort at **81.73%**, with zero untested mutants | Pass for configured cohort; expansion tracked | Cohort, operators, timeout behavior, tool version, and exclusions define the result |
| Operability | Stable exit classes, stderr/no-traceback tests, retained gate diagnostics | Pass for current CLI operating model | No deployed service, persistent database, or on-call operation exists |
| Performance | Two warmups and seven measurements per fixed operation; comparable local history | Conditional: baseline uncalibrated | Not yet a valid production gate |
| Compatibility | Portable same-revision and lockfile evidence with four-cell matrix gate | Fail: **1 of 4** required cells present | Missing required Linux and Python cells |
| Data quality | No managed dataset or production transformation pipeline | Not applicable | Reassess if persistent or externally sourced data is introduced |
| Accessibility and usability | CLI diagnostic behavior, stable structured output, and error recovery checks | Conditional / limited | No representative user study; broaden if the audience or interface changes |
| Deployment, rollback, restoration, failover | Installed-package verification; no deployed service or persistent operational state | Not applicable to current product form | Reassess if deployment or persistent state is introduced |

## Performance evidence and gate design

The project collects performance evidence before enforcing a strict production
gate.

### Current harness

For each fixed operation:

* **2 warmup executions**,
* **7 measured executions**,
* recorded artifact, platform, runtime, dependency, and configuration identity,
* comparable local history grouped by platform fingerprint.

### Calibration rule

Performance becomes release-blocking only after **10 comparable runs** have at
most **10% coefficient of variation** for the calibrated metric.

Until then:

* results are diagnostic,
* large regressions should still be investigated,
* the absence of a calibrated gate is an explicit production-readiness gap,
* incompatible machines or workloads are never treated as one series.

### Strict regression rule after calibration

After calibration, the local gate rejects a median that exceeds both:

1. **115% of baseline**, and
2. **baseline + 100 ms**.

Both the relative and absolute conditions are required so that small noisy
changes and large practically meaningful regressions are treated differently.

These values are project-specific decisions. They require review when workload,
hardware, implementation, dependencies, or user expectations change.

### Current status

**Blocking:** the baseline has not yet accumulated the required 10 comparable,
stable runs. The performance claim is therefore not ready to support production
release gating.

## Compatibility evidence and gate design

The production support commitment requires four cells:

| Operating system | Python | Current status |
| --- | --- | --- |
| Darwin | 3.13 | Missing |
| Darwin | 3.14 | Passing evidence present for Python 3.14 only; 3.13 remains missing |
| Linux | 3.13 | Missing |
| Linux | 3.14 | Missing |

Imported compatibility cells must match:

* the current source revision,
* the current `uv.lock` digest,
* the declared test-evidence schema,
* the required complete trusted selection,
* compatible tool and configuration identity.

Stale, partial, differently locked, or differently revised cells do not satisfy
the gate.

### Current status

**Blocking:** only **Darwin / Python 3.14** evidence is currently available. The
other three required cells are absent.

## Functional, contract, and artifact evidence

The release candidate retains:

* the executable responsibility map,
* unit and component evidence for critical logic and subsystem behavior,
* contract-purpose schema and public-API checks at declared structural scopes,
* system-scope smoke and regression workflows through the CLI,
* exact wheel and source-distribution inspection,
* isolated installation outside the checkout,
* an independent public-API consumer,
* archive digests and package metadata checks.

**Limitation:** these results do not extend to unsupported platforms,
configurations, dependency versions, or future artifacts.

## Security and supply-chain evidence

The required release workflow includes:

* repository and history secret scanning,
* dependency vulnerability audit,
* package metadata validation,
* source and wheel content inspection,
* SHA-256 artifact digests,
* isolated install and import verification,
* verification that the independent consumer does not rely on source-checkout
  paths.

Findings require triage rather than blanket suppression. A scanner pass is
limited to its configured rules, advisory database, and analyzed inputs.

## Operability and diagnostics

For the current CLI product form, operability evidence includes:

* stable exit classifications,
* expected separation of stdout and stderr,
* failure diagnostics without unhandled traceback leakage,
* bounded subprocess behavior,
* output-size controls,
* malformed worker-response handling,
* retained release artifacts and gate diagnostics.

Because the product is not currently a deployed service and has no managed
persistent state, service failover, backup restoration, production alerting,
and on-call runbook exercises are not applicable. That conclusion must be
revisited if the operating model changes.

## Release gate execution

`just release-check <directory>`:

1. runs every required local and imported evidence step even after an earlier
   failure,
2. records individual failures and limitations,
3. validates imported compatibility identity,
4. evaluates calibrated gates only when their preconditions are satisfied,
5. writes `.cache/release.json`,
6. produces a diagnosable aggregate release decision.

The command must not convert missing or invalid evidence into a pass merely
because unrelated checks succeeded.

## Release decision

Current decision: **fail for production release**.

Blocking conditions:

* three of four required compatibility cells are missing,
* the performance baseline is not yet calibrated for production gating.

No waiver is active. A release would require either:

* satisfying both blockers, or
* a separately authorized, bounded waiver identifying affected claims,
  mitigations, owner, expiry, and rollback or containment conditions.

## Maintenance readiness

Maintenance infrastructure currently supports:

* comparable run history,
* defect recording,
* performance-drift history,
* portable compatibility evidence,
* waiver-expiry representation,
* exact-artifact release records.

L2-P5 maintenance compliance is not claimed merely because this infrastructure
exists. It requires a real change, incident, dependency update, or
continued-operation decision with change-impact evidence.

## Residual uncertainty and revisit triggers

Reassess when:

* missing compatibility cells arrive,
* the performance baseline reaches calibration criteria,
* a dependency, runtime, lockfile, platform, or build process changes,
* the product gains a database, network service, broker, persistent state, or
  deployed operating environment,
* a security advisory, incident, escaped defect, usability finding, or
  accessibility issue appears,
* the support matrix or user cohort changes,
* a waiver is proposed or expires.
