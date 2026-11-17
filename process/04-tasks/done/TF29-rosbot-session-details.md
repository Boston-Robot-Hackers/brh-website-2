# TF29 Show ROSbot session front matter on session pages for Feature F29
**Date Created:** 2026-11-17

## TF29.0 — Write the tests first
**Status**: done

**Description**: Add to `tests/test_rosbot_section.py`:

* A session with `summary`, `medium` and `schedule` shows all three on its page, with labels.
* A session without them shows no empty labels.

## TF29.1 — Show the fields in the session page header
**Status**: done

**Description**: In `templates/details/rosbot-session-detail.html`, under the title:

* The summary, as a lead line.
* One meta line with "Format: <medium>" and "Schedule: <schedule>", each only when set, next to the existing date.

Reuse existing classes (`detail-brief-header__meta`, `note`). **No new CSS** unless the look is clearly wrong.

**Test**: TF29.0's tests.

## TF29.2 — Update the session template comment
**Status**: done

**Description**: Remove the "not shown on the site yet" line from `content/rosbot/sessions/_template.md`.

**Test**: none needed. It's a comment in a file the build skips, which `test_underscore_template_skipped` already covers.

## TF29.3 — Run the full suite and check the pages
**Status**: done

**Description**: Run `uv run pytest` and rebuild. Open sessions 1 to 3 in a browser and confirm the header reads well.

**Test**: the full suite. The visual check is manual, since the tests don't cover layout.

## TF29.4 — Close out
**Status**: done

**Description**:

* Remove the "ROSbot session fields not shown" item from `current.md`.
* Move both files to `done/` and set the feature's status fields.

**Test**: none; this is process bookkeeping.
