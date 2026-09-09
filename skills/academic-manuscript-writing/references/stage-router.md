# Stage Router and Agent Invocation

This reference decides what kind of manuscript work is authorized, which resources may be invoked, and when the manuscript may move to another stage.

## Determine the stage

Use evidence in this order:

1. an explicit editor/publisher decision or production notice;
2. the user's explicit description of the current round;
3. the requested deliverable and action verbs;
4. the canonical project handoff and manuscript state;
5. document maturity only when stronger signals are absent.

Choose the least mutating stage compatible with the evidence.

| Evidence/request | Stage |
|---|---|
| No complete manuscript; write from results, notes, outline, or Chinese draft | `initial_draft` |
| Complete manuscript; polish, standardize, improve figures/tables, apply template, refine English | `manuscript_polish` |
| Audit, self-review, rejection-risk check, verify before submission | `pre_submission_audit` |
| Editor says major revision or the comments require substantive new evidence/argument | `major_revision_preserving` |
| Editor says minor/final revision or requests narrow clarifications/corrections | `minor_revision_local` |
| Build/check final package, stage portal files, or decide submission readiness | `final_submission_audit` |
| Publisher proof, typeset correction, author proof query | `proof_correction` |

Special cases:

- “Modify/revise the paper” without a decision is ambiguous. Inspect the external decision and project state; if unavailable, ask before substantive mutation.
- A reviewer-response request inherits the actual major/minor revision stage. It is not a free-standing permission to rewrite the manuscript.
- “Rewrite” during a major or minor revision does not change the stage. Whole-paper rewriting requires explicit `rewrite_authorized` approval after showing preservation impact.
- A deadline never changes the stage or lowers a gate.
- When a task spans several stages, complete them sequentially. Do not edit while claiming to perform a read-only audit.

## Determine the manuscript stance and language mode

Stage selection controls what may change. The manuscript stance controls what kind of argument is being protected. Record both before writing:

- `empirical_research`: phenomenon/question -> controlled study -> finding -> implication;
- `method_or_system`: task -> design rationale -> fair evaluation -> reliability/cost/failure modes;
- `hypothesis_or_mechanism`: phenomenon -> competing explanations -> falsifiable hypothesis -> discriminating evidence -> bounded inference;
- `diagnostic_or_benchmark`: unresolved behavior/choice -> controlled characterization -> limits/decision guidance;
- `review_or_synthesis`: explicit scope -> organizing principle -> synthesis/disagreement -> open questions.

Use the author's actual paper and project rules, not the closest template, to decide the stance. Do not turn a diagnostic study into a leaderboard paper, a methods paper into an experiment diary, or an empirical comparison into a causal mechanism paper. For mixed papers, identify one primary stance and the subordinate role of the others.

Also record `source_language = en / zh / bilingual`. Chinese-to-English work translates the scientific intent and paragraph function, not Chinese syntax. A bilingual manuscript requires one terminology ledger and content synchronization; neither language is allowed to become a shortened summary of the other unless the author requests it.

## Stage permissions

| Stage | Structure | Scientific content | Language/style | External mutation |
|---|---|---|---|---|
| `initial_draft` | May build/reorder | Only from verified evidence; gaps explicit | Full drafting | None by implication |
| `manuscript_polish` | May refine for coherence/venue | Claims/results frozen unless separately reopened | Full claim-preserving polish | None by implication |
| `pre_submission_audit` | Read-only | Read-only | Read-only issue reporting | None |
| `major_revision_preserving` | Submitted structure preserved; local mapped changes | Reviewer/evidence/author-mapped changes | Local, voice-preserving | No upload/submit by implication |
| `minor_revision_local` | Frozen by default | Narrow mapped corrections | Local only | No upload/submit by implication |
| `final_submission_audit` | Frozen | Frozen | Diagnose only | Separate authorization required |
| `proof_correction` | Publisher layout only | No silent scientific change | Production corrections | Separate return/approval required |

## Main-agent and specialist invocation

The main agent always owns:

- stage determination and transition;
- canonical manuscript/source identity;
- mainline card and claim/evidence boundaries;
- final prose, terminology, section continuity, and response consistency;
- integration into canonical files;
- author-facing report and approval boundary.

Invoke a specialist only for a bounded need that the current stage permits:

| Need | Allowed specialist role |
|---|---|
| Literature/citations | Find and verify sources; do not write project results or change the mainline |
| Statistics/data validation | Verify calculations and uncertainty; do not choose a preferred result after seeing test outcomes |
| Figures/tables | Render or audit from canonical data and manuscript specifications; do not invent planning numbers |
| LaTeX/Word/PDF | Produce or inspect the authorized text/layout; do not edit scientific prose independently |
| Reviewer simulation | Read-only risk report; never directly rewrite the manuscript |
| Data/code availability | Verify repository/data facts and venue requirements; external release still needs authorization |
| Browser/portal | Read-only inspection or separately authorized staging; final submission remains a distinct confirmation |

