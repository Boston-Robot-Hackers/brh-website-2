from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

NAV_TEMPLATE = REPO_ROOT / "templates" / "components" / "navigation.html"

EXPECTED_LINKS = [
    "index.html",
    "learn.html",
    "members.html",
    "projects.html",
    "about.html",
]


def test_nav_has_all_five_original_links():
    nav_html = NAV_TEMPLATE.read_text()
    for link in EXPECTED_LINKS:
        assert link in nav_html, f"expected nav to still link to {link}"


def test_pupper_link_points_at_its_existing_project_page():
    nav_html = NAV_TEMPLATE.read_text()
    assert "projects/pupper.html" in nav_html
    # Same is_detail_page-conditional relative-path pattern the other 5
    # links already use, so Pupper resolves correctly from both top-level
    # pages (projects/pupper.html) and detail pages (../projects/pupper.html).
    assert "{{ '../' if is_detail_page else '' }}projects/pupper.html" in nav_html


def test_pupper_link_uses_real_photo_badge():
    nav_html = NAV_TEMPLATE.read_text()
    assert "images/projects/pupper_standing.jpg" in nav_html


def test_theme_toggle_button_preserved():
    nav_html = NAV_TEMPLATE.read_text()
    assert 'id="theme-toggle"' in nav_html
