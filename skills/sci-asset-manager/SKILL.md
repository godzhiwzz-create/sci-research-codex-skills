---
name: sci-asset-manager
description: Manage research project assets for long-term SCI paper work, including experiment archives, cleanup candidates, submission keep lists, and cold archive manifests while preserving evidence metadata. Use when deciding what to keep, archive, or delete in an experiment-driven research workspace.
---

# sci-asset-manager

## Purpose

Manage experiment archives, old paper versions, cleanup candidates, submission keep lists, and cold archive manifests without losing evidence metadata.

## Startup rule

First classify the task stage and read:

1. `PROJECT_HANDOFF.md`
2. `research_workspace/experiments/EXPERIMENT_INDEX.md`
3. relevant experiment cards
4. `research_workspace/paper/CLAIM_EVIDENCE_MAP.md`

Use lightweight indexes before raw file inspection.

## Context discipline policy

- Start from `EXPERIMENT_INDEX.csv` keep levels and experiment cards.
- Do not scan full checkpoint or log directories during ordinary planning.
- Scanning large artifact directories is acceptable when estimating cleanup candidates or preparing archive manifests.
- For cleanup review, list candidate paths from known run paths first.
- Never open large binary weights.
- Generate review manifests instead of reading large artifacts.

## Core rule

Never delete experiment metadata.

May clean:
- large checkpoints
- cache
- duplicate logs
- temporary outputs
- failed intermediate weights

Must preserve:
- experiment card
- config
- result summary
- run command
- archive note
- claim evidence relation if any

## Archive review nodes

1. after `idea_probe`
2. after each phase
3. after central story is fixed
4. after `draft_core` is complete
5. before submission

## Delete rule

Codex must never directly delete files unless explicitly instructed by the user.

It must first create `delete_review.md` with:
- file path
- reason
- related experiment ID
- whether metadata is preserved
- risk
- recommended action

## No fabrication

Do not invent archive decisions or claim relations. Mark uncertain file ownership as `needs verification`.
