from __future__ import annotations

import re
import unittest
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

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src", "poster"} and value:
                self.refs.append(value)


def is_external(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "mailto", "data"} or value.startswith("#")


class RepositoryLinkTests(unittest.TestCase):
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
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
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
