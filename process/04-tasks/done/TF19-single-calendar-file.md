# TF19 Single calendar file and full calendar page for Feature F19
**Date Created:** 2026-10-27

## TF19.0 — Snapshot current outputs
**Status**: done

**Description**: Build once before any change and save `output/meetings.ics`, `output/upcoming-talks.txt` and the home/whatsnew meeting sections to the scratchpad. They are the baseline for confirming the migration changes nothing but the intended Jan 2027 date and the link targets.

**Test**: none; this produces the reference that TF19.3 and TF19.7 compare against.

## TF19.1 — Define the `calendar.yaml` schema and loader
**Status**: done

**Description**: Add a loader, likely a new `build/calendar_source.py` to keep `content_manager.py` from growing past its size. It reads `content/calendar.yaml`, merges `defaults` into each entry, derives `id` when absent, derives `title` and `type`, and returns the same `{id, metadata, date_obj, ...}` dicts `load_meetings()` returns today. Unknown keys, a missing `date`/`kind`, a bad `kind` and duplicate ids all raise a `ValueError` naming the entry. Add `pyyaml` to `[project] dependencies`; today it's only installed indirectly through `python-frontmatter`.

**Test**: new `tests/test_calendar_source.py` covers defaults merging, id derivation versus explicit id, title derivation, and each validation error.

## TF19.2 — Migrate the 35 meeting files into `calendar.yaml`
**Status**: done

**Description**: Use a one-off script in the scratchpad (not committed) to write `content/calendar.yaml` from the frontmatter. Fields equal to a default are dropped, and every entry keeps its explicit `id`. Change `30-meeting` to `2027-01-14`.

**Test**: a round-trip check in the scratchpad confirms that each migrated entry, once loaded, yields the same metadata as its `.md` file, apart from the one date fix.

## TF19.3 — Switch every reader to the new loader
**Status**: done

**Description**: Point `load_meetings()` and the `meetings` content type's `get_all_content` path at the new loader, so that `get_future_meetings`, `get_upcoming_talks`, `get_calendar_events`, hero, whatsnew and the home calendar all read `calendar.yaml`. Then delete `content/meetings/`.

**Test**: update the existing meeting fixtures in `tests/` to build a `calendar.yaml` instead of `.md` files, and the full suite passes. Diff `meetings.ics` and `upcoming-talks.txt` against the TF19.0 snapshot; the only differences should be the Jan 2027 date and the event URLs.

## TF19.4 — Retarget meeting links to `meetings.html#<id>`
**Status**: done

**Description**: Change `meeting_page_path()` and the fallback hrefs in `templates/cards/monthly-meeting-card.html` from `meetings/<id>.html` to `meetings.html#<id>`. Announcement links (`news/...`) are unchanged.

**Test**: unit test for `meeting_page_path()` in the no-announcement case; the existing `.ics` tests updated for the new URL.

## TF19.5 — Build the full calendar page
**Status**: done

**Description**: Rewrite `templates/pages/meetings.html` to show an "Upcoming" and a "Past" section. Each meeting is an element with `id="<id>"` showing date, time, kind, speaker/topic (or "Speaker and topic to be announced"), the blurb, and announcement/report links where present. Add a subscribe link to `meetings.ics`. Replace the current sort dropdown, since the two sections make it unnecessary. Use classes in `css/main.css` rather than the template's current inline `<style>` (in line with F15).

**Test**: a page-builder test renders the page from a small fixture and checks the upcoming/past split, the anchor ids, the TBD placeholder and the announcement link. Visually check light and dark mode at desktop and phone widths.

## TF19.6 — Remove meeting detail pages
**Status**: done

**Description**: Stop calling `build_detail_pages` for meetings in `build_meetings_page`, drop `detail_template` from the `meetings` content type, and delete `templates/details/meeting-detail.html`.

**Test**: a build test asserts that `output/meetings/` isn't produced. Grep `output/` for `meetings/` hrefs and expect only `images/meetings/` matches.

## TF19.7 — Tests and docs
**Status**: done

**Description**: Make sure every step above has its test and the full suite plus `ruff check` pass. Update README.md's content-model section to describe `calendar.yaml`. Replace the "Speakers to confirm" note in `current.md` with the new "edit `calendar.yaml`" instruction. Run the demo from F19.

**Test**: `uv run pytest` and `uv run ruff check` both pass; the demo steps in F19 produce the expected output.

## Result

- **Single source**: `content/calendar.yaml` (35 meetings, migrated losslessly, with Jan 2027 moved to 2027-01-14) is read by `build/calendar_source.py`; `content/meetings/` and the meeting detail pages are gone.
- **Outputs unchanged except as intended**: against the TF19.0 baseline, only the Jan 2027 date and the fallback links (`meetings/<id>.html` → `meetings.html#<id>`) differ; all 18 `.ics` UIDs are identical.
- **Dead code removed**: the monthly meeting cards (`render_monthly_meeting_cards`, `group_meetings_by_month`, `cards/monthly-meeting-card.html`, their CSS) had no remaining user, since `whatsnew.html` never rendered its `meetings_content`.
- **Anchor offset**: `.calendar-entry` has a per-breakpoint `scroll-margin-top`, so `meetings.html#<id>` lands below the sticky header (76–237px tall depending on nav wrapping); verified at 390–1280px.
