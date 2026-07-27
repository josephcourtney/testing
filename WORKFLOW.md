# Testing-policy workflow

Use this workflow for a change, merge, release, deployment, continued-operation
review, or explicit risk acceptance. `Overview.md` remains the normative policy;
this document is the operational route through it.

## 1. Identify the decision

Name the decision before selecting tests. Record its owner and the consequence
of a wrong decision. Typical decision contexts are `merge`, `release`,
`deployment`, `continued_operation`, and `risk_acceptance`.

In a policy-enabled project, inspect the current state:

```console
testpolicy profile show
testpolicy validate
```

## 2. Resolve the applicable policy

Declare the claims the project relies on and map source paths and architectural
boundaries to those claims. Then resolve the active lifecycle profiles, decision
context, claim categories, boundaries, project additions, and reviewed
exceptions:

```console
testpolicy plan --decision merge
testpolicy plan --decision release --base origin/main
```

The second form limits claim-dependent obligations to claims affected by the
change. Core obligations and lifecycle governance still apply.

Use `testpolicy explain RULE-ID` to see why a rule applies, its current evidence
status, and the exact canonical guidance section. Applicability is about
material risk; a lifecycle profile changes defaults and confidence expectations
but does not erase a material claim or boundary.

## 3. Perform the assessment

For a material or unfamiliar decision, start an assessment record:

```console
testpolicy assess start --id ASSESSMENT-ID --kind release --owner OWNER
```

Complete its claims, failure modes, selected evidence, residual uncertainty, and
waiver fields using `L1.md`. Keep the record in draft until the evidence and
uncertainty support a decision.

## 4. Collect mechanical evidence

Run the project’s narrow checks while editing. Before the decision, run the
resolved mechanical obligations:

```console
testpolicy run --decision merge
```

Projects should expose stable named commands for complete trusted tests,
installed-artifact checks, performance evidence, compatibility cells, and
release aggregation. Generated and normalized evidence belongs in disposable
run storage such as `.cache/`; reviewed decisions and policy state belong in
version control.

## 5. Complete human evaluation

Automation can verify that required records exist and are current. It cannot
establish comprehension, usability, accessibility, recovered-state usefulness,
or whether residual uncertainty is acceptable. Review only the unresolved human
work:

```console
testpolicy review --decision release
testpolicy explain RULE-ID --decision release
```

Record a performed evaluation with `testpolicy attest`. Record an exception only
with `testpolicy waive`; every waiver needs an owner, rationale, mitigation, and
future expiry.

## 6. Enforce the decision gate

Run the hard gate for the actual decision:

```console
testpolicy gate --decision merge
testpolicy gate --decision release
```

The gate fails closed for missing, invalid, stale, or unresolved blocking
obligations. A passing process exit alone is not evidence unless the applicable
validator accepts the retained artifact.

## 7. Finalize and retain the decision

Finalize the assessment with its outcome, rationale, and approver:

```console
testpolicy decision finalize ASSESSMENT-ID \
  --outcome pass --approved-by APPROVER --rationale RATIONALE
```

Retain accepted lifecycle and threshold changes with the project. Keep
short-lived run evidence according to project retention policy. Revisit the
assessment when claims, architecture, supported environments, profiles,
thresholds, incidents, or evidence limitations materially change.

## Changing governed state

Preview lifecycle changes before applying them:

```console
testpolicy profile propose stabilization
testpolicy profile apply stabilization --decision-id DECISION-ID \
  --approved-by APPROVER --rationale RATIONALE
```

Threshold changes follow the same propose-and-approve pattern:

```console
testpolicy metric propose METRIC --id DECISION-ID --threshold VALUE \
  --owner OWNER --rationale RATIONALE
testpolicy metric apply DECISION-ID --approved-by APPROVER
```

See `policy_tool.md` for the state contract and automation boundary.
