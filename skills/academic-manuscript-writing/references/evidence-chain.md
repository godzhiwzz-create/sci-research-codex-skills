# Evidence Chain

## Evidence status ladder
- Final paper-facing result
  - Explicitly marked as final, paper-used, or representative final.
- Verified summary
  - A paper-facing summary backed by stable raw files.
- Raw verification source
  - Useful for checking numbers, not for direct manuscript citation unless the summary is absent.
- Unsafe intermediate artifact
  - Archived, placeholder, mixed-status, guardrail-only, or otherwise incomplete.

## Evidence map template

| Claim | Evidence file | Evidence role | Finality | Risk | Notes |
|---|---|---|---|---|---|

## Role rubric
- Phenomenon-establishing: show that the pattern exists.
- Mechanism-discriminating: compare competing explanations and separate them by evidence.
- Reinforcement/robustness: show the pattern survives denser checks or repeated runs.
- Consequence/method implication: show that the mechanism can guide a useful design change.
- Generalization/boundary: show what transfers across architectures or settings, and what does not.

## Decision rules
- Prefer paper-facing directories over archive directories.
- Trust directory-level README status labels when present.
- Verify summaries against raw files, but do not promote raw files above a stable paper-facing summary without cause.
- If a result comes from a mixed-status folder, do not cite it as final.
- If a result is only a representative checkpoint, call it representative and keep the claim narrow.
- If a result is archived for traceability only, treat it as background, not as main evidence.
