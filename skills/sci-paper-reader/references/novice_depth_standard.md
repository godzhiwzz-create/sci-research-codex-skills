# Novice-Readable Deep Read Standard

Use this reference for every full paper understanding packet unless the user
explicitly asks for a brief preview.

## Core Standard

The output must be understandable to a smart reader who has not read the paper
and may not know the field.  It should feel like a patient senior researcher is
walking them through the paper, not like a reminder note for someone who already
knows the topic.

The packet should answer three layers:

1. **What is happening?** Define the problem, objects, variables, method steps,
   figures, and numbers.
2. **Why is it happening?** Explain the paper's causal logic: why old methods
   fail, why the new mechanism should help, why each control matters.
3. **How do we know?** Tie every claim to a figure, table, result, ablation, or
   limitation.

## Minimum Depth Requirements

For a full deep read, include all of the following unless the paper type makes a
section irrelevant.

### 1. Prerequisite Ladder

Before the method section, write a short "读这篇论文前需要知道" section:

- domain task in plain language;
- important objects and variables;
- what a baseline is;
- what metric(s) mean and whether larger/smaller is better;
- one simple example that lets a non-expert picture the task.

Do not assume the reader knows field abbreviations, dataset names, model family
names, loss names, or evaluation metrics.

### 2. Problem Story

Explain the problem as a story:

- What did people do before this paper?
- What worked about that old route?
- What was still painful, slow, inaccurate, expensive, unstable, or
  theoretically unsatisfying?
- Why would a researcher at the time believe a new method was needed?
- What must a new method prove to be convincing?

### 3. Concept Dictionary

For every recurring technical term, provide a concise definition and its role in
the paper.  Include formula symbols when relevant:

```text
Term / symbol:
Plain meaning:
Role in this paper:
Common misunderstanding:
```

### 4. Method Walkthrough

Do not list modules only.  For each method component, explain:

- input it receives;
- output it produces;
- why it is needed;
- what would break or weaken without it;
- whether it is new, inherited, or a design choice;
- how it connects to the next component.

When formulas appear, unpack them line by line:

- what each symbol means;
- what operation is being performed;
- what intuition the formula implements;
- what changes if a term is removed.

### 5. Figure/Table Teaching Cards

For every key figure/table, write a teaching card with:

- where the crop is from;
- first-glance description of what the reader sees;
- how to read rows, columns, arrows, axes, colors, blocks, or labels;
- what comparison/control makes the figure meaningful;
- what claim it supports;
- what it does not prove;
- why the figure matters in the paper's proof route;
- one "如果你只看一眼，就看这里" pointer.

If a table has metrics, explain metric direction, baseline, gap size, and why the
gap matters.  Do not merely repeat numbers.

### 6. Evidence Ladder

Separate evidence into levels:

- main performance evidence;
- ablation evidence;
- diagnostic/mechanism evidence;
- robustness/generalization evidence;
- efficiency/cost evidence;
- negative or boundary evidence;
- missing evidence.

For each level, say whether it is strong, partial, weak, or unsupported.

### 7. Misunderstandings And Boundaries

Add a section for:

- "这篇论文没有证明什么";
- "容易误读成什么";
- "后来大家常把它归因为什么，但本文证据其实只支持到哪里";
- "什么时候不该引用这篇论文".

### 8. Relation Map

Explain neighboring papers and methods with a map:

```text
Earlier work -> what this paper inherits
This paper -> what it changes
Later work -> what it enables or leaves open
Competing route -> why it differs
```

If exact related papers are not verified, mark them as `needs verification`
instead of inventing citations.

### 9. Reader Checkpoint

End with a self-check:

- If the reader remembers only three things, what should they be?
- What question should they be able to answer after reading?
- What should they still not claim without extra evidence?

## Length Guidance

Do not optimize for shortness.  A full packet should usually be long enough to
replace a first serious reading session:

- foundational or famous method paper: often 3,000-6,000 Chinese characters or
  more, plus figures/tables;
- dense theory/method paper: longer if formulas require unpacking;
- HTML/PPT: fewer words per screen/slide, but more screens/cards, with captions
  and teaching narration.

If the output becomes too long, split into sections or pages instead of deleting
the reasoning.

## Bad Output Signs

Rework the packet if:

- it mostly restates the abstract;
- it uses terms before defining them;
- figures appear without detailed explanation;
- tables repeat numbers without teaching the comparison;
- method modules are listed but not motivated;
- limitations are one or two generic sentences;
- a beginner would still need the original paper open to understand the main
  claim.
