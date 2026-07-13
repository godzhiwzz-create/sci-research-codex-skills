# Research Audit Checklists

Select only the checklist matching the task. Report issues with severity, evidence, and repair; do not silently mutate sources during an audit-only request.

## Pre-write safety

- Confirm project root and applicable `AGENTS.md` chain.
- Confirm whether the request authorizes writes, movement, deletion, remote execution, commit, or publication.
- Inspect Git/worktree status and preserve unrelated changes.
- Identify provenance-sensitive original assets and current canonical files.
- Prefer targeted reads through handoffs/query maps over global scans.

## Workspace/navigation audit

- Root and each managed project have discoverable README/HANDOFF/AGENTS entry points.
- Current entry links and symlinks resolve within intended ownership boundaries.
- Each directory has one owner and canonical entry point.
- Root contains no unowned project scripts/results unless designated.
- README, HANDOFF, WIKI, memory, and registry responsibilities are not duplicated.
- Archived/frozen work is read-only and points to its replacement.
- Dirty Git state is reported, not repaired automatically.

Run `scripts/audit_workspace.py <root>` for the deterministic first pass. Add `--all-markdown` only for a deliberate broad link audit.

## Experiment/evidence audit

- Stable ID and canonical card exist.
- Raw result, config, command/run path, commit, split, seeds, metric, baseline, and selection rule are traceable.
- Reported numbers can be reproduced from the cited raw artifact.
- Dataset/evaluation protocol matches the comparison.
- Test-set checkpoint/threshold/method selection is labeled unsafe for a main claim.
- Competing explanations and required controls are present.
- Card interpretation separates supports from does-not-support.
- Card, index, registry, claim map, and handoff agree.
- Missing artifacts are `needs_verification`; filenames/chat summaries are not proof.

## Claim/manuscript audit

- Every paper-facing claim has an ID, strength, and exact evidence source.
- Claim scope matches dataset, split, metric, seeds, and protocol.
- Diagnostic/trend/source-only evidence is not phrased as robust general superiority.
- Negative boundaries and contrary evidence are disclosed where material.
- Figures/tables use the same canonical numbers as cards and registries.
- Citations support external claims; literature is not proof of project results.
- Manuscript, supplementary material, data/code statements, and public code agree.

## Submission audit

- Official current venue guidelines/template/checklist and access date are recorded.
- Article type, limits, anonymity, structure, figures/tables, references, supplementary material, declarations, and data/code availability are covered.
- Submission files point to one frozen manuscript/evidence version.
- Public code reproduces the described protocol or the mismatch is disclosed.
- Artifact hashes/commits and final rendered PDF are recorded.
- No requirement is guessed; unclear items remain `needs_verification`.

## Migration/archive audit

- User authorized the move/archive scope.
- Ownership, evidence role, and downstream references are known.
- A provenance snapshot exists before movement.
- Same-volume move is used when possible; copy/extract time is not treated as experiment time.
- Old-to-new mapping and rollback steps are recorded.
- Links, content, size, modification time, and optional hash are rechecked.
- Metadata, configs, summaries, commands, and claim relations remain accessible.
- Deletion candidates remain separate until explicitly authorized.

## Closeout

- Validate the changed scope and high-risk downstream consumers.
- Recheck Git/worktree state and protected assets.
- Update handoff/registry only when factual state changed.
- State what was verified, what remains uncertain, and what should happen next.
