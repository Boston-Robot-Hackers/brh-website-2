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
