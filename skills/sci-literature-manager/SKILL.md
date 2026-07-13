---
name: sci-literature-manager
description: Manage an academic paper library independently from project experiment evidence. Use when discovering papers, organizing literature folders, maintaining indexes/query maps/reading routes, tracking bibliographic verification, deduplicating sources, or producing an experiment-facing literature brief. Use sci-paper-reader for deep reading and never treat literature claims as proof of project results.
---

# SCI Literature Manager

Make literature discoverable and reusable without mixing it with experiment records. Follow project-local rules and `sci-research-manager` evidence boundaries.

## Classify the task

- `literature_discovery`: find candidate papers from primary/official sources.
- `literature_indexing`: organize PDFs, notes, folders, and indexes.
- `deep_reading`: hand the located source to `sci-paper-reader`.
- `route_synthesis`: map papers to a research question and competing causes.
- `citation_verification`: verify title, author, venue, year, DOI/arXiv, code, and exact claims.
- `experiment_support`: produce a literature-to-experiment brief.
- `maintenance`: deduplicate, repair links, or archive superseded notes.

## Retrieve before reading broadly

Read the project's literature query map/index, then matching collection manifests/cards, then the PDF or official source for exact claims, figures, metrics, or bibliography. Do not batch-read the entire library unless the user asks for a full audit.

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

Use project-relative paths and existing conventions. Keep the Markdown understanding artifact canonical; treat HTML/PPT/Word as derivatives. Put dated project-specific implications at the end so the paper packet remains reusable.

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

## Produce a literature-to-experiment brief

Before an experiment is created, provide:

- source identities and verification status;
- theoretical motivation and project-facing hypothesis;
- variables/cues and required controls;
- success/failure criteria;
- likely confounds and non-transferable assumptions;
- do-not-overclaim/do-not-do-next;
- recommended lifecycle stage.

Then hand experiment IDs, protocols, runs, and results to `sci-experiment-manager`. Literature-only items never enter the experiment index or claim map as project evidence.
