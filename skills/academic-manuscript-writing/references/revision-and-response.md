# Major/Minor Revision and Reviewer Response

The objective is to satisfy the editor and reviewers completely and politely while preserving scientific accuracy, the submitted manuscript's identity, and the coherent mainline. Revision is controlled editing of an existing paper, not a new writing opportunity.

## Freeze the revision basis

For a full revision or when establishing/replacing its basis, record:

- exact decision letter and original reviewer comments;
- stable comment IDs;
- previous submitted manuscript/source and hash;
- current editable source and generated reference;
- revision type, deadline, venue requirements, and author decisions;
- mainline card: problem, stance, ordered contributions, evidence chain, limitations, terminology/metrics;
- comment–evidence–action matrix.

The matrix must include comment ID, request, Chinese working interpretation when needed, evidence, decision, experiment/data/code action, manuscript action, supplement action, response status, final location, and blocker.

For a bounded authorized edit, reuse the relevant submitted base, current source, stage and author/comment scope. A spelling-only correction does not require creating a complete decision letter, mainline card, comment matrix, preservation report or response package. Verify the exact text change and scientific meaning; leave the stage unchanged. A substantive change still needs its supporting evidence and affected dependencies.

Classify the response need without labeling the reviewer: `blocking_scientific / reproducibility_or_protocol / interpretation_or_scope / literature_or_novelty / presentation_or_minor / compliance`. Also record whether the issue is shared by several reviewers. This controls priority and duplication; it does not change the obligation to answer every subpart.

Do not edit the canonical manuscript until the user authorizes implementation when the task begins as review/planning only.

## Decide what may change

Classify every substantive change:

| Class | Allowed use |
|---|---|
| `reviewer_required` | Directly resolves a unique editor/reviewer requirement |
| `evidence_correction` | Corrects verified facts, numbers, protocol, metrics, citation, or overclaim |
| `consistency_propagation` | Synchronizes an approved change across dependent manuscript locations and external materials |
| `language_only` | Improves clarity/grammar without changing content; limited by revision stage |
| `author_requested_extension` | Adds an author-approved experiment, section, figure/table, or argument |
| `unmapped` | No justified source; do not integrate |

Reviewer service is the priority, but do not fabricate evidence, accept scientifically false premises, force irrelevant references into technical claims, or destroy the mainline. When declining or narrowing a request, answer directly, show the evidence, and offer the most helpful valid alternative.

For each substantive comment choose one explicit response action:

- `add_or_reanalyze`: supply requested evidence under a frozen protocol;
- `clarify`: the evidence already exists but the manuscript did not make it accessible;
- `correct`: replace a verified factual, numerical, protocol, citation, or interpretation error;
- `narrow`: align the claim's scope or verb with the available evidence;
- `defend`: retain a supported claim and explain the evidence/positioning more clearly;
- `decline_with_basis`: do not make an irrelevant, invalid, impossible, or policy-conflicting change, while addressing the underlying concern helpfully.

Do not default to defending every claim or narrowing every claim. The evidence decides. A reviewer request for a result does not justify inventing one; a novelty concern does not justify relabeling an empirical contribution as an algorithmic invention.

## Protect the mainline

For every proposed change ask:

1. Which comment, verified error, consistency dependency, or author decision requires it?
2. Which mainline step or contribution does it support?
3. Can a smaller insertion/replacement close the issue?
4. Does it introduce a new claim, module, experiment, figure/table, section, mechanism, or deployment implication?
5. Which abstract/results/discussion/conclusion/supplement/response locations depend on it?

Block or escalate the change if it has no mapped reason, if a local edit would suffice, or if it creates a new paper direction without author approval.

Keep these revision-process statements out of manuscript prose unless scientifically necessary:

- “In response to the reviewer...”;
- “We re-audited/reorganized...”;
- completion counts, internal checks, failed drafts, interrupted runs, or file-management history;
- explanations of why the authors changed wording.

