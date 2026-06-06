"""Shared resolution of news references to output URLs.

A meeting's `announcement`/`report` may reference a news item by its filename
stem or by an explicit `slug`. The published page is named after the item's
`slug` (or stem), so links survive a file being renamed or slugged.
"""

from pathlib import Path
from typing import Dict, Tuple

import frontmatter


def build_news_index(news_dir: Path) -> Dict[str, str]:
    """Map every news reference (filename stem and `slug`) to its output id."""
    mapping: Dict[str, str] = {}
    if news_dir.exists():
        for f in news_dir.glob('*.md'):
            slug = frontmatter.load(f).metadata.get('slug')
            out_id = slug or f.stem
            mapping[f.stem] = out_id
            if slug:
                mapping[slug] = out_id
    return mapping


def resolve_news_html(index: Dict[str, str], ref: str) -> Tuple[str, bool]:
    """Resolve a reference to (html_filename, exists) using a prebuilt index.

    No ref means the link is genuinely absent (e.g. report not written yet) ->
    (no link, False). A ref that is present but doesn't resolve is a typo or a
    deleted file -> raise rather than silently dropping the link.
    """
    if not ref:
        return '', False
    key = str(ref).rsplit('.', 1)[0]  # tolerate .md/.html suffixes
    if key not in index:
        raise ValueError(f"Unresolved news reference: {ref!r}")
    return f'{index[key]}.html', True
