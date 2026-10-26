# TF18 Description for Feature F18

**Date Created:** 2026-10-26

## TF18.0 — Template for standalone pages
**Status**: done
**Description**:

- New `templates/pages/content-page.html`, extending `layouts/page.html`.
- Sets `current_page = 'about'` and puts the page `title` in `<title>`.
- Renders the page HTML in a content wrapper, reusing About's existing CSS class so there is no new CSS.

**Test**: covered by TF18.3's built-page tests. A template on its own has nothing to unit test.

**Result**:

- `templates/pages/content-page.html` renders the title as the first `h2` inside `.about-content`, so the page matches About's styling.

## TF18.1 — Build loop for `content/pages/`
**Status**: done
**Description**:

- Add a `build_content_pages` method that renders every `content/pages/*.md` file to `output/<slug>.html`, called from `build()`.
- Reuse `ContentManager`'s markdown processing. A missing `title` raises `ValueError` naming the file.
- **Placement**: `build/build.py` is already about 405 lines, past the ~300-line guideline. Keep the new method small (under ~20 lines). If it grows, put it in a new module rather than lengthening `build.py`.

**Test**: missing `title` raises; a fixture page renders to `<slug>.html`.

**Result**:

- `build_content_pages` in `build/build.py`, 16 lines, called right after `build_about_page`.
- Pages get `resolve_banner` from their own frontmatter, so a per-page banner override works with no extra code.

## TF18.2 — Move the speaker tips content
**Status**: done
**Description**:

- Move the "Tips for Speakers" section from `content/about.md` to `content/pages/speaker-tips.md`, with `title: Tips for Speakers`.
- In its place on About, add a short "Speaking at BRH" section that links to `speaker-tips.html`.

**Test**: covered by TF18.3.

**Result**:

- `content/pages/speaker-tips.md` holds the tips; its closing line links to `about.html#contact-us`.
- About's new "Speaking at BRH" section sits between Meeting Location and Contact Us.

## TF18.3 — Tests
**Status**: done
**Description**:

- New `tests/test_content_pages.py`:
  - Building the fixture tree produces `<slug>.html` containing the page title and body.
  - A page with no `title` raises `ValueError`.
  - The real build's `about.html` links to `speaker-tips.html`, and `speaker-tips.html` contains key phrases.
- Add any `conftest.py` fixture changes needed for a `content/pages/` directory.

**Test**: this task is the tests. `uv run pytest` and `ruff check` must pass.

**Result**:

- 4 tests in `tests/test_content_pages.py`; "Speaking at BRH" added to `test_about_content_preserved.py`.
- 202 passed; `ruff check` and `ruff format --check` clean.
