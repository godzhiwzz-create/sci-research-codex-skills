# Lifecycle Artifact Contracts

Follow established local templates first. Use these contracts only to fill missing structure or audit responsibility boundaries.

## Contents

- Document responsibilities
- Handoff minimum
- Experiment card minimum
- Result registry minimum
- Claim-evidence entry minimum
- Literature-to-experiment brief
- Migration/archive manifest minimum

## Document responsibilities

| Artifact | Owns | Must not become |
|---|---|---|
| `README.md` | Directory purpose, entry points, ownership, boundaries | A result diary |
| `HANDOFF.md` | Current stage/state, verified evidence, blocker, next actions, execution/Git state | Permanent storage for every historical detail |
| `SESSION_MEMORY.md` | Stable cross-session decisions, corrections, and red lines | A substitute for raw evidence |
| `AGENTS.md` | Agent behavior, read/write boundaries, required checks | A changing experiment ledger |
| `WIKI.md` / `QUERY_MAP.md` | Problem-to-artifact retrieval map | An authoritative result source |
| Experiment card | Hypothesis, frozen protocol, result, interpretation, provenance | A literature note or unverified headline |
| Result registry | Canonical card/result path and evidence status across projects | A duplicate experiment card |
| Claim-evidence map | Claim strength and exact supporting evidence | Free-form manuscript prose |
| Archive/migration manifest | Old/new path, reason, evidence risk, replacement, preservation proof | Permission to delete |

## Handoff minimum

Record project status and task stage; central question; canonical route; verified evidence and source links; unverified/conflicting evidence; active work and owners; blockers and do-not-do-next items; prioritized next actions with gates; Git/remote state; and update date. Keep detailed metrics in cards/registries and link to them.

## Experiment card minimum

Record:

- Stable ID, name, parent family, stage, and status.
- Scientific question, hypothesis, competing explanation, and validation requirement.
- Frozen protocol: dataset/version, split, seeds, metric definition, baseline, model/checkpoint, threshold/method selection rule, config, command/run path, result path, and code commit.
- Controls, promotion gate, and stop gate declared before the result.
- Raw result plus extraction/aggregation method.
- `supports`, `does_not_support`, weakened/falsified assumption, and confounds.
- Evidence status, claim strength/paper role, and next decision.
- Related experiments, archived children, do-not-repeat conditions, and provenance links.

Never backfill a missing field by guessing. Use `not available` or `needs_verification`.

## Result registry minimum

Use one row per canonical evidence item: project, stable ID, question, canonical card, raw result, protocol/commit, lifecycle status, evidence status, claim role, selection warning, and last verification date.

## Claim-evidence entry minimum

Record claim ID and exact wording, claim strength, supporting experiment/result IDs, protocol compatibility, contrary evidence, allowed manuscript location, missing evidence, and verification owner/date. Do not let one metric row support a broader causal/generalization claim than its protocol permits.

## Literature-to-experiment brief

Record source identity and verification status; the paper's problem, mechanism, and evidence boundary; project-facing hypothesis; variables/cues; controls; confounds; success/failure criteria; transferable and non-transferable parts; and recommended lifecycle stage. Create an experiment ID only after the brief yields a concrete validation requirement.

## Migration/archive manifest minimum

Record old path, new path, owner/project, related experiment/claim IDs, original modification time, size, optional hash, migration date, reason, replacement/canonical entry, rollback step, and evidence-preservation status. Keep deletion as a later explicit decision.