Those belong in the response or internal audit. The manuscript should read as a self-contained scientific paper.

## Major revision: `major_revision_preserving`

A major revision may add substantial evidence, analysis, figures, tables, methods, and limitations when the review requires them. It does not authorize a global rewrite for stylistic preference.

- Preserve the section order, contribution order, argument spine, original experiments, and author voice unless a mapped scientific reason requires change.
- Prefer the smallest passage that closes the comment. Do not rewrite an entire paragraph when a sentence-level addition or correction is sufficient.
- Add a new experiment/module/section/figure/table only when requested, needed to correct evidence, or separately author-approved.
- Integrate new evidence into the existing question–method–result–interpretation chain; do not append a disconnected “reviewer experiment” section.
- Use the main text for decisive facts and the supplement for extended protocols/tables that would interrupt the narrative. Do not hide evidence required to understand a main claim.
- Retain original content that remains correct. Do not delete an experiment or figure merely because the new narrative seems cleaner.

Preservation report over comparable body text, excluding references and submission metadata:

- unchanged retained content;
- language-only retained content;
- substantively changed content;
- deleted content;
- added content;
- reordered sections/paragraphs/figures/tables;
- every substantive change not directly requested by an editor/reviewer.

Default target: at least 70% of original content retained unchanged or with language-only editing. Below 60% requires explicit `rewrite_authorized` approval. Necessary additions do not reduce the retained-original denominator. This diagnostic never protects known errors.

When a claim must be narrowed, update the smallest complete dependency chain needed for coherence—typically the claim sentence, the decisive evidence interpretation, and dependent abstract/introduction/discussion/conclusion wording. Do not respond with a parenthetical disclaimer patch, but also do not rebuild unrelated sections merely because a global rewrite would read more elegantly.

## Minor revision: `minor_revision_local`

Treat the accepted or nearly accepted scientific structure as frozen.

- Modify only the final comments, verified errors they expose, and strictly necessary consistency dependencies.
- Do not add experiments, sections, contributions, baselines, extensive literature discussion, or narrative restructuring unless explicitly requested or author-approved.
- Avoid unrelated whole-paper language polishing. Limit language changes to the touched passages and clear consistency errors.
- Target at least 90% retained original content. Any section deletion/reorder or mainline change requires author review.
- If a seemingly minor comment reveals a major scientific error, stop and report it rather than concealing it with wording.

## Revision execution order

This is the full revision sequence. A local task performs only its applicable steps; completion of that task does not trigger final packaging or stage advancement.

1. Parse and number the comments without losing qualifiers or subparts.
2. Audit existing evidence and manuscript locations.
3. Decide experiments/data/code/citation/protocol actions and obtain required author decisions.
4. Freeze any new experiment protocol before execution; verify results before prose.
5. Draft proposed manuscript changes in `_draft` or another project-approved staging area.
6. Integrate author-approved changes into the canonical manuscript in comment dependency order.
7. Propagate necessary consistency changes and update figures/tables/supplement/code/data statements.
8. Compile/render and verify scientific and visual integrity.
9. Generate preservation and unmapped-change reports against the previous submitted version.
10. Draft/finalize the response against the frozen clean manuscript.
11. Generate marked-up manuscript against the exact previous-round base.
12. Verify clean/marked-up/response/supplement/source equivalence and hand off to final audit.

Do not draft a polished final response before the changes and locations are real. A planning response may use explicit placeholders, but placeholders cannot enter the submission file.

## Reviewer-response structure and style

### Overall form

- Include journal, manuscript ID, exact title, authors, revision round, and a courteous opening.
- Thank the editor once and each reviewer once at the beginning of their block unless the author/venue requests another convention.
- Preserve every original comment verbatim. An internal Chinese translation may follow for author review but does not replace the English original in the external response.
- Keep stable comment IDs across drafts, tables, and response sections.
- Do not repeat editor requests that are truly identical to reviewer items; give a precise cross-reference while answering every unique element.

