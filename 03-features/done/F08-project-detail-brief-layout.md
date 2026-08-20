# F08 — Apply the "technical brief" layout to the project detail page
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* F07 rebuilt the news detail page to a two-column "technical brief"
  layout: compact header, article body, and a real sidebar table of
  contents built from the post's own headings. The user wants the same
  treatment applied to the project detail page
  (`templates/details/project-detail.html`).
* Real project content supports it: of 9 real projects, 6 have real
  `##`/`###` headings (e.g. `pupper.md`'s Overview/What is Pupper
  v3?/The Boston Build Team/Our Mission in Boston/Get Involved, or
  `dome-robot.md`'s Software/Hardware) — the same generic `toc_tokens`/
  `reading_time` fields F07 added to `content_manager.py` already cover
  every content type, so project posts get them for free, no backend
  change needed.
* This is a smaller change than F07 in one way and larger in another:
  * Smaller — no new backend fields needed.
  * Larger — the project header carries more than news does (a status
    badge, a Started/Team/Lead/GitHub meta bar, an optional members
    list), so the header needs to fit those in rather than a straight
    copy of the news header.
* Refactor `css/main.css`'s `.news-brief-*` classes to generic
  `.detail-brief-*` (rename, no visual change to news) so both news and
  project detail share one CSS pattern instead of duplicating it —
  `templates/details/news-detail.html` updates to match.
* The project's existing `status` badge becomes the brief header's
  kicker line (visually identical treatment, one less class); the
  existing `Started:`/`Team:`/`Lead:`/`GitHub:` meta bar and the members
  list stay as their own already-working components, placed between the
  new header and the two-column body.

**Non-goals**:
* Meeting/member detail pages — out of scope, stay on `.detail-header*`.
* Any new project content fields.

## How to Demo
**Setup**: `uv run python build/build.py`, open in a browser:
`output/projects/pupper.html` (5 real top-level headings),
`output/projects/dome-robot.html` (2 headings, no `##` level at all —
confirms level-relative nesting), `output/projects/midi.html` (no
headings — confirms the no-sidebar collapse).

**Steps**:
1. Confirm Pupper/dome-robot show the two-column layout: compact header
   (status kicker, title, image, excerpt), the existing meta bar and
   members list unchanged, then body + real sidebar ToC.
2. Confirm `midi.html` renders single-column, no dead sidebar space.
3. Toggle dark/light.
4. Confirm news/meeting/member detail pages are visually unchanged.

**Expected output**: Project detail pages use the same two-column
technical-brief shell as news, with a real per-project table of contents;
every other page is unaffected.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
