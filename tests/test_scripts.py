from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
AUDIT = ROOT / "skills/sci-research-manager/scripts/audit_workspace.py"
LIBRARY_AUDIT = ROOT / "skills/sci-research-manager/scripts/audit_research_libraries.py"
PROVENANCE = ROOT / "skills/sci-research-manager/scripts/provenance_guard.py"
DISCLOSURE_SCAN = ROOT / "skills/sci-research-manager/scripts/scan_external_disclosures.py"
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
        timeout=15,
    )


def run_disclosure(
    *args: object,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(DISCLOSURE_SCAN), *map(str, args)],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
        env=env,
    )


def build_library_workspace(root: Path) -> None:
    literature = root / "library"
    metadata = literature / "metadata"
    papers = literature / "papers"
    project_literature = root / "work/p1/literature"
    notes = project_literature / "notes"
    experiment_namespace = root / "evidence/p1"
    current = experiment_namespace / "current"
    for directory in (metadata, papers, notes, current):
        directory.mkdir(parents=True, exist_ok=True)

    for name in ("AGENTS.md", "README.md", "HANDOFF.md", "WIKI.md", "LIBRARY_SKILL_INTERFACE.md"):
        (literature / name).write_text(f"# {name}\n", encoding="utf-8")
    (papers / "CATALOG.md").write_text("# Catalog\n", encoding="utf-8")
    (metadata / "PDF_INTAKE.tsv").write_text("pdf_path\n", encoding="utf-8")
    (metadata / "SOURCE_INDEX.tsv").write_text(
        "source_id\tmetadata_status\n"
        "doi:10.1/example\tbib_ready\n",
        encoding="utf-8",
    )
    (metadata / "SOURCE_ALIASES.tsv").write_text(
        "alias_source_id\tcanonical_source_id\trelation\tverification_source\tverified_at\n",
        encoding="utf-8",
    )

    (project_literature / "README.md").write_text("# Project literature\n", encoding="utf-8")
    (project_literature / "SOURCES.tsv").write_text(
        "source_id\ttags\tproject_role\treading_depth\tnote\texperiments\tclaims\n"
        "doi:10.1/example\tbaseline\tbackground\tfull_read\t\tE001\tLC001\n",
        encoding="utf-8",
    )
    (project_literature / "LITERATURE_CLAIMS.tsv").write_text(
        "literature_claim_id\tsource_id\tverification_status\tnote_path\texperiments\tmanuscript_claims\tverified_at\n"
        "LC001\tdoi:10.1/example\tclaim_verified\tnotes/LC001.md\tE001\tC001\t2026-01-01\n",
        encoding="utf-8",
    )
    (project_literature / "INDEX.md").write_text("- doi:10.1/example\n", encoding="utf-8")
    (project_literature / "QUERY_MAP.md").write_text("# Query map\n", encoding="utf-8")
    (notes / "LC001.md").write_text("# Verified claim\n", encoding="utf-8")

    for name in ("README.md", "HANDOFF.md", "QUERY_MAP.md"):
        (root / "evidence" / name).write_text(f"# {name}\n", encoding="utf-8")
    (experiment_namespace / "card.md").write_text("# E001\n", encoding="utf-8")
    (experiment_namespace / "raw.json").write_text("{}\n", encoding="utf-8")
    (experiment_namespace / "protocol.md").write_text("# Protocol\n", encoding="utf-8")
    (experiment_namespace / "EXPERIMENTS.tsv").write_text(
        "experiment_id\tcard\ttask_stage\texperiment_status\tevidence_status\tclaim_strength\tdirection_decision\traw_artifact\tprotocol_anchor\tselection_warning\treplacement_id\tlast_verified\n"
        "E001\tcard.md\tresult_analysis\tcomplete\tverified\tmain_claim\tcontinue\traw.json\tprotocol.md\tnone\t\t2026-01-01\n",
        encoding="utf-8",
    )
    (root / "evidence/RESULTS_REGISTRY.tsv").write_text(
        "evidence_id\tproject\texperiment_id\tquestion\tcanonical_card\traw_result\tprotocol_anchor\texperiment_status\tevidence_status\tclaim_strength\tselection_warning\tpromotion_reason\tlast_verified\n"
        "p1:E001\tp1\tE001\tDoes it work?\tevidence/p1/card.md\tevidence/p1/raw.json\tevidence/p1/protocol.md\tcomplete\tverified\tmain_claim\tnone\tcanonical result\t2026-01-01\n",
        encoding="utf-8",
    )
    (root / "evidence/RESULTS_REGISTRY.md").write_text("# Registry\n", encoding="utf-8")


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

            empty = root / "empty"
            empty.mkdir()
            result = run(AUDIT, empty, "--json", "--no-git", "--skip-required-entrypoints")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_research_library_audit_supports_layouts_vocabularies_and_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_library_workspace(root)
            layout = (
                "--literature-root", "library",
                "--experiments-root", "evidence",
                "--projects-root", "work",
                "--reference-dir", "papers",
                "--json",
            )

            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["root"], ".")
            self.assertNotIn(str(root), result.stdout)

            index = root / "evidence/p1/EXPERIMENTS.tsv"
            original = index.read_text(encoding="utf-8")
            index.write_text(original.replace("\tcomplete\t", "\tcomplete_with_note\t"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid_experiment_status", result.stdout)
            result = run(
                LIBRARY_AUDIT,
                root,
                *layout,
                "--allow-value",
                "experiment_status=complete_with_note",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("registry_state_mismatch", result.stdout)
            result = run(
                LIBRARY_AUDIT,
                root,
                *layout,
                "--allow-value",
                "experiment_status=complete_with_note",
                "--map-value",
                "experiment_status=complete_with_note:complete",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            index.write_text(
                original.replace("\tcomplete\t", "\tcomplete_with_note\t").replace(
                    "\tverified\tmain_claim\tcontinue\traw.json\tprotocol.md\t",
                    "\tverified\tmain_claim\tcontinue\t\t\t",
                ),
                encoding="utf-8",
            )
            result = run(
                LIBRARY_AUDIT,
                root,
                *layout,
                "--map-value",
                "experiment_status=complete_with_note:complete",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("complete_experiment_incomplete_pointer", result.stdout)

            index.write_text(
                original.replace("\tverified\tmain_claim\tcontinue\traw.json\tprotocol.md\t", "\tnot_assessed\tunsupported\tstop\t\t\t"),
                encoding="utf-8",
            )
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("complete_experiment_incomplete_pointer", result.stdout)

            index.write_text(original, encoding="utf-8")
            (root / "library/README.md").write_text("当前 PDF：1 篇\n", encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)["status"], "WARN")
            result = run(LIBRARY_AUDIT, root, *layout, "--strict")
            self.assertEqual(result.returncode, 1)

            (root / "library/metadata/SOURCE_INDEX.tsv").write_bytes(b"\xff")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "INCOMPLETE")

            result = run(LIBRARY_AUDIT, root, "--literature-root", "../outside")
            self.assertEqual(result.returncode, 2)
            self.assertIn("escapes workspace root", result.stderr)

    def test_research_library_audit_handles_short_rows_doi_characters_and_path_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "workspace"
            build_library_workspace(root)
            layout = (
                "--literature-root", "library",
                "--experiments-root", "evidence",
                "--projects-root", "work",
                "--reference-dir", "papers",
                "--json",
            )

            for relative in (
                "library/metadata/SOURCE_INDEX.tsv",
                "work/p1/literature/SOURCES.tsv",
                "work/p1/literature/LITERATURE_CLAIMS.tsv",
                "work/p1/literature/INDEX.md",
            ):
                path = root / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace("doi:10.1/example", "doi:10.1/foo(bar)"),
                    encoding="utf-8",
                )
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            sources = root / "work/p1/literature/SOURCES.tsv"
            source_header = sources.read_text(encoding="utf-8").splitlines()[0]
            sources.write_text(source_header + "\ndoi:10.1/foo(bar)\tbaseline\n", encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)["status"], "FAIL")
            self.assertNotIn("Traceback", result.stderr + result.stdout)

            build_library_workspace(root)
            outside = base / "outside.md"
            outside.write_text("external note\n", encoding="utf-8")
            claims = root / "work/p1/literature/LITERATURE_CLAIMS.tsv"
            claim_text = claims.read_text(encoding="utf-8")
            claims.write_text(claim_text.replace("notes/LC001.md", "../../../../outside.md"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsafe_literature_claim_note_path", result.stdout)

            escape = root / "work/p1/literature/notes/escape.md"
            escape.symlink_to(outside)
            claims.write_text(claim_text.replace("notes/LC001.md", "notes/escape.md"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsafe_literature_claim_note_path", result.stdout)

    def test_research_library_audit_reconciles_registry_and_claim_safety(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_library_workspace(root)
            layout = (
                "--literature-root", "library",
                "--experiments-root", "evidence",
                "--projects-root", "work",
                "--reference-dir", "papers",
                "--json",
            )
            registry = root / "evidence/RESULTS_REGISTRY.tsv"
            registry_original = registry.read_text(encoding="utf-8")
            index = root / "evidence/p1/EXPERIMENTS.tsv"
            index_original = index.read_text(encoding="utf-8")

            registry.write_text(registry_original.replace("\tcomplete\tverified\t", "\tcomplet\tverified\t"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid_registry_experiment_status", result.stdout)

            registry.write_text(registry_original.replace("\tmain_claim\tnone\t", "\ttrend_only\tnone\t"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("registry_state_mismatch", result.stdout)

            (root / "evidence/p1/alternate.json").write_text("{}\n", encoding="utf-8")
            registry.write_text(registry_original.replace("evidence/p1/raw.json", "evidence/p1/alternate.json"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("registry_pointer_mismatch", result.stdout)

            index.write_text(index_original.replace("\tnone\t\t2026-01-01", "\ttest_selected\t\t2026-01-01"), encoding="utf-8")
            registry.write_text(registry_original.replace("\tnone\tcanonical result", "\ttest_selected\tcanonical result"), encoding="utf-8")
            result = run(LIBRARY_AUDIT, root, *layout)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsafe_main_claim_selection", result.stdout)
            self.assertIn("unsafe_registry_main_claim_selection", result.stdout)

            index.write_text(index_original.replace("\tverified\tmain_claim\t", "\tconfirmed\tmain_claim\t"), encoding="utf-8")
            registry.write_text(registry_original.replace("\tverified\tmain_claim\t", "\tconfirmed\tmain_claim\t"), encoding="utf-8")
            result = run(
                LIBRARY_AUDIT,
                root,
                *layout,
                "--allow-value",
                "evidence_status=confirmed",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("registry_nonverified_promotion", result.stdout)
            result = run(
                LIBRARY_AUDIT,
                root,
                *layout,
                "--map-value",
                "evidence_status=confirmed:verified",
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_research_library_audit_rejects_external_paths_without_echoing_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            layout = (
                "--literature-root", "library",
                "--experiments-root", "evidence",
                "--projects-root", "work",
                "--reference-dir", "papers",
                "--json",
            )

            pointer_root = base / "pointer-workspace"
            build_library_workspace(pointer_root)
            private_result = base / "private-result.json"
            private_result.write_text("{}\n", encoding="utf-8")
            index = pointer_root / "evidence/p1/EXPERIMENTS.tsv"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "\traw.json\tprotocol.md\t",
                    f"\t{private_result}\thttps://example.invalid/protocol\t",
                ),
                encoding="utf-8",
            )
            result = run(LIBRARY_AUDIT, pointer_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("unsafe_experiment_raw_artifact_path", result.stdout)
            self.assertIn("unsafe_experiment_protocol_anchor_path", result.stdout)
            self.assertIn("registry_pointer_mismatch", result.stdout)
            self.assertNotIn(str(private_result), result.stdout)
            self.assertNotIn("https://example.invalid/protocol", result.stdout)

            registry_root = base / "registry-workspace"
            build_library_workspace(registry_root)
            registry = registry_root / "evidence/RESULTS_REGISTRY.tsv"
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    "evidence/p1/raw.json",
                    str(private_result),
                ),
                encoding="utf-8",
            )
            result = run(LIBRARY_AUDIT, registry_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("unsafe_registry_pointer_path", result.stdout)
            self.assertIn("registry_pointer_mismatch", result.stdout)
            self.assertNotIn(str(private_result), result.stdout)

            project_root = base / "project-link-workspace"
            build_library_workspace(project_root)
            external_project = base / "external-project"
            (project_root / "work/p1").rename(external_project)
            (project_root / "work/p1").symlink_to(external_project, target_is_directory=True)
            result = run(LIBRARY_AUDIT, project_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("unsafe_project_root_target", result.stdout)
            self.assertNotIn(str(external_project), result.stdout)

            internal_project_root = base / "internal-project-link-workspace"
            build_library_workspace(internal_project_root)
            internal_project = internal_project_root / "project-target"
            (internal_project_root / "work/p1").rename(internal_project)
            (internal_project_root / "work/p1").symlink_to(
                internal_project,
                target_is_directory=True,
            )
            result = run(LIBRARY_AUDIT, internal_project_root, *layout)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            current_root = base / "current-link-workspace"
            build_library_workspace(current_root)
            current = current_root / "evidence/p1/current"
            current.rmdir()
            external_current = base / "external-current"
            external_current.mkdir()
            current.symlink_to(external_current, target_is_directory=True)
            result = run(LIBRARY_AUDIT, current_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("unsafe_experiment_current_target", result.stdout)
            self.assertNotIn(str(external_current), result.stdout)

            internal_current_root = base / "internal-current-link-workspace"
            build_library_workspace(internal_current_root)
            internal_current = internal_current_root / "evidence/p1/current"
            internal_current.rmdir()
            current_target = internal_current_root / "current-target"
            current_target.mkdir()
            internal_current.symlink_to(current_target, target_is_directory=True)
            result = run(LIBRARY_AUDIT, internal_current_root, *layout)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            required_root = base / "required-link-workspace"
            build_library_workspace(required_root)
            source_index = required_root / "library/metadata/SOURCE_INDEX.tsv"
            source_index.unlink()
            external_index = base / "external-source-index.tsv"
            external_index.write_text(
                "source_id\tmetadata_status\nprivate-source\tbib_ready\n",
                encoding="utf-8",
            )
            source_index.symlink_to(external_index)
            result = run(LIBRARY_AUDIT, required_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("unsafe_required_entry_target", result.stdout)
            self.assertNotIn("private-source", result.stdout)
            self.assertNotIn(str(external_index), result.stdout)

            broken_root = base / "broken-link-workspace"
            build_library_workspace(broken_root)
            broken_index = broken_root / "library/metadata/SOURCE_INDEX.tsv"
            broken_index.unlink()
            broken_index.symlink_to(base / "does-not-exist.tsv")
            result = run(LIBRARY_AUDIT, broken_root, *layout)
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("broken_required_entry_link", result.stdout)

    def test_external_disclosure_scan_handles_text_archives_ooxml_and_incomplete_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = root / "clean.txt"
            clean.write_text("No disclosure candidates are present.\n", encoding="utf-8")
            result = run_disclosure(clean, "--json")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)["status"], "no_candidates_found")

            candidate = root / "candidate.txt"
            candidate.write_text("Drafted with GPT-4o and 生成式人工智能.\n", encoding="utf-8")
            result = run_disclosure(candidate, "--json")
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "candidates_found")
            self.assertGreaterEqual(len(report["findings"]), 2)
            self.assertEqual(report["inventory"][0]["path"], "input-1/candidate.txt")
            self.assertEqual(report["inventory"][0]["sha256"], hashlib.sha256(candidate.read_bytes()).hexdigest())
            self.assertNotIn(str(root), result.stdout)

            document = root / "document.docx"
            with zipfile.ZipFile(document, "w") as archive:
                archive.writestr("word/document.xml", '<root><text clean="true">ordinary prose</text><link target="Codex"/></root>')
            result = run_disclosure(document, "--json")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["status"], "candidates_found")

            inner_bytes = BytesIO()
            with zipfile.ZipFile(inner_bytes, "w") as inner:
                inner.writestr("note.txt", "writing assistant")
            outer = root / "package.zip"
            with zipfile.ZipFile(outer, "w") as archive:
                archive.writestr("nested.zip", inner_bytes.getvalue())
            result = run_disclosure(outer, "--json")
            self.assertEqual(result.returncode, 1)

            unsupported = root / "legacy.doc"
            unsupported.write_bytes(b"legacy")
            result = run_disclosure(unsupported, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "incomplete_scan")

            link = root / "linked.txt"
            link.symlink_to(clean)
            result = run_disclosure(link, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("symbolic-link component", result.stdout)
            self.assertNotIn(str(root), result.stdout)

    def test_external_disclosure_scan_refuses_empty_or_unclassified_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty"
            empty.mkdir()
            result = run_disclosure(empty, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "incomplete_scan")

            unknown = root / "artifact.opaque"
            unknown.write_text("OpenAI", encoding="utf-8")
            result = run_disclosure(unknown, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["coverage"]["checked"], [])

            mixed = root / "mixed"
            mixed.mkdir()
            (mixed / "clean.txt").write_text("ordinary prose", encoding="utf-8")
            (mixed / "artifact.opaque").write_bytes(b"opaque")
            result = run_disclosure(mixed, "--json")
            self.assertEqual(result.returncode, 2)
            report = json.loads(result.stdout)
            self.assertTrue(report["coverage"]["checked"])
            self.assertIn("unclassified input format", result.stdout)

            mixed_archive = root / "mixed.zip"
            with zipfile.ZipFile(mixed_archive, "w") as archive:
                archive.writestr("clean.txt", "ordinary prose")
                archive.writestr("artifact.opaque", b"opaque")
            result = run_disclosure(mixed_archive, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("unclassified archive member format", result.stdout)

            ignorable_sidecar = root / "sidecar.zip"
            with zipfile.ZipFile(ignorable_sidecar, "w") as archive:
                archive.writestr("clean.txt", "ordinary prose")
                archive.writestr("__MACOSX/._clean.txt", b"sidecar")
            result = run_disclosure(ignorable_sidecar, "--json")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue(json.loads(result.stdout)["coverage"]["not_applicable"])

            style = root / "submission.sty"
            style.write_text("% drafted with OpenAI\n", encoding="utf-8")
            result = run_disclosure(style, "--json")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["status"], "candidates_found")

            source_package = root / "source.zip"
            with zipfile.ZipFile(source_package, "w") as archive:
                archive.writestr("journal.cls", "% edited with ChatGPT\n")
                archive.writestr("references.bst", "% ordinary style\n")
            result = run_disclosure(source_package, "--json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ChatGPT", result.stdout)

    def test_external_disclosure_scan_handles_ooxml_boundaries_and_parent_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            split_runs = root / "split-runs.docx"
            with zipfile.ZipFile(split_runs, "w") as archive:
                archive.writestr(
                    "word/document.xml",
                    '<w:document xmlns:w="urn:test"><w:p><w:r><w:t>Chat</w:t></w:r>'
                    '<w:r><w:t>GPT</w:t></w:r></w:p></w:document>',
                )
            result = run_disclosure(split_runs, "--json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ChatGPT", result.stdout)

            embedded_svg = root / "embedded-svg.docx"
            with zipfile.ZipFile(embedded_svg, "w") as archive:
                archive.writestr("word/document.xml", "<root>ordinary prose</root>")
                archive.writestr("word/media/disclosure.svg", "<svg><text>Codex</text></svg>")
            result = run_disclosure(embedded_svg, "--json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Codex", result.stdout)

            malformed = root / "malformed.docx"
            with zipfile.ZipFile(malformed, "w") as archive:
                archive.writestr("word/document.xml", "<root><broken>")
            result = run_disclosure(malformed, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("XML parse failed", result.stdout)

            entity_xml = root / "entity.docx"
            with zipfile.ZipFile(entity_xml, "w") as archive:
                archive.writestr(
                    "word/document.xml",
                    '<!DOCTYPE root [<!ENTITY x "ordinary">]><root>&x;</root>',
                )
            result = run_disclosure(entity_xml, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("DOCTYPE declarations require manual review", result.stdout)

            unknown_media = root / "unknown-media.docx"
            with zipfile.ZipFile(unknown_media, "w") as archive:
                archive.writestr("word/document.xml", "<root>ordinary prose</root>")
                archive.writestr("word/media/vector.emf", b"opaque")
            result = run_disclosure(unknown_media, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("embedded media format unsupported", result.stdout)

            unknown_member = root / "unknown-member.docx"
            with zipfile.ZipFile(unknown_member, "w") as archive:
                archive.writestr("word/document.xml", "<root>ordinary prose</root>")
                archive.writestr("custom/artifact.opaque", b"opaque")
            result = run_disclosure(unknown_member, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("unclassified OOXML/ODF member format", result.stdout)

            clean_odf = root / "clean.odt"
            with zipfile.ZipFile(clean_odf, "w") as archive:
                archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
                archive.writestr("content.xml", "<root>ordinary prose</root>")
            result = run_disclosure(clean_odf, "--json")
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            real = root / "real"
            real.mkdir()
            (real / "candidate.txt").write_text("Codex", encoding="utf-8")
            alias = root / "alias"
            alias.symlink_to(real, target_is_directory=True)
            result = run_disclosure(alias / "candidate.txt", "--json")
            self.assertEqual(result.returncode, 2)
            report = json.loads(result.stdout)
            self.assertEqual(report["findings"], [])
            self.assertIn("symbolic-link component", result.stdout)

    def test_external_disclosure_scan_matches_paths_direct_phrases_and_bounds_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "package"
            notes = package / "notes"
            notes.mkdir(parents=True)
            named = notes / "We used AI.txt"
            named.write_text("ordinary prose\n", encoding="utf-8")
            result = run_disclosure(package, "--json")
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("We used AI.txt", result.stdout)
            self.assertNotIn(str(root), result.stdout)

            named_archive = root / "named.zip"
            with zipfile.ZipFile(named_archive, "w") as archive:
                archive.writestr("notes/artificial intelligence.txt", "ordinary prose")
            result = run_disclosure(named_archive, "--json")
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            self.assertIn("artificial intelligence.txt", result.stdout)
            self.assertNotIn(str(root), result.stdout)

            long_name_archive = root / "long-name.zip"
            long_member = "notes/" + ("a" * 700) + "/OpenAI.txt"
            with zipfile.ZipFile(long_name_archive, "w") as archive:
                archive.writestr(long_member, "ordinary prose")
            result = run_disclosure(long_name_archive, "--json")
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            finding_sources = [str(item["source"]) for item in report["findings"]]
            self.assertTrue(any("[sha256:" in source for source in finding_sources))
            self.assertTrue(all(len(source) <= 500 for source in finding_sources))

            direct = root / "direct.txt"
            direct.write_text(
                "We used AI during drafting.\n"
                "Artificial intelligence was used for another task.\n"
                "本文使用人工智能检查格式。\n"
                "本文使用了 AI 检查格式。\n",
                encoding="utf-8",
            )
            result = run_disclosure(direct, "--json")
            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            contexts = "\n".join(str(item["context"]) for item in report["findings"])
            self.assertIn("We used AI", contexts)
            self.assertIn("Artificial intelligence", contexts)
            self.assertIn("本文使用人工智能", contexts)
            self.assertIn("本文使用了 AI", contexts)

            repeated = root / "repeated.txt"
            repeated.write_text("We used AI.\n" * 20, encoding="utf-8")
            result = run_disclosure(
                repeated,
                "--max-findings", "2",
                "--max-output-items", "4",
                "--json",
            )
            self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(len(report["findings"]), 2)
            output_items = (
                len(report["findings"])
                + len(report["inventory"])
                + len(report["coverage"]["checked"])
                + len(report["coverage"]["not_applicable"])
                + len(report["coverage"]["skipped"])
            )
            self.assertLessEqual(output_items, 4)
            self.assertIn("finding output limit exhausted", result.stdout)

    def test_external_disclosure_scan_enforces_resource_limits_and_tool_timeouts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = root / "clean.txt"
            clean.write_text("ordinary prose\n", encoding="utf-8")
            for flag in (
                "--max-files",
                "--max-file-mb",
                "--max-total-mb",
                "--max-member-mb",
                "--max-members",
                "--max-expanded-mb",
                "--max-compression-ratio",
                "--max-depth",
                "--tool-timeout-seconds",
                "--max-tool-output-mb",
                "--max-tool-calls",
                "--max-total-seconds",
                "--max-findings",
                "--max-output-items",
            ):
                with self.subTest(flag=flag):
                    result = run_disclosure(clean, flag, "0", "--json")
                    self.assertEqual(result.returncode, 2)
            result = run_disclosure(clean, "--max-compression-ratio", "nan", "--json")
            self.assertEqual(result.returncode, 2)

            oversized = root / "oversized.txt"
            oversized.write_bytes(b"x" * (1024 * 1024 + 1))
            result = run_disclosure(oversized, "--max-file-mb", "1", "--json")
            self.assertEqual(result.returncode, 2)
            report = json.loads(result.stdout)
            self.assertIsNone(report["inventory"][0]["sha256"])

            too_many = root / "too-many"
            too_many.mkdir()
            (too_many / "a.txt").write_text("ordinary", encoding="utf-8")
            (too_many / "b.txt").write_text("ordinary", encoding="utf-8")
            result = run_disclosure(too_many, "--max-files", "1", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("input file budget exhausted", result.stdout)

            total_size = root / "total-size"
            total_size.mkdir()
            (total_size / "a.txt").write_bytes(b"x" * 700_000)
            (total_size / "b.txt").write_bytes(b"x" * 700_000)
            result = run_disclosure(total_size, "--max-total-mb", "1", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("package input-byte budget exhausted", result.stdout)

            expanded = root / "expanded.zip"
            with zipfile.ZipFile(expanded, "w") as archive:
                archive.writestr("a.txt", os.urandom(700_000))
                archive.writestr("b.txt", os.urandom(700_000))
            result = run_disclosure(expanded, "--max-expanded-mb", "1", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("expanded-byte budget exhausted", result.stdout)

            high_ratio = root / "high-ratio.zip"
            with zipfile.ZipFile(high_ratio, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("repeated.txt", "x" * 100_000)
            result = run_disclosure(high_ratio, "--max-compression-ratio", "2", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("compression-ratio limit", result.stdout)

            inner_bytes = BytesIO()
            with zipfile.ZipFile(inner_bytes, "w") as inner:
                inner.writestr("a.txt", "ordinary")
                inner.writestr("b.txt", "ordinary")
            nested = root / "nested-budget.zip"
            with zipfile.ZipFile(nested, "w") as archive:
                archive.writestr("inner.zip", inner_bytes.getvalue())
            result = run_disclosure(nested, "--max-members", "2", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("member budget exhausted", result.stdout)

            tools = root / "tools"
            tools.mkdir()
            sleeper = f"#!{PYTHON}\nimport time\ntime.sleep(5)\n"
            for name in ("pdftotext", "tesseract"):
                executable = tools / name
                executable.write_text(sleeper, encoding="utf-8")
                executable.chmod(0o755)
            env = dict(os.environ)
            env["PATH"] = str(tools) + os.pathsep + env.get("PATH", "")
            for name, suffix, data in (
                ("PDF", ".pdf", b"%PDF-1.4\n"),
                ("image", ".png", b"not-a-real-image"),
            ):
                artifact = root / f"timeout{suffix}"
                artifact.write_bytes(data)
                with self.subTest(tool=name):
                    result = run_disclosure(
                        artifact,
                        "--tool-timeout-seconds",
                        "0.05",
                        "--json",
                        env=env,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("timed out", result.stdout)

            fast_tool = tools / "tesseract"
            fast_tool.write_text(f"#!{PYTHON}\nprint('ordinary prose')\n", encoding="utf-8")
            fast_tool.chmod(0o755)
            images = root / "tool-budget"
            images.mkdir()
            (images / "one.png").write_bytes(b"image-one")
            (images / "two.png").write_bytes(b"image-two")
            result = run_disclosure(
                images,
                "--max-tool-calls", "1",
                "--json",
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
            self.assertIn("external-tool-call budget exhausted", result.stdout)

            loud_tool = tools / "tesseract"
            loud_tool.write_text(
                f"#!{PYTHON}\nprint('x' * (2 * 1024 * 1024))\n",
                encoding="utf-8",
            )
            loud_tool.chmod(0o755)
            loud_image = root / "large-tool-output.png"
            loud_image.write_bytes(b"image")
            result = run_disclosure(
                loud_image,
                "--max-tool-output-mb", "1",
                "--json",
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
            self.assertIn("output exceeds size limit", result.stdout)

            sleeper_tool = tools / "tesseract"
            sleeper_tool.write_text(
                f"#!{PYTHON}\nimport time\ntime.sleep(0.2)\nprint('ordinary prose')\n",
                encoding="utf-8",
            )
            sleeper_tool.chmod(0o755)
            timed_image = root / "total-time.png"
            timed_image.write_bytes(b"image")
            result = run_disclosure(
                timed_image,
                "--tool-timeout-seconds", "1",
                "--max-total-seconds", "0.05",
                "--json",
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
            self.assertIn("total-time budget exhausted", result.stdout)

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