### Per-comment form

Use four explicit parts:

1. **Comment** — complete verbatim original, including subparts.
2. **Response** — answer first, then evidence, interpretation, action, and any scientifically necessary boundary.
3. **Corresponding changes** — reproduce the complete added/revised manuscript wording. When several locations changed, use clear bullets with each complete extract. Do not use an ellipsis or a vague summary instead of the modification.
4. **Location** — final clean manuscript/supplement section, page, table/figure, and stable line number when available.

When a figure or table is needed to understand the answer, include the complete relevant item or extract if permitted; otherwise identify it exactly and summarize only what is necessary.

### Response prose

- Be appreciative, direct, factual, and non-defensive.
- Avoid formulaic gratitude in every item, exaggerated agreement, reviewer-motive speculation, or accusations about citations.
- Lead with the outcome: “We added...”, “We clarified...”, “The existing evidence shows...”, or “We respectfully did not make this change because...”
- Distinguish what was newly added, reanalyzed from existing evidence, corrected, clarified, or intentionally not changed.
- Do not call a directional check validation, a finite candidate-set result universal, or a non-significant/low-sample pattern proof of stability.
- Do not mention internal errors or interrupted work unless scientifically material. State the verified current evidence and correction.
- Never claim a DOI, release, experiment, upload, manuscript location, or disclosure is complete until verified.
- Allocate detail by scientific risk: blocking evidence/protocol/claim issues receive the fullest answer; a misread receives a concise clarification with exact evidence; a correctable minor issue receives the change and location without consuming the space needed for the main concerns.
- For a supported challenge, state the paper's actual contribution and evaluation standard confidently, then show the evidence. For an unsupported part of the original wording, acknowledge and correct it without turning the entire response into an apology.
- Preserve negative results and non-monotonic patterns when they bear on the comment. Explain their role and boundary instead of hiding them or forcing a favorable interpretation.

### Editor and reviewer blocks

- Editor block: answer unique editorial/compliance requirements and summarize reviewer-resolution status without duplicating full technical responses.
- Positive/acceptance reviewer: thank once and record that no manuscript action was required unless a factual correction followed.
- Technical reviewer: answer every subpart with evidence and exact modifications.
- Novelty/impact reviewer: articulate the paper's verified contribution and relation to prior work without manufacturing algorithmic novelty or broad SOTA claims.
- Reproducibility/protocol reviewer: give the exact decision-relevant protocol in the main response, place exhaustive configuration detail in the manuscript or supplement as appropriate, and verify every location.
- Literature request: read and verify the source, state its actual relationship to the work, cite it where genuinely relevant, and otherwise explain the non-addition politely without speculating about motive.

## Clean and marked-up manuscripts

- Clean manuscript contains the final scientific text without tracked changes or colored revision markup.
- Marked-up manuscript is generated against the exact previous submitted/round version, not an intermediate draft.
- Mark the smallest substantive additions, deletions, and content changes. Do not highlight unchanged sentences because another sentence in the paragraph changed.
- Treat language-only changes according to venue requirements and author choice; never hide substantive changes as grammar.
- Highlight newly added references and the corresponding citation callouts when required.
- Compare extracted substantive text between clean and marked-up versions. Resolve any unexplained difference.
- Produce an unmarked-content-change report and close every item before final packaging.

## Completion gates

The entire revision stage is complete only when:

- all comment IDs are answered and their subparts closed or transparently declined;
- every reported number/protocol/citation resolves to verified evidence;
- mainline and contribution order remain coherent;
- preservation threshold and unmapped-change review pass;
- manuscript, supplement, figures/tables, response, data/code statements, and public artifacts agree;
- clean and marked-up manuscripts are substantively equivalent;
- corresponding changes and locations in the response match the frozen clean files;
- remaining author choices and external disclosure approvals are explicit;
- final-package handoff requirements are ready.
