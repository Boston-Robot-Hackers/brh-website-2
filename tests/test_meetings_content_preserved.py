from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def _real_meeting_file_count() -> int:
    return len(
        [
            f
            for f in (REPO_ROOT / "content" / "meetings").glob("*.md")
            if not f.stem.startswith("_")
        ]
    )


@pytest.fixture(scope="module")
def built_pages():
    builder = WebsiteBuilder()
    builder.build_meetings_page()
    meetings_html = (builder.dist_dir / "meetings.html").read_text()

    first_detail_file = min((builder.dist_dir / "meetings").glob("*.html"))
    detail_html = first_detail_file.read_text()
    return meetings_html, detail_html


def test_every_meeting_entry_present(built_pages):
    meetings_html, _ = built_pages
    expected = _real_meeting_file_count()
    assert expected > 0

    actual = meetings_html.count('class="meeting-entry meeting-entry--clickable"')
    assert actual == expected, (
        f"expected {expected} meeting entries in built meetings.html, found {actual}"
    )


def test_meeting_detail_page_renders_full_content(built_pages):
    _, detail_html = built_pages
    assert 'class="detail-header__title"' in detail_html
    assert 'class="content"' in detail_html
    assert "Back to Meetings" in detail_html


def test_meeting_detail_shows_blurb_not_broken_thumb(built_pages):
    """Regression test: no content/meetings/*.md sets `image`, so every
    meeting detail page hit the image-less fallback, which crammed the
    full text blurb (meant as a short label elsewhere) into a fixed
    140x140px thumbnail box - visibly overflowing. Fixed by dropping the
    thumb for meetings and showing the blurb as a normal excerpt instead."""
    _, detail_html = built_pages
    assert 'class="detail-header-thumb"' not in detail_html
    assert 'class="detail-header__excerpt"' in detail_html
