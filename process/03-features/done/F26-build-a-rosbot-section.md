# F26 — Build-A-ROSBot section
**Priority**: Medium
**Date Created:** 2026-11-05
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**: A new section for the **Build-A-ROSBot** program. It has an overview page, one page per session, and one page per program resource. It is reached from a featured-program link in the top nav, like the Pupper link. All content is plain Markdown with frontmatter, **one file per page**, so it's easy to organize and edit.

## Content layout

- `content/rosbot/overview.md` → `output/rosbot.html`. The program description, written by hand.
- `content/rosbot/sessions/<slug>.md` → `output/rosbot-sessions/<slug>.html`. One file per session.
- `content/rosbot/resources/<slug>.md` → `output/rosbot-resources/<slug>.html`. One file per resource, such as a parts list, a setup guide or reading.
- The output folders are **one level deep**, so the existing `../` path prefix for detail pages works unchanged.

## Frontmatter

- **Sessions**: `title` and `session` (an integer that sets the order) are required. `summary` and `date` are optional.
- **Resources**: `title` is required. `summary` is optional, and so is `order`, an integer that sets the order. Without `order`, resources are sorted by title.
- A missing required field raises `ValueError` naming the file. Two sessions with the same `session` number also raise an error.

## Pages

- **Overview**: the hand-written overview text, then two lists the build generates: *Sessions* (number, title, summary) and *Resources* (title, summary). Adding a file adds it to the lists with no other edit.
- **Session page**: "Session N: title", the date if set, the body, previous and next session links, and a link back to the overview.
- **Resource page**: title, body, and a link back to the overview.
- **Nav**: a "Build-A-ROSBot" featured link after Pupper, with the same badge styling and no photo yet. It shows as active on every page in the section.

## Placement

- The build code goes in a new module, `build/rosbot_builder.py`. `build/build.py` is already over the ~300-line guideline, so it gets only the call.

## Out of scope

- Writing the real session and resource content. That's content work for the user.
- Session dates in `calendar.yaml`, iCal entries, or a Home-page spotlight.
- Nested folders under `sessions/` or `resources/`.

## How to Demo
**Setup**: `uv run python build/build.py`, then open `output/index.html`.

**Steps**:
1. Click "Build-A-ROSBot" in the top nav.
2. From the overview, open a session, then step through it with Next and Previous.
3. Go back to the overview and open a resource.
4. Add a new file in `content/rosbot/sessions/`, rebuild, and reload the overview.

**Expected output**: all pages render in the site layout with the Build-A-ROSBot link active, and the new session appears in the overview list, in order, with no other edits.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
