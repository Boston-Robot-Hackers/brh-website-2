#!/usr/bin/env python3
# test_upcoming_talks — Tests for the plain-text upcoming meetings list
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-09-21
# Updated: 2026-10-28
# Open Source Under MIT license

import json
import re
from datetime import date
from pathlib import Path

import pytest
from content_manager import format_long_date
from jinja2 import Environment, FileSystemLoader

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE = {
    "title": "Boston Robot Hackers",
    "site_url": "https://bostonrobothackers.com",
}
SAMPLE_TALK = {
    "kind": "main",
    "topic": 'Robots & Rain: "Wet" Autonomy',
    "speaker": "Ada Lovelace",
    "summary": "A talk about <robots> in weather.",
    "date_obj": date(2026, 10, 15),
    "time": "7:00pm",
    "location": "Artisans Asylum",
    "page_path": "news/ada-talk.html",
}
SAMPLE_TBA = {
    **SAMPLE_TALK,
    "speaker": None,
    "topic": None,
    "summary": "Speaker and topic to be announced.",
    "date_obj": date(2026, 12, 10),
}
SAMPLE_HANDSON = {
    **SAMPLE_TBA,
    "kind": "handson",
    "summary": "Just hacking together.",
    "date_obj": date(2026, 11, 25),
}


def render(meetings):
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "templates")))
    env.filters["long_date"] = format_long_date
    template = env.get_template("pages/upcoming-talks.txt")
    return template.render(site=SITE, meetings=meetings, generated=date(2026, 9, 18))


class TestSiteConfig:
    def test_site_url_is_https_without_trailing_slash(self):
        config = json.loads((REPO_ROOT / "config" / "site.json").read_text())
        assert config["site_url"].startswith("https://")
        assert not config["site_url"].endswith("/")


class TestTemplate:
    def test_header_says_upcoming_meetings(self):
        assert "Boston Robot Hackers — Upcoming Meetings" in render([])

    def test_every_url_is_plain_absolute_site_url(self):
        urls = re.findall(r"https?://\S+", render([SAMPLE_TALK]))
        assert urls
        for url in urls:
            assert re.fullmatch(r"https://bostonrobothackers\.com/\S+", url), url

    def test_confirmed_talk_names_speaker_and_topic(self):
        text = render([SAMPLE_TALK])
        assert "October Main Club Meeting" in text
        assert "Speaker: Ada Lovelace" in text
        assert f'Topic: "{SAMPLE_TALK["topic"]}"' in text

    def test_tba_main_meeting_shows_tbd(self):
        text = render([SAMPLE_TBA])
        assert "December Main Club Meeting" in text
        assert "Speaker: TBD" in text
        assert "Topic: TBD" in text

    def test_handson_meeting_has_no_speaker_line(self):
        text = render([SAMPLE_HANDSON])
        assert "November Hands-on meeting" in text
        assert "Speaker:" not in text

    def test_no_trailing_whitespace(self):
        text = render([SAMPLE_TALK, SAMPLE_TBA, SAMPLE_HANDSON])
        assert [line for line in text.splitlines() if line != line.rstrip()] == []

    def test_every_block_has_when_and_where(self):
        text = render([SAMPLE_TALK, SAMPLE_TBA, SAMPLE_HANDSON])
        assert text.count("When: ") == 3
        assert text.count("Where: Artisans Asylum") == 3

    def test_talk_url_joins_site_url_and_page_path(self):
        text = render([SAMPLE_TALK])
        assert "https://bostonrobothackers.com/news/ada-talk.html" in text

    def test_text_is_not_html_escaped(self):
        text = render([SAMPLE_TALK])
        assert SAMPLE_TALK["topic"] in text
        assert SAMPLE_TALK["summary"] in text
        assert "&amp;" not in text
        assert "&#34;" not in text
        assert "&lt;" not in text

    def test_no_redirect_wrappers(self):
        assert "google.com" not in render([SAMPLE_TALK])

    def test_long_date_format(self):
        assert "Thursday, October 15, 2026" in render([SAMPLE_TALK])


class TestBuildMissingConfig:
    def test_missing_site_url_raises(self):
        builder = WebsiteBuilder()
        del builder.site_config["site_url"]
        with pytest.raises(ValueError, match="site_url"):
            builder.build_upcoming_talks(date(2026, 9, 18))


@pytest.fixture(scope="module")
def built_text():
    builder = WebsiteBuilder()
    builder.build_upcoming_talks(date(2026, 9, 18))
    return (builder.dist_dir / "upcoming-talks.txt").read_text(encoding="utf-8-sig")


class TestRealBuild:
    def test_starts_with_utf8_bom(self):
        builder = WebsiteBuilder()
        builder.build_upcoming_talks(date(2026, 9, 18))
        raw = (builder.dist_dir / "upcoming-talks.txt").read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf")
        assert "—".encode() in raw

    def test_lists_the_confirmed_talks(self, built_text):
        assert "Speaker: Arjun Viswanathan" in built_text
        assert "Speaker: Yun Chang" in built_text

    def test_includes_handson_and_tba_meetings(self, built_text):
        assert "Hands-on meeting" in built_text
        assert "Speaker: TBD" in built_text
