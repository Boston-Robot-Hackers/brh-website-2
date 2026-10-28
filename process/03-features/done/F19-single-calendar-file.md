# F19 — Single calendar file and full calendar page
**Priority**: Medium
**Date Created:** 2026-10-27
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Replace the 35 `content/meetings/*.md` files with one hand-edited file, `content/calendar.yaml`, as the single source of truth for the meeting schedule. Turn `meetings.html` into a full calendar page that shows every meeting's details inline, and drop the per-meeting detail pages.

## Why

- Today a schedule change means finding and editing the right numbered `.md` file, and the schedule was also tracked in a separate Google Sheet ("Meeting Schedule"). The two had drifted, e.g. the Jan 2027 main meeting date.
- One file makes the whole schedule visible and editable in one place, reviewable in `git diff`.

## Scope

- **New source file**: `content/calendar.yaml` with a `defaults` block (location, per-kind time, hands-on text) and a `meetings` list. An entry needs only `date` and `kind`; `speaker`, `topic`, `text`, `title`, `announcement`, `report` are optional overrides.
- **Stable ids**: every migrated entry keeps its current id (`24-meeting`, `27-handson-meeting`, ...) via an explicit `id:` field, because `meetings.ics` derives event UIDs from it. Changing a UID would duplicate events in subscribers' calendars. New entries without `id:` get one derived from the date and kind.
- **One loader**: `load_meetings()` and the generic content-type path both read `calendar.yaml`. Hero, `upcoming-talks.txt`, `meetings.ics`, whatsnew's meeting column and the home page calendar consume the same data as before.
- **Calendar page**: `meetings.html` lists upcoming meetings, then past ones, each with date, time, kind, speaker/topic and blurb, linking to its announcement and report where present. It also shows the `.ics` subscribe link. Each meeting is an anchor (`meetings.html#<id>`).
- **Detail pages removed**: no more `meetings/<id>.html`. Links that fell back to a detail page now go to `meetings.html#<id>`. That covers the monthly meeting cards, `meeting_page_path()` and the `.ics` event URL.
- **Migration**: a one-off conversion of the 35 files into `calendar.yaml`, then delete `content/meetings/` and `templates/details/meeting-detail.html`. Fix the Jan 2027 main meeting to **2027-01-14** in the same pass.
- **Sheet retired**: the build never reads the Google Sheet. The user retires it by hand.

## Out of scope

- Redirects for old `meetings/<id>.html` URLs (GitHub Pages has no server-side redirects; old links 404).
- Filling in the TBD speakers for Dec 2026 – Mar 2027.

## How to Demo
**Setup**: `uv sync`.

**Steps**:
1. Edit one entry in `content/calendar.yaml`, e.g. add a `speaker`, `topic` and `text` to the 2026-12-10 meeting.
2. `uv run python build/build.py`.
3. Open `output/meetings.html`, `output/index.html`, `output/upcoming-talks.txt`, `output/meetings.ics`.

**Expected output**:

- `meetings.html`, `upcoming-talks.txt` and `meetings.ics` show the new speaker and topic.
- `index.html`'s upcoming-meetings rail shows the new `text` (it displays only date, time and text).
- `meetings.html` shows the full schedule with details inline, and `output/meetings/` doesn't exist.
- Existing `.ics` UIDs are unchanged.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
