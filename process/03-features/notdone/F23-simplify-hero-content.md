# F23 — Simplify hero content
**Priority**: Low
**Date Created:** 2026-11-05
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no

**Description**:

* Keep `content/heroes/` as the Markdown source for each page's intro text, and remove the parts that never reach a page.
* A hero file becomes a body of text and nothing else.
* **Rendered pages stay the same.** This is a cleanup, not a redesign.

**Start condition**:

* **Start only after F22 is committed.** Its uncommitted changes overlap this work in `build/build.py`, `css/main.css`, `css/shared.css` and `README.md`.

**Unused files**:

* Delete `content/heroes/community.md`. Nothing loads it.
* Delete `content/heroes/whatsnew.md`, which has no body. What's New passes `hero={}`, as content pages already do.

**Unused fields**:

* Remove `title` and `subtitle` from hero files. No template shows them.
* `build_hero_content` returns only the body.
* Remove `banner_*` from hero handling, and main pages call `resolve_banner({})`. No hero file sets these fields, so this reverses that part of F09.
* Banner overrides on detail pages stay, including the one in `content/projects/pupper.md`.

**Home page "Next…" line**:

* **The line stays, in the same place and with the same look.** The user confirmed this on 2026-11-05.
* `home-lead.html` renders it directly from a value passed by `build_index`.
* Remove `generate_index_hero` and the `<hr/>` convention in `content/heroes/index.md`.
* `format_future_meetings_section` and `upcoming-meetings-hero.html` stay.

**Must not change**:

* The Meetings page keeps its banner and intro text.
* Home keeps its mission paragraph and join link.
* Files with hero text remain required, so a missing one still fails the build.

**Non-goals**:

* No wording changes to hero text. The "memebrs" typo and the "Meets monthly" versus "twice a month" mismatch are separate content fixes.
* No change to `banner.html` or to the banner on any page.
* No move of hero text into templates.

## How to Demo
**Setup**: a build of the current site saved for comparison, then `make try`.

**Steps**:

1. Compare the top-level HTML in `output/` with the saved build.
2. Open `http://localhost:8000/index.html` and `http://localhost:8000/meetings.html`.
3. Run `uv run pytest`.

**Expected output**:

* The page content is the same, apart from whitespace.
* Home shows the mission paragraph and the "Next…" line, and Meetings shows its banner and intro.
* All tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
