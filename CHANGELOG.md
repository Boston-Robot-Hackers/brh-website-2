# Changelog — Deep Dive Session (branch `deepdive`)

Full-codebase review of `build/` (Python) and `scripts/` + inline template
JavaScript, looking for dead code, bugs, and duplication. Every change below
was followed by a full `uv run pytest` run and a full `uv run python
build/build.py`; the site was also spot-checked with a local HTTP server
(link check across all main pages, news detail, meeting detail, PDF asset,
CSS, and images) after the changes landed. No behavior regressions found —
test suite stayed green throughout (133/133 before and after).

## Scope reviewed

| Area | Files | Lines |
|---|---|---|
| Python (`build/`) | 5 files: `build.py`, `page_builder.py`, `content_manager.py`, `asset_manager.py`, `news_links.py` | ~1,185 |
| Python (`tests/`) | 19 test files | — |
| JavaScript | `scripts/script.js` + 2 inline `<script>` blocks (`templates/layouts/base.html`, `templates/pages/meetings.html`) | ~130 |
| Templates | all `templates/**/*.html` (checked for orphaned/unused files) | — |

## Bugs fixed

1. **Meetings page sort toggle was a one-way switch** (`templates/pages/meetings.html`).
   Switching the "Sort" dropdown to *Earlier → Later* reversed the DOM order
   in place with no memory of the original order. Switching back to
   *Later → Earlier* then did nothing, because the code only had an `if
   (sortOrder.value === 'earlier-first')` branch and no corresponding
   restore step — the list stayed reversed. Fixed by snapshotting the
   rendered (newest-first) order once on load and always recomputing the
   displayed order from that fixed snapshot, so toggling is now reversible
   in both directions.

2. **Meetings filter only checked one of two dates per month card**
   (`templates/pages/meetings.html`). A month card can contain both a Main
   Meeting and a Hands-On Meeting, each with its own `.meeting-entry__line`
   date. The Upcoming/Passed filter used
   `card.querySelector('.meeting-entry__line')`, which only ever returns the
   *first* match — so a card's passed/upcoming status was decided solely by
   whichever meeting happened to render first, ignoring the other one. Fixed
   so a card counts as "upcoming" if *either* meeting inside it hasn't
   happened yet.

## Dead code removed

3. **3 unused JavaScript functions** (`scripts/script.js`): `loadMoreNews()`,
   `loadMoreProjects()`, `loadAllMembers()` — each just an `alert()`
   placeholder, never wired to any button, link, or `onclick` anywhere in
   the templates. Confirmed via full-repo grep before removal.

4. **2 unused dict fields** in `PageBuilder.render_upcoming_meetings_calendar`
   (`build/page_builder.py`): `title` and `month_year` were computed for
   every upcoming meeting but never read by
   `components/upcoming-meetings-calendar.html`, the only template that
   consumes this data.

## Duplication removed

5. **Duplicate news-index caching logic**, implemented separately (but
   identically) in `ContentManager.resolve_news_html` and
   `PageBuilder.news_html_name` — both had their own `_news_map = None` +
   lazy-build-on-first-call pattern wrapping the same `build_news_index()` /
   `resolve_news_html()` calls from `news_links.py`. Consolidated into a
   single `NewsResolver` class in `news_links.py` that both `ContentManager`
   and `PageBuilder` now hold an instance of. Also removed a third,
   separately-computed copy of the `content/news` path used only for
   `extract_slides_pdf()` in `resolve_announcement_report` — now reuses
   `self._news_resolver.news_dir`.

6. **Duplicate sort branches** in `ContentManager.get_all_content`
   (`build/content_manager.py`): the `"date"` and `"published_date"` sort
   cases were nearly line-for-line identical (introduced in the same
   session, just before this deep dive, when `published_date` sorting was
   added for news). Merged into one branch keyed by field name. This also
   fixed a `ruff` `E501` (line too long) violation and dropped
   `get_all_content`'s cyclomatic complexity from 11 back under the
   `C901` threshold of 10.

## Checked, not changed

- All template files (`templates/**/*.html`) were cross-referenced for
  orphaned/unused files — none found.
- All top-level and method-level Python functions in `build/*.py` were
  cross-referenced for callers (build code, tests, or templates) — none
  found unused beyond the two dict fields above.
- 5 pre-existing `ruff --select E501` line-length warnings in `tests/*.py`
  fixture strings were left alone — cosmetic only, not part of this
  session's changes, and `ruff check` (default rule set, matching the
  project's pre-commit hook) reports clean.
