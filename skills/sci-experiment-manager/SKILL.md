---
name: sci-experiment-manager
description: Manage experiment records for SCI research projects with low-token retrieval, stable experiment IDs, experiment cards, lightweight indexes, result paths, keep levels, and no-fabrication rules. Use when creating, updating, indexing, auditing, or retrieving experiment evidence.
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

Every experiment must have a stable ID:

`E001`, `E002`, `E003`, ...

Experiment ID must not change after creation.

## Experiment statuses

- `idea_probe`
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
- `not_used`

## Keep levels

- `submission_keep`
- `reproduce_keep`
- `cold_archive`
- `delete_large_files`
- `delete_candidate`

## Minimal probe rule

For early ideas, design the smallest experiment that can falsify or support the hypothesis. Do not build a full pipeline unless the probe justifies it.

## Formal experiment rule

Formal experiments must record config path, run path, result path, seed, dataset, metrics, status, paper role, tags, related experiments, and keep decision.

## No fabrication

Do not create fake results. If `results.csv` or logs are missing, write `not available yet` or `needs verification`.
