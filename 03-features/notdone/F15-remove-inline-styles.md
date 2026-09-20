# F15 — Move remaining inline styles into CSS classes
**Priority**: Low
**Done:** no
**Tasks File Created:** no
**Tests Written:** no
**Test Passing:** no

**Description**:
* Found during a code/architecture deep-dive review (session on the
  `deepdive` branch). Not a bug — pages render correctly today in both
  themes. This is a consistency observation.
* The codebase otherwise has a deliberate, consistently-applied
  CSS-variable-based theming system (`--primary`, `--bg-card`, `--text`,
  `--border`, etc., defined once and swapped for dark mode), enforced in
  part by `tests/test_css_theme.py` (which already caught and rejected
  hardcoded hex colors during earlier work this session, e.g. the
  slides-download button's original `#f59e0b`/`#10b981` had to be
  switched to `var(--accent)`/`var(--success)`).
* A handful of `style="..."` attributes bypass that system by hardcoding
  layout values directly in templates instead of using a class governed
  by the CSS variable system. Confirmed via grep, 6 occurrences across 3
  files:
  * `templates/components/banner.html` — inline
    `style="background-image: url(...)"` (this one is inherently
    per-page dynamic data, likely stays inline or moves to a CSS custom
    property set inline, e.g. `style="--banner-image: url(...)"` with
    the rest of the rule in CSS).
  * `templates/details/meeting-detail.html` — inline `style="opacity:
    0.5; cursor: default;"` on the two disabled "Announcement
    TBD"/"Report TBD" buttons, and a `<style>` block embedded directly
    in the template body for `.meeting-resources` layout rules that
    could live in `css/main.css` instead.
  * `templates/pages/meetings.html` — inline `style="display: flex;
    align-items: baseline; gap: 1rem; flex-wrap: wrap;"` and `style=
    "margin: 0;"` on the page header, plus a `<style>` block for
    `.meetings-controls` (the sort/filter bar) that could also move to
    `css/main.css`.
* **Proposed fix**: for each of the non-dynamic cases (everything except
  the per-page banner image), add a small named class to `css/main.css`
  (or `shared.css` if it's a cross-page pattern) and reference it from
  the template instead of the inline `style=`. The banner image case
  can either stay as-is (it's legitimately per-instance dynamic data,
  not a style choice) or move to a CSS custom property pattern if the
  team wants total consistency.

**Non-goals**:
* Not a visual redesign — every rule moves verbatim from inline `style=`
  or an embedded `<style>` block into `css/main.css`; no new colors,
  spacing, or layout choices.
* Not touching the per-page banner background-image mechanism's
  fundamental approach (F09's dynamic banner feature) — only how much of
  it lives inline vs. in the stylesheet.

## How to Demo
**Setup**: `uv run python build/build.py`, open the affected pages
(`meetings.html`, any meeting detail page, any page with a banner) in
both light and dark mode, before and after the change.

**Steps**:
1. Visual diff before/after — pixel-identical rendering in both themes.
2. `uv run pytest` — `test_css_theme.py` and every content-preservation
   test still pass.
3. Grep for `style="` in `templates/` afterward — occurrences drop to
   just the genuinely-dynamic banner-image case (or zero, if that one is
   also converted to a CSS custom property).

**Expected output**: No visible change to any page; inline styles that
used to bypass the theme system are now expressed the same way as every
other style rule in the codebase.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
