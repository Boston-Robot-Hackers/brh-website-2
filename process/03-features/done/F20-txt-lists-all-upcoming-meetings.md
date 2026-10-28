# F20 — upcoming-talks.txt lists every upcoming meeting
**Priority**: Medium
**Date Created:** 2026-10-28
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**: Make `upcoming-talks.txt` list **every** future meeting, not just confirmed talks. That covers main meetings without a speaker yet and every hands-on meeting. This reverses F11's "confirmed talks only, no hands-on" rule.

## Why

- The file exists to paste into emails so other groups can put our meetings on their calendars. Leaving out TBA and hands-on dates hides real meetings people could attend.
- As of 2026-10-28 it lists 1 meeting, though 10 future meetings are scheduled (5 main, 5 hands-on).

## Scope

- **Which meetings**: every meeting dated today or later, both kinds, soonest first. That's the same set as `get_future_meetings(today)`.
- **Query**: `ContentManager.get_upcoming_talks(today)` becomes **`get_upcoming_meetings(today)`**. Each item gains `kind`, and `speaker`/`topic` are `None` when they aren't set.
- **One block per meeting, in three shapes** (the template picks one by kind and whether a talk is set). **The user rewrote the wording** after the first draft; this is what shipped:
  - **Confirmed talk** (main, with `speaker` + `topic`): "*Month* Main Club Meeting", When, Where, Speaker, Topic, the `text` summary, and a "More info" URL.
  - **TBA main**: "*Month* Main Club Meeting", When, Where, "Speaker: TBD", "Topic: TBD".
  - **Hands-on**: "*Month* Hands-on meeting: Smaller, without an agenda or a speaker. Don't publicize.", When, Where. It has no blurb, because the user dropped the default text from this block.
  - The register and full-schedule lines were dropped, so the build no longer requires `registration_url`.
- **Header**: "Upcoming Talks" becomes **"Upcoming Meetings"**.
- **Filename and URL unchanged**: it stays `upcoming-talks.txt`, because the URL may already be shared and the home and meetings pages link to it. The link tooltips ("Upcoming talks as plain text") change to "Upcoming meetings as plain text".

## Out of scope

- `meetings.ics` stays as it is: main meetings only.
- No renaming the file.
- No new calendar fields.

## How to Demo
**Setup**: `uv sync`.

**Steps**:
1. `uv run python build/build.py`.
2. `cat output/upcoming-talks.txt`.

**Expected output**:

- One block for every meeting from today on, soonest first, hands-on included.
- The Nov 12 talk reads as before.
- The Dec 10 main meeting shows "Speaker: TBD" and "Topic: TBD".
- Each hands-on meeting shows the hands-on line, When and Where.
- The build prints `Built upcoming-talks.txt with N meetings`, where N matches the number of future entries in `content/calendar.yaml`.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
