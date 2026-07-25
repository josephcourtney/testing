# L3-T2 — Component Testing: Design, Writing, Evaluation

## 1. Purpose

Provide evidence about a coherent subsystem through a supported interface while preserving the collaboration that gives the component its behavior.

## 2. Applicability

Use component scope when:

* several units collaborate to deliver a supported behavior,
* the subsystem boundary is meaningful to callers,
* outside dependencies can be controlled without removing the semantics at risk,
* unit tests alone do not establish orchestration or subsystem behavior.

Use integration scope when evidential value depends on real external semantics. Use system scope when the claim concerns the assembled product through a user or operator boundary.

## 3. Define the boundary

Record:

* supported entrypoints,
* responsibilities and invariants inside the component,
* dependencies and resources inside the boundary,
* dependencies outside the boundary,
* external semantics deliberately excluded.

Classify by semantics actually executed, not merely by process count or use of SQLite, temporary files, or fakes.

## 4. Collaborator strategy

Code inside the component should normally collaborate through its real implementation.

Replace an internal collaborator only when control, determinism, or fault injection is necessary and the replacement does not remove the semantics the component evidence is intended to establish.

Dependencies outside the component may be replaced, simulated, recorded, or provided through lightweight real implementations.

Temporary files and local databases are appropriate when they belong to the declared boundary and cleanup is deterministic. When production SQL dialect, isolation, extensions, or migration behavior matters, add integration evidence using the actual engine.

## 5. Assertions

Prefer:

* supported API outputs,
* boundary-visible state changes,
* emitted domain events,
* caller-visible errors,
* stable subsystem invariants.

Avoid internal call graphs, private state, and exact logs unless interaction or observability is itself contractual.

## 6. Writing procedure

1. State the claim and failure mode.
2. Define inside and outside boundaries.
3. Select real or controlled collaborators.
4. Exercise representative nominal, boundary, and failure workflows.
5. Assert boundary-visible outcomes.
6. Deliberately break a relevant behavior to validate the oracle.
7. Record excluded semantics needing contract, integration, or system evidence.

## 7. Evaluation

Good component evidence:

* uses supported interfaces,
* preserves meaningful internal collaboration,
* justifies any internal replacement,
* is deterministic and diagnosable,
* adds confidence beyond unit tests,
* remains sensitive to the intended failure mode.

Red flags include god fixtures, internal mock graphs, unrealistic fakes treated as integration proof, and component suites that duplicate every unit case or drift into an unharnessed system suite.

## 8. Outputs

* component boundary and responsibility map,
* workflow and failure-mode coverage,
* collaborator-fidelity limitations,
* missing contract, integration, or system evidence,
* candidates for scope adjustment.
