# F23 — Remove the hero concept
**Priority**: Low
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:

* A "hero" is only a short page intro, so **remove the concept** rather than slim it down. The user chose this on 2026-11-05, replacing the earlier plan to keep `content/heroes/` with body text only.
* `content/heroes/`, `components/hero.html` and `build_hero_content` all go.
* **The intros that stay keep their exact wording.** Pages keep the same text and look, except for the three cut intros.

**Start condition**:

* F22 is committed (`228696a`), so nothing blocks this work.

**Home page**:

* **The mission paragraph moves to `content/home.md`.** It keeps its Markdown and its signup link, and a missing file still fails the build.
* `build_index` loads it with `process_single_content_file`.
* **The "Next…" line stays, in the same place and with the same look.** The user confirmed this on 2026-11-05.
* `build_index` passes the mission text and the rendered line to `home-lead.html`, which also takes over the `<hr/>`.
* Remove `generate_index_hero` and the `<hr/>` convention.
* `format_future_meetings_section` stays. `upcoming-meetings-hero.html` becomes `upcoming-meetings-next.html`.

**Other pages**:

* **Projects keeps its intro in its own page template.** Changing it now means editing HTML.
* **Meetings lost its intro** in a later header change the user asked for (chore 46).
* **About, Learn and Members lose their intros.** The text is generic and adds nothing to the page below it. The user left this choice to Claude on 2026-11-05.
* `layouts/page.html` gets an empty `intro` block in place of the `hero.html` include, and Projects fills it.
* All other pages leave it empty, so `hero={}` goes away.

**Banners**:

* Main pages call `resolve_banner({})` and keep the site default. No hero file sets a banner, so this reverses that part of F09.
* Banner overrides on detail pages stay, including the one in `content/projects/pupper.md`.

**Deleted without moving**:

* `content/heroes/community.md`, which nothing loads.
* `content/heroes/whatsnew.md`, which has no body.
* `content/heroes/about.md`, `learn.md` and `members.md`, the cut intros.
* `title` and `subtitle` in hero files, which no template shows.

**CSS**:

* `.hero` and `.hero-section` become `.page-intro` and `.page-intro__inner`, with the same styling.
* Remove `.hero-title` and any rules that no longer match anything.

**Non-goals**:

* No wording changes to the text that stays. The "Meets monthly" versus "twice a month" mismatch is a separate content fix.
* No change to `banner.html` or to the banner on any page.

## How to Demo
**Setup**: a build of the current site saved for comparison, then `make try`.

**Steps**:

1. Compare the top-level HTML in `output/` with the saved build.
2. Open `http://localhost:8000/index.html` and `http://localhost:8000/meetings.html`.
3. Run `uv run pytest`.

**Expected output**:

* The page content is the same, apart from whitespace, the renamed CSS classes, the intros cut from About, Learn and Members, and the chore 46 changes to Meetings.
* Home shows the mission paragraph and the "Next…" line, and Meetings shows its banner and its tightened header.
* `content/heroes/` no longer exists, and all tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
