# TF20 upcoming-talks.txt lists every upcoming meeting, for Feature F20
**Date Created:** 2026-10-28

## TF20.0 — Replace the query
**Status**: done

**Description**: In `build/content_manager.py`, rename `get_upcoming_talks(today)` to `get_upcoming_meetings(today)`.

- Drop the main-only and speaker+topic filters, so it returns every meeting from `get_future_meetings(today)`.
- Add `kind` to each item. `speaker`/`topic` come from `metadata.get(...)`, so they're `None` when unset.
- Update the docstring. Keep the existing `page_path` rule.

**Test**: covered in TF20.3.

## TF20.1 — Rework the text template
**Status**: done

**Description**: In `templates/pages/upcoming-talks.txt`:

- Change the header to "Upcoming Meetings".
- Branch each block into the three shapes in F20: confirmed talk, TBA main, hands-on.
- Keep the shared When / Where / learn-more / register / schedule lines in one place rather than copying them three times.

**Test**: covered in TF20.3.

**Result**:

- Claude drafted the three branches. The user then rewrote the template, so each branch now has its own When/Where lines and there are no register or schedule lines.

## TF20.2 — Wire up the build and update the link labels
**Status**: done

**Description**:

- In `build/build.py`, `build_upcoming_talks` calls `get_upcoming_meetings`, passes `meetings` to the template, and prints `Built upcoming-talks.txt with N meetings`.
- Added after the template rewrite: stop requiring `registration_url`, since no template uses it. The key stays in `config/site.json`.
- In `templates/pages/index.html` and `templates/pages/meetings.html`, change the TXT link's `title` to "Upcoming meetings as plain text".

**Test**: covered in TF20.3. The existing link test in `test_ical_feed.py` checks the `href`, which doesn't change.

## TF20.3 — Write and update tests
**Status**: done

**Description**: Update `tests/test_content_manager.py` and `tests/test_upcoming_talks.py` for the new behavior:

- The query returns TBA main meetings and hands-on meetings, still drops past ones, and sorts soonest first.
- Items carry `kind`, and `speaker`/`topic` are `None` when unset.
- The rendered text has the "Upcoming Meetings" header.
- A confirmed talk's block keeps its current wording.
- A TBA main block shows its `text` and doesn't contain "Our main speaker".
- A hands-on block shows the hands-on intro and its default blurb.
- Each block has When / Where and the learn-more URL.
- Remove the old assertions that TBA and hands-on meetings are excluded.

**Test**: `uv run pytest` passes.

## TF20.4 — Update docs that describe the old rule
**Status**: done

**Description**: Update the places that say a meeting needs `speaker` + `topic` to appear in the text file:

- `README.md` (the content-model bullets).
- `process/02-doc/current.md`'s "Speakers to confirm" note.

Both should say `speaker` + `topic` only control the confirmed-talk wording here, plus a named event in `meetings.ics`.

**Test**: not feasible, docs only. Verified by reading the diff.
