# Evidence Spine Guide

Use this reference when a paper reading risks becoming a list of sections,
modules, or results.  The goal is to reconstruct the paper's proof route.

## Spine Template

```text
1. Problem
2. Cause / gap claimed by the paper
3. Method principle
4. Mechanism or architecture
5. Main proof object
6. Ablation or diagnostic proof
7. Robustness / generalization proof
8. Failure cases and limits
9. Relation to other papers
10. Project-facing validation requirement
```

## How To Read A Figure Or Table

For each figure/table, write a proof card:

```markdown
### Figure/Table X

What it shows:
What a beginner sees first:
What to look at:
How to read the rows/columns/arrows/axes:
Comparison/control:
Paper claim supported:
What it does not prove:
Why it matters:
One-glance pointer:
```

The explanation should be readable without seeing the whole paper.  If a number
matters, explain the baseline, direction, and implication; do not just repeat
the number.

For beginner-facing packets, each proof card should include enough local
context that the reader understands the figure without knowing the surrounding
section of the paper.

## Claim Calibration

Use precise labels:

- `main evidence`: directly supports the paper's central claim.
- `ablation evidence`: isolates a component or design choice.
- `diagnostic evidence`: explains a mechanism but may not prove performance.
- `robustness evidence`: tests stability across settings.
- `negative or boundary evidence`: shows where the method fails.
- `unsupported from paper`: tempting claim not actually proven.

## Relation To Project Evidence

A paper can suggest:

- a hypothesis;
- a variable or cue to measure;
- a control experiment;
- a failure criterion;
- a diagnostic view;
- a route to stop.

A paper cannot by itself prove the user's project claim.  If the packet includes
project implications, label them as hypothesis, reference, diagnostic, or
experiment requirement.

## Red Flags

Stop and rebuild the spine if the output:

- starts with implementation details before explaining the problem;
- lists modules without explaining why each module exists;
- says "performance improves" without naming the baseline/control;
- uses a figure without explaining what the reader should inspect;
- uses a metric or dataset name without explaining what it measures;
- repeats a table's numbers without interpreting the direction and size of the
  comparison;
- treats a mature framework's built-in mechanism as the user's contribution;
- hides limitations or missing controls.
