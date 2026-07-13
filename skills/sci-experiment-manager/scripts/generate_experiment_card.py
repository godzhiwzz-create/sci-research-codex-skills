#!/usr/bin/env python3
"""Create a non-overwriting experiment or direction-family card."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


ID_RE = re.compile(r"(?:E\d{3,}|F\d{3,}(?:-D\d{2,})?)", re.IGNORECASE)
DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "experiment_card_template.md"


def slugify(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).strip().lower()
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value).strip("._")
    return value or "experiment"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment_id", help="E001, F012, or F012-D01")
    parser.add_argument("name", help="Human-readable experiment/family name")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument(
        "--cards-dir",
        type=Path,
        default=Path("research_workspace/experiments/cards"),
        help="Cards directory, relative to root unless absolute",
    )
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Card template")
    parser.add_argument("--dry-run", action="store_true", help="Show target without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    experiment_id = args.experiment_id.strip().upper()
    if not ID_RE.fullmatch(experiment_id):
        print("Experiment ID must look like E001, F012, or F012-D01", file=sys.stderr)
        return 2

    root = args.root.expanduser().resolve()
    cards_dir = args.cards_dir.expanduser()
    if not cards_dir.is_absolute():
        cards_dir = root / cards_dir
    template_path = args.template.expanduser().resolve()
    if not template_path.is_file():
        print(f"Template does not exist: {template_path}", file=sys.stderr)
        return 2

    name = args.name.strip()
    if not name:
        print("Experiment name cannot be empty", file=sys.stderr)
        return 2
    card_path = cards_dir / f"{experiment_id}_{slugify(name)}.md"
    rendered = template_path.read_text(encoding="utf-8")
    rendered = rendered.replace("{{ID}}", experiment_id).replace("{{NAME}}", name)

    if card_path.exists():
        print(f"Card already exists; not overwritten: {card_path}")
        return 1
    if args.dry_run:
        print(f"Would create: {card_path}")
        return 0

    cards_dir.mkdir(parents=True, exist_ok=True)
    try:
        with card_path.open("x", encoding="utf-8") as stream:
            stream.write(rendered.rstrip() + "\n")
    except FileExistsError:
        print(f"Card already exists; not overwritten: {card_path}")
        return 1
    print(f"Created {card_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
