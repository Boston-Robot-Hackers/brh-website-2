# TF22 Meetings page as a tighter card grid for Feature F22
**Date Created:** 2026-11-05

## TF22.0 — Approve the layout
**Status**: done

**Description**: The user chose the layout from a prototype on 2026-11-05: main meeting cards with date boxes and blurbs, a hands-on line, a line of to-be-announced dates, the existing banner, and higher-contrast cards.

**Test**: not feasible, this is a user decision.

## TF22.1 — Add the `blurb` field
**Status**: done

**Description**: Allow an optional `blurb` in `build/calendar_source.py`, and add the 16 approved blurbs to `content/calendar.yaml`. Document the field in `README.md`.

**Test**: an entry with `blurb` loads with it, one without still loads, and the home page and feed output are unchanged.

## TF22.2 — Give the template its card data
**Status**: done

**Description**: Extend `calendar_sections` in `build/page_builder.py` to drop hands-on meetings, split out main meetings with no topic, and give each card its announcement `image` and its blurb, falling back to `text`.

**Test**: hands-on meetings are excluded, a meeting with no topic is split out, a card gets the announcement image, and a card with no `blurb` gets `text`.

## TF22.3 — Build the card and page templates
**Status**: done

**Description**: Rewrite `templates/components/calendar-entry.html` as the card, and update `templates/pages/meetings.html` with the hands-on line, the to-be-announced line and the grids. Keep the `<article id=...>` anchor on cards, and give each to-be-announced date its own anchor. Add the hands-on wording to `config/site.json`.

**Test**: rendered cards show image, date box, title, speaker and blurb and link to the announcement. The hands-on line appears, and each to-be-announced date has its anchor.

## TF22.4 — Style the page
**Status**: done

**Description**: Replace the `.calendar-entry` rules in `css/main.css` with the responsive grid, 16:9 image crop, date box, title and blurb line limits, and page-scoped card colors for both themes. Keep the `:target` highlight and the scroll margin that clears the sticky header.

**Test**: not feasible for appearance, so the user checks it in TF22.6. `tests/test_css_theme.py` still has to pass.

## TF22.5 — Write the feature's tests
**Status**: done

**Description**: Add the tests from TF22.1 to TF22.3 to `tests/test_calendar_source.py`, `tests/test_page_builder.py` and `tests/test_meetings_content_preserved.py`.

Change `test_every_meeting_has_an_anchored_entry` to expect main meetings only, and make `test_meeting_links_resolve_to_calendar_anchors` accept the to-be-announced anchors.

**Test**: `uv run pytest` passes in full, and every `meetings.html#` link in `meetings.ics` and `upcoming-talks.txt` lands on a real anchor.

## TF22.6 — Check it in a browser
**Status**: done

**Description**: Run the F22 demo at laptop and phone widths in both themes. Check every image crop, and adjust the crop position if faces or labels are cut off.

**Test**: not feasible to automate, so the user signs off on how it looks.
