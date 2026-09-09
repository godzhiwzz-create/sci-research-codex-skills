# Manuscript Writing and Polishing Standards

These standards govern `initial_draft`, `manuscript_polish`, and the shared prose used during revision. Apply the target venue's official requirements where they are stricter. Scientific truth and author intent take precedence over stylistic neatness.

Whole-manuscript execution checklists and deliverables apply to whole-stage tasks. For a bounded edit, apply the relevant scientific and prose standards to the affected content and dependencies without restarting the full checklist or implying stage completion.

## Shared scientific prose standard

### Establish the writing basis

Before drafting or materially restructuring, freeze a compact mainline card:

- scientific question and primary manuscript stance;
- one-sentence answer/contribution;
- ordered argument chain and contribution order;
- decisive evidence for each major claim;
- scope, competing explanations, and known limitations;
- canonical terminology, notation, metrics, and bilingual equivalents;
- target venue/article type and current official constraints.

For every major claim, maintain enough information to answer: `claim text and verb -> claim type -> supporting artifact -> protocol/condition -> boundary -> status`. Claim types include observation, comparison, association, intervention, causal mechanism, generalization, efficiency, and deployment. A claim without an artifact is a gap; a causal claim supported only by association is a mismatch. Do not compensate for either with stronger prose.

### Preserve the argument chain

The paper should read as one continuous scientific argument:

```text
problem and consequence
  -> gap in existing knowledge or practice
  -> precise question/hypothesis
  -> method or controlled study design
  -> evidence and comparisons
  -> interpretation
  -> scope, limitations, and contribution
```

Every section and figure/table must advance this chain. Do not turn the paper into a chronological experiment diary, a reviewer-response transcript, or a list of disconnected tests.

Assign each experiment or evidence block one primary manuscript role: phenomenon-establishing, mechanism-discriminating, robustness/reinforcement, consequence/method implication, or generalization/boundary. A result may support several discussions, but duplicating it across sections does not create additional evidence.

Use the argument architecture implied by the primary stance:

- empirical research: need -> unresolved question -> study -> finding -> implication -> boundary;
- method/system: task -> limitations of alternatives -> design and rationale -> fair evaluation -> reproducibility/cost/failure modes;
- hypothesis/mechanism: phenomenon -> competing explanations -> falsifiable hypothesis -> discriminating test -> rival explanations -> bounded conclusion;
- diagnostic/benchmark: unresolved behavior or decision -> controlled characterization -> negative/positive boundaries -> practical or scientific guidance;
- review/synthesis: scope and inclusion logic -> thematic synthesis -> disagreement/gap -> reasoned outlook.

These are reasoning checks, not mandatory section headings. If the evidence cannot complete the selected chain, expose the missing link rather than writing around it.

### Calibrate claims to evidence

- Use the strongest wording the verified evidence supports, neither hype nor unnecessary self-denial.
- Distinguish observation, comparison, association, diagnosis, mechanism, causation, generalization, and deployment readiness.
- State the dataset, protocol, metric, uncertainty, and candidate-set boundary where they materially limit a claim; do not stack defensive disclaimers into every sentence.
- Keep oracle or test-label diagnostics explicitly diagnostic. Keep exploratory, negative-boundary, and sensitivity results in their correct role.
- Do not let language polishing delete uncertainty, turn a mean comparison into universal superiority, or convert an intervention ranking into unique causal localization.

### Build paragraphs, not bullet dumps

Use a functional paragraph arc when appropriate:

1. topic or claim;
2. evidence or technical explanation;
3. interpretation and scope;
4. transition only when the next step is not already obvious.

Vary paragraph length with content. Avoid one-sentence fragments for substantive reasoning and avoid paragraphs that mix several unrelated claims.

A paragraph may perform context, gap, approach, result, comparison, interpretation, limitation, or transition, but should have one dominant job. Use a reverse outline when the full text is hard to judge: extract one sentence per paragraph and verify that the resulting sequence advances the paper's question without a topic appearing, disappearing, or changing meaning without explanation.

