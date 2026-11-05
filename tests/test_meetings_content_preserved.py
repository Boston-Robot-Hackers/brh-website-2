#!/usr/bin/env python3
# test_meetings_content_preserved — Calendar page shows calendar.yaml's main meetings
# Author: Pito Salas and Claude Code
# Version: 6
# Created: 2026-09-21
# Updated: 2026-11-05
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
def built(tmp_path_factory):
    builder = WebsiteBuilder()
    builder.dist_dir = tmp_path_factory.mktemp("output")
    builder.page_builder.dist_dir = builder.dist_dir
    builder.build_meetings_page(TODAY)
    builder.build_ical_feed(datetime.now(UTC))
    return builder


@pytest.fixture(scope="module")
def meetings_html(built):
    return (built.dist_dir / "meetings.html").read_text()


def test_builds_outside_the_real_output_directory(built):
    assert built.dist_dir.resolve() != (REPO_ROOT / "output").resolve()


def page_anchors(meetings_html):
    """Every meeting anchor on the page: cards plus to-be-announced dates."""
    return re.findall(
        r'id="([^"]+)" class="calendar-(?:entry|tba__date)"', meetings_html
    )


def schedule():
    return load_calendar(REPO_ROOT / "content" / "calendar.yaml")


def test_every_main_meeting_has_an_anchor(meetings_html):
    main_ids = [m["id"] for m in schedule() if m["metadata"]["kind"] == "main"]
    assert main_ids
    assert sorted(page_anchors(meetings_html)) == sorted(main_ids)


def test_handson_meetings_are_not_listed(meetings_html):
    handson_ids = [m["id"] for m in schedule() if m["metadata"]["kind"] == "handson"]
    assert handson_ids
    assert not set(handson_ids) & set(page_anchors(meetings_html))


def test_header_line_holds_location_and_feeds(meetings_html):
    header = re.search(
        r'<h2 class="section-heading calendar-section-title">Upcoming Meetings.*?</h2>',
        meetings_html,
        re.DOTALL,
    ).group(0)
    assert "All meetings at" in header
    assert 'href="meetings.ics"' in header
    assert 'href="upcoming-talks.txt"' in header


def test_past_section_is_titled_past_meetings(meetings_html):
    heading = 'section-heading--spaced calendar-section-title">Past Meetings</h2>'
    assert heading in meetings_html


def test_removed_header_elements_stay_gone(meetings_html):
    assert "Hands-on meetings:" not in meetings_html
    assert "We meet twice a month" not in meetings_html
    assert "calendar-header" not in meetings_html


def test_cards_show_title_blurb_and_link_to_announcement(meetings_html):
    articles = re.findall(r"<article.*?</article>", meetings_html, re.DOTALL)
    by_id = {re.search(r'id="([^"]+)"', a).group(1): a for a in articles}
    cards = [
        m
        for m in schedule()
        if m["metadata"].get("blurb") and m["metadata"].get("announcement")
    ]
    assert cards
    for meeting in cards:
        card = by_id[meeting["id"]]
        metadata = meeting["metadata"]
        assert metadata["topic"] in card
        assert metadata["blurb"] in card
        assert 'class="calendar-entry__link" href="news/' in card
        assert 'class="calendar-entry__month"' in card


def test_to_be_announced_dates_have_no_card(meetings_html):
    to_announce = [
        m
        for m in schedule()
        if m["metadata"]["kind"] == "main"
        and not m["metadata"].get("topic")
        and m["date_obj"] >= TODAY
    ]
    for meeting in to_announce:
        assert f'<span id="{meeting["id"]}"' in meetings_html
        assert f'<article id="{meeting["id"]}"' not in meetings_html


def test_upcoming_section_precedes_past(meetings_html):
    upcoming_at = meetings_html.index(">Upcoming Meetings")
    assert upcoming_at < meetings_html.index(">Past Meetings<")


def test_no_meeting_detail_pages(built):
    assert not (built.dist_dir / "meetings").exists()


def test_upcoming_talks_links_resolve_to_calendar_anchors(built, meetings_html):
    """Every `meetings.html#id` page path in the upcoming list has an anchor."""
    upcoming = built.content_manager.get_upcoming_meetings(TODAY)
    targets = {
        meeting["page_path"].split("#")[1]
        for meeting in upcoming
        if "#" in meeting["page_path"]
    }
    assert targets <= set(page_anchors(meetings_html))


def test_meeting_links_resolve_to_calendar_anchors(built, meetings_html):
    """Every `meetings.html#id` link in the iCal feed lands on a real entry."""
    raw = (built.dist_dir / "meetings.ics").read_bytes().decode()
    feed = raw.replace("\r\n ", "").replace("\r\n", "\n")
    targets = set(re.findall(r"^URL:\S+/meetings\.html#(\S+)$", feed, re.MULTILINE))
    assert targets
    assert targets <= set(page_anchors(meetings_html))
    assert "/meetings/" not in feed
