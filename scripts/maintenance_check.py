#!/usr/bin/env python3
"""Validate repository maintenance and release invariants without modifying files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

PUBLIC_SKILLS = (
    "academic-manuscript-writing",
    "sci-asset-manager",
    "sci-experiment-manager",
    "sci-literature-manager",
    "sci-paper-manager",
    "sci-paper-reader",
    "sci-research-manager",
    "sci-result-auditor",
)

REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    "MAINTENANCE.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "docs/index.html",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/tests.yml",
    ".github/workflows/maintenance.yml",
    ".github/dependabot.yml",
)

FORBIDDEN_TRACKED_PARTS = {"__pycache__", ".mypy_cache", ".pytest_cache"}
ACTION_NAMES = ("actions/checkout", "actions/setup-python")


@dataclass
class Report:
    mode: str
    root: Path
    version: str | None = None
    errors: list[str] = field(default_factory=list)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def parse_version(value: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.fullmatch(value)
    if match is None:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def changelog_has_release(text: str, version: str) -> bool:
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
        re.MULTILINE,
    )
    return pattern.search(text) is not None


def tracked_files(root: Path) -> list[str]:
    result = run_git(root, "ls-files", "-z")
    if result.returncode != 0:
        return []
    return [item for item in result.stdout.split("\0") if item]


def action_refs(workflow_text: str, action: str) -> set[str]:
    return set(re.findall(rf"uses:\s*{re.escape(action)}@([^\s#]+)", workflow_text))


def check_repository(root: Path) -> Report:
    root = root.resolve()
    report = Report(mode="check", root=root)
    report.require(root.is_dir(), f"repository root does not exist: {root}")
    if not root.is_dir():
        return report

    for relative in REQUIRED_FILES:
        path = root / relative
        report.require(path.is_file() and path.stat().st_size > 0, f"missing required file: {relative}")

    version = read_text(root, "VERSION").strip()
    report.version = version or None
    report.require(parse_version(version) is not None, "VERSION must contain strict MAJOR.MINOR.PATCH")

    if parse_version(version) is not None:
        readme = read_text(root, "README.md")
        changelog = read_text(root, "CHANGELOG.md")
        docs = read_text(root, "docs/index.html")
        report.require(f"当前版本：**{version}**" in readme, "README current version differs from VERSION")
        report.require(f"/tag/v{version}" in readme, "README stable Release link differs from VERSION")
        report.require("(MAINTENANCE.md)" in readme, "README does not link MAINTENANCE.md")
        report.require(changelog_has_release(changelog, version), "CHANGELOG lacks a dated entry for VERSION")
        report.require(
            f"compare/v{version}...HEAD" in changelog,
            "CHANGELOG Unreleased comparison link differs from VERSION",
        )
        report.require(f"v{version}" in docs, "docs/index.html version differs from VERSION")

    maintenance = read_text(root, "MAINTENANCE.md")
    for command in (
        "maintenance_check.py check",
        "maintenance_check.py release-candidate",
        "maintenance_check.py verify-tag",
    ):
        report.require(command in maintenance, f"MAINTENANCE.md lacks command: {command}")

    agents = read_text(root, "AGENTS.md")
    contributing = read_text(root, "CONTRIBUTING.md")
    report.require("MAINTENANCE.md" in agents, "AGENTS.md does not route maintenance to MAINTENANCE.md")
    report.require("MAINTENANCE.md" in contributing, "CONTRIBUTING.md does not link MAINTENANCE.md")

    skills_root = root / "skills"
    for skill_name in PUBLIC_SKILLS:
        skill = skills_root / skill_name
        report.require((skill / "SKILL.md").is_file(), f"missing public Skill: {skill_name}/SKILL.md")
        report.require(
            (skill / "agents" / "openai.yaml").is_file(),
            f"missing public Skill metadata: {skill_name}/agents/openai.yaml",
        )

    test_workflow = read_text(root, ".github/workflows/tests.yml")
    maintenance_workflow = read_text(root, ".github/workflows/maintenance.yml")
    report.require(
        "python scripts/maintenance_check.py check" in test_workflow,
        "tests workflow does not run the maintenance check",
    )
    report.require(
        "python -m unittest discover -s tests -v" in test_workflow,
        "tests workflow does not run the full unit suite",
    )
    report.require("schedule:" in maintenance_workflow, "maintenance workflow has no schedule")
    report.require("workflow_dispatch:" in maintenance_workflow, "maintenance workflow is not manually runnable")
    report.require("fetch-depth: 0" in maintenance_workflow, "maintenance workflow does not fetch tag history")
    report.require(
        "maintenance_check.py verify-tag" in maintenance_workflow,
        "maintenance workflow does not verify the current stable tag",
    )

    for action in ACTION_NAMES:
        refs = {
            *action_refs(test_workflow, action),
            *action_refs(maintenance_workflow, action),
        }
        report.require(bool(refs), f"workflows do not use {action}")
        report.require(len(refs) <= 1, f"workflow action versions drifted for {action}: {sorted(refs)}")

    dependabot = read_text(root, ".github/dependabot.yml")
    report.require(
        re.search(r"package-ecosystem:\s*[\"']?github-actions[\"']?", dependabot) is not None,
        "Dependabot is not configured for GitHub Actions",
    )

    for relative in tracked_files(root):
        path = Path(relative)
        if any(part in FORBIDDEN_TRACKED_PARTS for part in path.parts):
            report.errors.append(f"tracked cache file: {relative}")
        if path.suffix.lower() in {".pyc", ".pem", ".key"} or path.name == ".env":
            report.errors.append(f"tracked sensitive/generated file: {relative}")

    return report


def check_release_candidate(root: Path) -> Report:
    report = check_repository(root)
    report.mode = "release-candidate"
    version = report.version or ""

    git_dir = run_git(root, "rev-parse", "--git-dir")
    report.require(git_dir.returncode == 0, "release candidate must be checked inside a Git repository")
    if git_dir.returncode != 0 or parse_version(version) is None:
        return report

    branch = run_git(root, "branch", "--show-current")
    report.require(branch.returncode == 0 and branch.stdout.strip() == "main", "release candidate must be on main")

    status = run_git(root, "status", "--porcelain")
    report.require(status.returncode == 0 and not status.stdout.strip(), "release candidate worktree must be clean")

    head = run_git(root, "rev-parse", "HEAD")
    remote_main = run_git(root, "rev-parse", "origin/main")
    report.require(remote_main.returncode == 0, "origin/main is unavailable; fetch before release validation")
    if head.returncode == 0 and remote_main.returncode == 0:
        report.require(head.stdout.strip() == remote_main.stdout.strip(), "local main differs from origin/main")

    tag = f"v{version}"
    existing = run_git(root, "show-ref", "--verify", "--quiet", f"refs/tags/{tag}")
    report.require(existing.returncode != 0, f"release tag already exists and must not be moved: {tag}")

    tags = run_git(root, "tag", "--list", "v[0-9]*")
    current = parse_version(version)
    previous: list[tuple[int, int, int]] = []
    if tags.returncode == 0:
        for raw in tags.stdout.splitlines():
            match = TAG_RE.fullmatch(raw.strip())
            if match:
                previous.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))
    if current is not None and previous:
        report.require(current > max(previous), f"VERSION {version} is not newer than existing tags")

    return report


def git_show(root: Path, spec: str) -> subprocess.CompletedProcess[str]:
    return run_git(root, "show", spec)


def verify_tag(root: Path, tag: str) -> Report:
    root = root.resolve()
    report = Report(mode="verify-tag", root=root)
    match = TAG_RE.fullmatch(tag)
    report.require(match is not None, "tag must use vMAJOR.MINOR.PATCH")
    if match is None:
        return report
    version = ".".join(match.groups())
    report.version = version

    tag_ref = run_git(root, "show-ref", "--verify", "--quiet", f"refs/tags/{tag}")
    report.require(tag_ref.returncode == 0, f"tag does not exist: {tag}")
    if tag_ref.returncode != 0:
        return report

    object_type = run_git(root, "cat-file", "-t", tag)
    report.require(object_type.returncode == 0 and object_type.stdout.strip() == "tag", f"tag is not annotated: {tag}")

    commit = run_git(root, "rev-parse", f"{tag}^{{}}")
    report.require(commit.returncode == 0, f"cannot resolve tag commit: {tag}")
    if commit.returncode == 0:
        ancestor = run_git(root, "merge-base", "--is-ancestor", commit.stdout.strip(), "main")
        report.require(ancestor.returncode == 0, f"tag commit is not reachable from main: {tag}")

    version_file = git_show(root, f"{tag}:VERSION")
    report.require(version_file.returncode == 0, f"tag snapshot has no VERSION file: {tag}")
    if version_file.returncode == 0:
        report.require(version_file.stdout.strip() == version, f"tag name and VERSION disagree: {tag}")

    readme = git_show(root, f"{tag}:README.md")
    changelog = git_show(root, f"{tag}:CHANGELOG.md")
    docs = git_show(root, f"{tag}:docs/index.html")
    report.require(readme.returncode == 0 and f"当前版本：**{version}**" in readme.stdout, "tag README version mismatch")
    report.require(
        changelog.returncode == 0 and changelog_has_release(changelog.stdout, version),
        "tag CHANGELOG lacks a dated version entry",
    )
    report.require(docs.returncode == 0 and f"v{version}" in docs.stdout, "tag Pages version mismatch")

    return report


def print_report(report: Report, as_json: bool) -> None:
    payload = {
        "status": "ok" if report.ok else "error",
        "mode": report.mode,
        "version": report.version,
        "root": str(report.root),
        "errors": report.errors,
        "public_skills": len(PUBLIC_SKILLS),
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if report.ok:
        print(
            f"[ok] maintenance check passed: mode={report.mode} "
            f"version={report.version or 'n/a'} public_skills={len(PUBLIC_SKILLS)}"
        )
        return
    print(f"[error] maintenance check failed: mode={report.mode}", file=sys.stderr)
    for error in report.errors:
        print(f"- {error}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        default="check",
        choices=("check", "release-candidate", "verify-tag"),
        help="validation mode (default: check)",
    )
    parser.add_argument("tag", nargs="?", help="annotated tag for verify-tag mode")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit a JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.mode == "check":
        if args.tag is not None:
            build_parser().error("check mode does not accept a tag")
        report = check_repository(root)
    elif args.mode == "release-candidate":
        if args.tag is not None:
            build_parser().error("release-candidate mode does not accept a tag")
        report = check_release_candidate(root)
    else:
        if args.tag is None:
            build_parser().error("verify-tag mode requires vMAJOR.MINOR.PATCH")
        report = verify_tag(root, args.tag)
    print_report(report, args.as_json)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
