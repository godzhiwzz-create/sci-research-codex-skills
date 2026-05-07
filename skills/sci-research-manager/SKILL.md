---
name: sci-research-manager
description: Preserve research direction and manage long-term SCI paper projects across idea exploration, minimal probes, formal experiments, result analysis, paper writing, submission preparation, and maintenance. Use when starting, resuming, planning, or redirecting an experiment-driven research project.
---

# sci-research-manager

## When to use this skill

Use this skill when:
- starting or resuming a research project;
- receiving a new research idea;
- deciding whether to explore or implement an idea;
- updating the project handoff document;
- summarizing current project stage;
- preventing research direction drift;
- preparing a next-step plan.

## Required reading order

1. `PROJECT_HANDOFF.md`
2. `research_workspace/project/STAGE_PLAN.md`
3. `research_workspace/project/DECISION_LOG.md`
4. `research_workspace/experiments/EXPERIMENT_INDEX.md`
5. `research_workspace/paper/CLAIM_EVIDENCE_MAP.md`

Read lightweight files first. Do not scan raw runs/logs/results unless the indexed context is insufficient.

## Context discipline policy

Keep startup context purposeful, then expand when the research decision requires it.

- Read only the current-stage, central-story, active-experiment, next-action, and risk sections when files become large.
- Do not read all experiment cards for ordinary stage planning.
- It is acceptable to inspect many cards or raw files when doing broad phase review, evidence audit, or exact metric verification.
- If more context is needed, expand in this order: handoff section -> index row -> experiment card -> raw file excerpt.

## Research-stage policy

Always classify the current task before acting.

### idea_exploration

- Goal: judge whether an idea is worth testing.
- Forbidden: direct complex engineering.
- Output: hypothesis, minimal validation, risks, success criteria, failure criteria, and whether to move to `minimal_probe`.

### minimal_probe

- Goal: test for signal with the lowest-cost experiment.
- Output: probe experiment design, run parameters, expected observation, and whether to enter formal experiments.

### formal_experiment

- Goal: produce paper-supporting evidence.
- Output: experiment matrix, configs, run plan, result record, and evidence mapping.

### result_analysis

- Goal: judge paper evidence from existing results.
- Output: trend summary, risks, missing evidence, and claim-evidence updates.

### paper_writing

- Goal: write from evidence.
- Output: paper text, figure/table plan, claim checks, and uncertainty markers.

### submission_prepare

- Goal: convert mature `draft_core` into target-journal submission files.
- Required first step: read official target-journal requirements, template, and submission checklist.
- Output: guideline notes, submission manuscript, cover letter, supplementary materials, checklist, compliance report, and revision package.
- Do not guess formatting requirements. Mark unverifiable requirements as `needs verification`.

### maintenance

- Goal: organize project assets and update lightweight memory files.
- Output: updated handoff, index, stage plan, decision log, and risk register.

## Anti-premature-engineering rule

When the user gives an early research idea, first produce:

1. hypothesis
2. theoretical motivation
3. related evidence from experiment cards
4. minimal validation experiment
5. success criteria
6. failure criteria
7. risks
8. recommendation: reject, refine, or move to `minimal_probe`

Do not create large modules, complete pipelines, formal method names, or paper claims at this stage.

## Handoff rule

`PROJECT_HANDOFF.md` is the highest-priority project memory. Update it when the central story, stage, active experiments, risks, claims, or next actions change.

Never rely on chat context as the only carrier of the research direction.

## No fabrication

Do not invent results, citations, datasets, metrics, conclusions, or evidence. Mark incomplete information as `uncertain`, `preliminary`, or `needs verification`.
