#!/usr/bin/env python3
# test_layout_bugs — Guards the F24 fixes for phone layout, contrast and keyboard access
# Author: Pito Salas and Claude Code
# Version: 3
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
MIN_TEXT_CONTRAST = 4.5
RGB_CHANNEL_STARTS = (0, 2, 4)


def css_text(name):
    source = (REPO_ROOT / "css" / name).read_text()
    return re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)


def all_css():
    return "".join(
        css_text(name)
        for name in ["base.css", "layout.css", "components.css", "pages.css"]
    )


def media_blocks(css, max_width_px):
    """Return the bodies of every @media (max-width: N px) block in the CSS."""
    bodies = []
    for match in re.finditer(rf"@media \(max-width: {max_width_px}px\)\s*\{{", css):
        depth = 1
        end = match.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(css[end], 0)
            end += 1
        bodies.append(css[match.end() : end - 1])
    return "\n".join(bodies)


def light_variable(name):
    root = re.search(r":root\s*\{(.*?)\}", css_text("base.css"), re.DOTALL).group(1)
    return re.search(rf"{name}:\s*(#[0-9a-fA-F]{{6}})", root).group(1)


def luminance(hex_color):
    channels = [
        int(hex_color[1:][start : start + 2], 16) / 255 for start in RGB_CHANNEL_STARTS
    ]
    linear = [
        value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


@pytest.fixture(scope="module")
def home_html(tmp_path_factory):
    builder = WebsiteBuilder()
    builder.dist_dir = tmp_path_factory.mktemp("output")
    builder.page_builder.dist_dir = builder.dist_dir
    builder.build_index()
    return (builder.dist_dir / "index.html").read_text()


def test_nav_is_not_sticky_at_tablet_width_and_below():
    block = media_blocks(css_text("layout.css"), 980)
    assert re.search(r"\.site-nav\s*\{\s*position: static;", block)


def test_scroll_offset_comes_from_one_variable():
    assert set(re.findall(r"scroll-margin-top:\s*([^;]+);", all_css())) == {
        "var(--nav-offset)"
    }


def test_sticky_sidebar_clears_the_nav():
    assert re.search(
        r"\.detail-brief-sidebar\s*\{[^}]*top: var\(--nav-offset\);",
        css_text("pages.css"),
    )


def test_images_and_code_blocks_cannot_widen_the_page():
    shared = css_text("base.css")
    assert re.search(r"(^|\n)img\s*\{\s*max-width: 100%;", shared)
    assert re.search(r"(^|\n)pre\s*\{[^}]*overflow-x: auto;", shared)


def test_article_images_keep_their_shape_and_stop_floating_on_phones():
    main = css_text("pages.css")
    assert re.search(r"\.detail-brief-body img[^{]*\{\s*object-fit: contain;", main)
    assert "float: none !important" in media_blocks(main, 620)


@pytest.mark.parametrize("heading", ["h1", "h2", "h3"])
def test_heading_size_is_only_set_responsively(heading):
    sizes = re.findall(
        rf"(?:^|\n){heading}\s*\{{[^}}]*font-size:\s*([^;]+);", css_text("base.css")
    )
    assert len(sizes) == 1
    assert sizes[0].startswith("clamp(")


def test_shared_heading_rule_does_not_set_a_fixed_size():
    rule = re.search(r"h1, \.banner h1\s*\{([^}]*)\}", css_text("base.css"))
    assert "font-size" not in rule.group(1)


@pytest.mark.parametrize(
    "background", ["--bg", "--calendar-card-bg", "--primary-light"]
)
def test_primary_text_passes_contrast_in_light_mode(background):
    ratio = contrast(light_variable("--primary"), light_variable(background))
    assert ratio >= MIN_TEXT_CONTRAST


def test_feed_buttons_are_solid_with_readable_text():
    css = css_text("components.css")
    rule = re.search(r"\.rail-feeds a\s*\{([^}]*)\}", css).group(1)
    assert "color: var(--on-accent);" in rule
    assert "background-color: var(--accent);" in rule
    ratio = contrast(light_variable("--on-accent"), light_variable("--accent"))
    assert ratio >= MIN_TEXT_CONTRAST


def test_home_meeting_rows_are_real_links(home_html):
    rows = re.findall(r'<div class="rail-item">.*?</div>', home_html, re.DOTALL)
    assert rows
    links = [row for row in rows if 'class="rail-item__link" href="news/' in row]
    assert links


def test_click_handler_for_rows_is_gone(home_html):
    assert "data-href" not in home_html
    assert "meeting-row" not in home_html
    assert "data-href" not in (REPO_ROOT / "scripts" / "script.js").read_text()


def test_row_without_announcement_has_no_link():
    env = Environment(loader=FileSystemLoader(REPO_ROOT / "templates"))
    html = env.get_template("components/upcoming-meetings-calendar.html").render(
        meetings=[
            {
                "type_label": "Main Meeting",
                "month_abbr": "Jan",
                "day": 14,
                "year": 2027,
                "time": "7:00pm",
                "text": "",
                "announcement_url": "",
            }
        ]
    )
    assert "rail-item__link" not in html
    assert "Jan 14, 2027" in html
