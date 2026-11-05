# TF23 Remove the hero concept for Feature F23
**Date Created:** 2026-11-05

## TF23.0 — Save a comparison build
**Status**: done

**Description**: Copy a build of the current site outside `output/`, so later steps can be compared with it.

**Test**: not feasible, this step only saves a reference for TF23.6.

## TF23.1 — Move the Home text
**Status**: done

**Description**: Move the mission paragraph to `content/home.md`, without the `<hr/>`. `build_index` loads it and passes it to `home-lead.html`.

**Test**: Home shows the mission paragraph, and a missing `content/home.md` raises `FileNotFoundError`.

## TF23.2 — Render the "Next…" line from the template
**Status**: done

**Description**: `build_index` passes the rendered line to `home-lead.html`, which also takes over the `<hr/>`. Remove `generate_index_hero`, and rename `upcoming-meetings-hero.html` to `upcoming-meetings-next.html`.

**Test**: Home shows the mission paragraph, then the line with the next two meetings and their links.

## TF23.3 — Move the remaining intros into page templates
**Status**: done

**Description**: Replace the `hero.html` include in `layouts/page.html` with an empty `intro` block. Fill it, word for word, in the Meetings and Projects templates. The markup is a `.page-intro` section holding a `.page-intro__inner` div. The About, Learn and Members intros are not moved. Chore 46 later removed the Meetings intro at the user's request.

**Test**: Meetings and Projects show their intros, and About, Learn, Members, What's New and content pages have no intro section.

## TF23.4 — Remove hero handling from the build
**Status**: done

**Description**: Delete `build_hero_content`, `components/hero.html` and `content/heroes/`. Remove `hero=` from every build call, and main pages call `resolve_banner({})`. Detail page overrides stay.

**Test**: main pages get the site default banner, and the Pupper detail page keeps its override.

## TF23.5 — Rename the CSS and update docs
**Status**: done

**Description**:

* Rename `.hero` and `.hero-section` to `.page-intro` and `.page-intro__inner`, and remove `.hero-title` and rules that match nothing.
* Update `README.md`, the Home entry in `spec.md`, and the "hero" wording in the comments of `layouts/page.html`, `layouts/home.html` and `pages/about.html`.
* Rescope F14, whose proposed helper wraps `build_hero_content`.

**Test**: `tests/test_css_theme.py` still passes. Appearance is checked in TF23.7.

## TF23.6 — Write the feature's tests
**Status**: done

**Description**:

* Add the tests from TF23.1 to TF23.4.
* Remove the tests for `generate_index_hero` and `build_hero_content`, and the `heroes` fixtures in `tests/conftest.py`.
* Point `test_signup_links_match_signup_url` in `tests/test_signup_qr.py` at `content/home.md`, so the signup link stays covered.
* Add build tests that the Meetings intro and Home's "Next…" line render, since no test covers them today.

**Test**: `uv run pytest` passes in full, and the top-level pages match the TF23.0 build apart from whitespace, the renamed classes and the three cut intros.

## TF23.7 — Check it in a browser
**Status**: done

**Description**: Run the F23 demo, looking at Home, Meetings and a page with a cut intro (About) in both themes.

**Test**: not feasible to automate, so the user signs off on how it looks.
