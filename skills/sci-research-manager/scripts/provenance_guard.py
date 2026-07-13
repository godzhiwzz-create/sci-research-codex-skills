#!/usr/bin/env python3
"""Snapshot and verify file provenance without changing source assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def within_root(path: Path, root: Path) -> Path:
    resolved = Path(os.path.abspath(path.expanduser()))
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes root: {path}") from exc


def collect(root: Path, targets: list[Path], with_hash: bool) -> list[dict[str, object]]:
    selected: dict[str, Path] = {}
    for raw in targets:
        candidate = raw if raw.is_absolute() else root / raw
        if not candidate.exists() and not candidate.is_symlink():
            raise FileNotFoundError(candidate)
        relative = within_root(candidate, root)
        if candidate.is_dir() and not candidate.is_symlink():
            for current, dirs, files in os.walk(candidate, followlinks=False):
                current_path = Path(current)
                for name in list(dirs):
                    path = current_path / name
                    if path.is_symlink():
                        selected[str(within_root(path, root))] = path
                        dirs.remove(name)
                for name in files:
                    path = current_path / name
                    selected[str(within_root(path, root))] = path
        else:
            selected[str(relative)] = candidate

    entries: list[dict[str, object]] = []
    for relative_key, path in sorted(selected.items()):
        stat = path.lstat()
        if path.is_symlink():
            entry: dict[str, object] = {
                "path": relative_key,
                "type": "symlink",
                "mtime_ns": stat.st_mtime_ns,
                "target": os.readlink(path),
            }
        else:
            entry = {
                "path": relative_key,
                "type": "file",
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
            if with_hash:
                entry["sha256"] = sha256(path)
        entries.append(entry)
    return entries


def parse_mapping(values: list[str]) -> list[tuple[str, str]]:
    mappings: list[tuple[str, str]] = []
    for value in values:
        if "=" not in value:
            raise ValueError(f"Mapping must be OLD=NEW: {value}")
        old, new = value.split("=", 1)
        old = old.strip().strip("/")
        new = new.strip().strip("/")
        if not old:
            raise ValueError(f"Mapping OLD prefix cannot be empty: {value}")
        mappings.append((old, new))
    return sorted(mappings, key=lambda item: len(item[0]), reverse=True)


def remap(path: str, mappings: list[tuple[str, str]]) -> str:
    for old, new in mappings:
        if path == old:
            return new
        if path.startswith(old + "/"):
            suffix = path[len(old) + 1 :]
            return f"{new}/{suffix}" if new else suffix
    return path


def snapshot(args: argparse.Namespace) -> int:
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Root is not a directory: {root}", file=sys.stderr)
        return 2
    output = args.output.expanduser().resolve(strict=False)
    if output.exists() and not args.force:
        print(f"Manifest exists; refusing to overwrite: {output}", file=sys.stderr)
        return 2
    if not output.parent.is_dir():
        print(f"Manifest parent does not exist: {output.parent}", file=sys.stderr)
        return 2

    try:
        entries = collect(root, args.targets, args.sha256)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(root),
        "hash_algorithm": "sha256" if args.sha256 else None,
        "entries": entries,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"snapshot: entries={len(entries)} manifest={output}")
    return 0


def verify_entry(root: Path, entry: dict[str, object], mappings: list[tuple[str, str]]) -> list[str]:
    original = str(entry["path"])
    relative = remap(original, mappings)
    try:
        safe_relative = within_root(root / relative, root)
    except ValueError:
        return [f"mapped path escapes root: {original} -> {relative}"]
    path = root / safe_relative
    if not path.exists() and not path.is_symlink():
        return [f"missing: {original} -> {relative}"]

    issues: list[str] = []
    stat = path.lstat()
    expected_type = entry["type"]
    actual_type = "symlink" if path.is_symlink() else "file"
    if actual_type != expected_type:
        return [f"type mismatch: {original} expected={expected_type} actual={actual_type}"]
    if stat.st_mtime_ns != entry["mtime_ns"]:
        issues.append(f"mtime mismatch: {original} expected={entry['mtime_ns']} actual={stat.st_mtime_ns}")

    if expected_type == "symlink":
        target = os.readlink(path)
        if target != entry["target"]:
            issues.append(f"symlink target mismatch: {original} expected={entry['target']} actual={target}")
        return issues

    if stat.st_size != entry["size"]:
        issues.append(f"size mismatch: {original} expected={entry['size']} actual={stat.st_size}")
    expected_hash = entry.get("sha256")
    if expected_hash and sha256(path) != expected_hash:
        issues.append(f"sha256 mismatch: {original}")
    return issues


def verify(args: argparse.Namespace) -> int:
    root = args.root.expanduser().resolve()
    try:
        manifest = json.loads(args.manifest.expanduser().read_text(encoding="utf-8"))
        mappings = parse_mapping(args.map)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    issues: list[str] = []
    for entry in manifest.get("entries", []):
        issues.extend(verify_entry(root, entry, mappings))
    if issues:
        for issue in issues:
            print(f"[mismatch] {issue}")
        print(f"verify: entries={len(manifest.get('entries', []))} mismatches={len(issues)}")
        return 1
    print(f"verify: entries={len(manifest.get('entries', []))} mismatches=0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Snapshot and verify size, modification time, symlink target, and optional SHA-256."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser("snapshot", help="Create a provenance manifest")
    snapshot_parser.add_argument("root", type=Path, help="Root used for relative paths")
    snapshot_parser.add_argument("targets", nargs="+", type=Path, help="Files/directories under root")
    snapshot_parser.add_argument("--output", required=True, type=Path, help="New manifest path")
    snapshot_parser.add_argument("--sha256", action="store_true", help="Hash file contents")
    snapshot_parser.add_argument("--force", action="store_true", help="Allow manifest overwrite")
    snapshot_parser.set_defaults(handler=snapshot)

    verify_parser = subparsers.add_parser("verify", help="Verify assets against a manifest")
    verify_parser.add_argument("root", type=Path, help="Current root containing the assets")
    verify_parser.add_argument("--manifest", required=True, type=Path, help="Snapshot manifest")
    verify_parser.add_argument(
        "--map",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Map a recorded relative path prefix to its new prefix; repeat as needed",
    )
    verify_parser.set_defaults(handler=verify)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
