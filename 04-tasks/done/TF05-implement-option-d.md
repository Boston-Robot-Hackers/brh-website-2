# TF05 Description for Feature F05

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF05.N`, starting at `.0`.

Organized in 3 phases per the user's request: phase 1 lands Option D
sitewide-theme + home page; phase 2 gradually extends it to every other
page; phase 3 removes Bootstrap once nothing depends on it anymore.
Recommend pausing for a look after each phase before continuing to the
next — noted again at TF05.7, TF05.15.

## Phase 1 — Sitewide theme + home page

## TF05.0 — Audit current Bootstrap/CSS-variable usage
**Status**: done
**Description**: Catalog, across `templates/` and `css/`: every place
Bootstrap grid/card/btn/nav classes are used (so later phases know what
still needs re-skinning), every hardcoded color, and every existing use of
`css/shared.css`'s CSS custom properties (so Phase 1 knows exactly what
re-theming the `:root` block will and won't automatically cover). Mirrors
TF01.0's audit approach for F01.
**Test**: N/A — documentation/inventory step, not a behavior change. The
resulting list is recorded as this task's completion evidence.

**Result**:
* Bootstrap classes appear in 26 of ~30 templates — essentially everywhere.
* `shared.css` holds the only "real" hardcoded colors (23, all expected —
  TF05.1's target); `main.css`'s 4 are already on the `BESPOKE_CHROME_HEX`
  allowlist.
* CSS variables are already used broadly — confirms repainting them
  re-skins most of the site for free, no markup changes needed.
* `data-bs-theme` touchpoints: `base.html`, `script.js`, `shared.css` —
  the surface TF05.2 must preserve.

## TF05.1 — Re-theme CSS custom properties + typography sitewide
**Status**: done
**Description**: In `css/shared.css`, replace the palette values in the
light `:root` block and the `:root[data-bs-theme="dark"]` block with
Option D's system (cream/off-white light ground, near-black ink, red
accent; a new near-black dark ground with the same red accent, adjusted
for contrast) — keeping every variable *name* unchanged
(`--bg`/`--bg-card`/`--border`/`--border-hover`/`--text`/`--text-muted`/
`--text-light`/`--primary`/etc.) so everything already referencing them
re-skins for free. Swap the `@import`ed Google Font from Telex to Archivo
Narrow (weights 400–900 + italic) and update the heading/nav-link/card-title
font-family rule to match.
**Test**: Extend `tests/test_css_theme.py`'s light/dark parity check (still
passes unchanged in shape) plus a new assertion that the new palette's hex
values and `Archivo Narrow` appear in `css/shared.css`.

**Result**:
* `shared.css`: Telex → Archivo Narrow (400–900 + italic), now used by
  `body` too, not just headings.
* Light palette repainted to cream/ink/red; dark palette repainted to a
  warm near-black (not the old blue-slate). `--secondary`/`--accent`/
  `--success` left unchanged (isolated badge fills only, per F01).
* Deviated from F01's "accents unchanged across themes" precedent for
  `--primary` only: dark mode gets a lighter red tint, since red is now
  running link/nav text, not just fills, and needs the contrast — noted
  inline in the CSS.
* New `test_shared_css_uses_option_d_palette_and_type`; all 5
  `test_css_theme.py` tests pass.

## TF05.2 — Redesign the shared nav
**Status**: done
**Description**: Rebuild `templates/components/navigation.html` (and its
CSS in `css/main.css`) to Option D's pattern: wordmark, uppercase links,
Pupper as a 6th entry in italic red with a circular real-photo badge
(`images/projects/pupper_standing.jpg`), linking to
`{{ '../' if is_detail_page else '' }}projects/pupper.html`. Preserve the
existing `current_page` active-state logic and `is_detail_page` relative-
path handling exactly — only the visual treatment changes. Keep the
`#theme-toggle` button working, restyled to fit the new nav.
**Test**: New test asserting the Pupper nav link renders in built output
pointing at `projects/pupper.html` on top-level pages and
`../projects/pupper.html` on detail pages; existing nav-related assertions
in `tests/test_page_builder.py` still pass unchanged.

