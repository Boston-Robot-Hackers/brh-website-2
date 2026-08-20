import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Layouts/components included on every page, or on listing/detail pages -
# the QR code must never appear in these, only in home.html (index-only).
SHARED_TEMPLATES = [
    "templates/layouts/base.html",
    "templates/layouts/page.html",
    "templates/layouts/detail.html",
    "templates/components/hero.html",
]


def test_site_config_has_signup_url():
    site_config = json.loads((REPO_ROOT / "config" / "site.json").read_text())
    assert site_config.get("signup_url"), "config/site.json must set signup_url"


def test_home_layout_renders_qr_code():
    home_html = (REPO_ROOT / "templates" / "layouts" / "home.html").read_text()
    assert "signup-qr.png" in home_html
    assert 'alt="' in home_html


def test_shared_templates_do_not_render_qr_code():
    for rel_path in SHARED_TEMPLATES:
        text = (REPO_ROOT / rel_path).read_text()
        assert "signup-qr" not in text, f"{rel_path} must not render the signup QR code"
