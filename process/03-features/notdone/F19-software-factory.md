# F19 — Software factory: unattended lanes for content and refactors
**Priority**: Medium
**Date Created:** 2026-10-27
**Done:** no
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Let Claude Code run two narrow kinds of work without a live
human at each step, landing the result as a pull request for review.

## Scope

* **Lane 1 — content.** A "Speaker confirmed" GitHub issue carries the date,
  speaker, topic and blurb. The agent fills in the matching meeting file,
  rebuilds, confirms the talk appears in `upcoming-talks.txt` and
  `meetings.ics`, and opens a PR.

* **Lane 2 — behavior-preserving refactors.** For parked features whose
  intent is "same output, cleaner code" (F12, F14, F16). The oracle is the
  built site: `output/` must be identical before and after, ignoring the
  iCal `DTSTAMP` lines, plus the full test suite.

* **Everything else stays interactive.** Features that change behavior or
  output (F13, F15, new pages) keep the existing plan-then-go gate.

## Key decisions

* **The PR replaces the "wait for go" gate — in the factory lanes only.**
  The plan goes in the PR description; merging is the approval. Interactive
  work keeps committing straight to `main` as before.

* **Verification moves into CI.** `deploy.yml` gains a test job (pytest +
  ruff) that the build depends on, so a PR cannot go green without it.

* **Agents cannot declare done on a red suite.** A Stop hook runs pytest and
  ruff and blocks completion when either fails.

* **Start local, move to Actions later.** `make factory ISSUE=n` runs the job
  headless on this machine. A label-triggered GitHub Action comes after a few
  clean lane-1 PRs.

## How to Demo
**Setup**: `gh` authenticated; `claude` CLI installed; `uv sync` done.

**Steps**:
1. Open a "Speaker confirmed" issue for the December 10 meeting.
2. `make factory ISSUE=<n>`.
3. Open the PR it creates.

**Expected output**: a PR on a `factory/issue-<n>` branch that edits only
`content/meetings/28-meeting.md`, with green CI, a plan in the description,
and the reviewer agent's notes. After merge the talk shows on the site and in
the calendar feed.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
