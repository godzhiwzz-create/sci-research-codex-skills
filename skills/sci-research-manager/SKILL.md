---
name: sci-research-manager
description: Preserve research direction and manage long-term SCI paper projects across idea exploration, root-cause direction design, minimal probes, formal experiments, result analysis, paper writing, submission preparation, and maintenance. Use when starting, resuming, planning, redirecting, or diagnosing a research project, especially when the user wants causes and architecture-level direction rather than local tuning.
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

## Skill coordination rule

This is the route-owner skill for long-term research projects. Specialist
skills such as `sci-literature-manager`, `sci-paper-reader`,
`sci-experiment-manager`, `sci-paper-manager`, `sci-result-auditor`,
`sci-asset-manager`, and paper-to-PPT skills must defer to the current project
handoff, local instructions, and this skill's stage decision. Use the
specialist skill for execution, but do not let a specialist workflow override a
stopped route or promote an unsupported claim.

If the mechanism is unclear or the user says the work should be paper-grounded,
route through `sci-literature-manager` and `sci-paper-reader` before designing
experiments.

## Direction exploration layer

This skill also owns the generic direction-exploration layer. Do not create a
separate project-specific exploration skill unless the user explicitly asks for
one.

Use this layer when the user asks:

- what new research direction may work;
- why a route failed at the root-cause level;
- how to turn a physical or methodological observation into a testable
  architecture idea;
- whether a route should be stopped, redirected, or moved to a minimal probe;
- how to compare multiple possible direction families.

The direction-exploration output should separate:

1. **Problem diagnosis**: the failure mode or unresolved mechanism.
2. **Existing evidence**: experiment cards, stopped routes, negative controls,
   and known guardrails.
3. **Hypothesis**: the new explanatory idea, not a module name.
4. **Architecture implication**: what kind of model/training/data structure
   would change if the hypothesis were true.
5. **Validation requirement**: what evidence is needed before training.
6. **Promotion gate**: what must be observed before implementation.
7. **Stop gate**: what result would kill the direction.

Direction exploration must prefer root causes over patching. It should not jump
from "this metric failed" to "tune a loss/head/gate"; it should explain what
the failure reveals about representation, supervision, data structure, domain
support, or evaluation.

### Direction-exploration pain-point guardrails

When the user asks for direction exploration, root-cause analysis, architecture
design, or asks "why did this fail?", apply these guardrails before proposing
any experiment or implementation.

**1. Restate the real user intent.**
Do not silently shrink the task. If the user is asking for a new paradigm,
root cause, or architecture-level explanation, say that explicitly and do not
answer with a local module, loss, head, gate, seed, or epoch plan.

**2. Start from "what assumption failed", not "which metric was bad".**
For each negative result, identify the falsified assumption. Classify the
failure cause as one or more of:

- signal mismatch: the proposed cue does not measure the needed factor;
- task mismatch: the cue may be meaningful but not for this prediction target;
- interface mismatch: the cue is placed at the wrong decision layer;
- supervision mismatch: the target/loss does not express the phenomenon;
- carrier mismatch: the chosen detector cannot naturally use the signal;
- real-domain support mismatch: synthetic evidence does not transfer safely;
- control/confound failure: RGB, metadata, shuffle, or detector-native stats
  explain the effect.

**3. Use a "do-not-do-next" list.**
After diagnosing a stopped route, explicitly list what must not be tried next.
Typical forbidden reflexes are: add epochs, add seeds, tune loss weights, tune
gates, add a verifier, insert a query residual, add a box delta, add a scalar
quality head, use a favored cue as mask/top-k/trust, or rescue the route by
switching to a stronger mature carrier without changing the research question.

**4. Separate reference tracks from main architecture tracks.**
Strong existing frameworks can be used as references, baselines, or analysis
tools. Do not let "a mature framework can do this better" become the project's
main contribution unless the user explicitly chooses a framework-adaptation
paper. If a route relies mainly on a mature framework's built-in mechanism, mark
it as `reference_probe` or `baseline_tool`, not the original architecture.

**5. Convert insertion questions into role questions.**
Do not ask "where do we insert this cue?" or "which head should use this signal?"
until the role is proven. First ask:

- What physical or statistical factor is this cue supposed to represent?
- Why did previous interfaces fail to use it?
- Is the cue a condition, target, context, diagnostic, or decision signal?
- What evidence would prove that role against RGB, metadata, detector-native
  statistics, and shuffle controls?

