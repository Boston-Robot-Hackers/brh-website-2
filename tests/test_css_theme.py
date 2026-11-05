#!/usr/bin/env python3
# test_css_theme — Tests that CSS colors go through theme variables in both modes
# Author: Pito Salas and Claude Code
# Version: 6
# Created: 2026-09-21
# Updated: 2026-11-05
# Open Source Under MIT license
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = REPO_ROOT / "css"
STYLESHEET_ORDER = ["base.css", "layout.css", "components.css", "pages.css"]

# Variables that must have a dark-mode counterpart (the neutral scale +
# shadows). Brand/accent colors (--primary, --accent, --success,
# etc.) are deliberately unchanged across modes - see F01's audit.
DARK_MODE_VARS = {
    "--bg",
    "--bg-card",
    "--border",
    "--border-hover",
    "--text",
    "--text-muted",
    "--emphasis",
    "--shadow-sm",
    "--shadow-lg",
}

# Colors intentionally left hardcoded outside base.css: the banner's fallback
# background, and white behind the QR code and meeting date boxes. They
# look the same in both themes, so they don't need a variable.
BESPOKE_CHROME_HEX = {"#1a1a1a", "#ffffff"}


def base_css():
    return (CSS_DIR / "base.css").read_text()


def test_dark_mode_defines_every_required_variable():
    dark_block = re.search(
        r':root\[data-theme="dark"\]\s*\{(.*?)\}', base_css(), re.DOTALL
    )
    assert dark_block, 'expected a :root[data-theme="dark"] override'

    dark_vars = set(re.findall(r"(--[\w-]+)\s*:", dark_block.group(1)))
    missing = DARK_MODE_VARS - dark_vars
    assert not missing, f"dark mode is missing variables: {missing}"


@pytest.mark.parametrize("name", STYLESHEET_ORDER[1:])
def test_only_base_css_hardcodes_colors(name):
    css = (CSS_DIR / name).read_text()
    hex_colors = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{3,6}", css)}
    unexpected = hex_colors - {c.lower() for c in BESPOKE_CHROME_HEX}

    assert not unexpected, f"unexpected hardcoded hex colors in {name}: {unexpected}"


def test_base_template_sets_theme_before_paint():
    base_html = (REPO_ROOT / "templates" / "layouts" / "base.html").read_text()

    assert "data-theme" in base_html
    assert "prefers-color-scheme: dark" in base_html


def test_base_css_uses_option_d_palette_and_type():
    """Locks in F05/TF05.1's re-theme: Option D's red-on-cream palette and
    Archivo Narrow, in both the light and dark `:root` blocks."""
    css = base_css()

    assert "Archivo+Narrow" in css, "expected the Archivo Narrow Google Fonts import"
    assert "Archivo Narrow" in css, "expected Archivo Narrow used as a font-family"

    light_block = re.search(r":root\s*\{(.*?)\n\}", css, re.DOTALL)
    assert light_block, "expected a light :root block"
    assert "#fffef7" in light_block.group(1), "expected the cream --bg value"
    assert "#d00029" in light_block.group(1), "expected the red --primary value"

    dark_block = re.search(r':root\[data-theme="dark"\]\s*\{(.*?)\}', css, re.DOTALL)
    assert dark_block, 'expected a :root[data-theme="dark"] override'
    assert "#121110" in dark_block.group(1), (
        "expected the warm near-black dark --bg value"
    )
    assert "--primary" in dark_block.group(1), (
        "dark mode must redefine --primary too (unlike neutrals-only F01 precedent) "
        "since red is used as running text/link color, not just isolated fills"
    )


def test_stylesheets_load_in_cascade_order():
    """base.css defines the variables the others use, and each later file
    can override the earlier ones."""
    head_html = (REPO_ROOT / "templates" / "components" / "head.html").read_text()
    positions = [head_html.index(f"css/{name}") for name in STYLESHEET_ORDER]

    assert positions == sorted(positions)


def test_no_bootstrap_cdn_reference():
    """F05 Phase 3: Bootstrap CSS/JS/Icons were removed entirely in favor of
    our own CSS and inline SVG icons (templates/components/icons.html)."""
    head_html = (REPO_ROOT / "templates" / "components" / "head.html").read_text()
    assert "cdn.jsdelivr.net/npm/bootstrap" not in head_html
