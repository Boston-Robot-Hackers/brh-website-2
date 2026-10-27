---
description: Run one factory job end to end, from a GitHub issue to a pull request
argument-hint: <issue number>
allowed-tools: Read Write Edit Glob Grep Agent Bash(gh *) Bash(git *) Bash(uv *) Bash(tools/golden_diff.sh*) Bash(ls *) Bash(mv *)
---
Run factory job for issue #$ARGUMENTS.

You are running **unattended**. Nobody will answer a question. The factory-lane
rules in `.claude/process.md` apply: the pull request is the approval gate, so
do not stop to ask for "go". When you cannot proceed, say why on the issue and
stop — never guess past a gap.

## Hard limits

* Never push to `main`, never merge, never close the issue yourself.
* Never edit `.claude/`, `.github/`, `.githooks/`, `Makefile` or `tools/`. The
  factory does not change its own rules.
* Work only on the current branch (the Makefile has already created
  `factory/issue-$ARGUMENTS` in a separate worktree off `origin/main`).

## 1. Read and classify

Run `gh issue view $ARGUMENTS --json number,title,body,labels`.

* Label `lane:content` → **lane 1**.
* Label `lane:refactor` → **lane 2**.
* Anything else, or both → comment "Not a factory job: <reason>" with
  `gh issue comment` and stop.

Write a short plan (what file(s) change and how you'll verify) — it becomes the
top of the PR description.

## 2a. Lane 1 — speaker confirmed

1. Find the meeting in `content/meetings/` whose frontmatter `date:` equals the
   issue's meeting date. It must be `kind: main`. If there's no match, more
   than one, or it already has a `speaker`, comment with what you found and
   stop.
2. Set `speaker`, `topic` and `text` (the blurb) in that file's frontmatter,
   copying names and titles **exactly** as the issue spells them. Leave every
   other field alone.
3. If the issue includes announcement text, write a news post modelled on the
   most recent `content/news/*-talk-announcement.md` (same frontmatter keys,
   next free number, `published_date` = today) and set the meeting's
   `announcement` field to its filename. If not, skip it and say so in the PR.
4. Verify:
   * `uv run python build/build.py` succeeds.
   * The topic appears in `output/upcoming-talks.txt` and the speaker in
     `output/meetings.ics`.
   * `git diff --name-only origin/main` lists only files under `content/`.

## 2b. Lane 2 — behavior-preserving refactor

1. The issue names a feature (`FNN`) in `process/03-features/notdone/`. Read
   it. If its intent changes what the site outputs, this is not lane 2:
   comment and stop.
2. If it has no task file, write `TFNN-<slug>.md` per `.claude/process.md` and
   `/feature`'s rules — but skip `/feature`'s stop-and-wait gate.
3. Implement task by task, following `.claude/style_guide.md`. Mark each task
   done with a one-line **Result**.
4. Verify:
   * `tools/golden_diff.sh origin/main` reports identical output.
   * `uv run pytest -q` and `uv run ruff check .` pass.
5. Close the feature per `/close-feature` (move files to `done/`).

## 3. Independent review

Dispatch the `reviewer` agent with only: the issue text, and
`git diff origin/main`. It has not seen your work, which is the point. Ask it
for blocking problems only — wrong facts vs. the issue, style-guide MUST
violations, anything that changes behavior in lane 2.

If it reports a blocker, fix it and review once more. If a blocker remains,
open the PR as a **draft** with the finding at the top.

## 4. Ship the PR

1. Commit: `Factory: <issue title> (#$ARGUMENTS)`.
2. `git push -u origin HEAD`.
3. `gh pr create --base main` with this body:

   * **Plan** — from step 1.
   * **Changes** — files touched, one line each.
   * **Checks** — each command you ran and its result.
   * **Review** — the reviewer's notes, verbatim, or "no findings".
   * `Closes #$ARGUMENTS`

4. Comment the PR link on the issue.

End with one line: the PR URL, or why you stopped.
