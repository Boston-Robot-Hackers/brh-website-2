# F24 — Fix layout and accessibility bugs
**Priority**: High
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Fix the bugs visitors can hit, all found by the 2026-11-05 HTML and CSS audit and measured in the browser.
* **This is not the CSS cleanup.** Dead code, shared styles and type scales stay out, so these fixes can ship on their own.

**Measured today**:

* The sticky nav is 237px tall at 375px wide.
* 10 of 61 pages scroll sideways at 375px wide, by up to 2,317px.
* The banner title stays 56px on phones.
* "On this page" links land the heading under the nav, at 16–41px with the nav ending at 76px.
* The sticky sidebar sits at 24px, also under the nav.
* Amber buttons have 2.12:1 contrast on cream. Red links have 3.92:1 on cream and 3.41:1 on meeting cards.
* Home's meeting rows can't be used by keyboard.

**Sticky nav**:

* **At 980px and below, the nav stops being sticky and scrolls away.** No hamburger menu, which would add JavaScript and a new control to maintain.
* At 620px and below, the wordmark and gaps get smaller, so the nav takes less room at the top of the page.

**Scroll offsets**:

* One `--nav-offset` variable replaces the 6, 10, 13 and 16rem values.
* It's the nav's height above 980px, and a small margin below it.
* Meeting cards, article headings and the sticky sidebar all use it.

**Sideways scrolling**:

* All images get `max-width: 100%`, and code blocks scroll inside themselves.
* In article bodies, `object-fit: contain` keeps images with an inline height from distorting.
* At 620px and below, images in article bodies stop floating and sit on their own line.
* **That rule needs `!important`**, because it has to override inline styles in the content files. Replacing those styles is separate work.

**Heading sizes**:

* Remove the fixed `h1`, `h2` and `h3` sizes that override the responsive ones.
* Cap the responsive sizes at today's values, so desktop headings stay the same size.

**Contrast**:

* **Light mode `--primary` changes from `#ff0033` to `#d00029`.** That's 5.59:1 on cream, 4.86:1 on meeting cards and 4.69:1 on the Pupper box. It's a visibly deeper red, and dark mode keeps its own.
* `--primary-hover` gets a darker matching shade.
* Amber buttons become solid amber with dark text, in both themes. The first version kept a faint tint with dark text, and the user reported it no longer looked like a button.
* Their text grows from 0.65rem to 0.75rem.

**Keyboard access**:

* Home's meeting rows get a real link on the date, and the whole row stays clickable through CSS.
* Rows with no announcement have no link and no pointer cursor.
* Remove `data-href`, `.meeting-row` and the JavaScript behind them.

**Non-goals**:

* No dead code removal, shared styles or font and breakpoint scales.
* No edits to content files. The agenda lists that are indented and so render as code blocks are a separate content fix.
* No fix for pages with two `h1`s.
* No other nav redesign.

## How to Demo
**Setup**: `make try`.

**Steps**:

1. At 375px wide, load every page and compare page width with screen width.
2. On a news page with an "On this page" list, at 1200px wide, click a link and scroll.
3. On Home, Tab to a meeting row and press Enter.
4. Check Home, Meetings, a news page and a member page in both themes, at 375px and 1200px.
5. Run `uv run pytest`.

**Expected output**:

* No page scrolls sideways at 375px, and the nav scrolls away on phones.
* The linked heading and the sidebar both sit fully below the nav.
* Enter opens the meeting's announcement.
* Desktop looks the same apart from the deeper red and the darker button text.
* All tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
