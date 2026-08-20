from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def _real_project_file_count() -> int:
    return len(
        [
            f
            for f in (REPO_ROOT / "content" / "projects").glob("*.md")
            if not f.stem.startswith("_")
        ]
    )


@pytest.fixture(scope="module")
def built_pages():
    builder = WebsiteBuilder()
    builder.build_projects_page()
    projects_html = (builder.dist_dir / "projects.html").read_text()
    pupper_html = (builder.dist_dir / "projects" / "pupper.html").read_text()
    dome_robot_html = (builder.dist_dir / "projects" / "dome-robot.html").read_text()
    midi_html = (builder.dist_dir / "projects" / "midi.html").read_text()
    return projects_html, pupper_html, dome_robot_html, midi_html


def test_every_project_entry_present(built_pages):
    projects_html, *_ = built_pages
    expected = _real_project_file_count()
    assert expected > 0

    actual = projects_html.count('class="story-row"')
    assert actual == expected, (
        f"expected {expected} project entries in built projects.html, found {actual}"
    )


def test_pupper_detail_page_renders_full_content(built_pages):
    _, pupper_html, _, _ = built_pages
    assert 'class="detail-brief-header__title"' in pupper_html
    assert "Stanford Pupper v3" in pupper_html
    assert 'class="detail-brief-body"' in pupper_html
    assert "Back to Projects" in pupper_html


def test_pupper_toc_lists_real_top_level_headings(built_pages):
    _, pupper_html, _, _ = built_pages
    assert '<a href="#overview">Overview</a>' in pupper_html
    assert '<a href="#what-is-pupper-v3">What is Pupper v3?</a>' in pupper_html
    assert '<a href="#the-boston-build-team">The Boston Build Team</a>' in pupper_html
    assert '<a href="#our-mission-in-boston">Our Mission in Boston</a>' in pupper_html
    assert (
        '<a href="#get-involved-get-in-touch">Get Involved &amp; Get in Touch</a>'
        in pupper_html
    )


def test_pupper_toc_omits_nested_subheadings(built_pages):
    _, pupper_html, _, _ = built_pages
    assert "Key Features</a>" not in pupper_html
    assert "Project Members</a>" not in pupper_html


def test_dome_robot_toc_nests_correctly_with_no_h2(built_pages):
    """dome-robot.md has only ### headings, no ##; both must still be
    top-level ToC entries since there's no shallower heading to nest
    under."""
    _, _, dome_robot_html, _ = built_pages
    assert '<a href="#software">Software</a>' in dome_robot_html
    assert '<a href="#hardware">Hardware</a>' in dome_robot_html


def test_midi_has_no_sidebar_when_headingless(built_pages):
    _, _, _, midi_html = built_pages
    assert "detail-brief-sidebar" not in midi_html
