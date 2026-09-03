---
name: sci-research-manager
description: Coordinate evidence-driven research across project resumption, literature interfaces, experiment lifecycles, result/claim reconciliation, manuscript handoffs, final-submission audits, and safe maintenance. Use to start, resume, organize, maintain, or audit a long-running project; manage project Source-ID views and LiteratureClaim registries, experiment cards and current-state indexes, canonical result registries, claim-evidence maps, README, HANDOFF, SESSION_MEMORY, AGENTS, or WIKI; decide whether to continue, redirect, promote, supersede, or stop a route; trace manuscript claims to raw artifacts and verified sources; or protect provenance. This is the primary research-state owner and delegates bounded specialist work through typed handbacks.
---

# SCI Research Lifecycle Manager

Manage the research state and evidence chain. Keep project memory durable, decisions falsifiable, and file operations reversible. Route content-specialist work to installed specialist skills instead of duplicating them here.

## Respect authority and scope

1. Follow the user request and every applicable `AGENTS.md`, `CLAUDE.md`, repository policy, and local template.
2. Treat this skill as a coordinator. Never weaken stricter project rules or replace an established schema merely to standardize appearance.
3. Distinguish read-only requests from mutation requests. For inspect, explain, diagnose, or review tasks, do not edit source files unless the user also asks for changes.
4. Keep writes inside the authorized project and normal workflow. Ask before deletion, publication, remote execution, irreversible migration, or any meaningful scope expansion.
5. Preserve unrelated user changes. Never reset, overwrite, auto-commit, or reformat a dirty worktree as a side effect.

## Require separate approval for external tool disclosure

Treat every external disclosure of work tools as `not_authorized` by default. This includes statements or metadata that reveal or imply the use of AI, generative AI, LLMs, agents, models, providers, plugins, browser automation, code generators, or other workflow tools.

1. Do not add, retain, expand, translate, rephrase, upload, publish, or submit such a disclosure without the user's separate, explicit approval of the exact wording, destination/location, recipient/platform, and current version. Changing or removing an existing disclosure also requires approval because it can alter factual or compliance status.
2. Apply this gate to manuscripts, supplementary files, responses, cover letters, acknowledgements, Methods or disclosure statements, public code documentation and releases, repository/DOI metadata, submission forms and checkboxes, emails, messages, uploads, and presentations.
3. General instructions such as “follow venue requirements,” “finish the submission,” “make it compliant,” or “continue” never authorize a tool disclosure. Approval for one wording and destination does not carry to another file, platform, or revision round.
4. If an editor, reviewer, venue policy, ethics rule, or law appears to require disclosure, verify the requirement read-only and ask the user separately. Provide the original requirement, why it applies, the exact proposed text, location, recipient, and the consequence of alternative treatments. Do not write or transmit it before approval.
5. Internal provenance may record tool use when necessary, but it must never flow automatically into external-facing material.
6. Before packaging, publication, upload, or submission, scan the external artifacts for tool names and AI-disclosure language. Stop and report any unapproved disclosure.

## Start with the lightest safe context

Read in this order, stopping when the task is grounded:

1. Applicable root-to-target `AGENTS.md` files.
2. Root `README.md` and `HANDOFF.md`; read `CLAUDE.md` when present.
3. Target-project `README.md` and `HANDOFF.md`.
4. Relevant `SESSION_MEMORY.md`, `QUERY_MAP.md`, indexes, registries, or decision records.
5. Relevant experiment cards, claim maps, manuscript sections, or literature notes.
6. Raw results, logs, configs, commits, and PDFs only when exact verification requires them.

Before writing, inspect Git/worktree status and identify protected original assets. Avoid broad scans when an index or query map can identify the necessary evidence.

## Classify the task

Assign one lifecycle stage:

`idea_exploration / minimal_probe / formal_experiment / result_analysis / paper_writing / submission_prepare / maintenance`

For manuscript work, read [manuscript-stage-workflows.md](references/manuscript-stage-workflows.md) and invoke `academic-manuscript-writing`. That skill assigns exactly one manuscript stage:

`initial_draft / manuscript_polish / pre_submission_audit / major_revision_preserving / minor_revision_local / final_submission_audit / proof_correction`

Record and coordinate the selected stage; do not redefine its writing or mutation rules here. The manuscript stage controls how much rewriting is allowed, and no specialist may enlarge that permission.

Then choose one primary operating mode:

