# TF17 Description for Feature F17

**Date Created:** 2026-09-21

## TF17.0 — Config: `meeting_duration_minutes`
**Status**: done
**Description**:

* Add `"meeting_duration_minutes": 120` to `config/site.json` (7:00–9:00pm).
* The build raises if it's missing or not a positive integer.

**Test**: config test asserts the key is a positive integer.

**Result**:

* Added `"meeting_duration_minutes": 120`; `build_ical_feed` raises unless it's a positive int (tested for 0, -5, `"120"`, 1.5).

## TF17.1 — Parse meeting start time
**Status**: done
**Description**:

* New `parse_meeting_time` in `build/content_manager.py`: `"7:00pm"` → `time(19, 0)`.
* Anything not matching `H:MMam/pm` raises `ValueError` naming the file.

**Test**: `tests/test_content_manager.py` — `6:00pm`, `7:00pm`, `12:00pm`, `12:30am`; bad values (`7pm`, `19:00`, empty) raise.

**Result**:

* `parse_meeting_time` lives in the new `build/ical_format.py`, not `content_manager.py`, which was already past the ~300-line guideline.
* Tests in `tests/test_ical_feed.py::TestParseMeetingTime`.

## TF17.2 — `ContentManager.get_calendar_events`
**Status**: done
**Description**:

* All main meetings (past + future), ascending by date; hands-on excluded.
* Per event: `uid`, `summary`, `description`, `location`, `start` (aware `datetime`, `America/New_York` via `zoneinfo`), `end`, `page_path`.
* Summary rule and `page_path` rule as in F17. Reuse F11's `page_path` logic rather than duplicating it.

**Test**: fixture meetings cover talk and TBA main summaries, hands-on excluded, UID format, start+duration → end, announcement vs meeting-page URL.

**Result**:

* Extracted `load_meetings` (shared by `get_future_meetings`) and `meeting_page_path` (shared with F11's `get_upcoming_talks`).
* Summary wording lives in the template, using `site.title`; events carry `topic`/`speaker` (None when TBA).

## TF17.3 — iCal template + RFC 5545 formatting
**Status**: done
**Description**:

* New `templates/pages/meetings.ics` (Jinja): `VCALENDAR`, `VTIMEZONE` for `America/New_York`, one `VEVENT` per event.
* New `ics_text` Jinja filter: escapes `\` `;` `,` and newlines.
* New `fold_ics` function: CRLF line endings and 75-octet folding, never splitting a multi-byte UTF-8 character.
* `WebsiteBuilder.build_ical_feed` renders, folds, and writes `output/meetings.ics`; called from `build()`.

**Test**: unit tests for `ics_text` (each escaped character) and `fold_ics` (short line untouched, long ASCII line folded, long line with em dashes folded on a character boundary, all lines end in CRLF).

**Result**:

* `templates/pages/meetings.ics`, `ics_text` filter, `fold_ics` in `build/ical_format.py`.
* Written as bytes so CRLF survives on every platform. Blank template lines are dropped by `fold_ics`.

## TF17.4 — Write tests (dedicated)
**Status**: done
**Description**:

* Add `icalendar` as a **dev dependency** and use it to parse the built file — an independent check that the output is well-formed.
* Build-level test against real content:
  * Parses without error; one `VEVENT` per main meeting file, none for hands-on.
  * UIDs are unique.
  * Oct 15 talk: summary contains Arjun's topic, starts 19:00 America/New_York.
  * Every line ≤ 75 octets and ends in CRLF.

**Test**: this task is the tests.

**Result**:

* `icalendar` added as a dev dependency. `tests/test_ical_feed.py`: 38 tests, all pass.
* The real build yields 18 events (one per main meeting).

## TF17.6 — Tiny TXT / iCal links on the home page
**Status**: done
**Description**:

* In `templates/pages/index.html`, next to the "Upcoming Meetings" rail heading: `TXT` → `upcoming-talks.txt`, `iCal` → `meetings.ics`.
* Small, muted, right-aligned; styles in `css/main.css` as a named class using theme variables — no inline `style=`.

**Test**: build the home page; assert both links sit inside the rail heading, point at `upcoming-talks.txt` and `meetings.ics`, and both targets exist after a full build.

**Result**:

* Links sit right-aligned inside the rail heading, each in its own orange (`--accent`) rounded pill (`.rail-feeds` in `css/main.css`).
* Checked visually with a headless Chrome screenshot.
* `TestHomePageFeedLinks` in `tests/test_ical_feed.py`: 2 tests pass.

## TF17.5 — Full verification
**Status**: done
**Description**:

* `uv run python build/build.py` builds cleanly; `uv run pytest` passes; `uvx ruff check build/ tests/` shows no new findings.
* Manual: import `output/meetings.ics` into Apple or Google Calendar; spot-check times and links.

**Test**: the commands above; manual import check recorded here.

**Result**:

* Build is clean; ruff shows no new findings.
* `uv run pytest`: 198/198 pass.
* Manual calendar-app import check: confirmed by the user 2026-09-21.
