# L3-T11 — Metric Design and Validation

## 1. Purpose

Define quantitative evidence so that a reported number has a stable meaning and a justified relationship to a decision. This procedure applies before coverage, mutation, flake, runtime, defect, performance, reliability, data-drift, or similar metrics are used as targets or gates.

## 2. Metric specification

For each metric, record:

* **decision** — what action the metric informs,
* **claim** — what property the metric is evidence about,
* **population** — tests, code, requests, versions, environments, users, records, or incidents included,
* **denominator** — the basis of the rate or percentage,
* **measurement method** — tool, configuration, sampling, exclusions, and aggregation,
* **environment** — hardware, platform, dependency, data, and workload identity,
* **window or baseline** — period, revision, cohort, and comparability rules,
* **uncertainty** — variance, confidence interval, sparse-data limitations, and known bias,
* **threshold** — rationale and practical effect represented by the boundary,
* **response** — block, investigate, warn, recalibrate, or collect more data,
* **owner and review trigger**.

A metric without these fields is diagnostic information, not a valid gate.

## 3. Common metrics

### Coverage

Line and branch coverage indicate which instrumented code executed. They do not demonstrate assertion quality, requirement coverage, or correctness.

When gating coverage:

* define the code cohort and exclusions,
* prefer changed-code or risk-focused analysis when aggregate coverage hides new gaps,
* inspect uncovered responsibilities rather than only the percentage,
* do not define general path-coverage percentages without a meaningful, computable path model.

### Mutation score

Mutation score is meaningful only for the declared code cohort, mutation operators, timeout policy, equivalent-mutant treatment, and `no_tests` handling. Compare scores only when those inputs are stable.

### Flake observations

Define what counts as a flake, distinguish test nondeterminism from infrastructure failure, and state whether the unit of analysis is test run, test case, job, or suite. Do not claim a precise probability from a small number of observations.

### Runtime and feedback latency

Measure the workflows users actually wait for. Separate setup, execution, teardown, queue time, and retries where they imply different remedies.

### Performance

Define workload, warmup, sample count, hardware, noise controls, statistic, baseline, and both relative and practical absolute effects. Do not combine incompatible environments.

### Defect and incident metrics

Define severity, discovery stage, attribution, reporting process, and observation period. Avoid cross-project comparisons based on KLOC or raw counts without controlling for language, reporting, and exposure.

### Data and model drift

Define the reference population, feature or output distribution, sample size, multiple-testing policy, operational meaning, and whether a threshold should alert, block, or trigger investigation. Generic KS, PSI, or accuracy thresholds are not portable defaults.

## 4. Validation procedure

1. Write the metric specification.
2. Test the collection pipeline with known fixtures or synthetic cases.
3. Verify that partial, stale, or non-comparable observations cannot contaminate the result.
4. Estimate natural variation before setting a regression threshold.
5. Check whether the metric changes when a relevant failure is deliberately introduced.
6. Check for obvious gaming or perverse incentives.
7. Define what human investigation accompanies a threshold crossing.
8. Review the definition when tools, cohorts, environments, workloads, or decisions change.

## 5. Gate criteria

A metric may gate a decision only when:

* its definition is versioned and reproducible,
* its data is fresh and comparable,
* its sensitivity to the relevant failure has been demonstrated,
* its uncertainty is compatible with the decision,
* its threshold has a documented technical or product rationale,
* the response to failure is actionable.

Otherwise report it as descriptive evidence with an explicit limitation.

## 6. Outputs

* metric specification,
* validation evidence,
* baseline or comparison cohort,
* threshold rationale,
* uncertainty and comparability limits,
* action and ownership.
