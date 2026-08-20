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
    return projects_html, pupper_html


def test_every_project_entry_present(built_pages):
    projects_html, _ = built_pages
    expected = _real_project_file_count()
    assert expected > 0

    actual = projects_html.count('class="story-row"')
    assert actual == expected, (
        f"expected {expected} project entries in built projects.html, found {actual}"
    )


def test_pupper_detail_page_renders_full_content(built_pages):
    _, pupper_html = built_pages
    assert 'class="detail-header__title"' in pupper_html
    assert "Stanford Pupper v3" in pupper_html
    assert 'class="content"' in pupper_html
    assert "Back to Projects" in pupper_html
