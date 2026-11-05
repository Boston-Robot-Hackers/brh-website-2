#!/usr/bin/env python3
# test_css_structure — Locks in the CSS scales, shared styles and four-file split
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
import re
from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = REPO_ROOT / "css"
STYLESHEETS = ["base.css", "layout.css", "components.css", "pages.css"]
BREAKPOINTS_PX = {"620", "760", "980"}
FONT_SIZE_EXCEPTIONS = {"inherit", "1.7rem", "3rem"}
ALLOWED_RADII = {
    "var(--radius)",
    "var(--radius-lg)",
    "999px",
    "0 0 var(--radius-lg) var(--radius-lg)",
}
SHARED_RULE_TOKENS = {"1px solid var(--border)", "2px solid var(--text)"}


def css(name):
    return re.sub(r"/\*.*?\*/", "", (CSS_DIR / name).read_text(), flags=re.DOTALL)


def all_css():
    return "".join(css(name) for name in STYLESHEETS)


def rule_body(source, selector):
    """Body of the rule whose whole selector is `selector`, not a group it's in."""
    pattern = rf"(?:^|(?<!,)\n){re.escape(selector)}\s*\{{([^}}]*)\}}"
    match = re.search(pattern, source)
    assert match, f"no rule for {selector}"
    return match.group(1)


@pytest.fixture(scope="module")
def built_site(tmp_path_factory):
    builder = WebsiteBuilder()
    builder.dist_dir = tmp_path_factory.mktemp("output")
    builder.asset_manager.dist_dir = builder.dist_dir
    builder.page_builder.dist_dir = builder.dist_dir
    builder.build()
    return builder.dist_dir


def test_font_sizes_come_from_the_scale():
    sizes = set(re.findall(r"font-size:\s*([^;]+);", all_css()))
    off_scale = {
        size
        for size in sizes
        if not size.startswith(("var(--fs-", "clamp("))
        and size not in FONT_SIZE_EXCEPTIONS
    }
    assert not off_scale


def test_only_three_breakpoints():
    widths = set(re.findall(r"@media \(max-width: (\d+)px\)", all_css()))
    assert widths == BREAKPOINTS_PX


def test_text_inherits_its_color():
    assert "color" not in rule_body(css("base.css"), "p, li, blockquote")


def test_labels_share_one_style():
    label = rule_body(css("components.css"), ".label")
    assert "text-transform: uppercase" in label
    assert "font-size: var(--fs-xs)" in label
    kicker_rules = [
        ".home-lead__kicker",
        ".detail-brief-header__kicker",
        ".member-projects-label",
    ]
    for selector in kicker_rules:
        body = rule_body(all_css(), selector)
        assert "font-size" not in body
        assert "text-transform" not in body


def test_section_headings_share_one_size_and_rule():
    heading = rule_body(css("components.css"), ".section-heading,\n.about-content h2")
    assert "border-bottom: var(--rule-strong)" in heading
    assert "font-size: var(--fs-lg)" in heading
    assert "font-size" not in rule_body(css("pages.css"), ".about-content h2")


def test_borders_use_the_two_rule_tokens():
    source = all_css()
    for token in SHARED_RULE_TOKENS:
        assert source.count(token) == 1, f"{token} should appear only in base.css"


def test_corner_radii_are_limited():
    assert set(re.findall(r"border-radius:\s*([^;]+);", all_css())) == ALLOWED_RADII


def test_one_muted_grey():
    source = all_css()
    assert "--text-light" not in source
    assert "--dek" not in source


def test_buttons_share_size_and_type():
    shared = rule_body(css("components.css"), ".btn-outline,\n.btn-slides")
    assert "padding" in shared
    assert "font-size" in shared
    for selector in [".btn-outline", ".btn-slides"]:
        body = rule_body(css("components.css"), selector)
        assert "padding" not in body
        assert "font-size" not in body


@pytest.mark.parametrize(
    "selector",
    [".story-row__excerpt", ".rail-item__blurb", ".learn-card-intro", ".rail-note"],
)
def test_small_grey_text_uses_the_note_style(selector):
    body = rule_body(all_css(), selector)
    assert "color" not in body
    assert "font-size" not in body


@pytest.mark.parametrize(
    "selector", [".learn-card", ".page-intro", ".pupper-spotlight", ".card"]
)
def test_boxes_use_the_panel_style(selector):
    body = rule_body(all_css(), selector)
    assert "border:" not in body
    assert "border-radius" not in body


def test_pages_link_the_four_stylesheets_in_order(built_site):
    html = (built_site / "index.html").read_text()
    positions = [html.index(f"css/{name}") for name in STYLESHEETS]
    assert positions == sorted(positions)
    for name in STYLESHEETS:
        assert (built_site / "css" / name).exists()


def test_old_stylesheets_are_gone():
    assert not (CSS_DIR / "main.css").exists()
    assert not (CSS_DIR / "shared.css").exists()


def test_built_pages_use_the_shared_classes(built_site):
    home = (built_site / "index.html").read_text()
    projects = (built_site / "projects.html").read_text()
    assert 'class="label' in home
    assert 'class="section-heading' in home
    assert 'class="note' in home
    assert 'class="panel' in projects
