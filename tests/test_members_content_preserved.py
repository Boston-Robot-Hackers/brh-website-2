from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def real_member_file_count() -> int:
    return len(
        [
            f
            for f in (REPO_ROOT / "content" / "members").glob("*.md")
            if not f.stem.startswith("_")
        ]
    )


@pytest.fixture(scope="module")
def built_members_html():
    builder = WebsiteBuilder()
    builder.build_members_page()
    return (builder.dist_dir / "members.html").read_text()


def test_every_member_entry_present(built_members_html):
    expected = real_member_file_count()
    assert expected > 0

    actual = built_members_html.count('class="card member-card')
    assert actual == expected, (
        f"expected {expected} member cards in built members.html, found {actual}"
    )


def test_open_to_work_banner_present_for_flagged_members(built_members_html):
    opentowork_count = sum(
        1
        for f in (REPO_ROOT / "content" / "members").glob("*.md")
        if not f.stem.startswith("_") and "opentowork: true" in f.read_text()
    )
    assert opentowork_count > 0, (
        "expected at least one opentowork: true member in real content"
    )

    actual = built_members_html.count("open-to-work")
    assert actual == opentowork_count
