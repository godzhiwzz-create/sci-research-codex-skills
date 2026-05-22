---
name: sci-result-auditor
description: Audit SCI research projects for consistency across experiments, result files, claim-evidence maps, paper drafts, indexes, and reproducibility metadata. Use when checking whether claims are supported, results are traceable, or project memory files are internally consistent.
---

# sci-result-auditor

## Purpose

Audit whether experiments, results, paper claims, and lightweight indexes are trustworthy, traceable, and consistent.

## Startup rule

First classify the task stage. Read lightweight context in this order:

1. `PROJECT_HANDOFF.md`
2. `research_workspace/experiments/QUERY_MAP.md`
3. `research_workspace/experiments/EXPERIMENT_INDEX.md`
4. `research_workspace/paper/CLAIM_EVIDENCE_MAP.md`
5. relevant experiment cards

Only inspect raw files when exact verification is required.

## Context discipline policy

- Start with index consistency before raw-file inspection.
- Audit selected claims or selected experiment IDs when possible.
- For broad audits, produce a staged audit plan before loading many cards and raw files.
- Use generated reports and indexes as the first pass.
- Inspect raw files for high-risk claims, missing evidence, exact metric verification, or reproducibility checks.

## Audit checklist

### Experiment audit

- dataset split is consistent
- teacher is frozen
- student architecture is consistent
- seed is recorded
- config is saved
- result comes from real files
- metric definition is consistent
- baseline is fair

### Paper audit

- every claim has evidence
- no unsupported conclusion is used
- no old central-story residue remains
- exploratory results are not written as confirmed results
- method contribution is not exaggerated
- failed directions are not packaged as the core method
- claim strength matches evidence strength (`main_claim`, `trend_only`, `diagnostic_only`, `negative_boundary`, `internal_exploration`, `unsupported`)

### File audit

- cards referenced by `EXPERIMENT_INDEX` exist
- raw paths referenced by cards exist or are marked missing
- experiment IDs in `CLAIM_EVIDENCE_MAP` exist in `EXPERIMENT_INDEX.csv`
- `PAPER_STATUS.md` is current
- `PROJECT_HANDOFF.md` is current

## Output rule

Report issues with severity, evidence, and recommended fix. Do not modify source files unless explicitly asked.

For result interpretation, always separate:

1. **supports**: what the result can safely support;
2. **does_not_support**: tempting conclusions that are not justified;
3. **next_action**: continue, pause, stop, or run a smaller follow-up;
4. **paper_role**: main text, appendix, discussion boundary, internal only, or not used;
5. **risk**: confound, missing baseline, weak seeds, metric mismatch, or unsupported generalization.

## Go/no-go rule

For minimal probes and exploratory families, produce a decision:

- `go`: enough signal for a paired or formal follow-up;
- `pause`: signal is mixed; needs a narrower hypothesis;
- `blocked`: a required prerequisite failed;
- `stop`: do not continue without a fresh hypothesis.

Do not recommend training or larger matrices when the probe only provides weak
or confounded diagnostic evidence.

## No fabrication

Do not infer metrics or results from filenames. If raw files are unavailable, mark the point as `needs verification`.
