# TF09 Description for Feature F09

## TF09.0 — Add `default_banner_image` to `config/site.json`
**Status**: done
**Description**: Add `"default_banner_image": "images/meetings/meeting1-1.jpg"`
(today's hardcoded path) to `config/site.json`, so the fallback image is
configured in one place instead of buried in `css/main.css`.
**Test**: `uv run pytest` — existing config-loading tests still pass with
the new key present.

**Result**: Added the key; existing `test_signup_qr.py` config test still
passes unchanged.

## TF09.1 — `content_manager.build_hero_content` returns raw banner fields
**Status**: done
**Description**: Extend `build_hero_content` in `build/content_manager.py`
to also return `banner_image`, `banner_title`, `banner_subtitle` — read
straight from the hero file's frontmatter (`None` when absent). No
fallback logic here; this method just surfaces what's in the file.
**Test**: `tests/test_content_manager.py` — new cases: hero file with all
three fields set returns them; hero file with none set returns `None` for
each; existing hero tests unaffected.

**Result**: Added the 3 keys via `hero_data["metadata"].get(...)`. Two new
tests in `tests/test_content_manager.py` (absent → `None`, present →
values); 42/42 in that file pass.

## TF09.2 — `PageBuilder.resolve_banner` helper
**Status**: done
**Description**: New method on `PageBuilder` in `build/page_builder.py`:
`resolve_banner(metadata: dict, path_prefix: str = "") -> dict`. Returns
`{"banner_image": ..., "banner_title": ..., "banner_subtitle": ...}` —
uses `metadata`'s `banner_image`/`banner_title`/`banner_subtitle` when
present, else falls back to `self.site_config["default_banner_image"]`,
`site.title`, `site.subtitle`. An overridden (non-default) image path
gets `path_prefix` prepended (`"../"` for detail pages, `""` for main
pages), matching the existing convention in
`templates/details/project-detail.html`'s `../{{ project.image }}`.
**Test**: `tests/test_page_builder.py` — override case (all three
fields), partial-override case (only image set, title/subtitle fall
back), no-override case (all three fall back), and path-prefix applied
only when an override is present (default image path is not
double-prefixed).

**Result**:
* Design correction made during implementation: `path_prefix` is applied
  to *whichever* image is chosen — override or default — not only to
  overrides. Both paths are root-relative, and detail pages moved the
  banner from CSS (relative to the CSS file's own fixed location) to an
  inline HTML style (relative to that page's own directory), so the
  default image needs the same per-depth prefixing as an override does.
* 5 new tests in `tests/test_page_builder.py::TestResolveBanner`
  (no-override defaults, full override, partial override, prefix applied
  to an override, prefix applied to the default); 30/30 in that file
  pass.

## TF09.3 — Wire `resolve_banner` into detail-page and main-page builds
**Status**: done
**Description**: In `PageBuilder.build_detail_pages` (`build/page_builder.py`),
call `resolve_banner(item["metadata"], path_prefix="../")` and merge the
result into `template_vars` as top-level keys. In each of the 6 main-page
builders in `build/build.py` (about, projects, members, meetings,
whatsnew, learn), call `resolve_banner(hero_content, path_prefix="")` and
pass the result into `build_page(...)` as top-level keys.
**Test**: Build the site; assert every generated main page and every
generated detail page's HTML contains a `banner_image`-derived
`background-image` (i.e. `resolve_banner` ran for all of them, not just
projects).

**Result**: Wired in both places (`build_detail_pages` covers all 4 detail
types generically). Full build succeeded — "Built 24 news / 9 projects /
14 members / 24 meetings detail pages", all 6 main pages built; grepped
every generated page's `.banner` div for a `background-image` style,
present on all.

## TF09.4 — Update `banner.html` and `.banner` CSS
**Status**: done
**Description**: `templates/components/banner.html` renders
`banner_title`/`banner_subtitle` (instead of hardcoded `site.title`/
`site.subtitle`) and sets `style="background-image: url('{{ banner_image }}')"`
inline. `css/main.css`'s `.banner` rule drops the hardcoded
`url(...)`, keeping `background-color`, `background-size`,
`background-position` as fallback/safety styling.
**Test**: `tests/test_layout_markup.py` (or nearest equivalent) — asserts
the banner element carries an inline `background-image` style and the
overlay text matches the resolved `banner_title`/`banner_subtitle`.

**Result**: Template uses Jinja `default(...)` filters so it degrades
safely even if a caller forgets to pass the resolved vars. New
`tests/test_banner.py` (override case, fallback case) renders the real
template file directly; 2/2 pass.

## TF09.5 — Set Pupper's own banner as the first real instance
**Status**: done
**Description**: Add `banner_image`, `banner_title`, `banner_subtitle` to
`content/projects/pupper.md` frontmatter with real values.
**Test**: Build the site; assert `output/projects/pupper.html`'s banner
uses Pupper's own image/text, not the site default.

**Result**: Used `images/projects/pupper_resting.jpg` (distinct from the
`pupper_standing.jpg` already used as the page's own thumbnail, so the
banner and the header image aren't identical), title "Stanford Pupper
v3", subtitle "An open-source quadruped robot, built with Boston Robot
Hackers". Confirmed in the built HTML.

## TF09.6 — Full verification
**Status**: done
**Description**: Run the full build and test suite; confirm no visual
regression on pages without an override.
**Test**: `uv run python build/build.py` succeeds with no errors/warnings;
`uv run pytest` passes in full; manual/browser spot-check of Pupper's
page plus one unmodified main page and one unmodified detail page in
both light and dark themes.

**Result**:
* Clean full build, no errors/warnings. `uv run pytest`: 129/129 pass
  (was 120; +9 new tests from TF09.1/TF09.2/TF09.4).
* `uvx ruff check build/ tests/`: only the 3 pre-existing, already
  deferred `DTZ` findings — no new lint issues.
* Playwright spot-check (local Playwright install in the scratchpad dir,
  served `output/` over `python3 -m http.server`) of `projects/pupper.html`
  (override), `about.html` (unmodified main page), and `projects/midi.html`
  (unmodified detail page), light + dark: Pupper shows its own
  image/title/subtitle, the other two match today's site default exactly,
  0 console/network errors on any of the 6 runs.
