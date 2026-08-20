from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def _real_news_file_count() -> int:
    return len(
        [
            f
            for f in (REPO_ROOT / "content" / "news").glob("*.md")
            if not f.stem.startswith("_")
        ]
    )


@pytest.fixture(scope="module")
def built_pages():
    builder = WebsiteBuilder()
    builder.build_news_page()
    whatsnew_html = (builder.dist_dir / "whatsnew.html").read_text()

    first_detail_file = min((builder.dist_dir / "news").glob("*.html"))
    detail_html = first_detail_file.read_text()
    return whatsnew_html, detail_html


def test_every_news_entry_present(built_pages):
    whatsnew_html, _ = built_pages
    expected = _real_news_file_count()
    assert expected > 0

    actual = whatsnew_html.count('class="story-row"')
    assert actual == expected, (
        f"expected {expected} news entries in built whatsnew.html, found {actual}"
    )


def test_news_detail_page_renders_full_content(built_pages):
    _, detail_html = built_pages
    assert 'class="detail-header__title"' in detail_html
    assert 'class="content"' in detail_html
    assert "Back to What" in detail_html
