import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Variables that must have a dark-mode counterpart (the neutral scale +
# shadows). Brand/accent colors (--primary, --secondary, --accent, --success,
# etc.) are deliberately unchanged across modes - see F01's audit.
DARK_MODE_VARS = {
    "--bg", "--bg-card", "--border", "--border-hover",
    "--text", "--text-muted", "--text-light",
    "--shadow-sm", "--shadow-md", "--shadow-lg", "--shadow-xl",
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


def test_bootstrap_css_loads_before_custom_css():
    """Regression test: Bootstrap's CSS must load before shared.css/main.css.

    Both define rules for `body`/`.card` etc. at equal specificity, so
    whichever loads last wins the cascade. Bootstrap loading second silently
    overrode our custom colors in both modes (only obviously wrong in dark
    mode, where the two competing dark grays clashed) until this was fixed.
    """
    head_html = (REPO_ROOT / "templates" / "components" / "head.html").read_text()

    bootstrap_pos = head_html.index("bootstrap.min.css")
    shared_pos = head_html.index("css/shared.css")
    main_pos = head_html.index("css/main.css")

    assert bootstrap_pos < shared_pos < main_pos, (
        "Bootstrap CSS must load before shared.css and main.css"
    )
