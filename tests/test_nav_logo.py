from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_robot_logo_asset_exists():
    assert (REPO_ROOT / "images" / "robot-logo.png").exists()


def test_nav_renders_logo_with_dark_mode_invert():
    nav_html = (REPO_ROOT / "templates" / "components" / "navigation.html").read_text()
    assert "images/robot-logo.png" in nav_html
    assert 'class="site-nav__logo"' in nav_html

    css = (REPO_ROOT / "css" / "main.css").read_text()
    assert ':root[data-bs-theme="dark"] .site-nav__logo' in css