Do not invoke a second generic manuscript-writing owner. Use specialists only for the bounded roles above.

## Subagent invocation

Follow the applicable project and system rules for delegation. A manuscript-stage label never grants permission to bypass those rules, and no parallel worker may edit the canonical manuscript concurrently.

When delegation is authorized:

| Stage | Permitted delegation | Prohibited delegation |
|---|---|---|
| `initial_draft` | Independent read-only evidence/citation checks; isolated section drafts against one frozen outline | Independent agents inventing different paper theses or editing the canonical source concurrently |
| `manuscript_polish` | Independent language, figure, citation, or layout audits | Multiple agents rewriting the same section or silently changing claims |
| `pre_submission_audit` | Independent read-only reviewer perspectives with one common evidence packet | Any agent modifying manuscript files during audit |
| `major_revision_preserving` | Read-only comment/evidence/protocol checks; bounded draft alternatives in `_draft` | Direct canonical edits, whole-paper rewriting, or separate agents redefining the mainline |
| `minor_revision_local` | Read-only verification of comments, citations, or locations | Parallel prose rewriting or restructuring |
| `final_submission_audit` | Independent read-only content, visual, metadata, or file-identity checks | Upload, release, terms acceptance, or final submit without exact authorization |
| `proof_correction` | Read-only comparison of accepted manuscript and proof | Uncoordinated scientific editing |

Every delegated result returns to the main agent as evidence, an issue list, or a draft alternative. The main agent must verify it against project rules and the canonical source before use. Do not use agent count as confidence.

## Transition conditions

These gates govern completion or advancement of an entire stage, not every local edit within it. Close a narrow authorized task after verifying its affected text/evidence and scope; leave the manuscript stage unchanged and report any broader unchecked work. Reuse an existing author-approved repair selection rather than asking for the same permission again.

### `initial_draft` → `manuscript_polish`

Require:

- complete end-to-end argument and all expected sections;
- each contribution linked to evidence or marked gap;
- methods, experiments, limitations, and conclusion present;
- figure/table plan and terminology stable enough to polish;
- primary manuscript stance recorded and preserved across title, abstract, section order, figures/tables, and conclusion;
- no hidden placeholder presented as a result.

### `manuscript_polish` → `pre_submission_audit`

Require:

- target venue/template identified and applied;
- claim wording, terminology, figures/tables, citations, references, and declarations internally consistent;
- manuscript compiles/renders without known fatal defects;
- scientific gaps found during polishing resolved or explicitly blocked.
- a reverse outline reads as one continuous argument, and claim/evidence/terminology ledgers contain no unresolved internal contradiction.

### `pre_submission_audit` → repair stage

The audit itself never edits. Use the author's issue selection or still-applicable repair authorization, then:

- language/layout/citation fixes return to `manuscript_polish`;
- a material missing argument or reopened science returns to `initial_draft` or the applicable experiment/evidence stage;
- after repair, return to `pre_submission_audit` and rerun affected checks.

### `pre_submission_audit` → `final_submission_audit`

Require no unresolved submission-blocking or major scientific issue, an author-approved final content state, and a complete expected deliverable set.

### External review → `major_revision_preserving` or `minor_revision_local`

Require the original decision/comments, exact prior submitted version, current source authority, deadline, and author decision to continue. Freeze them before edits.

### `major_revision_preserving` / `minor_revision_local` → `final_submission_audit`

Require:

- stable comment IDs and closed comment matrix;
- verified evidence for every numerical or protocol change;
- author-reviewed mainline and preservation/unmapped-change report;
- clean and marked-up manuscripts with substantive-text equivalence;
- final response with exact corresponding changes and locations;
- supplement, figures/tables, source files, data/code statements, and external metadata synchronized;
- no pending content decision disguised as formatting.

### `final_submission_audit` → submitted

Require every final audit gate, exact author confirmation at the irreversible action, successful submission, and a portal receipt. Uploading or reaching the Review page is not submission.

### accepted manuscript → `proof_correction`

Require the publisher proof and accepted-manuscript reference. Close only after the corrected proof is verified or the publisher acknowledges the correction list.

## Multiple simultaneous requests

Process by dependency, not convenience:

```text
evidence decision
  -> manuscript content
  -> figures/tables/supplement
  -> response and locations
  -> clean/marked-up pair
  -> pre/final audit
  -> portal staging
  -> final author confirmation
```

If a later step exposes a content error, return to the owning earlier stage and invalidate downstream hashes, page/line locations, marked-up files, response extracts, and portal copies that depend on it.
