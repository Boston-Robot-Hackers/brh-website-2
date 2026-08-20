# F07 — Implement Option 2 ("Technical brief") on the real news detail page
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* F06 produced two on-theme mockup options for the news detail page; the
  user picked **Option 2** (`design-mockups/f06-news-detail-redesign/option-2-brief.html`,
  the "technical brief" two-column layout with a sidebar table of
  contents) to implement for real.
* Real implementation differs from the mockup in two ways the mockup
  faked with static content:
  * **Table of contents** — the mockup hand-wrote 3 links for one known
    post. The real site has 24 news posts with varying heading counts (0
    to 6+, mixed `##`/`###`/`####` depth). The ToC must be generated from
    each post's real headings via `python-markdown`'s already-active
    `toc` extension (`toc_tokens`), not hard-coded, and must disappear
    cleanly for a post with no headings.
  * **Reading time** — the mockup hard-coded "2 min read". The real site
    has no such field; compute it from real word count (~200 wpm) in
    `build/content_manager.py` alongside `toc_tokens`, for every content
    type that goes through `process_markdown_file` (harmless to add
    generically; only news-detail consumes it in this feature).
* Rebuild `templates/details/news-detail.html` to the Option 2 markup
  (compact non-full-bleed header image, two-column body/sidebar grid,
  collapsing to one column under 720px) and add its CSS to `css/main.css`,
  scoped under new class names so `meeting-detail.html`/`project-detail.html`/
  `member-detail.html` (which keep the existing `.detail-header*`/
  `.detail-article` shared system) are unaffected.
* The mockup's sidebar also duplicated a "Back to What's New" link; the
  real page already gets one from `layouts/detail.html`'s shared
  `.detail-back` block below the content, so the real sidebar carries the
  ToC only — no duplicate link.

**Non-goals**:
* Redesigning meeting/project/member detail pages — out of scope, must
  render unchanged.
* A "related posts" module or any other content the real data doesn't
  support (unchanged from F06's decision).

## How to Demo
**Setup**: `uv run python build/build.py`, open `output/news/24-ankush-dhawan-talk-announcement.html`
(has 3 real headings) and one short post with none, e.g. a post with a
single paragraph and no `###` headings, in a browser.

**Steps**:
1. Confirm the Pupper post shows the two-column brief layout: compact
   header image + meta row (date, reading time) + excerpt, then body with
   a sidebar ToC linking to its 3 real headings, matching the approved
   Option 2 mockup's visual treatment.
2. Confirm a heading-less post renders single-column with no empty
   sidebar box.
3. Toggle dark/light — confirm it matches the rest of the site.
4. Confirm meeting/project/member detail pages are visually unchanged.

**Expected output**: News detail pages use the Option 2 two-column
technical-brief layout with a real, per-post table of contents and a real
computed reading time; every other page is unaffected.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
