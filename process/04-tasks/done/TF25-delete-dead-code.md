# TF25 Delete dead code and Bootstrap leftovers for Feature F25
**Date Created:** 2026-11-05

## TF25.0 — Save a comparison build
**Status**: done

**Description**: Copy a build of the site outside `output/`, so later steps can be compared with it.

**Test**: not feasible, this step only saves a reference for TF25.6.

## TF25.1 — Delete unused CSS classes
**Status**: done

**Description**: Remove the listed `.btn`, `.card-*`, `.section-title`, `.detail-header*` and `.image-*` rules, including the `.card-title` and `.section-title` entries in the shared heading rule.

**Test**: the guard test from TF25.5 finds no unused classes, and `.detail-header__title` remains.

## TF25.2 — Delete unused CSS variables
**Status**: done

**Description**: Remove the listed variables from both theme blocks where they appear, and drop the two shadows from `DARK_MODE_VARS`.

**Test**: the guard test from TF25.5 finds no unused variables, and `tests/test_css_theme.py` still passes.

## TF25.3 — Delete unused code
**Status**: done

**Description**: Remove `image_classes` from `render_news_cards`, the smooth-scroll handler from `scripts/script.js`, and the `extra_head` block from `layouts/base.html`.

**Test**: Home's news cards render the same in the build comparison, and `scripts/script.js` still has the theme toggle.

## TF25.4 — Clear the Bootstrap leftovers
**Status**: done

**Description**: Rename `data-bs-theme` to `data-theme` everywhere. Remove the listed `!important` rules and `min-height: auto`, the two stale allowed colors, and the outdated comment wording.

**Test**: `data-bs-theme` appears nowhere in `css/`, `templates/`, `scripts/` or `tests/`, and the only `!important` left in the CSS is in the article image rule.

## TF25.5 — Write the feature's tests
**Status**: done

**Description**: Add `tests/test_no_dead_css.py`, with the guard for unused classes and variables and the checks from TF25.1 to TF25.4. Rename `test_base_template_syncs_bootstrap_theme`, and update tests that name the old attribute.

**Test**: `uv run pytest` passes in full.

## TF25.6 — Compare with the saved build
**Status**: done

**Description**: Diff all HTML against the TF25.0 build, and record how many CSS lines were removed.

**Test**: the HTML differs only in the attribute rename and whitespace.

## TF25.7 — Check it in a browser
**Status**: done

**Description**: Run the F25 demo in both themes, including the theme toggle. Removing `!important` could only affect `.card`, `.member-projects` and `.page-intro`, so look at Members, a Projects page intro and member cards.

**Test**: not feasible to automate, so the user signs off on how it looks.