### Write naturally and directly

- Prefer concrete subjects and verbs over abstract nominalizations.
- Avoid repeated formulae such as “It is worth noting that,” “Importantly,” “Moreover,” or “This highlights” when the evidence can speak directly.
- Avoid mechanical signposting such as “Section 3 discusses...” inside the scientific narrative unless the venue or document structure genuinely needs a roadmap.
- Do not write “as described later,” “its expansion is provided in §...,” or similar forward references when a short local explanation is clearer.
- Avoid apology-like or legalistic prose in the manuscript. Put review-process explanations in the response letter.
- Do not compress technical content merely to make the paper shorter unless the author or venue imposes a limit. Remove repetition, not evidence or reasoning.
- Preserve the author's established terminology and voice across English and Chinese versions; maintain a terminology ledger when bilingual synchronization matters.
- Treat sentence-length targets, preferred voice, and phrase lists as diagnostics rather than quotas. Clarity and scientific precision outrank uniform sentence length.
- In English, prefer explicit subjects and verbs, use active voice for author actions and passive voice when the process or object is genuinely central, keep tense consistent by function, and do not use `significantly` without the intended statistical meaning.
- In Chinese, avoid translation-like word order, mechanical sequences such as “首先/其次/最后”, empty emphasis such as “值得注意的是”, and abstract praise unsupported by evidence. Natural Chinese may retain necessary context, conditions, explanatory clauses, and limited repetition; de-template editing must not become information deletion.
- For Chinese-to-English drafting, first extract claim, evidence, condition, comparison, implication, and limitation, then rebuild the English paragraph in the section's logical order. Do not translate sentence by sentence.

### Prevent manuscript contamination

Keep author instructions, review history, drafting notes, placeholders, experiment-planning prompts, audit counts, file provenance, and workflow explanations out of the scientific manuscript. A planning table cannot replace the prose needed to explain a scientific argument. Place unresolved facts in an internal gap list or explicit drafting placeholder, and remove every placeholder before a submission-ready state.

### Separate manuscript roles

- **Methods** owns reproducible protocol, parameter scope, sampling, training/evaluation procedures, metrics, and implementation facts.
- **Results** owns observations and prespecified comparisons, with only the methods detail needed to interpret them.
- **Discussion** owns interpretation, competing explanations, implications, limitations, and relation to prior work.
- **Response letter** owns why changes were made, reviewer history, and exact modification mapping.
- **Supplement** owns necessary detail or extended results that would interrupt the main argument, not evidence that the main claim requires to be intelligible.

## Section standards

### Title

- State the scientific problem and distinguishing setting precisely.
- Avoid unnecessary punctuation, stacked qualifiers, undefined acronyms, hype, or a title broader than the evaluation.
- Follow venue length/style requirements without sacrificing accuracy.

### Abstract

Cover, in a coherent compact sequence:

1. problem and consequence;
2. unresolved gap and setting;
3. what was done;
4. principal quantitative or qualitative findings from verified evidence;
5. bounded conclusion and contribution.

Do not introduce claims, datasets, or qualifiers absent from the paper body. Do not turn the abstract into a table of numbers or a limitation disclaimer.

### Introduction

- Establish why the problem matters, what existing work leaves unresolved, and the exact question this paper answers.
- Build the contribution list only after the gap and design make it necessary.
- Phrase contributions as scientific outputs supported by the paper, not project-management activities.
- Keep related-work detail sufficient to establish the gap; move exhaustive taxonomy to Related Work when present.
- Prefer a concrete problem, observation, or decision over a generic “recently attracted attention” opening. The transition from prior knowledge to the paper's exact question must be explicit.

### Related Work

