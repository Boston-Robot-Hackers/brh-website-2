# F12 — Turn build/ into a proper Python package
**Priority**: Low
**Done:** no
**Tasks File Created:** no
**Tests Written:** no
**Test Passing:** no

**Description**:
* Found during a code/architecture deep-dive review (session on the
  `deepdive` branch). Not a bug — the build works correctly today. This
  is a maintainability/tooling gap.
* `build/` has no `__init__.py` and is not a real, installable Python
  package. Its five modules (`build.py`, `content_manager.py`,
  `page_builder.py`, `asset_manager.py`, `news_links.py`) import each
  other as bare top-level names, e.g. `from content_manager import
  ContentType, classify_meeting, parse_date` rather than `from
  build.content_manager import ...`.
* This works today through two separate, easy-to-miss mechanisms:
  1. Running `build/build.py` directly as a script puts its own
     directory (`build/`) on `sys.path[0]`, so its sibling modules
     resolve as top-level imports.
  2. `pyproject.toml`'s `[tool.pytest.ini_options] pythonpath = ["build"]`
     does the same trick for the test suite.
* Consequences of the current setup:
  * Standard tooling that expects a real package (type checkers like
    mypy/pyright run in strict "no untyped `sys.path` hacking" modes,
    `python -m build.build`, editable installs via `pip install -e .`)
    doesn't work without extra configuration a new contributor has to
    discover.
  * IDE "go to definition" / "find references" across module boundaries
    can be less reliable without an explicit package structure some
    IDEs key off of.
  * The dependency on `pythonpath = ["build"]` is a single line a future
    contributor could delete (e.g. while tidying `pyproject.toml`)
    without realizing it silently breaks every test's imports.
* **Proposed fix** (either is behavior-preserving if done carefully):
  * **Option A — minimal**: add `build/__init__.py` (can be empty) and
    switch the five modules' cross-imports to explicit relative imports
    (`from .content_manager import ...`). Update `pytest`'s
    configuration accordingly (likely `pythonpath = ["."]` with `build`
    imported as `build.content_manager`, or keep `rootdir`-relative
    imports — needs a small spike to get right without breaking the
    "run `build/build.py` directly" entry point, which would need
    updating to `python -m build.build` or an equivalent wrapper).
  * **Option B — larger**: move to a `src/build_site/` layout (avoiding
    the name clash with the standard library's `build` package name)
    with a proper `pyproject.toml` entry point (e.g. `brh-build =
    "build_site.build:main"`), so the whole thing is installable and
    invocable as `uv run brh-build` instead of a raw script path. This
    also sidesteps `build/` shadowing the third-party `build` PyPI
    package name, which is a latent foot-gun for anyone who later adds
    that package as a dependency.
* Either option should preserve today's `uv run python build/build.py`
  and `uv run pytest` invocations (updating the Makefile/README/CI to
  match, if the invocation syntax needs to change).

**Non-goals**:
* Not part of this: adding type hints project-wide, adding mypy/pyright
  to CI, or otherwise expanding static-analysis tooling. This feature is
  only about making the package structure itself sound; using that
  soundness for stricter tooling is a separate, later decision.

## How to Demo
**Setup**: `uv sync && uv run pytest && uv run python build/build.py`
(or their post-change equivalents, whatever the chosen invocation ends
up being — documented in the corresponding task file).

**Steps**:
1. Full test suite passes, same 138 tests, same results.
2. `output/` is byte-identical to a pre-change build (diff the two
   `output/` trees).
3. CI's `deploy.yml` workflow still builds and deploys successfully
   (verify via a dry run or a non-`main` branch push, since this repo's
   CI triggers on `main`).

**Expected output**: No visible change to the built site or test
results — this is a structural refactor of how Python code is organized
and imported, not a behavior change.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
