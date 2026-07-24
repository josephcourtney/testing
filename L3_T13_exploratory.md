# L3-T13 — Exploratory Testing

## 1. Purpose

Discover important behavior, risks, ambiguities, and failure modes through simultaneous learning, test design, and execution. Exploratory testing complements predefined checks by investigating what was not fully anticipated.

## 2. Applicability

Use when:

* requirements or behavior are incompletely understood,
* a new feature, interface, or workflow needs critique,
* automation passes but confidence remains low,
* an incident or surprising defect suggests an unknown failure class,
* usability, configuration, interoperability, or operational behavior has many contextual variables,
* release risk warrants investigation outside scripted cases.

## 3. Charter

Define a lightweight charter containing:

* mission or question,
* area and boundaries,
* relevant risks or heuristics,
* environment, data, and personas,
* time box,
* evidence to capture.

A charter guides investigation without predetermining every action.

## 4. Procedure

1. Review known claims, risks, recent changes, and existing automated evidence.
2. Select a charter focused on an uncertainty or failure class.
3. Explore through representative, boundary, invalid, interrupted, and unexpected workflows.
4. Vary data, configuration, sequence, timing, environment, permissions, and recovery behavior where relevant.
5. Record observations, questions, coverage notes, and reproducible failures during the session.
6. Distinguish defects, specification ambiguities, usability problems, testability problems, and new risks.
7. Minimize important reproductions.
8. Convert durable findings into acceptance criteria, regression tests, contract obligations, monitoring, or design changes as appropriate.
9. Record what was not explored.

## 5. Heuristics

Useful prompts include:

* recent changes and adjacent behavior,
* interruption, cancellation, retry, and recovery,
* empty, maximal, malformed, duplicated, reordered, or stale data,
* different roles, permissions, locales, devices, and environments,
* dependency degradation or inconsistent responses,
* installation, upgrade, migration, rollback, and cleanup,
* misleading output, inaccessible interaction, and operator confusion.

Heuristics are idea generators, not completeness claims.

## 6. Evaluation

A useful exploratory session:

* addresses a stated uncertainty,
* produces reproducible evidence or a clearer specification,
* records coverage and limitations,
* identifies follow-up appropriate to the finding,
* avoids presenting unstructured clicking as sufficient testing.

Red flags:

* no charter or question,
* findings that cannot be reproduced or explained,
* no record of environment or data,
* repeated exploration of familiar paths while high-risk areas remain untouched,
* treating exploration as a substitute for durable regression evidence.

## 7. Outputs

* session charter and notes,
* defects and minimized reproductions,
* requirement or design questions,
* new risks and evidence gaps,
* regression, acceptance, contract, monitoring, or usability follow-up,
* unexplored areas.
