# SCI Research Codex Skills

Codex skills for long-term, experiment-driven SCI paper projects.

This package helps Codex act less like a one-off writing assistant and more like a research workflow partner: it keeps project direction stable, grounds new ideas in literature, retrieves experiment evidence with low context cost, prevents unsupported paper claims, and preserves enough metadata to make results auditable later.

## Skills Included

| Skill | Use it for |
|---|---|
| `sci-research-manager` | Project handoff memory, stage planning, decisions, risks, and direction control |
| `sci-literature-manager` | Paper discovery, library organization, reading-route maps, verification queues, and literature-to-experiment handoff |
| `sci-paper-reader` | Deep Chinese paper-understanding packets with problem route, method route, figure/table explanations, evidence spine, and project attachment |
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
cp -R sci-research-codex-skills/skills/sci-literature-manager ~/.codex/skills/
cp -R sci-research-codex-skills/skills/sci-paper-reader ~/.codex/skills/
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
  literature/
    indexes/
    paper_packets/
    reading_routes/
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

### 4. Build The Literature Layer Before Experiments

When a new idea is not yet mechanically clear, ask Codex:

```text
Use sci-literature-manager and sci-paper-reader. Build a paper-first reading route for this research problem. Do not design experiments until the papers produce a hypothesis, variables, controls, success criteria, failure criteria, and do-not-do-next list.
```

For a single important paper, ask:

```text
Use sci-paper-reader. Create a Chinese paper-understanding packet with abstract interpretation, method route, figure/table explanations, evidence spine, limitations, relation to other papers, and a dated project attachment at the end.
```

The paper packet explains the paper itself first. Project-specific implications belong at the end and must not become experiment evidence unless your own experiments verify them.

### 5. Add An Experiment

Create a card:

```bash
python ~/.codex/skills/sci-experiment-manager/scripts/generate_experiment_card.py E001 "baseline experiment"
```

Then ask Codex:

```text
Use sci-experiment-manager. Update E001 with the real config path, run path, result path, status, paper role, tags, and one-line summary. Do not invent missing metrics.
```

### 6. Map Claims To Evidence

After results exist, ask:

```text
Use sci-paper-manager. Add the supported claims to CLAIM_EVIDENCE_MAP.md and mark unsupported claims as needs verification.
```

This keeps draft text from drifting beyond the experiment evidence.

### 7. Audit Before Writing Or Submission

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
2. Use the literature layer when the mechanism is unclear or the user wants paper-grounded exploration.
3. Use `QUERY_MAP.md` to retrieve only the experiments relevant to the current task.
4. Record each experiment in a card and in both experiment indexes.
5. Link paper claims to experiment IDs in `CLAIM_EVIDENCE_MAP.md`.
6. Keep unsupported ideas marked as `uncertain`, `preliminary`, or `needs verification`.
7. Use result auditing before major paper writing, rebuttal work, or submission formatting.

## Direction Exploration Loop

The research manager now treats direction exploration as a closed loop:

```text
problem -> cause -> method hypothesis -> mechanism/tool
-> validation requirements -> result interpretation -> next problem
```

Use this loop when the user asks for a new architecture direction, root-cause
review, or why a line of experiments failed.  The expected answer is not a list
of local tweaks.  It should identify the failed assumption, compare supportive
and negative evidence, state what must not be tried next, and decide whether
the route should continue, redirect, become reference-only, stop, or go back to
literature.

## Paper Foundation Layer

The literature skills are independent from experiment records:

- `sci-literature-manager` owns paper discovery, source verification, library
  folders, reading queues, and problem-driven reading routes.
- `sci-paper-reader` owns serious paper-understanding artifacts: Markdown
  first, with optional HTML/PPT/Word derivatives built from the same argument
  route.
- Experiment IDs are created only after literature produces a concrete
  validation requirement.

This prevents the common failure mode where a paper, metric, or physical cue is
turned directly into a detector plug-in before its role has been established.

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
