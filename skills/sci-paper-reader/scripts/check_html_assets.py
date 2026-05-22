#!/usr/bin/env python3
"""Check local visual assets referenced by a paper deep-read HTML file."""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ASSET_ATTRS = {"src", "href", "poster"}
LOCAL_IMAGE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".avif",
}


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ASSET_ATTRS and value:
                self.refs.append(value)


def is_local_asset(ref: str) -> bool:
    if ref.startswith("#") or ref.startswith("data:"):
        return False
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https", "mailto"}:
        return False
    suffix = Path(parsed.path).suffix.lower()
    return suffix in LOCAL_IMAGE_SUFFIXES


def resolve_ref(html_path: Path, ref: str) -> Path:
    parsed = urlparse(ref)
    raw_path = unquote(parsed.path)
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (html_path.parent / candidate).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate local image assets referenced by a paper deep-read HTML file."
    )
    parser.add_argument("html", type=Path, help="HTML file to inspect")
    args = parser.parse_args()

    html_path = args.html.expanduser().resolve()
    if not html_path.exists():
        print(f"[error] HTML file does not exist: {html_path}", file=sys.stderr)
        return 2

    parser_obj = AssetParser()
    parser_obj.feed(html_path.read_text(encoding="utf-8"))

    missing: list[Path] = []
    empty: list[Path] = []
    checked: list[Path] = []

    for ref in parser_obj.refs:
        if not is_local_asset(ref):
            continue
        path = resolve_ref(html_path, ref)
        checked.append(path)
        if not path.exists():
            missing.append(path)
        elif path.stat().st_size == 0:
            empty.append(path)

    if missing or empty:
        if missing:
            print("[missing]")
            for path in missing:
                print(path)
        if empty:
            print("[empty]")
            for path in empty:
                print(path)
        print(f"[summary] checked={len(checked)} missing={len(missing)} empty={len(empty)}")
        return 1

    print(f"[ok] checked={len(checked)} local visual assets; all exist and are non-empty.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
