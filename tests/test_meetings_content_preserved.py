#!/usr/bin/env python3
# test_meetings_content_preserved — Calendar page shows every calendar.yaml meeting
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-09-21
# Updated: 2026-10-28
# Open Source Under MIT license
import re
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from calendar_source import load_calendar

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
TODAY = date(2026, 11, 1)


@pytest.fixture(scope="module")
def built():
    builder = WebsiteBuilder()
    builder.asset_manager.clean_output_directory()
    builder.build_meetings_page(TODAY)
    builder.build_ical_feed(datetime.now(UTC))
    return builder


@pytest.fixture(scope="module")
def meetings_html(built):
    return (built.dist_dir / "meetings.html").read_text()


def test_every_meeting_has_an_anchored_entry(meetings_html):
    meetings = load_calendar(REPO_ROOT / "content" / "calendar.yaml")
    assert meetings
    anchors = re.findall(r'<article id="([^"]+)" class="calendar-entry', meetings_html)
    assert sorted(anchors) == sorted(meeting["id"] for meeting in meetings)


def test_upcoming_section_precedes_past(meetings_html):
    assert meetings_html.index(">Upcoming<") < meetings_html.index(">Past<")


def test_no_meeting_detail_pages(built):
    assert not (built.dist_dir / "meetings").exists()


def test_meeting_links_resolve_to_calendar_anchors(built, meetings_html):
    """Every `meetings.html#id` link in the iCal feed lands on a real entry."""
    raw = (built.dist_dir / "meetings.ics").read_bytes().decode()
    feed = raw.replace("\r\n ", "").replace("\r\n", "\n")
    targets = set(re.findall(r"^URL:\S+/meetings\.html#(\S+)$", feed, re.MULTILINE))
    assert targets
    anchors = set(re.findall(r'<article id="([^"]+)"', meetings_html))
    assert targets <= anchors
    assert "/meetings/" not in feed
