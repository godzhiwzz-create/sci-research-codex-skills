#!/usr/bin/env python3
"""Preview selective local installs; explicit upgrades preserve whole-directory backups."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import uuid

SOURCE = Path(__file__).resolve().parents[1] / "skills"
Fingerprint = tuple[tuple[str, int, str], ...]


class InstallError(Exception):
    """An unsafe or incomplete installation request."""


@dataclass(frozen=True)
class Plan:
    name: str
    source: Path
    target: Path
    source_state: Fingerprint
    target_state: Fingerprint | None
    action: str


def fingerprint(root: Path) -> Fingerprint:
    """Include custom files, empty directories and modes; never follow symlinks."""
    entries: list[tuple[str, int, str]] = []

    def visit(path: Path) -> None:
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISDIR(info.st_mode):
            entries.append((str(path.relative_to(root)), mode, "directory"))
            for child in sorted(path.iterdir()):
                visit(child)
        elif stat.S_ISREG(info.st_mode):
            entries.append((str(path.relative_to(root)), mode, hashlib.sha256(path.read_bytes()).hexdigest()))
        else:
            raise InstallError(f"Refusing symlink or special file: {path}")

    if not root.is_dir() or root.is_symlink():
        raise InstallError(f"Expected a real skill directory: {root}")
    visit(root)
    return tuple(entries)


def overlaps(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def validate_paths(destination: Path, backup_root: Path, source: Path) -> tuple[Path, Path]:
    for path in (destination, backup_root):
        if path.is_symlink():
            raise InstallError(f"Refusing symlink root: {path}")
        if path.exists() and not path.is_dir():
            raise InstallError(f"Expected directory: {path}")
    destination, backup_root = destination.resolve(), backup_root.resolve()
    if destination in (Path(destination.anchor), Path.home().resolve()):
        raise InstallError("Destination must be a dedicated skills directory, not root or home")
    if overlaps(destination, source.parent) or overlaps(backup_root, source.parent):
        raise InstallError("Installation and backup paths must not overlap the source repository")
    if overlaps(destination, backup_root):
        raise InstallError("Backups must be outside the skill discovery directory")
    return destination, backup_root


def make_plan(source: Path, destination: Path, names: list[str], upgrade: bool) -> list[Plan]:
    plans = []
    for name in sorted(set(names)):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise InstallError(f"Invalid skill name: {name}")
        origin, target = source / name, destination / name
        if not (origin / "SKILL.md").is_file():
            raise InstallError(f"Unknown skill: {name}")
        source_state = fingerprint(origin)
        target_state = fingerprint(target) if os.path.lexists(target) else None
        action = "install" if target_state is None else "unchanged" if target_state == source_state else "upgrade"
        if action == "upgrade" and not upgrade:
            raise InstallError(f"{name} differs locally; review it and use --upgrade for a backed-up replacement")
        plans.append(Plan(name, origin, target, source_state, target_state, action))
    return plans


def existing_device(path: Path) -> int:
    while not path.exists():
        path = path.parent
    return path.stat().st_dev


def apply_plan(plans: list[Plan], destination: Path, backup_root: Path) -> Path | None:
    changed = [plan for plan in plans if plan.action != "unchanged"]
    if not changed:
        return None
    if len({existing_device(destination), existing_device(destination.parent), existing_device(backup_root)}) != 1:
        raise InstallError("Destination, its parent and backups must share a filesystem for recoverable renames")
    destination.parent.mkdir(parents=True, exist_ok=True)
    lock = destination.parent / f".{destination.name}-install.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise InstallError(f"Installation lock exists: {lock}; check its owner before removing it") from exc
    staging: Path | None = None
    backup: Path | None = None
    installed: list[Plan] = []
    moved: list[Plan] = []
    keep_staging = False
    try:
        staging = Path(tempfile.mkdtemp(prefix=".skill-stage-", dir=destination.parent))
        for plan in changed:
            shutil.copytree(plan.source, staging / plan.name, copy_function=shutil.copy2, symlinks=True)
            if fingerprint(staging / plan.name) != plan.source_state:
                raise InstallError(f"Source changed while staging: {plan.name}")
        # Recheck every selection before any target is moved, including no-ops.
        for plan in plans:
            current = fingerprint(plan.target) if os.path.lexists(plan.target) else None
            if current != plan.target_state:
                raise InstallError(f"Installation changed after preview: {plan.name}")
        destination.mkdir(parents=True, exist_ok=True)
        if any(plan.action == "upgrade" for plan in changed):
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = backup_root / f"{stamp}-{uuid.uuid4().hex[:12]}"
            backup.mkdir(parents=True, exist_ok=False)
        try:
            for plan in changed:
                if plan.action == "upgrade":
                    assert backup is not None
                    os.rename(plan.target, backup / plan.name)
                    moved.append(plan)
                os.rename(staging / plan.name, plan.target)
                installed.append(plan)
        except OSError as exc:
            try:
                for plan in reversed(installed):
                    if fingerprint(plan.target) != plan.source_state:
                        raise InstallError(f"Installed directory changed during rollback: {plan.name}")
                    os.rename(plan.target, staging / plan.name)
                for plan in reversed(moved):
                    assert backup is not None
                    if os.path.lexists(plan.target):
                        raise InstallError(f"Rollback target unexpectedly exists: {plan.target}")
                    os.rename(backup / plan.name, plan.target)
            except (OSError, InstallError) as rollback_error:
                keep_staging = True
                raise InstallError(f"Rollback incomplete; preserve {staging} and {backup}: {rollback_error}") from exc
            raise InstallError(f"Install failed; original skill directories restored: {exc}") from exc
        return backup
    finally:
        if staging is not None and not keep_staging:
            shutil.rmtree(staging)
        lock.rmdir()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="Select all bundled skills")
    selection.add_argument("--skill", nargs="+", metavar="NAME", help="Select one or more bundled skill IDs")
    default = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    parser.add_argument("--destination", type=Path, default=default)
    parser.add_argument("--backup-dir", type=Path, help="Backup root outside destination; default: sibling skill-backups")
    parser.add_argument("--upgrade", action="store_true", help="Allow replacement only with a recoverable directory backup")
    parser.add_argument("--apply", action="store_true", help="Write changes; without this flag, preview only")
    args = parser.parse_args(argv)
    try:
        source = SOURCE.resolve()
        destination = args.destination.expanduser()
        backup_root = args.backup_dir.expanduser() if args.backup_dir else destination.parent / "skill-backups"
        destination, backup_root = validate_paths(destination, backup_root, source)
        names = sorted(path.parent.name for path in source.glob("*/SKILL.md")) if args.all else args.skill
        if not names:
            raise InstallError("No bundled skills found")
        plans = make_plan(source, destination, names, args.upgrade)
        print(f"{'APPLY' if args.apply else 'PREVIEW (no files changed)'}: {destination}")
        for plan in plans:
            print(f"  {plan.action}: {plan.name}")
        if any(plan.action == "upgrade" for plan in plans):
            print(f"  Backup root: {backup_root}")
        if args.apply:
            backup = apply_plan(plans, destination, backup_root)
            if backup:
                print(f"Original directories preserved at: {backup}")
        return 0
    except (InstallError, OSError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
