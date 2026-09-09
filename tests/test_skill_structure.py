from __future__ import annotations

import re
import unittest
from ipaddress import IPv4Address, IPv4Network
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
PRIVATE_PATTERNS = {
    "macOS user-home path": re.compile("/" + "Users" + r"/[^/\s]+/"),
    "Linux user-home path": re.compile("/" + "home" + r"/[^/\s]+/"),
    "mounted personal path": re.compile("/" + "Volumes" + r"/[^/\s]+/"),
    "Windows user-home path": re.compile(r"[A-Za-z]:\\" + "Users" + r"\\[^\\\s]+\\"),
    "GitHub access token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "GitHub fine-grained token": re.compile("github" + r"_pat_[A-Za-z0-9_]{20,}"),
    "API secret token": re.compile("sk" + r"-[A-Za-z0-9_-]{16,}"),
    "AWS access key": re.compile("AK" + "IA" + r"[0-9A-Z]{16}"),
    "private key block": re.compile("BEGIN " + r"(?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    "provider-specific infrastructure": re.compile("auto" + "dl", re.IGNORECASE),
}
IPV4_RE = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
EXAMPLE_NETWORKS = tuple(IPv4Network(network) for network in (
    "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "127.0.0.0/8",
))
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
ALLOWED_EMAIL_DOMAINS = {"example.invalid", "users.noreply.github.com"}
IGNORED_TREE_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"}
TEXT_SUFFIXES = {
    "", ".cfg", ".css", ".csv", ".env", ".html", ".ini", ".js", ".json", ".md", ".py", ".svg",
    ".rst", ".sh", ".toml", ".tsv", ".txt", ".yaml", ".yml",
}


def skill_dirs() -> list[Path]:
    return sorted(path.parent for path in SKILLS.glob("*/SKILL.md"))


def non_example_ips(text: str) -> list[str]:
    findings = []
    for match in IPV4_RE.finditer(text):
        try:
            address = IPv4Address(match.group())
        except ValueError:
            continue
        if not any(address in network for network in EXAMPLE_NETWORKS):
            findings.append(match.group())
    return findings


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
            for source in sorted(directory.rglob("*.md")):
                text = FENCED_CODE_RE.sub("", source.read_text(encoding="utf-8"))
                for match in LINK_RE.finditer(text):
                    raw = match.group(1).strip()
                    target = raw[1 : raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
                    parsed = urlparse(target)
                    if parsed.scheme or target.startswith("#"):
                        continue
                    path_text = unquote(parsed.path)
                    if not path_text:
                        continue
                    resolved = (source.parent / path_text).resolve(strict=False)
                    with self.subTest(skill=directory.name, source=source.name, target=target):
                        self.assertTrue(resolved.is_relative_to(directory.resolve()))
                        self.assertTrue(resolved.exists())

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

    def test_lifecycle_upgrade_preserves_public_ids_and_single_owners(self) -> None:
        research = SKILLS / "sci-research-manager"
        manuscript = SKILLS / "academic-manuscript-writing"
        expected_research_assets = (
            "references/project-literature-interface.md",
            "references/experiment-library-lifecycle.md",
            "references/research-library-workflow.md",
            "references/manuscript-stage-workflows.md",
            "references/final-submission-audit.md",
            "scripts/audit_research_libraries.py",
            "scripts/scan_external_disclosures.py",
        )
        expected_manuscript_assets = (
            "references/stage-router.md",
            "references/writing-standards.md",
            "references/revision-and-response.md",
            "references/submission-handoff.md",
        )
        for relative in expected_research_assets:
            with self.subTest(asset=relative):
                self.assertTrue((research / relative).is_file())
        for relative in expected_manuscript_assets:
            with self.subTest(asset=relative):
                self.assertTrue((manuscript / relative).is_file())

        research_text = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(research.rglob("*.md"))
        )
        manuscript_text = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(manuscript.rglob("*.md"))
        )
        self.assertNotIn("research-lifecycle-manager", research_text + manuscript_text)
        self.assertNotIn("manuscript-lifecycle-writing", research_text + manuscript_text)
        self.assertIn("typed handback", research_text)
        self.assertIn("minor_revision_local", manuscript_text)

        card_template = (SKILLS / "sci-experiment-manager/templates/experiment_card_template.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("designed / running / partial / complete / stopped / superseded", card_template)
        self.assertIn("not_assessed / verified / pending_artifact / protocol_mismatch / unverifiable", card_template)
        self.assertIn("continue / redirect / reference_only / stop / needs_literature", card_template)

        paper_status = (SKILLS / "sci-paper-manager/templates/PAPER_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("Current Artifact Layer", paper_status)
        self.assertIn("Manuscript Lifecycle Stage", paper_status)
        self.assertIn("minor_revision_local", paper_status)
        self.assertIn("not_assessed", paper_status)
        self.assertNotIn("needs verification", paper_status)
        self.assertNotIn("Current Paper Stage", paper_status)

        claim_audit = (
            SKILLS / "sci-result-auditor/templates/claim_audit_template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Claim Strength", claim_audit)
        self.assertIn(
            "main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported",
            claim_audit,
        )
        self.assertIn(
            "not_assessed / verified / pending_artifact / protocol_mismatch / unverifiable",
            claim_audit,
        )
        self.assertIn("no_issue / issue_found / incomplete", claim_audit)
        self.assertNotIn("preliminary / weak / moderate / strong", claim_audit)
        self.assertNotIn("supported / partially_supported", claim_audit)

        claim_map = (
            SKILLS / "sci-paper-manager/templates/CLAIM_EVIDENCE_MAP.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Claim Strength", claim_map)
        self.assertIn("Evidence Status", claim_map)
        self.assertIn("Allowed evidence statuses", claim_map)

        paper_manager_metadata = (
            SKILLS / "sci-paper-manager/agents/openai.yaml"
        ).read_text(encoding="utf-8")
        # This checks the routing surface, not actual model behavior (forward-tested separately).
        self.assertIn("manuscript-writing owner", paper_manager_metadata)
        self.assertIn("only when integration is in scope", paper_manager_metadata)
        self.assertNotIn("reconcile this manuscript", paper_manager_metadata)

        paper_reader_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((SKILLS / "sci-paper-reader").rglob("*.md"))
        )
        self.assertIn("typed reading handback", paper_reader_text)
        self.assertNotIn(
            "Decision: use / reference_only / verify_more / reject",
            paper_reader_text,
        )

    def test_repository_text_has_no_private_paths_or_high_confidence_secrets(self) -> None:
        for path in sorted(ROOT.rglob("*")):
            if any(part in IGNORED_TREE_PARTS for part in path.parts):
                continue
            with self.subTest(path=str(path.relative_to(ROOT)), boundary="symlink"):
                self.assertFalse(path.is_symlink(), "repository symlinks require explicit privacy review")
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in PRIVATE_PATTERNS.items():
                with self.subTest(path=str(path.relative_to(ROOT)), pattern=label):
                    self.assertIsNone(pattern.search(text), f"{label} found in {path.relative_to(ROOT)}")
            for match in EMAIL_RE.finditer(text):
                with self.subTest(path=str(path.relative_to(ROOT)), pattern="email"):
                    self.assertIn(match.group(1).lower(), ALLOWED_EMAIL_DOMAINS)
            with self.subTest(path=str(path.relative_to(ROOT)), pattern="non-example IP"):
                self.assertFalse(non_example_ips(text), "use a placeholder host or documentation IP")

    def test_privacy_patterns_have_positive_and_negative_controls(self) -> None:
        positives = {
            "macOS user-home path": "/" + "Users" + "/private-account/work/",
            "Linux user-home path": "/" + "home" + "/private-account/work/",
            "mounted personal path": "/" + "Volumes" + "/PrivateDisk/work/",
            "Windows user-home path": "C:\\" + "Users" + "\\private-account\\work\\",
            "GitHub access token": "gh" + "p_" + "A" * 24,
            "GitHub fine-grained token": "github" + "_pat_" + "A" * 28,
            "API secret token": "sk" + "-" + "A" * 24,
            "AWS access key": "AK" + "IA" + "A" * 16,
            "private key block": "BEGIN " + "PRIVATE KEY",
            "provider-specific infrastructure": "AUTO" + "DL",
        }
        for label, sample in positives.items():
            with self.subTest(pattern=label, control="positive"):
                self.assertIsNotNone(PRIVATE_PATTERNS[label].search(sample))
        for label, pattern in PRIVATE_PATTERNS.items():
            with self.subTest(pattern=label, control="negative"):
                self.assertIsNone(pattern.search("public example with no credential or personal path"))

    def test_ip_privacy_check_allows_only_documentation_and_loopback_examples(self) -> None:
        self.assertEqual(non_example_ips("server " + ".".join(("10", "23", "45", "67"))),
                         [".".join(("10", "23", "45", "67"))])
        self.assertTrue(non_example_ips("server " + ".".join(("8", "8", "4", "4"))))
        self.assertEqual(non_example_ips("192.0.2.1 198.51.100.2 203.0.113.3 127.0.0.1"), [])
        self.assertEqual(non_example_ips("999.999.999.999 research-server"), [])


if __name__ == "__main__":
    unittest.main()
