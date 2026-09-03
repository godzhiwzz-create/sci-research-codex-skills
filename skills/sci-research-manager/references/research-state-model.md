# Research State Model

Use an existing project vocabulary when one is defined. Otherwise use this compact model. Keep lifecycle stage, experiment status, evidence status, claim strength, and direction decision in separate fields; do not compress them into one overloaded status.

## Lifecycle stages

| Stage | Question | Promotion gate |
|---|---|---|
| `idea_exploration` | Is the hypothesis coherent and distinguishable? | A falsifiable mechanism, controls, and stop gate exist |
| `minimal_probe` | Does the cheapest diagnostic expose the proposed signal/mechanism? | Predeclared signal survives controls |
| `formal_experiment` | Can stable evidence support a paper-facing statement? | Protocol, baseline, seeds, selection, and provenance are frozen |
| `result_analysis` | What does completed evidence actually support? | Confounds and competing explanations are resolved or disclosed |
| `paper_writing` | How should verified evidence form the argument? | Claims resolve to evidence at matching strength |
| `submission_prepare` | Are manuscript, artifacts, code, and venue rules consistent? | Compliance and reproducibility checks pass |
| `maintenance` | Can another session find, trust, and continue the work? | Navigation and handoff checks pass without damaging provenance |

Stages are task-local and may move backward when evidence exposes a new uncertainty.

## Project status

Use one of:

- `active`: research work is progressing.
- `paused`: deliberately inactive but resumable.
- `submission`: the central evidence is fixed and packaging/revision dominates.
- `maintenance`: no new scientific claim is being pursued in the current task.
- `archived`: historical and read-only by default.

## Experiment status

Use one of:

- `designed`: protocol exists; no authoritative result yet.
- `running`: execution is active.
- `partial`: execution produced some artifacts but did not satisfy the completion gate.
- `complete`: expected execution artifacts and provenance are available.
- `stopped`: execution or the route ended before completion.
- `superseded`: retained for history but replaced by a named canonical record.

Keep claim strength in its separate field below. An optional manuscript placement such as main result or ablation may be recorded, but it must not replace or upgrade claim strength.

## Evidence status

- `not_assessed`: execution state is known but scientific evidence has not been checked.
- `verified`: raw artifact, frozen protocol, extraction, and interpretation agree.
- `pending_artifact`: a result is reported but a required artifact is missing or unlocated.
- `protocol_mismatch`: compared artifacts use incompatible splits, metrics, selection, code, or evaluation rules.
- `unverifiable`: available material cannot establish the result or protocol provenance.

For legacy data, map `stop` to `stopped` and `session_result_pending_artifact` to `pending_artifact`. Do not mechanically map a legacy experiment status of `needs_verification`: retain the true run state and choose `pending_artifact` or `unverifiable` on the evidence axis after inspecting what is missing. A project with a stricter established vocabulary may preserve it, but must document the mapping and extend audit-tool allowed values explicitly. If an alias must participate in completion, verification, or claim-safety gates, also pass `--map-value FIELD=ALIAS:CANONICAL`; allowing a spelling alone never weakens a gate.

## Claim strength

- `main_claim`: formal evidence directly supports the central statement.
- `trend_only`: a limited average direction; avoid significance, robustness, or superiority language.
- `diagnostic_only`: mechanism/behavior evidence, not a performance contribution.
- `negative_boundary`: a reliable failure or scope boundary.
- `internal_exploration`: useful for decisions but not paper-facing.
- `unsupported`: omit or explicitly label as a hypothesis.

## Direction decision

- `continue`: mechanism and next minimal validation are clear.
- `redirect`: the problem remains but the current signal, interface, or explanation failed.
- `reference_only`: useful baseline/tool/insight, not the project's main method.
- `stop`: no supported role remains without a new hypothesis.
- `needs_literature`: mechanism is too uncertain to design a defensible probe.

## Failure-cause taxonomy

Use one or more of:

- `signal_mismatch`: the cue does not represent the needed factor.
- `task_mismatch`: the cue is meaningful but not for the target prediction.
- `interface_mismatch`: the role may be valid but is attached to the wrong decision layer.
- `supervision_mismatch`: the target or loss does not express the phenomenon.
- `carrier_mismatch`: the model/pipeline cannot naturally use the proposed mechanism.
- `target_domain_support_mismatch`: source/synthetic evidence does not transfer safely.
- `control_or_confound_failure`: a trivial baseline, leakage check, randomization, selection artifact, or another control explains the apparent effect.

Tie every failure label to observed evidence and an alternative explanation. A label is not itself a diagnosis.
