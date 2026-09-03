---
name: sci-paper-manager
description: Manage evidence-driven supporting paper artifacts, including claim-evidence maps, paper-status ledgers, figure/table plans, target-venue requirement caches, submission checklists, package inventories, and unsupported-claim control. Use when creating or reconciling those bounded artifacts for a manuscript or submission. Return structure or package plans to academic-manuscript-writing, which owns manuscript stages, mainline, prose, responses, and canonical integration; use sci-result-auditor for pure evidence audits.
---

# SCI Paper Manager

Turn verified project evidence into auditable supporting plans and status artifacts. Follow `sci-research-manager` and project-local evidence rules, and return manuscript-facing plans to `academic-manuscript-writing` for integration.

## Separate artifact layers from manuscript stages

Maintain two artifact layers when the project uses them:

1. `draft_core`: venue-neutral story, claims, sections, figures, tables, and evidence.
2. `submission_targets/<target>`: official template, manuscript, figures/tables, supplementary files, declarations, cover letter, checklist, compliance report, submitted versions, and revisions.

These are storage layers, not manuscript lifecycle stages. `academic-manuscript-writing` selects the writing/revision stage and owns prose, mainline, response content, and canonical integration. Do not adapt to a target venue until the draft core is coherent.

## Ground every paper-facing claim

Before changing a claim map, paper-status ledger, figure/table plan, or package inventory:

1. Read project handoff and paper status.
2. Read the claim-evidence map.
3. Read only cards/raw artifacts tied to the claims in scope.
4. Classify claim strength as `main_claim`, `trend_only`, `diagnostic_only`, `negative_boundary`, `internal_exploration`, or `unsupported`.
5. Record contrary evidence, protocol compatibility, and missing validation.

Do not treat old prose as evidence. Report any mainline discrepancy to the manuscript owner instead of rewriting the prose here.

## Maintain paper artifacts

Use the bundled templates when the project lacks equivalents:

- [PAPER_STATUS.md](templates/PAPER_STATUS.md)
- [CLAIM_EVIDENCE_MAP.md](templates/CLAIM_EVIDENCE_MAP.md)
- [FIGURE_PLAN.md](templates/FIGURE_PLAN.md)
- [TABLE_PLAN.md](templates/TABLE_PLAN.md)
- [submission_checklist.md](templates/submission_checklist.md)
- [guideline_notes.md](templates/guideline_notes.md)
- [format_compliance_report.md](templates/format_compliance_report.md)

Keep experiment numbers in cards/registries and link to them rather than duplicating mutable tables across status files.

## Verify target-venue requirements

Before changing a submission package, read cached `guideline_notes.md`. If missing, stale, or conflicting, verify current official author guidelines, template, article type, limits, structure, figures/tables, references, supplementary material, declarations, data/code availability, anonymity, and upload rules. Record source URL/path and access date.

Never guess a requirement. Mark ambiguity `needs_verification`.

## Reconcile before submission

Check that manuscript, figures/tables, raw results, claim map, supplementary files, public code, and data/code statements use one compatible protocol and frozen version. Label mismatches `protocol_mismatch`; do not claim full reproducibility until resolved.

Use `academic-manuscript-writing` only after claim roles are fixed. Use `sci-result-auditor` for independent consistency checks. Return updated claim maps, plans, requirement notes, checklists, or package inventories to the active primary owner; do not decide final readiness, broaden claims, rewrite manuscript prose, or perform an irreversible submission action.
