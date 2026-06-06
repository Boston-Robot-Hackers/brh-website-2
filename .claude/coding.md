# Coding Standards

## General Python (applies everywhere)

### Language and style
* Write code in Python 3; always use `python3` and `pip3` — never `python` or `pip`
* Write idiomatic Python
* Always have a shebang line (`#!/usr/bin/env python3`)
* First comment: module name and one-line description
* Second comment: `Author: Pito Salas and Claude Code`
* Third comment: `Open Source Under MIT license`
* Use double quotes throughout; single quotes only when specifically required
* Put all imports at the top of the file
* Use absolute imports with module aliases rather than relative imports

### Structure and organization
* Functions and methods no longer than 50 lines
* Files no longer than ~300 lines
* One class per file; name the file after the class
* Put dataclasses in the file where they are constructed
* Give classes, methods and functions intention-revealing names; abbreviate to keep identifiers ≤ ~15 chars
* Avoid if/else nested more than 1 deep — find another design
* No if statement with more than 3 branches — find another design
* Avoid 1-line and 2-line methods
* Avoid simple wrappers
* Avoid functions with more than 3 arguments
* No default parameters on functions — make callers provide all values explicitly
* Do not assign a function result to a variable used only once; call the function directly

### Code quality
* Look for code duplication and DRY it up when it makes sense
* Do not go overboard on error checking
* Never use bare `except Exception:` — be specific and log or re-raise
* Do not code defensively; let exceptions bubble up

#### Fail fast on what you control
We own our content, config, and internal contracts. Treat a malformed value
there as a bug to fix at the source — not a case to detect and silently repair.

* One canonical format per concept (dates are ISO `YYYY-MM-DD`, IDs are slugs, …). Enforce it; don't accept variants.
* No multi-format fallback loops (`for fmt in [...]: try/except`) over data we author — that's a smell.
* On bad input, raise with context (name the value and the file); never coerce or rewrite it to "make it work".
* Never return the bad input unchanged as a fallback (e.g. `format_date("garbage") -> "garbage"`) — it hides the problem downstream.
* Never `except Exception: return None` (or `continue`) to swallow a bug and keep going — that turns a loud failure into silent-wrong output.
* Validate once at the boundary (when content loads), not defensively at every use site.
* Litmus test: "Could this malformed value only exist because *we* made a mistake?" If yes → assert/raise. Only genuinely external, untrusted input (web forms, third-party APIs) gets validate-and-reject — and even then, reject, don't silently fix.
* Add a comment to a method or function ONLY if the name is not self-explanatory
* Follow YAGNI: only add code explicitly required by current requirements
* Prefer async/await over threading when there is a choice
* Look for existing libraries before reinventing solutions
* Undertake multi-step refactoring so a runnable program exists after each step

---

## Standalone library code

### Packaging
* Use standard Python packaging with `pyproject.toml` and `setuptools`
* Install with `pip3 install -e . --break-system-packages` on Raspberry Pi
* Source directory name must match the project directory name
* If the repo also needs to work as a ROS2 colcon package, add `package.xml`, `setup.py`, and `resource/<package_name>` alongside `pyproject.toml`

### Design
* Library modules expose clean classes and functions — no `main()`, no `argparse`
* All configuration flows through a config dataclass loaded from YAML — no hardcoded values
* Example scripts in `examples/` are thin wiring scripts (~40 lines); all real logic lives in the library package
* Do not import ROS2 packages (`rclpy`, `sensor_msgs`, etc.) from library modules — keep the standalone path ROS-free

---

## ROS2 package code

### Structure
* ROS2 nodes live under a `ros/` subpackage and are the only place that imports `rclpy` or ROS message types
* Nodes are lifecycle nodes (`rclpy.lifecycle.Node`) where appropriate
* Message conversion helpers go in `ros/converters.py`, not in the node

### Launch files
* Use `better_launch` — not the standard `ros2 launch` Python API
* Launch files live in `launch/` with `.launch.py` extension
* Entry point is `@launch_this` decorator on a plain Python function
* Function parameters with type annotations become CLI arguments automatically — no substitution DSL
* Use `bl.node(...)`, `bl.group(...)`, `bl.include(...)` — plain Python, no deferred evaluation
* Lifecycle nodes transitioned via `node.lifecycle.transition(LifecycleStage.ACTIVE)`
* Files work with both `bl` CLI and `ros2 launch`

### Dependencies
* ROS2 runtime dependencies (`rclpy`, `sensor_msgs`, `vision_msgs`, `diagnostic_updater`) are system-installed via apt — do not add them to `pyproject.toml`
* Declare them as `exec_depend` in `package.xml`

---

## Combined repo (standalone + ROS2 in one repo)

* The repo must be cloneable standalone (`pip3 install -e .`) and into `ros2_ws/src` (`colcon build`) without any changes
* Required files for dual packaging: `pyproject.toml`, `package.xml`, `setup.py`, `resource/<package_name>`
* ROS2 imports must never appear outside the `ros/` subpackage — guard with `try/except ImportError` if truly needed at the boundary
* `pyproject.toml` build backend: `setuptools.build_meta`
* Tests in `tests/` must run with plain `pytest` — no `colcon test` dependency
