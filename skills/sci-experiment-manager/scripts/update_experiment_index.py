#!/usr/bin/env python3
"""Generate reviewable Markdown and CSV indexes from active experiment cards."""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import tempfile
from pathlib import Path


ID_RE = re.compile(r"\b(?:E\d{3,}|F\d{3,}(?:-D\d{2,})?)\b", re.IGNORECASE)
ARCHIVE_PARTS = {"archive", "_archive", "archived"}
FIELDS = [
    "experiment_id",
    "name",
    "stage",
    "status",
    "evidence_status",
    "claim_role",
    "key_finding",
    "card_path",
    "raw_result_path",
]


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_bullet(text: str, key: str) -> str:
    match = re.search(rf"^- {re.escape(key)}:\s*`?([^`\n]*)`?\s*$", text, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        value = line.strip().lstrip("- ")
        if value:
            return value
    return "not available yet"


def parse_card(path: Path, root: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    title = lines[0].lstrip("#").strip() if lines else path.stem
    match = ID_RE.search(title) or ID_RE.search(path.stem)
    if not match:
        return None
    experiment_id = match.group(0).upper()
    name = title[match.end() :].strip(" -_") if ID_RE.search(title) else path.stem
    identity = extract_section(text, "Identity")
    paper_usage = extract_section(text, "Paper Usage")
    provenance = extract_section(text, "Provenance")
    status_decision = extract_section(text, "Status Decision")
    stage = extract_bullet(identity, "Stage") or first_nonempty_line(extract_section(text, "Stage"))
    status = extract_bullet(identity, "Status") or extract_bullet(status_decision, "status")
    evidence_status = extract_bullet(identity, "Evidence status")
    claim_role = extract_bullet(paper_usage, "Claim strength") or extract_bullet(paper_usage, "paper_role")
    raw_result = extract_bullet(provenance, "Raw result") or extract_bullet(text, "Result path")
    return {
        "experiment_id": experiment_id,
        "name": name or path.stem,
        "stage": stage,
        "status": status,
        "evidence_status": evidence_status,
        "claim_role": claim_role,
        "key_finding": first_nonempty_line(extract_section(text, "One-line Summary")),
        "card_path": str(path.relative_to(root)),
        "raw_result_path": raw_result,
    }


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(content)
        temp_name = stream.name
    os.replace(temp_name, path)


def markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# EXPERIMENT_INDEX.generated",
        "",
        "Generated from active experiment cards. Review before promoting into a hand-edited canonical index.",
        "",
        "| ID | Name | Stage | Status | Evidence | Claim Role | Key Finding | Card | Raw Result |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        values = [
            row["experiment_id"],
            row["name"],
            row["stage"],
            row["status"],
            row["evidence_status"],
            row["claim_role"],
            row["key_finding"],
            row["card_path"],
            row["raw_result_path"],
        ]
        lines.append("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in values) + " |")
    return "\n".join(lines) + "\n"


def csv_text(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument(
        "--cards-dir",
        type=Path,
        default=Path("research_workspace/experiments/cards"),
        help="Cards directory relative to root unless absolute",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("research_workspace/experiments/EXPERIMENT_INDEX.generated.md"),
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=Path("research_workspace/experiments/EXPERIMENT_INDEX.generated.csv"),
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse and report without writing")
    return parser.parse_args()


def resolve(root: Path, path: Path) -> Path:
    return path.expanduser() if path.is_absolute() else root / path


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    cards_dir = resolve(root, args.cards_dir)
    if not cards_dir.is_dir():
        print(f"No cards directory found: {cards_dir}")
        return 0

    cards = [
        path
        for path in cards_dir.rglob("*.md")
        if not any(part.lower() in ARCHIVE_PARTS for part in path.relative_to(cards_dir).parts)
    ]
    parsed = [parse_card(path, root) for path in sorted(cards)]
    rows = sorted((row for row in parsed if row is not None), key=lambda row: row["experiment_id"])
    if args.dry_run:
        print(f"Parsed {len(rows)} active cards; no files written.")
        return 0

    markdown_output = resolve(root, args.markdown_output)
    csv_output = resolve(root, args.csv_output)
    atomic_write(markdown_output, markdown(rows))
    atomic_write(csv_output, csv_text(rows))
    print(f"Wrote {len(rows)} rows to {markdown_output} and {csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
