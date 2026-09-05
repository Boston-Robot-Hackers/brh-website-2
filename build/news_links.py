#!/usr/bin/env python3
"""news_links.py — Shared resolution of news references to output URLs.

A meeting's `announcement`/`report` may reference a news item by its filename
stem or by an explicit `slug`. The published page is named after the item's
`slug` (or stem), so links survive a file being renamed or slugged.

Author: Pito Salas and Claude Code
Open Source Under MIT license
"""

from pathlib import Path

import frontmatter


def build_news_index(news_dir: Path) -> dict[str, str]:
    """Map every news reference (filename stem and `slug`) to its output id."""
    mapping: dict[str, str] = {}
    if news_dir.exists():
        for f in news_dir.glob("*.md"):
            slug = frontmatter.load(f).metadata.get("slug")
            out_id = slug or f.stem
            mapping[f.stem] = out_id
            if slug:
                mapping[slug] = out_id
    return mapping


def resolve_news_html(index: dict[str, str], ref: str) -> tuple[str, bool]:
    """Resolve a reference to (html_filename, exists) using a prebuilt index.

    No ref means the link is genuinely absent (e.g. report not written yet) ->
    (no link, False). A ref that is present but doesn't resolve is a typo or a
    deleted file -> raise rather than silently dropping the link.
    """
    if not ref:
        return "", False
    key = str(ref).rsplit(".", 1)[0]  # tolerate .md/.html suffixes
    if key not in index:
        raise ValueError(f"Unresolved news reference: {ref!r}")
    return f"{index[key]}.html", True


class NewsResolver:
    """Caches a news directory's reference index and resolves refs against it.

    Building the index means scanning every file in the news directory for its
    frontmatter, so it's built once on first use and reused for every
    subsequent `resolve()` call on this instance.
    """

    def __init__(self, news_dir: Path):
        self.news_dir = news_dir
        self.index: dict[str, str] | None = None

    def resolve(self, ref: str) -> tuple[str, bool]:
        if self.index is None:
            self.index = build_news_index(self.news_dir)
        return resolve_news_html(self.index, ref)


def extract_slides_pdf(news_dir: Path, ref: str) -> str | None:
    """Extract slides_pdf metadata from a news file reference.

    Returns the slides_pdf value if it exists and is non-empty, else None.
    Raises ValueError if ref doesn't resolve to a file.
    """
    if not ref:
        return None
    key = str(ref).rsplit(".", 1)[0]  # tolerate .md/.html suffixes
    news_file = news_dir / f"{key}.md"
    if not news_file.exists():
        raise ValueError(f"News reference file not found: {ref!r}")
    metadata = frontmatter.load(news_file).metadata
    return metadata.get("slides_pdf") or None
