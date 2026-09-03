# Manuscript Stage Coordination Bridge

The bundled `academic-manuscript-writing` skill is the single authority for manuscript-stage selection, transition gates, prose standards, major/minor revision preservation, reviewer responses, clean/marked-up preparation, and manuscript-content handoff.

Use this lifecycle manager only to coordinate:

- project stage and durable handoff state;
- evidence hierarchy, claim status, experiment provenance, and external artifact identity;
- specialist routing outside manuscript prose;
- final-submission audit, disclosure review, portal-copy verification, and irreversible-action boundary.

For any request that creates, edits, audits, revises, responds for, or prepares the content of a manuscript:

1. invoke `academic-manuscript-writing`;
2. accept its selected manuscript stage and mutation boundary;
3. provide verified project evidence, canonical paths, and current external decision;
4. do not invoke another generic writing module in parallel;
5. receive its stage artifacts and record only durable state changes in the project handoff;
6. use [final-submission-audit.md](final-submission-audit.md) after the writing skill declares the content handoff complete.

The manuscript stages are:

`initial_draft / manuscript_polish / pre_submission_audit / major_revision_preserving / minor_revision_local / final_submission_audit / proof_correction`

Do not redefine these stages here. If the writing skill and project evidence disagree about the stage, stop and arbitrate using the editor/publisher decision, user instruction, and canonical handoff before mutation.
