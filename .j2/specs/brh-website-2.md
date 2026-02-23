# brh-website-2 Spec

## Overview

Static website generator for the Boston Robot Hackers (BRH) community. Written in Python 3.12 using Jinja2 templates and Markdown content files. Builds a complete multi-page site into an `output/` directory, suitable for GitHub Pages deployment.

## Architecture

The build system lives in `build/` and is structured as three focused modules orchestrated by `WebsiteBuilder`:

- **`build.py`** — `WebsiteBuilder` class: orchestrates asset copying, content loading, and page rendering. Entry point via `uv run python build/build.py`.
- **`content_manager.py`** — `ContentManager` + `ContentType`: loads Markdown files with frontmatter, converts to HTML, handles date parsing, generates hero sections with upcoming meeting info.
- **`page_builder.py`** — `PageBuilder`: renders Jinja2 templates and writes HTML files to `output/`.
- **`asset_manager.py`** — `AssetManager`: copies static assets (images, scripts, CSS), generates Pygments syntax-highlighting CSS.

## Content Model

All content is Markdown files with YAML frontmatter, stored in `content/`:

| Directory | Content Type | Sort Order |
|---|---|---|
| `content/news/` | News/announcements | Date descending |
| `content/projects/` | Project descriptions | Default |
| `content/members/` | Member profiles | Title ascending |
| `content/meetings/` | Meeting records | Date descending |
| `content/heroes/` | Per-page hero sections | n/a |
| `content/about.md` | About page body | n/a |

## Pages Generated

- `index.html` — home page with highlighted news, project cards, upcoming meetings
- `whatsnew.html` — full news list + meetings sidebar
- `projects.html` + per-project detail pages
- `members.html` + per-member detail pages
- `meetings.html` + per-meeting detail pages
- `about.html`

## Templates

Jinja2 templates in `templates/`:
- `layouts/` — base layout(s)
- `pages/` — full-page templates
- `components/` — reusable partials
- `details/` — content-type detail page templates
- `cards/` — card component templates

## Configuration

- `config/site.json` — site-wide settings (name, URL, etc.)

## Dependencies

- `jinja2` — templating
- `markdown` — Markdown to HTML conversion with codehilite, fenced_code, tables, toc extensions
- `python-frontmatter` — YAML frontmatter parsing
- `pygments` — syntax highlighting CSS generation

## Deployment

GitHub Actions CI builds and deploys to GitHub Pages on push to main.

## Constraints

- No tests currently exist
- Build must be run from repo root: `uv run python build/build.py`
- Output directory is wiped clean before each build
