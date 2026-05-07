#!/usr/bin/env python3
"""Generate a new experiment card without overwriting existing cards."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CARD_TEMPLATE = """# {experiment_id} {experiment_name}

## One-line Summary

not available yet

## Research Question

## Hypothesis

## Stage

idea_exploration / minimal_probe / formal_experiment / result_analysis

## Setup

- Teacher:
- Student:
- Dataset:
- Visibility levels:
- Seed:
- Epochs:
- Fraction:
- Config path:
- Run path:
- Result path:

## Key Results

Use tables only if real results exist.
If results are not available, write: not available yet.

## Interpretation

Use cautious language.
Do not overclaim.

## Paper Usage

- paper_role:
- candidate section:
- candidate table:
- candidate figure:
- related claim:

## Related Experiments

## Status Decision

- status:
- keep_level:
- archive decision:

## Notes

- uncertainties:
- risks:
- do-not-repeat:

## Tags

- 

## Raw File Links

- config:
- logs:
- results:
- weights:
"""


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "experiment"


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: generate_experiment_card.py E001 \"experiment_name\"")
        return 1

    experiment_id = argv[1].strip().upper()
    experiment_name = argv[2].strip()
    if not re.fullmatch(r"E\d{3,}", experiment_id):
        print("Experiment ID must look like E001, E002, ...")
        return 1

    cards_dir = Path.cwd() / "research_workspace" / "experiments" / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    card_path = cards_dir / f"{experiment_id}_{slugify(experiment_name)}.md"

    if card_path.exists():
        print(f"Card already exists, not overwritten: {card_path}")
        return 0

    card_path.write_text(
        CARD_TEMPLATE.format(experiment_id=experiment_id, experiment_name=experiment_name),
        encoding="utf-8",
    )
    print(f"Created {card_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

