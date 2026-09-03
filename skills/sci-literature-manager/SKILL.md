---
name: sci-literature-manager
description: Manage a reusable academic source library independently from project experiment evidence. Use when discovering papers, assigning stable source identities, organizing source packets, maintaining global indexes and reading routes, tracking bibliographic verification and versions, deduplicating sources, or returning a source-grounded handback for project adoption. Use sci-paper-reader for deep reading; leave project tags, LiteratureClaim state, experiment decisions, and evidence promotion to sci-research-manager.
---

# SCI Literature Manager

Make literature discoverable and reusable without mixing it with experiment records. Follow project-local rules and the ownership boundary in `sci-research-manager`.

## Classify the task

- `literature_discovery`: find candidate papers from primary/official sources.
- `literature_indexing`: organize global PDFs, source packets, notes, and indexes.
- `deep_reading`: hand the located source to `sci-paper-reader`.
- `route_synthesis`: return source-grounded options for a project question and competing causes.
- `citation_verification`: verify title, author, venue, year, DOI/arXiv, code, and exact claims.
- `experiment_support`: return verified source material for a literature-to-experiment brief.
- `maintenance`: deduplicate, repair links, or archive superseded notes.

## Retrieve before reading broadly

Read the global library query map/index, then matching collection manifests/cards, then the PDF or official source for exact claims, figures, metrics, or bibliography. If a project supplied a Source ID, use it as the retrieval key; do not edit project tags or claim state as a side effect. Do not batch-read the entire library unless the user asks for a full audit.

## Keep a portable paper packet

Prefer:

```text
<category>/<paper-slug>/
  paper.pdf
  paper_understanding_YYYYMMDD.md
  paper_visual_YYYYMMDD.html
  assets/
  README.md
```

Use library-relative paths and existing conventions. Keep the Markdown understanding artifact canonical; treat HTML/PPT/Word as derivatives. Return source packets and any candidate relevance to `sci-research-manager`; do not embed project state or adoption decisions in global source identity, metadata, or the reusable understanding artifact.

## Maintain verification states

Use clear labels such as:

- `verified`;
- `cached_pdf`;
- `needs_download`;
- `needs_bibliographic_verification`;
- `needs_metric_verification`;
- `paywalled_or_access_limited`.

Do not invent bibliographic fields or exact metrics. Record page/table/figure anchors for numerical claims. Distinguish preprints from accepted publications.

## Build problem-driven reading routes

Use:

`problem -> competing causes -> paper groups -> variables/controls -> evidence limits -> validation implication -> next question`

Do not turn a mature framework or paper module into the project's contribution by default.

## Return a typed source handback

Before an experiment is created, return:

- stable source identities, canonical locations, versions, and bibliographic verification status;
- bounded source claims with exact locations and protocol limits;
- theoretical motivation separated from any proposed project hypothesis;
- variables/cues and required controls;
- success/failure criteria;
- likely confounds and non-transferable assumptions;
- do-not-overclaim/do-not-do-next;
- unresolved identity, access, or citation gaps.

Return this packet to `sci-research-manager`, which owns project adoption, tags, LiteratureClaim verification, experiment allocation, and downstream state. Literature-only items never enter the experiment index or claim map as project evidence.
