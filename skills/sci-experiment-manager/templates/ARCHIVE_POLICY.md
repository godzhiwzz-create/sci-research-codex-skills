# ARCHIVE_POLICY

## Purpose

Preserve evidence while reducing storage cost.

## Keep Levels

| keep_level | Meaning | Required preserved metadata |
|---|---|---|
| submission_keep | Required for submission or rebuttal | card, config, result summary, logs, reproducibility notes |
| reproduce_keep | Needed to reproduce core evidence | card, config, result summary, command, seed |
| cold_archive | Not active but informative | card, config, summary, archive note |
| delete_large_files | Large files can be cleaned after review | card, config, summary, delete review |
| delete_candidate | Candidate for deletion after explicit user approval | metadata preserved before deletion |

Never delete metadata. Never delete files without explicit user instruction.

