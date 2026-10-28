#!/usr/bin/env python3
# test_calendar_source — Tests for loading the meeting schedule from calendar.yaml
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-10-28
# Updated: 2026-10-28
# Open Source Under MIT license
from datetime import date

import pytest
from calendar_source import load_calendar

DEFAULTS = """\
defaults:
  location: Asylum
  main:
    time: "7:00pm"
  handson:
    time: "6:00pm"
    text: Just hacking.
"""


def load(tmp_path, body, defaults=DEFAULTS):
    path = tmp_path / "calendar.yaml"
    path.write_text(defaults + body)
    return load_calendar(path)


def test_missing_file_means_no_meetings(tmp_path):
    assert load_calendar(tmp_path / "calendar.yaml") == []


def test_defaults_merged_by_kind(tmp_path):
    meetings = load(
        tmp_path,
        "meetings:\n  - {date: 2026-11-12, kind: main}\n"
        "  - {date: 2026-11-25, kind: handson}\n",
    )
    main, handson = (meeting["metadata"] for meeting in meetings)
    assert main == {
        "location": "Asylum",
        "time": "7:00pm",
        "kind": "main",
        "date": "2026-11-12",
    }
    assert handson["time"] == "6:00pm"
    assert handson["text"] == "Just hacking."


def test_entry_overrides_defaults(tmp_path):
    meetings = load(
        tmp_path, "meetings:\n  - {date: 2026-11-25, kind: handson, text: Special}\n"
    )
    assert meetings[0]["metadata"]["text"] == "Special"


def test_explicit_empty_value_overrides_default(tmp_path):
    meetings = load(
        tmp_path, "meetings:\n  - {date: 2026-11-25, kind: handson, text: ''}\n"
    )
    assert meetings[0]["metadata"]["text"] == ""


def test_explicit_id_kept_and_not_in_metadata(tmp_path):
    meetings = load(
        tmp_path, "meetings:\n  - {id: 24-meeting, date: 2026-11-12, kind: main}\n"
    )
    assert meetings[0]["id"] == "24-meeting"
    assert "id" not in meetings[0]["metadata"]


def test_id_derived_from_date_and_kind(tmp_path):
    meetings = load(tmp_path, "meetings:\n  - {date: 2026-12-16, kind: handson}\n")
    assert meetings[0]["id"] == "2026-12-16-handson"


def test_sorted_ascending_with_date_obj(tmp_path):
    meetings = load(
        tmp_path,
        "meetings:\n  - {date: 2027-01-14, kind: main}\n"
        "  - {date: 2027-01-13, kind: handson}\n",
    )
    assert [meeting["date_obj"] for meeting in meetings] == [
        date(2027, 1, 13),
        date(2027, 1, 14),
    ]


def test_quoted_iso_date_accepted(tmp_path):
    meetings = load(tmp_path, 'meetings:\n  - {date: "2026-12-10", kind: main}\n')
    assert meetings[0]["date_obj"] == date(2026, 12, 10)


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        ("{date: 2026-12-10, kind: talk}", "kind"),
        ("{date: 2026-12-10}", "kind"),
        ("{kind: main}", "missing 'date'"),
        ("{date: 12/10/2026, kind: main}", "invalid date"),
        ("{date: 2026-12-10, kind: main, speakr: Ada}", "speakr"),
    ],
)
def test_bad_entry_raises_naming_entry(tmp_path, entry, message):
    with pytest.raises(ValueError, match=message) as excinfo:
        load(tmp_path, f"meetings:\n  - {entry}\n")
    assert "meeting #1" in str(excinfo.value)


def test_duplicate_id_raises(tmp_path):
    body = (
        "meetings:\n  - {id: x, date: 2026-12-10, kind: main}\n"
        "  - {id: x, date: 2026-12-16, kind: handson}\n"
    )
    with pytest.raises(ValueError, match="duplicate meeting id 'x'"):
        load(tmp_path, body)


def test_duplicate_derived_id_raises(tmp_path):
    body = (
        "meetings:\n  - {date: 2026-12-10, kind: main}\n"
        "  - {date: 2026-12-10, kind: main}\n"
    )
    with pytest.raises(ValueError, match="duplicate"):
        load(tmp_path, body)


@pytest.mark.parametrize(
    "defaults",
    ["defaults:\n  colour: red\n", "defaults:\n  main:\n    colour: red\n"],
)
def test_unknown_default_key_raises(tmp_path, defaults):
    with pytest.raises(ValueError, match="colour"):
        load(tmp_path, "meetings: []\n", defaults=defaults)


def test_unknown_top_level_key_raises(tmp_path):
    with pytest.raises(ValueError, match="meeting"):
        load(tmp_path, "meeting: []\n")
