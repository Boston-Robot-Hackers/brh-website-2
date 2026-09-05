# F14 — Reduce repeated boilerplate across build.py's build_*_page methods
**Priority**: Low
**Done:** no
**Tasks File Created:** no
**Tests Written:** no
**Test Passing:** no

**Description**:
* Found during a code/architecture deep-dive review (session on the
  `deepdive` branch). Not a bug — every page builds correctly today.
  This is a duplication/maintainability observation.
* `WebsiteBuilder` (`build/build.py`) has six page-building methods —
  `build_news_page`, `build_projects_page`, `build_members_page`,
  `build_about_page`, `build_learn_page`, `build_meetings_page` — that
  all follow the same shape:
  1. Load content via `self.content_manager.get_all_content(...)` (or,
     for `about`/`learn`, read a single file).
  2. Optionally call `self.page_builder.build_detail_pages(...)`.
  3. Render section content.
  4. Build hero content: `self.content_manager.build_hero_content("X")`.
  5. Call `self.page_builder.build_page(..., hero=hero_content, ...,
     **self.page_builder.resolve_banner(hero_content))`.
  The `hero_content = build_hero_content(...)` +
  `**resolve_banner(hero_content)` envelope in step 4-5 repeats
  near-verbatim in all six methods (`build_index` is the one exception —
  it uses `layouts/home.html`, which suppresses the banner, so it
  doesn't call `resolve_banner`).
  The per-page variation is real and shouldn't be flattened away:
  `build_projects_page`/`build_members_page` build extra
  slug-to-URL maps for cross-linking, `build_learn_page` parses a
  different content format entirely (`parse_learn_sections`), and each
  passes different extra template variables.
* **Proposed fix**: extract the repeated hero+banner+build_page envelope
  into a small helper, e.g.:
  ```python
  def _build_hero_page(self, page_name: str, template_name: str,
                        output_filename: str, **extra_context):
      hero_content = self.content_manager.build_hero_content(page_name)
      self.page_builder.build_page(
          template_name, output_filename,
          hero=hero_content,
          **self.page_builder.resolve_banner(hero_content),
          **extra_context,
      )
      return hero_content  # some callers use it for print()/logging
  ```
  Each `build_X_page` method keeps its own content-loading and
  detail-page-building logic (the genuinely different part), and ends
  with a call to `_build_hero_page(...)` instead of the repeated
  `hero_content = ...; self.page_builder.build_page(...)` block. This is
  a pure refactor — same templates rendered with the same context in the
  same order, just less repeated code to read.
* Lower priority than F11/F12/F13 since it's purely internal code
  organization with no external-facing or tooling implications — the
  main benefit is future changes to the hero/banner envelope (e.g., a
  new site-wide banner field) only needing to happen in one place
  instead of six.

**Non-goals**:
* Not touching `build_index` (different layout, no banner) or
  `build_news_page`'s meetings/related-reports logic — those stay as
  page-specific code, not folded into the shared helper.
* Not a behavior change of any kind — every page's rendered HTML should
  be byte-identical before and after.

## How to Demo
**Setup**: `uv run python build/build.py`, run both before and after the
refactor.

**Steps**:
1. Diff the two `output/` trees (e.g. `diff -r output-before
   output-after`) — should be empty.
2. Full test suite (`uv run pytest`) passes unchanged, including the
   content-preservation tests
   (`test_*_content_preserved.py`) that build real pages from real
   content.

**Expected output**: No visible or behavioral difference; `build.py`
is shorter and the six page-building methods read as "what's different
about this page" rather than repeating "how to build any page."

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
