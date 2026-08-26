# History

Completed-work log. `02-doc/current.md`'s `## Open` section is the only
part that matters for new work; entries move here once done, per
`.claude/process.md`'s checkpoint step.

## 2026-08-26 (F09 closed: per-page customizable banner)
* F09 (per-page banner image + overlay text) done, all 7 `TF09` steps.
  Optional `banner_image`/`banner_title`/`banner_subtitle` frontmatter on
  any main page's `content/heroes/<page>.md`, or any
  project/member/meeting/news item's own `.md` file, overrides that
  page's banner; unset falls back to `config/site.json`'s new
  `default_banner_image` + `site.title`/`site.subtitle` (identical to
  pre-F09 behavior).
* New `PageBuilder.resolve_banner()` resolves override-or-default and
  applies the correct relative path prefix for the page's own depth
  (`"../"` for one-level-deep detail pages, `""` for top-level pages) —
  needed because the banner image moved from a CSS-relative `url()` to
  an HTML-relative inline `style`, so path resolution now depends on
  where each page itself lives.
* `content/projects/pupper.md` carries the first real override
  (`pupper_resting.jpg` — distinct from the `pupper_standing.jpg` already
  used as the page's own thumbnail).
* Verified with a real Playwright browser check (light + dark) against
  the built `output/`: Pupper shows its own banner, an unmodified main
  page and an unmodified detail page render pixel-identical to before,
  0 console/network errors.
* Tests: `uv run pytest` — 129 passed (was 120; +9 new: 2
  `content_manager` hero-field cases, 5 `resolve_banner` cases, 2
  `banner.html` render cases). `ruff check .` / `ruff format --check .`
  clean except the pre-existing, still-deferred `DTZ` findings.

## 2026-08-20 (F04 + F05 closed: full Option D site redesign)
* F04 (site redesign concept exploration) done: 4 mockup directions —
  A blueprint, B terminal/circuit, C industrial minimal, D a Futurism.com
  editorial homage (the one later implemented) — in
  `design-mockups/f04-site-redesign/`, published as a comparison gallery
  artifact. Discovered `content/projects/pupper.md` is a real, current
  project (Stanford Pupper v3), not hypothetical, so all mockups used its
  real photos/copy. Moved to `done/`.
* F05 (implement Option D in the real site) done, all 18 `TF05` steps
  across 3 phases:
  - **Phase 1**: sitewide CSS variable/typography re-theme (cream/ink/red
    palette, Archivo Narrow), nav + footer redesign (Pupper added as a
    6th nav entry, linking to its existing project page), full home page
    rebuild (lead block, story rivers, rail).
  - **Phase 2**: Learn/What's New/Meetings/Projects/Members/About all
    re-skinned from Bootstrap to the site's own CSS, each with its own
    content-preservation regression test.
  - **Phase 3**: Bootstrap CSS/JS/Icons removed entirely — 11
    hand-authored inline SVG icons replace Bootstrap Icons, a new
    `.page-content`/`.hero` absorbed the layout utility classes Bootstrap
    was providing, added the `box-sizing: border-box` reset Bootstrap's
    reboot.css was quietly supplying.
* Real bugs found and fixed along the way (unrelated to the redesign
  itself): a stray literal "+" rendering as visible text on every page
  (all 3 layout templates); every meeting-detail page overflowing a
  fixed-size thumbnail box with a full paragraph of text; the
  long-dangling `images/robot-logo.png` reference (flagged since F01)
  finally resolved with a user-supplied hand-drawn logo, circle-cropped
  and made theme-aware via `filter: invert()`.
* Content-count parity verified exact across the whole migration: 24
  news / 24 meetings / 9 projects / 14 members — nothing lost.
* Also this session: filled in `02-doc/spec.md` (was an unfilled
  template); tightened `.claude/process.md`'s md-brevity rule with a
  concrete bullet-count ceiling after drifting back into pre-rule
  verbosity once.
* `uv run pytest` — 107 passed (up from 78 at session start). Checkpoint:
  `uvx ruff check .`/`ruff format --check .` clean except the 3
  pre-existing, deliberately-deferred `DTZ` findings (unchanged, see
  `current.md`). Committed and pushed on branch `f04-site-redesign` (not
  merged to `main`).

## 2026-08-20 (F03 closed: signup QR code)
* F03 (QR code to signup form on home page header) done: all 5 TF03 steps
  (`TF03.0`-`TF03.4`) done. Moved `03-features/notdone/F03-qrcode.md` ->
  `03-features/done/` and `04-tasks/notdone/TF03-qrcode.md` ->
  `04-tasks/done/`.
* Added `signup_url` to `config/site.json` (the group's Google Form,
  confirmed by the user; cross-checked against the hero's existing
  "Request an invite" link — same form via a `forms.gle` short link).
  Build-time QR generation (`qrcode[pil]` dependency,
  `AssetManager.generate_qr_code`) writes `output/images/signup-qr.png`
  from that field — not a checked-in static image, so it stays in sync if
  the URL ever changes.
* Rendered in `templates/layouts/home.html` (index-only), not the shared
  `hero.html` component — that component turned out to also be included
  by `templates/layouts/page.html` (every listing page), which would have
  put the QR on every page instead of just home. Caught by grepping
  template includes before editing, not after.
* Styled with a fixed white "quiet zone" frame independent of the
  light/dark theme variables (`css/main.css`'s `.signup-qr-cta`/
  `.signup-qr-frame`), since QR codes don't recolor safely — verified with
  real Playwright/Chromium rendering (scratch npm install, same approach
  as F01's TF01.7) in both themes, plus confirmed no QR code leaks onto
  `meetings.html`/`whatsnew.html`/`members.html`/a news detail page.
* `uv run pytest` — 78 passed (5 new: `TestGenerateQrCode` in
  `test_asset_manager.py`, `test_signup_qr.py`).
* Also this session: reworked `.claude/process.md`'s "writing .md files"
  rule to default to bullets over prose paragraphs (was producing overly
  narrative feature/task descriptions); fixed a filename mismatch in the
  same file (`task-template.md` -> `task_template.md`, matching the real
  file); updated the conflicting `feedback_md_formatting` memory to match.
* Follow-up styling tweaks per user feedback (chores 17-21 in
  `04-tasks/chores.md`): the QR badge went from an 80x80 in-flow block
  top-left of the page to a 100x100 `position: fixed` badge
  (`z-index: 200`) floating over both the sticky nav bar and the hero
  photo; trimmed the white "quiet zone" padding around it (the `qrcode`
  library already bakes its own in); caption text changed to "Join BRH";
  `signup_url` switched from the full Google Forms URL to its
  `forms.gle` short link (confirmed to redirect to the same form),
  cutting the QR from 41x41 to 29x29 modules — less visually busy and
  easier to scan at the small display size.
* Found and removed a second, git-tracked, pre-reorg duplicate
  `build/pyproject.toml` (+ its local `.venv`/`uv.lock`) — chore #18.
  `uv` silently resolved to it instead of root's `pyproject.toml` when a
  command's cwd was inside `build/`, so it was missing the `qrcode`
  dependency just added to root and broke with `ModuleNotFoundError`.
  This is the "three separate pyproject.toml files" issue F02 flagged
  2026-07-30 but never actually removed.
* Checkpoint: ran `uvx ruff check . --fix` (no ruff dependency/config
  existed in this repo before now) — 48 issues auto-fixed (import
  sorting, unused imports, `typing.Dict`/`List` -> builtin generics, an
  unnecessary-key-check simplification), plus 3 more by hand (2 implicit
  `Optional` -> `X | None` per `style_guide.md`, `chmod +x` on 5
  shebang'd files missing the executable bit). Also ran `uvx ruff format .`
  (first-ever formatting pass) — 10 files reformatted, mostly single- to
  double-quote per `style_guide.md`'s own SHOULD rule. Deliberately left 3
  `DTZ` (naive-datetime) findings unfixed — see `current.md`'s `## Open`.
  `uv run pytest` — 78 passed before and after.
* Migrated `02-doc/current.md`/`02-doc/history.md` to the split CLAUDE.md
  already documented (only `## Open` matters here) but that had never
  actually been done — this file was a flat chronological log with no
  `## Open` section until this checkpoint.
* Committed and pushed as part of this checkpoint.

## 2026-08-19 (F01 closed)
- F01 (dark/light mode correctness) confirmed done: all 8 TF01 steps
  (TF01.0-TF01.7) done, `uv run pytest` — 73 passed. Moved
  `03-features/notdone/F01-dark-light-mode.md` -> `03-features/done/` and
  `04-tasks/notdone/TF01-dark-light-mode.md` -> `04-tasks/done/`.
- `03-features/notdone/F03-qrcode.md` left alone — it's a one-line idea
  note ("add a qr code on every page to go to the signup form"), not a
  properly formatted feature file, and has no matching task file. Not done,
  nothing to close.
- `03-features/notdone/` and `04-tasks/notdone/` are now otherwise empty.

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
