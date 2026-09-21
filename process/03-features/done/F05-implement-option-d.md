# F05 — Implement Option D (Futurism editorial) in the real site
**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* Brings F04's "Option D" mockup (`design-mockups/f04-site-redesign/option-d-futurism-editorial.html`
  — the futurism.com editorial homage) into the live Jinja2/CSS site,
  replacing the current Bootstrap-based look, on the existing
  `f04-site-redesign` branch.
* User-confirmed scope (clarifying questions asked and answered before this
  file was written): start with **sitewide theme + home page**, but design
  the task list as phases that gradually extend Option D to the *entire*
  site within this same feature, rather than stopping after the home page.
* Phase 1 (this session's target): re-theme `css/shared.css`'s CSS custom
  properties (palette, both light and dark) and typography to Option D's
  system, keeping the existing variable *names* so every page that already
  references them (`.card`, `.btn`, links, footer, etc.) inherits the new
  look immediately with near-zero HTML risk. Redesign the shared
  `navigation.html` (adds Pupper as a 6th entry) and `footer.html`. Fully
  rebuild the home page's content structure (lead block, hero photo,
  What's New / Projects story rivers, Upcoming Meetings + Pupper rail) by
  restyling the *existing* card partials (`templates/cards/*.html`,
  `upcoming-meetings-calendar.html`) rather than changing
  `build/page_builder.py`'s data pipeline.
* Phase 2 (later steps, same task list): extend the story-row/kicker/byline
  visual language to every remaining page — Learn, Members (listing +
  detail), Projects (listing + detail, including Pupper's own project
  page), What's New (listing + detail), Meetings (listing + detail),
  About.
* Phase 3 (final steps): once no template references Bootstrap classes,
  remove the Bootstrap CSS/JS/Icons CDN from `head.html` entirely and
  replace the theme-toggle's Bootstrap Icon with a small inline SVG.
* **Dark/light toggle preserved**: F01's mechanism (`data-bs-theme`
  attribute, `#theme-toggle` button, `localStorage`) stays exactly as-is
  structurally — this feature designs an Option-D *dark* palette (cream
  flips to near-black, red accent kept, ink/text adjusted for contrast)
  the same way TF01.1 added dark counterparts for every light variable.
* **QR signup CTA preserved** (user's answer): F03's generated QR code
  stays on the home page, restyled to the new palette — not replaced by
  Option D mockup's simpler text-link CTA.
* **Pupper nav item** (user's answer): links directly to the existing
  generated detail page for `content/projects/pupper.md`
  (`projects/pupper.html`, confirmed via a real build) — no new template
  in this feature. A dedicated Pupper page/template is left for a future
  feature if wanted later.
* No content is dropped anywhere — every existing news/meeting/project/
  member entry, and every existing page, keeps rendering; only markup/CSS/
  fonts/colors change, plus the one new Pupper nav link.
* Keep the HTML/CSS as simple as possible; Bootstrap is not required for
  any newly-written markup (existing pages not yet reached by a given
  phase may keep using it until their own phase lands).

**Non-goals**:
* A dedicated standalone Pupper page/template — deferred; Pupper links to
  its existing project detail page for now.
* Removing Bootstrap before every page has actually been re-skinned
  (Phase 3 is contingent on Phases 1–2 fully landing first).
* Redesigning content itself (copy, photos, data) — visual/structural
  only.
* Options A, B, C from F04 — this feature implements Option D only.

## How to Demo
**Setup**: On branch `f04-site-redesign`, run `uv run python build/build.py`,
then serve `output/` locally (e.g. `python3 -m http.server 8000 --directory
output`) and open it in a browser.

**Steps**:
1. Open the home page. Confirm it matches Option D's structure: wordmark +
   uppercase nav (with Pupper as a distinct 6th entry) + theme toggle,
   lead block (kicker/headline/dek/byline), hero photo, "What's New" and
   "Projects" story rivers, and an "Upcoming Meetings" + Pupper rail —
   all real content, nothing invented.
2. Click the Pupper nav link — confirm it opens the real Pupper project
   detail page.
3. Confirm the QR signup code is still present on the home page, restyled
   to the new cream/red/ink palette.
4. Toggle dark/light mode — confirm the whole page (not just the home
   page) recolors correctly and stays legible in both.
5. Browse every other page (Learn, Members, Projects, About, What's New,
   Meetings, and one detail page per type). Once Phase 1 alone is done,
   confirm they show the new nav/footer/palette/type but keep their
   current Bootstrap-based content layout; once Phase 2 lands, confirm
   their content structure matches Option D's system too.
6. Confirm no page shows a broken image or a console/network error.

**Expected output**: The real site visually matches Option D, phased in
per the task list, with zero content loss and the dark/light toggle and
QR signup CTA both still working.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
