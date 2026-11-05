# TF24 Fix layout and accessibility bugs for Feature F24
**Date Created:** 2026-11-05

## TF24.0 — Save a comparison build and screenshots
**Status**: done

**Description**: Copy a build outside `output/`, and take screenshots of Home, Meetings, a news page and a member page at 1200px.

**Test**: not feasible, this step only saves a reference for TF24.7.

## TF24.1 — Fix the sticky nav on phones
**Status**: done

**Description**: Make the nav non-sticky at 980px and below. Reduce the wordmark size and gaps at 620px and below.

**Test**: a CSS check that `.site-nav` is `position: static` at 980px. The height is measured in TF24.7.

## TF24.2 — Use one scroll offset
**Status**: done

**Description**: Add `--nav-offset` and use it for `.calendar-entry`, `.calendar-tba__date`, article headings and `.detail-brief-sidebar`. Remove the breakpoint-specific `scroll-margin-top` values.

**Test**: a CSS check that only one `scroll-margin-top` value remains and it uses the variable. Placement is measured in TF24.7.

## TF24.3 — Stop pages scrolling sideways
**Status**: done

**Description**: Add the image and code block rules, `object-fit: contain` for article images, and the phone rule that stops them floating.

**Test**: CSS checks for each rule. The page widths are measured in TF24.7.

## TF24.4 — Make headings responsive
**Status**: done

**Description**: Remove the fixed `h1`, `h2` and `h3` sizes in `css/shared.css`, keeping their line height and margins. Cap the `clamp()` sizes at 3.5, 2.25 and 1.75rem.

**Test**: a CSS check that these headings have only one `font-size`, and that it uses `clamp()`.

## TF24.5 — Fix contrast
**Status**: done

**Description**: Change light mode `--primary` and `--primary-hover`. Make the pill buttons solid amber with dark text, in one shared rule, and raise their text size.

**Test**: a test that computes `--primary` contrast from `css/shared.css` and requires at least 4.5:1 on `--bg`, `--calendar-card-bg` and `--primary-light`, plus a check that pills are solid `--accent` with `--on-accent` text at 4.5:1 or better.

## TF24.6 — Make Home's meeting rows real links
**Status**: done

**Description**: Add the link in `upcoming-meetings-calendar.html`, stretch it over the row with CSS, and remove `data-href`, `.meeting-row` and the handler in `scripts/script.js`.

**Test**: Home has a real link to each announcement in its rows, `data-href` is gone from the page and the script, and a row with no announcement has no link.

## TF24.7 — Write the feature's tests and measure
**Status**: done

**Description**: Add the tests from TF24.1 to TF24.6 in `tests/test_layout_bugs.py`. Repeat the audit's browser measurements across all pages.

**Test**: `uv run pytest` passes in full. The browser shows no page scrolling sideways at 375px, and the linked heading and sidebar sit below the nav at 1200px.

## TF24.8 — Check it in a browser
**Status**: done

**Description**: Run the F24 demo, comparing with the TF24.0 screenshots, in both themes at 375px and 1200px.

**Test**: not feasible to automate, so the user signs off on how it looks.
