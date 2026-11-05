#!/usr/bin/env python3
# test_rosbot_section — Tests for the Build-A-ROSBot section builder
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
import pytest
from content_manager import ContentManager
from rosbot_builder import RESOURCES_OUT, SESSIONS_OUT, RosbotSection

from build import WebsiteBuilder


def write_page(path, frontmatter_lines, body="Body text."):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(frontmatter_lines) + f"\n---\n{body}\n")


def make_section(content_dir, out_dir):
    builder = WebsiteBuilder()
    builder.page_builder.dist_dir = out_dir
    out_dir.mkdir(exist_ok=True)
    content_manager = ContentManager(content_dir, builder.jinja_env)
    return RosbotSection(content_manager, builder.page_builder)


@pytest.fixture
def rosbot_dir(tmp_content_dir):
    section = tmp_content_dir / "rosbot"
    write_page(section / "overview.md", ["title: ROSBot Program"], "Welcome, builders.")
    write_page(section / "sessions" / "b.md", ["title: Wheels", "session: 2"])
    write_page(
        section / "sessions" / "a.md",
        ["title: Kickoff", "session: 1", "summary: Meet the kit."],
    )
    write_page(section / "sessions" / "c.md", ["title: Lidar", "session: 3"])
    write_page(section / "sessions" / "_template.md", ["title: Template", "session: 9"])
    write_page(section / "resources" / "zeta.md", ["title: Zeta Guide"])
    write_page(section / "resources" / "alpha.md", ["title: Alpha Notes"])
    write_page(section / "resources" / "parts.md", ["title: Parts", "order: 1"])
    return section


@pytest.fixture
def section(tmp_content_dir, rosbot_dir, tmp_path):
    return make_section(tmp_content_dir, tmp_path / "out")


class TestLoading:
    def test_sessions_sorted_by_number_not_filename(self, section):
        titles = [page["title"] for page in section.load_sessions()]
        assert titles == ["Kickoff", "Wheels", "Lidar"]

    def test_underscore_template_skipped(self, section):
        titles = [page["title"] for page in section.load_sessions()]
        assert "Template" not in titles

    def test_resources_ordered_first_then_by_title(self, section):
        titles = [page["title"] for page in section.load_resources()]
        assert titles == ["Parts", "Alpha Notes", "Zeta Guide"]

    def test_missing_title_raises(self, section, rosbot_dir):
        write_page(rosbot_dir / "sessions" / "untitled.md", ["session: 4"])
        with pytest.raises(ValueError, match="untitled.md"):
            section.load_sessions()

    def test_missing_session_number_raises(self, section, rosbot_dir):
        write_page(rosbot_dir / "sessions" / "nonum.md", ["title: No Number"])
        with pytest.raises(ValueError, match="nonum.md.*'session'"):
            section.load_sessions()

    def test_non_integer_session_raises(self, section, rosbot_dir):
        write_page(rosbot_dir / "sessions" / "word.md", ["title: W", "session: two"])
        with pytest.raises(ValueError, match="word.md"):
            section.load_sessions()

    def test_duplicate_session_number_raises(self, section, rosbot_dir):
        write_page(rosbot_dir / "sessions" / "dup.md", ["title: Dup", "session: 2"])
        with pytest.raises(ValueError, match="session 2 is already used"):
            section.load_sessions()

    def test_non_integer_order_raises(self, section, rosbot_dir):
        write_page(rosbot_dir / "resources" / "bad.md", ["title: Bad", "order: first"])
        with pytest.raises(ValueError, match="bad.md.*'order'"):
            section.load_resources()


class TestBuild:
    @pytest.fixture
    def built(self, section):
        section.build()
        return section.page_builder.dist_dir

    def test_overview_lists_sessions_in_order(self, built):
        html = (built / "rosbot.html").read_text()
        assert "Welcome, builders." in html
        kickoff = html.index("Session 1: Kickoff")
        assert (
            kickoff < html.index("Session 2: Wheels") < html.index("Session 3: Lidar")
        )
        assert 'href="rosbot-sessions/a.html"' in html
        assert "Meet the kit." in html

    def test_overview_lists_resources(self, built):
        html = (built / "rosbot.html").read_text()
        for slug in ["parts", "alpha", "zeta"]:
            assert f'href="rosbot-resources/{slug}.html"' in html

    def test_every_page_written(self, built):
        for slug in ["a", "b", "c"]:
            assert (built / SESSIONS_OUT / f"{slug}.html").exists()
        for slug in ["parts", "alpha", "zeta"]:
            assert (built / RESOURCES_OUT / f"{slug}.html").exists()
        assert not (built / SESSIONS_OUT / "_template.html").exists()

    def test_first_session_has_only_next_link(self, built):
        html = (built / SESSIONS_OUT / "a.html").read_text()
        pager = html.split('class="rosbot-pager"', 1)[1].split("</nav>", 1)[0]
        assert 'href="b.html"' in pager
        assert "&larr;" not in pager

    def test_middle_session_links_both_ways(self, built):
        html = (built / SESSIONS_OUT / "b.html").read_text()
        assert 'href="a.html"' in html
        assert 'href="c.html"' in html

    def test_last_session_has_only_previous_link(self, built):
        html = (built / SESSIONS_OUT / "c.html").read_text()
        pager = html.split('class="rosbot-pager"', 1)[1].split("</nav>", 1)[0]
        assert 'href="b.html"' in pager
        assert "&rarr;" not in pager

    def test_nav_link_active_with_right_prefix(self, built):
        overview = (built / "rosbot.html").read_text()
        session = (built / SESSIONS_OUT / "a.html").read_text()
        resource = (built / RESOURCES_OUT / "parts.html").read_text()
        assert 'href="rosbot.html"' in overview
        assert "site-nav__featured-link active" in overview
        for html in [session, resource]:
            assert 'href="../rosbot.html"' in html
            assert "site-nav__featured-link active" in html
            assert "Back to Build-A-ROSBot" in html

    def test_nav_link_not_active_elsewhere(self, section):
        html = section.page_builder.build_page(
            "pages/content-page.html", "x.html", page_title="X", page_content=""
        ).read_text()
        assert "site-nav__featured-link active" not in html


class TestRealContent:
    def test_real_section_builds(self, tmp_path):
        builder = WebsiteBuilder()
        section = make_section(builder.content_dir, tmp_path / "out")
        section.build()
        out = tmp_path / "out"
        assert "Build-A-ROSBot" in (out / "rosbot.html").read_text()
        assert list((out / SESSIONS_OUT).glob("*.html"))
        assert list((out / RESOURCES_OUT).glob("*.html"))
        assert not (out / SESSIONS_OUT / "_template.html").exists()
        assert not (out / RESOURCES_OUT / "_template.html").exists()
