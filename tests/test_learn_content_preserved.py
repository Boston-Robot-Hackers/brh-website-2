import re
from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent


def _real_learn_link_count() -> int:
    text = (REPO_ROOT / "content" / "learn.md").read_text()
    return len(re.findall(r"^\s*- \[", text, re.MULTILINE))


@pytest.fixture(scope="module")
def built_learn_html():
    builder = WebsiteBuilder()
    builder.build_learn_page()
    return (builder.dist_dir / "learn.html").read_text()


def test_every_learn_link_present(built_learn_html):
    expected = _real_learn_link_count()
    assert expected > 0, "expected at least one resource link in content/learn.md"

    actual = built_learn_html.count('class="learn-link"')
    assert actual == expected, (
        f"expected {expected} resource links in built learn.html, found {actual}"
    )
