# Current

## Open

**Reminder: clean up after abandoned F10 (pupper subdomain)**. Two external
leftovers need manual cleanup (design record in
`process/03-features/deferred/F10-pupper-subdomain-redirect.md`):

* Delete (or archive) the GitHub repo `Boston-Robot-Hackers/brh-pupper-redirect`.
* In Namecheap Advanced DNS for `bostonrobothackers.com`, delete the
  `pupper` CNAME record (→ `boston-robot-hackers.github.io.`).

**Nov 11 hands-on meeting**: moved from Nov 25 on 2026-11-04, and it falls on
Veterans Day. Confirm the space is open and let members know.

**Dec 10 announcement**: Addisu Taddese is the speaker. "Robotics in the Real
World" is a working title until confirmed.
`content/news/30-december-talk-announcement.md` is no longer hidden. Its
lightning talks are still TBD.

**Jan 14 announcement**: Tully Foote on Intrinsic Core.
`content/news/31-january-talk-announcement.md` is published with Tully's
headshot. Its lightning talks are still TBD.

**Speakers to confirm**: the 2 main meetings on 2027-02-11 and 2027-03-11 have
no speaker yet, so they show the "Speaker and topic to be announced." default,
and "TBD" in `upcoming-talks.txt`.

* When a speaker is confirmed, edit that entry in `content/calendar.yaml`:
  add `speaker`, `topic`, `text`, and `announcement`. Once both `speaker`
  and `topic` are set, `upcoming-talks.txt` names them and `meetings.ics`
  gets a named event.

**Speaker page follow-ups**: `content/pages/speaker-tips.md` is now an FAQ,
and these are still open:

* The page title is "FAQ For Speakers", but the link at `content/about.md:33`
  still says "Tips for Speakers". The filename and URL stay `speaker-tips`,
  by the user's decision.
* Typos: "bstract", "When are the meetings ?", a stray colon after "What info
  do you need from the speaker?", and "which I need those in order to".
* The "Title of the talk" list is indented four spaces, so it probably renders
  as a code block. Rendered output not checked.

**Open features (none started)**: F12 (build as a real package), F13 (unify
CI/local build invocation), F14 (reduce page-builder boilerplate), F15
(remove inline styles), F16 (robust root-dir detection). None has a task
file yet.

**HTML and CSS cleanup**: what remains from the 2026-11-05 audit,
in the recommended order:

* Tidy templates: planned as F28, parked and awaiting the user's go. Its feature
  and task files are in `notdone/`.
* Replace inline image styles in content files. F15 is out of date and should be
  rewritten around this. It also removes the `!important` F24 added.

**Tests overwrite local output**: `tests/test_upcoming_talks.py` and
`tests/test_ical_feed.py` build into the real `output/`, so running the tests
leaves test data (dated 2026-09-18) in `output/upcoming-talks.txt` and
`meetings.ics`. Deploys aren't affected, since CI builds without running tests.
Rebuild after testing locally. Same kind of bug as chore 43; not fixed yet.

**ROSbot pages after F27**: the F26 templates were moved onto F27's shared
classes during the merge. Their HTML was checked, not their look in a browser.

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
