#!/usr/bin/env python3
# test_content_pages — Tests for standalone content/pages/*.md pages linked from About
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-10-26
# Updated: 2026-10-26
# Open Source Under MIT license
import pytest
from content_manager import ContentManager

from build import WebsiteBuilder


@pytest.fixture
def fixture_builder(tmp_content_dir, tmp_path):
    """A builder reading tmp_content_dir and writing to a temp output dir."""
    builder = WebsiteBuilder()
    builder.content_manager = ContentManager(tmp_content_dir, builder.jinja_env)
    builder.page_builder.dist_dir = tmp_path / "out"
    builder.page_builder.dist_dir.mkdir()
    (tmp_content_dir / "pages").mkdir()
    return builder


class TestBuildContentPages:
    def test_renders_page_to_slug_html(self, fixture_builder, tmp_content_dir):
        (tmp_content_dir / "pages" / "guide.md").write_text(
            "---\ntitle: Visitor Guide\n---\nPark on **Holton Street**.\n"
        )
        fixture_builder.build_content_pages()
        html = (fixture_builder.page_builder.dist_dir / "guide.html").read_text()
        assert "<title>Visitor Guide - " in html
        assert "<strong>Holton Street</strong>" in html
        assert 'site-nav__link active">About' in html

    def test_missing_title_raises(self, fixture_builder, tmp_content_dir):
        (tmp_content_dir / "pages" / "untitled.md").write_text("No frontmatter.\n")
        with pytest.raises(ValueError, match="untitled.md"):
            fixture_builder.build_content_pages()


@pytest.fixture(scope="module")
def real_builder():
    builder = WebsiteBuilder()
    builder.build_about_page()
    builder.build_content_pages()
    return builder


class TestRealBuild:
    def test_about_links_to_speaker_tips(self, real_builder):
        about = (real_builder.dist_dir / "about.html").read_text()
        assert 'href="speaker-tips.html"' in about

    def test_speaker_tips_content(self, real_builder):
        tips = (real_builder.dist_dir / "speaker-tips.html").read_text()
        for phrase in ["Tips for Speakers", "Types of Talks", "Afterwards"]:
            assert phrase in tips, f"missing expected phrase: {phrase}"
