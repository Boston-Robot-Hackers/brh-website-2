from pathlib import Path

import pytest

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent

# Key phrases from every section of the real content/about.md - a
# regression test that the restyle didn't drop any section.
EXPECTED_PHRASES = [
    "Our Mission",
    "Boston Robot Hackers is a community-driven organization",
    "Resources",
    "Monthly Meetups",
    "Mailing List",
    "Educational Resources",
    "Our Community",
    "Students",
    "Meeting Location",
    "Artisans Asylum",
    "Contact Us",
    "Currently BRH is led by Pito Salas",
]


@pytest.fixture(scope="module")
def built_about_html():
    builder = WebsiteBuilder()
    builder.build_about_page()
    return (builder.dist_dir / "about.html").read_text()


def test_every_about_section_present(built_about_html):
    for phrase in EXPECTED_PHRASES:
        assert phrase in built_about_html, f"missing expected phrase: {phrase}"
