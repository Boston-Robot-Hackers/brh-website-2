# TF23 Simplify hero content for Feature F23
**Date Created:** 2026-11-05

## TF23.0 — Save a comparison build
**Status**: not done

**Description**: After F22 is committed, copy a build of the site outside `output/`, so later steps can be compared with it.

**Test**: not feasible, this step only saves a reference for TF23.6.

## TF23.1 — Remove the unused hero files
**Status**: not done

**Description**: Delete `community.md` and `whatsnew.md` from `content/heroes/`. `build_news_page` passes `hero={}` and calls `resolve_banner({})`.

**Test**: What's New builds with no hero section and the default banner.

## TF23.2 — Reduce hero files to their body
**Status**: not done

**Description**: Remove `title` and `subtitle` from hero files, and make `build_hero_content` return only the body. Update `hero.html` and `home-lead.html` to match.

**Test**: a hero file's body comes back as HTML, and a missing file still raises `FileNotFoundError`.

## TF23.3 — Remove banner fields from hero handling
**Status**: not done

**Description**: Drop `banner_*` from `build_hero_content`, and main pages call `resolve_banner({})`. Detail page overrides stay.

**Test**: main pages get the site default banner, and the Pupper detail page keeps its override.

## TF23.4 — Render the "Next…" line from the template
**Status**: not done

**Description**: `build_index` passes the rendered line to `home-lead.html`, which also takes over the `<hr/>`. Remove `generate_index_hero` and the `<hr/>` in `content/heroes/index.md`.

**Test**: Home shows the mission paragraph, then the line with the next two meetings and their links.

## TF23.5 — Remove unused CSS and update docs
**Status**: not done

**Description**: Remove the `.hero` rules that match nothing, and `.hero-title`. Update the hero row in `README.md`, and rescope F14's proposed helper to the simpler hero code.

**Test**: `tests/test_css_theme.py` still passes. Appearance is checked in TF23.7.

## TF23.6 — Write the feature's tests
**Status**: not done

**Description**: Add the tests from TF23.1 to TF23.4, and remove the tests for `generate_index_hero` and for hero banner fields and titles. Add build tests that the Meetings intro and Home's "Next…" line render, since no test covers them today.

**Test**: `uv run pytest` passes in full, and the top-level pages match the TF23.0 build apart from whitespace.

## TF23.7 — Check it in a browser
**Status**: not done

**Description**: Run the F23 demo, looking at Home and Meetings in both themes.

**Test**: not feasible to automate, so the user signs off on how it looks.