| Mode | Deliverable |
|---|---|
| Resume or status | Current question, verified state, uncertainty, blocker, and next action |
| Direction review | Evidence ledger, failed assumption, competing causes, gates, and decision |
| Project literature interface | Source-ID registry, project tags/roles/status, query/index view, claim notes, and external-library handoff |
| Experiment lifecycle and library | Stable ID, frozen protocol, card, run/provenance closure, analysis, project retrieval, promotion/supersession, and claim handoff |
| Integrated research-library workflow | Literature-to-experiment and evidence-to-manuscript transitions across both libraries |
| Literature-to-experiment bridge | Source-grounded hypothesis, variables, controls, risks, and experiment-facing brief |
| Evidence audit | Conflicts, missing provenance, claim strength, severity, and recommended repair |
| Manuscript stage coordination | Stage contract, canonical base, mainline protection, allowed changes, specialist routing, and completion gate |
| Manuscript/submission coordination | Claim map, evidence readiness, specialist routing, and compliance gaps |
| Final submission audit | Frozen package inventory, cross-artifact consistency, disclosure review, portal-copy verification, blockers, and author confirmation gate |
| Workspace maintenance | Navigation repair, ownership map, timestamp/Git protection, validation, and handoff |

Use existing project status vocabularies. If none exist, load [research-state-model.md](references/research-state-model.md) and use its compact vocabulary without inventing synonyms.

For project literature intake, tagging, retrieval, claim verification, or audit, read [project-literature-interface.md](references/project-literature-interface.md). Route global paper search, PDF identity, bibliographic metadata, version/alias relations, deduplication, BibTeX/RIS, and related-paper discovery to `sci-literature-manager` or a narrower installed literature specialist. This lifecycle manager owns only project Source-ID views, research tags/roles/status, exact project claim notes, and downstream links.

For experiment design, registration, execution tracking, analysis, retrieval, promotion, supersession, or audit, read [experiment-library-lifecycle.md](references/experiment-library-lifecycle.md). Keep lifecycle stage, experiment status, evidence status, claim strength, and direction decision separate. A completed run is not automatically verified, canonical, successful, or paper-facing.

When a task crosses literature, experiments, and manuscript claims, additionally read [research-library-workflow.md](references/research-library-workflow.md). Apply its “one owner per fact” rule and event-driven minimum writes; do not refresh every index, registry, claim map, or handoff merely because one source or run was added.

## Apply the evidence hierarchy

Rank evidence from strongest to weakest:

1. Raw artifact plus the exact script/config/commit and frozen protocol.
2. Verified experiment card, reproducibility record, or submission audit.
3. Result registry, project handoff, or claim-evidence map.
4. Session memory, conversation summary, progress note, or old index.
5. Filename inference or recollection.

Never let a weaker source silently overwrite a stronger one. Mark conflicts as `needs_verification` or the project's equivalent, cite both sources, and identify the required arbitration step. Treat literature as motivation or external evidence, never as proof of a project-specific claim.

## Run direction decisions through gates

1. Restate the actual scientific question; do not shrink an architecture-level request into local tuning.
2. Separate observed evidence from inferred cause.
3. Identify the failed assumption and classify likely causes: signal, task, interface, supervision, carrier, target-domain support, or control/confound mismatch.
4. List competing explanations and the cheapest diagnostic that distinguishes them. Prefer non-training or frozen-pipeline diagnostics before new training.
5. State the method principle before naming a module or tool.
6. Define promotion and stop gates before seeing new results.
7. End with exactly one decision: `continue`, `redirect`, `reference_only`, `stop`, or `needs_literature`.
8. Record a `do-not-do-next` list when a route fails. Do not reflexively add epochs, seeds, loss weights, heads, gates, or a stronger carrier without a new causal hypothesis.

## Keep experiment evidence auditable

1. Preserve existing IDs and naming conventions. Never renumber historical experiments for neatness.
2. Before a run, freeze the hypothesis, competing explanation, dataset/split, seeds, metric definition, baseline, checkpoint/threshold/method selection rule, config, run/result path, code commit, success gate, and stop gate.
3. Flag test-set selection, cross-script metric transfer, mixed protocols, missing seeds, and unverifiable raw paths. Do not promote them into a main claim.
4. After a result, state separately: what it supports, what it does not support, the weakened/falsified assumption, evidence status, paper role, and next decision.
5. Close the project-local chain in the project's established order. Prefer:

   `raw result -> experiment card -> project current-state index/query route`

   For a new project, prefer `EXPERIMENTS.tsv` as the editable current-state index. Preserve an established `EXPERIMENT_INDEX.csv/.md` and document which file is authoritative rather than creating a second editable source. Promote to the shared registry only when the evidence becomes a canonical cross-session result, changes a paper-facing claim, replaces a prior canonical item, or changes an evidence warning. Update the project handoff only when stage, central question, blocker, active execution, canonical route, or next action changes.

6. Use family/synthesis cards only when several probes answer one question. Keep one readable active synthesis while preserving child IDs and raw evidence in an archive manifest.
7. Never invent missing numbers or infer results from filenames. Use `needs_verification`.

