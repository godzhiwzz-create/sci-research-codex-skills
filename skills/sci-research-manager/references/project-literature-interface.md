# Project Literature Interface

Read this reference when a task adds, retrieves, tags, verifies, audits, or hands off literature inside a research project. It governs the project-facing view only. Global PDF identity, metadata, version relations, deduplication, and bibliography remain owned by `sci-literature-manager` or a narrower installed literature specialist.

## Interface boundary

```text
`sci-literature-manager` or narrower literature specialist
  -> stable Source ID + canonical source/metadata status + explicit alias/version relation
  -> projects/<project>/literature/SOURCES.tsv
  -> generated INDEX + curated QUERY_MAP
  -> projects/<project>/literature/LITERATURE_CLAIMS.tsv
  -> project note for each exact verified claim
  -> experiment brief or manuscript evidence packet
```

The project records why and how a source is used. It must not become a second bibliographic database.

## Canonical project artifacts

| Artifact | Ownership | Mutation rule |
|---|---|---|
| `SOURCES.tsv` | Machine-readable project source registry | Canonical editable source for project literature semantics |
| `LITERATURE_CLAIMS.tsv` | Machine-readable exact-claim registry | Canonical verification/link state for source-backed project claims |
| `INDEX.md` | Human-readable generated view | Regenerate; do not hand-edit factual rows |
| `QUERY_MAP.md` | Research question/tag routing | Curate only when a source set or question route changes |
| `notes/` | Exact project-specific evidence and protocol boundaries | Create only after a source enters a claim, experiment, or decision |
| Global `SOURCE_INDEX.tsv` | Source identity, canonical PDF and metadata state | Read through Source ID; never copy its fields into the project registry |
| Global `SOURCE_ALIASES.tsv` | Version/duplicate/replacement relation between Source IDs | Owned by the literature specialist; never infer it in a project |

When a project already has stricter names or schemas, preserve them and record the mapping in its README rather than moving historical assets.

## `SOURCES.tsv` minimum schema

| Field | Requirement |
|---|---|
| `source_id` | Required stable ID issued by the global library; unique within the project |
| `tags` | Required comma-separated lowercase retrieval terms; describe topic/protocol, not conclusions |
| `project_role` | Required stable project role such as background, baseline candidate, implementation source, competing explanation, or historical reference |
| `reading_depth` | Required access depth: `metadata_only / abstract_checked / full_read` |
| `note` | Optional general project-relative reading note; exact claim verification belongs in `LITERATURE_CLAIMS.tsv` |
| `experiments` | Optional stable experiment IDs or links; never raw result values |
| `claims` | Optional claim IDs; never free-form manuscript prose |

Reading depth is an evidence-access state, not a quality score:

`metadata_only -> abstract_checked -> full_read`

Do not encode `claim_verified` in `SOURCES.tsv`: reading a paper and verifying a particular claim are different axes. Use `LITERATURE_CLAIMS.tsv` for the latter. If legacy input still has `reading_status`, read it compatibly, but migrate the header to `reading_depth` before new writes.

## `LITERATURE_CLAIMS.tsv` minimum schema

| Field | Requirement |
|---|---|
| `literature_claim_id` | Stable project-local ID, unique within the project |
| `source_id` | Stable global Source ID |
| `verification_status` | `needs_verification / claim_verified / contradicted / superseded` |
| `note_path` | Required project-relative note containing exact location and scope |
| `experiments` | Optional downstream experiment IDs |
| `manuscript_claims` | Optional downstream manuscript claim IDs |
| `verified_at` | ISO date/time when verification was last checked; empty unless verified |

One row verifies one bounded claim, not a paper. A `claim_verified` row requires a resolvable note and exact location. `contradicted` and `superseded` remain retrievable and are never silently deleted.

## Operations

### Retrieve

Start from `QUERY_MAP.md`, query `SOURCES.tsv`, then open the project note. Resolve the global PDF or formal source only when the question requires exact text, methods, numbers, or citation identity. Retrieval is read-only; do not improve tags or statuses as an incidental side effect.

### Adopt a newly collected source

1. Route the PDF/identifier to the literature-management specialist.
2. Wait for a stable Source ID or an explicit unresolved identity state.
3. Add one `SOURCES.tsv` row with tags, role, and honest reading depth.
4. Regenerate `INDEX.md` and add a `QUERY_MAP.md` route only when it improves retrieval.
5. Stop unless the task also requires claim verification, an experiment brief, or a manuscript citation.

Do not copy the PDF, title, authors, venue, DOI, arXiv metadata, BibTeX, or version history into the project directory.

### Verify a claim

The project note must record:

- Source ID and source version used;
- exact page, section, table, figure, or quoted fragment location;
- the supported statement in bounded wording;
- protocol/population/task/metric boundary;
- prohibited extrapolations and contradictory evidence;
- downstream experiment and claim IDs;
- verification date.

Only then create or promote the matching `LITERATURE_CLAIMS.tsv` row to `claim_verified`. If the global library later changes the canonical version, the global specialist records the relation in `SOURCE_ALIASES.tsv`; recheck version-sensitive claims before keeping their verified status.

### Exclude or replace

Do not delete a source row that already feeds an experiment, claim, response, or historical decision. Remove it from active query routes, record the reason and replacement in a note or decision record, and preserve its Source ID links. A metadata correction alone must not silently change project interpretation.

## Outputs to other lifecycle modes

- To experiment design: a literature-to-experiment brief that separates external evidence from the project hypothesis.
- To manuscript writing: LiteratureClaim ID, Source ID, exact verified statement/location, protocol boundary, allowed wording, manuscript claim ID, and bibliography resolution status.
- To maintenance: registry/schema errors, unknown Source IDs, stale generated views, unresolved aliases, or `claim_verified` rows without notes.

## Completion gates

- Intake is complete when the Source ID resolves globally and the project row is valid and retrievable.
- Claim verification is complete only when exact support and scope are recorded in a note and a valid `LITERATURE_CLAIMS.tsv` row points to it.
- A project literature view is healthy when Source IDs are unique/resolvable, reading depths are valid, claim rows resolve, `INDEX.md` reflects `SOURCES.tsv`, query routes resolve, and no global bibliographic facts are duplicated as project-owned data.