**Result**:
* `navigation.html` rebuilt as `.site-nav`: wordmark + 5 links (unchanged
  active-state/relative-path logic, new class names) + Pupper as a 6th
  italic-red link with a real photo badge, linking to the existing
  `projects/pupper.html`. `#theme-toggle` kept as-is, just restyled.
* `main.css`: new `.site-nav*` rules replace `.nav-bar-thin`/`.nav-logo`
  (the latter was already-dead code, removed alongside it).
* `shared.css`: dropped the now-unused `.nav-link` rule.
* New `tests/test_navigation.py` (4 tests). Manual Playwright check, both
  themes, clean (only the pre-existing unrelated missing-logo warning).
  79 → 83 passed.

## TF05.3 — Redesign the shared footer
**Status**: done
**Description**: Restyle `templates/components/footer.html` to Option D's
system — drop the `bg-dark text-light` Bootstrap utilities in favor of the
new CSS variables. `{{ site.footer_text }}` keeps rendering unchanged.
**Test**: Covered by TF05.7's regression pass; existing tests already
checking `footer_text` renders (if any) must still pass unchanged.

**Result**:
* `footer.html`: dropped Bootstrap's `bg-dark text-light` utilities —
  they were overriding `shared.css`'s already theme-aware `footer` rule
  (same cascade issue TF01 fixed elsewhere), so the footer had been stuck
  permanently dark regardless of theme.
