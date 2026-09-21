#!/usr/bin/env python3
"""
test_ical_feed.py — Tests for the meetings iCalendar feed.

Author: Pito Salas and Claude Code
Open Source Under MIT license
"""

import json
import re
from datetime import UTC, datetime, time, timedelta
from pathlib import Path

import pytest
from content_manager import BOSTON, ContentManager
from ical_format import fold_ics, ics_text, parse_meeting_time
from icalendar import Calendar

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
TWO_HOURS = timedelta(minutes=120)


def write_meeting(content_dir, name, **fields):
    lines = "".join(f'{key}: "{value}"\n' for key, value in fields.items())
    (content_dir / "meetings" / f"{name}.md").write_text(f"---\n{lines}---\n")


class TestParseMeetingTime:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("6:00pm", time(18, 0)),
            ("7:00pm", time(19, 0)),
            ("12:00pm", time(12, 0)),
            ("12:30am", time(0, 30)),
            ("9:15am", time(9, 15)),
        ],
    )
    def test_parses_valid_times(self, value, expected):
        assert parse_meeting_time(value) == expected

    @pytest.mark.parametrize("value", ["7pm", "19:00", "", None, "7:00 pm", "13:00pm"])
    def test_rejects_other_shapes(self, value):
        with pytest.raises(ValueError, match="7:00pm"):
            parse_meeting_time(value)


class TestIcsText:
    @pytest.mark.parametrize(
        ("raw", "escaped"),
        [
            ("a\\b", "a\\\\b"),
            ("a;b", r"a\;b"),
            ("a,b", "a\\,b"),
            ("a\nb", "a\\nb"),
            ("a\r\nb", "a\\nb"),
        ],
    )
    def test_escapes_special_characters(self, raw, escaped):
        assert ics_text(raw) == escaped

    def test_plain_text_unchanged(self):
        assert ics_text("Robots — rain") == "Robots — rain"


class TestFoldIcs:
    def test_short_line_untouched_with_crlf(self):
        assert fold_ics("BEGIN:VEVENT\n") == "BEGIN:VEVENT\r\n"

    def test_blank_template_lines_dropped(self):
        assert fold_ics("A:1\n\n   \nB:2\n") == "A:1\r\nB:2\r\n"

    def test_long_ascii_line_folded_at_75_octets(self):
        folded = fold_ics("X:" + "a" * 200)
        lines = folded.split("\r\n")[:-1]
        assert all(len(line.encode()) <= 75 for line in lines)
        assert all(line.startswith(" ") for line in lines[1:])
        assert "".join(line[1:] if i else line for i, line in enumerate(lines)) == (
            "X:" + "a" * 200
        )

    def test_multibyte_characters_never_split(self):
        original = "DESCRIPTION:" + "é—" * 60
        lines = fold_ics(original).split("\r\n")[:-1]
        assert all(len(line.encode()) <= 75 for line in lines)
        rejoined = "".join(line[1:] if i else line for i, line in enumerate(lines))
        assert rejoined == original


