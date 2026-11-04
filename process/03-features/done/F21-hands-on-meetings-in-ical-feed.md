# F21 — Hands-on meetings in the iCalendar feed
**Priority**: Medium
**Date Created:** 2026-11-04
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Add hands-on meetings to `output/meetings.ics`, so subscribers see every meeting on the calendar page.
* **This reverses F17's "No hands-on meetings" decision.** F17's other feed rules still apply.

**Which meetings**:

* **All meetings of both kinds, past and future.**
* Past hands-on meetings are included, matching F17's rule that past meetings stay in the feed.

**Per-event fields**:

* `SUMMARY` for a hands-on meeting: `Boston Robot Hackers hands-on meeting`.
* `SUMMARY` for a main meeting: unchanged.
* `DTEND` = start + the existing `meeting_duration_minutes` (120), so hands-on events run 6:00–8:00pm.
  * **No separate hands-on duration setting.**
* `DESCRIPTION`, `LOCATION`, `URL`, and `DTSTART` follow F17's rules, using each entry's values or the `handson` defaults in `content/calendar.yaml`.

**Subscriber impact**:

* `UID`s stay `<meeting-id>@bostonrobothackers.com`, so **existing events update in place**.
* The hands-on meetings appear as new events.

**Non-goals**:

* No separate feeds per meeting kind.
* No change to `upcoming-talks.txt`, which already lists both kinds.
* No site UI changes.

## How to Demo
**Setup**: `make try`.

**Steps**:

1. Open `http://localhost:8000/meetings.ics`.
2. Find the Nov 11, 2026 event.
3. Import the file into a calendar app and check both a main and a hands-on meeting.

**Expected output**:

* The Nov 11 event is titled `Boston Robot Hackers hands-on meeting` and runs 6:00–8:00pm Boston time.
* Main meetings are unchanged.
* The feed has one event per entry in `content/calendar.yaml`.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
