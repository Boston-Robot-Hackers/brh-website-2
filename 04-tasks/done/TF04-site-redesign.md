# TF04 Description for Feature F04

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF04.N`, starting at `.0`.

## TF04.0 — Create the feature branch
**Status**: done
**Description**: Create and check out a new git branch off `main`,
`f04-site-redesign`, to isolate all redesign-exploration work. No site
files change in this step.
**Test**: N/A — a git operation, not application logic. Verified via
`git branch --show-current` reporting `f04-site-redesign`.

**Result**: Branch created and checked out; confirmed via
`git branch --show-current` → `f04-site-redesign`.

## TF04.1 — Draft three "modern engineering" visual directions
**Status**: done
**Description**: Define three distinct visual directions (palette, type,
graphic motif) for a modern-engineering redesign. Each must keep all
current content and the 5 existing nav areas (Home, Learn, Members,
Projects, About), plus a 6th nav entry, Pupper, styled distinctly from the
rest (different font and/or its own icon/graphic). Record the three
directions (name + short description each) in this task's Result before
building anything.
**Test**: N/A — a design decision, not executable logic; recorded directly
in this step's Result for user review before TF04.2 builds it out.

**Result**: Discovered while reading real content that `content/projects/pupper.md`
already exists — Pupper is a real, current BRH initiative (Stanford Pupper v3
quadruped, `content/news/24-ankush-dhawan-talk-announcement.md` announces the
talk), with real photos in `images/projects/pupper_*.jpg`. Used that real
photo asset directly rather than inventing mascot art. Three directions:

* **A — Blueprint**: dark navy, cyan/white technical-drawing palette, fine
  grid-line background, `IBM Plex Mono` uppercase labels + `Space Grotesk`
  headings, dashed-corner "schematic" card framing, line-art SVG diagrams.
  Pupper nav item: dashed-border callout box with a line-art paw-print SVG
  icon, keeping the schematic language but visually flagged as distinct.
* **B — Terminal/Circuit**: near-black, `JetBrains Mono` throughout, green/
  cyan terminal palette, `$ prompt` styling, circuit-trace SVG divider with
  glowing nodes, blinking-cursor hero accent. Pupper nav item: switches to
  `Fredoka` (rounded/playful) in amber, breaking the monospace command-line
  language on purpose — like a friendly daemon easter egg.
* **C — Industrial Minimal**: light concrete/steel palette, safety-orange
  accent, bold `Archivo` uppercase type, hairline rules, diagonal
  hazard-stripe accent bars top/bottom. Pupper nav item: the one nav entry
  using a real photo — a circular crop of `pupper_standing.jpg` — inside an
  orange pill badge set in `Baloo 2` (rounded/playful), instead of a line-art
  glyph like the other two directions.

All three keep the real hero/news/meetings/projects copy (from
`content/heroes/index.md`, `content/news/`, `content/meetings/`,
`content/projects/`) and add a small "Pupper spotlight" strip on the home
page (real photo + real project excerpt) as the graphic-interest element,
in addition to the nav-item treatment itself.

## TF04.2 — Build three standalone home-page mockups
**Status**: done
**Description**: For each direction, build a self-contained HTML+CSS
mockup of the home page — reusing real hero/news/meetings copy from
`content/`, not invented copy — implementing that direction's
palette/type/graphics and the redesigned nav (5 existing areas + Pupper).
Mockups are standalone files outside the Jinja2 build pipeline
(`build/`/`templates/` untouched).
**Test**: Manual — open each mockup directly in a browser; confirm it
renders with no console/network errors and all 6 nav entries are visible
and legible under both light and dark system color scheme. Recorded per
`.claude/style_guide.md`'s manual-test-notes convention (command/setup,
expected vs. actual) since this is a rendering/visual check pytest can't
assert.

**Result**:
* Correction to the plan: dropped the "both light and dark system color
  scheme" check. Each of these 3 mockups is a concept pitch that commits
  to one fixed, deliberately-designed palette (that commitment is part of
  the pitch) — not F01's light/dark toggle feature, which only applies
  once a direction is chosen and built into the real templates/CSS.
* Built `design-mockups/f04-site-redesign/option-a-blueprint.html`,
  `option-b-terminal-circuit.html`, `option-c-industrial-minimal.html` —
  each self-contained (inline `<style>`, Google Fonts `@import` with
  system-font fallback stacks), referencing real images via
  `../../images/...` and real copy from `content/heroes/index.md`,
  `content/news/`, `content/meetings/`, `content/projects/`.
* No file under `build/`, `templates/`, `css/`, `content/`, or `config/`
  touched.
* Manual check, done with real rendering (Playwright/Chromium, scratch npm
  project outside the repo, same approach as F01/F03): for each mockup,
  loaded via `file://`, checked console errors, network errors (>=400),
  and that all 6 nav entries (Home, Learn, Members, Projects, About,
  Pupper) are present. Command: `node check.js` against a small Playwright
  script. Expected vs. actual: all 3 mockups — 0 console errors, 0 failed
  requests, all 6 nav entries present. Matched.

