# TF27 Shared CSS styles, scales and file split for Feature F27
**Date Created:** 2026-11-05

## TF27.0 — Save the before state
**Status**: done

**Description**: Save a build outside `output/`, and record the CSS line and declaration counts. Write the screenshot script, and take before screenshots of every page at 375px and 1200px in both themes.

**Test**: not feasible, this step only saves a reference. The first script version turned out to shoot dark only and wider than 375px. The fixed version loads each page in an iframe of the exact width and sets the color scheme explicitly, and a probe confirmed both.

## TF27.1 — Add the font size scale
**Status**: done

**Description**: Define the seven `--fs-*` sizes, and replace each `font-size` with the nearest one, apart from the listed exceptions.

**Test**: `test_font_sizes_come_from_the_scale`.

## TF27.2 — Reduce the breakpoints to three
**Status**: done

**Description**: Move each media query to 620, 760 or 980px, and merge queries that end up at the same width in the same part of the file.

**Test**: `test_only_three_breakpoints`.

## TF27.3 — Let text inherit its color
**Status**: done

**Description**: Remove the color from the global `p`, `li` and `blockquote` rule. Set muted color once on containers that currently set it on each child.

**Test**: `test_text_inherits_its_color`.

## TF27.4 — Add the `.label` class
**Status**: done

**Description**: Add `.label` and `.label--muted`, use them in the templates, and trim the old label rules down to what's unique to each.

**Test**: `test_labels_share_one_style` and `test_built_pages_use_the_shared_classes`.

## TF27.5 — Add the `.section-heading` class
**Status**: done

**Description**: Add `.section-heading`, use it in the templates, and include `.about-content h2` in the same rule.

**Test**: `test_section_headings_share_one_size_and_rule`.

## TF27.6 — Add the `.placeholder` class
**Status**: done

**Description**: Add `.placeholder`, use it for missing-image boxes, and trim the old rules.

**Test**: the dead-CSS guard fails if the old fallback rules come back unused, and existing page tests still find each fallback's text.

## TF27.7 — Split the CSS into four files
**Status**: done

**Description**: Move every rule into `base.css`, `layout.css`, `components.css` or `pages.css`, and delete `main.css` and `shared.css`. Update `head.html`, `copy_css_files` and the tests that read CSS.

**Test**: `test_pages_link_the_four_stylesheets_in_order`, `test_old_stylesheets_are_gone` and `test_copies_every_css_file`.

## TF27.8 — Make near-identical styles identical
**Status**: done

**Description**: The ten changes the user approved on 2026-11-05: `.panel`, `.detail-title`, one label size, one section heading size, the two rule tokens, `.note`, `.meta`, shared button sizing, one muted grey and two corner radii.

**Test**: `test_borders_use_the_two_rule_tokens`, `test_corner_radii_are_limited`, `test_one_muted_grey`, `test_buttons_share_size_and_type`, `test_small_grey_text_uses_the_note_style`, `test_boxes_use_the_panel_style` and `test_detail_pages_share_one_title_style`.

## TF27.9 — Write the feature's tests and measure
**Status**: done

**Description**: Add the tests from TF27.1 to TF27.8 in `tests/test_css_structure.py`. Record the new line and declaration counts against TF27.0.

**Test**: `uv run pytest` passes in full: 305 tests. Counts went from 1,588 lines and 831 declarations to 1,523 and 713.

## TF27.10 — Compare screenshots
**Status**: done

**Description**: Take after screenshots and compare them with the before set. Every page differs, because the nav text size changed slightly, so the comparison is by eye with side-by-side images.

**Test**: side-by-side review of Home, Meetings, a news page, a member page, Learn, Projects (dark) and Members (phone). Differences match the plan: small size and spacing shifts, thinner divider lines, lighter grey for the Home mission text, the Learn card shadow, and the shorter phone nav.

## TF27.11 — Check it in a browser
**Status**: done

**Description**: Run the F27 demo, focusing on the changes listed in TF27.10.

**Test**: not feasible to automate, so the user signs off on how it looks.
