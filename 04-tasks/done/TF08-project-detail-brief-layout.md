# TF08 Description for Feature F08

## TF08.0 — Generalize the brief CSS: `.news-brief-*` → `.detail-brief-*`
**Status**: done
**Description**: Rename the F07 CSS classes in `css/main.css` to a
content-type-neutral prefix (`.detail-brief-header*`, `.detail-brief-layout`,
`.detail-brief-body`, `.detail-brief-sidebar*`, `.detail-brief-toc`,
`.detail-brief-layout--no-sidebar`) and the `.detail-page:has(...)` width
override to match. Update `templates/details/news-detail.html`'s class
references to match. No visual change to news pages.
**Test**: `uv run pytest` — existing news ToC/no-sidebar/regression tests
(currently asserting `news-brief-*` strings) updated to the new class
names and still pass; full suite green.

**Result**: Straight rename (`news-brief` → `detail-brief`) across
`css/main.css`, `templates/details/news-detail.html`, and
`tests/test_whatsnew_content_preserved.py` — no visual/behavioral
change. Full build + `uv run pytest`: 116/116 pass.

## TF08.1 — Rebuild `templates/details/project-detail.html`
**Status**: done
**Description**: Replace `.detail-header`/`.detail-article` with the
`.detail-brief-*` shell. Header: `project.metadata.status` as the kicker,
title, image (or fallback), excerpt. Immediately after the header, keep
the existing `.project-detail__meta` bar (Started/Team/Lead/GitHub) and
`.project-detail__members` list unchanged. Then a two-column
body/sidebar — sidebar ToC from `project.toc_tokens`, omitted when empty
(reuse the `--no-sidebar` modifier from TF08.0).
**Test**: Build the site; assert the built `pupper.html` contains its 5
real top-level ToC links (and excludes nested `### Key Features`/
`### Project Members`), `dome-robot.html` contains its 2 (Software,
Hardware — confirms headings nest correctly with no `##` present), and
`midi.html` has no sidebar markup.

**Result**:
* `templates/details/project-detail.html` rebuilt to `.detail-brief-*`;
  `project.metadata.status` now doubles as the header kicker
  (identical visual treatment, so the old dedicated
  `.project-detail__status` CSS rule was dead and removed); the existing
  `.project-detail__meta` bar and `.project-detail__members` list kept
  unchanged, placed between the new header and the two-column body.
* Verified against real built output: `pupper.html` — 5 correct
  top-level ToC links, nested `Key Features`/`Project Members` correctly
  excluded; `dome-robot.html` — both `###`-only headings correctly
  top-level (no `##` present to nest under); `midi.html` — no sidebar
  markup.
* Extended `tests/test_projects_content_preserved.py` with 5 new tests
  (ToC content, nested-heading exclusion, no-`##` nesting, no-sidebar
  collapse) plus updated the pre-existing content test for the renamed
  classes; 6/6 pass.

## TF08.2 — CSS fit-and-finish for the project header
**Status**: done
**Description**: Resolve the border collision between the brief header's
own bottom border and `.project-detail__meta`'s existing top border
(would otherwise double up); adjust spacing so the kicker-as-status,
meta bar, and members list read as one coherent header block.
**Test**: Manual — Playwright render of the built Pupper/dome-robot/midi
project pages, light + dark, console/network-error check. Recorded per
the style guide's manual-test-notes convention.

**Result**:
* Confirmed via computed-style inspection: `.detail-brief-header`'s 3px
  bottom border and `.project-detail__meta`'s 1px top border sat flush
  against each other with 0 margin between — a visible double rule.
  Removed the now-redundant `border-top` from `.project-detail__meta`
  (only ever used directly after the brief header); also dropped the
  now-dead `.project-detail__status` CSS rule (superseded by the header
  kicker).
* Manual check (command: `node <inline script>` against a local
  Playwright scratch project, real built `output/` files): Pupper (5
  headings + images interspersed in body), dome-robot (2 `###`-only
  headings), midi (no headings, long status kicker string as a stress
  case) — light + dark, 0 console/network errors on all 6 runs; single
  clean rule under the header, no dead sidebar space, both themes read
  correctly.

## TF08.3 — Regression check: other detail pages unaffected
**Status**: done
**Description**: Confirm news/meeting/member detail pages render
unchanged after the TF08.0 rename and TF08.1/TF08.2 additions.
**Test**: Full `uv run pytest` suite passes; Playwright spot-check of one
news, one meeting, and one member detail page.

**Result**: Full suite: 120/120 pass (was 116 before F08's 4 new
project-ToC tests). Playwright spot-check of the Pupper news page, a
meeting detail page, and Adam Ring's member page: 0 console/network
errors, all three render identically to before F08.

## TF08.4 — Full verification
**Status**: done
**Description**: Run the full build and test suite.
**Test**: `uv run python build/build.py` succeeds, "Built 9 projects
detail pages", no errors/warnings; `uv run pytest` passes.

**Result**: Clean full build — "Built 9 projects detail pages", no
errors/warnings. `uv run pytest` — 120/120 pass.
