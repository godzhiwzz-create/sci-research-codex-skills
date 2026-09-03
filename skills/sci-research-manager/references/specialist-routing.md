# Specialist Skill Routing

Select one primary owner and the smallest bounded specialist set. `sci-research-manager` owns research state and evidence promotion; `academic-manuscript-writing` owns manuscript stage, mainline, prose, and integration. Every other skill is a specialist for the current task.

Before delegation, define the input artifacts or IDs, allowed operation, prohibited state changes, required output type, and return destination. A specialist must return source paths, verified scope, limitations, and any proposed state change rather than applying that change to a canonical registry or manuscript on its own.

## Literature and paper understanding

| Need | Bundled default | Optional narrower specialist when installed |
|---|---|---|
| Paper discovery, identifiers, metadata, deduplication, versions, bibliography, and reading route | `sci-literature-manager` | `nature-academic-search` |
| Full source-grounded paper understanding | `sci-paper-reader` | `nature-reader` |
| CV baseline mining, critique, and gap/wedge finding | `sci-paper-reader` | `cv-paper-reading` |
| Project-specific synthesis from already verified claims | `academic-manuscript-writing` | `evidence-driven-writing` |

The identity chain is: a literature specialist resolves source identity and metadata; a paper-reading specialist inspects the selected source when full evidence is needed; the lifecycle owner records project tags, role, reading depth, bounded LiteratureClaim verification, and downstream links. Do not let a discovery result or paper summary become project experimental evidence.

## Experiment and quantitative work

| Need | Bundled default | Optional narrower specialist when installed |
|---|---|---|
| Stable experiment ID, frozen protocol, card, run closure, and project index | `sci-experiment-manager` | none required |
| Read-only protocol, result, claim, and cross-artifact consistency audit | `sci-result-auditor` | data-validation skills |
| Result-table/figure schema after the scientific protocol is frozen | `sci-experiment-manager` | `experiment-results-planning` |
| Statistical test selection and reporting | none required | `statistical-analysis` |
| Reproducible notebook | none required | `jupyter-notebook` or `data-analytics:jupyter-notebooks` |
| Structured data trustworthiness | `sci-result-auditor` | `data-analytics:analyze-data-quality` |
| Independent analysis validation | `sci-result-auditor` | `data-analytics:validate-data` |
| Metric-change or anomaly diagnosis | `sci-result-auditor` | `data-analytics:metric-diagnostics` |

Scientific hypotheses, controls, seeds, metrics, selection rules, promotion/stop gates, IDs, and evidence state remain with the lifecycle manager and experiment card. A computed result must return through card provenance and claim calibration before promotion.

## Manuscript, response, and submission artifacts

Read [manuscript-stage-workflows.md](manuscript-stage-workflows.md), then invoke `academic-manuscript-writing`. Do not invoke a second generic writing owner in parallel.

| Need | Prefer |
|---|---|
| Initial drafting, polishing, pre-submission audit, major/minor revision, reviewer response, clean/marked-up preparation, or proof correction | `academic-manuscript-writing` |
| Claim map, paper status, figure/table plan, or submission-artifact inventory | `sci-paper-manager`, bounded by the selected manuscript stage |
| Independent evidence/claim consistency report | `sci-result-auditor`, read-only |
| Explicit mock-referee report | an installed reviewer specialist, read-only |
| Citation placement or bibliography validation | an installed citation specialist |
| Data/code availability and FAIR planning | an installed data-availability specialist |

Resolve claim/evidence status before prose drafting. A citation, reviewer, document, or figure specialist may supply bounded evidence or artifacts but cannot own the paper mainline or enlarge the selected stage.

Stage defaults:

| Manuscript stage | Specialist boundary |
|---|---|
| `initial_draft` | The writing owner controls the complete argument; bounded evidence, figure, and citation specialists may support it. |
| `manuscript_polish` | Specialists standardize bounded artifacts without changing meaning, claim scope, or architecture. |
| `pre_submission_audit` | The writing owner produces the integrated read-only issue list; other reviewers add only read-only perspectives. |
| `major_revision_preserving` | The writing owner controls comment mapping, mainline preservation, manuscript changes, response, and clean/marked-up content. |
| `minor_revision_local` | Only local, comment-mapped changes are allowed; restructuring is disabled by default. |
| `final_submission_audit` | Use [final-submission-audit.md](final-submission-audit.md); specialists diagnose blockers but do not silently repair them. |
| `proof_correction` | The writing owner compares against accepted text; document/PDF specialists support production correction only. |

## Figures, documents, and presentation

| Need | Bundled default | Optional narrower specialist when installed |
|---|---|---|
| Exploratory quantitative chart | none required | `data-analytics:visualize-data` |
| Submission-grade quantitative plot | `sci-paper-manager` for the frozen data contract | a publication-figure skill |
| Method, architecture, or conceptual diagram | `sci-paper-manager` for the figure role | a research-figure skill |
| Paper-understanding presentation | `sci-paper-reader` | a paper-deck skill |
| Word, PDF, spreadsheet, or slide artifact | none required | the exact installed document specialist |

All figures and documents must consume canonical registered evidence. A rendered artifact is not a new scientific source.

## Assets, engineering, and remote actions

Use `sci-asset-manager` for a bounded retention, migration, archive, or delete review. It may produce a manifest and recommendation but cannot move or delete material without explicit authorization.

Use an exact platform specialist only when installed and authorized. Do not publish, push, submit, upload, click an irreversible control, or start costly remote work merely because a specialist can perform the action.
