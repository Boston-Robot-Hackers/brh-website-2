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

**Result**: Added a `@media (prefers-color-scheme: dark)` block to
`css/shared.css` redefining the 7 neutral variables plus all 4 shadow
variables (11 total), using a symmetric slate-scale flip (`--bg: #0f172a`,
`--bg-card: #1e293b`, `--border: #334155`, `--border-hover: #475569`,
`--text: #f1f5f9`, `--text-muted: #94a3b8`, `--text-light: #64748b`), with
shadow opacity bumped (0.05/0.1 → 0.3/0.4) since low-opacity black shadows
barely register on a dark background. `--primary`/`--primary-hover`/
`--primary-light`/`--secondary`/`--accent`/`--success` were deliberately
left unchanged — confirmed via grep that they're only used on self-contained
saturated fills (badges, gradients), never as page/card backgrounds, so they
read fine in both modes.

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
one place.

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

**Result**: Added `tests/test_css_theme.py` with 3 tests — note (a) checks
an explicit allowlist of the 11 variables that need dark counterparts
(*not* literally every light variable, since brand/accent colors are
intentionally unchanged; the original task description predates that
finding). `uv run pytest` — 72 passed.

Manual pass: **no browser tool is available in this environment**, so
rendering was not visually confirmed — flagging that limitation rather than
claiming a visual check that didn't happen. Instead did a thorough static
verification: confirmed `data-bs-theme` script present in built output for
all 7 page types plus one detail page per content type (news, meetings,
projects, members); confirmed the dark `:root` block is present in
`output/css/shared.css`; confirmed no leftover `text-dark`/`bg-light`/
`border-dark` in built output for the pages that use the fixed templates.
Recommend the user do a quick visual spot-check (devtools
`prefers-color-scheme: dark` emulation) before considering this fully
verified.
