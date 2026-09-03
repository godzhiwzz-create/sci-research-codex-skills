#!/usr/bin/env python3
"""Read-only candidate scan for workflow-tool disclosure in external packages.

Exit codes: 0=no candidates in fully scanned supported content; 1=candidates;
2=incomplete scan or invalid input. A clean scan is never disclosure approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import TypeVar, cast
from xml.etree import ElementTree


TEXT_SUFFIXES = {
    ".bash", ".bbx", ".bib", ".bst", ".cbx", ".cff", ".cfg", ".cls", ".conf",
    ".css", ".csv", ".dtx", ".eps", ".html", ".ini", ".ins", ".js",
    ".ipynb", ".json", ".log", ".ltx", ".lua", ".md", ".py", ".r", ".rst",
    ".rtf", ".sh", ".sty", ".svg", ".tex", ".toml", ".ts", ".tsv",
    ".txt", ".xml", ".yaml", ".yml", ".zsh",
}
OOXML_SUFFIXES = {".docx", ".docm", ".pptx", ".pptm", ".xlsx", ".xlsm", ".odt", ".ods", ".odp"}
IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff"}
EXPECTED_BUT_UNSUPPORTED = {".doc", ".pages", ".key", ".numbers", ".7z", ".rar", ".tar", ".gz", ".tgz"}
CONTAINER_SUFFIXES = {".zip"}
TEXT_FILENAMES = {
    ".dockerignore", ".gitattributes", ".gitignore", "citation", "dockerfile",
    "license", "makefile", "mimetype", "readme",
}
IGNORABLE_SYSTEM_FILENAMES = {".ds_store", "thumbs.db"}
SOURCE_LABEL_MAX_CHARS = 500
REPORT_TEXT_MAX_CHARS = 500
MATCH_TEXT_MAX_CHARS = 200
ReportItem = TypeVar("ReportItem")

PATTERNS = {
    "named_ai_tool": re.compile(
        r"\b(?:Chat\s*GPT|Codex|OpenA[Iil1]|Claude|Gemini|Copilot|DeepSeek|GPT[- ]?\d(?:\.\d+)?[A-Za-z]?)\b",
        re.IGNORECASE,
    ),
    "generic_ai_disclosure": re.compile(
        r"(?:\b(?:artificial intelligence|generative[- ]AI|large language model(?:s)?|LLM(?:s)?|AI[- ]assisted|AI tool(?:s)?)\b|人工智能|大语言模型|AI\s*辅助)",
        re.IGNORECASE,
    ),
    "direct_ai_use_statement": re.compile(
        r"(?:\b(?:we|I|the authors?)\s+(?:used?|utili[sz]ed?|employed?|applied?)\s+(?:an?\s+)?AI\b|本文\s*使用\s*(?:了\s*)?(?:AI|人工智能))",
        re.IGNORECASE,
    ),
    "workflow_automation": re.compile(
        r"(?:\b(?:browser automation|coding assistant(?:s)?|code generator(?:s)?|translation tool(?:s)?|writing assistant(?:s)?|AI agent(?:s)?|agentic tool(?:s)?|plugin(?:s)?)\b|浏览器自动化|代码生成器|翻译工具|写作助手|AI\s*智能体|插件)",
        re.IGNORECASE,
    ),
}


@dataclass
class ScanBudget:
    """Package-wide runtime, tool-call, finding, and report-output limits."""

    max_tool_calls: int
    max_total_seconds: float
    max_findings: int
    max_output_items: int
    started_at: float = field(default_factory=time.monotonic)
    used_tool_calls: int = 0
    used_findings: int = 0
    incomplete_reasons: set[str] = field(default_factory=set)

    def mark_incomplete(self, reason: str) -> None:
        self.incomplete_reasons.add(reason)

    def remaining_seconds(self) -> float:
        return self.max_total_seconds - (time.monotonic() - self.started_at)

    def expired(self) -> bool:
        if self.remaining_seconds() <= 0:
            self.mark_incomplete("package total-time budget exhausted")
            return True
        return False

    def tool_timeout(self, requested_seconds: float) -> tuple[float | None, str | None]:
        if self.expired():
            return None, "package total-time budget exhausted"
        if self.used_tool_calls >= self.max_tool_calls:
            self.mark_incomplete("package external-tool-call budget exhausted")
            return None, "package external-tool-call budget exhausted"
        self.used_tool_calls += 1
        return min(requested_seconds, max(self.remaining_seconds(), 0.001)), None


@dataclass
class ArchiveBudget:
    """A package-wide budget shared by nested archives and OOXML containers."""

    max_members: int
    max_expanded_bytes: int
    max_member_bytes: int
    max_compression_ratio: float
    used_members: int = 0
    used_expanded_bytes: int = 0

    def reserve(self, info: zipfile.ZipInfo) -> str | None:
        if self.used_members >= self.max_members:
            return "archive member budget exhausted"
        self.used_members += 1
        if info.file_size > self.max_member_bytes:
            return "member exceeds size limit"
        if info.file_size and info.file_size / max(info.compress_size, 1) > self.max_compression_ratio:
            return "member exceeds compression-ratio limit"
        if self.used_expanded_bytes + info.file_size > self.max_expanded_bytes:
            return "archive expanded-byte budget exhausted"
        self.used_expanded_bytes += info.file_size
        return None


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("must be finite and greater than zero")
    return parsed


def read_limited_bytes(path: Path, max_bytes: int) -> tuple[bytes | None, str | None]:
    with path.open("rb") as handle:
        data = handle.read(max_bytes + 1)
    if len(data) > max_bytes:
        return None, "input exceeds size limit"
    return data, None


def bounded_source_label(source: str) -> str:
    """Keep report labels bounded while retaining recognizable ends and identity."""

    normalized = " ".join(source.split())
    if len(normalized) <= SOURCE_LABEL_MAX_CHARS:
        return normalized
    digest = hashlib.sha256(source.encode("utf-8", errors="surrogatepass")).hexdigest()[:12]
    marker = f"...[sha256:{digest}]..."
    remaining = SOURCE_LABEL_MAX_CHARS - len(marker)
    prefix_length = remaining // 2
    suffix_length = remaining - prefix_length
    return f"{normalized[:prefix_length]}{marker}{normalized[-suffix_length:]}"


def bounded_report_text(value: object, max_chars: int = REPORT_TEXT_MAX_CHARS) -> str:
    """Collapse control whitespace and bound one free-text report field."""

    return " ".join(str(value).split())[:max_chars]


def read_tool_output(
    path: Path,
    max_bytes: int,
    tool_name: str,
) -> tuple[bytes | None, str | None]:
    """Check a completed tool output's size before any bounded read."""

    try:
        if path.stat().st_size > max_bytes:
            return None, f"{tool_name} output exceeds size limit"
        data, read_error = read_limited_bytes(path, max_bytes)
    except OSError as exc:
        return None, f"{tool_name} output read failed: {type(exc).__name__}"
    if read_error:
        return None, f"{tool_name} output exceeds size limit"
    return data, None


