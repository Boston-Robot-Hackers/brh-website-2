# F04 — Modern-engineering visual redesign: 3 concept options
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* `02-doc/spec.md` is an unfilled template (no Description/Goals/Non-Goals
  content) — this feature doesn't contradict it, but there's nothing in it
  to confirm coverage against either. Noted per the spec-check step; not a
  blocker, consistent with how F01–F03 shipped under the same empty spec.
* All work happens on a new git branch (`f04-site-redesign`), created as
  this feature's first task step, so exploration stays isolated from
  `main` until a direction is picked.
* Goal: produce **three distinct visual-design directions** for the site,
  all aiming at a "modern engineering" look (confirmed by user: use
  graphics for visual interest, not just typography/color).
* Same content, same 5 existing nav areas confirmed in
  `templates/components/navigation.html` — Home, Learn, Members, Projects,
  About — plus one new 6th nav entry, **Pupper**, styled distinctly from
  the other five (different font and/or its own icon/graphic), per user
  request. Pupper has no real content model yet — mockups use placeholder
  content for it only; the other 5 areas reuse real copy from `content/`.
* Deliverable is exploratory: standalone HTML/CSS home-page mockups (one
  per direction) plus browser screenshots for side-by-side comparison —
  not wired into `build/build.py`, `templates/`, or `output/`. Nothing in
  the real build pipeline changes.
* Reopened after initial close: user asked for a 4th option that mimics
  the visual identity of a specific external article page
  (futurism.com's "European Central Bank Warns That AI Crash Is Looming"),
  not another "modern engineering" direction — an editorial/tech-magazine
  homage rather than the blueprint/terminal/industrial family of A–C.

**Non-goals**:
* Picking/adopting a final direction — that's a follow-up feature once the
  user reviews the three options.
* Wiring any chosen direction into the real Jinja2 templates/build/CSS.
* Building real content/pages for Pupper — nav-entry treatment only.
* Merging `f04-site-redesign` into `main`.

## How to Demo
**Setup**: `git checkout f04-site-redesign`. No build step required — the
mockups are standalone HTML files.

**Steps**:
1. Open each of the three mockup HTML files directly in a browser.
2. Compare the three "modern engineering" treatments side by side (or via
   the provided screenshot comparison).
3. Confirm each mockup shows the same site content, the 5 existing nav
   areas, and the new Pupper nav entry with its distinct treatment.

**Expected output**: Three clearly differentiated, modern-engineering
visual directions to choose from, with zero changes to the live
`build/`/`templates/`/`output/` pipeline.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