* Manual check: footer now correctly follows theme in both modes.
* 83 passed, unchanged (low-risk enough to defer a dedicated test to
  TF05.7's regression pass).

## TF05.4 — Make the generic title banner overridable per page
**Status**: done
**Description**: Wrap `layouts/base.html`'s
`{% include 'components/banner.html' %}` in a
`{% block banner %}{% include 'components/banner.html' %}{% endblock %}`
so `layouts/home.html` can override it empty — Option D's home page has
its own richer lead block instead of the generic title bar. Every other
page keeps showing `banner.html` as today, unchanged, until its own
Phase-2 task redesigns it. Template-inheritance override, not an
if-chain, per the style guide's nesting/branching guidance.
**Test**: New test: built `index.html` does not contain `banner.html`'s
markup; built `learn.html` (or another still-untouched page) still does.

**Result**:
* `base.html`'s banner include is now an overridable block; `home.html`
  overrides it empty, other layouts unchanged. Verified via build: home
  no longer shows it, `learn.html` still does.
* **Found and fixed in passing**: all 3 layout files had a stray literal
  "+" before their content `<div>` — a bad-patch leftover rendering as
  visible text sitewide. Fixed; logged as chore #24.
* New `tests/test_layout_markup.py` (4 tests). 87 passed.

## TF05.5 — Rebuild the home page content
**Status**: done
**Description**: Rewrite `templates/layouts/home.html` +
`templates/pages/index.html` to Option D's structure — lead block
(kicker/headline/dek/byline, using real copy from `content/heroes/index.md`),
full-bleed hero photo + caption, "What's New" and "Projects" story rivers,
a right rail with "Upcoming Meetings" + a Pupper spotlight card. Reuse the
*existing* Python data pipeline
(`news_content`/`meetings_content`/`projects_content`, built by
`build/build.py`'s `build_index()`) by restyling the underlying partials —
`templates/cards/news-card.html`, `templates/cards/project-card.html`,
`templates/components/upcoming-meetings-calendar.html` — to the new
story-row/rail markup, rather than touching `build/page_builder.py`'s
logic. Restyle (don't remove) the existing QR CTA
(`.signup-qr-cta`/`.signup-qr-frame`/`.signup-qr-caption` in
`css/main.css`) to fit the new palette.
**Test**: Extend `tests/test_page_builder.py`/`tests/test_signup_qr.py`-style
assertions: built `index.html` still contains every real highlighted-news
title, every real home-page project title, the Pupper spotlight, the QR
`<img>` with its alt text, and the upcoming-meetings entries — i.e.
confirms no content silently dropped in the rewrite.

**Result**:
* New `components/home-lead.html` (kicker/headline/subtitle/mission
  copy/byline + hero photo) replaces `hero.html` on home only; `hero.html`
  itself is untouched, still used by `page.html`.
* `index.html` rewritten to a river+rail grid, reusing the same
  `news_content`/`projects_content`/`meetings_content` Python pipeline —
  no `build/` changes. Added a static Pupper spotlight card in the rail.
* `news-card.html`, `project-card.html`, `upcoming-meetings-calendar.html`
  restyled to a shared `.story-row`/`.rail-item` pattern; orphaned
  `section.html` deleted (no longer included anywhere).
* New `tests/test_home_content_preserved.py` (5 tests, checked against
  real content, not fixtures) — confirms every highlighted news title,
  every project title, Pupper, the QR, and meetings all still render.
* Manual: real build + Playwright screenshots, both themes — matches
  Option D, all 23 river items present, no console/network errors beyond
  the pre-existing missing-logo one. 92 passed.

## TF05.6 — Phase 1 rendered verification
**Status**: done
**Description**: Real-browser check (Playwright, same approach as F01/F04)
of the home page and at least one still-unredesigned page, in both
`prefers-color-scheme` values and via the manual toggle — catches
cascade-order/contrast/broken-image bugs static checks miss (per F01's
TF01.7 precedent).
**Test**: Manual — recorded per `.claude/style_guide.md`'s manual-test-notes
convention (command/setup, pages checked, expected vs. actual, both
themes).

**Result**:
* Screenshotted `learn.html` (still fully Bootstrap-structured, untouched
  by any Phase 1 template edit) in both themes — it already inherits the
  new nav/banner/palette/type for free, confirming Phase 1's core premise.
* Clicked `#theme-toggle` on the home page: `data-bs-theme` flips
  light→dark, `localStorage` persists it, and it survives a reload —
  toggle still fully functional after the nav rewrite.
* No console/network errors beyond the pre-existing unrelated missing
  `images/robot-logo.png` preload.

## TF05.7 — Phase 1 regression tests + full pytest run
**Status**: done
**Description**: Dedicated test-writing task for Phase 1. Consolidate/
finalize the automated tests added in TF05.1–TF05.5, run the full suite.
**Recommend stopping here for a look before starting Phase 2.**
**Test**: `uv run pytest` includes and passes all Phase 1 additions.

**Result**:
* Full build + full suite both clean: `uv run python build/build.py`
  succeeds end to end; `uv run pytest` — 92 passed (up from 78 at the
  start of this feature — 14 new tests across `test_css_theme.py`,
  `test_navigation.py`, `test_layout_markup.py`,
  `test_home_content_preserved.py`).
* `git status` confirms the touched-file set matches the plan: `css/`,
  the nav/footer/layout/home templates, plus the new test files — nothing
  under `content/`, `config/`, or `build/` changed.
* Phase 1 complete: sitewide theme/type/nav/footer + full home-page
  rebuild all done, dark/light toggle and QR CTA both verified working.
  **Pausing here for review before starting Phase 2.**
* Follow-up refinement (post-review, still Phase 1): moved the QR from a
  fixed floating overlay to the home lead block's own left margin column
  (was empty space beside the centered text), sized up to 110px since it
  no longer has to squeeze inline next to the headline, with a "Join BRH"
  caption restored underneath. Stacks above the text on narrow viewports.
  `tests/test_signup_qr.py` updated to match; 93 passed.
* Fidelity pass against the Option D mockup (computed-style diff, not
  eyeballing): added missing `--header-bg`/`--dek` tokens and the
  `.eyebrow-links`-equivalent breadcrumb; matched nav wordmark size/
  tracking, Pupper link font-size, kicker tracking, river/rail-title
  weight (900) and `.rail-title`'s missing red-dot `::before`, home-grid
  to a fixed `340px` rail column, story-row thumbnails to sharp corners,
  story-row titles to weight 800, footer size, and gave the dek its
  mockup typography (italic/600/1.3rem) while still rendering the full
  dynamic hero content rather than a truncated quote. Split the rail's
  combined type+date line into two (`.rail-item__cat` + `__date`) and
  switched `.rail-item` from a red left-border to the mockup's bottom-
  divider, matching `.meeting-entry`'s existing structure. 101 passed;
  spot-checked whatsnew/meetings/learn (shared classes) for regressions.

## Phase 2 — Extend to every remaining page

## TF05.8 — Learn page
**Status**: done
**Description**: Re-skin Learn's resource-link cards to Option D's type/
color system. Likely low-risk — confirm in TF05.0's audit how much is
already inherited for free via the Phase 1 variable/font changes versus
needing real markup changes.
**Test**: Built `learn.html` still contains every resource link from
`content/learn.md` (count-based regression check) after the restyle.

**Result**:
* `learn.html`: replaced Bootstrap grid/card/utility classes with own
  `.learn-grid`/`.learn-card*` classes (own CSS, variable-driven); kept
  the Bootstrap Icons markup as-is (Phase 3's job).
* New `tests/test_learn_content_preserved.py` — confirms all 40 real
  resource links from `content/learn.md` still render.
* Manual: real build + Playwright screenshots, both themes — all 8
  sections/40 links present, no console/network errors beyond the
  pre-existing missing-logo one. 94 passed.

## TF05.9 — What's New listing + News detail
**Status**: done
**Description**: Extend the story-row pattern built in TF05.5 to the full
news archive (`templates/pages/whatsnew.html`,
`templates/cards/compact-news-card.html`) and the news-detail template
header (`templates/details/news-detail.html`).
**Test**: Built `whatsnew.html` still lists every `content/news/*.md`
entry (count-based regression check); one news detail page still renders
its full content.

**Result**:
* `whatsnew.html`/`compact-news-card.html` reuse the existing `.story-row`
  pattern directly (DRY) — same real 24 news entries, now story-rows.
* `news-detail.html`'s header re-skinned to a shared `.detail-header*`
  system, plus `layouts/detail.html` itself (own container + `.btn-outline`
  back link, replacing Bootstrap `row`/`col-lg-8`) — this is shared by all
  4 detail types, so TF05.10–12 inherit it for free.
* Found but left alone: `build_news_page()` computes `meetings_content`
  for a "right column" that the current template never renders (pre-
  existing, not a regression from this task) — noted, not fixed, out of
  this task's scope.
* New `tests/test_whatsnew_content_preserved.py` (2 tests). Manual: real
  build + Playwright, both themes, listing and one detail page — clean.
  96 passed.

## TF05.10 — Meetings listing + Meeting detail
**Status**: done
**Description**: Extend the "Upcoming Meetings" rail/row pattern to the
full meetings page (`templates/pages/meetings.html`,
`templates/cards/monthly-meeting-card.html`,
`templates/cards/compact-meeting-card.html`) and
`templates/details/meeting-detail.html`.
**Test**: Built `meetings.html` still lists every `content/meetings/*.md`
entry (count-based regression check).

**Result**:
* `compact-meeting-card.html` was confirmed dead (never rendered by any
  Python call, grep-verified) — deleted rather than restyled, along with
  its now-unused CSS.
* `meetings.html`/`monthly-meeting-card.html` restyled to Option D
  (kicker-label meeting entries, reusing `.rail-note`); `meeting-detail.html`
  reuses TF05.9's `.detail-header*` system.
* **Real bug found and fixed**: no meeting ever sets `image`, so every
  meeting detail page hit the image-less fallback, cramming the full text
  blurb (a short label for news/projects, but a full sentence for
  meetings) into a fixed 140x140px box — visibly overflowing on all 24
  pages. Dropped the thumb for meetings, show the blurb as a proper
  excerpt instead (previously invisible on the detail page entirely).
* New `tests/test_meetings_content_preserved.py` (3 tests, incl. a
  regression test for the overflow bug). Manual: real build + Playwright,
  both themes, listing + one detail page — clean. 101 passed.

## TF05.11 — Projects listing + Project detail
**Status**: done
**Description**: Extend the story-row/kicker pattern to the full projects
grid (`templates/pages/projects.html`,
`templates/cards/project-listing-item.html`) and
`templates/details/project-detail.html` — including Pupper's own detail
page, the nav's actual link target.
**Test**: Built `projects.html` still lists every `content/projects/*.md`
entry (count-based regression check); `projects/pupper.html` still renders
its full real content.

**Result**:
* `projects.html`/`project-listing-item.html` reuse `.story-row` directly
  (DRY). Added `.story-row__submeta` for the lead/started/GitHub line.
* Follow-up (per user request): restored the original 2-column CSS
  `columns` flow (`.projects-two-col`, dropped then re-added), with
  `break-inside: avoid` on `.story-row` so entries don't split across
  columns, and a single-column fallback under 700px.
* `project-detail.html` reuses the `.detail-header*` system from TF05.9,
  plus new `.project-detail__meta`/`__members` for the status/team/lead/
  GitHub grid and member links. Pupper's detail page (the nav's real link
  target) verified rendering its full content.
* Removed now-dead CSS (`.project-listing-item`, `.badge-status`,
  `.project-meta`, `.project-thumb`, `.project-detail-img`,
  `.projects-two-col`).
* New `tests/test_projects_content_preserved.py` (2 tests, real content).
  Manual: real build + Playwright, both themes, listing + Pupper's detail
  page — clean. 103 passed.

## TF05.12 — Members listing + Member detail
**Status**: done
**Description**: Re-skin `templates/pages/members.html`,
`templates/cards/member-card.html`, and
`templates/details/member-detail.html`, preserving the "open to work"
banner and hashtag/skills badges (`.member-skills`, `.member-tag`,
`.open-to-work`).
**Test**: Built `members.html` still lists every `content/members/*.md`
entry (count-based regression check); the "open to work" banner still
renders for at least one member with `opentowork: true`.

**Result**:
* `members.html`/`member-card.html`: Bootstrap grid → CSS grid
  (`.members-grid`, `auto-fill` responsive columns); kept `.card`,
  `.open-to-work`, `.member-skills`/`.member-tag`/`.member-projects*`
  exactly as-is (unchanged CSS, per the task's preservation note).
* `member-detail.html`: kept the `member-detail` class (existing
  `.member-detail .content p` rule depends on it) alongside the new
  `detail-article` convention; restyled the 2-column header, links, and
  projects line with new `.member-detail-header*`/`.member-detail__*`.
* New `tests/test_members_content_preserved.py` (2 tests) — all 14
  members present, open-to-work banner count matches the 4 real
  `opentowork: true` entries exactly. Manual: real build + Playwright,
  both themes, listing + one detail page — clean. 105 passed.

## TF05.13 — About page
**Status**: done
**Description**: Apply the lead-block/byline treatment to
`templates/pages/about.html`'s mission/contact content from
`content/about.md`.
**Test**: Built `about.html` still contains the same real paragraphs
(spot-check key phrases) after the restyle.

**Result**:
* Dropped the Bootstrap `row`/`col-lg-8 mx-auto` wrapper for a plain
  `.about-content` max-width container. `about_content` is raw markdown
  HTML (h2/p/ul/strong/a), not structured metadata, so "lead-block
  treatment" here means styling those tags directly: each `## ` section
  becomes a bold-900 uppercase heading with a bottom border (matching
  `.river-header`'s look), and `**bold**` emphasis picks up the red
  accent (matching `.hero strong`'s existing convention).
* New `tests/test_about_content_preserved.py` — spot-checks a key phrase
  from all 5 real sections (Mission/Resources/Community/Location/Contact).
  Manual: real build + Playwright, both themes — clean. 106 passed.

## TF05.14 — Phase 2 rendered verification
**Status**: done
**Description**: Real-browser check of every page type (all 7 top-level
pages + one detail page per content type), both themes — same method as
TF05.6, now covering the whole site.
**Test**: Manual — recorded per the style guide's convention.

**Result**:
* Playwright sweep: 7 top-level pages + 4 detail pages (news/meeting/
  project/member), both themes — 22 checks, zero console/network errors
  (the long-standing missing-`robot-logo.png` warning is gone too, fixed
  earlier this session).
* Theme toggle re-verified on a non-home page: flips correctly and
  persists across navigation to another page.

## TF05.15 — Phase 2 regression tests + full pytest run
**Status**: done
**Description**: Dedicated test-writing task for Phase 2.
**Recommend stopping here for a look before starting Phase 3.**
**Test**: `uv run pytest` includes and passes all Phase 2 additions.

**Result**:
* Full build + full suite clean: `uv run python build/build.py` succeeds;
  `uv run pytest` — 106 passed (up from 92 at the start of Phase 2 — 14
  new tests across the 5 content-preservation test files for Learn/
  WhatsNew/Meetings/Projects/Members/About).
* `git status` shows only the planned files touched, plus two
  `content/heroes/*.md` files the user edited directly (not by me) —
  unrelated to this feature, left as-is.
* Phase 2 complete: every page now matches Option D's system, no content
  lost anywhere. **Pausing here for review before starting Phase 3**
  (removing Bootstrap entirely).

## Phase 3 — Remove Bootstrap

## TF05.16 — Drop the Bootstrap CDN + Icons
**Status**: done
**Description**: Once TF05.0's audit (re-checked) confirms no template
references a Bootstrap CSS/JS class, remove the Bootstrap CSS/JS and
Bootstrap Icons `<link>`/`<script>` tags from
`templates/components/head.html`. Replace the theme-toggle's Bootstrap
Icon (`bi bi-moon-stars-fill`/`bi bi-sun-fill`) with a small inline SVG
sun/moon icon in `templates/components/navigation.html`, updating
`scripts/script.js`'s icon-swap logic accordingly.
**Test**: New test asserting no built page's `<head>` contains a
`cdn.jsdelivr.net/npm/bootstrap` reference.

**Result**:
* Re-audit found more than the task anticipated: `home.html`/`page.html`
  still used Bootstrap's `container`/`px-3`/`py-*` (→ new `.page-content`
  class), `hero.html` used `text-center`/`mx-auto` (→ moved into `.hero`
  CSS), and — since the task title says "+ Icons" — `learn.html`'s 8
  category icons also depend on Bootstrap Icons, not just the toggle.
* New `templates/components/icons.html`: a `icon(name)` macro with 11
  hand-authored inline SVGs (8 Learn categories + fallback + sun/moon),
  matching each existing `bi-*` name string so no Python/data change was
  needed. Theme toggle now renders both sun and moon inline and lets CSS
  show the right one off `data-bs-theme` — removed `script.js`'s icon-sync
  JS entirely rather than porting it.
* Added the `box-sizing: border-box` + form-element font-inheritance reset
  to `shared.css` that Bootstrap's reboot.css was quietly providing and
  several of this feature's own rules (QR/logo/icon sizing) depend on.
* `tests/test_css_theme.py`: replaced the now-moot cascade-order test with
  `test_no_bootstrap_cdn_reference` and a simpler load-order check.
* Manual: full Playwright sweep (11 pages × 2 themes) — zero console/
  network errors; screenshotted Learn (all 8 custom icons render
  correctly) and confirmed the toggle still flips/persists with zero
  icon-sync JS. 107 passed.

## TF05.17 — Final full-site regression pass
**Status**: done
**Description**: Dedicated test-writing task for Phase 3 and final
verification: full `uv run pytest`; full manual Playwright pass across
every page in both themes; grep-confirm zero remaining Bootstrap class
references anywhere in `templates/`; confirm every original news/meeting/
project/member entry still renders somewhere on the built site (no content
lost across the whole migration).
**Test**: `uv run pytest` passes; manual pass recorded per the style
guide's convention.

**Result**:
* Final grep sweep of every `templates/*.html` file: zero Bootstrap CDN
  references, zero `bi bi-*` icon classes, zero remaining Bootstrap
  utility classes (manually verified each grep hit — all were false
  positives from own class names like `.home-lead` containing "lead").
* Full build + full suite clean: `uv run pytest` — 107 passed.
* Content-count parity, built output vs. real source, exact on every
  type: 24 news / 24 meetings / 9 projects / 14 members — nothing lost
  across the entire F05 migration.
* F05 complete: all 3 phases done. Site fully matches Option D, dark/light
  toggle and QR signup both working, zero Bootstrap dependency, zero
  content lost.
