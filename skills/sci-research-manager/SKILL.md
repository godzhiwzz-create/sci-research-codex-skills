---
name: sci-research-manager
description: Coordinate evidence-driven academic research across project resumption, direction decisions, literature-to-experiment handoffs, experiment ledgers, result/claim reconciliation, submission readiness, and safe workspace maintenance. Use when Codex must start, resume, organize, maintain, or audit a long-running research project; decide whether to continue, redirect, or stop a research route; create or reconcile README, HANDOFF, SESSION_MEMORY, AGENTS, WIKI, QUERY_MAP, experiment cards, result registries, or claim-evidence maps; trace claims to raw artifacts; protect timestamps and Git worktrees during cleanup; or prepare a durable cross-session handoff. Route specialist paper-reading, manuscript-writing, statistics, figure, and document work to the matching installed skill.
---

# SCI Research Manager

Manage research state and evidence chains. Keep project memory durable, decisions falsifiable, and file operations reversible. Coordinate the other `sci-*` skills without duplicating their specialist work.

## Respect authority and scope

1. Follow the user request and every applicable `AGENTS.md`, `CLAUDE.md`, repository policy, and local template.
2. Never weaken stricter project rules or replace an established schema merely to standardize appearance.
3. Distinguish read-only requests from mutation requests. For inspect, explain, diagnose, or review tasks, do not edit source files unless the user also asks for changes.
4. Ask before deletion, publication, remote access/execution, irreversible migration, or meaningful scope expansion. Treat remote inspection as out of scope for a local/read-only audit unless the user explicitly requests it.
5. Preserve unrelated user changes. Never reset, overwrite, auto-commit, or reformat a dirty worktree as a side effect.

## Start with the lightest safe context

Read in this order, stopping when the task is grounded:

1. Applicable root-to-target `AGENTS.md` files.
2. Root `README.md` and `HANDOFF.md`; read `CLAUDE.md` when present.
3. Target-project `README.md` and `HANDOFF.md`.
4. Relevant `SESSION_MEMORY.md`, `QUERY_MAP.md`, indexes, registries, or decision records.
5. Relevant experiment cards, claim maps, manuscript sections, or literature notes.
6. Raw results, logs, configs, commits, and PDFs only when exact verification requires them.

Before writing, inspect Git/worktree status and identify protected original assets. Avoid broad scans when an index or query map can identify the necessary evidence.

## Classify the task

Assign one lifecycle stage:

`idea_exploration / minimal_probe / formal_experiment / result_analysis / paper_writing / submission_prepare / maintenance`

Then choose one primary operating mode:

| Mode | Deliverable |
|---|---|
| Resume or status | Current question, verified state, uncertainty, blocker, and next action |
| Direction review | Evidence ledger, failed assumption, competing causes, gates, and decision |
| Literature bridge | Source-grounded hypothesis, variables, controls, risks, and experiment-facing brief |
| Experiment lifecycle | Stable ID, frozen protocol, card, provenance, interpretation, and registry update |
| Evidence audit | Conflicts, missing provenance, claim strength, severity, and recommended repair |
| Manuscript/submission coordination | Claim map, evidence readiness, specialist routing, and compliance gaps |
| Workspace maintenance | Navigation repair, ownership map, timestamp/Git protection, validation, and handoff |

Use existing project vocabularies. If none exist, read [research-state-model.md](references/research-state-model.md) and use its compact model without inventing synonyms.

## Apply the evidence hierarchy

Rank evidence from strongest to weakest:

1. Raw artifact plus the exact script/config/commit and frozen protocol.
2. Verified experiment card, reproducibility record, or submission audit.
3. Result registry, project handoff, or claim-evidence map.
4. Session memory, conversation summary, progress note, or old index.
5. Filename inference or recollection.

Never let a weaker source silently overwrite a stronger one. Mark conflicts as `needs_verification` or the project's equivalent, cite both sources, and identify the required arbitration step. Treat literature as motivation or external evidence, never as proof of a project-specific claim.

## Run direction decisions through gates

