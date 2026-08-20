# F01 — dark/light mode correctness
**Priority**: Medium

**Done:** yes

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes


**Description**: The site currently defines only one color palette (light) as
CSS custom properties in `css/shared.css`, loads Bootstrap 5.3.2 without
configuring its dark-mode support (`data-bs-theme`), and has ~14 hardcoded hex
colors in `css/main.css` that bypass the variable system entirely. As a
result the site always renders in light colors regardless of the visitor's
OS/browser `prefers-color-scheme` setting, which can produce poor contrast or
a jarring light flash for visitors whose systems are set to dark mode.

This feature makes every page (homepage, listing pages, and detail pages)
render correctly in both light and dark mode, automatically following the
visitor's system preference via `prefers-color-scheme`, with Bootstrap's own
component theming kept in sync and no unreadable/low-contrast combinations.

**Non-goals**: no manual light/dark toggle switch UI (system-preference-driven
only); no redesign of the existing light color palette itself; no Bootstrap
version upgrade — 5.3.2 (currently loaded) already has the full color-mode
system this feature needs, so a version bump isn't required and would add
unrelated risk.

## How to Demo
**Setup**: Run `uv run python build/build.py`, then open pages from `output/`
in a browser (or a local static server) with devtools able to emulate the
`prefers-color-scheme` CSS media feature.

**Steps**:
1. With `prefers-color-scheme: light` emulated, load `output/index.html`,
   `output/meetings.html`, and one detail page (e.g. a news detail page).
   Confirm colors match today's existing light appearance.
2. Switch devtools emulation to `prefers-color-scheme: dark` and reload the
   same pages.
3. Check page background, card backgrounds, body/heading text, links, nav
   bar, footer, and badges/borders on each page.

**Expected output**: In dark mode, every element switches to a dark-appropriate
color with readable contrast — no light-mode card floating on a dark
background, no white-on-white or black-on-black text, and no leftover
hardcoded light colors. Light mode is visually unchanged from today.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
