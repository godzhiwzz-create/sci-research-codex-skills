#!/usr/bin/env python3
"""Generate EXPERIMENT_INDEX.generated.md from experiment cards.

This script does not overwrite the hand-edited EXPERIMENT_INDEX.md.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path.cwd()
EXP_DIR = ROOT / "research_workspace" / "experiments"
CARDS_DIR = EXP_DIR / "cards"
OUT_PATH = EXP_DIR / "EXPERIMENT_INDEX.generated.md"


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_bullet_value(text: str, key: str) -> str:
    match = re.search(rf"^- {re.escape(key)}:\s*(.*)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return "not available yet"


def parse_card(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = text.splitlines()[0].lstrip("#").strip() if text.splitlines() else path.stem
    match = re.match(r"(E\d{3,})\s*(.*)", title)
    exp_id = match.group(1) if match else path.stem.split("_", 1)[0]
    name = match.group(2).strip() if match else path.stem
    status_decision = extract_section(text, "Status Decision")
    paper_usage = extract_section(text, "Paper Usage")
    tags = extract_section(text, "Tags").replace("\n", " ").strip()
    return {
        "id": exp_id,
        "name": name or path.stem,
        "phase": first_nonempty_line(extract_section(text, "Stage")),
        "status": extract_bullet_value(status_decision, "status"),
        "paper_role": extract_bullet_value(paper_usage, "paper_role"),
        "key_finding": first_nonempty_line(extract_section(text, "One-line Summary")),
        "tags": tags,
        "card": str(path.relative_to(ROOT)),
    }


def main() -> int:
    if not CARDS_DIR.exists():
        print(f"No cards directory found: {CARDS_DIR}")
        return 0

    cards = sorted(p for p in CARDS_DIR.glob("E*.md") if p.is_file())
    rows = [parse_card(card) for card in cards]

    lines = [
        "# EXPERIMENT_INDEX.generated",
        "",
        "Generated from experiment cards. Review manually before copying into EXPERIMENT_INDEX.md.",
        "",
        "| ID | Name | Phase | Status | Paper Role | Key Finding | Tags | Card |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['name']} | {row['phase']} | {row['status']} | "
            f"{row['paper_role']} | {row['key_finding']} | {row['tags']} | {row['card']} |"
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