**6. Require an original-architecture gate.**
A proposed direction counts as architecture-level only if it changes at least
one of:

- representation factorization;
- supervision structure;
- matching/positive-quality decision;
- localization-quality representation;
- cross-domain or cross-density data relation;
- inference confidence semantics.

Adding a branch to an existing detector is not enough unless it changes one of
these core decisions and has a diagnostic showing why.

**7. Prefer cause-finding diagnostics over training.**
Before training, design the cheapest no-training or frozen-model diagnostic
that can distinguish the competing causes. Training is allowed only after the
diagnostic identifies a mechanism and a promotion gate.

**8. Be honest when the signal is the wrong one.**
If the evidence says the current signal does not explain the failure, say so.
Do not keep preserving a favored signal by demoting it from target to input to
context to scalar unless each new role has independent evidence.

**9. Produce a decision-grade output.**
A direction-exploration answer should end with one of:

- `continue`: clear mechanism and minimal probe;
- `redirect`: original problem remains, current signal/interface is wrong;
- `reference_only`: useful insight from a mature method, not main contribution;
- `stop`: no supported role remains under current evidence;
- `needs_literature`: mechanism unclear; read papers before designing.

### Required output shape for difficult direction questions

For hard route decisions, use this shape:

1. User intent restatement.
2. What I previously narrowed or mishandled.
3. Evidence ledger: supportive, negative, and confounded evidence.
4. Root-cause tree: what failed and why.
5. Reframed research question.
6. Architecture implication.
7. Validation requirements before implementation.
8. Do-not-do-next list.
9. Decision label: continue / redirect / reference_only / stop /
   needs_literature.

### CVPR-style direction loop

For a serious new-method direction, organize the exploration as a closed
research loop rather than a list of experiments. The loop is:

```text
problem -> cause -> method hypothesis -> mechanism/tool
-> validation requirements -> result interpretation -> next problem
```

Each loop iteration must answer the following questions.

1. **Problem: what exactly is unsolved?**
   - Name the failure mode, not just the dataset or metric.
   - State why existing methods or previous project routes do not solve it.
   - Example forms: confidence/localization mismatch, synthetic shortcut,
     sparse supervision, visibility-factor entanglement, real-domain support
     failure.

2. **Cause: why does the problem happen?**
   - State the mechanism-level explanation being tested.
   - Separate observed facts from inferred causes.
   - If multiple causes compete, list the alternatives and what would
     distinguish them.

3. **Method hypothesis: what new principle follows from the cause?**
   - Express the idea as a modeling principle, not a module name.
   - A good hypothesis says what should be represented, supervised, aligned,
     calibrated, disentangled, or matched differently.

4. **Mechanism/tool: what do we use to realize or measure it?**
   - Identify the signal, carrier, dataset structure, supervision, diagnostic,
     or architecture mechanism.
   - Clarify the role of each tool: condition, target, context, diagnostic,
     carrier, baseline, or control.
   - Do not confuse the tool with the method. A mature framework may be a
     reference or carrier; the method must still answer the project problem.

5. **Validation requirements: what must a later experiment prove?**
   - At the direction-exploration stage, state the requirement, not the full
     experiment protocol.
   - Specify which causes must be separated and which controls must be present:
     RGB-only, metadata-only, shuffle/random, detector-native stats,
     real-domain guardrails, and ablations that isolate the mechanism.
   - Define success and stop criteria before seeing results.
   - Hand off the actual experiment ID, card, config, run path, and result path
     planning to the experiment stage and `sci-experiment-manager`.

6. **Result interpretation: what did the result actually prove?**
   - Separate metric movement from mechanism evidence.
   - Mark whether the result supports the method hypothesis, only supports a
     reference/baseline effect, is confounded, or falsifies the assumption.
   - Do not promote source-only or synthetic-only gains into method claims.

7. **Next problem: what sharper question emerges?**
   - Every result should either close the loop or create a narrower next
     problem.
   - If the result is negative, report the reason category and the new
     unresolved cause.
   - If the result is positive, state what stronger control or real-domain
     check is needed before implementation or paper claims.

The direction loop should be written as a chain of reasoning. Avoid a flat
sequence such as "try A, then B, then C." Each next step must be caused by the
previous result.

