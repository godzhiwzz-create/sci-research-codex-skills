# Research Audit Checklists

Select only the checklist matching the task. Report issues with severity, evidence, and repair; do not silently mutate sources during an audit-only request.

## Pre-write safety

- Confirm project root and applicable `AGENTS.md` chain.
- Confirm whether the request authorizes writes, movement, deletion, remote execution, commit, or publication.
- Inspect Git/worktree status and preserve unrelated changes.
- Identify original assets whose modification times are provenance-sensitive.
- Identify current canonical files before creating another index or template.
- Prefer targeted reads through handoffs/query maps over global scans.

## Workspace/navigation audit

- Root and each managed project have discoverable README/HANDOFF/AGENTS entry points.
- Every link used as a current entry point resolves.
- Symlinks resolve and do not unexpectedly escape the intended ownership boundary.
- Each directory has one clear owner and canonical entry point.
- Root contains no unowned project scripts/results unless explicitly designated.
- README, HANDOFF, WIKI, memory, and registry responsibilities are not duplicated.
- Archived/frozen work is labeled read-only and points to its replacement.
- Git repositories/worktrees are identified; dirty state is reported, not repaired automatically.

Run `scripts/audit_workspace.py <root>` for the deterministic first pass. Add `--all-markdown` only for a deliberate broad link audit.

## Experiment/evidence audit

- Stable ID and canonical card exist.
- Raw result, config, command/run path, code commit, split, seeds, metric, baseline, and selection rule are traceable.
- Reported numbers can be reproduced from the cited raw artifact.
- Dataset/evaluation protocol matches the comparison.
- Checkpoint, threshold, method, or hyperparameter selection did not use the test set; otherwise label the evidence unsafe for a main claim.
- Competing explanations and required controls are present.
- Card interpretation separates supports from does-not-support.
- Card, project `EXPERIMENTS.tsv`, shared registry, claim map, and handoff agree within their ownership boundaries.
- Missing artifacts are labeled `needs_verification`; filenames and chat summaries are not treated as proof.
- Lifecycle stage, execution status, evidence status, claim strength, and direction decision are separate and semantically compatible.
- `complete` runs have exit state and expected raw artifacts; `verified` evidence agrees with the frozen protocol and extraction code.
- Shared registry items satisfy a promotion reason and point back to the project card/raw source; superseded items name their replacement.

Use a data-validation or statistical specialist skill for calculation/methodology details.

## Project literature-interface audit

- Global search/identity/metadata/version/dedup/BibTeX facts remain owned by the literature-management specialist.
- Every project source row has a unique resolvable Source ID, normalized tags, a project role, and a valid reading depth.
- `INDEX.md` is a generated view of the canonical project registry; `QUERY_MAP.md` routes research questions without duplicating global metadata.
- `claim_verified` LiteratureClaim rows have a project note with exact source location, bounded wording, protocol boundary, downstream IDs, and verification date.
- Alias or source-version changes do not silently preserve version-sensitive claim verification.
- Project directories contain no copied PDF/BibTeX merely for convenience.

## Claim/manuscript audit

- Identify the manuscript stage using [manuscript-stage-workflows.md](manuscript-stage-workflows.md); verify that the mutation scope matches that stage.
- Every paper-facing claim has an ID, strength, and exact evidence source.
- Claim scope matches dataset, split, metric, seeds, and protocol.
- Diagnostic/trend/source-only evidence is not phrased as robust general superiority.
- Negative boundaries and contrary evidence are disclosed where material.
- Old-route language and unsupported contribution statements are removed or clearly historical.
- Figures/tables use the same canonical numbers as cards and registries.
- Citations support external claims; literature is not used as proof of project results.
- Manuscript, supplementary material, data/code statements, and public code agree.
- In a major/minor revision, the submitted base, mainline card, comment matrix, preservation report, response locations, clean/marked-up equivalence, and unmapped changes are accounted for.

## Submission audit

For a final package, portal staging, or final-submit readiness decision, use [final-submission-audit.md](final-submission-audit.md). At minimum:

- Official current venue guidelines/template/checklist have been verified and access date recorded.
- Article type, anonymity, title/abstract, authors, corresponding author, figures/tables, references, supplementary material, ethics, funding, conflicts, author contributions, and data/code availability are covered.
- All submission files point to one frozen content version; derived and portal copies are traceable to it.
- Public code and archived releases reproduce the described protocol or the mismatch is disclosed.
- Artifact hashes/commits and final rendered PDF are recorded.
- Every potential external workflow-tool disclosure is inventoried with exact text and location; unapproved or changed disclosures block packaging, upload, and submission.
- Portal copies are reverse-checked when the platform permits download.
- No requirement is guessed; unclear items remain `needs_verification`.
- Final submission remains blocked until the author confirms at the point of the irreversible action.

## Migration/archive audit

- User authorized the move/archive scope.
- Ownership, evidence role, and downstream references are known.
- A provenance snapshot or equivalent record exists before movement.
- Same-volume move is used when possible; copy/extract time is not mistaken for experiment time.
- Old-to-new mapping and rollback steps are recorded.
- Links and symlinks are updated and rechecked.
- Original content, size, modification time, and optional hash still match.
- Experiment metadata, configs, result summaries, commands, and claim relations remain accessible.
- Deletion candidates are listed separately and not deleted without explicit instruction.

## Closeout

- Validate the changed scope and any high-risk downstream consumers.
- Recheck Git/worktree state and protected assets.
- Update handoff/registry only when factual state changed.
- State what was verified, what remains uncertain, and what should happen next.
- Do not call the task complete if a required artifact, protocol decision, or user authorization is still missing.
