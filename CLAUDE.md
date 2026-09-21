# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

See [README.md](README.md) for what this project is, its architecture, content
model, templates, and configuration. This file covers only how to work in the
repo as an agent.

## Commands

```bash
# Install dependencies
uv sync

# Build the full website
uv run python build/build.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_content_manager.py

# Run a specific test
uv run pytest tests/test_content_manager.py::TestClassName::test_method_name

# Run tests with coverage
uv run pytest --cov=build
```

## Development Process

Read and follow all rules in the `.claude/` folder:
- @.claude/process.md — development workflow, feature/task tracking rules, and
  agent model selection
- `process/02-doc/current.md` — session handoff; only the `## Open` section matters for
  new work, see `process/02-doc/history.md` for the completed-work log
- `process/02-doc/notes.md` — semi-permanent project notes

Before writing or reviewing code, read and follow `.claude/style_guide.md`
(coding standards, style rules, and review checklist) — apply it yourself
before committing; do not substitute a generic/plugin review for it.

Features and tasks tracked in j3 structure:
- `process/02-doc/spec.md` — app description and goals
- `process/02-doc/current.md` — session handoff and current status
- `process/02-doc/notes.md` — architecture decisions and notes
- `process/03-features/notdone/` — FNN-slug.md planned features
- `process/03-features/done/` — completed features
- `process/04-tasks/notdone/` — TFNN-slug.md pending tasks
- `process/04-tasks/done/` — completed tasks
- `process/05-issues/` — bugs not yet converted to features

## Session Start

At session start, read `process/02-doc/current.md`'s `## Open` section for status and
next steps. If it is unreadable, fall back to `git log --oneline -15` and say
so. (The `/start` skill already does this in more depth — use it when
available; this is the fallback.)

## Workflow & Approval Gates

Do not run tests, commits, or multi-file changes until the user has explicitly
approved the plan. Present the plan, wait for "go", then execute. Never jump ahead
of a process gate.

- **Stuck-loop rule**: if the same tool call fails or returns unchanged output
  twice, stop retrying. Report the failure, what was tried, and a proposed
  workaround (e.g. `cat` via Bash instead of Read), then wait for direction.

## Accuracy Rules

Never state a fact about the environment (model backend, Docker availability,
schema semantics, file existence) from naming conventions or inference. Read the
config/file first, then state the finding and cite the source. If you cannot
verify, say "unverified" explicitly.

## Environment & Data Access

This checkout may not include required credentials or data files. Before any
live external-system or data-extract work, check for these and stop with a
short list of what's missing instead of improvising.

## Write Safety

Treat any live external system (database, API, SaaS platform) as read-only by
default. Do not write, update, or delete data through a live integration
unless the user has explicitly approved it. If the project has a dedicated
read-only client/wrapper, use it exclusively — do not construct or reach
through to the raw client elsewhere. If a task seems to need a write, stop
and ask; it is rarely the right default.

## Tone

No flattery, no praise openers ("Great question!", "You're absolutely right").
Lead with the answer or the finding. Be direct and terse.
