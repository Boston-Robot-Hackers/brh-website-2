# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website generator for the Boston Robot Hackers community. Python + Jinja2 templates + UV package management. Content is written in Markdown with YAML frontmatter. Build outputs to `output/`.

## Commands

```bash
# Install dependencies
uv sync

# Build the full website
uv run python build/build.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_content_manager.py

# Run a specific test
uv run pytest tests/test_content_manager.py::TestClassName::test_method_name

# Run tests with coverage
uv run pytest --cov=build
```

## Architecture

The build system lives in `build/` and is composed of three modules orchestrated by `WebsiteBuilder` in `build/build.py`:

- **`content_manager.py`** — Loads and processes Markdown files using `python-frontmatter` and the `markdown` library (with codehilite, fenced_code, tables, toc extensions). Handles date parsing from frontmatter or filename prefix. Builds hero content from `content/heroes/`. Dynamically injects upcoming meeting dates into the index hero.
- **`page_builder.py`** — Renders Jinja2 templates and writes HTML files to `output/`. Handles both listing pages and per-item detail pages (news, projects, members, meetings).
- **`asset_manager.py`** — Copies static assets (CSS, images, scripts) to `output/` and generates Pygments syntax highlighting CSS.

The `build/` directory has its own `pyproject.toml` and `.venv` (Python 3.13), separate from the root-level `pyproject.toml` (Python 3.12+). Tests use the root `pyproject.toml` with `pythonpath = ["build"]`.

## Content Files

All content lives in `content/` as Markdown with YAML frontmatter:

- `content/news/*.md` — News posts. Key fields: `title`, `date`, `image`, `excerpt`, `highlight` (bool — only highlighted posts appear on homepage)
- `content/members/*.md` — Member profiles. Key fields: `name`, `role`, `image`, `featured`, `skills`, `github`, `linkedin`, `projects`, `opentowork`
- `content/projects/*.md` — Project descriptions. Key fields: `title`, `image`, `excerpt`
- `content/meetings/*.md` — Meeting entries. Key fields: `title`, `date` (MM/DD/YYYY format), `time`, `location`, `announcement` (filename of linked news post)
- `content/heroes/*.md` — Hero section content for each page (named by page: `index.md`, `about.md`, `members.md`, etc.). The `index.md` hero uses an `<hr>` as a separator — content above is static, content below is replaced dynamically with upcoming meeting info.
- `content/about.md` — About page content

Filename convention for dated content: `YYYY-MM-DD-slug.md` (date is extracted from filename if not in frontmatter).

## Templates

Jinja2 templates in `templates/`:
- `layouts/` — `base.html`, `home.html`, `page.html`, `detail.html`
- `pages/` — One template per page (`index.html`, `about.html`, `members.html`, `projects.html`, `whatsnew.html`, `meetings.html`)
- `components/` — Reusable partials (`head.html`, `navigation.html`, `hero.html`, `footer.html`, `banner.html`, `section.html`, `upcoming-meetings-calendar.html`)
- `cards/` — Card components for listings
- `details/` — Detail page templates for individual items

## Configuration

`config/site.json` — Site-wide text strings (title, section titles, button labels, footer text). Available in all templates as the `site_config` context variable.

## Deployment

GitHub Actions automatically deploys to GitHub Pages on push to `main`. The `output/` directory is not committed; it's generated during the CI build.
