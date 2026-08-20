import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Variables that must have a dark-mode counterpart (the neutral scale +
# shadows). Brand/accent colors (--primary, --secondary, --accent, --success,
# etc.) are deliberately unchanged across modes - see F01's audit.
DARK_MODE_VARS = {
    "--bg",
    "--bg-card",
    "--border",
    "--border-hover",
    "--text",
    "--text-muted",
    "--text-light",
    "--shadow-sm",
    "--shadow-md",
    "--shadow-lg",
    "--shadow-xl",
}

# The 3 bespoke dark-UI-chrome colors intentionally left hardcoded in
# main.css (nav-bar gradient, banner, nav-link hover) - already dark
# regardless of page theme, so they don't need a variable.
BESPOKE_CHROME_HEX = {"#1e293b", "#334155", "#1a1a1a", "#ffffff"}


def test_dark_mode_defines_every_required_variable():
    css = (REPO_ROOT / "css" / "shared.css").read_text()

    dark_block = re.search(r':root\[data-bs-theme="dark"\]\s*\{(.*?)\}', css, re.DOTALL)
    assert dark_block, 'expected a :root[data-bs-theme="dark"] override'

    dark_vars = set(re.findall(r"(--[\w-]+)\s*:", dark_block.group(1)))
    missing = DARK_MODE_VARS - dark_vars
    assert not missing, f"dark mode is missing variables: {missing}"


def test_main_css_has_no_unexpected_hardcoded_colors():
    main_css = (REPO_ROOT / "css" / "main.css").read_text()

    hex_colors = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{3,6}", main_css)}
    unexpected = hex_colors - {c.lower() for c in BESPOKE_CHROME_HEX}

    assert not unexpected, f"unexpected hardcoded hex colors in main.css: {unexpected}"


def test_base_template_syncs_bootstrap_theme():
    base_html = (REPO_ROOT / "templates" / "layouts" / "base.html").read_text()

    assert "data-bs-theme" in base_html
    assert "prefers-color-scheme: dark" in base_html


def test_shared_css_uses_option_d_palette_and_type():
    """Locks in F05/TF05.1's re-theme: Option D's red-on-cream palette and
    Archivo Narrow, in both the light and dark `:root` blocks."""
    css = (REPO_ROOT / "css" / "shared.css").read_text()

    assert "Archivo+Narrow" in css, "expected the Archivo Narrow Google Fonts import"
    assert "Archivo Narrow" in css, "expected Archivo Narrow used as a font-family"

    light_block = re.search(r":root\{(.*?)\n\}", css, re.DOTALL)
    assert light_block, "expected a light :root block"
    assert "#fffef7" in light_block.group(1), "expected the cream --bg value"
    assert "#ff0033" in light_block.group(1), "expected the red --primary value"

    dark_block = re.search(r':root\[data-bs-theme="dark"\]\s*\{(.*?)\}', css, re.DOTALL)
    assert dark_block, 'expected a :root[data-bs-theme="dark"] override'
    assert "#121110" in dark_block.group(1), (
        "expected the warm near-black dark --bg value"
    )
    assert "--primary" in dark_block.group(1), (
        "dark mode must redefine --primary too (unlike neutrals-only F01 precedent) "
        "since red is used as running text/link color, not just isolated fills"
    )


def test_shared_css_loads_before_main_css():
    """shared.css defines the CSS variables main.css consumes; both are our
    own files now (no more Bootstrap cascade-order concern - F05 Phase 3
    removed the Bootstrap CDN entirely, see test_no_bootstrap_cdn_reference)."""
    head_html = (REPO_ROOT / "templates" / "components" / "head.html").read_text()

    shared_pos = head_html.index("css/shared.css")
    main_pos = head_html.index("css/main.css")

    assert shared_pos < main_pos, "shared.css must load before main.css"


def test_no_bootstrap_cdn_reference():
    """F05 Phase 3: Bootstrap CSS/JS/Icons were removed entirely in favor of
    our own CSS and inline SVG icons (templates/components/icons.html)."""
    head_html = (REPO_ROOT / "templates" / "components" / "head.html").read_text()
    assert "cdn.jsdelivr.net/npm/bootstrap" not in head_html