- The theme-toggle split between `templates/layouts/base.html` (sets
  `data-bs-theme` before paint, avoiding a flash of the wrong theme) and
  `scripts/script.js` (wires up the toggle button click) looks like
  duplication at a glance but is a deliberate, non-duplicated split — left
  as is.

## Statistics

| Metric | Value |
|---|---|
| Python files reviewed | 5 (`build/`) + 19 (`tests/`) |
| JS files/blocks reviewed | 1 file + 2 inline `<script>` blocks |
| Template files cross-checked for orphans | all of `templates/**/*.html` |
| Bugs found & fixed | 2 |
| Dead functions removed | 3 (`scripts/script.js`) |
| Dead dict fields removed | 2 (`page_builder.py`) |
| Duplicated logic blocks consolidated | 2 (news-index caching; date/published_date sort) |
| `ruff` findings fixed | 1 `E501`, 1 `C901` (complexity 11 → ≤10) |
| Net lines changed | +66 / −56 across 5 files |
| Test runs during session | continuous, after every change |
| Tests passing before session | 133 / 133 |
| Tests passing after session | 133 / 133 |
| Full-site link check (local build) | 12/12 URLs 200 OK, before and after |
| Regressions introduced | 0 |

## Files touched

- `build/content_manager.py`
- `build/news_links.py`
- `build/page_builder.py`
- `scripts/script.js`
- `templates/pages/meetings.html`

---

# Round 2 — Architecture analysis and follow-up

A broader architecture review (docs, project structure, CI, cross-module
coupling) surfaced 8 findings beyond the code-level bugs/dead-code/duplication
above. Three were fixed directly on this branch; the remaining five were
written up as features in `03-features/notdone/` for future work rather than
implemented now, per the project's own process rules (a feature file first,
then a task breakdown, then code).

## Fixed this round

1. **Documentation drift** (`README.md`). The Architecture section claimed
   `build/` has its own `pyproject.toml` and `.venv` (Python 3.13) separate
   from the root project — no longer true; there's one root `pyproject.toml`
   and `build/` is a flat module directory importable via pytest's
   `pythonpath`. The Content Files table was missing `published_date`,
   `slides_pdf`, `type` (news), `report`, `text` (meetings), and had stale
   member fields (`role`/`skills` instead of the actual `hashtags`/`website`).
   The Templates section listed a nonexistent `section.html` and omitted
   `home-lead.html`, `icons.html`, `upcoming-meetings-hero.html`. All
   reconciled against the actual code and content files.

2. **Stray local files removed**: `src/assets/images/builtin/.DS_Store` (a
   leftover, entirely unreferenced directory tree from a 2025 project
   restructure) and `build/.venv` (a 13MB orphaned virtualenv from when
   `build/` had its own `pyproject.toml`, per the now-corrected README claim
   above). Both were already untracked/gitignored — no repository diff, just
   local disk cleanup, confirmed via `git ls-files` before removal.

7. **Derived `related_report` instead of hand-maintaining it.** A meeting's
   `report:` field and its announcement's `related_report:` field encoded the
   same relationship from two directions, by hand, in two separate files,
   with nothing checking they agreed — confirmed zero references to
   `related_report` anywhere in `build/` before this change (it was read only
   by the template). Added `PageBuilder.build_related_reports_map(meetings)`,
   which derives the announcement → report link from each meeting's own
   `announcement`/`report` fields at build time. `news-detail.html` now reads
   the derived map instead of `post.metadata.related_report`; the
   hand-maintained field was removed from
   `content/news/19-june-meeting-announcement.md`. Added 4 unit tests
   (`TestBuildRelatedReportsMap` in `tests/test_page_builder.py`) plus 1
   integration test on real content (`test_announcement_links_to_its_derived_report`
   in `tests/test_whatsnew_content_preserved.py`) confirming the September 3
   meeting's announcement still links to its report after the change.

## Written up as features (not implemented)

