# TF06 Description for Feature F06

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF06.N`, starting at `.0`.

## TF06.0 — Reference research
**Status**: done
**Description**: Look at 2-3 real examples of how editorial/news sites
present a single article page (byline placement, pull-quote/lead
treatment, image captioning, related-content patterns) — building on the
same real-world research already used for Option D (futurism.com) plus
1-2 more. Record concrete, nameable structural/typographic ideas each
option below will draw from, not just a vibe.
**Test**: N/A — research step, not a behavior change. Findings recorded
as this task's completion evidence.

**Result**: Two real references, inspected live (Playwright, not just
scraped text):
* **futurism.com** (already deeply analyzed for Option D) — magazine/
  tabloid style: kicker, huge bold headline, italic dek, full-bleed hero
  photo, minimal byline.
* **github.blog/engineering** (new) — technical-blog style: dark title
  band, byline row with reading-time estimate + share icons below a
  square hero image, then a **two-column body**: main content + a right
  sidebar with a **table of contents** (jump links to real headings),
  topic tags, and a related-posts module. Concretely different structural
  idea from Futurism's single-column magazine approach.
* Option 1 below draws on Futurism's single-column magazine feature;
  Option 2 draws on GitHub Blog's two-column sidebar-with-ToC approach.

## TF06.1 — Confirm real content shape available to design with
**Status**: done
**Description**: Re-confirm exactly which fields a real news post
provides (`post.title`, `post.date`, `post.image`, `post.excerpt`,
`post.content`, `formatted_date`, plus `back_link`/`back_text`) via
`build/page_builder.py`/`content_manager.py`, and pick one real,
already-published post (with a real image) both options will use — so
neither option invents content or a field that doesn't exist.
**Test**: N/A — confirms available fields via reading existing code, no
behavior change.

**Result**:
* No `author` field exists anywhere in `content/news/*.md` frontmatter —
  confirmed neither option can show a byline name (unlike both real
  references). Using real dates/reading-time (computed from real word
  count) instead.
* Markdown is processed with the `toc` extension already on
  (`content_manager.py`), which auto-adds `id=` to every heading in real
  built output (confirmed: `output/news/24-ankush-dhawan-*.html` has
  `id="meeting-announcement"`, `id="agenda"`, `id="featured-talk"`) — a
  real, already-working table-of-contents anchor target for Option 2, not
  a new feature to invent.
* Both options use `content/news/24-ankush-dhawan-talk-announcement.md`
  (the "Meet Pupper" post) — real image, real excerpt, 3 real headings,
  ties into the Pupper theme already prominent elsewhere on the site.

## TF06.2 — Build Option 1 mockup
**Status**: done
**Description**: Standalone HTML mockup
(`design-mockups/f06-news-detail-redesign/option-1.html`) for the chosen
real post, applying one of TF06.0's reference ideas while staying on the
site's established Option D palette/type/nav/footer.
**Test**: Manual — real-browser check (Playwright), console/network
errors, both themes if the option's design supports it. Recorded per
`.claude/style_guide.md`'s manual-test-notes convention.

**Result**:
* `option-1-magazine.html` — single-column magazine feature: full-bleed
  hero photo, kicker/headline/dek, a red-rule pull-quote pulled from real
  body text, back-to-What's-New button.
* Links the real `../../css/shared.css`/`main.css` directly (no invented
  palette/type) and reproduces the real nav/footer verbatim; only new CSS
  is the layout-specific `.article-magazine*` rules.
* Playwright check: 0 console/network errors, light + dark both render
  correctly (screenshots in `screenshots/option-1-magazine-{light,dark}.png`).

## TF06.3 — Build Option 2 mockup
**Status**: done
**Description**: A second standalone HTML mockup
(`design-mockups/f06-news-detail-redesign/option-2.html`) for the *same*
real post, meaningfully different from Option 1 (different structural
idea from TF06.0's research, not just a color/spacing tweak), same theme
constraints.
**Test**: Manual — same as TF06.2.

**Result**:
* `option-2-brief.html` — two-column technical brief: compact non-full-bleed
  hero thumbnail beside the byline/excerpt, then a body/sidebar grid with a
  real sticky table-of-contents (jump links to the 3 real heading `id`s)
  and the back link, collapsing to one column under 720px.
* Same real CSS links/nav/footer reuse as Option 1; only new CSS is the
  layout-specific `.brief-*` rules.
* Playwright check: 0 console/network errors, light + dark both render
  correctly (screenshots in `screenshots/option-2-brief-{light,dark}.png`).

## TF06.4 — Comparison view + present to user
**Status**: done
**Description**: Screenshot both options (full-page, matching F04's
approach) and assemble a comparison (reuse/extend the existing published
gallery artifact pattern from F04, or a new small comparison page) so the
user can review both side by side before any implementation decision.
**Test**: Manual — visual comparison confirms both render as intended;
recorded per the style guide's convention.

**Result**: Full-page screenshots taken for both options in both themes
(4 PNGs in `screenshots/`); reviewed directly, both stay on the Option D
palette/type/nav/footer and differ only in layout as the user specified.
Presenting both mockup files to the user directly for review (no separate
gallery artifact needed for a 2-option comparison).

## TF06.5 — Verification: no production files touched
**Status**: done
**Description**: Dedicated test-writing task. Like F04, this feature ships
no code — confirm via `git status`/`git diff --stat` against `main` that
only files under `design-mockups/f06-news-detail-redesign/` (plus this
feature's own tracking docs) changed, so `uv run pytest` is unaffected.
**Test**: `uv run pytest` passes with the same pass count as before this
feature — confirms no production-code change required a new automated
test.

**Result**: `git diff --stat HEAD` excluding `design-mockups/`,
`03-features/`, `04-tasks/` is empty — no production file touched.
`uv run pytest` still passes 107/107, same count as before this feature.
