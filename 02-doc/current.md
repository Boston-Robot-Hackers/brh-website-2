# Current

## 2026-08-19 (F01 done)
- Executed all 7 TF01 steps for F01 (dark/light mode correctness).
  `css/shared.css`: added a `prefers-color-scheme: dark` block with a
  symmetric slate-scale flip for the 7 neutral variables + 4 shadows;
  brand/accent colors left unchanged (confirmed only used on self-contained
  fills). `templates/layouts/base.html`: inline script syncs
  `data-bs-theme` with system preference before first paint — confirmed
  necessary since 17 templates use Bootstrap's theme-aware `.card`
  component. `css/main.css`: converted the 10 real light-mode-only hex
  colors (meeting-card component) to variables; left 3 bespoke-dark-chrome
  colors hardcoded. Fixed 3 template bugs (`section.html`'s `text-dark`,
  `member-detail.html`'s `bg-light text-dark` badge,
  `news-card.html`'s `border-dark`) using Bootstrap's theme-aware
  equivalents.
- Added `tests/test_css_theme.py` (3 tests). `uv run pytest` — 72 passed.
- Manual visual verification **not done** — no browser tool available in
  this environment. Did a thorough static check instead (confirmed
  `data-bs-theme` + dark CSS block present across all page types in built
  output, no leftover bad classes). Recommend the user spot-check visually
  before considering this fully verified.
- F01 and TF01 marked Done/Tests Written/Test Passing: yes, still sitting
  in `notdone/` (not moved to `done/` — say the word if you want that).

## 2026-08-19 (F01 follow-up: real rendering found a cascade bug, added a toggle)
- User reported dark mode looked "ugly" and asked me to actually look at
  it. Got Playwright working (isolated scratch npm install, no
  `package.json` in this repo) and screenshotted real pages in both modes.
  Found the actual bug: `templates/components/head.html` loaded Bootstrap's
  CSS *after* `shared.css`/`main.css`, so Bootstrap's own `body`/`.card`
  rules won the cascade tie and silently used Bootstrap's default dark gray
  (`#212529`) instead of our palette (`#0f172a`) — in both modes, only
  obviously wrong in dark mode. Fixed by reordering `head.html`. This is
  the kind of bug static analysis/grepping can't catch — needed a rendered
  page.
- User then asked for a manual light/dark toggle (reversing F01's original
  system-preference-only non-goal). Implemented: switched
  `css/shared.css`'s dark block from a `prefers-color-scheme` media query
  to the `:root[data-bs-theme="dark"]` attribute selector; `base.html`'s
  inline script now checks `localStorage` first; added a toggle button to
  the nav bar (`components/navigation.html` + `.theme-toggle-btn` in
  `main.css` + click handling in `script.js`). Verified interactively with
  Playwright (click → attribute flips → survives reload even with OS still
  emulated light).
- Added a regression test locking in the cascade-order fix
  (`test_bootstrap_css_loads_before_custom_css`). `uv run pytest` — 73
  passed. F01/TF01 docs updated with both additions as TF01.2's follow-up
  note and a new TF01.7. Not yet committed.

## 2026-08-19 (removed image-swapping feature)
- Removed the hand-drawn/photo swap mechanism entirely, per user request to
  keep only the photo images: deleted `scripts/set-images.sh` and all of
  `image-sources/` (handdrawn/, photo/, an unused posters/ source, and its
  README). Confirmed `images/news/`'s 10 swap-set files were already the
  photo versions (verified by hash against the old image-sources/photo/
  before deleting it) — no image content changed, just the swap capability
  and its unused source files removed. Updated README.md's Project
  Structure tree to drop the swap-mechanism mentions.
- `uv run pytest` — 69 passed, full rebuild clean.

## 2026-08-19 (F02 closed)
- F02 (codebase structure & consistency review) confirmed done: all 7 TF02
  steps done, `uv run pytest` — 69 passed. Moved
  `03-features/notdone/F02-structure-review.md` -> `03-features/done/` and
  `04-tasks/notdone/TF02-structure-review.md` -> `04-tasks/done/`.
- F01 (dark/light mode correctness) remains open in notdone/ — not started.

## 2026-08-19 (images/ cleanup)
- Reorganized images/: deleted 11 orphaned/unreferenced files (Skill.png,
  demo.png, banner-1.png, kalman.png, Robot.png, hardware.png, Network.png,
  projects/midi_blinky.png, projects/pupper_white.jpg, meetings/meeting1.MOV,
  meetings/meeting1-2.jpeg); moved 3 loose-but-real root files (team.png,
  kalman3.png, people.png) into images/news/ to match their content type;
  renamed images/people/ -> images/members/ to match content/members/.
  Updated all cross-references (14 member files' `image:` field, 5 news
  posts).
- Follow-up: also moved the 10-file documented swappable image set (was
  loose at images/ root) into images/news/, since every reference to them
  is from content/news/*.md. Updated scripts/set-images.sh (now writes to
  images/news/) and image-sources/README.md. images/ root now contains only
  the 4 content-type subdirectories, nothing loose.
- Found but did NOT fix (out of scope, flagged to user): images/robot-logo.png
  referenced by templates/components/head.html's preload link doesn't exist
  anywhere in the repo — pre-existing, unrelated to this cleanup.
- Verified: full image-reference resolution scan across all built output
  HTML — zero broken references introduced. `uv run pytest` — 69 passed.
  Not yet committed/pushed.

## 2026-08-19 (chores applied)
- Applied all 16 chores: the 8 pre-existing build/*.py style-guide items plus
  the 8 chores from F02's structure-review findings.
- Content renames: content/members/member_template.md -> pito-salas.md,
  content/projects/project_template.md -> dome-robot.md (both held real live
  content, not templates); 9 other content/members/ files standardized to
  lowercase-hyphens; 3 content/news/ underscore files renamed to hyphens.
  Fixed cross-refs in adam-ring.md, pito-salas.md, and the Dec meeting
  summary news post. Added content/{members,projects}/_template.md as real
  blank scaffolds, excluded from the build via a leading-underscore
  convention in content_manager.py's get_all_content.
- Removed legacy/ (incl. a git-tracked node_modules/), archive/build.py, and
  the dangling rules.md symlink. Created 05-issues/{open,closed,deferred}/.
  Updated README.md's Project Structure tree (image-sources/, scripts/).
- build/*.py: moved hero HTML generation into a new Jinja template
  (templates/components/upcoming-meetings-hero.html), extracted a shared
  resolve_announcement_report() helper (was duplicated 3x in page_builder.py),
  deleted dead code, fixed import placement/shadowing, added file
  headers/shebangs, fixed a type hint and an indentation bug, wrapped all
  lines over 88 chars.
- Tests: `uv run pytest` — 69 passed (added tests for the leading-underscore
  exclusion and the new resolve_announcement_report helper). Full site
  rebuild verified: same page counts as before, all renamed URLs resolve,
  cross-links updated correctly.
- Not yet committed or pushed.

## 2026-08-19
- Completed F02 (codebase structure & consistency review): all 7 TF02 steps
  done. Findings written up in `02-doc/structure-review.md` — 8 numbered
  issues, ordered by priority, each with proposed change and disposition
  (all chore-sized). Headline finding: `content/members/member_template.md`
  and `content/projects/project_template.md` aren't templates — they hold
  Pito Salas's real live profile/project and are published under
  template-looking URLs.
- Added a regression guardrail test (`tests/test_docs_integrity.py`):
  asserts every `.claude/`-relative file referenced from `CLAUDE.md`
  actually exists. `uv run pytest` — 66 passed.
- None of the review's proposed changes have been applied yet — they're
  queued for the user to pick up (as chores, most bundled with finding 1's
  content renames).

## 2026-07-30
- Reviewed build/*.py (build.py, content_manager.py, page_builder.py, asset_manager.py, news_links.py) against .claude/style_guide.md.
- Findings recorded as 8 numbered chores in 04-tasks/chores.md, not yet applied.
- No code changes made yet — chores are pending pickup.
- Tests: `uv run pytest` — 65 passed.
- Working tree still has pre-existing uncommitted .claude/ restructuring (codereview.md/how_to_be.md/CLAUDE.md/method.md deleted, replaced by process.md/style_guide.md; several other .claude files modified) predating this session — deliberately left uncommitted per user choice, not part of this checkpoint's commit.
