# Boston Robot Hackers Website

Static website generator for the Boston Robot Hackers community built with Python, Jinja2 templates, and UV package management.

## Prerequisites

- Python 3.12 or higher
- UV package manager

**Install UV:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
git clone https://github.com/Boston-Robot-Hackers/brh-website-2.git
cd brh-website-2
uv sync
```

## Usage

### Build the Website

```bash
uv run python build/build.py
```

Output is written to `output/`.

### Run Tests

```bash
uv run pytest
uv run pytest --cov=build
```

## Project Structure

```
├── build/                  # Build system (flat modules, no __init__.py -
│   │                       # importable via pytest's pythonpath, see below)
│   ├── build.py            # Main build script (WebsiteBuilder)
│   ├── content_manager.py  # Loads/processes Markdown content
│   ├── page_builder.py     # Renders Jinja2 templates to HTML
│   ├── asset_manager.py    # Copies static assets, generates CSS
│   └── news_links.py       # Shared announcement/report link resolution
├── content/                # Markdown source content
│   ├── heroes/             # Hero section content per page
│   ├── news/               # News/announcements
│   ├── meetings/           # Meeting entries
│   ├── projects/           # Project descriptions
│   ├── members/            # Member profiles
│   ├── about.md            # About page content
│   └── learn.md            # Learn page content
├── templates/              # Jinja2 templates
│   ├── layouts/            # Base layouts (base, home, page, detail)
│   ├── pages/              # Per-page templates
│   ├── components/         # Reusable partials
│   ├── cards/              # Card components for listings
│   └── details/            # Detail page templates
├── css/                    # Stylesheets
├── images/                 # Static images, one subdirectory per content type
│   ├── news/               # News images
│   ├── meetings/           # Meeting images
│   ├── members/            # Member photos
│   └── projects/           # Project images
├── scripts/                # JavaScript
├── config/
│   └── site.json           # Site-wide text strings and configuration
├── tests/                  # Pytest test suite
├── pyproject.toml          # Root dependencies (Python 3.12+)
└── output/                 # Generated website (not committed)
```

## Architecture

The build system lives in `build/` and is composed of four modules orchestrated by `WebsiteBuilder` in `build/build.py`:

- **`content_manager.py`** — Loads and processes Markdown files using `python-frontmatter` and the `markdown` library (with codehilite, fenced_code, tables, toc extensions). Handles date parsing from frontmatter. Builds hero content from `content/heroes/`. Dynamically injects upcoming meeting dates into the index hero.
- **`page_builder.py`** — Renders Jinja2 templates and writes HTML files to `output/`. Handles both listing pages and per-item detail pages (news, projects, members, meetings).
- **`asset_manager.py`** — Copies static assets (CSS, images, scripts) to `output/` and generates Pygments syntax highlighting CSS.
- **`news_links.py`** — Resolves a meeting's `announcement`/`report` references (or a news item's own `slug`) to the news item's actual output filename, shared by both `content_manager.py` and `page_builder.py` via the `NewsResolver` class.

There's a single `pyproject.toml` at the repo root (Python 3.12+, one `.venv`). `build/` has no `pyproject.toml` of its own and its modules aren't a real Python package (no `__init__.py`) — they're imported as flat top-level modules. This works via two mechanisms: running `build/build.py` directly puts its own directory on `sys.path`, and `pytest.ini_options.pythonpath = ["build"]` in the root `pyproject.toml` does the same for tests.

## Content Files

All content is Markdown with YAML frontmatter. Dated files use the `YYYY-MM-DD-slug.md` naming convention (the date is extracted from the filename if not given in frontmatter).

All `date:` frontmatter fields use ISO `YYYY-MM-DD` — the single canonical format. `parse_date` accepts nothing else and the build fails loudly (naming the file) on any other value.

| Directory | Key frontmatter fields |
|---|---|
| `content/news/` | `title`, `date`, `image`, `excerpt`, `highlight` (bool — only highlighted posts appear on homepage), `published_date` (when the post was actually written; used to sort What's New and the homepage — see note below), `slides_pdf` (path under `content/meeting-reports/`, shown as a download button), `type` (always `news`) |
| `content/members/` | `name`, `image`, `hashtags` (validated against `config/site.json`'s `valid_hashtags`), `featured`, `github`, `linkedin`, `website`, `projects` (slugs linking to `content/projects/`), `opentowork` |
| `content/projects/` | `title`, `image`, `excerpt`, `text`, `status`, `date`, `lead`, `members`, `github` |
| `content/meetings/` | `title`, `date` (ISO `YYYY-MM-DD`), `kind` (`main` or `handson`, required), `time`, `location`, `text`, `announcement` (filename of the linked news post), `report` (filename of the linked follow-up news post) |
| `content/heroes/` | Named by page (e.g. `index.md`, `about.md`, `members.md`). `index.md` uses an `<hr>` separator — content above is static, content below is replaced dynamically with upcoming meeting info |

Any content item (news, project, member, or meeting) can also set `banner_image`, `banner_title`, `banner_subtitle` to override that page's banner; unset fields fall back to `config/site.json`'s `default_banner_image`/`title`/`subtitle`.

**Note on dates**: a news item's `date` is its associated *meeting* date (used for detail-page display and for the meeting's own `announcement`/`report` links), while `published_date` is when the post itself was written — that's the field What's New and the homepage sort by, so a meeting report written the day after its meeting sorts by that day, not by the (earlier) meeting date.

## Templates

Jinja2 templates in `templates/`:
- `layouts/` — `base.html`, `home.html`, `page.html`, `detail.html`
- `pages/` — One template per page (`index.html`, `about.html`, `members.html`, `projects.html`, `whatsnew.html`, `meetings.html`, `learn.html`)
- `components/` — Reusable partials (`head.html`, `navigation.html`, `hero.html`, `home-lead.html`, `footer.html`, `banner.html`, `icons.html`, `upcoming-meetings-calendar.html`, `upcoming-meetings-hero.html`)
- `cards/` — Card components for listings
- `details/` — Detail page templates for individual items

## Configuration

`config/site.json` — Site-wide text strings (title, section titles, button labels, footer text). Available in all templates as the `site_config` context variable.

## Deployment

GitHub Actions automatically builds and deploys to GitHub Pages on push to `main`. The `output/` directory is not committed.

## License

MIT — see [LICENSE](LICENSE)
