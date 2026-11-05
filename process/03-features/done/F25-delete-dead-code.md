# F25 — Delete dead code and Bootstrap leftovers
**Priority**: Medium
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Remove the code the 2026-11-05 HTML and CSS audit found to be unused, along with what's left over from Bootstrap.
* **Rendered pages stay the same.** This is a cleanup, not a redesign.

**Unused CSS classes**:

* `.btn`, `.card-body`, `.card-title` and `.section-title`.
* `.detail-header`, `.detail-header-img`, `.detail-header-thumb`, `.detail-header__meta` and `.detail-header__excerpt`. `.detail-header__title` stays, because the member detail page uses it.
* `.image-base`, `.image-square` and `.image-rectangle`, including their hover, media query and accessibility rules.

**Unused CSS variables**:

* `--secondary`, `--shadow-xl` and `--space-1` to `--space-5`.
* `--shadow-md`, whose only use goes away with `.btn`.
* `DARK_MODE_VARS` in `tests/test_css_theme.py` stops requiring the two shadows.

**Unused code**:

* `image_classes` in `render_news_cards`. No template reads it, and it holds the last Bootstrap class names.
* The nav's smooth-scroll handler in `scripts/script.js`. No nav link starts with `#`.
* The `extra_head` block in `layouts/base.html`, which no page fills.

**Bootstrap leftovers**:

* **Rename `data-bs-theme` to `data-theme`** in the CSS, `layouts/base.html`, `scripts/script.js` and tests. Saved choices aren't affected, because `localStorage` keeps them under `theme`.
* Remove the `!important` from `.card`, `.member-projects` and `.page-intro`, and the no-op `min-height: auto`. No rule competes with them.
* **The `!important` rules F24 added for article images stay.** They override inline styles in content files, until those styles are replaced.
* Remove `#1e293b` and `#334155` from the colors `tests/test_css_theme.py` allows, since the nav design they belonged to is gone.
* Update comments that mention Bootstrap, or that name `--secondary`.

**A guard against new dead code**:

* A new test fails if `css/main.css` or `css/shared.css` defines a class that nothing uses, or a variable that nothing reads.

**Non-goals**:

* No shared styles, font scale or breakpoint scale.
* No template tidying.
* No changes to content files.
* The `bi-*` icon names in `components/icons.html` stay, since they're only lookup names.
* No removal of "Option D" comments, which aren't dead code.

## How to Demo
**Setup**: a build of the current site saved for comparison, then `make try`.

**Steps**:

1. Compare all HTML in `output/` with the saved build.
2. Compare the size of `css/main.css` and `css/shared.css` with the saved build.
3. Open Home, Projects, Members and a member page in both themes, and use the theme toggle.
4. Run `uv run pytest`.

**Expected output**:

* The HTML differs only in the attribute rename and whitespace.
* The CSS is smaller, and pages look the same in both themes.
* The theme toggle still works and remembers its choice.
* All tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
