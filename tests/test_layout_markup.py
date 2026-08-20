import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LAYOUT_FILES = [
    "templates/layouts/home.html",
    "templates/layouts/page.html",
    "templates/layouts/detail.html",
]


def test_layouts_have_no_stray_leading_plus():
    """Regression test: home.html, page.html, and detail.html each had a
    literal leading "+" character (a leftover bad-patch artifact) sitting
    right before their content <div>, rendering as visible text on every
    built page. Guards against reintroducing it."""
    for rel_path in LAYOUT_FILES:
        text = (REPO_ROOT / rel_path).read_text()
        stray_plus_lines = [
            line for line in text.splitlines() if re.match(r"^\s*\+\s*<", line)
        ]
        assert not stray_plus_lines, (
            f"{rel_path} has a stray '+' before markup: {stray_plus_lines}"
        )


def test_home_overrides_banner_block_empty():
    home_html = (REPO_ROOT / "templates" / "layouts" / "home.html").read_text()
    assert "{% block banner %}{% endblock %}" in home_html


def test_page_layout_does_not_override_banner_block():
    page_html = (REPO_ROOT / "templates" / "layouts" / "page.html").read_text()
    assert "{% block banner %}" not in page_html


def test_base_layout_defines_overridable_banner_block():
    base_html = (REPO_ROOT / "templates" / "layouts" / "base.html").read_text()
    assert (
        "{% block banner %}{% include 'components/banner.html' %}{% endblock %}"
        in base_html
    )
