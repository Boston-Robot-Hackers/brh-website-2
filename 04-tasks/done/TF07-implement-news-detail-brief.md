# TF07 Description for Feature F07

## TF07.0 — Add real `toc_tokens` and `reading_time` to processed content
**Status**: done
**Description**: In `build/content_manager.py`'s `process_markdown_file`,
capture `md_processor.toc_tokens` (built by the already-active `toc`
extension) and add a computed `reading_time` (word count of the stripped
HTML content / 200 wpm, minimum 1) to the returned dict. Generic to all
content types — harmless for types that don't use it.
**Test**: Unit tests in `tests/test_content_manager.py` — a post with 2
known `##`/`###` headings produces matching top-level `toc_tokens`
entries (id/name); a post with no headings gives an empty list; word
count of a known-length body produces the expected `reading_time`.

**Result**:
* `compute_reading_time()` (word count / 200 wpm, min 1) and simplified
  `toc_tokens` (`[{"id", "name"}, ...]`, top-level only — nested headings
  already excluded by `markdown`'s own `nest_toc_tokens`) added to
  `process_markdown_file`'s return dict.
* Confirmed via source read that `TocExtension.reset()` clears
  `md.toc_tokens` on every `.convert()` call, so reusing one
  `md_processor` across files (as `get_all_content` does) can't leak one
  post's headings into the next — added a regression test for this.
* 6 new tests in `tests/test_content_manager.py`; 40/40 pass.

## TF07.1 — Rebuild `templates/details/news-detail.html` to Option 2
**Status**: done
**Description**: Replace the shared `.detail-header`/`.detail-article`
markup with the Option 2 two-column structure: compact non-full-bleed
header image + meta row (formatted date, `post.reading_time`) + excerpt,
then a body/sidebar grid — sidebar renders a ToC from `post.toc_tokens`
(top-level entries only, matching the approved mockup) and is omitted
entirely when there are no headings. New class names only (e.g.
`.news-brief*`) — do not touch `.detail-header*`/`.detail-article`, which
`meeting-detail.html`/`project-detail.html`/`member-detail.html` still use.
**Test**: Build the site; assert in a new/extended test that the built
Pupper post HTML contains the 3 expected ToC links with the real heading
ids, and that a real heading-less news post's built HTML has no sidebar
markup.

**Result**:
* `templates/details/news-detail.html` rewritten to `.news-brief-header*`/
  `.news-brief-layout`/`.news-brief-body`/`.news-brief-sidebar`/
  `.news-brief-toc` — no shared `.detail-header*`/`.detail-article`/
  `.content` classes touched.
* Kept the same missing-image fallback convention already used by
  `cards/news-card.html` (`{% if post.image %}...{% else %}fallback div{% endif %}`).
* Extended `tests/test_whatsnew_content_preserved.py`: updated the
  existing content-render test for the new classes, added a no-ToC
  regression test (real post `1-first-meeting.md` has no headings), and a
  `TestNewsDetailTableOfContents` class asserting the Pupper post's 3 real
  ToC links, that nested h4s are excluded, and reading time is shown.
  6/6 pass.

## TF07.2 — Add Option 2 CSS to `css/main.css`
**Status**: done
**Description**: Port the mockup's `.brief-*` rules (renamed to
`.news-brief*` to match TF07.1) into `css/main.css`, using existing
`var(--...)` tokens only — no new colors/fonts. Include the <720px
single-column collapse.
**Test**: Manual — Playwright render of the real built Pupper page and a
heading-less post, light + dark, console/network-error check. Recorded
per the style guide's manual-test-notes convention.

**Result**:
* `.news-brief-*` rules added to `css/main.css`, all via existing
  `var(--...)` tokens; `.detail-page:has(.news-brief-layout)` widens the
  shared 760px detail shell to 920px only for news pages (`:has()`
  scoping confirmed not to leak into meeting/project/member pages).
* Playwright caught a real layout bug during manual testing: a
  heading-less post still reserved the 220px sidebar column, leaving
  dead whitespace and narrowing the effective reading column. Fixed with
  a `.news-brief-layout--no-sidebar` modifier (single column, capped
  reading width) applied when `post.toc_tokens` is empty.
* Manual check (command: `node check-f07.js` against a local Playwright
  scratch project, real built `output/` files): Pupper post (has ToC),
  `1-first-meeting` (no ToC), and a meeting-detail page (regression) —
  light + dark + one 480px-narrow pass — 0 console/network errors on all
  runs; screenshots confirmed correct layout, no dead space, meeting page
  visually unchanged, responsive collapse works.

## TF07.3 — Regression check: other detail pages unaffected
**Status**: done
**Description**: Confirm `meeting-detail.html`/`project-detail.html`/
`member-detail.html` render unchanged (they still use `.detail-header*`)
after TF07.1/TF07.2's CSS additions.
**Test**: Existing `tests/test_*_content_preserved.py` suite still
passes; Playwright screenshot of one meeting/project/member detail page
before and after, confirming no visual diff.

**Result**:
* Full suite: 116/116 pass (baseline 107 + 10 new TF07 tests).
* Playwright spot-check of real built `meetings/10-meeting.html`,
  `projects/dome-robot.html`, `members/adam-ring.html`: 0 console/network
  errors, still render at the original 760px shared `.detail-page` shell
  — confirms `.detail-page:has(.news-brief-layout)`'s wider 920px rule
  applies only to news pages.

## TF07.4 — Full verification
**Status**: done
**Description**: Run the full build and test suite; confirm no other
page regressed.
**Test**: `uv run pytest` passes (baseline 107 + new TF07.0/TF07.1 tests);
`uv run python build/build.py` succeeds with no errors/warnings for all
24 news posts.

**Result**: Clean full build — "Built 24 news detail pages", no
errors/warnings. `uv run pytest` — 116/116 pass.
