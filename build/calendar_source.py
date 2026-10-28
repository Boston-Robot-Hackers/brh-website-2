#!/usr/bin/env python3
# calendar_source — Load the meeting schedule from content/calendar.yaml
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-10-28
# Updated: 2026-10-28
# Open Source Under MIT license
"""The single source of truth for the meeting schedule.

`calendar.yaml` has a `defaults` block and a `meetings` list. Each entry
needs only `date` and `kind`; every other field falls back first to
`defaults.<kind>`, then to the top level of `defaults`. An entry's `id` is
explicit for meetings migrated from the old per-file layout (it is the
`.ics` event UID, so it must never change) and otherwise derived from the
date and kind. Anything unexpected - an unknown key, a bad kind, a
duplicate id - raises, naming the entry. A missing file raises too, since
the site always has a schedule; an empty file means no meetings.
"""

from datetime import date
from pathlib import Path
from typing import Any

import yaml

KINDS = ("main", "handson")
DEFAULTABLE_FIELDS = {
    "time",
    "location",
    "text",
    "speaker",
    "topic",
    "announcement",
    "report",
}
ENTRY_FIELDS = DEFAULTABLE_FIELDS | {"id", "date", "kind"}


def load_calendar(path: Path) -> list[dict[str, Any]]:
    """Load every meeting from `path`, sorted by date ascending.

    Each meeting is `{"id", "date_obj", "metadata"}`, where `metadata` holds
    the merged fields with `date` as an ISO string.
    """
    if not path.exists():
        raise FileNotFoundError(f"meeting schedule not found: {path}")
    schedule = yaml.safe_load(path.read_text()) or {}
    unknown = set(schedule) - {"defaults", "meetings"}
    if unknown:
        raise ValueError(f"{path.name}: unknown top-level keys {sorted(unknown)}")
    defaults = schedule.get("defaults") or {}
    check_defaults(defaults, path.name)

    meetings = []
    seen_ids = set()
    for index, entry in enumerate(schedule.get("meetings") or []):
        try:
            meeting = build_meeting(entry, defaults)
        except ValueError as e:
            raise ValueError(f"{path.name}: meeting #{index + 1}: {e}") from e
        if meeting["id"] in seen_ids:
            raise ValueError(f"{path.name}: duplicate meeting id {meeting['id']!r}")
        seen_ids.add(meeting["id"])
        meetings.append(meeting)

    meetings.sort(key=lambda meeting: meeting["date_obj"])
    return meetings


def check_defaults(defaults: dict[str, Any], filename: str):
    """Raise if `defaults` has a key that no meeting could use."""
    unknown = set(defaults) - DEFAULTABLE_FIELDS - set(KINDS)
    for kind in KINDS:
        unknown |= set(defaults.get(kind) or {}) - DEFAULTABLE_FIELDS
    if unknown:
        raise ValueError(f"{filename}: unknown keys in defaults {sorted(unknown)}")


def build_meeting(entry: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    """Validate one entry and merge its defaults into a meeting dict."""
    unknown = set(entry) - ENTRY_FIELDS
    if unknown:
        raise ValueError(f"unknown keys {sorted(unknown)}")
    kind = entry.get("kind")
    if kind not in KINDS:
        raise ValueError(f"'kind' must be 'main' or 'handson', got {kind!r}")
    if not entry.get("date"):
        raise ValueError("missing 'date'")
    try:
        meeting_date = date.fromisoformat(str(entry["date"]))
    except ValueError as e:
        raise ValueError(f"invalid date {entry['date']!r}: expected YYYY-MM-DD") from e

    shared = {key: defaults[key] for key in DEFAULTABLE_FIELDS & set(defaults)}
    metadata = {**shared, **(defaults.get(kind) or {}), **entry}
    metadata["date"] = meeting_date.isoformat()
    meeting_id = str(entry.get("id") or f"{metadata['date']}-{kind}")
    metadata.pop("id", None)
    return {"id": meeting_id, "date_obj": meeting_date, "metadata": metadata}
