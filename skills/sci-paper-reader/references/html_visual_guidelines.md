# Visual HTML Deep-Read Guidelines

Use this reference before producing a browser-style paper understanding packet.
The HTML should feel like a guided reading artifact, not a plain Markdown dump.

## Core Rule

The HTML layout must follow the Markdown evidence spine.  Visual design cannot
replace reading.  First understand the paper; then design the page around the
proof route.

## Page Structure

Recommended order:

1. Hero section with English title and Chinese subtitle.
2. Paper identity block: authors, venue/year, source status, paper type, and
   verified metadata.
3. Abstract/front-page crop with detailed Chinese abstract interpretation.
4. "How to read this paper" navigation or route map.
5. Problem and gap section.
6. Method principle and step-by-step mechanism.
7. Assistant-drawn architecture/mechanism diagram.
8. Figure/table proof cards with original crops where useful.
9. Evidence spine and limitations.
10. Relation to other papers.
11. Dated project attachment.

## Visual Standards

- Preserve every screenshot/crop aspect ratio.  Do not stretch figures to fit a
  layout.
- Let the layout adapt to the image, not the other way around.
- Use captions that explain what the reader should learn from the figure.
- Use enough text for a reader who has not read the PDF.  Short labels alone
  are not enough.
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

## CSS/Layout Guidance

Prefer:

- a constrained reading width for prose;
- wide sections for diagrams and large figures;
- two-column layouts only when both columns have comparable density;
- proof cards where image and explanation are balanced;
- callout boxes for "what this proves" and "what it does not prove".

Avoid:

- stretching images;
- placing screenshots without explanation;
- tiny screenshots that cannot be read;
- walls of unstructured text;
- over-templated boxes where every section looks identical.

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

