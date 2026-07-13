from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_NAMES = {
    "academic-manuscript-writing",
    "sci-asset-manager",
    "sci-experiment-manager",
    "sci-literature-manager",
    "sci-paper-manager",
    "sci-paper-reader",
    "sci-research-manager",
    "sci-result-auditor",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)


def skill_dirs() -> list[Path]:
    return sorted(path.parent for path in SKILLS.glob("*/SKILL.md"))


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must begin with YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise AssertionError("Unclosed YAML frontmatter") from exc
    values: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise AssertionError(f"Unsupported multiline frontmatter: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


class SkillStructureTests(unittest.TestCase):
    def test_expected_public_skill_names_are_preserved(self) -> None:
        self.assertEqual({path.name for path in skill_dirs()}, EXPECTED_NAMES)

    def test_skill_frontmatter_names_lengths_and_placeholders(self) -> None:
        for directory in skill_dirs():
            with self.subTest(skill=directory.name):
                text = (directory / "SKILL.md").read_text(encoding="utf-8")
                meta = frontmatter(text)
                self.assertEqual(set(meta), {"name", "description"})
                self.assertEqual(meta["name"], directory.name)
                self.assertTrue(meta["description"])
                self.assertLess(len(text.splitlines()), 500)
                self.assertNotIn("TODO", text)

    def test_skill_relative_links_resolve(self) -> None:
        for directory in skill_dirs():
            skill_file = directory / "SKILL.md"
            text = FENCED_CODE_RE.sub("", skill_file.read_text(encoding="utf-8"))
            for match in LINK_RE.finditer(text):
                raw = match.group(1).strip()
                target = raw[1 : raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                path_text = unquote(parsed.path)
                if not path_text:
                    continue
                with self.subTest(skill=directory.name, target=target):
                    self.assertTrue((skill_file.parent / path_text).exists())

    def test_openai_metadata_is_present_and_consistent(self) -> None:
        for directory in skill_dirs():
            with self.subTest(skill=directory.name):
                path = directory / "agents" / "openai.yaml"
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                display = re.search(r'^\s*display_name:\s*"([^"]+)"\s*$', text, re.MULTILINE)
                short = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', text, re.MULTILINE)
                prompt = re.search(r'^\s*default_prompt:\s*"([^"]+)"\s*$', text, re.MULTILINE)
                self.assertIsNotNone(display)
                self.assertIsNotNone(short)
                self.assertIsNotNone(prompt)
                assert short is not None
                assert prompt is not None
                self.assertGreaterEqual(len(short.group(1)), 25)
                self.assertLessEqual(len(short.group(1)), 64)
                self.assertIn(f"${directory.name}", prompt.group(1))

    def test_python_scripts_compile(self) -> None:
        scripts = [
            *sorted((ROOT / "scripts").glob("*.py")),
            *sorted(SKILLS.glob("*/scripts/*.py")),
        ]
        self.assertGreaterEqual(len(scripts), 7)
        for path in scripts:
            with self.subTest(script=str(path.relative_to(ROOT))):
                compile(path.read_text(encoding="utf-8"), str(path), "exec")


if __name__ == "__main__":
    unittest.main()
