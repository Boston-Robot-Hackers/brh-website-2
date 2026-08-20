# TF02 Description for Feature F02

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF02.N`, starting at `.0`.

## TF02.0 — Inventory top-level structure vs. documented structure
**Status**: done
**Description**: List every top-level directory and file, and compare
against what `CLAUDE.md` and `README.md`'s "Project Structure" section claim.
Note anything present but undocumented (`legacy/`, `archive/`,
`image-sources/`, `rules.md`) or documented but not matching reality.
**Test**: None — inventory step, no runtime behavior to assert. Findings
feed the write-up in TF02.5.

## TF02.1 — Audit dead/legacy code for removal or archival
**Status**: done
**Description**: Examine `legacy/` (an earlier Tailwind-based prototype with
its own `main.py` and `pyproject.toml`, and a git-tracked `node_modules/`)
and `archive/build.py` (an orphaned old build script). Confirm neither is
referenced by the live build, templates, or docs, and draft a specific
proposed disposition (delete vs. move out of git history) for the write-up.
**Test**: None — a `grep`-based check already confirms nothing in the live
codebase references `legacy/` or `archive/`; recorded as evidence for this
task rather than a pytest, since "this directory is unused" isn't runtime
behavior to assert.

## TF02.2 — Audit `rules.md` and other machine-specific artifacts
**Status**: done
**Description**: `rules.md` is a git-tracked symlink to an absolute path
outside the repo, so it dangles on any other checkout. Confirm nothing in
the build or `.claude/` config depends on it, and propose either removing it
from git or replacing it with a real, repo-local file.
**Test**: None — analysis step, same reasoning as TF02.1.

## TF02.3 — Audit naming and content-model consistency
**Status**: done
**Description**: Check filename conventions across `content/news/`,
`content/meetings/`, `content/members/`, `content/projects/` (numbering
scheme, hyphen vs. underscore), and cross-reference frontmatter fields
actually in use against what `CLAUDE.md`/`README.md` document, to find drift
an AI agent would trip over when adding new content.
**Test**: None — analysis step.

## TF02.4 — Reconcile against already-tracked debt
**Status**: done
**Description**: Cross-check findings against the 8 pending chores already
logged in `04-tasks/chores.md` (prior `build/*.py` style-guide review) and
the still-empty `05-issues/{open,closed,deferred}/` subfolders expected by
`.claude/process.md`, so the write-up references existing tracked work
instead of duplicating it.
**Test**: None — reconciliation step.

## TF02.5 — Write up the review and proposed changes
**Status**: done
**Description**: Produce `02-doc/structure-review.md` covering every finding
from TF02.0–TF02.4: what's inconsistent or AI-unfriendly, a concrete
proposed change for each, and a recommended disposition (chore / new
feature / defer). This is the feature's deliverable — no code or content
changes beyond writing this document.
**Test**: None — the deliverable is documentation itself, not executable
behavior.

## TF02.6 — Add a regression guardrail test
**Status**: done
**Description**: Dedicated test-writing task. Pick the review's most
durable, mechanically-checkable finding — e.g. "every `.claude/`-relative
file referenced from `CLAUDE.md` actually exists" (the exact class of bug
fixed by hand earlier: stale references to `.claude/how_to_be.md` and
`.claude/codereview.md`) — and encode it as a pytest test, so future edits
can't silently reintroduce that class of drift.
**Test**: `uv run pytest` includes and passes the new test.