class TestGetCalendarEvents:
    TALK = {"kind": "main", "time": "7:00pm", "location": "Asylum", "text": "Hi"}

    def events(self, content_dir):
        return ContentManager(content_dir).get_calendar_events(TWO_HOURS)

    def test_includes_past_and_future_main_meetings_ascending(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "future", date="2099-01-01", **self.TALK)
        write_meeting(tmp_path, "past", date="2020-01-01", **self.TALK)
        assert [e["id"] for e in self.events(tmp_path)] == ["past", "future"]

    def test_handson_excluded(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        handson = {**self.TALK, "kind": "handson", "time": "6:00pm"}
        write_meeting(tmp_path, "h", date="2026-10-01", **handson)
        assert self.events(tmp_path) == []

    def test_start_is_boston_local_and_end_adds_duration(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "m", date="2026-10-15", **self.TALK)
        event = self.events(tmp_path)[0]
        assert event["start"] == datetime(2026, 10, 15, 19, 0, tzinfo=BOSTON)
        assert event["end"] == datetime(2026, 10, 15, 21, 0, tzinfo=BOSTON)

    def test_topic_and_speaker_none_when_tba(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "m", date="2026-10-15", **self.TALK)
        event = self.events(tmp_path)[0]
        assert event["topic"] is None
        assert event["speaker"] is None

    def test_page_path_uses_announcement_when_present(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        (tmp_path / "news").mkdir()
        (tmp_path / "news" / "talk.md").write_text("---\ntitle: T\n---\nx.\n")
        write_meeting(
            tmp_path, "m", date="2026-10-15", announcement="talk.md", **self.TALK
        )
        assert self.events(tmp_path)[0]["page_path"] == "news/talk.html"

    def test_page_path_falls_back_to_meeting_page(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "7-meeting", date="2026-10-15", **self.TALK)
        assert self.events(tmp_path)[0]["page_path"] == "meetings/7-meeting.html"

    def test_bad_time_raises_naming_meeting(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        bad_time = {**self.TALK, "time": "7pm"}
        write_meeting(tmp_path, "7-meeting", date="2026-10-15", **bad_time)
        with pytest.raises(ValueError, match="7-meeting"):
            self.events(tmp_path)


class TestConfig:
    def test_meeting_duration_is_positive_int(self):
        config = json.loads((REPO_ROOT / "config" / "site.json").read_text())
        minutes = config["meeting_duration_minutes"]
        assert isinstance(minutes, int)
        assert minutes > 0

    @pytest.mark.parametrize("bad", [0, -5, "120", 1.5])
    def test_bad_duration_raises(self, bad):
        builder = WebsiteBuilder()
        builder.site_config["meeting_duration_minutes"] = bad
        with pytest.raises(ValueError, match="meeting_duration_minutes"):
            builder.build_ical_feed(datetime.now(UTC))


@pytest.fixture(scope="module")
def built_feed() -> bytes:
    builder = WebsiteBuilder()
    builder.build_ical_feed(datetime(2026, 9, 18, tzinfo=UTC))
    return (builder.dist_dir / "meetings.ics").read_bytes()


class TestRealBuild:
    def test_parses_as_valid_calendar(self, built_feed):
        Calendar.from_ical(built_feed)

    def test_one_event_per_main_meeting(self, built_feed):
        meetings = ContentManager(REPO_ROOT / "content").load_meetings()
        main_count = sum(1 for m in meetings if m["metadata"]["kind"] == "main")
        events = Calendar.from_ical(built_feed).walk("VEVENT")
        assert len(events) == main_count
        assert main_count > 0

    def test_uids_unique(self, built_feed):
        uids = [str(e["UID"]) for e in Calendar.from_ical(built_feed).walk("VEVENT")]
        assert len(uids) == len(set(uids))

    def test_talk_summary_and_local_start(self, built_feed):
        events = Calendar.from_ical(built_feed).walk("VEVENT")
        arjun = next(e for e in events if "Arjun" in str(e["SUMMARY"]))
        assert "Reinforcement Learning for Multimodal Locomotion" in str(
            arjun["SUMMARY"]
        )
        start = arjun["DTSTART"].dt
        assert start == datetime(2026, 10, 15, 19, 0, tzinfo=BOSTON)
        assert str(start.tzinfo) == "America/New_York"

    def test_every_line_crlf_and_at_most_75_octets(self, built_feed):
        assert built_feed.endswith(b"\r\n")
        lines = built_feed.split(b"\r\n")[:-1]
        assert all(b"\n" not in line and b"\r" not in line for line in lines)
        assert all(len(line) <= 75 for line in lines)


@pytest.fixture(scope="module")
def rail_heading():
    builder = WebsiteBuilder()
    builder.build()
    html = (builder.dist_dir / "index.html").read_text()
    match = re.search(r'<h2 class="rail-title">.*?</h2>', html, re.S)
    assert match and "Upcoming Meetings" in match[0]
    return builder.dist_dir, match[0]


class TestHomePageFeedLinks:
    @pytest.mark.parametrize(
        ("label", "target"), [("TXT", "upcoming-talks.txt"), ("iCal", "meetings.ics")]
    )
    def test_link_beside_heading_points_at_built_file(
        self, rail_heading, label, target
    ):
        dist_dir, heading = rail_heading
        assert re.search(rf'<a href="{re.escape(target)}"[^>]*>{label}</a>', heading)
        assert (dist_dir / target).is_file()
