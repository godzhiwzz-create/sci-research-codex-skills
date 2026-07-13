---
name: sci-experiment-manager
description: Manage experiment evidence for long-running academic research with stable E/F identifiers, frozen protocols, experiment and family cards, low-token indexes, raw-result provenance, synthesis, and safe generated outputs. Use when creating, updating, combining, indexing, retrieving, or closing experiments and diagnostic probes. Defer route-level continue/redirect/stop decisions to sci-research-manager and pure cross-artifact audits to sci-result-auditor.
---

# SCI Experiment Manager

Maintain the chain:

`validation requirement -> experiment/probe -> raw result -> interpretation -> claim role -> next decision`

Follow project-local instructions and the lifecycle/evidence rules in `sci-research-manager`.

## Retrieve evidence efficiently

Read the project's equivalents of:

1. `HANDOFF.md` or `PROJECT_HANDOFF.md`.
2. `QUERY_MAP.md`.
3. Experiment index/registry.
4. Relevant cards.
5. Raw files only for exact verification.

Do not globally scan runs, logs, results, or weights when an index can narrow the task.
Do not connect to remote hosts during a local/read-only audit unless the user explicitly requests remote verification; mark remote-only artifacts unavailable instead.

## Preserve stable identifiers

- Use the project's established convention.
- Use `E001`, `E002`, ... for formal or standalone experiments when no convention exists.
- Use `F012` for a direction family and `F012-D01` for a diagnostic inside it.
- Never renumber historical records for appearance.
- Keep aliases and archived child IDs in the canonical family card.

## Freeze the protocol before execution

Record:

- question, hypothesis, competing explanation, and validation requirement;
- dataset/version, split, seeds, model/checkpoint, baseline, and controls;
- metric definition and aggregation;
- checkpoint/threshold/method-selection rule;
- config, command/run path, result path, and code commit;
- promotion gate, stop gate, and do-not-do-next.

Flag test-set selection, mixed protocols, missing seeds, or unverifiable paths. Do not promote unsafe evidence into a main claim.

## Use three record levels

### Single experiment card

Record one run, diagnostic, smoke test, or formal evidence item. Use [experiment_card_template.md](templates/experiment_card_template.md) when the project has no template.

### Direction family card

Summarize one research question across several probes: shared hypothesis, validation requirements, child table, synthesis, conflicts/confounds, blocked branches, promotion/stop decision, do-not-repeat list, and raw links.

### Evidence synthesis

When several records support one conclusion, keep one readable active family/synthesis card and archive redundant child cards without deleting their IDs or raw evidence. Include a merge manifest with old ID/path, new status, reason, and preservation proof.

## Interpret results conservatively

After each result, state separately:

1. `supports`;
2. `does_not_support`;
3. weakened/falsified assumption;
4. confounds and protocol warnings;
5. evidence status;
6. paper role/claim strength;
7. next decision and smallest justified validation.

Never infer metrics from filenames or conversation. Use `not available` or `needs_verification`.

## Maintain indexes with generated outputs

- Use `scripts/generate_experiment_card.py` to create a non-overwriting E/F card.
- Use `scripts/update_experiment_index.py` to generate reviewable Markdown and CSV indexes. Do not overwrite hand-edited indexes automatically.
- Use `scripts/collect_results.py` only when explicit result collection is needed. Review the generated table before treating it as evidence.
- Run scripts with `--help` and prefer explicit `--root`, directory, and output arguments in nonstandard projects.

After verified results change, update the project's established chain, preferably:

`raw result -> card -> project index -> shared registry -> HANDOFF`

Use `sci-result-auditor` before paper promotion or when artifacts disagree.