| # | Feature file | Priority | Summary |
|---|---|---|---|
| 3 | `03-features/notdone/F11-robust-root-dir-detection.md` | Low | `WebsiteBuilder` infers the project root from `Path.cwd().name == "build"` rather than the script's own file location — works for today's two invocation styles but is fragile to any other cwd. |
| 4 | `03-features/notdone/F12-build-as-real-package.md` | Low | `build/` has no `__init__.py` and isn't a real package; modules import each other as flat top-level names via a `pytest` `pythonpath` hack and Python's script-directory-on-sys.path behavior. |
| 5 | `03-features/notdone/F13-unify-ci-local-build-invocation.md` | Low | CI's `deploy.yml` does `cd build && uv sync && uv run python build.py`; the Makefile/README do `uv run python build/build.py` from the repo root. Both work today only because `uv` walks up to find the root `pyproject.toml` — confirmed empirically. |
| 6 | `03-features/notdone/F14-reduce-page-builder-boilerplate.md` | Low | Six `build_*_page` methods in `build.py` repeat the same hero-content + banner-resolution + `build_page(...)` envelope almost verbatim. |
| 8 | `03-features/notdone/F15-remove-inline-styles.md` | Low | 6 inline `style="..."` occurrences across 3 templates bypass the otherwise-consistent CSS-variable theming system that `test_css_theme.py` enforces elsewhere. |

## Round 2 statistics

| Metric | Value |
|---|---|
| Findings from architecture review | 8 |
| Findings fixed directly | 3 (#1 docs, #2 stray files, #7 derived link) |
| Findings written up as features for later | 5 |
| New tests added | 5 (4 unit + 1 integration) |
| Tests passing before round 2 | 133 / 133 |
| Tests passing after round 2 | 138 / 138 |
| Full-site link check (local build) | 6/6 key URLs 200 OK, before and after |
| Regressions introduced | 0 |

## Files touched (round 2)

- `README.md`
- `build/build.py`
- `build/page_builder.py`
- `content/news/19-june-meeting-announcement.md`
- `templates/details/news-detail.html`
- `tests/test_page_builder.py`
- `tests/test_whatsnew_content_preserved.py`
- `03-features/notdone/F11-robust-root-dir-detection.md` (new)
- `03-features/notdone/F12-build-as-real-package.md` (new)
- `03-features/notdone/F13-unify-ci-local-build-invocation.md` (new)
- `03-features/notdone/F14-reduce-page-builder-boilerplate.md` (new)
- `03-features/notdone/F15-remove-inline-styles.md` (new)

---

# Round 3 — Style guide compliance: leading underscores

`.claude/style_guide.md` has an unconditional rule not checked in rounds 1-2:
**MUST: No leading underscore prefix on methods, functions, instance
variables, or other custom identifiers.** A full grep of `build/*.py` and
`tests/*.py` for `self._x` and `def _x` found 9 occurrences (2 distinct
names) in application code and 10 (all pytest helper functions/methods) in
tests. All renamed; call sites updated to match; `__init__`/other dunders are
a Python language feature, not a style choice, and are unaffected.

## Renamed

**`build/*.py`** (traces back to `self._news_map`, already present on `main`
before this deep-dive branch; this session's `NewsResolver` refactor carried
the underscore forward instead of fixing it):
- `self._news_resolver` → `self.news_resolver` (`ContentManager`, `PageBuilder`)
- `self._index` → `self.index` (`NewsResolver`)

**`tests/*.py`** (9 pre-existing, 1 — `_make_news_file` — added this session
alongside round 2's `build_related_reports_map` tests):
- `_real_learn_link_count` → `real_learn_link_count`
- `_real_member_file_count` → `real_member_file_count`
- `_real_meeting_file_count` → `real_meeting_file_count`
- `_real_project_file_count` → `real_project_file_count`
- `_real_news_file_count` → `real_news_file_count`
- `_frontmatter_titles` → `frontmatter_titles`
- `_make_items` → `make_items`
- `_news_item` → `make_news_item`
- `_meeting_item` → `make_meeting_item`
- `_make_news_file` → `make_news_file`

Avoiding pytest's `test_*` auto-collection only requires *not* starting with
`test_` — any other prefix works, so `make_`/`real_` names dodge collection
the same way the underscore did, without the style-guide violation.

## Round 3 statistics

| Metric | Value |
|---|---|
| Style guide MUST violations found | 19 occurrences, 12 distinct identifiers |
| Application code (`build/`) | 9 occurrences, 2 identifiers |
| Test code (`tests/`) | 10 occurrences, 10 identifiers |
| Files touched | 10 |
| Tests passing before | 138 / 138 |
| Tests passing after | 138 / 138 |
| `ruff check` / `ruff format --check` | clean, both before and after |
| Full-site link check (local build) | 5/5 key URLs 200 OK |
| Regressions introduced | 0 |
