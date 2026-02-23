# brh-website-2 Feature List

Status values:
- **Status**: `not started` / `in progress` / `done`
- **Tests written**: `no` / `yes`
- **Tests passing**: `n/a` / `no` / `yes`

---

<!-- ===== INCOMPLETE FEATURES (High → Medium → Low) ===== -->

## F01 — Test Suite
**Priority**: High
**Status**: not started | Tests written: no | Tests passing: n/a
**Description**: Add a pytest test suite covering the core build modules: `ContentManager` (markdown parsing, frontmatter extraction, date handling, hero generation), `PageBuilder` (template rendering, page output), and `AssetManager` (directory copying, CSS generation). Tests should run via `uv run pytest` from the repo root.

---

<!-- ===== COMPLETED FEATURES (High → Medium → Low) ===== -->

## F02 — Static Site Build System
**Priority**: High
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: `WebsiteBuilder` orchestrates a full site build: cleans `output/`, copies assets (images, scripts, CSS), generates Pygments syntax CSS, and builds all pages. Entry point: `uv run python build/build.py`.

---

## F03 — Content Loading and Markdown Processing
**Priority**: High
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: `ContentManager` loads Markdown files with YAML frontmatter from `content/` subdirectories, converts to HTML using the `markdown` library (codehilite, fenced_code, tables, toc extensions), handles date parsing from frontmatter or filename, and sorts content by configurable key.

---

## F04 — Jinja2 Page Rendering
**Priority**: High
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: `PageBuilder` renders Jinja2 templates from `templates/` with injected content and writes complete HTML pages to `output/`. Supports full pages, detail pages per content item, and reusable card/component rendering.

---

## F05 — Asset Management
**Priority**: High
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: `AssetManager` copies `images/` and `scripts/` directories to `output/`, copies `css/shared.css` and `css/main.css`, generates Pygments syntax-highlighting CSS, and wipes `output/` clean before each build.

---

## F06 — Multi-Page Site Generation
**Priority**: High
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: Builds six page types: index, whatsnew (news list + meetings sidebar), projects (list + detail pages), members (list + detail pages), meetings (list + detail pages), and about. Each page uses a dedicated Jinja2 template.

---

## F07 — Upcoming Meetings Hero Section
**Priority**: Medium
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: The index page hero dynamically injects the two nearest upcoming meetings (parsed from `content/meetings/` frontmatter dates). Supports `MM/DD/YYYY` and `YYYY-MM-DD` date formats. Links to announcement news items if specified in frontmatter.

---

## F08 — GitHub Actions CI/CD
**Priority**: Medium
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: GitHub Actions workflow builds the site and deploys to GitHub Pages on push to main branch.

---

## F09 — Highlighted News Filtering
**Priority**: Low
**Status**: done | Tests written: no | Tests passing: n/a
**Description**: News items support a `highlight: true` frontmatter flag. The index page shows only highlighted posts; the whatsnew page shows all posts.

---
