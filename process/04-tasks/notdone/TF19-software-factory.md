# TF19 Description for Feature F19

**Date Created:** 2026-10-27

## TF19.0 — Stop hook that blocks completion on a red suite
**Status**: done

**Description**: `.claude/hooks/stop-verify.sh`, registered under `Stop` in
`.claude/settings.json`. Runs `uv run pytest -q` and `uv run ruff check .`;
on failure prints the tail of the output to stderr and exits 2, which sends
Claude back to work instead of letting it finish. Honors
`stop_hook_active` so it cannot loop forever.

**Test**: `tests/test_factory.py` — hook exits 0 when `stop_hook_active` is
true; the hook is registered in `settings.json` under `Stop`.

## TF19.1 — CI verifies before it builds
**Status**: done

**Description**: Add a `test` job to `.github/workflows/deploy.yml` (uv sync,
pytest, ruff) and make `build` depend on it. Pull requests to `main` already
trigger the workflow, so factory PRs get gated.

**Test**: `tests/test_factory.py` — parse the workflow, assert the `test` job
runs pytest and ruff and that `build.needs` includes `test`.

## TF19.2 — Golden-output diff for refactor lane
**Status**: done

**Description**: `tools/golden_diff.sh [BASE_REF]` builds `BASE_REF`
(default `origin/main`) in a temporary git worktree and the working tree in
place, then `diff -r` the two `output/` trees ignoring `DTSTAMP:` lines (the
only nondeterministic content — verified by building twice). Exit 0 when
identical.

Lives in a new `tools/` folder, not `scripts/`: the build copies all of
`scripts/` into `output/`, so anything there is published to the live site.

**Result**: `make golden` against `origin/main` reports identical output.

**Test**: `tests/test_factory.py` — run the diff logic on two temp trees:
identical except `DTSTAMP` → passes; a real content change → fails.

## TF19.3 — `/factory-run` command
**Status**: done

**Description**: `.claude/commands/factory-run.md`. Reads the issue with `gh`,
classifies it into lane 1 or lane 2 (anything else: comment on the issue and
stop), works on a `factory/issue-<n>` branch, applies the lane's checks,
runs the `reviewer` agent cold on the diff, then pushes and opens a PR whose
description holds the plan, the checks run, and the review notes.

**Test**: not feasible as a unit test — it is a prompt. Exercised by the F19
demo (one real lane-1 issue end to end).

## TF19.4 — "Speaker confirmed" issue form
**Status**: done

**Description**: `.github/ISSUE_TEMPLATE/speaker-confirmed.yml` with required
fields: meeting date, speaker, topic, short blurb; optional announcement
text. Applies the `factory` and `lane:content` labels.

**Test**: `tests/test_factory.py` — form parses, required fields present,
labels set.

## TF19.5 — Makefile targets
**Status**: done

**Description**: `make factory ISSUE=n` runs `claude -p "/factory-run n"`
headless; `make golden` runs the golden diff. Both listed in `make help`.

**Test**: `tests/test_factory.py` — every Makefile target appears in `help`.

## TF19.6 — Factory-lane rules in `process.md`
**Status**: done

**Description**: New `# factory lanes` section: which work qualifies, that the
PR replaces the "wait for go" gate and the "no pull requests" rule *only*
for factory branches, and that interactive work is unchanged.

**Test**: not feasible — prose rule. Covered by review.

## TF19.7 — Tests
**Status**: done

**Description**: `tests/test_factory.py` covering TF19.0, .1, .2, .4, .5.

**Test**: `uv run pytest` — full suite green.

**Result**: 17 new tests; 219 pass, ruff clean. Stop hook also exercised by
hand: exit 0 on a green dirty tree, exit 2 with the pytest tail on a red one.

## TF19.9 — Factory guard hook
**Status**: done

**Description**: `.claude/hooks/factory-guard.sh`, a `PreToolUse` hook on
`Bash`. On `factory/*` branches only, blocks `git push` to main, `gh pr
merge` and `gh issue close`, so the command's hard limits are enforced
rather than requested. Interactive branches are untouched.

**Test**: `tests/test_factory.py` — blocks each of the three on a factory
branch, allows `git push -u origin HEAD`, allows pushing main from `main`.

## TF19.8 — Demo: first real lane-1 run
**Status**: not done

**Description**: Pito opens a "Speaker confirmed" issue for a real speaker
and runs `make factory ISSUE=<n>`. Review the PR, merge, confirm the site.

**Test**: the PR's CI and the merged site.
