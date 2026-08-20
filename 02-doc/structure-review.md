# Structure & Consistency Review

Findings from F02, ordered by priority. Each has evidence, the risk it poses
(especially to an AI agent navigating the repo cold), a concrete proposed
change, and a recommended disposition.

**Status: all 8 findings applied** (2026-08-19), logged as chores 9-16 in
`04-tasks/chores.md`. Each finding below now has a **Done** note describing
what actually happened. `uv run pytest` — 69 passed; full site rebuild
verified (same page counts, all renamed URLs resolve, cross-links updated).

## High priority

### 1. `member_template.md` and `project_template.md` aren't templates — they're live content

**Evidence**: `content/members/member_template.md`'s frontmatter is Pito
Salas's real profile (`name: "Pito Salas"`, real GitHub/LinkedIn links, real
image path) — not a blank scaffold. It builds into
`output/members/member_template.html` and appears on `output/members.html`
and `output/index.html` like any other member. `content/members/adam_ring.md`
even hardcodes a link to
`https://bostonrobothackers.com/members/member_template.html` as Pito's real
public profile URL. The same pattern repeats for
`content/projects/project_template.md`, which holds a real project ("Dome
ROBOT", lead: Pito Salas).

**Risk**: The site's own founder has an unprofessional public URL
(`/members/member_template.html`). Worse for future work: anyone — human or
AI agent — told to "copy the template to add a member/project" will
unknowingly clone or overwrite real, live content, because there is no
actual blank template for either content type. `content_manager.py` has no
filename-based exclusion, so any file matching this pattern gets built and
published.

**Proposed change**: Rename `member_template.md` → a real slug (e.g.
`pito-salas.md`) and `project_template.md` → e.g. `dome-robot.md`; update the
hardcoded link in `adam_ring.md`. Then create genuine blank templates (e.g.
prefixed `_template.md`) that `content_manager.py` explicitly skips by
filename convention, so a safe, non-published template can exist.

**Disposition**: Chore — but it changes a published URL, so get sign-off on
the new slug before applying. Needs a regression test (e.g. assert no
`*_template.md` file under `content/{members,projects}/` is ever built as a
public page).

**Done**: Renamed to `pito-salas.md` and `dome-robot.md`. Fixed the
hardcoded link in `adam_ring.md` (now `adam-ring.md`) and the `projects:`
cross-ref in `pito-salas.md`. Added a leading-underscore template convention
(`content/{members,projects}/_template.md`, real blank scaffolds) that
`content_manager.py`'s `get_all_content` now skips on `md_file.stem.startswith('_')`.
Regression test added: `tests/test_content_manager.py::TestGetAllContent::test_leading_underscore_file_excluded`.

### 2. `legacy/` and `archive/build.py` are fully dead weight, including a committed `node_modules/`

**Evidence**: `legacy/` (46 git-tracked files) is an earlier Tailwind-based
prototype — its own `main.py`, `pyproject.toml`, `package.json` /
`package-lock.json`, `tailwind.config.js`, 3 old dated content files, and a
**git-tracked `node_modules/`** (35 files). `archive/build.py` is an orphaned
pre-refactor build script. A repo-wide grep (excluding these two
directories) confirms zero references to either from `build/`, `templates/`,
docs, or `.github/workflows/deploy.yml`.

**Risk**: Tracked `node_modules/` is the classic repo-bloat anti-pattern.
More importantly for an AI agent: searching for "build.py" or "main.py"
turns up three candidates (`build/build.py`, `legacy/main.py`,
`archive/build.py`) instead of one, and nothing signals which is live.

**Proposed change**: `git rm -r legacy/ archive/`. Fully recoverable from git
history if ever needed — no working-tree functionality depends on either.

**Disposition**: Chore.

**Done**: `git rm -r legacy/ archive/`. Both fully recoverable from git
history.

## Medium priority

### 3. `rules.md` is a dangling, git-tracked symlink to a path outside the repo

**Evidence**: `rules.md` → `/Users/pitosalas/mydev/dotfiles/rules.md`. That
target doesn't exist even on the machine that created the symlink. Nothing
in the repo references `rules.md`.

**Risk**: Breaks on every checkout other than the one it was made on;
carries zero information for anyone who clones the repo.

**Proposed change**: `git rm rules.md`. If it was meant to carry personal
Claude Code preferences, that belongs in this machine's user-level Claude
settings, not a repo-tracked symlink.

**Disposition**: Chore.

**Done**: `git rm rules.md`.

### 4. `content/members/` filenames use four different conventions at once

**Evidence**: underscores (`adam_ring.md`, `buddy_e.md`, `chris_kennedy.md`,
`franklin_reynolds.md`, `randell_drane.md`), hyphens (`alan-kilian.md`,
`siddarth-profile.md`, `skyler-wiernik.md`), no separator
(`arjunviswanathan.md`, `dwarkesh.md`, `jerinpeter.md`, `kamalnath.md`), and
one capitalized filename (`Hari.md`).

**Risk**: `Hari.md` is a real portability risk, not just a style nit —
macOS's default case-insensitive filesystem treats `hari.md` and `Hari.md`
as the same file, but Linux (GitHub Actions' CI runner, where the site
actually builds) is case-sensitive. Any future case-mismatched reference
would only break in CI/production, never locally. More broadly, four
conventions in one folder means an agent adding a new member has no single
pattern to infer from.

**Proposed change**: Standardize on lowercase-hyphenated slugs, matching the
convention `content/news/` and `content/meetings/` already mostly use.
Rename files and fix any cross-references (bundle with finding 1, since
`adam_ring.md`'s link needs updating either way).

**Disposition**: Chore.

**Done**: Renamed all 9 to lowercase-hyphens (`adam-ring.md`, `buddy-e.md`,
`chris-kennedy.md`, `franklin-reynolds.md`, `randell-drane.md`,
`arjun-viswanathan.md`, `jerin-peter.md`, `kamal-nath.md`, `hari.md`).
`dwarkesh.md` and `siddarth-profile.md` left as-is (already single-word/
already hyphenated; not part of the identified inconsistency). Fixed the one
hand-written cross-reference (`buddy_e` → `buddy-e` in
`content/news/14-december-meerting-summary.md`).

## Low priority

### 5. Three `content/news/` files still use underscores

**Evidence**: `1-first_meeting.md`, `2-second_meeting.md`,
`7-third_meeting.md` — the three oldest posts — vs. hyphens in all 22 later
ones.

**Proposed change**: Rename to `1-first-meeting.md` etc. Cosmetic; bundle
with finding 4 if the naming cleanup is ever batched.

**Disposition**: Chore, low priority.

**Done**: Renamed all 3. No cross-references found to fix.

### 6. `README.md`'s Project Structure tree omits `image-sources/`

**Evidence**: `image-sources/` is real and actively used — it has its own
thorough `README.md` explaining a two-set (hand-drawn/photo) image-swap
workflow driven by `scripts/set-images.sh` — but nothing in the root
`README.md` or `CLAUDE.md` points to it. (The `.claude/`, `02-doc/` through
`05-issues/` folders are a non-issue here: they're already covered by
`CLAUDE.md`'s Development Process section, a reasonable human-doc /
agent-doc split.)

**Proposed change**: Add one line to `README.md`'s Project Structure tree:
`image-sources/` → see `image-sources/README.md`. Findings 2 and 3 remove
`legacy/`/`archive/`/`rules.md` outright, so they don't need documenting.

**Disposition**: Chore.

**Done**: Added `image-sources/` to the tree, pointing at its README.

### 7. `README.md` describes `scripts/` as "JavaScript" only

**Evidence**: `scripts/` also holds `set-images.sh`, an actively-used build
utility (see finding 6).

**Proposed change**: Update the one-line description in the tree. Bundle
with finding 6.

**Disposition**: Chore.

**Done**: Updated the description to "JavaScript + set-images.sh utility".

### 8. `05-issues/{open,closed,deferred}/` subfolders don't exist yet

**Evidence**: `.claude/process.md` documents this structure; `05-issues/` is
currently flat and empty (just `.gitkeep`).

**Proposed change**: `mkdir -p 05-issues/{open,closed,deferred}`.

**Disposition**: Chore.

**Done**: Created all three, each with a `.gitkeep` so git tracks the empty
directories.

## Already tracked — not duplicated here

- **8 style-guide items in `04-tasks/chores.md`** from the prior `build/*.py`
  review (inline-HTML-in-Python, duplicated link-resolution logic, dead
  code, import placement, file headers, type hints, indentation, line
  length) — same "quick wins" category as the findings above. **Done**:
  applied alongside this review's own findings (moved hero HTML generation
  into `templates/components/upcoming-meetings-hero.html`, extracted
  `PageBuilder.resolve_announcement_report()`, removed dead code, fixed
  import placement/shadowing, added file headers/shebangs, fixed a type
  hint and an indentation bug, wrapped all lines over 88 chars).
- **Three `pyproject.toml` files**: the root/`build/` split is intentional
  and already documented in `CLAUDE.md` (different Python versions — 3.12
  root, 3.13 build). `legacy/pyproject.toml` is dead weight, covered by
  finding 2 — removed along with the rest of `legacy/`.

## Summary

| # | Finding | Priority | Disposition | Status |
|---|---|---|---|---|
| 1 | `member_template.md`/`project_template.md` are live content, not templates | High | Chore (needed sign-off on new URL + regression test) | Done |
| 2 | `legacy/` + `archive/build.py` dead, incl. tracked `node_modules/` | High | Chore | Done |
| 3 | `rules.md` dangling symlink outside repo | Medium | Chore | Done |
| 4 | `content/members/` filenames: 4 conventions + 1 case-sensitivity risk | Medium | Chore | Done |
| 5 | 3 `content/news/` files use underscores | Low | Chore | Done |
| 6 | `image-sources/` undocumented from README | Low | Chore | Done |
| 7 | `scripts/` description stale in README | Low | Chore | Done |
| 8 | `05-issues/` subfolders missing | Low | Chore | Done |

All 8 applied 2026-08-19, logged as chores 9-16 in `04-tasks/chores.md`
alongside the 8 pre-existing `build/*.py` style-guide chores (also applied
in the same pass). `uv run pytest` — 69 passed. Not yet committed/pushed.
