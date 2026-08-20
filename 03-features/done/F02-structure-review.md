# F02 — codebase structure & consistency review
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Review the overall structure of the repository — directory
layout, naming conventions, dead/legacy code, and drift between what
`CLAUDE.md`/`README.md` document and what actually exists — to find what
makes the repo harder than necessary for a human or an AI coding agent to
navigate and modify safely. Produce a written, prioritized list of concrete
proposed changes with a recommended disposition for each (chore / new
feature / defer).

A first pass already surfaced concrete candidates worth digging into: a
`legacy/` directory (an earlier Tailwind-based prototype, including a
git-tracked `node_modules/`) and an `archive/build.py` sitting unreferenced
at the repo root; a `rules.md` that is a git-tracked symlink to an absolute
path outside the repo (`/Users/pitosalas/mydev/dotfiles/rules.md`, dangling
on any other checkout); three separate `pyproject.toml` files; content
filename conventions that drift between hyphens and underscores
(`1-first_meeting.md` vs. later `NN-slug-with-hyphens.md`); and
`05-issues/{open,closed,deferred}/` subfolders that `.claude/process.md`
expects but that don't exist yet. This feature does the full audit and
writes up the findings — it does not apply any of the proposed changes.

**Non-goals**: implementing any of the proposed changes (each becomes its
own chore/feature once reviewed and approved); re-auditing `build/*.py`
against `.claude/style_guide.md` (already done — see the 8 pending items in
`04-tasks/chores.md`).

## How to Demo
**Setup**: None beyond having the repo checked out.

**Steps**:
1. Open `02-doc/structure-review.md`.
2. Confirm it covers: top-level directory inventory vs. documented
   structure, dead/legacy code, the `rules.md` symlink, naming/content-model
   consistency, and reconciliation with already-tracked debt
   (`04-tasks/chores.md`, the missing `05-issues/` subfolders).
3. Confirm each finding has a concrete proposed change and a recommended
   disposition (chore / feature / defer).
4. Run `uv run pytest` and confirm the new guardrail test from this
   feature's test-writing task passes.

**Expected output**: A single reviewable document the user can work through
finding-by-finding, plus one new automated test that locks in the most
durable finding so it can't silently regress.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
