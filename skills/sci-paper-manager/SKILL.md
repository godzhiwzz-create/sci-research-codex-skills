---
name: sci-paper-manager
description: Manage evidence-driven SCI paper writing, including draft-core workflow, claim-evidence mapping, paper status tracking, figure/table plans, target journal preparation, and unsupported-claim control. Use when creating or revising manuscript structure, sections, figures/tables, claim-evidence maps, or submission packages. For pure result/claim consistency audits without manuscript writing, prefer sci-result-auditor.
---

# sci-paper-manager

## Purpose

Manage evidence-driven SCI paper writing without losing the project's central story or mixing old unsupported content into the current manuscript.

This skill owns manuscript artifacts and claim-to-paper organization. It does
not replace `sci-result-auditor` for pure evidence audits or
`academic-manuscript-writing` for prose-level drafting once the claim structure
is already fixed.

## Startup rule

First classify the task stage: `idea_exploration`, `minimal_probe`, `formal_experiment`, `result_analysis`, `paper_writing`, `submission_prepare`, or `maintenance`.

## Paper workflow

Two-stage workflow:

### Stage 1: draft_core

- generic paper draft
- not bound to any journal template
- focus on content, logic, claims, figures, tables, and evidence

### Stage 2: submission_targets

- target journal template
- only created after `draft_core` is mature
- includes manuscript, figures, tables, supplementary, cover letter, checklist, submitted versions, and revisions
- must be driven by official target-journal or target-conference requirements

## Target-journal requirement rule

After a target journal or conference is selected, Codex must not directly reformat from memory.

Before modifying the submission manuscript, Codex must read cached notes first:

`research_workspace/paper/submission_targets/<target_name>/guideline_notes.md`

If cached notes do not exist, are stale, are incomplete, or conflict with the requested change, Codex must read and summarize official sources:

1. official author guidelines
2. official manuscript template or class/style files
3. article type requirements
4. word/page limits
5. title page and abstract requirements
6. section structure requirements
7. figure, table, graphical abstract, and supplementary-material requirements
8. reference and citation style
9. data/code availability, ethics, funding, conflict-of-interest, and author contribution declarations
10. submission checklist and file naming/upload requirements

Record the source file path or URL, access date, and extracted requirements in:

`research_workspace/paper/submission_targets/<target_name>/guideline_notes.md`

Then create or update:

- `manuscript/`
- `figures/`
- `tables/`
- `supplementary/`
- `cover_letter.md`
- `submission_checklist.md`
- `format_compliance_report.md`

Do not guess target requirements. If official requirements are missing or unclear, mark them as `needs verification` and ask the user for the guideline file or URL.

## Context discipline policy

- For writing tasks, read `PAPER_STATUS.md`, `CLAIM_EVIDENCE_MAP.md`, and the target section file before reading the whole draft.
- Read only experiment cards connected to the claims being written.
- Loading all `draft_core/sections/` is appropriate for whole-manuscript consistency, restructuring, submission preparation, or revision.
- For target-journal formatting, start from `guideline_notes.md`, then reread official webpages or PDFs whenever exact compliance requires it.
- When official guideline files are large, first inspect headings, checklists, tables, and requirement sections; read full text when necessary.
- Keep `guideline_notes.md`, `submission_checklist.md`, and `format_compliance_report.md` as compact caches for future tasks.

## Submission compliance rule

When preparing `submission_targets`, every format/content change must trace to one of:

- official target guideline
- official template
- verified journal checklist
- evidence-supported paper content from `draft_core`

Do not introduce unsupported claims while adapting format.

## Writing rule

Before writing any section:

1. read `PROJECT_HANDOFF.md`
2. read `research_workspace/paper/PAPER_STATUS.md`
3. read `research_workspace/paper/CLAIM_EVIDENCE_MAP.md`
4. read relevant experiment cards
5. write only evidence-supported claims
6. mark uncertain claims clearly

## Claim rule

Every paper claim must have a claim ID and evidence in `CLAIM_EVIDENCE_MAP.md`.

If no evidence exists, mark it as unsupported and propose the missing experiment. Do not phrase it as a confirmed conclusion.

## Claim-strength rule

When updating a manuscript or `CLAIM_EVIDENCE_MAP.md`, classify each important claim:

- `main_claim`: central conclusion supported by formal or strongest available evidence.
- `trend_only`: average direction or limited signal; avoid words like significant, robust, or superior unless tested.
- `diagnostic_only`: mechanism or behavior evidence, not a performance claim.
- `negative_boundary`: failed or boundary result that narrows the method scope.
- `internal_exploration`: useful for decisions but not paper-facing unless moved into discussion/appendix.
- `unsupported`: no confirmed evidence; do not write as fact.

Manuscript wording must match the claim strength. A `trend_only` or
`diagnostic_only` result should not be written as a final method contribution.

## Evidence-to-writing rule

For each section, first decide the claim role:

1. what the evidence proves;
2. what it only suggests;
3. what it explicitly does not prove;
4. whether it belongs in main text, appendix, discussion boundary, or internal notes only.

This prevents result tables from becoming a stitched experiment log.

## Old-content rule

Before reusing older paper text, check whether it matches the current central story in `PROJECT_HANDOFF.md` and is supported by current experiment cards.

## No fabrication

Never invent results, citations, DOIs, author names, dataset statistics, or claims. Use `uncertain`, `preliminary`, or `needs verification` when evidence is incomplete.
