#!/usr/bin/env python3
"""Read-only consistency audit across research indexes, cards, claims, and handoffs."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ID_RE = re.compile(r"\b(?:E\d{3,}|F\d{3,}(?:-D\d{2,})?)\b", re.IGNORECASE)
PLACEHOLDER_VALUES = {"", "not available", "not available yet", "needs_verification", "needs verification"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--handoff", type=Path, help="Project handoff path")
    parser.add_argument("--query-map", type=Path, help="Experiment query-map path")
    parser.add_argument("--index-csv", type=Path, help="Experiment index CSV path")
    parser.add_argument("--claim-map", type=Path, help="Claim-evidence map path")
    parser.add_argument("--output", type=Path, help="Optional generated Markdown report")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--strict", action="store_true", help="Return failure when warnings exist")
    return parser.parse_args()


def resolve(root: Path, value: Path | None, candidates: list[str]) -> tuple[Path | None, bool]:
    if value is not None:
        path = value.expanduser()
        return (path if path.is_absolute() else root / path), True
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path, False
    return None, False


def first_value(row: dict[str, str], keys: tuple[str, ...]) -> str:
    lower = {str(key).strip().lower(): "" if value is None else str(value).strip() for key, value in row.items()}
    for key in keys:
        if lower.get(key):
            return lower[key]
    return ""


def is_external_or_placeholder(value: str) -> bool:
    normalized = value.strip().strip("`").lower()
    if normalized in PLACEHOLDER_VALUES:
        return True
    return urlparse(value).scheme in {"http", "https", "s3", "gs"}


def inspect_index(root: Path, path: Path) -> tuple[set[str], list[str], list[str], int]:
    ids: set[str] = set()
    errors: list[str] = []
    warnings: list[str] = []
    rows = 0
    try:
        stream = path.open(newline="", encoding="utf-8-sig")
    except OSError as exc:
        return ids, [f"Cannot read index CSV {path}: {exc}"], warnings, rows

    with stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            return ids, [f"Index CSV has no header: {path}"], warnings, rows
        for line, row in enumerate(reader, start=2):
            rows += 1
            experiment_id = first_value(row, ("experiment_id", "id"))
            if not experiment_id:
                warnings.append(f"Index line {line} has no experiment ID")
                continue
            experiment_id = experiment_id.upper()
            if not ID_RE.fullmatch(experiment_id):
                warnings.append(f"Index line {line} has nonstandard ID {experiment_id}")
            if experiment_id in ids:
                warnings.append(f"Duplicate experiment ID in index: {experiment_id}")
            ids.add(experiment_id)

            card = first_value(row, ("card_path", "card", "canonical_card"))
            if card and not is_external_or_placeholder(card):
                card_path = Path(card)
                if not card_path.is_absolute():
                    card_path = root / card_path
                if not card_path.exists():
                    errors.append(f"Index line {line} references missing card: {card}")

            raw = first_value(row, ("raw_result_path", "raw_result", "result_path"))
            if raw and not is_external_or_placeholder(raw):
                raw_path = Path(raw)
                if not raw_path.is_absolute():
                    raw_path = root / raw_path
                if not raw_path.exists():
                    warnings.append(f"Index line {line} references missing raw result: {raw}")
    return ids, errors, warnings, rows


def referenced_ids(path: Path | None) -> set[str]:
    if path is None or not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8", errors="replace")
    return {match.group(0).upper() for match in ID_RE.finditer(text)}


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Research Project Consistency Report",
        "",
        f"Generated at: {report['generated_at']}",
        f"Root: `{report['root']}`",
        "",
        "## Errors",
        "",
    ]
    lines.extend([f"- {item}" for item in report["errors"]] or ["- none"])
    lines.extend(["", "## Warnings", ""])
    lines.extend([f"- {item}" for item in report["warnings"]] or ["- none"])
    lines.extend(["", "## Summary", ""])
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "No source evidence was modified.", ""])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Project root is not a directory: {root}", file=sys.stderr)
        return 2

    handoff, explicit_handoff = resolve(root, args.handoff, ["HANDOFF.md", "PROJECT_HANDOFF.md"])
    query_map, explicit_query = resolve(
        root,
        args.query_map,
        ["research_workspace/experiments/QUERY_MAP.md", "experiments/QUERY_MAP.md"],
    )
    index_csv, explicit_index = resolve(
        root,
        args.index_csv,
        [
            "research_workspace/experiments/EXPERIMENT_INDEX.csv",
            "research_workspace/experiments/EXPERIMENT_INDEX.generated.csv",
            "experiments/EXPERIMENT_INDEX.csv",
        ],
    )
    claim_map, explicit_claim = resolve(
        root,
        args.claim_map,
        ["research_workspace/paper/CLAIM_EVIDENCE_MAP.md", "paper/CLAIM_EVIDENCE_MAP.md"],
    )

    errors: list[str] = []
    warnings: list[str] = []
    for label, path, explicit, required in (
        ("handoff", handoff, explicit_handoff, True),
        ("query map", query_map, explicit_query, False),
        ("experiment index CSV", index_csv, explicit_index, True),
        ("claim-evidence map", claim_map, explicit_claim, False),
    ):
        if path is None or not path.exists():
            message = f"Missing {label}" + (f": {path}" if path else "")
            if required or explicit:
                errors.append(message)
            else:
                warnings.append(message)

    index_ids: set[str] = set()
    index_rows = 0
    if index_csv is not None and index_csv.is_file():
        index_ids, index_errors, index_warnings, index_rows = inspect_index(root, index_csv)
        errors.extend(index_errors)
        warnings.extend(index_warnings)

    claim_ids = referenced_ids(claim_map)
    handoff_ids = referenced_ids(handoff)
    for experiment_id in sorted(claim_ids - index_ids):
        errors.append(f"Claim map references {experiment_id}, but the ID is absent from the index")
    for experiment_id in sorted(handoff_ids - index_ids):
        warnings.append(f"Handoff references {experiment_id}, but the ID is absent from the index")

    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(root),
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "index_rows": index_rows,
            "unique_index_ids": len(index_ids),
            "claim_referenced_ids": len(claim_ids),
            "handoff_referenced_ids": len(handoff_ids),
        },
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.json else markdown_report(report)
    if args.output:
        output = args.output.expanduser()
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(rendered, end="")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
