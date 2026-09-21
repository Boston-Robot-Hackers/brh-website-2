# Current

## Open

**Reminder: clean up after abandoned F10 (pupper subdomain)**. Two external
leftovers need manual cleanup:

* Delete (or archive) the GitHub repo `Boston-Robot-Hackers/brh-pupper-redirect`.
* In Namecheap Advanced DNS for `bostonrobothackers.com`, delete the
  `pupper` CNAME record (→ `boston-robot-hackers.github.io.`).

**Speakers to confirm**: the 4 monthly meetings from Dec 2026 to Mar 2027
(`28-meeting.md`, `30-meeting.md`, `32-meeting.md`, `34-meeting.md`) still
say "Speaker and topic to be announced."

* When a speaker is confirmed, fill in `text`, `announcement`, **and
  `speaker` + `topic`**. A talk only appears in `upcoming-talks.txt` and
  gets a named `meetings.ics` event once both are set.

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
* `pyproject.toml`'s `[tool.uv] dev-dependencies` field is deprecated by
  `uv` in favor of `[dependency-groups] dev` — a cosmetic warning on every
  `uv` invocation, not urgent.
* `build/build.py` (~405 lines), `build/content_manager.py` (~390), and
  `build/page_builder.py` (~390) are over the style guide's ~300-line
  guideline. The literate docs' closing observations suggest where to split.

See `process/02-doc/history.md` for the completed-work log.
