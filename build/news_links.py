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
            try:
                slug = frontmatter.load(f).metadata.get('slug')
            except Exception:
                slug = None
            out_id = slug or f.stem
            mapping[f.stem] = out_id
            if slug:
                mapping[slug] = out_id
    return mapping


def resolve_news_html(index: Dict[str, str], ref: str) -> Tuple[str, bool]:
    """Resolve a reference to (html_filename, exists) using a prebuilt index."""
    if not ref:
        return '', False
    key = str(ref).rsplit('.', 1)[0]  # tolerate .md/.html suffixes
    out_id = index.get(key)
    if out_id:
        return f'{out_id}.html', True
    return '', False
