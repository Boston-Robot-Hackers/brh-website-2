# Current

## Open

**Reminder: clean up after abandoned F10 (pupper subdomain)**. Two external
leftovers need manual cleanup (design record in
`process/03-features/deferred/F10-pupper-subdomain-redirect.md`):

* Delete (or archive) the GitHub repo `Boston-Robot-Hackers/brh-pupper-redirect`.
* In Namecheap Advanced DNS for `bostonrobothackers.com`, delete the
  `pupper` CNAME record (→ `boston-robot-hackers.github.io.`).

**Speakers to confirm**: the 4 main meetings from Dec 2026 to Mar 2027
(2026-12-10, 2027-01-14, 2027-02-11, 2027-03-11) have no speaker yet, so
they show the "Speaker and topic to be announced." default, and "TBD" in
`upcoming-talks.txt`.

* When a speaker is confirmed, edit that entry in `content/calendar.yaml`:
  add `speaker`, `topic`, `text`, and `announcement`. Once both `speaker`
  and `topic` are set, `upcoming-talks.txt` names them and `meetings.ics`
  gets a named event.

**Open features (none started)**: F12 (build as a real package), F13 (unify
CI/local build invocation), F14 (reduce page-builder boilerplate), F15
(remove inline styles), F16 (robust root-dir detection). None has a task
file yet.

Known, deliberately-deferred items (not urgent, no ticket filed):

* 3 ruff `DTZ` (naive-datetime) findings, left unfixed: `datetime.now()`
  and `datetime.min` in `build/content_manager.py`, `date.today()` in
  `build/page_builder.py`. The site only ever needs one local timezone
  (the group's own meetup "today"), so naive local dates are correct as
  written — forcing tz-awareness would be a real behavior-risk change with
  no matching `.claude/style_guide.md` rule, not a mechanical lint fix.
* `build/build.py` (~405 lines), `build/content_manager.py` (~345), and
  `build/page_builder.py` (~320) are over the style guide's ~300-line
  guideline. The literate docs' closing observations suggest where to split.

See `process/02-doc/history.md` for the completed-work log.