## TF04.3 — Capture comparison screenshots
**Status**: done
**Description**: Screenshot each of the three mockups (e.g. via
Playwright, consistent with F01/F03's manual-verification approach) and
assemble them into one comparison view for the user's feedback.
**Test**: Manual — screenshots reviewed side by side to confirm each
direction renders as intended; no automated assertion applies to visual
design output.

**Result**: Full-page screenshots (1280px viewport) captured to
`design-mockups/f04-site-redesign/screenshots/` — `option-a-blueprint.png`,
`option-b-terminal-circuit.png`, `option-c-industrial-minimal.png` — via
the same Playwright script as TF04.2. Reviewed all three: distinct
palettes/type/graphics as designed, real content and images render
correctly, Pupper nav item visually distinct from the other 5 in each.

## TF04.4 — Write regression tests and final verification
**Status**: done
**Description**: Dedicated test-writing task. This feature produces
exploratory mockups only — nothing under `build/`, `templates/`, `css/`,
`content/`, or `config/` is touched, so there's no production code path to
unit test. Confirm via `git status`/`git diff --stat` against `main` that
only new files under the mockup/screenshot location changed, so the
existing `uv run pytest` suite is unaffected by this feature.
**Test**: `uv run pytest` passes with the same pass count as before this
feature — confirms this exploratory feature required no new automated
tests because it made no production-code change.

**Result**:
* `git diff --stat main -- build/ templates/ css/ content/ config/` —
  empty; confirms zero production files changed on `f04-site-redesign`.
* New files are all under `design-mockups/f04-site-redesign/` (3 HTML
  mockups + 3 screenshots), plus this feature's own tracking files
  (`03-features/notdone/F04-site-redesign.md`,
  `04-tasks/notdone/TF04-site-redesign.md`) and `02-doc/spec.md` (filled in
  separately, at the user's request, before this task list ran).
* `uv run pytest` — 78 passed, same count as the pre-feature baseline.
  No new tests needed; this feature is verified by the manual checks in
  TF04.2/TF04.3, not pytest.

## TF04.5 — Add Option D: futurism.com editorial homage
**Status**: not done
**Description**: User asked for a 4th option that specifically mimics
futurism.com's visual identity (not another "modern engineering" take).
Inspect the live page (`https://futurism.com/future-society/european-central-bank-economy-ai-investment-crash`)
for its real typography/color/layout system, then build
`design-mockups/f04-site-redesign/option-d-futurism-editorial.html` —
same standalone-mockup constraints as A–C (real BRH content/images, no
`build/`/`templates/` changes), applying that borrowed identity to the
home page and to the Pupper nav item. Update the published comparison
gallery artifact to include the 4th option.
**Test**: Manual — same Playwright check as TF04.2 (console/network
errors, all 6 nav entries present), plus a full-page screenshot added to
`screenshots/` and to the gallery, per `.claude/style_guide.md`'s
manual-test-notes convention.

**Result**:
* Inspected the live page with Playwright (computed styles + full-page
  screenshot, not just the markdown-stripped text): body/headline font
  family `owners-xnarrow` (licensed, not on Google Fonts) at weight 900
  for the H1 (48px, -0.5px tracking), cream body background
  `rgb(255,254,247)`, `rgb(248,248,248)` header bar, black text, a single
  red accent `rgb(255,0,51)` used for kicker labels/"Most Popular" tags,
  a red-uppercase kicker line above the headline ("VASSAL STATE"), an
  italic sub-headline/dek, a "By [author] / Published [date]" byline row,
  a full-bleed hero photo with italic caption, and a right-rail "Most
  Popular" box (red dot + underline header, category-tag + headline rows).
* Substituted `owners-xnarrow` with Google Fonts `Archivo Narrow` (400–900
  + italics) — a free condensed grotesk covering the same single-family,
  multi-weight, italic-capable role the real site uses, rather than
  picking an unrelated display face.
* Built `design-mockups/f04-site-redesign/option-d-futurism-editorial.html`:
  cream background, black condensed-grotesk headline treatment, red kicker/
  accent color, byline row, full-bleed hero photo
  (`images/meetings/meeting1-1.jpg`) with italic caption, a "What's New" +
  "Projects" story river (thumbnail + red category tag + bold headline +
  dek, one row per real news/project item, including the real Pupper talk
  announcement `images/news/pupper.png`), and a right rail reusing the
  site's real "Most Popular" pattern for "Upcoming Meetings" plus a Pupper
  promo card. Pupper's nav treatment borrows the source site's own
  internal contrast — italic, lighter-weight, red — rather than an
  unrelated font swap like directions A–C use.
* All copy is real, either verbatim or excerpted/reformatted from
  `content/heroes/index.md`, `content/about.md`, `content/news/`,
  `content/meetings/`, `content/projects/` — no invented content.
* Manual check via the same scratch Playwright script/approach as TF04.2:
  loaded via `file://`, 0 console errors, 0 failed requests (>=400), all 6
  nav entries (Home, Learn, Members, Projects, About, Pupper) present.
  Full-page screenshot saved to
  `screenshots/option-d-futurism-editorial.png` and added as a 4th tab in
  the published comparison gallery artifact.
