# SCI Research Codex Skills

Codex skills for long-term, experiment-driven SCI paper projects.

This package helps Codex act less like a one-off writing assistant and more like a research workflow partner: it keeps project direction stable, retrieves experiment evidence with low context cost, prevents unsupported paper claims, and preserves enough metadata to make results auditable later.

## Skills Included

| Skill | Use it for |
|---|---|
| `sci-research-manager` | Project handoff memory, stage planning, decisions, risks, and direction control |
| `sci-experiment-manager` | Experiment IDs, experiment cards, lightweight indexes, result paths, and keep levels |
| `sci-paper-manager` | Evidence-driven manuscript drafting, claim maps, paper status, figure/table plans, and target-journal preparation |
| `sci-result-auditor` | Consistency checks across experiments, claims, paper drafts, and reproducibility metadata |
| `sci-asset-manager` | Archive reviews, cleanup decisions, submission keep lists, and cold archive manifests |
| `academic-manuscript-writing` | Academic section writing, evidence-aware revision, figure/table narration, and journal-style English |

## Install

Install all skills:

```bash
git clone <repository-url>
mkdir -p ~/.codex/skills
cp -R sci-research-codex-skills/skills/* ~/.codex/skills/
```

Install only selected skills:

```bash
mkdir -p ~/.codex/skills
cp -R sci-research-codex-skills/skills/sci-research-manager ~/.codex/skills/
cp -R sci-research-codex-skills/skills/sci-experiment-manager ~/.codex/skills/
cp -R sci-research-codex-skills/skills/sci-paper-manager ~/.codex/skills/
```

Restart Codex or reload skills after copying.

## Recommended Project Layout

These skills work best when each research project keeps lightweight memory files near the code and paper draft:

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

The templates are intentionally generic. Fill them with your own project-specific evidence, paths, and decisions.

## Quick Start Tutorial

### 1. Create The Workspace Skeleton

From the root of your research project:

```bash
mkdir -p research_workspace/experiments/cards
mkdir -p research_workspace/paper
mkdir -p research_workspace/project
```

Copy the starter templates:

```bash
cp ~/.codex/skills/sci-research-manager/templates/PROJECT_HANDOFF.md .
cp ~/.codex/skills/sci-research-manager/templates/DECISION_LOG.md research_workspace/project/
cp ~/.codex/skills/sci-research-manager/templates/STAGE_PLAN.md research_workspace/project/
cp ~/.codex/skills/sci-experiment-manager/templates/QUERY_MAP.md research_workspace/experiments/
cp ~/.codex/skills/sci-experiment-manager/templates/EXPERIMENT_INDEX.md research_workspace/experiments/
cp ~/.codex/skills/sci-experiment-manager/templates/EXPERIMENT_INDEX.csv research_workspace/experiments/
cp ~/.codex/skills/sci-paper-manager/templates/PAPER_STATUS.md research_workspace/paper/
cp ~/.codex/skills/sci-paper-manager/templates/CLAIM_EVIDENCE_MAP.md research_workspace/paper/
```

### 2. Tell Codex The Project Rules

Add an `AGENTS.md` file in your project root. A minimal version can say:

```markdown
# AGENTS.md

Before starting a research task, read:

1. PROJECT_HANDOFF.md
2. research_workspace/experiments/QUERY_MAP.md
3. research_workspace/experiments/EXPERIMENT_INDEX.md
4. relevant experiment cards only

Classify each task as one of:
idea_exploration, minimal_probe, formal_experiment, result_analysis,
paper_writing, submission_prepare, or maintenance.

Do not invent results, metrics, citations, or conclusions.
Every paper claim must be supported by CLAIM_EVIDENCE_MAP.md.
```

### 3. Start With Project Handoff

Ask Codex:

```text
Use sci-research-manager. Initialize the project memory files for my new SCI paper project. Keep uncertain details marked as uncertain.
```

Codex should fill `PROJECT_HANDOFF.md`, `STAGE_PLAN.md`, and `DECISION_LOG.md` with a compact, reusable project state.

### 4. Add An Experiment

Create a card:

```bash
python ~/.codex/skills/sci-experiment-manager/scripts/generate_experiment_card.py E001 "baseline experiment"
```

Then ask Codex:

```text
Use sci-experiment-manager. Update E001 with the real config path, run path, result path, status, paper role, tags, and one-line summary. Do not invent missing metrics.
```

### 5. Map Claims To Evidence

After results exist, ask:

```text
Use sci-paper-manager. Add the supported claims to CLAIM_EVIDENCE_MAP.md and mark unsupported claims as needs verification.
```

This keeps draft text from drifting beyond the experiment evidence.

### 6. Audit Before Writing Or Submission

Run the consistency checker from your project root:

```bash
python ~/.codex/skills/sci-result-auditor/scripts/check_project_consistency.py
```

Then ask:

```text
Use sci-result-auditor. Review the generated consistency report and tell me which claims, experiment cards, or index rows need repair before I write the paper.
```

## Typical Workflow

1. Capture the research direction in `PROJECT_HANDOFF.md`.
2. Use `QUERY_MAP.md` to retrieve only the experiments relevant to the current task.
3. Record each experiment in a card and in both experiment indexes.
4. Link paper claims to experiment IDs in `CLAIM_EVIDENCE_MAP.md`.
5. Keep unsupported ideas marked as `uncertain`, `preliminary`, or `needs verification`.
6. Use result auditing before major paper writing, rebuttal work, or submission formatting.

## Privacy Checklist Before Publishing Your Own Project

Before publishing a repository that used these skills, check for:

- credentials, API keys, tokens, SSH keys, and `.env` files
- personal names, emails, phone numbers, private server addresses, and local absolute paths
- private dataset paths, unpublished raw logs, checkpoint files, and metric tables
- manuscript text containing unsupported claims, confidential reviewer content, or target-journal files with redistribution restrictions
- generated caches such as `__pycache__`, `.DS_Store`, `.pytest_cache`, and large binary artifacts

The skills in this repository are generic templates and workflow instructions. Your own project memory files may contain private research evidence and should be reviewed separately.

## License

MIT License. See [LICENSE](LICENSE).
