#!/usr/bin/env python3
# test_page_intros — Home mission text and "Next" line, page intros, default banners
# Author: Pito Salas and Claude Code
# Version: 3
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
import pytest
from content_manager import ContentManager

from build import WebsiteBuilder

INTRO_MARKER = 'class="panel page-intro"'
PROJECTS_INTRO = "Get in touch with us if you would like your project highlighted"
DEFAULT_BANNER_PAGES = [
    "about",
    "learn",
    "meetings",
    "members",
    "projects",
    "whatsnew",
]


@pytest.fixture(scope="module")
def built_site(tmp_path_factory):
    """Runs the real build() into a temp directory, so the real output/ survives."""
    builder = WebsiteBuilder()
    builder.dist_dir = tmp_path_factory.mktemp("output")
    builder.asset_manager.dist_dir = builder.dist_dir
    builder.page_builder.dist_dir = builder.dist_dir
    builder.build()
    return builder


def page_html(built_site, page):
    return (built_site.dist_dir / f"{page}.html").read_text()


def test_home_shows_mission_then_rule_then_next_meetings(built_site):
    html = page_html(built_site, "index")
    after_body_start = html.split('class="home-lead__body">')[1]
    body = after_body_start.split('class="home-lead__byline"')[0]
    mission_at = body.index("Boston Robot Hackers is a community-driven")
    rule_at = body.index("<hr/>")
    next_line = body[rule_at:]
    assert mission_at < rule_at
    assert "<strong>" in next_line or "No upcoming meetings scheduled" in next_line


def test_next_line_shows_at_most_two_meetings_with_labels(built_site):
    meetings = built_site.content_manager.get_future_meetings()
    line = built_site.content_manager.format_future_meetings_section(meetings)
    assert line.count("<strong>") == min(len(meetings), 2)


def test_missing_home_text_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        ContentManager(tmp_path).process_single_content_file("home.md")


def test_projects_shows_its_intro(built_site):
    html = page_html(built_site, "projects")
    assert INTRO_MARKER in html
    assert PROJECTS_INTRO in html


@pytest.mark.parametrize(
    "page",
    ["about", "learn", "meetings", "members", "whatsnew", "speaker-tips", "index"],
)
def test_other_pages_have_no_intro_section(built_site, page):
    assert INTRO_MARKER not in page_html(built_site, page)


@pytest.mark.parametrize("page", DEFAULT_BANNER_PAGES)
def test_main_pages_use_the_default_banner(built_site, page):
    image = built_site.site_config["default_banner_image"]
    assert f"url('{image}')" in page_html(built_site, page)


def test_pupper_detail_page_keeps_its_banner_override(built_site):
    html = (built_site.dist_dir / "projects" / "pupper.html").read_text()
    assert "pupper_standing.jpg" in html
