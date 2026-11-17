# F29 — Show ROSbot session front matter on session pages
**Priority**: Medium
**Date Created:** 2026-11-17
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**: Each Build-A-ROSBot session page shows the details from its front matter in the page header, not just the title.

## Scope

* **Shown**: `summary`, `medium` (e.g. Zoom, In person) and `schedule` (e.g. TBD), each only when set. `date` is already shown and stays as it is.

* **Where**: the header of `templates/details/rosbot-session-detail.html`, under the title. **Template-only change**: `rosbot_builder.py` already passes the whole front matter through as `page.metadata`.

* **Not in scope**: showing medium or schedule on the overview list, and validating their values. Both stay free text and optional.

* The session template's comment that medium and schedule "are not shown on the site yet" is removed.

## How to Demo
**Setup**: none beyond `uv sync`.

**Steps**:
1. `uv run python build/build.py`
2. Open `output/rosbot-sessions/03-assembling-makers-pet.html`.

**Expected output**: under the title, the page shows the summary, then "In person" and "TBD", each labelled.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
