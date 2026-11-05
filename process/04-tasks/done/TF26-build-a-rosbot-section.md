# TF26 Build-A-ROSBot section for Feature F26
**Date Created:** 2026-11-05

## TF26.0 — Load and validate the section's content
**Status**: done

**Description**:

- New `build/rosbot_builder.py` with functions that load `content/rosbot/sessions/*.md` and `content/rosbot/resources/*.md` using `ContentManager.process_markdown_file`.
- Check the required frontmatter: `title` and `session` for sessions, `title` for resources. Reject duplicate session numbers.
- Sort sessions by `session`, and resources by `order`, then `title`.

**Test**: fixture files load in the right order. A missing `title`, a missing `session` and a duplicate `session` each raise `ValueError` naming the file.

**Result**:

- A `RosbotSection` class holds the content manager and page builder.
- `session` and an optional `order` must be integers; a string or a bool raises.
- Resources with an `order` come first, and the rest are sorted by title.

## TF26.1 — Session and resource page templates
**Status**: done

**Description**:

- New `templates/details/rosbot-session-detail.html`: "Session N: title", the optional date, the body, previous and next links, and a link back to the overview.
- New `templates/details/rosbot-resource-detail.html`: title, body, and a link back to the overview.
- Both set `current_page = 'rosbot'` and `is_detail_page = true`. They reuse existing detail-page CSS classes where they fit, so new CSS stays minimal.

**Test**: covered by TF26.2's build tests. A template on its own has nothing to unit test.

**Result**:

- Both reuse the `detail-brief-header` and `detail-brief-body` classes from the project and news pages.
- The only new CSS is the `.rosbot-pager` rules for the previous and next links.

## TF26.2 — Build the section's pages
**Status**: done

**Description**:

- In `rosbot_builder.py`, render each session to `output/rosbot-sessions/<slug>.html` with the previous and next links filled in, and each resource to `output/rosbot-resources/<slug>.html`.
- Render `content/rosbot/overview.md` to `output/rosbot.html` with a new `templates/pages/rosbot.html`. It shows the overview body, then the generated Sessions and Resources lists.
- `build/build.py` gets only one call to the new module.

**Test**: building the fixture tree produces all three kinds of page. The overview lists every session in order and every resource. The first session has no Previous link and the last has no Next link.

**Result**:

- The overview reuses About's `about-content` wrapper and adds the `.rosbot-list` rules.
- A Sessions or Resources heading is left out when its folder is empty.
- `build.py` gains one import and one call, right after `build_content_pages`.

## TF26.3 — Featured-program nav link
**Status**: done

**Description**:

- Add a "Build-A-ROSBot" link to `templates/components/navigation.html` after Pupper. It gets the `active` class when `current_page == 'rosbot'`.
- Give both featured links one shared class, `site-nav__featured-link`, in place of the Pupper-only `site-nav__pupper-link`, and add an active state. The Pupper photo rule stays as it is.
- Check the nav at phone width, since it gains another item.

**Test**: the nav on top-level and detail pages links to `rosbot.html` with the right `../` prefix, and is active on all pages in the section. `tests/test_no_dead_css.py` still passes. Phone width is checked by eye, since there's no layout test for wrapping.

**Result**:

- The active state is a `2px` underline in `--primary`, the same as the regular nav links.
- `tests/test_no_dead_css.py` is F25's and isn't on this branch, so it hasn't been run against these changes. It will run once F25 is merged.
- Phone width checked by eye by the user on 2026-11-05, and it looks fine.

## TF26.4 — Starter content
**Status**: done

**Description**:

- `content/rosbot/overview.md` with a short placeholder program description.
- Two placeholder session files and one placeholder resource file, each with a one-line "to be written" body. They show the frontmatter format for the user to copy.
- A `_template.md` in each folder, like `content/projects/_template.md`, skipped by the build.

**Test**: covered by TF26.5's real-build check. Skipping `_template.md` gets its own test there.

**Result**:

- Sessions: `01-getting-started.md` and `02-first-motion.md`. Resource: `parts-list.md`.
- Each `_template.md` lists the required and optional fields in YAML comments.

## TF26.5 — Write the feature's tests
**Status**: done

**Description**:

- New `tests/test_rosbot_section.py` covering TF26.0's loading and validation and TF26.2's fixture build.
- Extend the nav tests (`tests/test_navigation.py` or `tests/test_nav_logo.py`, wherever the Pupper link is covered) with the new link, its prefix, and its active state.
- Real-build check: `rosbot.html` and the starter session and resource pages exist, and `_template.md` produces no page.

**Test**: this task is the tests. `uv run pytest` and `ruff check` must pass.

**Result**:

- `tests/test_rosbot_section.py` has 17 tests. The real-content check writes to a temp directory, not the real `output/`.
- `tests/test_navigation.py` checks the new link's `../` prefix, its active condition, and that it comes after Pupper.
- Full suite: 292 passed. `ruff check` is clean.
