# TF01 Description for Feature F01

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF01.N`, starting at `.0`.

## TF01.0 — Audit current color usage
**Status**: done

**Description**: Catalog every hardcoded color (hex literals, Bootstrap color
utility classes like `bg-light`/`bg-dark`/`text-dark`/`border-dark`, inline
styles) across `css/main.css`, `css/shared.css`, and `templates/`, to build
the concrete scope list the rest of this feature works from.

**Test**: None — this is a documentation/inventory step, not a behavior
change. The resulting list (files + line numbers) is recorded as this task's
completion evidence instead.

**Findings**:

`css/shared.css` has one `:root` block with 8 real color variables
(`--primary`, `--primary-hover`, `--primary-light`, `--secondary`,
`--accent`, `--success`, `--bg`, `--bg-card`, `--border`, `--border-hover`,
`--text`, `--text-muted`, `--text-light`) and no dark counterparts.

`css/main.css` has 14 hardcoded hex colors, in two groups:

- 3 are bespoke dark UI chrome — `.nav-bar-thin`'s gradient (line 8),
  `.banner` (line 52), nav-link hover (line 114). Already dark regardless of
  page theme. **No fix needed.**
- 10 are the `.meeting-month-card`/`.compact-meeting-card` component (lines
  274, 280, 287, 293, 356, 358, 360, 368, 371, 384) — light-gray cards
  sitting directly on the page body in `meetings.html`/`whatsnew.html`.
  **Need dark counterparts.**

Templates: Bootstrap 5.3's *semantic* utilities (`bg-secondary`, `bg-primary`,
`text-white` on colored fills) already adapt to `data-bs-theme` — no changes
needed anywhere in `cards/`/`details/`. Confirmed separately that 17
templates use Bootstrap's `.card` component, whose background/border *are*
theme-aware — this makes syncing `data-bs-theme` (TF01.2) essential, not
optional.

The *fixed grayscale* utilities (`bg-light`, `bg-dark`, `text-light`,
`text-dark`, `border-dark`) do **not** respond to `data-bs-theme` at all.
`footer.html` and `navigation.html` use them but are already dark, so
they're fine as-is. Three spots are real bugs — see TF01.4.

## TF01.1 — Define a dark palette as CSS custom properties
**Status**: done

**Description**: In `css/shared.css`, add a `prefers-color-scheme: dark`
value for every variable currently defined in the light `:root` block
(`--bg`, `--bg-card`, `--border`, `--border-hover`, `--text`, `--text-muted`,
`--text-light`, and shadow variables as needed), keeping text/background
contrast readable.

**Test**: covered by the regression test written in TF01.6 (parity check
that every light-mode variable has a dark-mode counterpart).

**Result**: Added a dark-mode block to `css/shared.css` redefining the 7
neutral variables plus all 4 shadow variables (11 total), using a symmetric
slate-scale flip (`--bg: #0f172a`, `--bg-card: #1e293b`, `--border:
#334155`, `--border-hover: #475569`, `--text: #f1f5f9`, `--text-muted:
#94a3b8`, `--text-light: #64748b`), with shadow opacity bumped (0.05/0.1 →
0.3/0.4) since low-opacity black shadows barely register on a dark
background. `--primary`/`--primary-hover`/`--primary-light`/`--secondary`/
`--accent`/`--success` were deliberately left unchanged — confirmed via
grep that they're only used on self-contained saturated fills (badges,
gradients), never as page/card backgrounds, so they read fine in both
modes. (Originally implemented as `@media (prefers-color-scheme: dark)`;
switched to the `:root[data-bs-theme="dark"]` attribute selector in TF01.7
so the manual toggle can override the OS setting — see that entry.)

## TF01.2 — Sync Bootstrap's own theming with system preference
**Status**: done

**Description**: Set `data-bs-theme="dark"`/`"light"` on the `<html>`
element based on `prefers-color-scheme`, so Bootstrap's own component colors
(`bg-dark`, `text-light`, badges, borders, etc.) switch along with the
custom variables. Use a small inline script early in `<head>` so the theme
is set before first paint (avoids a flash of the wrong theme).

**Test**: covered by the regression test written in TF01.6 (asserts the
theme-setting script is present in generated page output).

**Result**: Added an inline `<script>` to `templates/layouts/base.html`,
immediately after `<meta charset>` (before any CSS/analytics loads), that
sets `data-bs-theme` via `window.matchMedia('(prefers-color-scheme: dark)')`.
All pages extend `layouts/base.html`, so this covers every page type from
one place. (Updated in TF01.7 to check `localStorage` first, for the manual
toggle.)

