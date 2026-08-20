# TF01 Description for Feature F01

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF01.N`, starting at `.0`.

## TF01.0 — Audit current color usage
**Status**: not done
**Description**: Catalog every hardcoded color (hex literals, Bootstrap color
utility classes like `bg-light`/`bg-dark`/`text-dark`/`border-dark`, inline
styles) across `css/main.css`, `css/shared.css`, and `templates/`, to build
the concrete scope list the rest of this feature works from.
**Test**: None — this is a documentation/inventory step, not a behavior
change. The resulting list (files + line numbers) is recorded as this task's
completion evidence instead.

## TF01.1 — Define a dark palette as CSS custom properties
**Status**: not done
**Description**: In `css/shared.css`, add a `prefers-color-scheme: dark`
value for every variable currently defined in the light `:root` block
(`--bg`, `--bg-card`, `--border`, `--border-hover`, `--text`, `--text-muted`,
`--text-light`, and shadow variables as needed), keeping text/background
contrast readable.
**Test**: covered by the regression test written in TF01.6 (parity check that
every light-mode variable has a dark-mode counterpart).

## TF01.2 — Sync Bootstrap's own theming with system preference
**Status**: not done
**Description**: Set `data-bs-theme="dark"`/`"light"` on the `<html>` element
based on `prefers-color-scheme`, so Bootstrap's own component colors
(`bg-dark`, `text-light`, badges, borders, etc.) switch along with the custom
variables. Use a small inline script early in `<head>` so the theme is set
before first paint (avoids a flash of the wrong theme).
**Test**: covered by the regression test written in TF01.6 (asserts the
theme-setting script is present in generated page output).

## TF01.3 — Replace remaining hardcoded colors in `main.css` with variables
**Status**: not done
**Description**: Convert the hex colors identified in TF01.0's audit within
`css/main.css` to reference `css/shared.css` custom properties (adding new
variables where no existing one fits), so they pick up dark values
automatically instead of staying fixed.
**Test**: covered by the regression test written in TF01.6 (asserts no raw
hex color literals remain in `css/main.css` outside variable definitions).

## TF01.4 — Fix template-level color-class assumptions
**Status**: not done
**Description**: Review templates flagged in TF01.0 (e.g.
`components/footer.html`'s `bg-dark text-light`, `components/section.html`'s
`text-dark`, `details/member-detail.html`'s `bg-light text-dark` badge,
`cards/news-card.html`'s `border-dark`/`bg-secondary`) for combinations that
would look wrong or low-contrast once Bootstrap is in dark mode, and adjust
classes/inline styles as needed.
**Test**: Manual — not practically assertable by pytest since it's a visual
contrast judgment. Record per `.claude/style_guide.md`'s manual-test-notes
convention: command/setup used, pages checked, expected vs. actual result.

## TF01.5 — Check logo/image assets for dark-mode legibility
**Status**: not done
**Description**: Check whether `images/robot-logo.png` and other UI-chrome
images remain legible against a dark background. Only add a dark-mode
variant if the check finds a real problem (e.g. a white-background logo
needing a swap) — don't create assets speculatively.
**Test**: Manual — same reasoning as TF01.4. Record what was checked and the
result.

## TF01.6 — Write regression tests and do final cross-page verification
**Status**: not done
**Description**: Dedicated test-writing task. Add automated tests to the
pytest suite: (a) every CSS custom property defined in the light `:root`
block of `css/shared.css` has a corresponding definition in the
`prefers-color-scheme: dark` block, (b) `css/main.css` contains no hardcoded
hex color literals outside variable definitions, (c) built page `<head>`
output includes the `data-bs-theme` sync script from TF01.2. Then do a final
manual pass: build the site and check every page type (homepage,
`whatsnew.html`, `meetings.html`, `projects.html`, `members.html`,
`about.html`, `learn.html`, plus one detail page per content type) under both
`prefers-color-scheme` values.
**Test**: `uv run pytest` includes and passes the three new automated checks;
manual pass results recorded per `.claude/style_guide.md`'s convention.
