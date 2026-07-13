#!/usr/bin/env python3
"""Collect results.csv files into a deterministic generated table."""

from __future__ import annotations

import argparse
import csv
import io
import os
import tempfile
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(content)
        temp_name = stream.name
    os.replace(temp_name, path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--runs-dir", type=Path, default=Path("runs"), help="Search root")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research_workspace/experiments/master_results.generated.csv"),
    )
    parser.add_argument("--dry-run", action="store_true", help="Report files/rows without writing")
    return parser.parse_args()


def resolve(root: Path, path: Path) -> Path:
    return path.expanduser() if path.is_absolute() else root / path


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    runs_dir = resolve(root, args.runs_dir)
    output = resolve(root, args.output)
    if not runs_dir.is_dir():
        print(f"No runs directory found: {runs_dir}")
        return 0

    result_files = sorted(path for path in runs_dir.rglob("results.csv") if path.resolve() != output.resolve())
    rows: list[dict[str, str]] = []
    fieldnames: list[str] = []
    seen: set[str] = set()
    for result_file in result_files:
        try:
            file_rows = read_csv(result_file)
        except (OSError, csv.Error, UnicodeError) as exc:
            print(f"Warning: could not read {result_file}: {exc}")
            continue
        for row in file_rows:
            clean = {str(key): "" if value is None else str(value) for key, value in row.items() if key is not None}
            try:
                source = str(result_file.relative_to(root))
            except ValueError:
                source = str(result_file)
            clean["source_path"] = source
            rows.append(clean)
            for key in clean:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)

    if not rows:
        print(f"Found {len(result_files)} result files but no readable rows. Nothing written.")
        return 0
    if args.dry_run:
        print(f"Would collect {len(rows)} rows from {len(result_files)} files into {output}")
        return 0

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    atomic_write(output, buffer.getvalue())
    print(f"Wrote {len(rows)} rows from {len(result_files)} files to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