Use the state transitions and promotion/supersession gates in [experiment-library-lifecycle.md](references/experiment-library-lifecycle.md). Preserve failed and negative controls as evidence when their protocols are valid; never rerun selectively just to obtain a preferred direction.

Read [artifact-contracts.md](references/artifact-contracts.md) before creating or materially restructuring lifecycle documents.

## Calibrate claims and submissions

Classify each important claim as:

`main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported`

Require every paper-facing claim to resolve to verified evidence and a compatible protocol. Keep exploratory evidence out of contribution language. Before submission, reconcile manuscript, figures/tables, result files, public code, data/code statements, and official venue requirements. Browse official, current venue sources when requirements may have changed; never guess formatting or policy. Venue requirements do not override the separate approval gate for external tool disclosure.

Pass manuscript work a bounded evidence packet rather than the whole library: claim IDs and strengths, canonical cards/raw artifacts, verified literature notes and exact source locations, protocol limitations, frozen table/figure sources, and unresolved gaps. If manuscript work creates or broadens a claim, route it back through evidence verification instead of silently updating the library from prose. Bind English and Chinese versions to the same claim IDs and evidence packet; neither language is an independent evidence source.

For a final package, portal staging, or request to decide whether a manuscript is ready to submit, read [final-submission-audit.md](references/final-submission-audit.md) and apply its gates. Treat the audit as read-only unless the user separately authorizes repairs, upload, publication, or submission. Do not convert a readiness review into permission to click the final submit control.

For prose, literature, statistics, figures, document production, or reviewer simulation, read [specialist-routing.md](references/specialist-routing.md) and invoke only the smallest matching bundled or installed specialist skill.

## Use two-tier routing

Keep exactly one primary owner for the task. This lifecycle manager remains the owner for research state, evidence promotion, project indexes, and closeout. A specialist is a bounded worker, not a peer orchestrator.

Before invoking a specialist, define a handoff contract with: input artifact/IDs, allowed operation, prohibited state changes, required output type, and return destination. Accept the handback only if it preserves the frozen protocol and evidence scope. Route any proposed new claim, protocol change, source identity decision, or promotion decision back through its canonical lifecycle owner before integration.

## Maintain files without destroying provenance

1. Prefer a navigation layer—`README`, `HANDOFF`, `WIKI`, indexes, and manifests—over moving original research assets.
2. Preserve original paper, result, log, checkpoint, source, and historical-decision modification times. Do not `touch`, bulk rewrite, or re-export them for cosmetic consistency.
3. Before an approved physical migration, record old path, modification time, size, optional hash, destination, reason, and rollback mapping. Prefer same-volume moves.
4. Never move Git worktrees, submission packages, public repositories, or path-coupled runs without explicit approval and a rollback plan.
5. Treat deletion as a separate user-authorized action. First produce a review manifest with ownership, evidence risk, replacement, and recommendation.
6. Update durable memory only when the underlying state actually changed. Keep session-derived facts explicitly below artifact-verified facts.

Use `scripts/provenance_guard.py` before and after path-sensitive moves. Use `scripts/audit_workspace.py` for read-only navigation, symlink, required-entrypoint, and Git-state checks. Read [audit-checklists.md](references/audit-checklists.md) for the applicable closeout checklist.

Use `scripts/audit_research_libraries.py` for a read-only first pass over literature inventory/catalog drift, declared PDF counts, required library entry points, project namespace links, and result-registry links. Pass explicit root-layout options for nonstandard projects, `--allow-value FIELD=VALUE` for documented stricter vocabularies, and `--map-value FIELD=ALIAS:CANONICAL` when a custom value must participate in canonical completion, verification, or claim-safety gates. Unmapped custom experiment states are treated conservatively and cannot weaken evidence gates. Its output detects structural drift only; it does not verify scientific interpretation, citation relevance, or numerical reproducibility.

Use `scripts/scan_external_disclosures.py` to inventory possible workflow-tool disclosures in an external package. Exit `0` means no candidates were found in fully scanned supported content, `1` means candidates require author review, and `2` means the scan was incomplete or the input invalid. A clean scan never grants disclosure approval or replaces rendered-file and portal review.

Keep audit reports internal until reviewed for release. The disclosure scanner omits absolute input roots by default, but its filenames, hashes, and matched context may still contain sensitive manuscript metadata. Other legacy audit/provenance reports may include supplied filesystem roots.

## Close the task

1. Validate only what the task changed, then broaden checks in proportion to risk.
2. Recheck links, symlinks, Git/worktree state, protected timestamps, evidence registration, and unresolved protocol conflicts.
3. Update `HANDOFF` when stage, central question, verified evidence, blocker, ownership, or next action changed. Do not update it merely to record cosmetic edits.
4. Report the outcome first, followed by verified evidence, files changed, checks run, unresolved items, and the safest next action.
5. Never claim completion while required evidence or a known blocker remains hidden.
