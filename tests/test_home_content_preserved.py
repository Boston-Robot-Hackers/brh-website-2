from pathlib import Path

import frontmatter
import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def _frontmatter_titles(
    content_subdir: str, only_highlighted: bool = False
) -> list[str]:
    titles = []
    for md_file in (REPO_ROOT / "content" / content_subdir).glob("*.md"):
        if md_file.stem.startswith("_"):
            continue
        post = frontmatter.load(md_file)
        if only_highlighted and not post.metadata.get("highlight"):
            continue
        titles.append(post.metadata.get("title", ""))
    return titles


@pytest.fixture(scope="module")
def built_index_html():
    """Runs the real build_index() against the real content/ directory -
    this is a content-preservation regression test for F05/TF05.5's home
    page rewrite, so it must check real content, not a fixture."""
    builder = WebsiteBuilder()
    builder.build_index()
    return (builder.dist_dir / "index.html").read_text()


def test_every_highlighted_news_title_present(built_index_html):
    titles = _frontmatter_titles("news", only_highlighted=True)
    assert titles, "expected at least one highlighted news post"
    for title in titles:
        assert title in built_index_html, f"missing highlighted news title: {title}"


def test_every_project_title_present(built_index_html):
    titles = _frontmatter_titles("projects")
    assert titles, "expected at least one project"
    for title in titles:
        assert title in built_index_html, f"missing project title: {title}"


def test_pupper_spotlight_present(built_index_html):
    assert "Meet Pupper" in built_index_html
    assert "images/projects/pupper_standing.jpg" in built_index_html
    assert "projects/pupper.html" in built_index_html


def test_qr_code_present(built_index_html):
    assert "signup-qr.png" in built_index_html
    assert 'alt="' in built_index_html


def test_upcoming_meetings_present(built_index_html):
    assert "Upcoming Meetings" in built_index_html