**Follow-up bug found via actual rendering** (not caught by TF01.0's static
audit or the automated tests, only by screenshotting the built pages): the
user reported the dark result looked "ugly." Inspecting computed styles
showed `body`'s background was rendering as `#212529` (Bootstrap's own
default dark body color) instead of our `--bg` (`#0f172a`) — same for
`.card`. Root cause: `templates/components/head.html` loaded Bootstrap's
CSS *after* `css/shared.css`/`css/main.css`, so Bootstrap's own `body`/
`.card` rules (equal specificity, later in the cascade) silently won over
ours — in both modes, but only obviously wrong in dark mode where the two
competing dark grays visibly clashed. Fixed by reordering `head.html` so
Bootstrap loads first and our custom CSS loads last. No test caught this
because the CSS variables were defined correctly; the bug was purely about
which stylesheet won the cascade, which needs a rendered page (or computed-
style inspection) to observe, not a text-content check.

## TF01.3 — Replace remaining hardcoded colors in `main.css` with variables
**Status**: done

**Description**: Convert the 10 `.meeting-month-card`/`.compact-meeting-card`
hex colors identified in TF01.0's audit to reference `css/shared.css`
custom properties (adding new variables where no existing one fits), so
they pick up dark values automatically instead of staying fixed. Leave the
3 bespoke-dark-chrome colors (nav-bar gradient, banner, nav-link hover)
hardcoded — they're already dark regardless of page theme and don't need to
change.

**Test**: covered by the regression test written in TF01.6 (asserts no raw
hex color literals remain in `css/main.css` outside variable definitions and
the 3 intentional bespoke-chrome exceptions).

**Result**: All 10 converted — `#212529` → `var(--text)`, `#6c757d` →
`var(--text-muted)`, `#0d6efd` → `var(--primary)`, `#f8f9fa` → `var(--bg)`
(the light gray was already near-identical to `--bg`'s light-mode value, so
this preserves the existing "flat, page-colored card" look rather than
introducing a new raised-white-card look), `#495057` → `var(--text)`,
`#ced4da` → `var(--border-hover)`, `#dee2e6` → `var(--border)`. Verified
only the 3 bespoke-chrome hex values remain in `css/main.css`.

## TF01.4 — Fix template-level color-class assumptions
**Status**: done

**Description**: Per TF01.0's audit, 3 concrete fixes, all fixed grayscale
utilities that don't respond to `data-bs-theme`:

- `components/section.html`'s `text-dark` heading — near-black text sitting
  on the page body; goes invisible once the page background goes dark.
- `details/member-detail.html`'s `bg-light text-dark` hashtag badge — a
  near-white chip that will glow against a dark page.
- `cards/news-card.html`'s `border border-dark` — a near-black border that
  will vanish against a dark card background.

`components/footer.html` and `components/navigation.html` are confirmed
fine as-is (already dark) — do not change them.

**Test**: Manual — not practically assertable by pytest since it's a visual
contrast judgment. Record per `.claude/style_guide.md`'s manual-test-notes
convention: command/setup used, pages checked, expected vs. actual result.

**Result**: `section.html` — removed `text-dark` entirely; the `<h2>` has no
other color override, so it now inherits `var(--text)` from `body`.
`member-detail.html` — replaced `bg-light text-dark` with
`bg-body-secondary text-body`, both theme-aware Bootstrap utilities that
flip together, keeping the badge readable in both modes. `news-card.html` —
replaced both `border-dark` occurrences with plain `border` (Bootstrap's
default `.border` uses the theme-aware `--bs-border-color`).

## TF01.5 — Check logo/image assets for dark-mode legibility
**Status**: done

**Description**: Check whether `images/robot-logo.png` and other UI-chrome
images remain legible against a dark background. Only add a dark-mode
variant if the check finds a real problem (e.g. a white-background logo
needing a swap) — don't create assets speculatively.

**Test**: Manual — same reasoning as TF01.4. Record what was checked and the
result.

