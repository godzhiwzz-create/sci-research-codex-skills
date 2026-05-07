---
name: academic-manuscript-writing
description: Academic paper and LaTeX manuscript drafting/revision focused on evidence-aware writing, section restructuring, figure/table narration, experiment-to-claim alignment, and journal-style English. Use when drafting or rewriting abstracts, introductions, related work, observation/results, mechanism analysis, discussion, conclusion, or when turning experiment folders into a manuscript evidence chain. Do not use for marketing/blog writing, bibliography lookup alone, or pure LaTeX build/debug tasks without writing intent.
---

# Academic Manuscript Writing

## What this skill is for
Use this skill to draft or revise academic manuscripts in English-first journal style. Use it to reshape sections around evidence, turn experiment folders into a claim-backed paper outline, and tighten figures and tables into argumentative prose.

## What this skill is not for
Do not use this skill for:
- marketing, blog, or general creative writing
- bibliography lookup alone
- LaTeX build or debug tasks without manuscript writing intent
- unrelated code refactoring

## Core workflow
1. Identify the manuscript goal: new draft, section rewrite, full restructure, or evidence/claim alignment.
2. Ground in source material before drafting. Inspect section files, figures, tables, and experiment assets. Classify each source as final, representative final, verified summary, raw verification source, or unsafe intermediate.
3. Build an evidence map. Record claim, supporting file, paper role, finality, and risk.
4. Assign a paper role to each experiment: phenomenon-establishing, mechanism-discriminating, reinforcement/robustness, consequence/method implication, or generalization/boundary.
5. Draft only after the evidence roles are fixed.
6. Prefer English manuscript output by default. Use Chinese only for planning, notes, or clarifying logic if needed.
7. Calibrate claims to the evidence. Prefer phrases such as “supported in this setting,” “among the tested mechanisms,” and “representative validation.”
8. Re-check whether each figure, table, or paragraph adds new evidence or only repeats existing results.

## Section-level writing rules
- Use `references/section-playbooks.md` for section-specific ordering.
- Keep the observation or results section compact unless the user explicitly asks for exhaustive reporting.
- Expand mechanism analysis more than the observation section when the paper is mechanism-driven.
- Let discussion explain what the evidence chain changes, not just restate results.
- Do not introduce new evidence in the conclusion.

## Evidence-handling rules
- Prefer paper-facing or final experiment directories over archive directories.
- Trust directory-level README status labels when present.
- Use raw result files to verify summaries, not to override stable paper-facing assets casually.
- Treat archived, placeholder, mixed-status, or guardrail-only material as unsafe until re-verified.
- Demote risky evidence to supplementary context or omit it if the main claim does not depend on it.
- Load `references/evidence-chain.md` when deciding whether an asset is final enough to cite.

## Figure/table narration rules
- Make each figure or table answer one argumentative question.
- State what is measured, what pattern appears, and why it matters.
- Avoid number dumping in prose.
- If a table only duplicates a figure, compress it or move it out of the main text.
- Use `references/figure-table-writing.md` for caption and prose patterns.

## Progressive disclosure map to references
- Read `references/workflow.md` for the end-to-end process.
- Read `references/section-playbooks.md` for section-by-section drafting logic.
- Read `references/evidence-chain.md` for finality and claim mapping.
- Read `references/figure-table-writing.md` for caption and narration patterns.
- Read `references/style-rules.md` for claim calibration and journal English.
- Read `references/examples.md` for compact before/after patterns.

## Validation checklist
Before finishing, confirm that:
- the manuscript goal is explicit
- each cited experiment has a role and finality status
- observation is compact and mechanism analysis carries the explanatory load
- claims are calibrated to the strongest evidence
- figure/table prose explains why the result supports the conclusion
- no intermediate or unsafe artifact is cited as final
