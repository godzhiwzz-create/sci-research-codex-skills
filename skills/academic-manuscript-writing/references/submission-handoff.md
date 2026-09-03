# Final Submission Handoff and Proof Correction

This skill owns the manuscript-content handoff. The bundled `sci-research-manager` owns the full final-submission audit, artifact identity, disclosure gate, portal-copy verification, and irreversible-action boundary.

## Entering `final_submission_audit`

Do not enter final audit until manuscript content is frozen. Required handoff:

- venue, article type, manuscript ID, round, deadline, and portal state;
- canonical source and content-approved clean rendering;
- for revisions: exact prior submitted version/hash, mainline card, comment matrix, preservation report, unrequested-change report, and unmarked-change report;
- clean and marked-up manuscripts;
- response letter and editable source;
- supplement and source;
- figure/table files and generation/provenance path;
- cover letter when required;
- bibliography databases and venue styles/templates;
- author order, affiliations, correspondence, contributions, funding, conflicts, ethics/consent, data/code availability, repository release/tag/commit, DOI, and other declarations;
- author-approved external disclosure status or explicit pending items.

If any item remains scientifically unsettled, return to the owning manuscript/evidence stage. Do not label it a formatting fix.

## Final package construction contract

When the user authorizes package construction:

1. freeze the canonical content and sources;
2. compile/render from the exact source intended for upload;
3. compare the generated manuscript with the approved clean reference;
4. finalize response, supplement, figures/tables, marked-up manuscript, cover letter, bibliography, and source archive;
5. separate external upload artifacts from source/recovery/internal-reference artifacts;
6. generate an upload-order checklist, per-file SHA-256 manifest, package archive, and archive-integrity result;
7. run the `sci-research-manager` final-submission audit;
8. after separate authorization, stage portal files and reverse-download/compare them when possible;
9. present the complete portal state, declarations, warnings, disclosure inventory, fees/terms, and irreversible effect for author confirmation;
10. submit only after at-action confirmation and verify the receipt.

The canonical package remains in the project-owned revision directory. Desktop, email, cloud-transfer, or download copies are not authoritative and must be compared with the canonical package before use.

## Package deliverables

The venue determines exact file types, but the inventory should explicitly classify:

- primary manuscript source/upload;
- system- or locally generated clean reference;
- marked-up manuscript;
- point-by-point response;
- cover letter;
- figures and tables;
- supplementary information;
- bibliography/style/source dependencies;
- data/code/repository/DOI information;
- internal recovery sources and audit records that must not be uploaded.

Do not rely on filenames such as `final`, `new`, or `latest`. Use hashes and provenance. A same-name portal file can still be stale.

## Final content checks before handoff

- Title, abstract, main text, conclusion, figures/tables, supplement, response, and portal metadata agree.
- Author information and declarations match the manuscript and author decision.
- Every response location matches the final clean rendering.
- Clean and marked-up substantive text agree.
- References and citations resolve and added references are marked as required.
- No internal note, TODO, tracked comment, hidden backup, private material, credential, or stale source enters upload artifacts.
- External workflow-tool disclosure candidates are listed for the final author review; no unapproved change is silently carried forward.
- Venue rules, response/marked-up requirements, declarations, anonymity, file limits, and portal instructions have been verified against current official sources rather than inherited from an older template or memory.
- A final reverse outline and claim/evidence closure check show that package construction did not compress, reorder, or desynchronize the scientific mainline.

Compiling successfully is necessary but insufficient. Visual inspection and scientific-text comparison remain required.

## Proof correction

For `proof_correction`, compare the publisher proof with the accepted manuscript and record each correction as:

| Field | Content |
|---|---|
| Proof location | Page, column, paragraph, line, figure/table/equation/reference |
| Current proof text/state | Exact publisher rendering |
| Requested correction | Exact replacement or production action |
| Basis | Accepted manuscript, author metadata, source figure/table, or verified reference |
| Type | Typesetting, transcription, metadata, figure/table, equation, reference, or author query |
| Scientific impact | None, or requires separate author/venue escalation |

Do not introduce new analysis, results, citations, authorship changes, methods, or interpretations through proof correction. If the proof exposes a material scientific error, stop and use the publisher's formal correction route with author approval.

Close only after the corrected proof or publisher acknowledgement is verified and stored in the project-owned publication record.
