#!/usr/bin/env bash
# Stop hook: refuse to let Claude finish while the test suite or ruff is red.
# Exit 2 sends stderr back to Claude as the reason it can't stop yet.
#
# Only enforces when the working tree has uncommitted changes, so a chat-only
# turn in an interactive session is never blocked. Honors stop_hook_active
# (set when Claude is already continuing because of this hook) so a suite
# that can't be fixed ends in a report rather than an infinite loop.

input=$(cat)
if echo "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

project_dir="${CLAUDE_PROJECT_DIR:-.}"
cd "$project_dir" || exit 0

if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
  exit 0
fi

command -v uv >/dev/null 2>&1 || exit 0

failures=""
if ! test_output=$(uv run pytest -q 2>&1); then
  failures+=$'pytest failed:\n'"$(echo "$test_output" | tail -25)"$'\n'
fi
if ! lint_output=$(uv run ruff check . 2>&1); then
  failures+=$'ruff failed:\n'"$(echo "$lint_output" | tail -25)"$'\n'
fi

if [[ -n "$failures" ]]; then
  {
    echo "Not done: the working tree has changes and the checks are red."
    echo "Fix these, or if they can't be fixed, say so plainly and stop."
    echo
    echo "$failures"
  } >&2
  exit 2
fi
exit 0
