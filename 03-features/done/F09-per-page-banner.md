# F09 — Per-page customizable banner (image + overlay text)
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* The top banner (background image + overlaid title/subtitle) is
  currently hardcoded site-wide: one image in `css/main.css`, text always
  `site.title`/`site.subtitle` from `config/site.json`. Every page,
  including every detail page (e.g. `projects/pupper.html`), shows the
  identical banner.
* Add three optional frontmatter fields — `banner_image`, `banner_title`,
  `banner_subtitle` — usable on any page that already renders a banner.
  Any field left out falls back to today's default.
* Move the default banner image out of CSS into `config/site.json` as
  `default_banner_image`, so the fallback lives in one configurable place
  instead of buried in a stylesheet rule.
* Applies to:
  * The 6 main pages (about, projects, members, meetings, whatsnew,
    learn) — via their existing `content/heroes/<page>.md` file.
  * Individual detail pages (project, member, meeting, news) — via that
    item's own existing `.md` file. All four share one code path
    (`PageBuilder.build_detail_pages`), so enabling it generically costs
    the same as enabling it for projects alone.
* First real instance: `content/projects/pupper.md` gets its own
  `banner_image`/`banner_title`/`banner_subtitle`.

**Non-goals**:
* Home page — its banner is already suppressed (`layouts/home.html`
  overrides the block to empty); stays that way, unaffected by this
  feature.
* No new admin UI — overrides are set by hand-editing frontmatter, same
  as every other per-page/per-item field in this codebase.

## How to Demo
**Setup**: `uv run python build/build.py`.

**Steps**:
1. Open `output/projects/pupper.html` — banner shows Pupper's own image
   and overlay text, not the site default.
2. Open any other detail page (news/member/meeting) and any main page
   without a `banner_*` override — banner is visually unchanged from
   today.
3. Toggle dark/light — banner text remains legible against the image on
   both.

**Expected output**: Pupper's project page has a distinct banner; every
page without an override looks exactly as it does today.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
