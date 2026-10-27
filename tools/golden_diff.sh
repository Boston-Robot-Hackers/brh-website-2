#!/usr/bin/env bash
# golden_diff — prove a refactor left the built site unchanged
#
#   tools/golden_diff.sh [BASE_REF]        build BASE_REF and the working tree, compare
#   tools/golden_diff.sh --compare A B     compare two existing output trees
#
# BASE_REF defaults to origin/main. The base is built in a throwaway git
# worktree so the working tree is never touched. Exit 0 = identical.
#
# DTSTAMP lines in meetings.ics are ignored: they record build time and are
# the only nondeterministic bytes in a build (verified by building twice).

set -euo pipefail

compare() {
  if diff -r -I '^DTSTAMP:' "$1" "$2"; then
    echo "golden: identical (ignoring DTSTAMP)"
  else
    echo "golden: OUTPUT CHANGED — not a behavior-preserving refactor" >&2
    return 1
  fi
}

if [[ "${1:-}" == "--compare" ]]; then
  compare "$2" "$3"
  exit $?
fi

base_ref="${1:-origin/main}"
repo_root=$(git rev-parse --show-toplevel)
scratch=$(mktemp -d)
trap 'git -C "$repo_root" worktree remove --force "$scratch/base" >/dev/null 2>&1; rm -rf "$scratch"' EXIT

git -C "$repo_root" worktree add --detach --quiet "$scratch/base" "$base_ref"

echo "golden: building $base_ref"
(cd "$scratch/base" && uv run --quiet python build/build.py >/dev/null)

echo "golden: building working tree"
(cd "$repo_root" && uv run --quiet python build/build.py >/dev/null)

compare "$scratch/base/output" "$repo_root/output"