def is_text_name(name: str) -> bool:
    path = PurePosixPath(name)
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.lower() in TEXT_FILENAMES


def is_ignorable_system_file(name: str) -> bool:
    path = PurePosixPath(name)
    return (
        path.name.lower() in IGNORABLE_SYSTEM_FILENAMES
        or path.name.startswith("._")
    )


def decode_text(data: bytes) -> str | None:
    for encoding in ("utf-8", "utf-8-sig", "utf-16", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def xml_text(data: bytes) -> tuple[str | None, str | None]:
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", data, re.IGNORECASE):
        return decode_text(data), "XML entity/DOCTYPE declarations require manual review"
    try:
        root = ElementTree.fromstring(data)
    except (ElementTree.ParseError, LookupError, ValueError):
        return decode_text(data), "XML parse failed"

    values: list[str] = []
    blocks = [
        element
        for element in root.iter()
        if str(element.tag).rsplit("}", 1)[-1].lower() in {"h", "is", "p", "si"}
    ]
    if not blocks:
        blocks = [root]
    for element in blocks:
        fragments = [text for text in element.itertext() if text]
        exact = "".join(fragments).strip()
        if exact and exact not in values:
            values.append(exact)
    values.extend(
        value.strip()
        for element in root.iter()
        for value in element.attrib.values()
        if value.strip() and value.strip() not in values
    )
    return "\n".join(values), None


def match_text(text: str, source: str, scan_budget: ScanBudget) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    pages = text.split("\f")
    for page_number, page in enumerate(pages, start=1):
        for line_number, line in enumerate(page.splitlines(), start=1):
            if scan_budget.expired():
                return findings
            normalized = " ".join(line.split())
            if not normalized:
                continue
            for category, pattern in PATTERNS.items():
                matches = sorted({item.group(0) for item in pattern.finditer(normalized)})[:20]
                if matches:
                    if scan_budget.used_findings >= scan_budget.max_findings:
                        scan_budget.mark_incomplete("finding output limit exhausted")
                        return findings
                    scan_budget.used_findings += 1
                    findings.append({
                        "source": source,
                        "page": page_number if len(pages) > 1 else None,
                        "line": line_number,
                        "category": category,
                        "matches": matches,
                        "context": normalized[:500],
                    })
    return findings


def pdf_text(
    path: Path,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
) -> tuple[str | None, str | None]:
    executable = shutil.which("pdftotext")
    if not executable:
        return None, "pdftotext not available"
    timeout, budget_error = scan_budget.tool_timeout(timeout_seconds)
    if budget_error:
        return None, budget_error
    assert timeout is not None
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as output_stream:
        output_path = Path(output_stream.name)
    try:
        try:
            completed = subprocess.run(
                [executable, "-layout", str(path), str(output_path)],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return None, "pdftotext timed out"
        if completed.returncode != 0:
            return None, f"pdftotext failed with exit code {completed.returncode}"
        output, read_error = read_tool_output(
            output_path,
            max_tool_output_bytes,
            "pdftotext",
        )
        if read_error:
            return None, read_error
        assert output is not None
        text = output.decode("utf-8", errors="replace")
    finally:
        output_path.unlink(missing_ok=True)
    if not text.strip():
        return None, "PDF has no extractable text; OCR/manual review required"
    return text, None


def pdf_bytes_text(
    data: bytes,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
) -> tuple[str | None, str | None]:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as stream:
        stream.write(data)
        temporary = Path(stream.name)
    try:
        return pdf_text(temporary, timeout_seconds, max_tool_output_bytes, scan_budget)
    finally:
        temporary.unlink(missing_ok=True)


def image_text(
    path: Path,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
) -> tuple[str | None, str | None]:
    executable = shutil.which("tesseract")
    if not executable:
        return None, "tesseract not available for image OCR"
    timeout, budget_error = scan_budget.tool_timeout(timeout_seconds)
    if budget_error:
        return None, budget_error
    assert timeout is not None
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as output_stream:
        output_path = Path(output_stream.name)
    try:
        try:
            with output_path.open("wb") as output_handle:
                completed = subprocess.run(
                    [executable, str(path), "stdout"],
                    check=False,
                    stdout=output_handle,
                    stderr=subprocess.DEVNULL,
                    timeout=timeout,
                )
        except subprocess.TimeoutExpired:
            return None, "image OCR timed out"
        if completed.returncode != 0:
            return None, f"image OCR failed with exit code {completed.returncode}"
        output, read_error = read_tool_output(
            output_path,
            max_tool_output_bytes,
            "image OCR",
        )
        if read_error:
            return None, read_error
        assert output is not None
        return output.decode("utf-8", errors="replace"), None
    finally:
        output_path.unlink(missing_ok=True)


def image_bytes_text(
    data: bytes,
    suffix: str,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
) -> tuple[str | None, str | None]:
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as stream:
        stream.write(data)
        temporary = Path(stream.name)
    try:
        return image_text(temporary, timeout_seconds, max_tool_output_bytes, scan_budget)
    finally:
        temporary.unlink(missing_ok=True)


def scan_ooxml_bytes(
    data: bytes,
    source: str,
    budget: ArchiveBudget,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[str]]:
    findings: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    checked: list[str] = []
    try:
        archive = zipfile.ZipFile(BytesIO(data))
    except zipfile.BadZipFile as exc:
        return findings, [{"source": source, "reason": f"invalid OOXML/ODF archive: {type(exc).__name__}"}], checked
    with archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        xml_members = [item for item in members if Path(item.filename).suffix.lower() in {".xml", ".rels"}]
        if not xml_members:
            skipped.append({"source": source, "reason": "no XML content found"})
        for info in members:
            if scan_budget.expired():
                skipped.append({"source": source, "reason": "package total-time budget exhausted"})
                break
            member_source = bounded_source_label(f"{source}!{info.filename}")
            findings.extend(match_text(info.filename, member_source, scan_budget))
            limit_error = budget.reserve(info)
            if limit_error:
                skipped.append({"source": member_source, "reason": limit_error})
                if limit_error == "archive member budget exhausted":
                    break
                continue
            suffix = Path(info.filename).suffix.lower()
            try:
                member_data = archive.read(info)
            except (EOFError, KeyError, NotImplementedError, OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
                skipped.append({"source": member_source, "reason": f"read failed: {type(exc).__name__}"})
                continue
            if is_ignorable_system_file(info.filename):
                continue
            if suffix in {".xml", ".rels"}:
                text, error = xml_text(member_data)
                if error:
                    skipped.append({"source": member_source, "reason": error})
                if text is not None:
                    if not error:
                        checked.append(member_source)
                    findings.extend(match_text(text, member_source, scan_budget))
            elif is_text_name(info.filename):
                text = decode_text(member_data)
                if text is None:
                    skipped.append({"source": member_source, "reason": "text decoding failed"})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text, member_source, scan_budget))
            elif suffix in IMAGE_SUFFIXES:
                text, error = image_bytes_text(
                    member_data,
                    suffix,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": member_source, "reason": error})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text or "", member_source, scan_budget))
            elif suffix == ".pdf":
                text, error = pdf_bytes_text(
                    member_data,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": member_source, "reason": error})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text or "", member_source, scan_budget))
            elif suffix in OOXML_SUFFIXES | CONTAINER_SUFFIXES | EXPECTED_BUT_UNSUPPORTED | {".bin"}:
                skipped.append({"source": member_source, "reason": "embedded object format unsupported"})
            elif {part.lower() for part in PurePosixPath(info.filename).parts} & {"embeddings", "media", "objectreplacements"}:
                skipped.append({"source": member_source, "reason": "embedded media format unsupported"})
            else:
                skipped.append({"source": member_source, "reason": "unclassified OOXML/ODF member format"})
    return findings, skipped, checked


def scan_zip_bytes(
    data: bytes,
    source: str,
    budget: ArchiveBudget,
    max_depth: int,
    timeout_seconds: float,
    max_tool_output_bytes: int,
    scan_budget: ScanBudget,
    depth: int = 0,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[str], list[str]]:
    findings: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    checked: list[str] = []
    not_applicable: list[str] = []
    if depth > max_depth:
        return findings, [{"source": source, "reason": "nested archive exceeds depth limit"}], checked, not_applicable
    try:
        archive = zipfile.ZipFile(BytesIO(data))
    except zipfile.BadZipFile as exc:
        return findings, [{"source": source, "reason": f"invalid zip: {type(exc).__name__}"}], checked, not_applicable
    with archive:
        members = [item for item in archive.infolist() if not item.is_dir()]
        for info in members:
            if scan_budget.expired():
                skipped.append({"source": source, "reason": "package total-time budget exhausted"})
                break
            member_source = bounded_source_label(f"{source}!{info.filename}")
            findings.extend(match_text(info.filename, member_source, scan_budget))
            limit_error = budget.reserve(info)
            if limit_error:
                skipped.append({"source": member_source, "reason": limit_error})
                if limit_error == "archive member budget exhausted":
                    break
                continue
            suffix = Path(info.filename).suffix.lower()
            try:
                member_data = archive.read(info)
            except (EOFError, KeyError, NotImplementedError, OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
                skipped.append({"source": member_source, "reason": f"read failed: {type(exc).__name__}"})
                continue
            if is_ignorable_system_file(info.filename):
                not_applicable.append(member_source)
            elif is_text_name(info.filename):
                text = decode_text(member_data)
                if text is None:
                    skipped.append({"source": member_source, "reason": "text decoding failed"})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text, member_source, scan_budget))
            elif suffix in OOXML_SUFFIXES:
                f, s, c = scan_ooxml_bytes(
                    member_data,
                    member_source,
                    budget,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                findings.extend(f); skipped.extend(s); checked.extend(c)
            elif suffix == ".pdf":
                text, error = pdf_bytes_text(
                    member_data,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": member_source, "reason": error})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text or "", member_source, scan_budget))
            elif suffix in IMAGE_SUFFIXES:
                text, error = image_bytes_text(
                    member_data,
                    suffix,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": member_source, "reason": error})
                else:
                    checked.append(member_source)
                    findings.extend(match_text(text or "", member_source, scan_budget))
            elif suffix in CONTAINER_SUFFIXES:
                f, s, c, n = scan_zip_bytes(
                    member_data,
                    member_source,
                    budget,
                    max_depth,
                    timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                    depth + 1,
                )
                findings.extend(f); skipped.extend(s); checked.extend(c); not_applicable.extend(n)
            elif suffix in EXPECTED_BUT_UNSUPPORTED:
                skipped.append({"source": member_source, "reason": "external document format unsupported"})
            else:
                skipped.append({"source": member_source, "reason": "unclassified archive member format"})
    return findings, skipped, checked, not_applicable


def has_symlink_component(path: Path) -> bool:
    absolute = path if path.is_absolute() else Path.cwd() / path
    trusted_anchors = (Path.cwd().absolute(), Path.home().absolute(), Path(tempfile.gettempdir()).absolute())
    candidates = [anchor for anchor in trusted_anchors if absolute.is_relative_to(anchor)]
    boundary = max(candidates, key=lambda item: len(item.parts)) if candidates else Path(absolute.anchor)
    current = boundary
    parts = absolute.relative_to(boundary).parts
    for part in parts:
        if part in {"", "."}:
            continue
        if part == "..":
            current = current.parent
            continue
        current /= part
        if current.is_symlink():
            return True
    return False


def candidate_files(
    inputs: list[Path], max_files: int, scan_budget: ScanBudget
) -> tuple[list[tuple[Path, str]], list[dict[str, object]]]:
    files: dict[Path, str] = {}
    skipped: list[dict[str, object]] = []

    def add_skipped(source: str, reason: str) -> None:
        skipped.append({"source": bounded_source_label(source), "reason": reason})

    for input_number, item in enumerate(inputs, start=1):
        if scan_budget.expired():
            add_skipped("coverage", "package total-time budget exhausted")
            break
        label = f"input-{input_number}"
        if has_symlink_component(item):
            add_skipped(f"{label}/{item.name}", "path contains symbolic-link component")
        elif item.is_file():
            absolute = item.absolute()
            if absolute not in files and len(files) >= max_files:
                add_skipped(label, "input file budget exhausted")
            else:
                files.setdefault(absolute, f"{label}/{item.name}")
        elif item.is_dir():
            saw_file_or_link = False
            traversal_failed = False
            try:
                for path in item.rglob("*"):
                    if scan_budget.expired():
                        add_skipped(label, "package total-time budget exhausted")
                        traversal_failed = True
                        break
                    member_label = f"{label}/{path.relative_to(item).as_posix()}"
                    if path.is_symlink():
                        saw_file_or_link = True
                        add_skipped(member_label, "symbolic link not followed")
                    elif path.is_file():
                        saw_file_or_link = True
                        absolute = path.absolute()
                        if absolute not in files and len(files) >= max_files:
                            add_skipped(label, "input file budget exhausted")
                            break
                        files.setdefault(absolute, member_label)
            except OSError as exc:
                traversal_failed = True
                add_skipped(label, f"directory traversal failed: {type(exc).__name__}")
            if not saw_file_or_link and not traversal_failed:
                add_skipped(label, "input directory contains no files")
        else:
            add_skipped(label, "input path not found")
    return sorted(files.items(), key=lambda pair: pair[1]), skipped


def logical_relative_name(source: str) -> str:
    """Remove only the synthetic input-N prefix used to hide real input roots."""

    _, separator, relative = source.partition("/")
    return relative if separator else source


def bound_report_output(
    scan_budget: ScanBudget,
    findings: list[dict[str, object]],
    skipped: list[dict[str, object]],
    checked: list[str],
    not_applicable: list[str],
    inventory: list[dict[str, object]],
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[str],
    list[str],
    list[dict[str, object]],
]:
    """Bound all variable-length report arrays and retain an explicit limit notice."""

    sanitized_findings: list[dict[str, object]] = []
    for finding in findings:
        sanitized = dict(finding)
        sanitized["source"] = bounded_source_label(str(finding.get("source", "")))
        sanitized["context"] = bounded_report_text(finding.get("context", ""))
        sanitized["matches"] = [
            bounded_report_text(value, MATCH_TEXT_MAX_CHARS)
            for value in cast(list[object], finding.get("matches", []))[:20]
        ]
        sanitized_findings.append(sanitized)
    findings = sanitized_findings
    skipped = [
        {
            "source": bounded_source_label(str(item.get("source", ""))),
            "reason": bounded_report_text(item.get("reason", "")),
        }
        for item in skipped
    ]
    checked = [bounded_source_label(item) for item in checked]
    not_applicable = [bounded_source_label(item) for item in not_applicable]
    inventory = [
        {**item, "path": bounded_source_label(str(item.get("path", "")))}
        for item in inventory
    ]

    raw_total = len(findings) + len(skipped) + len(checked) + len(not_applicable) + len(inventory)
    notice_needed = bool(scan_budget.incomplete_reasons)
    if raw_total + int(notice_needed) > scan_budget.max_output_items:
        scan_budget.mark_incomplete("report output item limit exhausted")

    bounded_findings: list[dict[str, object]] = []
    bounded_skipped: list[dict[str, object]] = []
    bounded_checked: list[str] = []
    bounded_not_applicable: list[str] = []
    bounded_inventory: list[dict[str, object]] = []
    remaining = scan_budget.max_output_items

    if scan_budget.incomplete_reasons and remaining:
        reasons = "; ".join(sorted(scan_budget.incomplete_reasons))
        bounded_skipped.append({"source": "coverage", "reason": reasons[:500]})
        remaining -= 1

    def take(target: list[ReportItem], values: list[ReportItem]) -> None:
        nonlocal remaining
        count = min(remaining, len(values))
        target.extend(values[:count])
        remaining -= count

    # Findings are the review-critical sample; coverage details follow.
    take(bounded_findings, findings)
    take(bounded_skipped, skipped)
    take(bounded_inventory, inventory)
    take(bounded_checked, checked)
    take(bounded_not_applicable, not_applicable)
    return (
        bounded_findings,
        bounded_skipped,
        bounded_checked,
        bounded_not_applicable,
        bounded_inventory,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-files", type=positive_int, default=10_000, help="Maximum top-level files")
    parser.add_argument("--max-file-mb", type=positive_int, default=100, help="Maximum bytes read from one input file, in MiB")
    parser.add_argument("--max-total-mb", type=positive_int, default=1024, help="Package-wide input-byte budget, in MiB")
    parser.add_argument("--max-member-mb", type=positive_int, default=25, help="Maximum expanded archive-member size, in MiB")
    parser.add_argument("--max-members", type=positive_int, default=5000, help="Package-wide archive-member budget")
    parser.add_argument("--max-expanded-mb", type=positive_int, default=512, help="Package-wide expanded archive-byte budget, in MiB")
    parser.add_argument("--max-compression-ratio", type=positive_float, default=200.0, help="Maximum archive-member expansion ratio")
    parser.add_argument("--max-depth", type=positive_int, default=2, help="Maximum nested ZIP depth")
    parser.add_argument("--tool-timeout-seconds", type=positive_float, default=30.0, help="Timeout for each PDF/OCR subprocess")
    parser.add_argument("--max-tool-output-mb", type=positive_int, default=50, help="Maximum text output read from one PDF/OCR subprocess, in MiB")
    parser.add_argument("--max-tool-calls", type=positive_int, default=250, help="Package-wide PDF/OCR subprocess-call budget")
    parser.add_argument("--max-total-seconds", type=positive_float, default=300.0, help="Package-wide elapsed-time budget")
    parser.add_argument("--max-findings", type=positive_int, default=1000, help="Maximum candidate findings retained")
    parser.add_argument("--max-output-items", type=positive_int, default=5000, help="Maximum variable-length report entries")
    args = parser.parse_args()

    scan_budget = ScanBudget(
        max_tool_calls=args.max_tool_calls,
        max_total_seconds=args.max_total_seconds,
        max_findings=args.max_findings,
        max_output_items=args.max_output_items,
    )
    files, boundary_skipped = candidate_files(args.paths, args.max_files, scan_budget)

    findings: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = list(boundary_skipped)
    checked: list[str] = []
    not_applicable: list[str] = []
    inventory: list[dict[str, object]] = []
    max_file_bytes = args.max_file_mb * 1024 * 1024
    max_total_bytes = args.max_total_mb * 1024 * 1024
    max_tool_output_bytes = args.max_tool_output_mb * 1024 * 1024
    input_bytes_used = 0
    input_budget_exhausted = False
    budget = ArchiveBudget(
        max_members=args.max_members,
        max_expanded_bytes=args.max_expanded_mb * 1024 * 1024,
        max_member_bytes=args.max_member_mb * 1024 * 1024,
        max_compression_ratio=args.max_compression_ratio,
    )

    for path, source in files:
        report_source = bounded_source_label(source)
        if scan_budget.expired():
            skipped.append({"source": report_source, "reason": "package total-time budget exhausted"})
            break
        suffix = path.suffix.lower()
        try:
            if input_budget_exhausted:
                skipped.append({"source": report_source, "reason": "package input-byte budget exhausted"})
                continue
            remaining_bytes = max_total_bytes - input_bytes_used
            read_limit = min(max_file_bytes, remaining_bytes)
            data, read_error = read_limited_bytes(path, read_limit)
            if read_error:
                inventory.append({"path": report_source, "size": path.stat().st_size, "sha256": None})
                if read_limit < max_file_bytes:
                    read_error = "package input-byte budget exhausted"
                    input_budget_exhausted = True
                skipped.append({"source": report_source, "reason": read_error})
                continue
            assert data is not None
            input_bytes_used += len(data)
            inventory.append({"path": report_source, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            if is_ignorable_system_file(path.name):
                not_applicable.append(report_source)
                continue

            findings.extend(match_text(logical_relative_name(source), report_source, scan_budget))
            if is_text_name(path.name):
                text = decode_text(data)
                if text is None:
                    skipped.append({"source": report_source, "reason": "text decoding failed"})
                else:
                    checked.append(report_source)
                    findings.extend(match_text(text, report_source, scan_budget))
            elif suffix in OOXML_SUFFIXES:
                f, s, c = scan_ooxml_bytes(
                    data,
                    report_source,
                    budget,
                    args.tool_timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                findings.extend(f); skipped.extend(s); checked.extend(c)
            elif suffix == ".pdf":
                text, error = pdf_bytes_text(
                    data,
                    args.tool_timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": report_source, "reason": error})
                else:
                    checked.append(report_source)
                    findings.extend(match_text(text or "", report_source, scan_budget))
            elif suffix in IMAGE_SUFFIXES:
                text, error = image_bytes_text(
                    data,
                    suffix,
                    args.tool_timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                if error:
                    skipped.append({"source": report_source, "reason": error})
                else:
                    checked.append(report_source)
                    findings.extend(match_text(text or "", report_source, scan_budget))
            elif suffix in CONTAINER_SUFFIXES:
                f, s, c, n = scan_zip_bytes(
                    data,
                    report_source,
                    budget,
                    args.max_depth,
                    args.tool_timeout_seconds,
                    max_tool_output_bytes,
                    scan_budget,
                )
                findings.extend(f); skipped.extend(s); checked.extend(c); not_applicable.extend(n)
            elif suffix in EXPECTED_BUT_UNSUPPORTED:
                skipped.append({"source": report_source, "reason": "external document format unsupported"})
            else:
                skipped.append({"source": report_source, "reason": "unclassified input format"})
        except OSError as exc:
            skipped.append({"source": report_source, "reason": f"input read failed: {type(exc).__name__}"})

    scan_budget.expired()
    if not checked and not skipped:
        skipped.append({"source": "coverage", "reason": "no supported content was checked"})

    if scan_budget.incomplete_reasons or skipped:
        status = "incomplete_scan"
    elif findings:
        status = "candidates_found"
    else:
        status = "no_candidates_found"
    findings, skipped, checked, not_applicable, inventory = bound_report_output(
        scan_budget,
        findings,
        skipped,
        checked,
        not_applicable,
        inventory,
    )
    if scan_budget.incomplete_reasons:
        status = "incomplete_scan"
    report = {
        "status": status,
        "note": "Candidates require author review; this scan neither grants approval nor verifies venue compliance. Input roots are replaced by input-N labels; the report still contains filenames, hashes, and matched context and should remain internal unless separately reviewed.",
        "coverage": {
            "checked": checked,
            "not_applicable": not_applicable,
            "skipped": skipped,
            "human_review_required": [
                "semantic interpretation of every candidate",
                "visual/layout review of rendered external artifacts",
                "portal fields, checkboxes, and dynamically rendered text",
            ],
        },
        "inventory": inventory,
        "findings": findings,
        "limits": {
            "tool_calls_used": scan_budget.used_tool_calls,
            "findings_retained": len(findings),
            "output_items_retained": (
                len(findings) + len(skipped) + len(checked) + len(not_applicable) + len(inventory)
            ),
        },
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {status}")
        print(report["note"])
        print(f"Files inventoried: {len(inventory)}; checked units: {len(checked)}; candidates: {len(findings)}; skipped: {len(skipped)}")
        for finding in findings:
            location = str(finding["source"])
            if finding["page"]:
                location += f":page {finding['page']}"
            location += f":line {finding['line']}"
            print(f"- [{finding['category']}] {location}")
            print(f"  matches={', '.join(cast(list[str], finding['matches']))}")
            print(f"  {finding['context']}")
        for item in skipped:
            print(f"- [skipped] {item['source']}: {item['reason']}")

    if skipped or scan_budget.incomplete_reasons:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
