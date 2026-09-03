# Final Submission Audit

Use this workflow only for a frozen submission package, portal staging, or a request to decide whether a manuscript is ready for final submission. It is a final responsibility gate, not a writing or revision workflow.

`sci-paper-manager` may prepare bounded checklists, requirement notes, and package inventories. `academic-manuscript-writing` owns manuscript content and stage completion. Neither specialist decides final readiness or performs an irreversible action; those decisions return to `sci-research-manager` and the author gate below.

## Authority and stopping rules

1. Audit is read-only by default. Do not repair files, upload, replace portal files, publish a repository/release, accept fees or terms, send correspondence, or submit unless the user separately authorizes that action.
2. Authorization to prepare, review, package, upload, or comply with venue requirements does not authorize the irreversible final submit action.
3. If a final action accepts publishing terms, article-processing charges, licences, declarations, or other legal commitments, show the exact consequence and request confirmation at the point of action.
4. Stop on an unresolved scientific mismatch, wrong or stale artifact, missing mandatory file, unapproved external tool disclosure, portal/local mismatch, or `needs_verification` item that affects submission truthfulness.

## Establish the frozen submission identity

Record before auditing:

- venue, article type, revision round, manuscript ID, deadline, and portal draft ID when available;
- canonical manuscript source and approved clean rendering;
- response, supplement, cover letter, figures, tables, marked-up manuscript, source archive, and public repository/release;
- package directory or archive, Git commit/tag, DOI/version, page counts, and SHA-256 hashes;
- which files are upload artifacts and which are internal reference-only files.

Do not treat a filename such as `final`, a desktop copy, or a recent modification time as proof of identity. Resolve same-name files by content, provenance, and hash.

For a revised submission, also require the previous submitted/round manuscript identity, mainline card, stable comment matrix, preservation report, unrequested-change report, clean/marked-up pair, and response-letter source. Missing revision provenance is a submission blocker until reconstructed or disclosed as `needs_verification`.

## Run the six audit gates

### Gate 1 — Scientific and response consistency

- Trace every revised headline number, table, figure, and material claim to the current canonical evidence and compatible protocol.
- Confirm that manuscript, supplement, response, cover letter, public code, and data/code statements make compatible claims.
- Check that every response claiming a change has the change in the stated location; identify manuscript changes not justified by an editor/reviewer request or an author-approved correction.
- Preserve the distinction between clean and marked-up manuscripts. The marked-up copy must contain the same substantive text as the clean copy and mark the intended content changes without becoming the primary manuscript.
- For a revision round, apply [manuscript-stage-workflows.md](manuscript-stage-workflows.md): confirm the correct major/minor stage, preservation threshold, mainline continuity, reviewer-response structure, and resolution of every unmapped or unmarked substantive change.

Use specialist writing, statistics, citation, document, or PDF skills only for their content domain. Their output does not bypass this consistency gate.

### Gate 2 — External workflow-tool disclosure review

Treat all potential disclosure of AI, generative AI, LLMs, agents, models/providers, coding or translation assistants, plugins, browser automation, code generators, and similar workflow tools as `not_authorized` unless the user approves it in the final submission review.

Inspect every external-facing artifact, including manuscript, supplement, response, cover letter, acknowledgements, data/code statements, repository README/CITATION/release, DOI metadata, email text, upload descriptions, and portal form fields. Run `scripts/scan_external_disclosures.py` on the assembled local package as the deterministic first pass. Its hits are candidates for human review, not proof of disclosure. Its coverage report is binding: `incomplete_scan`, any `skipped` expected artifact/member, or a supported format that could not be extracted blocks Gate 2 until rescanned or explicitly reviewed and recorded. `no_candidates_found` means only that no pattern matched the checked units; it is not author approval and does not cover portal-only fields.

For each candidate, report:

| Field | Required content |
|---|---|
| Tool or category | Exact named tool/provider or generic disclosure category |
| Exact wording | Complete sentence or field value; do not paraphrase |
| Location | File, page/section/line or portal field |
| Recipient/platform | Venue, editor, repository, DOI service, email, or other audience |
| Basis | Exact editor/venue requirement or author choice |
| Change from prior approved version | New, removed, reworded, moved, translated, or unchanged |
| Artifact identity | File name plus hash or portal file ID |
| Status | `not_authorized`, `authorized`, `mismatch`, or `not_applicable` |