- Organize by scientific relationship to the paper, not paper-by-paper summaries.
- For each group, explain what is established, the relevant assumption, and the remaining gap.
- Cite sources that directly support the claim. Do not use unrelated recommended citations as technical precedent; if retained for a narrow cross-domain analogy, say so accurately.
- Define the review scope and organize evidence by theme, assumption, mechanism, or disagreement. Each paragraph should end with a synthesis or boundary, not a courtesy list of papers.

### Methods

- Give enough detail to reproduce the study: data, splits, preprocessing, architecture, trainable/frozen components and state behavior, optimization, support/query rules, thresholds, metrics, uncertainty, and exclusions as applicable.
- Put definitions before first use and align them with code and aggregation order.
- Separate primary protocol, diagnostic oracle, sensitivity analysis, and external directional check.
- Avoid protocol dumps whose detail does not change interpretation; move exhaustive enumerations to supplement while keeping the decisive facts in the main text.
- Explain the method from input to output: inputs/constraints -> preprocessing or representation -> core operation -> training/inference or decision path -> outputs -> connection to evaluation. For each genuine module, state its motivation, mechanism, and evidential role; do not substitute a component inventory for technical flow.
- Define notation before reuse. Introduce every equation in prose and explain its operational meaning afterward. State assumptions, failure modes, and release/reproducibility scope without promising unverified resources.

### Results

- Follow the scientific question order, not execution chronology.
- Begin each subsection with the comparison or question, then report results, uncertainty, and cluster/event-specific departures before interpretation.
- Use tables for exact repeated comparisons, figures for patterns and relationships, and prose for the conclusion—not all three redundantly.
- Report negative and non-monotonic evidence where it changes the claim; do not bury it, but do not let a control dominate the mainline beyond its role.
- Organize decisive experiments as question/hypothesis -> comparison or intervention -> expected discriminating observation -> actual result -> supported boundary. Baselines, ablations, and stress tests must serve that question rather than appear because a standard table template expects them.
- Keep direct observations distinguishable from causal or mechanistic interpretation. Report effect size, evaluation unit, sample size and uncertainty when applicable; “higher” without the comparator and conditions is incomplete.

### Discussion

- Explain what the results support, plausible competing explanations, where the evidence generalizes, practical relevance, and material limitations.
- Keep limitations proportional and integrated. Avoid a wall of disclaimers that erases the demonstrated contribution.
- Distinguish evidence for a useful repair lever from proof of a unique anatomical or causal failure location.
- Practical value may be stated when connected to the tested workflow; do not equate a selected-tile budget with measured human labor or a directional check with deployment validation.
- Address credible competing explanations before broad generalization. A negative result should state what was not observed, what it rules out or fails to rule out, and how it changes the paper's boundary; do not hide it or manufacture a positive spin.

### Conclusion

- Reconnect the question, principal evidence, contribution, and bounded implication.
- Do not introduce new results, mechanisms, datasets, or deployment claims.
- Preserve the paper's value while matching the final evidence strength.

## Figure and table standardization

During whole-manuscript `manuscript_polish`, audit every figure and table as part of the argument, not as decoration. A local edit checks only affected items and dependencies.

- Each item has one purpose, is cited in order, and is understandable with its caption/notes.
- Use consistent typography, capitalization, abbreviations, colors, line weights, panel labels, dimensions, resolution, units, decimal precision, and metric direction.
- Prevent clipping, overlaps, line/text collisions, excessive blank space, illegible legends, and inconsistent axis scales.
- Captions state what is shown, evaluation unit/protocol where needed, uncertainty notation, and whether examples are illustrative or selected.
- Tables identify sample unit, aggregation, best-value highlighting rule, missing values, thresholds, and metric definition where ambiguity is possible.
- All numbers and visual encodings come from canonical evidence or the single-source generation path.
- Nearby prose should state what is measured, under which setting, the pattern that matters, and why that pattern bears on the section's claim. Avoid narrating every cell or repeating a caption without interpretation.

## Reference and cross-reference standardization

