---
name: sci-paper-reader
description: Deep-read academic papers into source-grounded Chinese or bilingual understanding packets that explain the problem, prerequisites, method, evidence spine, figures/tables, limitations, relation to other work, and dated project implications. Use when the user wants to understand, translate, teach, compare, or turn a paper into Markdown, HTML, Word, Obsidian, or presentation-ready material. Keep literature evidence separate from project experiment evidence.
---

# SCI Paper Reader

Create a reusable understanding artifact, not an abstract paraphrase or bullet dump. Assume the reader is intelligent but may be new to the topic. Teach the minimum prerequisites needed to understand the method and proof.

## Ground the source first

1. Verify paper identity, source status, and available PDF/HTML/arXiv/DOI.
2. Mark uncertain authors, venue, year, identifiers, code links, or metrics `needs_verification`.
3. Use page, section, figure, and table anchors for exact claims.
4. Do not let the current project lens distort the paper's own argument.
5. Never turn a paper claim into project evidence.

Use `sci-literature-manager` for discovery/indexing and `sci-research-manager` when the reading changes project direction.

## Build Markdown first

Default to a Chinese `paper_understanding.md` unless the user specifies another language or format. Produce Markdown before HTML/PPT/Word/Obsidian so every derivative follows the same argument and evidence spine.

For a durable library, prefer:

```text
<category>/<paper-slug>/
  paper.pdf
  paper_understanding_YYYYMMDD.md
  paper_visual_YYYYMMDD.html
  assets/
  README.md
```

Preserve original figure aspect ratios. Treat visual crops as evidence objects, not decoration.

## Load only the needed reference

- Read [novice_depth_standard.md](references/novice_depth_standard.md) for a full beginner-readable packet.
- Read [packet_schema.md](references/packet_schema.md) before building a complete Markdown packet.
- Read [evidence_spine.md](references/evidence_spine.md) when proof logic, figures, or cross-paper relations are unclear.
- Read [html_visual_guidelines.md](references/html_visual_guidelines.md) before producing visual HTML.
- Run `scripts/check_html_assets.py <html>` after creating HTML.

## Reconstruct the evidence spine

Build this before writing derivatives:

`problem -> claimed cause -> method principle -> proof objects -> result/ablation interpretation -> limitation -> project implication -> next validation requirement`

If this chain is unclear, do not design slides or experiments yet.

## Produce the understanding packet

Cover:

1. Plain-language orientation and prerequisites.
2. Paper identity and source verification.
3. Why the problem exists and why prior methods are insufficient.
4. Core claim, assumed cause, and method principle.
5. Inputs, outputs, mechanism, training/supervision, and what is genuinely new versus inherited.
6. Figure/table reading cards: what is visible, how to read it, what comparison matters, what it supports, and what it cannot prove.
7. Main results, ablations/diagnostics, robustness/generalization, failure cases, and limitations.
8. Relation to predecessor, competitor, and follow-up papers.
9. Durable takeaways, common misunderstandings, and evidence boundaries.
10. A dated project attachment when relevant.

For full structure and field details, follow `references/packet_schema.md` rather than expanding this coordinator.

## Teach instead of naming

- Explain a term before relying on it.
- Use a small concrete example for abstract tasks or formulas.
- Unpack formulas symbol by symbol when they are central.
- Describe what the reader physically sees before interpreting a figure.
- State what baseline/row/column makes a result meaningful.
- Distinguish “the paper claims” from “the evidence supports”.
- Explain why each module exists and what would fail without it.

Do not compress away the reasoning ladder. “Concise” means remove repetition, not prerequisites, proof logic, limitations, or controls.

## Keep project implications separate and dated

Append:

```markdown
## Project Attachment: <project/topic>

- Date:
- Current project stage:
- Why this paper matters:
- What it supports as literature:
- What it does not support for our project:
- Hypotheses/diagnostics suggested:
- Required controls and evidence boundary:
- Decision: use / reference_only / verify_more / reject
```

This section may inspire a hypothesis but cannot create a project claim.

## Hand off to experiments carefully

Before `sci-experiment-manager` creates an ID, provide:

```markdown
## Literature-to-Experiment Brief

Hypothesis:
Theory:
Sources and verification status:
Variables/cues:
Required controls:
Minimal validation:
Success criterion:
Failure criterion:
Confounds/risks:
Do-not-do-next:
Recommended stage:
```

Do not create configs, runs, results, or experiment claims in this skill.

## Validate derivatives

- Ensure Markdown, HTML, slides, and Word outputs share one evidence spine.
- Verify every local visual asset exists and is non-empty.
- Preserve screenshot aspect ratio and readable resolution.
- Keep source and assistant-drawn diagrams visibly distinct.
- Recheck that figures/tables support the nearby explanation.
- Mark every unresolved source detail instead of inventing it.