1. Restate the actual scientific question; do not shrink an architecture-level request into local tuning.
2. Separate observed evidence from inferred cause.
3. Identify the failed assumption and classify likely causes: signal, task, interface, supervision, carrier, target-domain support, or control/confound mismatch.
4. List competing explanations and the cheapest diagnostic that distinguishes them. Prefer no-training or frozen-model diagnostics before new training.
5. State the method principle before naming a module or tool.
6. Define promotion and stop gates before seeing new results.
7. End with exactly one decision: `continue`, `redirect`, `reference_only`, `stop`, or `needs_literature`.
8. Record a `do-not-do-next` list when a route fails. Do not reflexively add epochs, seeds, loss weights, heads, gates, or a stronger carrier without a new causal hypothesis.

## Keep experiment evidence auditable

1. Preserve existing IDs and naming conventions. Never renumber historical experiments for neatness.
2. Before a run, freeze the hypothesis, competing explanation, dataset/split, seeds, metric definition, baseline, checkpoint/threshold/method selection rule, config, run/result path, code commit, success gate, and stop gate.
3. Flag test-set selection, cross-script metric transfer, mixed protocols, missing seeds, and unverifiable raw paths. Do not promote them into a main claim.
4. After a result, state separately: what it supports, what it does not support, the weakened/falsified assumption, evidence status, paper role, and next decision.
5. Close the chain in the project's established order. Prefer:

   `raw result -> experiment card -> project index -> shared registry -> project HANDOFF`

6. Use family/synthesis cards only when several probes answer one question. Keep one readable active synthesis while preserving child IDs and raw evidence in an archive manifest.
7. Never invent missing numbers or infer results from filenames. Use `needs_verification`.

Read [artifact-contracts.md](references/artifact-contracts.md) before creating or materially restructuring lifecycle documents. Use `sci-experiment-manager` for card/index implementation and `sci-result-auditor` for consistency audits.

## Calibrate claims and submissions

Classify each important claim as:

`main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported`

Require every paper-facing claim to resolve to verified evidence and a compatible protocol. Keep exploratory evidence out of contribution language. Before submission, reconcile manuscript, figures/tables, result files, public code, data/code statements, and official venue requirements. Verify current official venue sources; never guess formatting or policy.

Use `sci-paper-manager` for claim/submission artifacts, `sci-literature-manager` and `sci-paper-reader` for literature, `academic-manuscript-writing` for prose, and [specialist-routing.md](references/specialist-routing.md) for optional installed skills outside this repository.

## Maintain files without destroying provenance

1. Prefer a navigation layer—`README`, `HANDOFF`, `WIKI`, indexes, and manifests—over moving original research assets.
2. Preserve original paper, result, log, checkpoint, source, and historical-decision modification times. Do not `touch`, bulk rewrite, or re-export them for cosmetic consistency.
3. Before an approved physical migration, record old path, modification time, size, optional hash, destination, reason, and rollback mapping. Prefer same-volume moves.
4. Never move Git worktrees, submission packages, public repositories, or path-coupled runs without explicit approval and a rollback plan.
5. Treat deletion as a separate user-authorized action. First produce a review manifest with ownership, evidence risk, replacement, and recommendation.
6. Update durable memory only when the underlying state actually changed. Keep session-derived facts explicitly below artifact-verified facts.

Use `scripts/provenance_guard.py` before and after path-sensitive moves. Use `scripts/audit_workspace.py` for read-only navigation, symlink, required-entrypoint, and Git-state checks. Read [audit-checklists.md](references/audit-checklists.md) for the applicable closeout checklist and use `sci-asset-manager` for archive/delete reviews.

## Close the task

1. Validate only what the task changed, then broaden checks in proportion to risk.
2. Recheck links, symlinks, Git/worktree state, protected timestamps, evidence registration, and unresolved protocol conflicts.
3. Update `HANDOFF` when stage, central question, verified evidence, blocker, ownership, or next action changed. Do not update it merely to record cosmetic edits.
4. Report the outcome first, followed by verified evidence, files changed, checks run, unresolved items, and the safest next action.
5. Never claim completion while required evidence or a known blocker remains hidden.
