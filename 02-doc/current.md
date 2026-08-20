# Current

## Open

Backlog is empty — `03-features/notdone/` and `04-tasks/notdone/` have
nothing pending. Nothing is in progress.

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

See `02-doc/history.md` for the completed-work log.
