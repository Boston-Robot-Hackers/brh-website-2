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

    dark_block = re.search(
        r"@media \(prefers-color-scheme: dark\).*?:root\s*\{(.*?)\}", css, re.DOTALL
    )
    assert dark_block, "expected a prefers-color-scheme: dark :root override"

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
