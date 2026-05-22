---
name: sci-experiment-manager
description: Manage experiment records for SCI research projects with low-token retrieval, stable experiment IDs, experiment cards, family/synthesis cards, lightweight indexes, result paths, keep levels, and no-fabrication rules. Use when creating, updating, combining, indexing, auditing, or retrieving experiment evidence.
---

# sci-experiment-manager

## Core principle

The experiment file system is not for beautiful classification.
It is for low-token retrieval.

Codex must be able to answer:
- which experiments are relevant to the current task?
- which experiments support this paper claim?
- which experiments are failed but informative?
- which experiments should not be repeated?
- where are the raw files if exact verification is needed?

Experiment records must preserve the chain:

```text
direction validation requirement -> experiment/probe -> result
-> supported/falsified assumption -> next problem / decision
```

The direction layer states what must be validated. The experiment layer records
how it was actually tested, what happened, and what the evidence can or cannot
support.

## Startup rule

First classify the task stage: `idea_exploration`, `minimal_probe`, `formal_experiment`, `result_analysis`, `paper_writing`, `submission_prepare`, or `maintenance`.

## Experiment retrieval order

1. `PROJECT_HANDOFF.md`
2. `QUERY_MAP.md`
3. `EXPERIMENT_INDEX.md`
4. relevant experiment cards
5. raw files only if necessary

Do not globally scan all runs, logs, results, or weights by default.

## Context discipline policy

- Use `QUERY_MAP.md` to choose task categories before opening cards.
- Use `EXPERIMENT_INDEX.md` or `.csv` to select matching rows.
- Open relevant cards for the task. A focused task may need only a few; a phase review or reviewer response may need many.
- If the task requires broad reading, state the scope before expanding.
- Read raw logs/results with targeted paths, `rg`, `head`, `tail`, or metric-specific extraction.
- Do not run `collect_results.py` as a default task startup step; run it only for index maintenance or explicit result collection.
- Do not run `update_experiment_index.py` on every task; use it when cards changed or the user asks to refresh the index.

## Experiment ID rule

Every formal experiment must have a stable ID:

`E001`, `E002`, `E003`, ...

Experiment ID must not change after creation.

For direction exploration, prefer family-level IDs when many probes answer the
same broad question:

- `F012`: direction family / umbrella record
- `F012-D01`: diagnostic or idea probe inside the family
- `E023`: legacy or formal experiment ID only when the project already uses it

Do not create a long flat sequence of same-level `E` IDs for early idea probes.
Use a family card plus a sub-index when a branch contains multiple diagnostics,
controls, or blocked follow-ups.

## Experiment-card architecture

Use three record levels.

### 1. Single experiment card

Use for a concrete run, diagnostic, smoke, or formal evidence item. It should
answer:

- what validation requirement it came from;
- what assumption it tested;
- exact setup and paths;
- key results;
- what the result supports;
- what it does not prove;
- next problem or decision.

### 2. Direction family card

Use for a route containing several sub-probes, controls, or failed interfaces.
The family card is the route-level memory and the default human-readable entry
point for that route. It should summarize:

- direction hypothesis;
- validation requirements;
- sub-probe table;
- cross-probe synthesis;
- blocked branches;
- do-not-repeat list;
- promotion/stop decision.

For long exploratory routes, the active project view should prefer one family
card over many sibling child cards. Child-level detail belongs in the family
card's sub-probe table, merge manifest, and raw links unless the child is a
formal paper evidence item that must remain separately citable.

### 3. Evidence merge / synthesis block

Use when the user asks to combine several experiments, when multiple probes
answer one question, or when a paper/rebuttal needs one clean conclusion from a
messy route.

Default to **visible merge**, not visible duplication:

1. Choose or create one canonical family/synthesis card as the active file.
2. Move superseded child cards out of the active card area into an archive
   location such as `cards/_archive/<canonical_id>/`, or mark them
   `archive_only` if the project already has an archive convention.
3. Preserve traceability in the canonical card through a merge manifest, raw
   file links, and child IDs.
4. Update `EXPERIMENT_INDEX.md` and `EXPERIMENT_INDEX.csv` so default lookup
   points to the canonical card, not every archived child card.

The goal is:

```text
one readable active route file + archived evidence trail
```

Do not keep many active files for one conclusion just because they once existed.
Do not erase evidence metadata. Hide clutter from the active view and keep the
trail in archive/manifest form.

A synthesis block must include:

