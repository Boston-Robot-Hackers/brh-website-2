# Current

## Open

**Ruff rules made portable via `.claude/` bootstrap (2026-09-05)** — the
calibrated ruff `select` list adopted in commit 6b44ffa (`pyproject.toml`)
is now also captured as `.claude/templates/ruff.toml.template`, a
standalone `ruff.toml` that `/bootstrap` copies as-is into a new project
(see updated `.claude/bootstrap.md` and `.claude/process.md`). No changes
to this repo's own `pyproject.toml` — it keeps its embedded
`[tool.ruff.lint]` config unchanged. `.claude/style_guide.md` (v3.3) now
annotates each checklist line with `[ruff: CODE]` / `[ruff: partial — ...]`
markers showing which rules are mechanically enforced vs. still
manual-review-only. Also fixed a stale `.claude/process.md` reference to
a nonexistent `.claude/codereview.md` (the real file is
`.claude/style_guide.md`) — same stale name reappeared in this session's
`/checkpoint` invocation; substituted `style_guide.md` since no Python
source changed this session, so no MUST/SHOULD review was applicable.
All template text was scrubbed of `brh-website-2`-specific wording per
user request, except `.claude/settings.json`'s `autoMode.environment`
block, which legitimately describes this project and isn't part of the
bootstrap-copied template set.

**F10 — pupper.bostonrobothackers.com subdomain over HTTPS** — on hold
awaiting user to configure custom domain in GitHub Pages settings for
`brh-pupper-redirect` repo (TF10.4, TF10.5). See history entry 2026-09-04
for details. HTTP version working; HTTPS cert not yet issued by GitHub.

**PDF asset delivery (2026-09-04)** — Fixed: meeting-reports directory
was not being copied during build, causing 404 on PDF downloads in
meeting announcements. Updated `build/asset_manager.py` to copy
`content/meeting-reports/` to `output/meeting-reports/`. All tests
passing (131/131). Deployed to production; full link verification
confirms all pages, assets, and PDF downloads working correctly.

Meeting schedule content is now filled in through March 2027 (10 new
`content/meetings/*.md` entries, chore-level content update, no
feature/task — see `02-doc/history.md` 2026-08-27 entry). The 4 monthly
meetings from Dec 2026–Mar 2027 have no speaker yet (`text: "Speaker and
topic to be announced."`); fill in `text`/`announcement` on
`28-meeting.md`, `30-meeting.md`, `32-meeting.md`, `34-meeting.md` as
speakers are confirmed.

The site's full visual redesign (F04 concept exploration, F05 real
implementation of Option D) is merged into `main` (commit 432757f).
Redesign is complete.

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
* `ruff` is not a project dependency (no entry in `pyproject.toml`); this
  session ran it via `uvx ruff` instead. Worth adding as a real dev
  dependency at some point so `uv run ruff` works directly.
* `01-literate/` has never actually been populated in this repo despite
  `.claude/process.md`'s "regenerate literate docs before committing"
  rule — confirmed via `git log` (no file has ever existed there).
  `build/content_manager.py`, `build/page_builder.py`, and `build/build.py`
  have all changed since (most recently for F09) with no literate docs
  generated for any of them. Deliberately skipped per user decision
  (2026-08-20) rather than starting a first-pass doc-gen project
  unprompted during a routine checkpoint.

See `02-doc/history.md` for the completed-work log.
