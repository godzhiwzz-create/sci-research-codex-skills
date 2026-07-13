#!/usr/bin/env python3
"""Read-only structural audit for a long-running research workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}

NAVIGATION_NAMES = {
    "AGENTS.md",
    "CATALOG.md",
    "HANDOFF.md",
    "INDEX.md",
    "QUERY_MAP.md",
    "README.md",
    "RESULTS_REGISTRY.md",
    "SESSION_MEMORY.md",
    "WIKI.md",
}

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit research-workspace entry points, local Markdown links, symlinks, "
            "and nested Git state without modifying the workspace."
        )
    )
    parser.add_argument("root", type=Path, help="Workspace root")
    parser.add_argument(
        "--all-markdown",
        action="store_true",
        help="Check every Markdown file instead of navigation documents only",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="NAME",
        help="Additional directory basename to skip; repeat as needed",
    )
    parser.add_argument(
        "--skip-required-entrypoints",
        action="store_true",
        help="Do not require README.md, HANDOFF.md, and AGENTS.md",
    )
    parser.add_argument("--no-git", action="store_true", help="Skip nested Git status checks")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args()


def walk_workspace(root: Path, excludes: set[str]) -> tuple[list[Path], list[Path], list[Path]]:
    markdown: list[Path] = []
    symlinks: list[Path] = []
    git_roots: list[Path] = []

    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        if ".git" in dirs or ".git" in files:
            git_roots.append(current_path)

        kept_dirs: list[str] = []
        for name in dirs:
            path = current_path / name
            if path.is_symlink():
                symlinks.append(path)
                continue
            if name in excludes:
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in files:
            path = current_path / name
            if path.is_symlink():
                symlinks.append(path)
            if path.suffix.lower() == ".md":
                markdown.append(path)

    return sorted(markdown), sorted(set(symlinks)), sorted(set(git_roots))


def link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    return value.split(maxsplit=1)[0] if value else ""


def local_link_path(source: Path, raw: str) -> Path | None:
    target = link_target(raw)
    if not target or target.startswith("#") or target.startswith("//"):
        return None
    if SCHEME_RE.match(target):
        return None
    parsed = urlparse(target)
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    candidate = Path(path_text)
    if not candidate.is_absolute():
        candidate = source.parent / candidate
    return candidate.resolve(strict=False)


def check_markdown(files: list[Path], all_markdown: bool) -> tuple[int, list[dict[str, str]]]:
    checked = 0
    broken: list[dict[str, str]] = []
    for path in files:
        if not all_markdown and path.name not in NAVIGATION_NAMES:
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        text = FENCED_CODE_RE.sub("", text)
        for match in LINK_RE.finditer(text):
            resolved = local_link_path(path, match.group(1))
            if resolved is not None and not resolved.exists():
                broken.append(
                    {
                        "source": str(path),
                        "target": link_target(match.group(1)),
                        "resolved": str(resolved),
                    }
                )
    return checked, broken


def check_required_entrypoints(root: Path) -> list[str]:
    missing: list[str] = []
    for name in ("README.md", "HANDOFF.md", "AGENTS.md"):
        if not (root / name).is_file():
            missing.append(str(root / name))

    projects = root / "projects"
    if projects.is_dir():
        for project in sorted(path for path in projects.iterdir() if path.is_dir() and not path.is_symlink()):
            for name in ("README.md", "HANDOFF.md", "AGENTS.md"):
                if not (project / name).is_file():
                    missing.append(str(project / name))
    return missing


def inspect_git(root: Path) -> dict[str, object]:
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"root": str(root), "error": str(exc)}

    if result.returncode != 0:
        return {"root": str(root), "error": result.stderr.strip() or f"git exited {result.returncode}"}
    entries = [line for line in result.stdout.splitlines() if line]
    return {
        "root": str(root),
        "dirty": bool(entries),
        "dirty_entries": len(entries),
        "sample": entries[:20],
    }


def render_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        "workspace audit: "
        f"markdown={summary['markdown_checked']} "
        f"broken_links={summary['broken_links']} "
        f"symlinks={summary['symlinks_checked']} "
        f"broken_symlinks={summary['broken_symlinks']} "
        f"missing_entrypoints={summary['missing_entrypoints']} "
        f"git_roots={summary['git_roots']}"
    )
    for item in report["missing_entrypoints"]:
        print(f"[missing entrypoint] {item}")
    for item in report["broken_links"]:
        print(f"[broken link] {item['source']} -> {item['target']}")
    for item in report["broken_symlinks"]:
        print(f"[broken symlink] {item}")
    for item in report["git"]:
        if "error" in item:
            print(f"[git warning] {item['root']}: {item['error']}")
        elif item["dirty"]:
            print(f"[git dirty] {item['root']}: {item['dirty_entries']} entries")


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Workspace root is not a directory: {root}", file=sys.stderr)
        return 2

    markdown, symlinks, git_roots = walk_workspace(root, DEFAULT_EXCLUDES | set(args.exclude))
    checked, broken_links = check_markdown(markdown, args.all_markdown)
    broken_symlinks = [str(path) for path in symlinks if not path.exists()]
    missing_entrypoints = [] if args.skip_required_entrypoints else check_required_entrypoints(root)
    git = [] if args.no_git else [inspect_git(path) for path in git_roots]

    report: dict[str, Any] = {
        "root": str(root),
        "summary": {
            "markdown_checked": checked,
            "broken_links": len(broken_links),
            "symlinks_checked": len(symlinks),
            "broken_symlinks": len(broken_symlinks),
            "missing_entrypoints": len(missing_entrypoints),
            "git_roots": len(git),
            "dirty_git_roots": sum(1 for item in git if item.get("dirty") is True),
        },
        "missing_entrypoints": missing_entrypoints,
        "broken_links": broken_links,
        "broken_symlinks": broken_symlinks,
        "git": git,
    }

    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        render_text(report)
    return 1 if missing_entrypoints or broken_links or broken_symlinks else 0


if __name__ == "__main__":
    raise SystemExit(main())
