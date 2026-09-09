# Lifecycle Artifact Contracts

Follow established local templates first. Use these contracts only to fill missing structure or audit responsibility boundaries.

## Contents

- Document responsibilities
- Handoff minimum
- Experiment card minimum
- Project literature registry and note minimum
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
| Project `literature/SOURCES.tsv` | Source ID, project tags/role/reading depth, and downstream IDs | A second global bibliography, claim-verification table, or PDF inventory |
| Project `literature/LITERATURE_CLAIMS.tsv` | Exact external-claim verification state and links | Whole-paper verification or free-form prose |
| Project literature note | Exact verified external claim/location and protocol boundary | A general paper summary or project result source |
| Experiment card | Hypothesis, frozen protocol, result, interpretation, provenance | A literature note or unverified headline |
| Project `EXPERIMENTS.tsv` | Current five-axis state and canonical pointers | Historical scientific narrative or raw numbers |
| Legacy `EXPERIMENT_INDEX.csv/.md` | Compatibility import or generated retrieval view | A second editable current-state authority |
| `RESULTS_REGISTRY.tsv` | Promoted canonical card/result path, reason and evidence status across projects | A duplicate experiment card |
| `RESULTS_REGISTRY.md` | Generated human view of the TSV | An independently edited authority |
| Claim-evidence map | Claim strength and exact supporting evidence | Free-form manuscript prose |
| Archive/migration manifest | Old/new path, reason, evidence risk, replacement, preservation proof | Permission to delete |

## Handoff minimum

Record:

1. Project status and task stage.
2. Central scientific question or maintenance objective.
3. Current canonical route/story.
4. Verified evidence and exact source links.
5. Unverified/session-only/conflicting evidence.
6. Active experiments or work items with owners/locations.
7. Blockers, risks, and do-not-do-next items.
8. Next actions in priority order with completion gates.
9. Git/worktree/remote execution state when relevant.
10. Update date; do not rewrite historical asset dates.

Keep large tables and detailed metrics in cards or registries and link to them.

## Experiment card minimum

Record:

- Stable ID, name, parent family, stage, and status.
- Scientific question, hypothesis, competing explanation, and validation requirement.
- Frozen protocol: dataset/version, split, seeds, metric definition, baseline, model/checkpoint, threshold/method selection rule, config, command/run path, result path, and code commit.
- Controls and fairness constraints.
- Promotion gate and stop gate declared before the result.
- Raw result plus extraction/aggregation method.
- Execution exit state, completed/partial run boundary, and uncertainty source/unit of analysis.
- `supports`, `does_not_support`, weakened/falsified assumption, and confounds.
- Evidence status, claim strength, optional manuscript placement, and next decision.
- Related experiments, archived children, and do-not-repeat conditions.
- Provenance links and missing-artifact markers.

Never backfill a missing field by guessing. Use `not available` or `needs_verification`.

## Project literature registry and note minimum

`SOURCES.tsv` must contain unique resolvable Source IDs plus project tags, role, reading depth, optional general note path, experiment IDs, and claim IDs. It must not duplicate title, authors, venue, DOI, BibTeX, global PDF path ownership, version relations, or exact claim-verification state.

A `claim_verified` LiteratureClaim row and note record the Source ID/version, exact page/section/table/figure, bounded supported wording, protocol/task/population/metric boundary, prohibited extrapolations, contradictory evidence, downstream experiment/claim IDs, and verification date. If any are unavailable, keep that claim `needs_verification`; do not lower or inflate the source's independent reading depth to encode it.

## Result registry minimum

Use one row per canonical evidence item. Field values use the exact canonical tokens from [research-state-model.md](research-state-model.md):

| Field | Meaning |
|---|---|
| `evidence_id` | Unique stable registry ID |
| `project` | Owning research project |
| `experiment_id` | Stable experiment/family ID |
| `question` | One-line validation target |
| `canonical_card` | Single default human entry point |
| `raw_result` | Exact authoritative artifact |
| `protocol_anchor` | Frozen protocol/code/config reproduction anchor |
| `experiment_status` | `designed / running / partial / complete / stopped / superseded` |
| `evidence_status` | `not_assessed / verified / pending_artifact / protocol_mismatch / unverifiable` |
| `claim_strength` | `main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported` |
| `selection_warning` | Test selection, mixed protocol, or `none` |
| `promotion_reason` | Why this item belongs in the shared canonical registry |
| `last_verified` | Verification date, not inferred experiment date |

The registry may only point to evidence already closed in the project card/raw chain. Completion alone is not promotion.

For a new project, prefer `EXPERIMENTS.tsv` as the editable current-state source. When an existing project uses `EXPERIMENT_INDEX.csv` or Markdown, preserve it and document the mapping; if both formats exist, designate exactly one editable authority and generate the others as views.

## Claim-evidence entry minimum

Record:

- Claim ID and exact wording.
- Claim strength.
- Supporting experiment/card/result IDs.
- Protocol compatibility.
- Contrary or limiting evidence.
- Allowed manuscript location.
- Required missing evidence.
- Verification owner/date.

Do not let one metric row support a broader causal or generalization claim than its protocol permits.

## Literature-to-experiment brief

Record:

- Source identity and verification status.
- Paper's problem, mechanism, and evidence boundary.
- Project-facing hypothesis; mark it as a hypothesis, not evidence.
- Variables/cues, controls, confounds, success criterion, and failure criterion.
- What is transferable and what is not.
- Recommended lifecycle stage.

Reuse a compact section of the existing brief/card. Allocate an experiment ID only for an accepted, authorized experiment with a concrete validation requirement; ordinary discussion stays in the response. New-method or investment decisions also need a traceable nearest-prior comparison, not an extra parallel registry.

## Migration/archive manifest minimum

Record old path, new path, owner/project, related experiment/claim IDs, original modification time, size, optional hash, migration date, reason, replacement/canonical entry, rollback step, and evidence preservation status. Keep deletion as a later explicit decision.
