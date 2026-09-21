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
render correctly in both light and dark mode, defaulting to the visitor's
system preference via `prefers-color-scheme`, with a manual toggle button
in the nav bar to override it (persisted in `localStorage`), Bootstrap's own
component theming kept in sync, and no unreadable/low-contrast combinations.

**Non-goals**: no redesign of the existing light color palette itself; no
Bootstrap version upgrade — 5.3.2 (currently loaded) already has the full
color-mode system this feature needs, so a version bump isn't required and
would add unrelated risk.

*(Revision: a manual toggle was originally a non-goal, system-preference-only.
The user asked for one after seeing the initial dark-mode result, so it was
added — see TF01.7.)*

## How to Demo
**Setup**: Run `uv run python build/build.py`, then serve `output/` locally
(e.g. `python3 -m http.server 8000 --directory output`) and open it in a
browser.

**Steps**:
1. Load `index.html`, `meetings.html`, and one detail page (e.g. a member or
   news detail page). Confirm colors match the existing light appearance.
2. Click the moon/sun icon button at the top-right of the nav bar. Confirm
   the whole page switches to dark colors immediately, the icon flips to a
   sun, and reloading the page keeps the dark choice (persisted via
   `localStorage`).
3. Check page background, card backgrounds, body/heading text, links, nav
   bar, footer, and badges/borders on each page. (Alternatively, skip the
   button and use devtools' `prefers-color-scheme` emulation to check the
   system-preference default before any manual toggle.)

**Expected output**: In dark mode, every element switches to a dark-appropriate
color with readable contrast — no light-mode card floating on a dark
background, no white-on-white or black-on-black text, and no leftover
hardcoded light colors. Light mode is visually unchanged from today.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
