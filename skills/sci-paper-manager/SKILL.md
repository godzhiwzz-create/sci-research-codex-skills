---
name: sci-paper-manager
description: Manage evidence-driven academic paper artifacts, including draft-core structure, claim-evidence maps, paper status, figure/table plans, target-venue requirement caches, submission packages, and unsupported-claim control. Use when creating or reconciling manuscript structure, claims, figures/tables, venue preparation, or submission files. Use academic-manuscript-writing for prose and sci-result-auditor for pure evidence audits.
---

# SCI Paper Manager

Turn verified project evidence into an auditable paper structure. Follow `sci-research-manager` and project-local evidence rules.

## Separate content from formatting

Use two stages:

1. `draft_core`: venue-neutral story, claims, sections, figures, tables, and evidence.
2. `submission_targets/<target>`: official template, manuscript, figures/tables, supplementary files, declarations, cover letter, checklist, compliance report, submitted versions, and revisions.

Do not adapt to a target venue until the draft core is coherent.

## Ground every paper-facing claim

Before drafting or restructuring:

1. Read project handoff and paper status.
2. Read the claim-evidence map.
3. Read only cards/raw artifacts tied to the claims in scope.
4. Classify claim strength as `main_claim`, `trend_only`, `diagnostic_only`, `negative_boundary`, `internal_exploration`, or `unsupported`.
5. Record contrary evidence, protocol compatibility, and missing validation.

Do not reuse old prose until it matches the current central story and evidence.

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

Use `academic-manuscript-writing` only after claim roles are fixed. Use `sci-result-auditor` for independent consistency checks.
