import json
from pathlib import Path

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent

# Layouts/components included on every page, or on listing/detail pages -
# the QR code must never appear in these, only in home-lead.html (home-only).
SHARED_TEMPLATES = [
    "templates/layouts/base.html",
    "templates/layouts/page.html",
    "templates/layouts/detail.html",
    "templates/components/hero.html",
    "templates/components/navigation.html",
]


def test_site_config_has_signup_url():
    site_config = json.loads((REPO_ROOT / "config" / "site.json").read_text())
    assert site_config.get("signup_url"), "config/site.json must set signup_url"


def test_home_lead_renders_qr_code():
    home_lead_html = (
        REPO_ROOT / "templates" / "components" / "home-lead.html"
    ).read_text()
    assert "signup-qr.png" in home_lead_html
    assert 'alt="' in home_lead_html
    assert "Join BRH" in home_lead_html


def test_shared_templates_do_not_render_qr_code():
    for rel_path in SHARED_TEMPLATES:
        text = (REPO_ROOT / rel_path).read_text()
        assert "signup-qr" not in text, f"{rel_path} must not render the signup QR code"


def test_qr_code_present_on_home_page_only():
    """Real-build check: the QR must render on index.html but not on a
    page that also goes through the shared nav (e.g. learn.html)."""
    builder = WebsiteBuilder()
    builder.build_index()
    builder.build_learn_page()

    index_html = (builder.dist_dir / "index.html").read_text()
    learn_html = (builder.dist_dir / "learn.html").read_text()

    assert "signup-qr.png" in index_html
    assert "signup-qr.png" not in learn_html
