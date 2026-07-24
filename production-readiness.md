# Production Testing Readiness

This assessment applies L2-P4 without claiming compliance before all release evidence exists.

## Risk-driven evidence

| Risk | Implemented evidence | Current decision |
| --- | --- | --- |
| Functional and contract regression | Unit, component, contract, smoke, requirement map, coverage ratchets | Pass |
| Installed behavior and packaging | Exact-wheel outside-checkout suite, independent consumer, archive inspection and SHA-256 digests | Pass |
| Import/subprocess trust boundary | Direct argv, timeout, environment sanitization, output bound, malformed/crash diagnostics | Pass |
| Security and supply chain | Secret scan in `just check`; dependency audit and distribution verification in `just release-check` | Required gate |
| Mutation sensitivity | Maintained cohort at 81.73%, zero untested mutants | Pass for configured cohort; expansion tracked |
| Operability | Stable exit classes, stderr/no-traceback tests, retained gate diagnostics | Pass |
| Performance | Two warmups and seven measurements per fixed operation; comparable local history | Conditional: baseline uncalibrated |
| Compatibility | Portable same-revision/lock evidence and four-cell matrix gate | Fail: 1 of 4 cells present |
| Data quality | No managed dataset | Not applicable |

Performance becomes release-blocking after ten comparable runs have at most 10% calibration
coefficient of variation. The strict gate then rejects a median that exceeds both 115% of baseline
and baseline plus 100 ms. Results from different platform fingerprints are never compared.

The compatibility gate requires Darwin and Linux on Python 3.13 and 3.14. Imported cells must match
the current revision and `uv.lock` digest. The current checkout has passing Darwin/Python 3.14
evidence only.

## Release decision

Current decision: **fail for production release**. Missing compatibility cells and an uncalibrated
performance baseline are explicit blockers. `just release-check` runs every step despite failures
and writes `.cache/release.json`, so the decision remains diagnosable. No waiver is active.

Maintenance readiness is infrastructural only: run history, defect recording, performance drift,
compatibility evidence, and waiver expiry are supported. L2-P5 cannot be claimed until real change
and escaped-defect history exists.
