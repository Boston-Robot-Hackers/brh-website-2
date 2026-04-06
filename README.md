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
├── images/                 # Static images
├── scripts/                # JavaScript
├── config/
│   └── site.json           # Site-wide text strings and configuration
├── tests/                  # Pytest test suite
├── pyproject.toml          # Root dependencies (Python 3.12+)
└── output/                 # Generated website (not committed)
```

## Content Files

All content is Markdown with YAML frontmatter. Dated files use the `YYYY-MM-DD-slug.md` naming convention.

| Directory | Key frontmatter fields |
|---|---|
| `content/news/` | `title`, `date`, `image`, `excerpt`, `highlight` |
| `content/members/` | `name`, `role`, `image`, `featured`, `skills`, `github`, `linkedin`, `projects`, `opentowork` |
| `content/projects/` | `title`, `image`, `excerpt` |
| `content/meetings/` | `title`, `date` (MM/DD/YYYY), `time`, `location`, `announcement` |
| `content/heroes/` | Named by page (e.g. `index.md`, `about.md`) |

## Deployment

GitHub Actions automatically builds and deploys to GitHub Pages on push to `main`. The `output/` directory is not committed.

## License

MIT — see [LICENSE](LICENSE)
