---
name: sci-literature-manager
description: Manage research-paper libraries for SCI-style academic projects independently from experiment records. Use when searching papers, organizing literature folders, creating paper indexes, reading-route maps, paper cards, source-verification queues, or experiment-facing literature briefs. Keeps literature assets separate from experiment evidence while making papers callable by later experiment design.
---

# sci-literature-manager

## Core Principle

The literature layer is not an experiment archive.
It answers:

- what papers exist and where they are stored;
- what problem each paper helps explain;
- which variables, controls, and failure modes the paper suggests;
- which claims still need source verification;
- how experiments should call papers without turning literature into evidence.

Experiment evidence belongs to `sci-experiment-manager`.
Paper claims belong to `sci-paper-manager`.
Deep reading and paper-to-project synthesis belong to `sci-paper-reader`.

## Stage Detection

Classify the task first:

- `literature_discovery`: find new papers from web or local library.
- `literature_indexing`: organize paper folders, indexes, cards, PDFs.
- `deep_reading`: read one or more papers and extract mechanisms.
- `route_synthesis`: turn papers into a research direction or diagnostic plan.
- `citation_verification`: verify title, venue, DOI/arXiv/source, metrics.
- `experiment_support`: produce an experiment-facing literature brief.
- `maintenance`: cleanup, deduplication, archive, skill/index repair.

If the user asks to understand a paper, extract its argument, compare multiple
papers, or turn a paper into a project-facing mechanism route, use
`sci-paper-reader` after locating the source in this literature layer.

## Retrieval Order

For a project with a `research_workspace/literature/` folder, read:

1. `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_QUERY_MAP.md`
2. `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_INDEX.md`
3. matching collection index or manifest
4. relevant paper cards / reading route files
5. PDF or official web source only for exact claims, figures, metrics, or
   bibliographic verification

Do not start with experiment indexes unless the user asks to connect papers to
project evidence or design an experiment.

## Output Types

### 0. Canonical paper folder

Use this folder layout for paper understanding assets:

```text
<paper_category>/<paper_title_slug>/
  <paper_title_slug>.pdf
  <paper_title_slug>_understanding_<YYYYMMDD>.md
  <paper_title_slug>_visual_<YYYYMMDD>.html
  assets/
  README.md
```

The category should describe the paper's general literature role, not only the
current experiment.  Examples: `visibility_physics`, `depth_geometry_proxy`,
`quality_alignment`, `domain_factorization`.

The Markdown understanding packet is the source artifact.  HTML/PPT/Word files
are derivatives and should follow the Markdown argument route.  Project-specific
interpretation should be appended at the end with a date, so future projects can
reuse the paper without inheriting today's project lens.

### 1. Literature seed manifest

Use when opening a new research route.

Must include:

- stage;
- research problem;
- paper table with title, venue/year, source, role, priority, status;
- reading priority;
- how paper groups map to project variables;
- verification queue;
- do-not-overclaim notes.

### 2. Reading route

Use when the user needs papers to solve a problem, not just a bibliography.

Organize as:

```text
problem -> cause -> paper group -> what to extract
-> validation implication -> next question
```

### 3. Paper card

Use one card per important paper.

Minimum schema:

```markdown
# Paper Title

## Source
- URL:
- PDF:
- Verification status:

## Problem
## Core mechanism
## What this paper suggests for our project
## Variables / controls to extract
## Evidence or figures to inspect
## Risks / confounds
## Project role
```

Mark missing bibliographic details as `needs verification`.

### 4. Experiment-facing literature brief

Use when an experiment is about to be designed.

Must include:

1. theoretical motivation;
2. variables/cues to measure;
3. required controls;
4. success criteria;
5. failure criteria;
6. likely confounds;
7. source papers and verification status.

Then hand off actual experiment IDs, cards, configs, runs, and result paths to
`sci-experiment-manager`.

For deep reading, use `sci-paper-reader` to create the brief.  This skill
should only manage where the paper lives and how it is indexed.

## Verification Rules

- Do not invent paper titles, arXiv IDs, DOIs, venues, authors, metrics, or
  code links.
- For new or unstable papers, verify with official sources or primary pages.
- Use labels:
  - `verified`
  - `cached_pdf`
  - `needs_download`
  - `needs_bibliographic_verification`
  - `needs_metric_verification`
  - `paywalled_or_access_limited`
- Do not cite exact metrics from a card unless the card records page/table or
  source-line evidence.

## Literature vs Experiment Boundary

Never add a literature-only item to:

- `research_workspace/experiments/EXPERIMENT_INDEX.md`
- `research_workspace/experiments/EXPERIMENT_INDEX.csv`

Only experiments/probes get experiment IDs.  Literature may propose validation
requirements, but it must not create run paths or result claims.

## Maintenance Rules

When adding or reorganizing literature assets, update only relevant lightweight
literature files:

- `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_QUERY_MAP.md`
- `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_INDEX.md`
- `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_INDEX.csv`
- collection-specific manifests/indexes
- `research_workspace/README.md` or `PROJECT_HANDOFF.md` only for major route
  changes

Cleanup sidecars such as `.DS_Store` and `._*` when organizing the library.

## Optional Defaults For Projects With A Literature Layer

If a project follows a bilingual or indexed literature layout, useful relative
entry points may include:

- `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_QUERY_MAP.md`
- `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_INDEX.md`
- `research_workspace/literature/方法速查卡_Method_Cards/METHOD_CARD_INDEX.md`
- `research_workspace/literature/方法速查卡_Method_Cards/READING_PRIORITY.md`
- `research_workspace/literature/研究路线与综合_Research_Routes_and_Synthesis/<route_name>/`

For paper-to-PPT work, use:

```text
deckforge-paper2ppt
```

For project-facing paper reading, use:

```text
sci-paper-reader
```

## Do Not

- Do not turn a mature framework paper into the user's contribution by default.
- Do not use literature to override negative experiment evidence.
- Do not batch-read the whole library unless the user asks for a full audit.
- Do not silently treat arXiv/preprints as accepted venues.
- Do not store private/paywalled PDFs without explicit approval.
- Do not make experiment claims from literature summaries.
