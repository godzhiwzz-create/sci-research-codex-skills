from __future__ import annotations

import re
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)


class LocalRefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src", "poster"} and value:
                self.refs.append(value)
            if name == "id" and value:
                self.ids.append(value)


def is_external(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "mailto", "data"} or value.startswith("#")


class RepositoryLinkTests(unittest.TestCase):
    def test_homepages_keep_release_history_in_dedicated_documents(self) -> None:
        for relative in ("README.md", "docs/index.html"):
            with self.subTest(page=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"\bv\d+\.\d+\.\d+\b")
                self.assertNotIn("shields.io/github/v/release", text)
                self.assertNotIn("Unreleased", text)
                self.assertNotIn("release-strip", text)
                self.assertNotIn("当前版本", text)
        self.assertIn("(CHANGELOG.md)", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_homepage_exposes_all_skills_and_safe_install_commands(self) -> None:
        text = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        parser = LocalRefParser()
        parser.feed(text)
        skill_links = {ref.rsplit("/", 1)[-1] for ref in parser.refs if "/tree/main/skills/" in ref}
        expected = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(skill_links, expected)
        commands = {name: unescape(value) for name, value in re.findall(
            r'<code id="([^"]+)">([^<]+)</code>', text
        )}
        copy_targets = re.findall(r'data-copy="([^"]+)" hidden', text)
        self.assertEqual(set(copy_targets), set(commands))
        self.assertNotIn("--apply", commands["preview-command"])
        self.assertIn("--apply", commands["apply-command"])
        self.assertIn('role="status" aria-live="polite"', text)
        self.assertIn('<noscript>', text)

    def test_homepage_navigation_targets_exist_and_are_unique(self) -> None:
        parser = LocalRefParser()
        parser.feed((ROOT / "docs/index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        targets = [unquote(ref[1:]) for ref in parser.refs if ref.startswith("#")]
        self.assertTrue(targets)
        for target in targets:
            with self.subTest(target=target):
                self.assertIn(target, parser.ids)

    def test_repository_markdown_links(self) -> None:
        files = [
            *sorted(ROOT.glob("*.md")),
            *sorted((ROOT / ".github").glob("*.md")),
            *sorted((ROOT / "docs").rglob("*.md")),
        ]
        for source in files:
            text = FENCED_CODE_RE.sub("", source.read_text(encoding="utf-8", errors="replace"))
            for match in LINK_RE.finditer(text):
                raw = match.group(1).strip()
                target = raw[1 : raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
                if is_external(target):
                    continue
                path_text = unquote(urlparse(target).path)
                if not path_text:
                    continue
                with self.subTest(source=str(source.relative_to(ROOT)), target=target):
                    self.assertTrue((source.parent / path_text).exists())

    def test_repository_community_files(self) -> None:
        expected = [
            ROOT / "CHANGELOG.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "MAINTENANCE.md",
            ROOT / "SECURITY.md",
            ROOT / ".github" / "dependabot.yml",
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
            ROOT / ".github" / "workflows" / "maintenance.yml",
        ]
        for path in expected:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn(f"## [{version}]", changelog)

    def test_docs_html_local_assets(self) -> None:
        for source in sorted((ROOT / "docs").rglob("*.html")):
            parser = LocalRefParser()
            parser.feed(source.read_text(encoding="utf-8", errors="replace"))
            for target in parser.refs:
                if is_external(target) or target.startswith("/"):
                    continue
                path_text = unquote(urlparse(target).path)
                if not path_text:
                    continue
                with self.subTest(source=str(source.relative_to(ROOT)), target=target):
                    self.assertTrue((source.parent / path_text).exists())


if __name__ == "__main__":
    unittest.main()
