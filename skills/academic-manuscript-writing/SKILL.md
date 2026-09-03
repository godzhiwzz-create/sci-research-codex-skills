---
name: academic-manuscript-writing
description: Own stage-aware academic manuscript work from initial drafting through standardized polishing, pre-submission audit, major or minor revision, reviewer response, final-package handoff, and proof correction. Use for writing, restructuring, polishing, reviewing, revising, responding to reviewers, producing clean and marked-up manuscripts, or preparing manuscript content for submission. Select one manuscript stage first and enforce its mutation, mainline-preservation, prose, figure/table, response, and transition rules. Do not replace literature search, citation verification, statistics, figure rendering, Word/PDF production, research evidence management, or irreversible submission controls.
---

# Academic Manuscript Lifecycle Writing

Write and revise manuscripts according to their actual lifecycle stage. Own the manuscript argument, prose, revision scope, response-letter content, and handoff to final submission; route evidence, citations, statistics, figures, documents, and portal actions to the appropriate specialist without surrendering narrative control.

## Respect authority and evidence

1. Follow the user, applicable `AGENTS.md`, project rules, `PAPER.md`, venue requirements, and evidence hierarchy. This skill never upgrades unverified notes into paper facts.
2. Identify the canonical manuscript source and rendered reference before editing. Preserve unrelated author changes and protected historical/submitted versions.
3. The main agent owns stage selection, mainline, claim/evidence alignment, canonical-file integration, and final prose. A specialist or subagent cannot enlarge the authorized mutation scope.
4. Never invent results, citations, table/figure locations, reviewer requirements, declarations, or completion states. Use `needs_verification` when evidence is missing.
5. External workflow-tool disclosure remains separately controlled by applicable project rules and the final-submission audit. This skill must not add, retain, remove, translate, or relocate such disclosure without the required author approval.
6. For claim-bearing work, consume the bounded evidence packet produced by the research lifecycle: claim ID/scope, canonical experiment card and raw source, or a `claim_verified` project literature note with exact location. Do not treat the global paper catalog, a project tag, a completed run, or fluent existing prose as verified evidence. Route new or broadened claims back to the owning literature/experiment workflow before writing them as findings.

## Select the manuscript stage first

Read [stage-router.md](references/stage-router.md) for every invocation. Assign exactly one stage:

`initial_draft / manuscript_polish / pre_submission_audit / major_revision_preserving / minor_revision_local / final_submission_audit / proof_correction`

State the detected stage and mutation scope briefly before substantive work. If the evidence supports multiple stages, use the least mutating safe stage and follow the transition gates; do not combine drafting, auditing, revision, and final submission into one uncontrolled pass.

## Load only the relevant writing rules

- For `initial_draft`, `manuscript_polish`, or `pre_submission_audit`, read [writing-standards.md](references/writing-standards.md).
- For `major_revision_preserving` or `minor_revision_local`, read [revision-and-response.md](references/revision-and-response.md) and the shared portions of [writing-standards.md](references/writing-standards.md).
- For `final_submission_audit`, read [submission-handoff.md](references/submission-handoff.md), then use the `sci-research-manager` final-submission audit.
- For `proof_correction`, read the proof section in [submission-handoff.md](references/submission-handoff.md).

Do not load every reference when only one stage applies.

## Consolidated manuscript owner

This skill contains the maintained, stage-aware writing standards for this package. Earlier generic drafting, polishing, response, self-review, and chapter-writing flows are consolidated here and are not parallel workflow owners. Do not reconstruct a multi-owner writing chain.

Preserve the useful separation of roles inside this single lifecycle: draft from evidence, polish without changing meaning, audit without editing, revise against the submitted base, and hand frozen content to final submission control. A request for several deliverables does not collapse these roles into one uncontrolled rewrite.

Specialist skills remain appropriate for bounded work:

- literature search and source verification;
- citation placement and bibliography validation;
- statistical analysis and quantitative validation;
- scientific figures and charts;
- data/code availability;
- LaTeX, Word, PDF, spreadsheet, and presentation production;
- read-only reviewer simulation;
- browser or portal operation after separate authorization.

Read [stage-router.md](references/stage-router.md) before invoking specialists or subagents; use only the smallest set that changes the outcome.

Use a two-tier contract: this skill is the sole manuscript owner, while each specialist receives a bounded input and returns one typed artifact such as a verified source packet, statistical result, quantitative plot, method diagram, compiled document, or mock-referee report. Specialists must not rewrite surrounding prose, change the selected manuscript stage, expand the revision scope, promote evidence, or integrate directly into the canonical manuscript. The main agent checks the handback and performs the final integration.

For path compatibility, existing projects may still link [workflow.md](references/workflow.md), [section-playbooks.md](references/section-playbooks.md), [evidence-chain.md](references/evidence-chain.md), [figure-table-writing.md](references/figure-table-writing.md), [style-rules.md](references/style-rules.md), or [examples.md](references/examples.md). Treat them as secondary reference material only; the stage router and stage-specific references above govern any conflict. Do not load them unless the user or an existing project explicitly points to them.

## Required stage artifacts

Maintain only artifacts that the current stage needs:

- canonical source/render identity;
- mainline card after the initial-draft stage;
- claim/evidence and terminology records when the project uses them;
- issue list for pre-submission audit;
- submitted-base identity, comment matrix, preservation report, unrequested-change report, clean/marked-up pair, and response for revisions;
- package inventory and final-audit report for submission;
- correction list and verified proof for production.

Do not create duplicate manuscript trees, decorative indexes, or a new permanent template when the project already has one.

## Close the stage

Use the completion and transition gates in [stage-router.md](references/stage-router.md). Report:

1. detected and completed stage;
2. canonical inputs and evidence used;
3. manuscript, response, figure/table, or package changes;
4. checks performed;
5. unresolved blockers and the only valid next stages.

Do not claim a stage is complete merely because prose was generated or a PDF compiled.
