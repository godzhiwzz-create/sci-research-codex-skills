from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
AUDIT = ROOT / "skills/sci-research-manager/scripts/audit_workspace.py"
PROVENANCE = ROOT / "skills/sci-research-manager/scripts/provenance_guard.py"
GENERATE_CARD = ROOT / "skills/sci-experiment-manager/scripts/generate_experiment_card.py"
UPDATE_INDEX = ROOT / "skills/sci-experiment-manager/scripts/update_experiment_index.py"
COLLECT_RESULTS = ROOT / "skills/sci-experiment-manager/scripts/collect_results.py"
CONSISTENCY = ROOT / "skills/sci-result-auditor/scripts/check_project_consistency.py"
HTML_ASSETS = ROOT / "skills/sci-paper-reader/scripts/check_html_assets.py"


def run(script: Path, *args: object, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(script), *map(str, args)],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


class ScriptTests(unittest.TestCase):
    def test_workspace_audit_clean_and_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[notes](notes.md)\n", encoding="utf-8")
            (root / "HANDOFF.md").write_text("# Handoff\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            (root / "notes.md").write_text("ok\n", encoding="utf-8")
            project = root / "projects/p1"
            project.mkdir(parents=True)
            for name in ("README.md", "HANDOFF.md", "AGENTS.md"):
                (project / name).write_text(f"# {name}\n", encoding="utf-8")

            result = run(AUDIT, root, "--json", "--no-git")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(report["summary"]["broken_links"], 0)
            self.assertEqual(report["summary"]["missing_entrypoints"], 0)

            (root / "notes.md").unlink()
            result = run(AUDIT, root, "--json", "--no-git")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["summary"]["broken_links"], 1)

    def test_provenance_snapshot_verify_and_escape_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("evidence\n", encoding="utf-8")
            link = root / "source-link"
            link.symlink_to("source.txt")
            manifest = root / "manifest.json"

            result = run(PROVENANCE, "snapshot", root, "source.txt", "source-link", "--output", manifest, "--sha256")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            result = run(PROVENANCE, "verify", root, "--manifest", manifest)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            moved_dir = root / "moved"
            moved_dir.mkdir()
            moved = moved_dir / "source.txt"
            source.rename(moved)
            result = run(
                PROVENANCE,
                "verify",
                root,
                "--manifest",
                manifest,
                "--map",
                "source.txt=moved/source.txt",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            result = run(
                PROVENANCE,
                "verify",
                root,
                "--manifest",
                manifest,
                "--map",
                "source.txt=../../outside.txt",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("escapes root", result.stdout)

            stat = moved.stat()
            os.utime(moved, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))
            result = run(
                PROVENANCE,
                "verify",
                root,
                "--manifest",
                manifest,
                "--map",
                "source.txt=moved/source.txt",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("mtime mismatch", result.stdout)

    def test_generate_cards_supports_e_and_f_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for experiment_id, name in (("E001", "Baseline"), ("F012-D01", "原因诊断")):
                result = run(GENERATE_CARD, experiment_id, name, "--root", root)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            cards = sorted((root / "research_workspace/experiments/cards").glob("*.md"))
            self.assertEqual(len(cards), 2)
            self.assertIn("# E001 Baseline", cards[0].read_text(encoding="utf-8"))
            result = run(GENERATE_CARD, "E001", "Baseline", "--root", root)
            self.assertEqual(result.returncode, 1)

    def test_nonstandard_experiment_paths_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run(
                GENERATE_CARD,
                "F020",
                "Portable Layout",
                "--root",
                root,
                "--cards-dir",
                "records/cards",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            result = run(
                UPDATE_INDEX,
                "--root",
                root,
                "--cards-dir",
                "records/cards",
                "--markdown-output",
                "records/index.generated.md",
                "--csv-output",
                "records/index.generated.csv",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((root / "records/index.generated.md").is_file())
            self.assertTrue((root / "records/index.generated.csv").is_file())

    def test_index_generation_includes_active_e_and_f_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for experiment_id, name in (("E001", "Baseline"), ("F012-D01", "Diagnostic")):
                result = run(GENERATE_CARD, experiment_id, name, "--root", root)
                self.assertEqual(result.returncode, 0)
            archive = root / "research_workspace/experiments/cards/_archive"
            archive.mkdir()
            (archive / "E999_old.md").write_text("# E999 Old\n", encoding="utf-8")

            result = run(UPDATE_INDEX, "--root", root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            csv_path = root / "research_workspace/experiments/EXPERIMENT_INDEX.generated.csv"
            with csv_path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual({row["experiment_id"] for row in rows}, {"E001", "F012-D01"})
            markdown = (root / "research_workspace/experiments/EXPERIMENT_INDEX.generated.md").read_text(encoding="utf-8")
            self.assertNotIn("E999", markdown)

    def test_collect_results_is_deterministic_and_source_traced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder, content in (
                ("a", "metric,value\nf1,0.5\n"),
                ("b", "metric,value,seed\nf1,0.6,2\n"),
            ):
                path = root / "runs" / folder
                path.mkdir(parents=True)
                (path / "results.csv").write_text(content, encoding="utf-8")
            result = run(COLLECT_RESULTS, "--root", root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            output = root / "research_workspace/experiments/master_results.generated.csv"
            with output.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 2)
            self.assertEqual([row["source_path"] for row in rows], ["runs/a/results.csv", "runs/b/results.csv"])
            self.assertIn("seed", rows[0])

    def test_consistency_audit_success_and_missing_claim_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "HANDOFF.md").write_text("Current evidence: E001\n", encoding="utf-8")
            experiments = root / "research_workspace/experiments"
            paper = root / "research_workspace/paper"
            cards = experiments / "cards"
            cards.mkdir(parents=True)
            paper.mkdir(parents=True)
            (experiments / "QUERY_MAP.md").write_text("# Query\n", encoding="utf-8")
            (cards / "E001.md").write_text("# E001 Baseline\n", encoding="utf-8")
            (experiments / "raw.json").write_text("{}\n", encoding="utf-8")
            (experiments / "EXPERIMENT_INDEX.csv").write_text(
                "experiment_id,card_path,raw_result_path\n"
                "E001,research_workspace/experiments/cards/E001.md,research_workspace/experiments/raw.json\n",
                encoding="utf-8",
            )
            claim_map = paper / "CLAIM_EVIDENCE_MAP.md"
            claim_map.write_text("| C001 | supported by E001 |\n", encoding="utf-8")

            result = run(CONSISTENCY, root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("- none", result.stdout)

            claim_map.write_text("| C001 | supported by E001 and E999 |\n", encoding="utf-8")
            result = run(CONSISTENCY, root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("E999", result.stdout)

    def test_html_asset_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html = root / "paper.html"
            image = root / "figure.png"
            image.write_bytes(b"png")
            html.write_text('<html><img src="figure.png"></html>', encoding="utf-8")
            result = run(HTML_ASSETS, html)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            image.unlink()
            result = run(HTML_ASSETS, html)
            self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
