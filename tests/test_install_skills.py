"""Exercise local installation against disposable fixtures, never installed skills."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install_skills.py"
SPEC = importlib.util.spec_from_file_location("install_skills", SCRIPT)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "repo" / "skills"
        self.destination = self.root / "profile" / "skills"
        self.backups = self.root / "profile" / "skill-backups"
        for name in ("skill-a", "skill-b"):
            folder = self.source / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: fixture\n---\n", encoding="utf-8")
        self.source_patch = patch.object(installer, "SOURCE", self.source)
        self.source_patch.start()
        self.addCleanup(self.source_patch.stop)

    def run_cli(self, *args: str) -> int:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return installer.main(["--destination", str(self.destination), *args])

    def test_preview_creates_nothing(self) -> None:
        self.assertEqual(self.run_cli("--all"), 0)
        self.assertFalse(self.destination.parent.exists())

    def test_all_public_skills_install_only_in_temporary_profile(self) -> None:
        bundled = SCRIPT.parents[1] / "skills"
        with patch.object(installer, "SOURCE", bundled):
            self.assertEqual(self.run_cli("--all", "--apply"), 0)
        names = {path.parent.name for path in bundled.glob("*/SKILL.md")}
        self.assertEqual(len(names), 8)
        self.assertEqual({path.name for path in self.destination.iterdir()}, names)
        for name in names:
            self.assertEqual(installer.fingerprint(self.destination / name), installer.fingerprint(bundled / name))

    def test_selective_install_and_identical_noop(self) -> None:
        self.assertEqual(self.run_cli("--skill", "skill-a", "--apply"), 0)
        self.assertFalse((self.destination / "skill-b").exists())
        target = self.destination / "skill-a" / "SKILL.md"
        before = target.stat().st_mtime_ns
        self.assertEqual(self.run_cli("--skill", "skill-a", "--apply"), 0)
        self.assertEqual(target.stat().st_mtime_ns, before)
        self.assertFalse(self.backups.exists())

    def test_upgrade_preserves_custom_files_and_timestamps(self) -> None:
        self.assertEqual(self.run_cli("--skill", "skill-a", "--apply"), 0)
        custom = self.destination / "skill-a" / "custom.txt"
        custom.write_text("local customization", encoding="utf-8")
        os.utime(custom, ns=(1000000000, 2000000000))
        self.assertEqual(self.run_cli("--all", "--apply"), 1)
        self.assertFalse((self.destination / "skill-b").exists())
        self.assertEqual(self.run_cli("--all", "--upgrade"), 0)
        self.assertFalse(self.backups.exists())
        self.assertTrue(custom.exists())
        self.assertEqual(self.run_cli("--all", "--upgrade", "--apply"), 0)
        copies = list(self.backups.glob("*/skill-a/custom.txt"))
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_text(), "local customization")
        self.assertEqual(copies[0].stat().st_mtime_ns, 2000000000)
        self.assertFalse(custom.exists())

    def test_unknown_and_traversal_selection_fail_before_writing(self) -> None:
        for name in ("missing", "../skill-a", "/skill-a"):
            with self.subTest(name=name):
                self.assertEqual(self.run_cli("--skill", "skill-b", name, "--apply"), 1)
                self.assertFalse(self.destination.exists())

    def test_later_conflict_does_not_install_earlier_selection(self) -> None:
        self.assertEqual(self.run_cli("--skill", "skill-b", "--apply"), 0)
        (self.destination / "skill-b" / "local.txt").write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_cli("--all", "--apply"), 1)
        self.assertFalse((self.destination / "skill-a").exists())

    def test_cross_filesystem_is_rejected_before_writes(self) -> None:
        plans = installer.make_plan(self.source, self.destination, ["skill-a"], False)
        with patch.object(installer, "existing_device", side_effect=[1, 1, 2]):
            with self.assertRaises(installer.InstallError):
                installer.apply_plan(plans, self.destination, self.backups)
        self.assertFalse(self.destination.parent.exists())

    def test_source_and_target_symlinks_are_rejected(self) -> None:
        (self.source / "skill-a" / "link").symlink_to(self.source / "skill-b" / "SKILL.md")
        self.assertEqual(self.run_cli("--all", "--apply"), 1)
        self.assertFalse(self.destination.exists())
        self.destination.mkdir(parents=True)
        (self.destination / "skill-b").symlink_to(self.source / "skill-b", target_is_directory=True)
        self.assertEqual(self.run_cli("--skill", "skill-b", "--upgrade", "--apply"), 1)
        self.assertTrue((self.destination / "skill-b").is_symlink())

    def test_unsafe_roots_and_backup_overlap(self) -> None:
        bad_destinations = (Path("/"), Path.home(), self.source, self.source.parent)
        for destination in bad_destinations:
            with self.subTest(destination=destination), self.assertRaises(installer.InstallError):
                installer.validate_paths(destination, self.backups, self.source)
        for backup in (self.destination, self.destination / "backups", self.destination.parent, self.source):
            with self.subTest(backup=backup), self.assertRaises(installer.InstallError):
                installer.validate_paths(self.destination, backup, self.source)

    def test_rollback_restores_entire_batch_on_swap_failure(self) -> None:
        self.assertEqual(self.run_cli("--all", "--apply"), 0)
        for name in ("skill-a", "skill-b"):
            (self.destination / name / "local.txt").write_text(name, encoding="utf-8")
        before = {name: installer.fingerprint(self.destination / name) for name in ("skill-a", "skill-b")}
        rename = os.rename

        def fail_second_swap(source: Path, destination: Path) -> None:
            if source.name == "skill-b" and source.parent.name.startswith(".skill-stage-"):
                raise OSError("injected second swap failure")
            rename(source, destination)

        with patch.object(installer.os, "rename", side_effect=fail_second_swap):
            self.assertEqual(self.run_cli("--all", "--upgrade", "--apply"), 1)
        for name, state in before.items():
            self.assertEqual(installer.fingerprint(self.destination / name), state)
        self.assertFalse(list(self.destination.parent.glob(".skill-stage-*")))

    def test_changed_target_and_existing_lock_block_application(self) -> None:
        self.assertEqual(self.run_cli("--all", "--apply"), 0)
        (self.source / "skill-a" / "new.txt").write_text("new", encoding="utf-8")
        plans = installer.make_plan(self.source, self.destination, ["skill-a"], True)
        (self.destination / "skill-a" / "concurrent.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            installer.apply_plan(plans, self.destination, self.backups)
        self.assertTrue((self.destination / "skill-a" / "concurrent.txt").exists())
        lock = self.destination.parent / ".skills-install.lock"
        lock.mkdir()
        self.assertEqual(self.run_cli("--all", "--upgrade", "--apply"), 1)
        self.assertTrue(lock.exists())


if __name__ == "__main__":
    unittest.main()
