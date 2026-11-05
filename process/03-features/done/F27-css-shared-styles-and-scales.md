# F27 — Shared CSS styles, scales and file split
**Priority**: Medium
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* Make the CSS smaller and easier to work in. It's 1,588 lines today, with 831 declarations.
* Replace repeated patterns with shared classes, and one-off values with short scales.
* Split the CSS into files by job.
* **Pages may shift slightly**, by at most a pixel or two in size and spacing. Anything bigger is a bug.

**Size**:

* Planned as roughly 10–20% fewer declarations.
* **Result: 831 → 713 declarations, 14% fewer.** Lines went from 1,588 to 1,523, because the split adds file headers and some one-line rules became normal multi-line ones.
* The scales and shared classes alone gave 8%. Making the near-identical styles identical gave the rest.
* More of the remaining duplication is in the detail page templates, which is later template work.

**Making near-identical styles identical** (added 2026-11-05 at the user's request):

* **Boxes**: `.panel` gives cards, Learn cards, the page intro and the Pupper box one border, corner and shadow. Learn cards gain the small shadow.
* **Detail titles**: news, project and member pages share `.detail-title`.
* **Labels**: one size everywhere.
* **Section headings**: one size and bottom margin, and `.section-heading--spaced` for the gap above a later section.
* **Dividers**: `--rule` (1px, light) and `--rule-strong` (2px, text color) replace 3px, 2px and dashed lines.
* **Small grey text**: `.note` for excerpts, blurbs and notes.
* **"Label: value" details**: `.meta` for project details and member links.
* **Buttons**: the outline and slides buttons share size and type, and differ only in fill.
* **Greys**: `--text-light` and `--dek` fold into `--text-muted`. `--text-light` failed text contrast at 4.28:1.
* **Corners**: only `--radius`, `--radius-lg` and fully round.

**Found and fixed along the way**:

* F24's phone nav rules came before the rules they meant to override, so they never applied. In the new file they come after, and the phone nav is about 60px shorter.

**Font size scale**:

* Seven sizes replace 28 values: `--fs-2xs` 0.65rem, `--fs-xs` 0.72rem, `--fs-sm` 0.85rem, `--fs-md` 0.95rem, `--fs-base` 1rem, `--fs-lg` 1.2rem, `--fs-xl` 1.35rem.
* Each old value moves to the nearest size, and the biggest move is about 0.08rem.
* The heading `clamp()` values, the nav wordmark and the large placeholder initials stay as they are.

**Breakpoints**:

* Three widths replace ten: **620px** for phones, **760px** for small tablets and **980px** for tablets.
* The home page's news and rail columns stack at 980px instead of 860px, and the meeting grid drops to 3 columns at 980px instead of 1000px.
* CSS can't use variables in media queries, so a comment in the base file lists the three widths.

**Text color default**:

* `p`, `li` and `blockquote` stop setting their own color, so text inherits its container's color.
* Containers that are muted set that color once, instead of on each child.

**Shared classes**:

* `.label` styles the small uppercase red labels, and `.label--muted` the grey version. It replaces 8 near-copies, such as `.story-row__meta`, `.rail-item__cat` and `.detail-brief-header__kicker`.
* `.section-heading` styles the underlined uppercase headings. It replaces `.river-header`, `.rail-title`, `.calendar-section-title` and the About page's `h2`s.
* `.placeholder` styles the boxes shown when an image is missing. It replaces 4 near-copies.
* Templates get the new class names. Each element keeps its own class only for what's really unique to it, such as margins.

**File split**:

* `main.css` and `shared.css` become four files, loaded in this order:
  * `base.css`: reset, fonts, theme variables, scales, typography and links.
  * `layout.css`: nav, banner, footer, page shells and grids.
  * `components.css`: labels, headings, buttons, cards, rail items, story rows and placeholders.
  * `pages.css`: rules for a single page.
* `head.html` links all four, and the build copies every file in `css/`.
* Tests that read the CSS read all four files.

**Checking for visual changes**:

* Claude can't see pages in the CLI, so a script takes headless Chrome screenshots of every page.
* It covers 375px and 1200px, in both themes, before and after, and reports the pages whose pixels differ.
* The script lives in the session's scratchpad, not the repo.

**Non-goals**:

* No template tidying, such as the detail-page partial or root path variable.
* No changes to content files.
* No new colors or design changes.
* No squeezing rules onto single lines to shrink the line count.
* No changes for F26 (ROSbot section). If F26 lands first, its CSS moves into the new files with everything else.

## How to Demo
**Setup**: the before screenshots and build from TF27.0, then `make try`.

**Steps**:

1. Run the screenshot comparison on every page.
2. Look at the pages it flags in both themes, at phone and desktop widths.
3. Compare the line and declaration counts with the TF27.0 numbers.
4. Run `uv run pytest`.

**Expected output**:

* Flagged pages differ only by small size and spacing shifts, plus the two breakpoint moves.
* The CSS is smaller, and split into four files.
* All tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
