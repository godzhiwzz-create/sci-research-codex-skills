# SCI Research Codex Skills

Codex skills for long-term, experiment-driven SCI paper projects.

This repository packages a small research workflow system:

- `sci-research-manager`: preserve project direction, stage plans, decisions, and handoff memory.
- `sci-experiment-manager`: manage experiment IDs, cards, lightweight indexes, and traceable results.
- `sci-paper-manager`: write and revise manuscripts through claim-evidence discipline.
- `sci-result-auditor`: audit consistency between experiments, claims, indexes, and drafts.
- `sci-asset-manager`: decide what to keep, archive, or delete without losing evidence metadata.
- `academic-manuscript-writing`: draft and revise academic manuscript sections with evidence-aware writing rules.

## Install

Copy the desired skill directories into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Restart Codex or reload skills after copying.

## Recommended Workspace Layout

These skills assume a research project keeps lightweight memory files near the code and paper draft:

```text
PROJECT_HANDOFF.md
research_workspace/
  experiments/
    QUERY_MAP.md
    EXPERIMENT_INDEX.md
    EXPERIMENT_INDEX.csv
    cards/
  paper/
    PAPER_STATUS.md
    CLAIM_EVIDENCE_MAP.md
  project/
    DECISION_LOG.md
    STAGE_PLAN.md
```

The templates included in each skill are intentionally generic. Fill them with your own project-specific evidence, paths, and decisions.

## Privacy Note

Do not publish real experiment logs, credentials, private datasets, unpublished metric tables, or personal server paths unless you have reviewed and approved them for release.
