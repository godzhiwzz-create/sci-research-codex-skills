#!/usr/bin/env python3
"""Read-only structural/semantic-interface audit for research libraries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
TAG_RE = re.compile(r"^[a-z0-9][a-z0-9+._-]*$")
COUNT_PATTERNS = (
    re.compile(r"当前\s*PDF\s*[:：]\s*(\d+)\s*(?:篇|份)", re.IGNORECASE),
    re.compile(r"当前全库(?:为|共)?\s*(\d+)\s*(?:篇|份)", re.IGNORECASE),
    re.compile(r"共\s*(\d+)\s*(?:篇|份)", re.IGNORECASE),
    re.compile(r"^>\s*(\d+)\s*(?:篇|份)\s*PDF", re.IGNORECASE | re.MULTILINE),
)

SOURCE_FIELDS = ("source_id", "tags", "project_role", "reading_depth", "note", "experiments", "claims")
READING_DEPTHS = {"metadata_only", "abstract_checked", "full_read"}
CLAIM_FIELDS = ("literature_claim_id", "source_id", "verification_status", "note_path", "experiments", "manuscript_claims", "verified_at")
CLAIM_STATUSES = {"needs_verification", "claim_verified", "contradicted", "superseded"}
ALIAS_FIELDS = ("alias_source_id", "canonical_source_id", "relation", "verification_source", "verified_at")
ALIAS_RELATIONS = {"duplicate_of", "version_of", "replaced_by", "same_work_as"}
EXPERIMENT_FIELDS = ("experiment_id", "card", "task_stage", "experiment_status", "evidence_status", "claim_strength", "direction_decision", "raw_artifact", "protocol_anchor", "selection_warning", "replacement_id", "last_verified")
TASK_STAGES = {"idea_exploration", "minimal_probe", "formal_experiment", "result_analysis", "paper_writing", "submission_prepare", "maintenance"}
EXPERIMENT_STATUSES = {"designed", "running", "partial", "complete", "stopped", "superseded"}
EVIDENCE_STATUSES = {"not_assessed", "verified", "pending_artifact", "protocol_mismatch", "unverifiable"}
CLAIM_STRENGTHS = {"main_claim", "trend_only", "diagnostic_only", "negative_boundary", "internal_exploration", "unsupported"}
DIRECTION_DECISIONS = {"continue", "redirect", "reference_only", "stop", "needs_literature"}
NONCOMPLETION_EXPERIMENT_STATUSES = {"designed", "running", "partial", "stopped", "superseded"}
CLEAR_SELECTION_WARNINGS = {"none", "not_applicable", "n/a"}
REGISTRY_FIELDS = ("evidence_id", "project", "experiment_id", "question", "canonical_card", "raw_result", "protocol_anchor", "experiment_status", "evidence_status", "claim_strength", "selection_warning", "promotion_reason", "last_verified")
ALLOWED_VALUE_FIELDS = {
    "reading_depth": READING_DEPTHS,
    "claim_status": CLAIM_STATUSES,
    "alias_relation": ALIAS_RELATIONS,
    "task_stage": TASK_STAGES,
    "experiment_status": EXPERIMENT_STATUSES,
    "evidence_status": EVIDENCE_STATUSES,
    "claim_strength": CLAIM_STRENGTHS,
    "direction_decision": DIRECTION_DECISIONS,
}


def issue(items: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    items.append({"severity": severity, "code": code, "message": message})


def exception_label(exc: BaseException) -> str:
    """Return an error class without leaking a local filename from the exception."""
    return type(exc).__name__


def read_tsv(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        fields = tuple(reader.fieldnames or ())
        rows = []
        for raw_row in reader:
            rows.append({
                field: value if isinstance((value := raw_row.get(field)), str) else ""
                for field in fields
            })
        return fields, rows


def local_cell(value: str) -> str:
    value = value.strip()
    match = re.fullmatch(r"\[[^\]]*\]\(([^)]+)\)", value)
    return match.group(1).strip().strip("<>") if match else value


def resolve_path(
    base: Path,
    workspace: Path,
    value: str,
    *,
    allowed_root: Path | None = None,
    allow_absolute: bool = True,
) -> Path | None:
    value = local_cell(value)
    if not value or SCHEME_RE.match(value):
        return None
    path = Path(unquote(urlparse(value).path))
    if path.is_absolute() and not allow_absolute:
        return None
    candidates: tuple[Path, ...]
    if path.is_absolute():
        candidates = (path,)
    else:
        candidates = (base / path, workspace / path)
    boundary = (allowed_root or workspace).resolve(strict=False)
    fallback: Path | None = None
    for candidate in candidates:
        try:
            candidate.resolve(strict=False).relative_to(boundary)
        except (OSError, RuntimeError, ValueError):
            if candidate.exists() or candidate.is_symlink():
                return None
            continue
        if fallback is None:
            fallback = candidate
        if candidate.exists():
            return candidate
    return fallback


def source_id_present(text: str, source_id: str) -> bool:
    token_chars = r"\w./:+;()%@=\-"
    return re.search(
        rf"(?<![{token_chars}]){re.escape(source_id)}(?![{token_chars}])",
        text,
    ) is not None


def markdown_local_links(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return [match.group(1) for match in LINK_RE.finditer(text)]


def layout_path(root: Path, value: Path, *, base: Path | None = None) -> Path:
    candidate = value.expanduser()
    if not candidate.is_absolute():
        candidate = (base or root) / candidate
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("audit path escapes workspace root") from exc
    return resolved


def path_is_within(path: Path, boundary: Path) -> bool:
    """Return whether a path, including any symlink target, stays in boundary."""
    try:
        path.resolve(strict=False).relative_to(boundary.resolve(strict=False))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def parse_allowed_values(specs: list[str]) -> dict[str, set[str]]:
    allowed = {field: set(values) for field, values in ALLOWED_VALUE_FIELDS.items()}
    for spec in specs:
        field, separator, value = spec.partition("=")
        field = field.strip()
        value = value.strip()
        if not separator or field not in allowed or not value:
            choices = ", ".join(sorted(allowed))
            raise ValueError(f"invalid --allow-value {spec!r}; expected FIELD=VALUE where FIELD is one of: {choices}")
        allowed[field].add(value)
    return allowed


def parse_value_mappings(
    specs: list[str], allowed: dict[str, set[str]]
) -> dict[str, dict[str, str]]:
    mappings: dict[str, dict[str, str]] = {field: {} for field in ALLOWED_VALUE_FIELDS}
    for spec in specs:
        field, separator, pair = spec.partition("=")
        alias, mapping_separator, canonical = pair.partition(":")
        field = field.strip()
        alias = alias.strip()
        canonical = canonical.strip()
        if (
            not separator
            or not mapping_separator
            or field not in mappings
            or not alias
            or canonical not in ALLOWED_VALUE_FIELDS[field]
        ):
            choices = ", ".join(sorted(mappings))
            raise ValueError(
                "invalid --map-value; expected FIELD=ALIAS:CANONICAL where FIELD is one of "
                f"{choices} and CANONICAL is a default value for that field"
            )
        allowed[field].add(alias)
        mappings[field][alias] = canonical
    return mappings


def canonical_value(field: str, value: str, mappings: dict[str, dict[str, str]]) -> str | None:
    if value in ALLOWED_VALUE_FIELDS[field]:
        return value
    return mappings[field].get(value)


def audit(
    root: Path,
    *,
    literature_root: Path = Path("shared/literature"),
    experiments_root: Path = Path("shared/experiments"),
    projects_root: Path = Path("projects"),
    reference_dir: Path = Path("参考文献"),
    allowed_values: dict[str, set[str]] | None = None,
    value_mappings: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    literature = layout_path(root, literature_root)
    experiments = layout_path(root, experiments_root)
    projects = layout_path(root, projects_root)
    reference_dir = layout_path(root, reference_dir, base=literature)
    allowed = allowed_values or parse_allowed_values([])
    mappings: dict[str, dict[str, str]] = value_mappings or {
        field: {} for field in ALLOWED_VALUE_FIELDS
    }
    metadata = literature / "metadata"
    source_index = metadata / "SOURCE_INDEX.tsv"
    intake = metadata / "PDF_INTAKE.tsv"
    aliases = metadata / "SOURCE_ALIASES.tsv"
    registry_tsv = experiments / "RESULTS_REGISTRY.tsv"
    registry_md = experiments / "RESULTS_REGISTRY.md"
    issues: list[dict[str, str]] = []
    coverage = {
        "checked": [],
        "not_checked": [
            "scientific interpretation and causal validity",
            "numerical recomputation from raw artifacts",
            "citation relevance and exact source support beyond claim-note structure",
            "manuscript/portal visual and semantic consistency",
        ],
        "human_review_required": [
            "claim wording versus exact source text",
            "protocol comparability and promotion judgment",
            "whether project roles/tags remain scientifically useful",
        ],
        "skipped": [],
    }

    required = [
        literature / "AGENTS.md", literature / "README.md", literature / "HANDOFF.md",
        literature / "WIKI.md", literature / "LIBRARY_SKILL_INTERFACE.md",
        reference_dir / "CATALOG.md", intake, source_index, aliases,
        experiments / "README.md", experiments / "HANDOFF.md", experiments / "QUERY_MAP.md",
        registry_tsv, registry_md,
    ]
    project_roots: list[Path] = []
    project_literature_dirs: list[Path] = []
    if projects.exists():
        for candidate in sorted(projects.glob("*")):
            if not candidate.is_dir() and not candidate.is_symlink():
                continue
            if candidate.is_symlink() and not candidate.exists():
                issue(
                    issues,
                    "error",
                    "broken_project_root_link",
                    str(candidate.relative_to(root)),
                )
                continue
            if not candidate.is_dir():
                continue
            if not path_is_within(candidate, root):
                issue(
                    issues,
                    "error",
                    "unsafe_project_root_target",
                    str(candidate.relative_to(root)),
                )
                continue
            project_roots.append(candidate)
            literature_candidate = candidate / "literature"
            if literature_candidate.is_symlink() and not literature_candidate.exists():
                issue(
                    issues,
                    "error",
                    "broken_project_literature_link",
                    str(literature_candidate.relative_to(root)),
                )
            elif not literature_candidate.is_dir():
                issue(
                    issues,
                    "error",
                    "missing_project_literature_interface",
                    str(literature_candidate.relative_to(root)),
                )
            elif not path_is_within(literature_candidate, root):
                issue(
                    issues,
                    "error",
                    "unsafe_project_literature_target",
                    str(literature_candidate.relative_to(root)),
                )
            else:
                project_literature_dirs.append(literature_candidate)
    for directory in project_literature_dirs:
        required.extend([directory / "README.md", directory / "SOURCES.tsv", directory / "LITERATURE_CLAIMS.tsv", directory / "INDEX.md", directory / "QUERY_MAP.md", directory / "notes"])
    unsafe_required: set[Path] = set()
    for path in required:
        if path.is_symlink() and not path.exists():
            issue(issues, "error", "broken_required_entry_link", str(path.relative_to(root)))
            unsafe_required.add(path)
        elif not path.exists():
            issue(issues, "error", "missing_required_entry", str(path.relative_to(root)))
        elif not path_is_within(path, root):
            issue(issues, "error", "unsafe_required_entry_target", str(path.relative_to(root)))
            unsafe_required.add(path)
        else:
            coverage["checked"].append(str(path.relative_to(root)))

    actual_pdfs: set[str] = set()
    if reference_dir.exists():
        for path in reference_dir.rglob("*.pdf"):
            if path.is_symlink() and not path_is_within(path, reference_dir):
                issue(
                    issues,
                    "error",
                    "unsafe_pdf_inventory_target",
                    str(path.relative_to(root)),
                )
            elif path.is_file():
                actual_pdfs.add(path.relative_to(reference_dir).as_posix())
    catalog = reference_dir / "CATALOG.md"
    catalog_pdfs: set[str] = set()
    for link_number, raw in enumerate(
        markdown_local_links(catalog) if catalog not in unsafe_required else [],
        start=1,
    ):
        value = raw.strip().strip("<>")
        if not value or value.startswith("#") or SCHEME_RE.match(value):
            continue
        target = unquote(urlparse(value).path)
        if target.lower().endswith(".pdf"):
            target_path = resolve_path(
                reference_dir,
                root,
                target,
                allowed_root=reference_dir,
                allow_absolute=False,
            )
            if target_path is None:
                issue(
                    issues,
                    "error",
                    "unsafe_catalog_pdf_path",
                    f"link {link_number}",
                )
            else:
                catalog_pdfs.add(
                    target_path.resolve(strict=False)
                    .relative_to(reference_dir.resolve(strict=False))
                    .as_posix()
                )
    for value in sorted(actual_pdfs - catalog_pdfs):
        issue(issues, "error", "pdf_missing_from_catalog", value)
    for value in sorted(catalog_pdfs - actual_pdfs):
        issue(issues, "error", "catalog_target_missing", value)

    declared_counts: list[dict[str, object]] = []
    for path in (literature / "README.md", literature / "HANDOFF.md", reference_dir / "INDEX.md", catalog):
        if not path.exists() or path in unsafe_required:
            continue
        if not path_is_within(path, root):
            issue(issues, "error", "unsafe_count_source_target", str(path.relative_to(root)))
            continue
        text = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:12])
        count_values = sorted({int(match.group(1)) for pattern in COUNT_PATTERNS for match in pattern.finditer(text)})
        if count_values:
            declared_counts.append({"path": str(path.relative_to(root)), "values": count_values})
        for declared_count in count_values:
            if declared_count != len(actual_pdfs):
                issue(issues, "warning", "declared_pdf_count_drift", f"{path.relative_to(root)} declares {declared_count}; actual is {len(actual_pdfs)}")

    global_rows: list[dict[str, str]] = []
    global_sources: set[str] = set()
    if source_index.exists() and source_index not in unsafe_required:
        try:
            fields, global_rows = read_tsv(source_index)
            coverage["checked"].append("global Source-ID uniqueness/schema")
            if "source_id" not in fields:
                issue(issues, "error", "global_source_schema", "SOURCE_INDEX.tsv missing source_id")
            source_ids = [row.get("source_id", "").strip() for row in global_rows]
            global_sources = {source_id for source_id in source_ids if source_id}
            if len(source_ids) != len(global_sources):
                issue(issues, "error", "duplicate_or_empty_global_source_id", str(len(source_ids) - len(global_sources)))
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "global_source_unreadable", exception_label(exc))
            coverage["skipped"].append(str(source_index.relative_to(root)))

    intake_rows: list[dict[str, str]] = []
    if intake.exists() and intake not in unsafe_required:
        try:
            _, intake_rows = read_tsv(intake)
            intake_paths: set[str] = set()
            for number, row in enumerate(intake_rows, start=2):
                value = row.get("pdf_path", "").strip()
                intake_path = resolve_path(
                    reference_dir,
                    root,
                    value,
                    allowed_root=reference_dir,
                    allow_absolute=False,
                )
                if not value:
                    issue(issues, "error", "empty_intake_pdf_path", f"row {number}:pdf_path")
                elif intake_path is None:
                    issue(issues, "error", "unsafe_intake_pdf_path", f"row {number}:pdf_path")
                else:
                    intake_paths.add(
                        intake_path.resolve(strict=False)
                        .relative_to(reference_dir.resolve(strict=False))
                        .as_posix()
                    )
            for value in sorted(actual_pdfs - intake_paths):
                issue(issues, "error", "pdf_missing_from_intake", value)
            for value in sorted(intake_paths - actual_pdfs):
                issue(issues, "error", "intake_pdf_missing", value)
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "intake_unreadable", exception_label(exc))
            coverage["skipped"].append(str(intake.relative_to(root)))

    alias_count = 0
    if aliases.exists() and aliases not in unsafe_required:
        try:
            fields, rows = read_tsv(aliases)
            missing = [field for field in ALIAS_FIELDS if field not in fields]
            if missing:
                issue(issues, "error", "alias_schema", ",".join(missing))
            seen_aliases: set[str] = set()
            for number, row in enumerate(rows, start=2):
                alias = row.get("alias_source_id", "").strip()
                canonical = row.get("canonical_source_id", "").strip()
                relation = row.get("relation", "").strip()
                if not alias or alias in seen_aliases:
                    issue(issues, "error", "duplicate_or_empty_alias", f"row {number}:{alias}")
                seen_aliases.add(alias)
                if alias == canonical or canonical not in global_sources:
                    issue(issues, "error", "invalid_alias_target", f"row {number}:{alias}->{canonical}")
                if relation not in allowed["alias_relation"]:
                    issue(issues, "error", "invalid_alias_relation", f"row {number}:{relation}")
                if not row.get("verification_source", "").strip() or not row.get("verified_at", "").strip():
                    issue(issues, "warning", "alias_missing_provenance", f"row {number}:{alias}")
            alias_count = len(rows)
            coverage["checked"].append("global source aliases")
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "alias_registry_unreadable", exception_label(exc))
            coverage["skipped"].append(str(aliases.relative_to(root)))

    project_source_counts: dict[str, int] = {}
    project_claim_counts: dict[str, int] = {}
    for directory in project_literature_dirs:
        project = directory.parent.name
        sources_path = directory / "SOURCES.tsv"
        claims_path = directory / "LITERATURE_CLAIMS.tsv"
        if not sources_path.exists() or sources_path in unsafe_required:
            continue
        try:
            fields, rows = read_tsv(sources_path)
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "project_sources_unreadable", f"{project}:{exception_label(exc)}")
            coverage["skipped"].append(str(sources_path.relative_to(root)))
            continue
        legacy_depth = "reading_depth" not in fields and "reading_status" in fields
        missing = [field for field in SOURCE_FIELDS if field != "reading_depth" and field not in fields]
        if not legacy_depth and "reading_depth" not in fields:
            missing.append("reading_depth")
        if missing:
            issue(issues, "error", "project_source_schema", f"{project}:{','.join(missing)}")
        if legacy_depth:
            issue(issues, "warning", "legacy_reading_status", f"{project}:migrate to reading_depth")
        seen: set[str] = set()
        index_path = directory / "INDEX.md"
        index_text = (
            index_path.read_text(encoding="utf-8", errors="replace")
            if index_path.exists() and index_path not in unsafe_required
            else ""
        )
        for number, row in enumerate(rows, start=2):
            source_id = row.get("source_id", "").strip()
            if not source_id or source_id in seen:
                issue(issues, "error", "duplicate_or_empty_project_source", f"{project}:row {number}:{source_id}")
            seen.add(source_id)
            if source_id not in global_sources:
                issue(issues, "error", "unknown_project_source_id", f"{project}:row {number}:{source_id}")
            tags = [value.strip() for value in row.get("tags", "").split(",") if value.strip()]
            if not tags or any(not TAG_RE.fullmatch(value) for value in tags):
                issue(issues, "error", "invalid_project_tags", f"{project}:row {number}:{row.get('tags','')}")
            if len(tags) != len(set(tags)):
                issue(issues, "warning", "duplicate_project_tag", f"{project}:row {number}:{source_id}")
            if not row.get("project_role", "").strip():
                issue(issues, "error", "missing_project_role", f"{project}:row {number}:{source_id}")
            depth = row.get("reading_depth", row.get("reading_status", "")).strip()
            if depth not in allowed["reading_depth"]:
                issue(issues, "error", "invalid_reading_depth", f"{project}:row {number}:{source_id}:{depth}")
            note = resolve_path(
                directory,
                root,
                row.get("note", ""),
                allowed_root=directory,
                allow_absolute=False,
            )
            if row.get("note", "").strip() and note is not None and not note.exists():
                issue(issues, "error", "missing_project_note", f"{project}:row {number}:note")
            if row.get("note", "").strip() and note is None:
                issue(issues, "error", "unsafe_project_note_path", f"{project}:row {number}:note")
            if not source_id_present(index_text, source_id):
                issue(issues, "error", "source_missing_from_generated_index", f"{project}:row {number}:{source_id}")
        project_source_counts[project] = len(rows)

        if claims_path.exists() and claims_path not in unsafe_required:
            try:
                claim_fields, claim_rows = read_tsv(claims_path)
                missing_claim = [field for field in CLAIM_FIELDS if field not in claim_fields]
                if missing_claim:
                    issue(issues, "error", "literature_claim_schema", f"{project}:{','.join(missing_claim)}")
                seen_claims: set[str] = set()
                for number, row in enumerate(claim_rows, start=2):
                    claim_id = row.get("literature_claim_id", "").strip()
                    source_id = row.get("source_id", "").strip()
                    status = row.get("verification_status", "").strip()
                    if not claim_id or claim_id in seen_claims:
                        issue(issues, "error", "duplicate_or_empty_literature_claim", f"{project}:row {number}:{claim_id}")
                    seen_claims.add(claim_id)
                    if source_id not in seen:
                        issue(issues, "error", "claim_source_not_in_project", f"{project}:row {number}:{source_id}")
                    if status not in allowed["claim_status"]:
                        issue(issues, "error", "invalid_claim_verification_status", f"{project}:row {number}:{status}")
                    note_value = row.get("note_path", "").strip()
                    note = resolve_path(
                        directory,
                        root,
                        note_value,
                        allowed_root=directory,
                        allow_absolute=False,
                    )
                    if not note_value:
                        issue(issues, "error", "literature_claim_note_missing", f"{project}:row {number}:note_path")
                    elif note is None:
                        issue(issues, "error", "unsafe_literature_claim_note_path", f"{project}:row {number}:note_path")
                    elif not note.exists():
                        issue(issues, "error", "literature_claim_note_missing", f"{project}:row {number}:note_path")
                    if status == "claim_verified" and not row.get("verified_at", "").strip():
                        issue(issues, "error", "verified_claim_without_date", f"{project}:row {number}:{claim_id}")
                project_claim_counts[project] = len(claim_rows)
            except (OSError, csv.Error, UnicodeError) as exc:
                issue(issues, "incomplete", "literature_claims_unreadable", f"{project}:{exception_label(exc)}")
                coverage["skipped"].append(str(claims_path.relative_to(root)))

        copied = [item.relative_to(directory).as_posix() for item in directory.rglob("*") if item.is_file() and item.suffix.lower() in {".pdf", ".bib", ".ris", ".nbib"}]
        for value in copied:
            issue(issues, "error", "global_literature_copied_into_project", f"{project}:{value}")

    experiment_counts: dict[str, int] = {}
    experiments_by_project: dict[str, set[str]] = {}
    experiment_rows_by_project: dict[str, dict[str, dict[str, str]]] = {}
    namespace_links: list[dict[str, object]] = []
    namespaces: list[Path] = []
    if experiments.exists():
        for candidate in sorted(experiments.iterdir()):
            if candidate.is_symlink() and not candidate.exists():
                issue(
                    issues,
                    "error",
                    "broken_experiment_namespace_link",
                    str(candidate.relative_to(root)),
                )
                continue
            if not candidate.is_dir():
                continue
            current = candidate / "current"
            if not current.exists() and not current.is_symlink():
                continue
            if not path_is_within(candidate, root):
                issue(
                    issues,
                    "error",
                    "unsafe_experiment_namespace_target",
                    str(candidate.relative_to(root)),
                )
                continue
            namespaces.append(candidate)
    for namespace in namespaces:
        project = namespace.name
        current = namespace / "current"
        index_path = namespace / "EXPERIMENTS.tsv"
        current_resolves = current.exists()
        current_within_workspace = current_resolves and path_is_within(current, root)
        namespace_links.append({
            "project": project,
            "path": str(current.relative_to(root)),
            "is_symlink": current.is_symlink(),
            "resolves": current_resolves,
            "within_workspace": current_within_workspace,
        })
        if current.is_symlink() and not current_resolves:
            issue(
                issues,
                "error",
                "broken_experiment_current_link",
                str(current.relative_to(root)),
            )
        elif not current_within_workspace:
            issue(
                issues,
                "error",
                "unsafe_experiment_current_target",
                str(current.relative_to(root)),
            )
        elif not current.is_dir():
            issue(
                issues,
                "error",
                "invalid_experiment_current_entry",
                str(current.relative_to(root)),
            )
        if index_path.is_symlink() and not index_path.exists():
            issue(issues, "error", "broken_experiment_index_link", str(index_path.relative_to(root)))
            continue
        if not index_path.exists():
            issue(issues, "error", "missing_experiment_machine_index", str(index_path.relative_to(root)))
            continue
        if not path_is_within(index_path, root):
            issue(issues, "error", "unsafe_experiment_index_target", str(index_path.relative_to(root)))
            continue
        try:
            fields, rows = read_tsv(index_path)
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "experiment_index_unreadable", f"{project}:{exception_label(exc)}")
            coverage["skipped"].append(str(index_path.relative_to(root)))
            continue
        missing = [field for field in EXPERIMENT_FIELDS if field not in fields]
        if missing:
            issue(issues, "error", "experiment_index_schema", f"{project}:{','.join(missing)}")
        experiment_ids = {row.get("experiment_id", "").strip() for row in rows if row.get("experiment_id", "").strip()}
        experiments_by_project[project] = experiment_ids
        experiment_rows_by_project[project] = {
            row.get("experiment_id", "").strip(): row
            for row in rows
            if row.get("experiment_id", "").strip()
        }
        if len(experiment_ids) != len(rows):
            issue(issues, "error", "duplicate_or_empty_experiment_id", project)
        for number, row in enumerate(rows, start=2):
            experiment_id = row.get("experiment_id", "").strip()
            checks = (
                ("task_stage", allowed["task_stage"]),
                ("experiment_status", allowed["experiment_status"]),
                ("evidence_status", allowed["evidence_status"]),
                ("claim_strength", allowed["claim_strength"]),
                ("direction_decision", allowed["direction_decision"]),
            )
            for field, allowed_set in checks:
                if row.get(field, "").strip() not in allowed_set:
                    issue(issues, "error", f"invalid_{field}", f"{project}:row {number}:{experiment_id}:{row.get(field,'')}")
            experiment_status = row.get("experiment_status", "").strip()
            canonical_experiment_status = canonical_value("experiment_status", experiment_status, mappings)
            evidence_status = canonical_value("evidence_status", row.get("evidence_status", "").strip(), mappings)
            claim_strength_value = row.get("claim_strength", "").strip()
            claim_strength = canonical_value("claim_strength", claim_strength_value, mappings)
            main_claim_like = claim_strength == "main_claim" or (
                claim_strength_value in allowed["claim_strength"] and claim_strength is None
            )
            card_value = row.get("card", "").strip()
            card_path = resolve_path(namespace, root, card_value)
            if card_value and card_path is None:
                issue(issues, "error", "unsafe_experiment_card_path", f"{project}:row {number}:card")
            elif not card_value or card_path is None or not card_path.exists():
                issue(issues, "error", "experiment_card_missing", f"{project}:row {number}:card")
            for field in ("raw_artifact", "protocol_anchor"):
                value = row.get(field, "").strip()
                pointer_path = resolve_path(namespace, root, value)
                if value and pointer_path is None:
                    issue(issues, "error", f"unsafe_experiment_{field}_path", f"{project}:row {number}:{field}")
                elif value and pointer_path is not None and not pointer_path.exists():
                    issue(issues, "error", f"experiment_{field}_missing", f"{project}:row {number}:{field}")
            completion_like = (
                canonical_experiment_status == "complete"
                or (
                    experiment_status in allowed["experiment_status"]
                    and canonical_experiment_status is None
                    and experiment_status not in NONCOMPLETION_EXPERIMENT_STATUSES
                )
            )
            if completion_like and (
                not row.get("raw_artifact", "").strip()
                or not row.get("protocol_anchor", "").strip()
            ):
                issue(issues, "error", "complete_experiment_incomplete_pointer", f"{project}:row {number}:{experiment_id}")
            if evidence_status == "verified" and (
                not row.get("raw_artifact", "").strip()
                or not row.get("protocol_anchor", "").strip()
                or not row.get("last_verified", "").strip()
            ):
                issue(issues, "error", "verified_experiment_incomplete_pointer", f"{project}:row {number}:{experiment_id}")
            if main_claim_like and evidence_status != "verified":
                issue(issues, "error", "main_claim_not_verified", f"{project}:row {number}:{experiment_id}")
            if main_claim_like and row.get("selection_warning", "").strip().lower() not in CLEAR_SELECTION_WARNINGS:
                issue(issues, "error", "unsafe_main_claim_selection", f"{project}:row {number}:{experiment_id}")
            replacement = row.get("replacement_id", "").strip()
            if replacement and replacement not in experiment_ids:
                issue(issues, "error", "unknown_replacement_id", f"{project}:row {number}:{replacement}")
        experiment_counts[project] = len(rows)
        coverage["checked"].append(f"{project} EXPERIMENTS five-axis state")

    for project_root in project_roots:
        project = project_root.name
        if project not in experiments_by_project:
            missing_index = experiments / project / "EXPERIMENTS.tsv"
            issue(issues, "error", "missing_project_experiment_interface", str(missing_index.relative_to(root)))

    registry_links_checked = 0
    registry_rows: list[dict[str, str]] = []
    if registry_tsv.exists() and registry_tsv not in unsafe_required:
        try:
            fields, registry_rows = read_tsv(registry_tsv)
            missing = [field for field in REGISTRY_FIELDS if field not in fields]
            if missing:
                issue(issues, "error", "result_registry_schema", ",".join(missing))
            seen_evidence: set[str] = set()
            for number, row in enumerate(registry_rows, start=2):
                evidence_id = row.get("evidence_id", "").strip()
                project = row.get("project", "").strip()
                experiment_id = row.get("experiment_id", "").strip()
                if not evidence_id or evidence_id in seen_evidence:
                    issue(issues, "error", "duplicate_or_empty_evidence_id", f"row {number}:{evidence_id}")
                seen_evidence.add(evidence_id)
                if experiment_id not in experiments_by_project.get(project, set()):
                    issue(issues, "error", "registry_experiment_not_indexed", f"row {number}:{project}:{experiment_id}")
                registry_checks = (
                    ("experiment_status", allowed["experiment_status"]),
                    ("evidence_status", allowed["evidence_status"]),
                    ("claim_strength", allowed["claim_strength"]),
                )
                for field, allowed_set in registry_checks:
                    if row.get(field, "").strip() not in allowed_set:
                        issue(issues, "error", f"invalid_registry_{field}", f"row {number}:{project}:{experiment_id}")
                project_row = experiment_rows_by_project.get(project, {}).get(experiment_id)
                if project_row is not None:
                    for field in ("experiment_status", "evidence_status", "claim_strength", "selection_warning"):
                        registry_value = row.get(field, "").strip()
                        project_value = project_row.get(field, "").strip()
                        if field in mappings:
                            registry_value = canonical_value(field, registry_value, mappings) or registry_value
                            project_value = canonical_value(field, project_value, mappings) or project_value
                        if registry_value != project_value:
                            issue(issues, "error", "registry_state_mismatch", f"row {number}:{project}:{experiment_id}:{field}")
                    pointer_pairs = (
                        ("canonical_card", "card"),
                        ("raw_result", "raw_artifact"),
                        ("protocol_anchor", "protocol_anchor"),
                    )
                    namespace = experiments / project
                    for registry_field, project_field in pointer_pairs:
                        registry_pointer = resolve_path(root, root, row.get(registry_field, ""))
                        project_pointer = resolve_path(namespace, root, project_row.get(project_field, ""))
                        if (
                            registry_pointer is None
                            or project_pointer is None
                            or registry_pointer.resolve(strict=False)
                            != project_pointer.resolve(strict=False)
                        ):
                            issue(
                                issues,
                                "error",
                                "registry_pointer_mismatch",
                                f"row {number}:{project}:{experiment_id}:{registry_field}",
                            )
                for field in ("canonical_card", "raw_result", "protocol_anchor"):
                    value = row.get(field, "").strip()
                    registry_path = resolve_path(root, root, value)
                    registry_links_checked += 1
                    if value and registry_path is None:
                        issue(issues, "error", "unsafe_registry_pointer_path", f"row {number}:{field}")
                    elif not value or registry_path is None or not registry_path.exists():
                        issue(issues, "error", "registry_pointer_missing", f"row {number}:{field}")
                registry_evidence = canonical_value("evidence_status", row.get("evidence_status", "").strip(), mappings)
                registry_claim_value = row.get("claim_strength", "").strip()
                registry_claim = canonical_value("claim_strength", registry_claim_value, mappings)
                registry_main_like = registry_claim == "main_claim" or (
                    registry_claim_value in allowed["claim_strength"] and registry_claim is None
                )
                if registry_evidence != "verified":
                    issue(issues, "error", "registry_nonverified_promotion", f"row {number}:{evidence_id}")
                if registry_main_like and row.get("selection_warning", "").strip().lower() not in CLEAR_SELECTION_WARNINGS:
                    issue(issues, "error", "unsafe_registry_main_claim_selection", f"row {number}:{evidence_id}")
                if not row.get("promotion_reason", "").strip() or not row.get("last_verified", "").strip():
                    issue(issues, "error", "registry_promotion_incomplete", f"row {number}:{evidence_id}")
            coverage["checked"].append("canonical result registry promotions and pointers")
        except (OSError, csv.Error, UnicodeError) as exc:
            issue(issues, "incomplete", "result_registry_unreadable", exception_label(exc))
            coverage["skipped"].append(str(registry_tsv.relative_to(root)))

    severities = {value: sum(item["severity"] == value for item in issues) for value in ("error", "warning", "incomplete")}
    if severities["incomplete"]:
        status = "INCOMPLETE"
    elif severities["error"]:
        status = "FAIL"
    elif severities["warning"]:
        status = "WARN"
    else:
        status = "PASS"
    return {
        "status": status,
        "root": ".",
        "path_policy": "workspace-relative; the absolute input root is intentionally omitted",
        "summary": {
            "actual_pdfs": len(actual_pdfs), "catalog_pdf_entries": len(catalog_pdfs),
            "global_source_ids": len(global_sources), "intake_rows": len(intake_rows),
            "source_aliases": alias_count,
            "metadata_bib_ready": sum(row.get("metadata_status") == "bib_ready" for row in global_rows),
            "metadata_pending": sum(row.get("metadata_status") != "bib_ready" for row in global_rows),
            "project_source_counts": project_source_counts, "project_claim_counts": project_claim_counts,
            "experiment_counts": experiment_counts, "registry_rows": len(registry_rows),
            "registry_links_checked": registry_links_checked,
            "errors": severities["error"], "warnings": severities["warning"], "incomplete": severities["incomplete"],
        },
        "declared_pdf_counts": declared_counts,
        "namespace_links": namespace_links,
        "coverage": coverage,
        "issues": issues,
    }


def render(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        f"research-library audit: status={report['status']} pdfs={summary['actual_pdfs']} "
        f"sources={summary['global_source_ids']} aliases={summary['source_aliases']} "
        f"registry={summary['registry_rows']} errors={summary['errors']} "
        f"warnings={summary['warnings']} incomplete={summary['incomplete']}"
    )
    print(f"project_sources={summary['project_source_counts']} project_claims={summary['project_claim_counts']}")
    print(f"experiments={summary['experiment_counts']}")
    for item in report["issues"]:
        print(f"[{item['severity']}] {item['code']}: {item['message']}")
    print("not_checked=" + "; ".join(report["coverage"]["not_checked"]))
    print("human_review_required=" + "; ".join(report["coverage"]["human_review_required"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--literature-root", type=Path, default=Path("shared/literature"), help="Workspace-relative literature root")
    parser.add_argument("--experiments-root", type=Path, default=Path("shared/experiments"), help="Workspace-relative experiment-library root")
    parser.add_argument("--projects-root", type=Path, default=Path("projects"), help="Workspace-relative projects root")
    parser.add_argument("--reference-dir", type=Path, default=Path("参考文献"), help="Literature-root-relative PDF inventory directory")
    parser.add_argument(
        "--allow-value",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="Extend a default vocabulary without rewriting established project states; repeat as needed",
    )
    parser.add_argument(
        "--map-value",
        action="append",
        default=[],
        metavar="FIELD=ALIAS:CANONICAL",
        help="Map a project vocabulary alias to a default semantic value; repeat as needed",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print("Workspace root is not a directory", file=sys.stderr)
        return 2
    try:
        allowed_values = parse_allowed_values(args.allow_value)
        value_mappings = parse_value_mappings(args.map_value, allowed_values)
        report = audit(
            root,
            literature_root=args.literature_root,
            experiments_root=args.experiments_root,
            projects_root=args.projects_root,
            reference_dir=args.reference_dir,
            allowed_values=allowed_values,
            value_mappings=value_mappings,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Audit incomplete: {exception_label(exc)}", file=sys.stderr)
        return 2
    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        render(report)
    if report["status"] == "INCOMPLETE":
        return 2
    if report["status"] == "FAIL" or (args.strict and report["status"] == "WARN"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
