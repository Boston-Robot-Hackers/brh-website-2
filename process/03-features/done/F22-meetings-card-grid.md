# F22 — Meetings page as a tighter card grid
**Priority**: Medium
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Redesign `meetings.html` from a single column of long entries to a tighter grid of cards.
* Images and titles become the most prominent parts, and more meetings fit on screen at once.
* The layout was chosen by the user from a working prototype.

**Layout**:

* Main meetings with a topic are cards in a grid: 5 columns wide, 3 at tablet width, 2 at phone width.
* Each card shows a 16:9 image, a date box over its corner (month, day, year), title, speaker and blurb.
* The Upcoming and Past sections stay. Upcoming is soonest first and Past is newest first.
* The banner, intro text and page header stay as they are. **The prototype's shorter banner was rejected.**

**Hands-on meetings**:

* **Hands-on meetings no longer appear individually on this page.**
* One line under the header replaces them: "Hands-on meetings: second Wednesday, 6:00pm." The wording lives in `config/site.json`.
* Their dates remain on the home page, `meetings.ics` and `upcoming-talks.txt`.
* Their feed events link to the hands-on news post, so removing them from this page breaks no feed link.

**Meetings with no topic yet**:

* These show as a single line of dates above the Upcoming grid, currently Feb 11 and Mar 11, 2027, instead of empty cards.
* **Each date keeps its `meetings.html#<id>` anchor.** `meetings.ics` and `upcoming-talks.txt` link there for main meetings with no announcement.

**Images**:

* **No new image field.** A card uses the `image` of the meeting's linked announcement.
* A card with no announcement image shows the date box in the card body, with no image block.

**New `blurb` field**:

* Add an optional `blurb` to meetings in `content/calendar.yaml`, about 120 characters, saying what the talk is about.
* A card shows `blurb`. With none, it shows `text`, limited to 4 lines.
* **`text` is unchanged** and stays in use by the home page, `upcoming-talks.txt` and `meetings.ics`.
* Add the 16 blurbs the user approved on 2026-11-05.

**Card details**:

* Titles are limited to 3 lines, with the full title as a tooltip.
* Each card links to its announcement, and a meeting with a report keeps its "Notes from the meeting" link.
* Card backgrounds and borders contrast more with the page: `#2a2722` in dark theme and `#f1eee2` in light.
* **The new colors apply to this page's cards only**, not to `--bg-card` across the site.

**Must not change**:

* Each main meeting keeps its `meetings.html#<id>` anchor.
* The header note and the iCal and TXT links stay.

**Non-goals**:

* No filtering, search, or client-side pagination.
* No change to the home page's meeting rail, `meetings.ics` or `upcoming-talks.txt`.
* No new or replacement images. Three past meetings share `clock.png`, and the date box covers part of the kinematics diagram's heading. Both are separate content edits.

## How to Demo
**Setup**: `make try`.

**Steps**:

1. Open `http://localhost:8000/meetings.html` at laptop width, in dark and light themes.
2. Narrow the window to phone width.
3. Open `http://localhost:8000/meetings.html#34-meeting`.

**Expected output**:

* Main meetings appear as a 5-column grid of cards that stand out from the page, each linking to its announcement.
* The hands-on line appears under the header, and no individual hands-on meetings appear.
* The grid drops to 2 columns at phone width, with no horizontal scrolling.
* The anchor link scrolls to and highlights Mar 11, 2027 in the line of dates.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