1. **Combined question**: what shared question these experiments answer.
2. **Included evidence**: child IDs and why each belongs.
3. **Excluded evidence**: related runs not included and why.
4. **Consistent pattern**: what agrees across experiments.
5. **Conflicts / confounds**: what disagrees or is explained by controls.
6. **Supported assumption**: what can be safely said.
7. **Falsified assumption**: what the combined evidence rules out.
8. **Paper role**: main, ablation, diagnostic, internal only, or not used.
9. **Decision**: continue, redirect, reference_only, blocked, or stop.

The canonical card should also include a compact merge manifest:

```markdown
## Merge Manifest / Archived Children

| Old ID | Old path | New status | Why archived | Raw evidence preserved |
|---|---|---|---|---|
| F0xx-D01 | cards/... | archive_only | superseded by family synthesis | yes: runs/... |
```

This lets several experiments be read as one argument without forcing the user
to visually navigate every child file.

## Experiment statuses

- `idea_probe`
- `direction_family`
- `mixed_signal`
- `blocked`
- `candidate`
- `paper_core`
- `paper_ablation`
- `diagnostic`
- `failed_but_informative`
- `deprecated`
- `archive_only`
- `trash_candidate`

## Paper roles

- `core_baseline`
- `main_result`
- `branch_analysis`
- `mechanism_analysis`
- `ablation`
- `external_eval`
- `negative_evidence`
- `diagnostic_only`
- `internal_reference`
- `direction_selection`
- `not_used`

## Keep levels

- `submission_keep`
- `reproduce_keep`
- `cold_archive`
- `delete_large_files`
- `delete_candidate`

## Minimal probe rule

For early ideas, translate the direction layer's validation requirement into
the smallest experiment that can falsify or support the hypothesis. Do not build
a full pipeline unless the probe justifies it.

The experiment card must record the validation requirement, not only the run
configuration. If no validation requirement exists, ask for or create a
direction-level statement before launching the probe.

## Direction-family record rule

A direction-family card should record:

1. hypothesis family and theoretical motivation;
2. canonical sub-probe IDs and any legacy aliases;
3. common constraints and do-not-repeat routes;
4. sub-probe status table;
5. stop/go decisions and blocked branches;
6. what evidence would be required to promote the family to `minimal_probe` or `formal_experiment`;
7. links to sub-index files when present.

Use this when experiments are exploratory, diagnostic, or mutually dependent.

For long exploratory routes, prefer one family card with sub-probe sections over
many isolated active cards. The family card should expose the route logic:

```text
validation requirement -> D00/D01/... -> interpretation -> next problem
```

When a route stops, the family card must explain the reason category, not only
the final metric.

If isolated cards already exist and the user asks to merge/clean the route,
convert them into archived children and make the family card the only active
entry unless a child card is needed as standalone formal paper evidence.

## Stop/go interpretation rule

After each minimal probe, record all of:

- what the result supports;
- what it does not support;
- what assumption it supports or falsifies;
- whether the result is mechanism evidence, metric movement, a confound, or a
  reference/baseline effect;
- whether the next branch is `go`, `pause`, `blocked`, or `stop`;
- the smallest next validation if any;
- the route that should not be repeated without a new hypothesis.

## Formal experiment rule

Formal experiments must record config path, run path, result path, seed, dataset, metrics, status, paper role, tags, related experiments, and keep decision.

## Standard card sections

Use this structure unless an existing card style is already established:

```markdown
# <ID> <Name>

## One-line Summary
## Stage
## Parent Direction / Family
## Validation Requirement
## Research Question
## Tested Assumption
## Hypothesis
## Setup
## Controls
## Key Results
## Interpretation
## Supports
## Does Not Support
## Falsified / Weakened Assumption
## Next Problem / Next Validation
## Paper Usage
## Related Experiments
## Status Decision
## Keep / Archive Decision
## Merge Manifest / Archived Children
## Do-not-repeat
## Tags
## Raw File Links
```

For formal paper evidence, keep `Key Results`, `Setup`, `Paper Usage`, and raw
paths precise. For exploratory diagnostics, make `Tested Assumption`,
`Does Not Support`, and `Next Problem` especially explicit.

## Index row rule

Every card must have matching rows in `EXPERIMENT_INDEX.md` and
`EXPERIMENT_INDEX.csv`.

The index key finding should be one sentence that encodes:

```text
main result + decision + paper role
```

For synthesis/family cards, the key finding should summarize the route decision,
not a single metric.

## No fabrication

Do not create fake results. If `results.csv` or logs are missing, write `not available yet` or `needs verification`.
