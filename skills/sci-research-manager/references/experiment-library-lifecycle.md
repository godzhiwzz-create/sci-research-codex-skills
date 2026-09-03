# Experiment Library Lifecycle

Read this reference when designing, registering, running, analyzing, retrieving, promoting, superseding, or auditing project experiments. Preserve an established project card format and ID namespace; apply this contract as the shared semantic layer rather than renumbering or relocating history.

`sci-research-manager` owns lifecycle integration, direction decisions, and evidence promotion. It may delegate card, run-record, and project-index implementation to `sci-experiment-manager`, which returns a typed handback and does not update shared canonical evidence or manuscript claims on its own.

## Ownership chain

```text
project question / literature brief
  -> frozen experiment card
  -> run directory + raw artifacts + exact code/config
  -> analyzed card interpretation
  -> project query/index route
  -> optional shared canonical registry promotion
  -> claim-evidence map / bounded manuscript packet
```

Each fact has one owner:

| Fact | Owner |
|---|---|
| Hypothesis, competing explanation, protocol, gates, interpretation | Experiment card |
| Metric value and uncertainty | Raw artifact plus exact extraction/aggregation code |
| Run progress and machine execution detail | Run record/log |
| Current five-axis state and canonical pointers | Project `EXPERIMENTS.tsv` |
| Project question-to-experiment retrieval | Project query map/index |
| Cross-session canonical evidence route | Shared result registry |
| Current project stage, blocker, active execution, next action | Project handoff |
| Paper-facing scope | Claim-evidence map |

Do not copy raw numbers into handoffs, shared registries, or prose as a new authority.

## Project interface

Every managed project must expose, through its README or equivalent current entry point:

1. canonical experiment root;
2. query/index entry point;
3. card location and stable ID convention;
4. raw result/run roots;
5. current versus historical/superseded boundary;
6. project handoff;
7. shared registry namespace, if used.
8. project `EXPERIMENTS.tsv`, or one explicitly mapped established equivalent, as the machine-readable current-state source for the five axes and canonical pointers.

These may be physical directories, symlinks, or legacy locations. Do not migrate them merely to obtain uniform paths. If legacy `EXPERIMENT_INDEX.csv/.md` files coexist with `EXPERIMENTS.tsv`, designate exactly one editable authority and generate or import the others as compatibility views.

## Keep five axes separate

Use the project's vocabulary when stricter. Otherwise map to:

| Axis | Values |
|---|---|
| Lifecycle stage | `idea_exploration / minimal_probe / formal_experiment / result_analysis / paper_writing / submission_prepare / maintenance` |
| Experiment status | `designed / running / partial / complete / stopped / superseded` |
| Evidence status | `not_assessed / verified / pending_artifact / protocol_mismatch / unverifiable` |
| Claim strength | `main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported` |
| Direction decision | `continue / redirect / reference_only / stop / needs_literature` |

`complete` means execution artifacts exist; it does not mean `verified`, `promoted`, paper-facing, successful, or scientifically positive. Negative and stopped experiments remain first-class evidence when their protocol is valid.

Historical cards remain immutable scientific/human records. `EXPERIMENTS.tsv` owns the current values of the five axes plus card/raw/protocol pointers and replacement ID. Do not bulk rewrite old card prose to synchronize mutable state; update the TSV and add a dated correction/addendum to a card only when scientific interpretation or provenance changes.

## State transitions

### 1. Question to designed experiment

Create an ID/card only when there is a falsifiable requirement. Before execution, freeze:

- hypothesis and competing explanation;
- dataset/version, split, access boundary, and exclusions;
- model/checkpoint, seeds, baseline and controls;
- metric definition, aggregation and uncertainty plan;
- checkpoint/threshold/hyperparameter/method selection rules;
- config, code revision, command and expected result path;
- promotion gate, stop gate, and `do-not-do-next`.

If literature triggered the experiment, link the literature-to-experiment brief. Literature is motivation or external evidence, not an experimental result.

### 2. Designed to running

