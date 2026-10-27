# Using the software factory

The factory lets Claude Code do two narrow kinds of work **without you
watching**: it takes a labeled GitHub issue and turns it into a pull request
you review and merge.

Everything else stays interactive, under the normal plan-then-go gate.

The design and rationale are in
`process/03-features/notdone/F19-software-factory.md`; the rules agents follow
are in the *factory lanes* section of `.claude/process.md`. This file is the
how-to.

## The two lanes

* **lane:content — "Speaker confirmed".** A speaker is booked for an existing
  monthly meeting. The factory fills in `speaker`, `topic` and `text` on that
  meeting's file, optionally writes an announcement news post, rebuilds, and
  checks the talk appears in `upcoming-talks.txt` and `meetings.ics`.

* **lane:refactor — "Factory refactor".** A parked feature whose intent is
  *same site, cleaner code* (today: F12, F14, F16). The factory writes the
  task file if needed, implements it, and must prove the built site is
  byte-identical to `main` (`make golden`) with the full suite green.

**Not factory work:** anything that changes what the site shows or how it
looks — new pages, F13, F15, design changes. Do those interactively.

## One-time setup

1. **Merge `factory/bootstrap` into `main`.** Factory runs branch off
   `origin/main`, so the command, hooks and tools must be there.

2. **Create the three labels.** GitHub issue forms silently drop labels that
   don't exist yet:

   ```bash
   gh label create factory       --color 5319e7 --description "Run by the software factory"
   gh label create lane:content  --color 0e8a16 --description "Factory lane 1: content update"
   gh label create lane:refactor --color 1d76db --description "Factory lane 2: output-preserving refactor"
   ```

3. **Check your machine has what a run needs:**

   * `gh auth status` — logged in, with push access to the repo.
   * `claude --version` — Claude Code CLI on your `PATH`.
   * `uv` — installed (each run does its own `uv sync`).

## Running a job

### 1. Open the issue

On GitHub, **New issue** and pick a form:

* **Speaker confirmed** — meeting date (`YYYY-MM-DD`, must match an existing
  main meeting), speaker, talk title, a one- or two-sentence blurb, and
  optionally longer announcement text. Spell names exactly as they should
  appear on the site — the factory copies them verbatim.

* **Factory refactor** — the `FNN` of a parked feature, plus optional notes.

The form applies the `factory` and lane labels for you. Note the issue number.

### 2. Run it

From your checkout of the repo:

```bash
make factory ISSUE=42
```

This:

* creates a worktree at `../brh-factory-42` on branch `factory/issue-42`,
  fresh from `origin/main` — **your own checkout is never touched**;
* runs `claude -p "/factory-run 42"` headless there, with edits auto-accepted
  and Bash limited to `gh`, `git`, `uv`, `ls`, `mv` and the golden diff.

A content job takes a few minutes; a refactor longer. You can walk away.

### 3. What you get back

One of two outcomes, always visible on the issue:

* **A pull request** linked from an issue comment. Its description has the
  **Plan**, **Changes**, **Checks** (each command run and its result), the
  **Review** notes from the independent `reviewer` agent, and
  `Closes #42`. A PR opened as a **draft** means the reviewer flagged a
  blocker the factory couldn't fix — it's at the top of the description.

* **A comment explaining why it stopped** — e.g. no meeting on that date, the
  meeting already has a speaker, or the feature changes output so it isn't a
  refactor. Fix the issue (or do the work interactively) and re-run.

### 4. Review and merge

* Wait for CI. The workflow now runs pytest and ruff before it builds, so a
  red check means don't merge.
* Read the diff. For content, check the names and date; for refactors, the
  golden-diff line in **Checks** is your main assurance.
* **Merging is the approval.** Merge on GitHub; the push to `main` deploys the
  site and closes the issue.
* If it's wrong, comment on the PR and either fix it by hand on the branch or
  close the PR and re-run after fixing the issue.

### 5. Clean up

```bash
make factory-clean ISSUE=42
```

Removes the `../brh-factory-42` worktree. Delete the remote branch from the
merged PR's page if GitHub didn't.

## Guardrails

These are enforced by hooks, not just requested in the prompt:

* **Can't finish on a red suite.** `.claude/hooks/stop-verify.sh` runs pytest
  and ruff whenever the tree has changes and blocks the agent from stopping
  until they pass. This applies to your interactive sessions too.

* **Can't land work unreviewed.** On any `factory/*` branch,
  `.claude/hooks/factory-guard.sh` blocks pushing to `main`, `gh pr merge` and
  `gh issue close`.

* **Can't change its own rules.** Factory runs are told never to edit
  `.claude/`, `.github/`, `.githooks/`, `Makefile` or `tools/`. Treat any PR
  that touches them as suspect.

* **CI is the backstop.** Every PR runs the full test suite and lint before
  the build job.

## Handy commands

```bash
make help                 # all targets, factory ones included
make factory ISSUE=n      # run issue n
make factory-clean ISSUE=n
make golden               # is the built site unchanged vs origin/main?
make golden BASE=<ref>    # ... vs any other ref
```

`make golden` is useful interactively too — run it after any refactor you do
by hand.

## Troubleshooting

* **`fatal: '../brh-factory-n' already exists`** — a previous run's worktree
  is still there. `make factory-clean ISSUE=n`, then re-run.

* **Run ended with no PR and no comment** — the headless session errored
  before reaching GitHub. Re-run in the worktree interactively to see why:
  `cd ../brh-factory-n && claude`, then `/factory-run n`.

* **`make golden` reports a change you expected to be invisible** — read the
  diff it prints; the refactor changed output, so it isn't a lane-2 job. The
  only ignored difference is `DTSTAMP` in `meetings.ics` (build time).

* **Labels missing from a new issue** — the labels weren't created (setup step
  2). Add them by hand, then run.

## Later

* Once a few content PRs have come back clean, move the trigger to a GitHub
  Action on the `factory` label so issues run without `make factory`.
* Fold these files into the canonical `j3` kit so new projects get the
  factory from `/bootstrap`.
