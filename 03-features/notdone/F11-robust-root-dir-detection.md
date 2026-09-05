# F11 — Robust project-root detection in WebsiteBuilder
**Priority**: Low
**Done:** no
**Tasks File Created:** no
**Tests Written:** no
**Test Passing:** no

**Description**:
* Found during a code/architecture deep-dive review (session on the
  `deepdive` branch). Not a reported bug — the build works correctly
  today under normal invocation. This is a robustness gap.
* `WebsiteBuilder.__init__` (`build/build.py:24-30`) decides where the
  project root is like this:
  ```python
  current_dir = Path.cwd()
  if current_dir.name == "build":
      self.root_dir = Path("..")
  else:
      self.root_dir = Path(".")
  ```
  It infers the root purely from the *name* of the current working
  directory at the moment the script runs, not from where the script
  file itself lives.
* This works for the two ways the project is normally invoked today
  (`uv run python build/build.py` from the repo root, or `cd build &&
  uv run python build.py`), but breaks or silently misbehaves for:
  * Running from any other cwd (e.g. an IDE's "run current file" that
    launches with the repo root as cwd but resolves paths differently,
    or a task runner that sets a different cwd).
  * A checkout or symlink where the repo itself happens to sit inside a
    directory literally named `build` (rare, but the check has no way to
    tell "the repo's build subdirectory" from "any directory named
    build").
  * Any future automation (cron job, packaging script, another CI step)
    that invokes `build.py` with an unexpected cwd.
* **Proposed fix**: derive the root from the script's own file location
  instead of the process's cwd:
  ```python
  self.root_dir = Path(__file__).resolve().parent.parent
  ```
  This is unconditionally correct regardless of cwd, and produces the
  exact same `root_dir` value as today for both of the currently-used
  invocation styles — a behavior-preserving change.

**Non-goals**:
* Not changing how the project is invoked (Makefile, CI, README stay the
  same).
* Not adding a `--root-dir` CLI flag or environment-variable override —
  no known use case for one today.

## How to Demo
**Setup**: `uv run python build/build.py` from the repo root, and
separately `cd build && uv run python build.py`.

**Steps**:
1. Both invocations produce byte-identical `output/` contents, same as
   before the change.
2. Full test suite (`uv run pytest`) still passes unchanged.

**Expected output**: No visible difference in build output or test
results — this is purely a robustness fix for invocation styles not
currently exercised by the Makefile, README, or CI.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
