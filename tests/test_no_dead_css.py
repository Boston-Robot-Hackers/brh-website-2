#!/usr/bin/env python3
# test_no_dead_css — Fails on unused CSS classes or variables and Bootstrap leftovers
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_FILES = ["base.css", "layout.css", "components.css", "pages.css"]
USAGE_GLOBS = [
    "templates/**/*.html",
    "build/*.py",
    "scripts/*.js",
    "content/**/*.md",
]
ALLOWED_IMPORTANT = {"float: none !important;", "margin: 1rem auto !important;"}


def css_without_comments():
    combined = "".join((REPO_ROOT / "css" / name).read_text() for name in CSS_FILES)
    without_comments = re.sub(r"/\*.*?\*/", "", combined, flags=re.DOTALL)
    return re.sub(r"@import[^;]*;", "", without_comments)


def usage_tokens():
    tokens = set()
    for pattern in USAGE_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            tokens.update(re.findall(r"[A-Za-z_][\w-]*", path.read_text()))
    return tokens


def test_every_css_class_is_used():
    selectors = re.findall(r"([^{}]+)\{", css_without_comments())
    defined = set()
    for selector in selectors:
        defined.update(re.findall(r"\.([A-Za-z_][\w-]*)", selector))
    unused = defined - usage_tokens()
    assert not unused, f"CSS classes that nothing uses: {sorted(unused)}"


def test_every_css_variable_is_read():
    css = css_without_comments()
    defined = set(re.findall(r"(--[\w-]+)\s*:", css))
    unread = defined - set(re.findall(r"var\((--[\w-]+)", css))
    assert not unread, f"CSS variables that nothing reads: {sorted(unread)}"


def test_only_article_images_use_important():
    declarations = re.findall(r"[\w-]+:[^;{}]*!important;", css_without_comments())
    assert set(declarations) == ALLOWED_IMPORTANT


def test_bootstrap_theme_attribute_is_gone():
    old_attribute = "data-" + "bs-theme"
    for pattern in ["css/*.css", "templates/**/*.html", "scripts/*.js", "tests/*.py"]:
        for path in REPO_ROOT.glob(pattern):
            assert old_attribute not in path.read_text(), path


@pytest.mark.parametrize("page", ["member-detail", "news-detail", "project-detail"])
def test_detail_pages_share_one_title_style(page):
    assert ".detail-title" in css_without_comments()
    template = REPO_ROOT / "templates" / "details" / f"{page}.html"
    assert 'class="detail-title"' in template.read_text()


def test_script_keeps_only_the_theme_toggle():
    script = (REPO_ROOT / "scripts" / "script.js").read_text()
    assert "theme-toggle" in script
    assert "scrollIntoView" not in script


def test_unused_template_inputs_are_gone():
    assert "image_classes" not in (REPO_ROOT / "build" / "page_builder.py").read_text()
    base = (REPO_ROOT / "templates" / "layouts" / "base.html").read_text()
    assert "extra_head" not in base
