# F17 — iCalendar feed of meetings
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Build `output/meetings.ics`, a standards-compliant (RFC 5545) iCalendar feed.
  * Served at `https://bostonrobothackers.com/meetings.ics`.
  * People subscribe once (Google Calendar "From URL", Apple Calendar, Outlook) and new meetings appear automatically.
  * The second use case alongside F11's `upcoming-talks.txt`: that one is for pasting into emails, this one is for calendars.

**Which meetings**:

* **All main meetings, past and future. No hands-on meetings.**
* Past meetings stay in the feed so subscribers' calendars keep their history instead of events vanishing.
* TBA meetings are included; they update in place once a speaker is added.

**Per-event fields**:

* `SUMMARY`:
  * Talk (has `speaker` + `topic`): `Boston Robot Hackers: <topic> (<speaker>)`.
  * Main meeting without a talk yet: `Boston Robot Hackers monthly meeting`.
* `DESCRIPTION` = the meeting's `text`, plus the details URL.
* `LOCATION` = `location`. `URL` = same announcement-or-meeting-page rule as F11.
* `DTSTART` from `date` + `time`, in `America/New_York`, with a `VTIMEZONE` block.
* `DTEND` = start + a **new config key `meeting_duration_minutes`** (120) — content has no end time; all main meetings are 7:00pm, so events run 7:00–9:00pm.
* `UID` = `<meeting-id>@bostonrobothackers.com`.
  * **Must stay stable** — it's how calendar clients update an event in place instead of duplicating it.

**Well-formedness** (the reason this isn't a pure template):

* The Jinja template holds the calendar structure.
* Python handles the RFC 5545 mechanics a template can't do reliably:
  * **Escaping** `\`, `;`, `,`, and newlines in text values (a Jinja filter).
  * **CRLF** line endings.
  * **Line folding** at 75 octets (UTF-8 safe — the em dashes in `text` are multi-byte).
* `time` must match `H:MMam/pm`; anything else raises, naming the file.

**Non-goals**:

* No per-meeting `.ics` download buttons on the site.
* No nav link. The only UI is two tiny `TXT` / `iCal` links beside the home page's "Upcoming Meetings" heading (added 2026-09-21 at the user's request; `TXT` points at F11's `upcoming-talks.txt`).
* No hands-on meetings.
* No recurrence rules (`RRULE`) — every meeting is an explicit event.

## How to Demo
**Setup**: `make try`.

**Steps**:
1. Open `http://localhost:8000/meetings.ics` — it downloads/shows the calendar.
2. Import the file into a calendar app; meetings show at the right local times.
3. After deploy, subscribe to `https://bostonrobothackers.com/meetings.ics` in Google Calendar.

**Expected output**: every meeting appears once, at the correct Boston-local time, with location and a working details link; re-subscribing after a content change updates events rather than duplicating them.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