**Result**: There is no actual logo `<img>` anywhere in the templates —
`images/robot-logo.png` is only referenced by a `<link rel="preload">` in
`components/head.html`, and that file doesn't exist anywhere in the repo
(confirmed during the earlier `images/` cleanup session — pre-existing,
unrelated to dark mode, out of scope for F01). The `.nav-logo` CSS class in
`main.css` is likewise unused by any template. No real image asset needs a
dark-mode variant; nothing was added speculatively. The other bespoke-chrome
image (`.banner`'s `images/meetings/meeting1-1.jpg`) sits on an already-dark
`#1a1a1a` background regardless of page theme, so it's unaffected.

## TF01.6 — Write regression tests and do final cross-page verification
**Status**: done

**Description**: Dedicated test-writing task. Add automated tests to the
pytest suite: (a) every CSS custom property defined in the light `:root`
block of `css/shared.css` has a corresponding definition in the
`prefers-color-scheme: dark` block, (b) `css/main.css` contains no hardcoded
hex color literals outside variable definitions, (c) built page `<head>`
output includes the `data-bs-theme` sync script from TF01.2. Then do a final
manual pass: build the site and check every page type (homepage,
`whatsnew.html`, `meetings.html`, `projects.html`, `members.html`,
`about.html`, `learn.html`, plus one detail page per content type) under
both `prefers-color-scheme` values.

**Test**: `uv run pytest` includes and passes the three new automated
checks; manual pass results recorded per `.claude/style_guide.md`'s
convention.

**Result**: Added `tests/test_css_theme.py`, now 4 tests (a 4th was added in
TF01.7's follow-up, see below) — note (a) checks an explicit allowlist of
the 11 variables that need dark counterparts (*not* literally every light
variable, since brand/accent colors are intentionally unchanged; the
original task description predates that finding). `uv run pytest` — 72
passed at the time.

Manual pass: initially done as a static-only check, since no browser tool
was available at first. **Superseded** — TF01.7 got Playwright working in
this environment (installed to a scratch npm project, isolated from the
repo, since it has no `package.json` of its own) and did real rendered
screenshots, which is how the TF01.7 cascade-order bug was actually found.
Static verification alone would not have caught it — the CSS variables
were all defined correctly, so every text-content check passed; only a
rendered page (or computed-style inspection) shows which stylesheet wins
the cascade. Lesson: for a visual-correctness feature like this one, a
rendered check is not optional polish, it's the only way to catch this
class of bug.

## TF01.7 — Manual toggle + the cascade-order bug it surfaced
**Status**: done

**Description**: Added after the rest of TF01 was already done — the user
asked to actually see the result rendered, which led to finding and fixing
a real bug, then asked for a manual light/dark toggle button (reversing
F01's original system-preference-only non-goal).

**Test**: `test_bootstrap_css_loads_before_custom_css` (new, in
`tests/test_css_theme.py`) locks in the cascade-order fix. The toggle
itself was verified interactively (see Result) rather than via a new
pytest test, since it's a click-and-observe DOM interaction; pytest has no
browser context here to drive.

**Result**:

*Rendering setup*: no project skill existed for running this static site
in a browser, so one was improvised: installed Playwright into an isolated
scratch npm project (this repo has no `package.json`), served `output/`
via `python3 -m http.server`, and drove headless Chromium with
`colorScheme: 'dark'`/`'light'` context options to screenshot real pages.

*Bug found*: see TF01.2's follow-up note — `head.html` loaded Bootstrap's
CSS after ours, so Bootstrap's `body`/`.card` rules won the cascade and
silently used Bootstrap's own dark palette (`#212529`) instead of ours
(`#0f172a`). Fixed by reordering `head.html`. Re-screenshotted after the
fix and confirmed cards now have correct, visually distinct backgrounds
matching the intended palette.

*Toggle implementation*: switched `css/shared.css`'s dark-mode block from
`@media (prefers-color-scheme: dark)` to the `:root[data-bs-theme="dark"]`
attribute selector, so it's driven by the same attribute Bootstrap uses
rather than the OS media query directly — this is what makes a manual
override possible. `templates/layouts/base.html`'s inline script now
checks `localStorage.getItem('theme')` first, falling back to
`prefers-color-scheme` only if nothing is stored (still runs before first
paint). Added a small round icon button (`#theme-toggle`,
sun/moon Bootstrap Icon) to `components/navigation.html`, positioned
top-right of the nav bar via `css/main.css`'s `.theme-toggle-btn`
(absolutely positioned against `.nav-bar-thin`'s existing `position:
sticky`, which already establishes a containing block). Click handling and
icon sync added to `scripts/script.js`'s existing `DOMContentLoaded`
listener: toggling flips `data-bs-theme` and writes `localStorage`.

*Interactive verification*: scripted a Playwright click-through — loaded
the homepage with OS emulated as light, confirmed `data-bs-theme` starts
`"light"`, clicked the button, confirmed it flips to `"dark"` and
`localStorage` gets `theme: "dark"`, reloaded the page, confirmed it stays
`"dark"` even though the OS emulation is still light (proving the manual
override beats the system default). Screenshotted before/after — icon
correctly swaps moon → sun and the whole page recolors. Checked
`console --errors`-equivalent (`page.on('console'/'pageerror')`); the only
errors are the pre-existing missing `images/robot-logo.png` and the
external analytics script being unreachable in this sandboxed test run —
both unrelated to this change.

`uv run pytest` — 73 passed (added the cascade-order regression test).
