# F13 — Unify how CI and local tooling invoke the build
**Priority**: Low
**Done:** no
**Tasks File Created:** no
**Tests Written:** no
**Test Passing:** no

**Description**:
* Found during a code/architecture deep-dive review (session on the
  `deepdive` branch). Not a bug — both invocation styles currently
  produce a working build. This is a consistency/clarity gap.
* The site is built two different ways depending on where you look:
  * `.github/workflows/deploy.yml`:
    ```yaml
    - name: Build website
      run: |
         cd build
         uv sync
         uv run python build.py
    ```
    i.e. change into `build/`, then `uv sync` and run `build.py` from
    there.
  * `Makefile`'s `build` target, and the README's documented usage:
    ```
    uv run python build/build.py
    ```
    i.e. stay at the repo root and reference the script by its full
    path.
* Both actually work today, but only because `uv sync`/`uv run` walk up
  the directory tree looking for the nearest `pyproject.toml` — verified
  empirically during the deep-dive review: running `cd build && uv
  sync` resolves to the *root* `pyproject.toml` and the *root* `.venv`
  (there is no `build/pyproject.toml` — see the now-corrected README,
  which used to incorrectly claim there was one). It happens to be
  correct, but a reader of `deploy.yml` in isolation would reasonably
  assume `build/` is its own project, which it is not (see F12 for the
  related packaging gap). This is exactly the kind of thing that could
  break in a confusing way if `uv`'s directory-discovery behavior ever
  becomes stricter, or if someone "helpfully" adds a
  `build/pyproject.toml` back for an unrelated reason.
* **Proposed fix**: change `deploy.yml`'s build step to match the
  Makefile/README convention — run from the repo root:
  ```yaml
  - name: Build website
    run: |
       uv sync
       uv run python build/build.py
  ```
  Purely a CI YAML change; no Python code changes needed. Should be
  verified with a CI dry run (e.g. a workflow_dispatch run or a
  short-lived branch push, since the workflow already supports
  `workflow_dispatch`) before merging to `main`, since a broken deploy
  step would take the live site down until fixed.

**Non-goals**:
* Not addressing F12 (making `build/` a real package) here — this
  feature is purely about aligning the *invocation command*, independent
  of whatever internal package structure `build/` ends up with.

## How to Demo
**Setup**: Push the change to a branch and trigger the workflow via
`workflow_dispatch` (or open a PR, since the workflow also triggers on
`pull_request`), without merging to `main` yet.

**Steps**:
1. CI's build step succeeds and produces the same `output/` artifact as
   today's `cd build && uv sync && uv run python build.py` step.
2. `actions/upload-pages-artifact` uploads successfully as before.
3. Only after confirming success on a non-`main` run, merge so the next
   push to `main` uses the corrected step.

**Expected output**: Identical deployed site; the only difference is the
YAML now matches how every human runs the build locally.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
