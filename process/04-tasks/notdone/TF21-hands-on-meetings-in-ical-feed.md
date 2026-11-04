# TF21 Description for Feature F21
**Date Created:** 2026-11-04

## TF21.0 — Include hands-on meetings in `get_calendar_events`
**Status**: done
**Description**:

* Remove the `kind != "main"` filter in `build/content_manager.py`.
* Add `kind` to each event dict, for the template to use.
* Update the docstring, which says "All main meetings".

**Test**: replace `test_handson_excluded` with a test that a hands-on meeting is included, starts at its own `time`, and ends `duration` later.

**Result**:

* Filter removed and `kind` added to each event.
* `test_handson_included_with_its_own_start_and_duration` replaces the old test.

## TF21.1 — Hands-on event title
**Status**: done
**Description**:

* In `templates/pages/meetings.ics`, add a `handson` branch to `SUMMARY`: `<site title> hands-on meeting`.
* The branch goes after the existing speaker-and-topic check, so no extra precedence logic is needed.
* Main meeting titles do not change.

**Test**: real-build test in TF21.3 asserts the title on the Nov 11, 2026 event.

**Result**:

* `SUMMARY` has a new `handson` branch after the speaker-and-topic check.
* No current hands-on entry has a speaker or topic, so all 17 get the hands-on title.

## TF21.2 — Update docs
**Status**: done
**Description**:

* Update the `build_ical_feed` docstring in `build/build.py`, which says "feed of main meetings".
* Update `README.md` wherever it describes the feed as main-only.

**Test**: not feasible, documentation only.

**Result**:

* `build_ical_feed` docstring updated.
* `README.md` needed no change: it never describes the feed as main-only.

## TF21.3 — Write tests (dedicated)
**Status**: done
**Description**:

* Fixture tests in `tests/test_ical_feed.py`:
  * Both kinds appear together, ascending by date.
  * A hands-on event's `page_path` uses its announcement.
* Real-build tests against `content/calendar.yaml`:
  * Replace `test_one_event_per_main_meeting` with one event per meeting of any kind.
  * The Nov 11, 2026 event has the hands-on title and starts at 18:00 `America/New_York`.
  * A main meeting's title and start are unchanged, via the existing `test_talk_summary_and_local_start`.
  * `UID`s remain unique, via the existing `test_uids_unique`.

**Test**: this task is the tests.

**Result**:

* Added `test_both_kinds_ascending_by_date` and `test_handson_page_path_uses_announcement`.
* Added `test_one_event_per_meeting_of_either_kind` and `test_handson_summary_and_local_start`.
* The Nov 11 test finds its event by the stable `27-handson-meeting` id, since that meeting's date has already moved once.

## TF21.4 — Full verification
**Status**: not done
**Description**:

* `uv run python build/build.py` builds cleanly.
* `uv run pytest` passes.
* `uvx ruff check build/ tests/` shows no new findings.
* Manual: import `output/meetings.ics` into a calendar app and spot-check one hands-on and one main meeting.

**Test**: the commands above. The manual import check needs a calendar app, so record its result here.

**Result**:

* Build is clean: `meetings.ics` has 35 events, 18 main and 17 hands-on.
* `uv run pytest`: 224 passed. `uvx ruff check build/ tests/`: all checks passed.
* **Manual calendar-app import check: still to do, by the user.** This task stays open until then.
