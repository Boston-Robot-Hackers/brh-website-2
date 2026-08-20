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
├── build/                  # Build system
│   ├── build.py            # Main build script (WebsiteBuilder)
│   ├── content_manager.py  # Loads/processes Markdown content
│   ├── page_builder.py     # Renders Jinja2 templates to HTML
│   ├── asset_manager.py    # Copies static assets, generates CSS
│   └── pyproject.toml      # Build-specific dependencies (Python 3.13)
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

The build system lives in `build/` and is composed of three modules orchestrated by `WebsiteBuilder` in `build/build.py`:

- **`content_manager.py`** — Loads and processes Markdown files using `python-frontmatter` and the `markdown` library (with codehilite, fenced_code, tables, toc extensions). Handles date parsing from frontmatter or filename prefix. Builds hero content from `content/heroes/`. Dynamically injects upcoming meeting dates into the index hero.
- **`page_builder.py`** — Renders Jinja2 templates and writes HTML files to `output/`. Handles both listing pages and per-item detail pages (news, projects, members, meetings).
- **`asset_manager.py`** — Copies static assets (CSS, images, scripts) to `output/` and generates Pygments syntax highlighting CSS.

The `build/` directory has its own `pyproject.toml` and `.venv` (Python 3.13), separate from the root-level `pyproject.toml` (Python 3.12+). Tests use the root `pyproject.toml` with `pythonpath = ["build"]`.

## Content Files

All content is Markdown with YAML frontmatter. Dated files use the `YYYY-MM-DD-slug.md` naming convention (the date is extracted from the filename if not given in frontmatter).

All `date:` frontmatter fields use ISO `YYYY-MM-DD` — the single canonical format. `parse_date` accepts nothing else and the build fails loudly (naming the file) on any other value.

| Directory | Key frontmatter fields |
|---|---|
| `content/news/` | `title`, `date`, `image`, `excerpt`, `highlight` (bool — only highlighted posts appear on homepage) |
| `content/members/` | `name`, `role`, `image`, `featured`, `skills`, `github`, `linkedin`, `projects`, `opentowork` |
| `content/projects/` | `title`, `image`, `excerpt` |
| `content/meetings/` | `title`, `date` (ISO `YYYY-MM-DD`), `kind` (`main` or `handson`), `time`, `location`, `announcement` (filename of linked news post) |
| `content/heroes/` | Named by page (e.g. `index.md`, `about.md`, `members.md`). `index.md` uses an `<hr>` separator — content above is static, content below is replaced dynamically with upcoming meeting info |

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

GitHub Actions automatically builds and deploys to GitHub Pages on push to `main`. The `output/` directory is not committed.

## License

MIT — see [LICENSE](LICENSE)
