# TF11 Description for Feature F11

**Date Created:** 2026-09-20

## TF11.0 — Add `site_url` to `config/site.json`
**Status**: done
**Description**:
* Add `"site_url": "https://bostonrobothackers.com"`.
* No trailing slash; the builder joins with `/`.

**Test**: config test asserts `site_url` exists, starts with `https://`, and has no trailing slash.

**Result**:

* Added `site_url` and `registration_url` (`https://brh.eventbrite.com`, the link current announcements use) to `config/site.json`.
* `build_upcoming_talks` raises if either key is missing.
* Tests in `tests/test_upcoming_talks.py::TestSiteConfig`.

## TF11.1 — Add `speaker` / `topic` to current talks
**Status**: done
**Description**:
* `content/meetings/25-meeting.md`: Arjun Viswanathan, "Reinforcement Learning for Multimodal Locomotion".
* `content/meetings/24-meeting.md`: Yun Chang, "Robot Scene Understanding for Extreme Environments: From Subterranean to Heavy Equipment".
* Past talks are not backfilled — they can never qualify.

**Test**: covered by TF11.4's integration check; no standalone test (pure content).

**Result**:

* Added `speaker`/`topic` to `25-meeting.md` (Arjun, Oct 15) and `24-meeting.md` (Yun Chang, Nov 12).

## TF11.2 — `ContentManager.get_upcoming_talks`
**Status**: done
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

**Result**:

* `get_upcoming_talks(today)` added, plus a `format_long_date` helper.
* `get_future_meetings` gained an optional `today` (for frozen-date tests) and an `id` per entry (for the meeting-page fallback).
* 8 new tests in `tests/test_content_manager.py`.

## TF11.3 — Text template + `build_upcoming_talks` in `build/build.py`
**Status**: done
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

**Result**:

* `templates/pages/upcoming-talks.txt` plus `WebsiteBuilder.build_upcoming_talks`, called from `build()` with `date.today()`.
* Template tests in `tests/test_upcoming_talks.py::TestTemplate`, including one for literal `&`, quotes, and `<` (no escaping).

* Dropped 2026-09-21 (user decision): the empty-list "no talks scheduled" line and its test; the template's `{% else %}` branch was removed.

## TF11.4 — Write tests (dedicated)
**Status**: done
**Description**:
* Consolidate and fill gaps across TF11.0–TF11.3.
* Add one build-level test: run the real build against real content and assert on `output/upcoming-talks.txt`:
  * It exists.
  * It contains Arjun and Yun Chang.
  * It contains no "Hands-On" and no "to be announced".
* Freeze "today" (e.g. 2026-09-18) so the test doesn't rot as dates pass.

**Test**: this task is the tests.

**Result**:

* `TestRealBuild` builds against real content with today frozen at 2026-09-18.
* It also checks that a missing config key raises.
* Full suite: 158/158 pass.

## TF11.5 — Full verification
**Status**: done
**Description**:
* `uv run python build/build.py` builds cleanly.
* `uv run pytest` passes in full.
* `uvx ruff check build/ tests/` shows no new findings.
* Manual: paste the file's contents into a Gmail draft; URLs stay plain and clickable.

**Test**: the commands above; manual paste check recorded here.

**Result**:

* Build is clean and `uv run pytest` passes (158/158).
* `uvx ruff check build/ tests/`: no new findings (the one remaining E501 is pre-existing in `tests/test_signup_qr.py`).
* **Bug fixed 2026-09-21**: em dashes showed as `â€”` when served as `text/plain` without a charset (e.g. `make try`'s `http.server`). The file is now written with a UTF-8 BOM; regression test `TestRealBuild::test_starts_with_utf8_bom`.
* Manual Gmail paste check: confirmed by the user 2026-09-21.
