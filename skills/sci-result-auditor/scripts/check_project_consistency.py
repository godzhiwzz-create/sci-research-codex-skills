#!/usr/bin/env python3
"""Check lightweight research project consistency without modifying sources."""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
WORKSPACE = ROOT / "research_workspace"
EXP_DIR = WORKSPACE / "experiments"
PAPER_DIR = WORKSPACE / "paper"
REPORT_PATH = WORKSPACE / "reports" / "consistency_check_report.generated.md"


def read_index_ids(index_csv: Path) -> tuple[set[str], list[str]]:
    ids: set[str] = set()
    warnings: list[str] = []
    if not index_csv.exists():
        return ids, [f"Missing EXPERIMENT_INDEX.csv: {index_csv}"]

    with index_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            exp_id = (row.get("experiment_id") or "").strip()
            if exp_id:
                ids.add(exp_id)
            card_path = (row.get("card_path") or "").strip()
            if card_path:
                full_path = ROOT / card_path
                if not full_path.exists():
                    warnings.append(f"Line {i}: missing card_path {card_path}")
    return ids, warnings


def claim_ids(claim_map: Path) -> set[str]:
    if not claim_map.exists():
        return set()
    text = claim_map.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"\bE\d{3,}\b", text))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        ROOT / "PROJECT_HANDOFF.md",
        EXP_DIR / "QUERY_MAP.md",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    index_ids, index_warnings = read_index_ids(EXP_DIR / "EXPERIMENT_INDEX.csv")
    warnings.extend(index_warnings)

    cmap = PAPER_DIR / "CLAIM_EVIDENCE_MAP.md"
    if not cmap.exists():
        errors.append(f"Missing required file: {cmap.relative_to(ROOT)}")
        referenced_ids = set()
    else:
        referenced_ids = claim_ids(cmap)

    missing_ids = sorted(referenced_ids - index_ids)
    for exp_id in missing_ids:
        warnings.append(f"CLAIM_EVIDENCE_MAP references {exp_id}, but it is absent from EXPERIMENT_INDEX.csv")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Consistency Check Report",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Errors",
        "",
    ]
    lines.extend([f"- {item}" for item in errors] or ["- none"])
    lines.extend(["", "## Warnings", ""])
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    lines.extend(["", "## Summary", ""])
    lines.append(f"- Experiment IDs in index: {len(index_ids)}")
    lines.append(f"- Experiment IDs referenced by claims: {len(referenced_ids)}")
    lines.append("- No source files were modified.")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

