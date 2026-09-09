# Integrated Research Library Workflow

Use this workflow when a task crosses project literature, experiment evidence, and manuscript claims. For literature-only work, read [project-literature-interface.md](project-literature-interface.md). For experiment-only work, read [experiment-library-lifecycle.md](experiment-library-lifecycle.md). Preserve an established project schema when it is stricter.

## Core contract

Give each fact one owner and make every other document a link or view:

| Fact | Canonical owner | Other documents may do |
|---|---|---|
| Physical literature inventory, Source ID, metadata, version, alias, and duplicate relation | `sci-literature-manager` or a narrower installed specialist and its global manifest | Project views link by stable Source ID |
| Project/question relevance | `projects/<project>/literature` query map and Source-ID registry | Link to the project source note |
| Verified external claim | Project `LITERATURE_CLAIMS.tsv` row + exact note | Reuse at equal or narrower scope |
| Experiment protocol and interpretation | Experiment card | Link and state evidence status |
| Numerical result | Raw artifact plus exact extraction script/config/commit | Display a generated value, never become a second source |
| Experiment current five-axis state | Project `EXPERIMENTS.tsv` | Route to the historical/scientific card |
| Cross-session canonical evidence | `RESULTS_REGISTRY.tsv` row pointing to the card/raw source | Route retrieval; do not duplicate the card |
| Current project state | Project handoff | Link to evidence, not store result diaries |
| Paper-facing statement | Claim-evidence map | Feed the manuscript at the verified scope |

Historical global indexes are snapshots. Do not keep their counts, statuses, or project stories synchronized with current project views; label them historical and point to the external library manifest and project query map.

## Select the minimum workflow

| Request | Load and apply |
|---|---|
| Add/tag/query/verify a paper inside a project | `project-literature-interface.md` |
| Search, identify, deduplicate, version, or export bibliography globally | `sci-literature-manager` or a narrower installed literature specialist |
| Design/register/run/analyze/promote/supersede an experiment | `experiment-library-lifecycle.md` |
| An experiment proposal is accepted for execution | Both references plus the existing literature-to-experiment brief/card |
| Evidence enters or changes a manuscript claim | Experiment reference plus claim-evidence map; project literature reference when an external claim is involved |
| Structural maintenance/audit | Both references, but inspect only the flagged owner and downstream consumers |

## Choose the operation before writing

### Retrieve

Read only. Start from the project/question view, then the source note or experiment card, and open the PDF/raw artifact only when exact verification is required. Do not edit indexes as a side effect of answering a question.

### Intake a literature source

Apply [project-literature-interface.md](project-literature-interface.md). The global specialist completes identity/metadata work; the project consumes only the stable Source ID and project semantics.

### Verify a literature claim

Create or update a `LITERATURE_CLAIMS.tsv` row plus project note with Source ID, exact location, protocol boundary, allowed wording, prohibited extrapolation, and downstream experiment/claim links. Global bibliographic fields remain owned by the literature specialist. Reading depth remains in `SOURCES.tsv`; only the individual LiteratureClaim becomes `claim_verified`.

### Bridge literature to an experiment

Apply [literature-decision-check.md](literature-decision-check.md) for novelty, feasibility, or investment decisions before proposal-specific preparation. Reuse a still-applicable comparison. During discussion, keep the bounded comparison in the answer; do not automatically create a brief or experiment ID.

For an accepted experiment, use a compact section of the existing brief/card before allocating an ID. Separate the paper's evidence from the project's hypothesis and state variables, controls, confounds, success/failure criteria, transferable elements, consequential protocol differences, and the cheapest informative validation. A decision is accepted only through user selection or a pre-authorized workflow's gate, not specialist preference.

### Design or run an experiment

Apply [experiment-library-lifecycle.md](experiment-library-lifecycle.md). Create the stable card and freeze the protocol before execution. During a run, update only the run/card state needed for safe resumption.

### Analyze and promote evidence

Follow the experiment state transitions and promotion gate. Update the project query route after analysis; update the shared registry only for canonical evidence; update the project handoff only when current project state changes.

An experiment may be complete without being paper-facing. Keep experiment status, evidence status, claim strength, and direction decision in separate fields.

### Hand evidence to manuscript writing

Provide a bounded evidence packet:

- claim ID, exact allowed wording, and claim strength;
- canonical experiment card and raw artifact/extraction source;
- verified literature note and exact source location for external claims;
- compatible protocol, contrary evidence, and required limitations;
- frozen table/figure generator or source;
- unresolved gaps marked `needs_verification`.

The manuscript-writing stage owns prose and revision scope. The research library owns evidence. A new or broadened manuscript claim returns to evidence verification; manuscript wording must not silently promote an experiment or source. English and Chinese manuscripts share the same claim IDs, values, and evidence packet.

### Audit or maintain

Run structural checks first, then inspect only flagged items. Check physical inventory against the catalog, current views against canonical owners, registry links, project namespace links, status vocabulary, and stale duplicated facts. Repair navigation and current-state views; do not rewrite original PDFs, raw results, logs, checkpoints, or historical records for cosmetic consistency.

## Minimum writes by event

| Event | Required writes | Conditional writes |
|---|---|---|
| New PDF/source | External literature specialist intake/metadata/dedup/global catalog | Project Source-ID row only if the project adopts it; note only beyond screening |
| Claim verification | LiteratureClaim row + exact note | Claim map/BibTeX if entering a manuscript |
| Experiment proposal accepted | Existing brief/card gains the bounded comparison and falsifiable requirement | Experiment ID/card when execution enters scope |
| Experiment designed | Experiment card + project `EXPERIMENTS.tsv`/query route | Handoff if it becomes the active project action |
| Run completes | Raw artifact + card + project `EXPERIMENTS.tsv` | Registry/claim map only after promotion |
| Evidence is superseded | Card/index replacement link | Registry and handoff if the canonical route changes |
| Manuscript consumes evidence | Claim-evidence map/evidence packet | No library mutation when prose merely restates verified evidence |
| Routine audit | Bounded findings in the response; repair only when authorized | Durable report when requested/required; handoff only for a real blocker or route change |

## Completion gates

- A source is available to a project when the external library has assigned a stable Source ID and the project has a tagged view; it is usable for a detailed external claim only when exact support and protocol boundary are recorded in a project note.
- An experiment is retrievable when its stable ID, card, project route, and raw provenance are linked.
- Evidence is promotable when raw artifact, protocol, extraction method, status, and claim strength agree.
- A manuscript handoff is ready when every paper-facing claim resolves to compatible internal evidence or a verified external source, and all gaps are explicit.
- Maintenance is complete when current entry points agree without forcing historical snapshots to mirror the present.
