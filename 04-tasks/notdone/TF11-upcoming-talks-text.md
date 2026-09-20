# TF11 Description for Feature F11

## TF11.0 — Add `site_url` to `config/site.json`
**Status**: not done
**Description**:
* Add `"site_url": "https://bostonrobothackers.com"`.
* No trailing slash; the builder joins with `/`.

**Test**: config test asserts `site_url` exists, starts with `https://`, and has no trailing slash.

## TF11.1 — Add `speaker` / `topic` to current talks
**Status**: not done
**Description**:
* `content/meetings/25-meeting.md`: Arjun Viswanathan, "Reinforcement Learning for Multimodal Locomotion".
* `content/meetings/24-meeting.md`: Yun Chang, "Robot Scene Understanding for Extreme Environments: From Subterranean to Heavy Equipment".
* Past talks are not backfilled — they can never qualify.

**Test**: covered by TF11.4's integration check; no standalone test (pure content).

## TF11.2 — `ContentManager.get_upcoming_talks`
**Status**: not done
**Description**:
* New method in `build/content_manager.py`, built on `get_future_meetings`.
* Keeps meetings where `classify_meeting` is `main` **and** `speaker` and `topic` are both non-empty.
* Returns per talk: `topic`, `speaker`, `summary` (`text`), `date_obj`, `time`, `location`, `page_path`.
* `page_path` = `news/<announcement>.html` if it resolves, else `meetings/<id>.html`.

**Test**: `tests/test_content_manager.py`, using fixture meeting files:
* Past talk excluded.
* Hands-on excluded.
* Missing speaker excluded; missing topic excluded.
* Qualifying talk included, sorted ascending.
* `page_path` uses announcement when present, meeting page when not.

## TF11.3 — Text template + `build_upcoming_talks` in `build/build.py`
**Status**: not done
**Description**:
* New `templates/pages/upcoming-talks.txt` (Jinja, plain text).
* Header, one block per talk, footer (Eventbrite link, `site_url/meetings.html`).
* Date formatted as "Thursday, October 15, 2026".
* URL = `site_url` + `/` + `page_path`.
* `WebsiteBuilder.build_upcoming_talks` renders it to `output/upcoming-talks.txt`; called from `build()`.
* The Jinja env has no autoescape, so `&`/quotes in topics stay literal.

**Test**: `tests/test_page_builder.py` (or new `tests/test_upcoming_talks.py`) renders the template with sample talks:
* Every URL matches `^https://bostonrobothackers\.com/\S+$`.
* No `google.com`, no `<`/`>`, no HTML entities.
* Empty-list case renders a "no talks scheduled" line, not an empty file.

## TF11.4 — Write tests (dedicated)
**Status**: not done
**Description**:
* Consolidate and fill gaps across TF11.0–TF11.3.
* Add one build-level test: run the real build against real content and assert on `output/upcoming-talks.txt`:
  * It exists.
  * It contains Arjun and Yun Chang.
  * It contains no "Hands-On" and no "to be announced".
* Freeze "today" (e.g. 2026-09-18) so the test doesn't rot as dates pass.

**Test**: this task is the tests.

## TF11.5 — Full verification
**Status**: not done
**Description**:
* `uv run python build/build.py` builds cleanly.
* `uv run pytest` passes in full.
* `uvx ruff check build/ tests/` shows no new findings.
* Manual: paste the file's contents into a Gmail draft; URLs stay plain and clickable.

**Test**: the commands above; manual paste check recorded here.
