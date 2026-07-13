from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "maintenance_check.py"


def run_check(*args: str, script: Path = CHECK, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def run_git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def ignore_local_state(_directory: str, names: list[str]) -> set[str]:
    ignored = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}
    return ignored.intersection(names)


class MaintenanceCheckTests(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        result = run_check("check", "--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(report["public_skills"], 8)

    def test_version_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repository"
            shutil.copytree(ROOT, copy, ignore=ignore_local_state)
            (copy / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            result = run_check(
                "check",
                "--root",
                str(copy),
                "--json",
                script=copy / "scripts" / "maintenance_check.py",
                cwd=copy,
            )
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "error")
            self.assertIn("README current version differs from VERSION", report["errors"])
            self.assertIn("CHANGELOG lacks a dated entry for VERSION", report["errors"])
            self.assertIn("docs/index.html version differs from VERSION", report["errors"])

    def test_current_stable_tag_is_annotated_and_consistent(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        result = run_check("verify-tag", f"v{version}", "--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["version"], version)

    def test_clean_newer_main_is_a_release_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repository"
            shutil.copytree(ROOT, copy, ignore=ignore_local_state)

            commands = (
                ("init", "-b", "main"),
                ("config", "user.name", "Maintenance Test"),
                ("config", "user.email", "maintenance-test@example.invalid"),
                ("add", "."),
                ("commit", "-m", "v2 baseline"),
                ("tag", "-a", "v2.0.0", "-m", "v2 baseline"),
            )
            for command in commands:
                completed = run_git(copy, *command)
                self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)

            (copy / "VERSION").write_text("2.0.1\n", encoding="utf-8")
            for relative in ("README.md", "docs/index.html"):
                path = copy / relative
                path.write_text(path.read_text(encoding="utf-8").replace("2.0.0", "2.0.1"), encoding="utf-8")
            changelog = copy / "CHANGELOG.md"
            text = changelog.read_text(encoding="utf-8")
            text = text.replace(
                "## [2.0.0] - 2026-07-13",
                "## [2.0.1] - 2026-07-14\n\n### Changed\n\n- Release candidate fixture.\n\n"
                "## [2.0.0] - 2026-07-13",
                1,
            ).replace("compare/v2.0.0...HEAD", "compare/v2.0.1...HEAD", 1)
            changelog.write_text(text, encoding="utf-8")

            for command in (("add", "."), ("commit", "-m", "prepare v2.0.1")):
                completed = run_git(copy, *command)
                self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            head = run_git(copy, "rev-parse", "HEAD")
            self.assertEqual(head.returncode, 0, head.stderr)
            remote_ref = run_git(copy, "update-ref", "refs/remotes/origin/main", head.stdout.strip())
            self.assertEqual(remote_ref.returncode, 0, remote_ref.stderr)

            result = run_check(
                "release-candidate",
                "--root",
                str(copy),
                "--json",
                script=copy / "scripts" / "maintenance_check.py",
                cwd=copy,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "ok")
            self.assertEqual(report["version"], "2.0.1")


if __name__ == "__main__":
    unittest.main()
