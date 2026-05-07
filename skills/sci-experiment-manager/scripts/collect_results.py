#!/usr/bin/env python3
"""Collect results.csv files under runs/ into a lightweight master table.

This script does not fabricate results. If no results.csv files are found, it
prints a message and exits successfully.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path.cwd()
RUNS_DIR = ROOT / "runs"
OUT_PATH = ROOT / "research_workspace" / "experiments" / "master_results.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    if not RUNS_DIR.exists():
        print(f"No runs directory found: {RUNS_DIR}")
        return 0

    result_files = sorted(RUNS_DIR.rglob("results.csv"))
    if not result_files:
        print("No results.csv files found under runs/. Nothing collected.")
        return 0

    rows: list[dict[str, str]] = []
    fieldnames: list[str] = []
    seen: set[str] = set()

    for result_file in result_files:
        try:
            file_rows = read_csv(result_file)
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: could not read {result_file}: {exc}")
            continue
        for row in file_rows:
            row = dict(row)
            row["source_path"] = str(result_file)
            rows.append(row)
            for key in row:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)

    if not rows:
        print("Found results.csv files, but no readable rows. Nothing written.")
        return 0

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