### Repeated pain points to actively counteract

The direction-exploration layer exists because this project repeatedly drifted
into the following failure modes. Check these explicitly when advising the
user.

1. **Parameter-tuning reflex**: responding to a failed idea by adding epochs,
   seeds, loss weights, thresholds, gates, heads, or tiny interface tweaks.
2. **Narrow-interface vision**: reducing a paradigm-level question to "where
   can this signal be inserted?" instead of asking what representation,
   supervision, or decision should change.
3. **Forgetting the original goal**: optimizing local metrics while losing the
   user's larger aim of a CVPR-level low-visibility detection paradigm.
4. **Tool-as-method confusion**: treating a physical cue, a mature framework,
   an edge map, a detector carrier, or a diagnostic metric as the method instead
   of asking what problem they solve and what role they play.
5. **Positive-result chasing**: preserving a weak signal through new wrappers
   even after RGB, metadata, shuffle, detector-native stats, or real-domain
   guardrails explain it.
6. **Framework escape**: switching to a strong mature framework to get cleaner
   numbers without defining the project's own mechanism.
7. **Evidence compression**: summarizing "failed" or "works" without explaining
   the reason, assumption, confound, or next sharper question.

When any of these are likely, pause and return to the loop: problem, cause,
method principle, tool role, validation requirement, interpretation, next
problem.

### Direction-loop output template

Use this compact template when the user asks to explore, redirect, or rebuild a
research direction:

```text
Loop ID / direction name:
Stage:

1. Problem
2. Current evidence
3. Root-cause hypothesis
4. Method principle
5. Tools and roles
   - signal:
   - carrier:
   - supervision:
   - diagnostic:
   - controls:
6. Validation requirements, not full experiment protocol
7. Success criteria
8. Failure criteria
9. Expected result interpretations
10. Next problem if positive / negative
11. Decision label
```

## Required reading order

Default order:

1. `PROJECT_HANDOFF.md`
2. `research_workspace/project/PROJECT_PLAN.md` when present
3. `research_workspace/project/STAGE_PLAN.md`
4. `research_workspace/project/DECISION_LOG.md`
5. `research_workspace/experiments/EXPERIMENT_INDEX.md`
6. `research_workspace/paper/CLAIM_EVIDENCE_MAP.md`

Read lightweight files first. Do not scan raw runs/logs/results unless the indexed context is insufficient.

## Startup depth policy

Use the lightest startup that can safely answer the task:

- **quick status / simple answer**: read current-stage, central-story, next-action, and risk snippets from `PROJECT_HANDOFF.md`; add `QUERY_MAP.md` only if experiment lookup is needed.
- **planning / redirection / new idea**: read `PROJECT_HANDOFF.md`, `PROJECT_PLAN.md` when present, `STAGE_PLAN.md`, and the relevant query-map category.
- **experiment, paper, audit, deletion, submission, or path-sensitive work**: use the full required order and relevant cards.

If a project has strict local instructions such as `AGENTS.md`, follow those even when they require a heavier startup.

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
- If multiple related ideas are being explored, group them under a direction family instead of making each idea look like a formal experiment.

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

## Direction-family rule

For long-running projects, distinguish:

- **paper/phase line**: a manuscript or major research project such as P1/P2/P3.
- **experiment family**: a research question or route, e.g. `F012`.
- **sub-probe**: an early diagnostic inside a family, e.g. `F012-D03`.
- **formal experiment**: paper-supporting evidence with stable protocol and claims.

Exploration probes that only decide stop/go should not be promoted to the same level as formal validation experiments. If a direction stops, record the stop decision and blocked branches.

## Project-route-map rule

When the project has more than one active line, keep or update a compact route map such as `research_workspace/project/PROJECT_PLAN.md` with:

1. active, frozen, archived, and blocked lines;
2. remaining work for each paper line;
3. promotion gates for new directions;
4. remote/local ownership if relevant;
5. current stop list.

## Handoff rule

`PROJECT_HANDOFF.md` is the highest-priority project memory. Update it when the central story, stage, active experiments, risks, claims, or next actions change.

Never rely on chat context as the only carrier of the research direction.

## No fabrication

Do not invent results, citations, datasets, metrics, conclusions, or evidence. Mark incomplete information as `uncertain`, `preliminary`, or `needs verification`.