Resolve protocol conflicts before starting. Record the exact run identity and execution location. During ordinary progress, update only the run record/card fields required to resume safely; do not repeatedly rewrite shared registries, claim maps, or project handoffs.

### 3. Running to complete

Completion requires the expected raw artifacts, exit state, config/command, code identity, and sufficient logs to distinguish success, partial completion, and interruption. A filename or chat report cannot establish completion.

### 4. Complete to analyzed evidence

Use the frozen metric/extraction method. Record separately:

- observed result and uncertainty source;
- what it supports;
- what it does not support;
- competing explanations and confounds;
- protocol deviations;
- evidence status and claim strength;
- direction decision and replacement/next experiment.

If protocol and raw artifact disagree, retain the run and mark `protocol_mismatch`; do not repair the story by relabeling the protocol after seeing the result.

### 5. Analyzed evidence to project retrieval

Update the project query/index so the experiment is discoverable by scientific question. The card remains the default human authority. A run may be complete and retrievable without entering the shared registry or manuscript.

### 6. Promotion to shared canonical evidence

Promote only when the evidence:

- supports or changes a paper-facing claim;
- becomes the canonical cross-session answer to a recurring question;
- replaces an earlier canonical item; or
- changes a material evidence warning.

The machine registry is `shared/experiments/RESULTS_REGISTRY.tsv`. It stores project, stable ID, question, canonical card, raw source, protocol/code anchor, statuses, claim role, selection warning, promotion reason, and verification date. `RESULTS_REGISTRY.md` is its generated/human view. Neither becomes a second experiment card or number table.

### 7. Supersession

Never renumber or rewrite historical experiments to match the new route. Mark the old card `superseded`, name the replacement and reason, preserve raw provenance, update active query routes, and update the shared registry only if its canonical target or warning changed.

## Selection and comparison safeguards

- Treat test-selected checkpoints, thresholds, methods, seeds, or hyperparameters as unsafe for a main claim unless the protocol explicitly defines a diagnostic oracle and labels it accordingly.
- Do not compare or pool results across incompatible datasets, splits, metrics, connectivity/matching rules, support/query definitions, or code paths.
- Separate training-seed, sampling/redraw, fold/cluster, and measurement uncertainty instead of collapsing them into one interval.
- Preserve failed, null, and negative controls. Do not rerun only to obtain a preferred direction; a new run needs a declared causal or uncertainty reason.
- A specialist analysis result must return through the card and provenance chain before promotion.

## Handoff to manuscript writing

Pass a bounded evidence packet containing:

- claim ID, allowed wording, and claim strength;
- canonical card and raw artifact/extraction source;
- dataset/split/metric/selection compatibility;
- uncertainty source and unit of analysis;
- contrary evidence and required limitation;
- frozen table/figure generator or source;
- unresolved gaps marked `needs_verification`.

The writing skill owns prose. It cannot promote evidence, broaden a claim, choose a favorable run, or change an experiment status. Any new manuscript assertion returns here for verification.

## Event-driven writes

| Event | Required | Conditional |
|---|---|---|
| Protocol designed | Card + project query route | Handoff only if this becomes the active next action |
| Run starts/progresses | Run record/card | Handoff only for active execution or blocker changes |
| Run completes | Raw artifacts + card + project `EXPERIMENTS.tsv`/query index | Registry/claim map only after analysis and promotion |
| Evidence verified | Card interpretation/status | Registry if canonical; claim map if paper-facing |
| Evidence superseded | Old/new card links + active query route | Registry/handoff when canonical route changes |
| Routine audit | Findings or repaired current navigation | No history rewrite or cosmetic mass update |

## Completion gates

- Designed: frozen card and gates exist before execution.
- Complete: raw artifacts and execution provenance exist.
- Verified: raw artifacts, frozen protocol, extraction, and interpretation agree.
- Retrievable: stable ID, canonical card, raw route, and project query entry resolve.
- Promoted: registry points to verified evidence with explicit scope/warnings.
- Manuscript-ready: the bounded packet supports the exact claim at a compatible protocol and strength.