The author may approve the complete inventory once during final review. Approval is limited to the listed wording, locations, recipients, and artifact version. A content change, translation, new destination, or additional disclosure invalidates that part of the approval. A byte-only rebuild may retain approval only after text, page count, and relevant rendered content are shown unchanged and the new hash is documented.

Ordinary scientific software and hardware required to reproduce the research—such as Python, PyTorch, CUDA, GIS software, statistical packages, or GPUs—remain part of the methods/reproducibility audit unless they are presented as workflow-assistance disclosures. Do not silently delete scientific-method information under this gate.

### Gate 3 — Files, rendering, and references

- Compile or render from the exact upload source using the venue-relevant path.
- Check page count, title, authors, abstract, figures, tables, equations, citations, cross-references, fonts, missing glyphs, blank pages, clipping, overlaps, and fatal/nonfatal build messages.
- Verify bibliography order/style and that added/removed references agree across source, rendered manuscript, response, and marked-up copy.
- Compare clean and marked-up substantive text. Explain intentional differences; block unexplained differences.
- Validate archive integrity and reject hidden, temporary, backup, internal-review, credential, private-data, or stale files.

### Gate 4 — Submission metadata and declarations

Cross-check the portal and frozen manuscript for:

- exact title, abstract, article type, review type, author order, spelling, emails, affiliations, corresponding author, equal-contribution notes, and contributions;
- ethics/consent, conflicts, funding and grant IDs, dual publication, third-party permissions, data availability, code availability, repository release/tag/commit, DOI, and supplementary descriptions;
- current venue requirements and any warning that affects the generated manuscript.

Record benign warnings with their evidence; do not dismiss warnings merely because compilation succeeded.

### Gate 5 — Package and portal-copy identity

- Generate one inventory of upload files and one separate list of internal reference-only files.
- Record SHA-256 for the frozen package and each material upload artifact.
- After upload, record portal file names, types, IDs, and generated-manuscript identity.
- When downloads are available, reverse-download the portal copies and compare hashes. If the platform transforms a file, compare extracted text, page count, images/layout, and relevant metadata, and document the transformation.
- Do not infer success from a toast, filename, or upload count. A same-name file may still be stale.

Any artifact changed after this gate must be rebuilt, re-inventoried, rechecked downstream, and reuploaded where applicable.

When the user authorizes package construction, build in this order:

1. freeze the canonical source and content-approved clean manuscript;
2. render/compile the exact upload source and compare it with the approved clean reference;
3. finalize the response, supplement, cover letter, figures/tables, marked-up manuscript, and public repository/release references;
4. separate upload artifacts from source/recovery/internal-reference artifacts so internal notes and backups cannot be uploaded accidentally;
5. generate the upload order/checklist, per-file SHA-256 manifest, package archive, and integrity test;
6. run all six gates on the assembled package before portal staging;
7. stage files in the portal only when authorized, then reverse-verify portal copies and the portal-generated manuscript;
8. present `ready_for_final_confirmation` and wait for at-action author confirmation.

The project-owned revision directory is canonical. A desktop or transfer copy is disposable and must be shown identical to the canonical package before use.

### Gate 6 — Author decision at the irreversible boundary

Present a compact final report containing:

1. submission identity and current portal state;
2. exact file inventory, pages, hashes, commit/tag/DOI, and portal-copy verification;
3. author/metadata/declaration summary;
4. external workflow-tool disclosure inventory and approval status;
5. warnings, unresolved items, and actions not taken;
6. the exact effect of the final button, including inability to edit, publishing terms, fees, licences, or declarations when applicable.

Use one final state:

- `blocked`: at least one required gate failed or remains materially uncertain;
- `ready_for_author_review`: audit is complete, but author review/approval is pending;
- `portal_staged_not_submitted`: files are uploaded and verified, but final action is not authorized;
- `ready_for_final_confirmation`: every gate passed and only at-action author confirmation remains;
- `submitted`: use only after the portal provides a submission receipt or equivalent proof.

Never convert `ready_for_final_confirmation` into `submitted` without executing the authorized action and verifying the receipt.

## Closeout

After an authorized submission, save or record the receipt, submission timestamp, manuscript ID, submitted-file inventory, portal-generated manuscript, and final hashes in the project-owned revision directory. Update the project handoff only after the external state actually changes. Do not place these records on the desktop as the canonical copy.
