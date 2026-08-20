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

    # "1-first-meeting.md" sorts first and has no markdown headings — also
    # the real no-ToC case exercised below.
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
    assert 'class="detail-brief-header__title"' in detail_html
    assert 'class="detail-brief-body"' in detail_html
    assert "Back to What" in detail_html


def test_news_detail_page_without_headings_has_no_sidebar(built_pages):
    _, detail_html = built_pages
    assert "detail-brief-sidebar" not in detail_html


class TestNewsDetailTableOfContents:
    @staticmethod
    @pytest.fixture(scope="class")
    def pupper_detail_html():
        builder = WebsiteBuilder()
        builder.build_news_page()
        pupper_file = (
            builder.dist_dir / "news" / "24-ankush-dhawan-talk-announcement.html"
        )
        return pupper_file.read_text()

    def test_toc_lists_real_top_level_headings(self, pupper_detail_html):
        assert '<a href="#meeting-announcement">Meeting Announcement</a>' in (
            pupper_detail_html
        )
        assert '<a href="#agenda">Agenda</a>' in pupper_detail_html
        assert '<a href="#featured-talk">Featured Talk</a>' in pupper_detail_html

    def test_toc_omits_nested_subheadings(self, pupper_detail_html):
        assert "Speaker: Ankush Dhawan</a>" not in pupper_detail_html

    def test_reading_time_shown(self, pupper_detail_html):
        assert "min read" in pupper_detail_html
