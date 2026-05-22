# Paper Understanding Packet Schema

Use this reference when the user wants a serious paper understanding artifact
rather than a short summary.

## Production Rule

Write the Markdown packet first.  HTML, PPTX, Word, and Obsidian outputs are
derivatives of the Markdown proof route, not separate summaries.

The main body explains the paper itself.  Project-specific interpretation goes
at the end under a dated project attachment so future projects can reuse the
reading without inheriting today's project lens.

## Required Packet Sections

### 0. Paper Identity

Include:

- English title as the main title;
- Chinese subtitle or translation;
- authors;
- venue or journal, year, and source status;
- paper type: method, dataset, theory, benchmark, review, or system paper;
- field and literature line;
- DOI, arXiv, OpenReview, publisher, project page, or PDF path when verified;
- journal partition notes only when relevant and verified.

If it is a conference paper, say that JCR/CAS journal partitions do not apply.
If venue/source metadata is uncertain, mark it as `needs verification`.

### 1. Abstract Screenshot And Abstract Interpretation

When the PDF is available, include a first-page or abstract crop in visual
outputs.  In Markdown, record the asset path.

Interpret the abstract in Chinese:

- what problem the paper says it solves;
- why existing methods are insufficient;
- the core idea;
- what the paper claims as output or improvement;
- hidden assumptions in the abstract;
- what the abstract does not prove.

This section should be detailed enough that a reader can understand the paper's
promise before reading the method.

### 2. One-Minute Explanation

Answer in plain Chinese:

- What is the paper trying to solve?
- What is the key insight?
- What changes compared with prior work?
- What evidence should the reader inspect first?
- What is the most important limitation?

### 3. Background And Gap

Explain the field context, not just a phrase from the introduction.

Include:

- what earlier approaches assumed;
- what breaks or remains unsolved;
- why this gap matters in practice;
- what a successful solution must prove.

### 4. Core Claim And Method Principle

Separate:

- paper claim;
- inferred mechanism;
- method principle;
- actual implemented components.

Avoid treating a module name as the idea.  State the modeling principle behind
the module.

### 5. Method Route

Describe:

- input;
- representation or intermediate variables;
- main modules and why each exists;
- training targets and losses;
- inference output;
- which parts are inherited from prior work;
- which parts are new according to the paper.

Use a diagram when the method has more than two moving parts.

### 6. Figure And Table Reading Guide

For each important figure/table, write:

- where it appears;
- what visual element or number to look at;
- what comparison/control makes it meaningful;
- what claim it supports;
- what it does not prove;
- whether the evidence is main, diagnostic, ablation, robustness, or failure
  analysis.

Do not simply paste captions.  Teach the reader how to read the evidence.

### 7. Evidence Spine

Build a route:

```text
problem -> claimed cause -> method principle -> proof object
-> result/ablation interpretation -> limitation -> relation to other work
```

The evidence spine is the backbone of the packet and of any visual output.

### 8. Limitations And Hidden Assumptions

List:

- assumptions required by the method;
- dataset or evaluation limitations;
- failure cases;
- missing controls;
- what should not be claimed from this paper.

### 9. Relation To Other Papers

Explain:

- what the paper inherits;
- what it changes;
- which papers it competes with;
- what later work might adopt or reject;
- how it fits into a reading route.

### 10. Project Attachment

Put this at the end.  Include:

- date;
- project or route name;
- why the paper matters now;
- what it suggests as hypothesis, variable, control, diagnostic, or risk;
- what it does not support;
- next validation requirement.

Keep this section explicitly separate from the paper's own claims.

## Quality Bar

The packet should let a reader who has not opened the PDF understand:

- the paper's problem;
- the method route;
- the important figures/tables;
- why the evidence supports or fails to support the claim;
- how the paper relates to neighboring literature;
- how it can and cannot be used in a project.
