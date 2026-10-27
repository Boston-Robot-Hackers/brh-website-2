#!/usr/bin/env bash
# PreToolUse hook (Bash): on factory/* branches, refuse anything that would
# land work without review — pushing to main, merging a PR, closing an issue.
# Interactive work on other branches is untouched.

project_dir="${CLAUDE_PROJECT_DIR:-.}"
branch=$(git -C "$project_dir" branch --show-current 2>/dev/null)
[[ "$branch" == factory/* ]] || exit 0

command=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)

block() {
  echo "factory-guard: blocked on $branch — $1. Factory work lands only through a reviewed PR." >&2
  exit 2
}

if [[ "$command" =~ git[[:space:]]+push ]] && [[ "$command" =~ (main|master)([[:space:]]|$) || "$command" =~ :(main|master) ]]; then
  block "pushing to main"
fi
[[ "$command" =~ gh[[:space:]]+pr[[:space:]]+merge ]] && block "merging a PR"
[[ "$command" =~ gh[[:space:]]+issue[[:space:]]+close ]] && block "closing an issue"
exit 0