- Use the venue's citation and bibliography style and order.
- Verify title, author, venue, year, pages/article number, and DOI for added references.
- Place citations immediately after the supported claim and avoid one citation marker carrying unrelated claims.
- Resolve every figure, table, equation, section, supplement, data, and code reference after final compilation.
- Do not add references merely to increase count or remove author-approved/reviewer-requested references during unrelated polishing.
- Verify current venue rules and bibliographic requirements from official sources at the time of use. Do not treat remembered page limits, anonymity rules, response formats, or old Skill notes as current policy.

## `initial_draft` execution standard

Prioritize completeness and reasoning before surface polish.

1. Inventory verified claims, evidence, figures/tables, constraints, target venue, and missing information.
2. Freeze a one-sentence paper question and provisional mainline.
3. Select the primary manuscript stance and build the section and figure/table architecture around its evidence chain.
4. Draft evidence-bearing sections before presentation-only summaries when practical; write the abstract after the body stabilizes. Draft all major sections to readable completeness and mark unknown facts `needs_verification`.
5. Check global argument continuity and contribution/evidence alignment.
6. Only then perform a light language pass sufficient for author review.

Initial-draft deliverables include the manuscript/outline, claim/evidence gaps, figure/table plan, terminology ledger, and author decisions needed before polishing. Do not spend repeated cycles on typography while major scientific sections are missing.

For full-manuscript work, progress section by section against one frozen mainline and shared ledger. User confirmation may be used at meaningful scientific decision points, but do not impose a fixed directory, a mandatory brainstorming package, or a fresh agent per chapter unless the project or user requires it.

## `manuscript_polish` execution standard

Treat content as complete and preserve scientific meaning.

1. Confirm target venue and official template/conventions.
2. Run a reverse outline to detect disconnected sections, redundant claims, and missing transitions.
3. Standardize manuscript architecture, headings, section balance, figure/table placement, captions, references, declarations, and supplementary links.
4. Polish paragraph logic, sentence clarity, terminology, tense, voice, and concision without changing claim strength or evidence.
5. Render and visually inspect the complete manuscript, including cropped/zoomed figures and dense tables.
6. Reconcile source, rendered PDF, figures/tables, bibliography, and any bilingual version.

If a requested “polish” would materially rewrite the mainline, add a new contribution, remove a limitation, change a result interpretation, or require evidence, stop and propose a stage change instead of silently proceeding.

Polishing is a shape-preserving edit: retain hedges, conditions, comparator identities, metric precision, negative findings, and author-approved terminology. Removing hype is not permission to weaken a supported result, and improving fluency is not permission to upgrade association to causation. When bilingual versions exist, reconcile scientific content paragraph by paragraph rather than assuming similar length means equivalence.

## `pre_submission_audit` execution standard

This stage is read-only.

Audit:

- problem/gap/contribution continuity;
- claim/evidence and protocol compatibility;
- novelty and related-work positioning;
- methods reproducibility and statistical support;
- result/table/figure consistency;
- limitations and practical claims;
- title/abstract/conclusion alignment;
- citations/references, data/code statements, ethics/funding/conflicts/authorship;
- venue format, anonymity, source compilation, PDF rendering, and supplement;
- unauthorized external workflow-tool disclosure candidates.

Report each issue with severity, exact location, evidence, minimum repair, affected downstream artifacts, and required authority. Do not write replacement prose unless the user asks for a draft alternative; a draft alternative remains outside the canonical manuscript until selected.

Use `Blocker / Major / Minor` consistently:

- `Blocker`: submission-invalidating policy/file defect or a central claim with absent/incompatible evidence;
- `Major`: a material reasoning, reproducibility, statistical, literature-positioning, figure/table, or cross-document inconsistency;
- `Minor`: local clarity, style, notation, or presentation issue that does not alter the scientific conclusion.

The audit should include a reverse outline, claim/evidence ledger, title–abstract–introduction–results–conclusion closure check, terminology scan, current official venue-rule check, and rendered-file inspection. Diagnose first; author-selected repairs return to the owning stage.
