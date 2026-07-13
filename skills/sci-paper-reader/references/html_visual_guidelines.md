# Visual HTML Deep-Read Guidelines

Use this reference before producing a browser-style paper understanding packet.
The HTML should feel like a guided reading artifact, not a plain Markdown dump.

## Contents

- Core rule
- Page structure
- Visual standards and figure crops
- Abstract and beginner teaching blocks
- CSS/layout guidance
- Validation

## Core Rule

The HTML layout must follow the Markdown evidence spine.  Visual design cannot
replace reading.  First understand the paper; then design the page around the
proof route.

Audience rule: write for a newcomer.  Every screen should teach one idea clearly
enough that a reader can continue without opening the PDF or already knowing the
field.  Screenshots make the page look professional only when paired with
detailed explanation.

## Page Structure

Recommended order:

1. Hero section with English title and Chinese subtitle.
2. Paper identity block: authors, venue/year, source status, paper type, and
   verified metadata.
3. Abstract/front-page crop with detailed Chinese abstract interpretation.
4. Prerequisite ladder: terms, task, metrics, and one concrete example.
5. "How to read this paper" navigation or route map.
6. Problem and gap section.
7. Method principle and step-by-step mechanism.
8. Assistant-drawn architecture/mechanism diagram.
9. Figure/table proof cards with original crops where useful.
10. Evidence spine and limitations.
11. Relation to other papers.
12. Dated project attachment.

## Visual Standards

- Preserve every screenshot/crop aspect ratio.  Do not stretch figures to fit a
  layout.
- Let the layout adapt to the image, not the other way around.
- Use captions that explain what the reader should learn from the figure.
- Use enough text for a reader who has not read the PDF.  Short labels alone
  are not enough.
- For each formula, table, or architecture block, add a plain-language
  explanation before or beside the visual.
- Avoid decorative cards that do not carry evidence.
- Use assistant-drawn diagrams for method flow, factorization, or relation maps
  when original figures do not explain the concept clearly.
- Keep text blocks scannable but substantive: explain the claim, mechanism,
  control, and limitation.

## Figure Crop Rules

Use original paper figures/tables only when they materially improve
understanding.  For each crop:

- store the file under `assets/`;
- use a descriptive filename;
- record the page/figure/table source when possible;
- include a proof-card caption;
- include a teaching paragraph that explains how a beginner should read the
  visual;
- do not crop so tightly that labels or axes become unreadable;
- do not use low-resolution screenshots when a better PDF crop is available.

## Abstract Section

The opening should include the abstract or first-page screenshot when available.
Then write a detailed interpretation:

- one paragraph for the problem;
- one paragraph for the proposed idea;
- one paragraph for claimed evidence/output;
- one paragraph for assumptions and what the abstract does not prove.

This prevents the artifact from becoming a shallow preview.

## Beginner Teaching Blocks

Use one or more of these blocks in HTML:

- `Before you read`: task, terms, metric direction, baseline.
- `What you are seeing`: first-glance description of a figure/table.
- `How to read it`: arrows, rows, columns, colors, axes, or formulas.
- `Why it matters`: link to the paper's claim.
- `What it does not prove`: boundary and missing controls.
- `Common misunderstanding`: what a non-expert may wrongly infer.

## CSS/Layout Guidance

Prefer:

- a constrained reading width for prose;
- wide sections for diagrams and large figures;
- two-column layouts only when both columns have comparable density;
- proof cards where image and explanation are balanced;
- callout boxes for "what this proves" and "what it does not prove".
- progressive sections: start simple, then add technical detail.

Avoid:

- stretching images;
- placing screenshots without explanation;
- tiny screenshots that cannot be read;
- walls of unstructured text;
- over-templated boxes where every section looks identical.
- assuming that the reader knows the metric, dataset, architecture family, or
  notation.

## Validation

After writing HTML, run:

```bash
python scripts/check_html_assets.py path/to/paper_understanding.html
```

Then open the HTML and inspect:

- no missing images;
- screenshots are readable;
- image aspect ratios look correct;
- text and figures do not overlap;
- the paper can be understood without returning immediately to the PDF.
- a newcomer can explain the problem, method intuition, main evidence, and
  limitations after reading the page.
