#!/usr/bin/env python3
"""
content_manager.py — Content management module for the website builder.
Handles loading and processing of markdown content.

Author: Pito Salas and Claude Code
Open Source Under MIT license
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import frontmatter
import markdown
from news_links import build_news_index, resolve_news_html

WORDS_PER_MINUTE = 200
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def compute_reading_time(html_content: str) -> int:
    """Estimate reading time in minutes from rendered HTML body content."""
    word_count = len(HTML_TAG_PATTERN.sub(" ", html_content).split())
    return max(1, round(word_count / WORDS_PER_MINUTE))


def parse_date(date_str):
    """Parse a canonical ISO date (YYYY-MM-DD).

    Empty/None returns None. Any other value raises ValueError — all content
    uses one date format, so a non-ISO value is a content bug to fix, not a
    case to accommodate.
    """
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(str(date_str))
    except ValueError as e:
        raise ValueError(
            f"Invalid date {date_str!r}: expected ISO format YYYY-MM-DD"
        ) from e


def classify_meeting(metadata: dict[str, Any]) -> str:
    """Return the meeting kind ('main' or 'handson').

    Requires an explicit `kind` field; a missing or unknown value is a content
    bug, not something to guess from the title.
    """
    kind = metadata.get("kind")
    if kind in ("main", "handson"):
        return kind
    raise ValueError(f"meeting 'kind' must be 'main' or 'handson', got {kind!r}")


class ContentType:
    """Configuration for different content types."""

    def __init__(
        self,
        name: str,
        directory: str,
        sort_key: str = "date",
        reverse: bool = True,
        detail_template: str | None = None,
        page_template: str | None = None,
        output_filename: str | None = None,
    ):
        self.name = name
        self.directory = directory
        self.sort_key = sort_key
        self.reverse = reverse
        self.detail_template = detail_template or f"details/{name}-detail.html"
        self.page_template = page_template or f"pages/{name}.html"
        self.output_filename = output_filename or f"{name}.html"


class ContentManager:
    """Manages content loading and processing."""

    def __init__(self, content_dir: Path, jinja_env=None):
        self.content_dir = content_dir
        self.jinja_env = jinja_env
        self._news_map = None
        config_file = content_dir.parent / "config" / "site.json"
        if config_file.exists():
            site_config = json.loads(config_file.read_text())
            self.valid_hashtags = set(site_config.get("valid_hashtags", []))
        else:
            self.valid_hashtags = set()

    def validate_member_hashtags(self, member_id: str, hashtags: list):
        """Warn about any hashtags not in the valid list."""
        if not self.valid_hashtags:
            return
        for tag in hashtags:
            if tag not in self.valid_hashtags:
                print(f"Warning: member '{member_id}' has unknown hashtag '{tag}'")

    def setup_markdown_processor(self):
        """Set up markdown processor with syntax highlighting."""
        return markdown.Markdown(
            extensions=["codehilite", "fenced_code", "tables", "toc"],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "use_pygments": True,
                    "noclasses": False,
                }
            },
        )

    def process_markdown_file(
        self, file_path: Path, md_processor=None
    ) -> dict[str, Any]:
        """Process a single markdown file and return structured data."""
        if md_processor is None:
            md_processor = self.setup_markdown_processor()

        post = frontmatter.load(file_path)
        html_content = md_processor.convert(post.content)
        metadata = post.metadata

        # Normalize the date to an ISO string and validate it at the boundary,
        # so a bad date fails the build here, naming the file.
        raw_date = metadata.get("date")
        metadata["date"] = (
            raw_date.isoformat() if hasattr(raw_date, "isoformat") else raw_date
        )
        try:
            parse_date(metadata["date"])
        except ValueError as e:
            raise ValueError(f"{file_path}: {e}") from e

        return {
            "id": metadata.get("slug") or file_path.stem,
            "title": metadata.get("title", metadata.get("name", "Untitled")),
            "date": metadata.get("date"),
            "image": metadata.get("image", ""),
            "text": metadata.get("text", metadata.get("emoji")),
            "excerpt": metadata.get("excerpt", ""),
            "content": html_content,
            "toc_tokens": [
                {"id": token["id"], "name": token["name"]}
                for token in md_processor.toc_tokens
            ],
            "reading_time": compute_reading_time(html_content),
            "metadata": metadata,
        }

    def get_all_content(self, content_type: ContentType) -> list[dict[str, Any]]:
        """Generic method to get all content of a given type."""
        content_dir = self.content_dir / content_type.directory
        if not content_dir.exists():
            print(f"Warning: {content_dir} directory not found")
            return []

        md_processor = self.setup_markdown_processor()
        items = []

        for md_file in content_dir.glob("*.md"):
            if md_file.stem.startswith("_"):
                continue  # leading-underscore files are scaffolding, never published
            item_data = self.process_markdown_file(md_file, md_processor)
            if item_data:
                if content_type.directory == "members":
                    hashtags = item_data["metadata"].get("hashtags", [])
                    self.validate_member_hashtags(item_data["id"], hashtags)
                if content_type.directory == "meetings":
                    try:
                        classify_meeting(item_data["metadata"])
                    except ValueError as e:
                        raise ValueError(f"meetings/{item_data['id']}.md: {e}") from e
                items.append(item_data)

        # Sort by specified key
        if content_type.sort_key == "order":
            # Default to 0 if not present, so items without order come first
            items.sort(
                key=lambda x: x["metadata"].get("order", 0),
                reverse=content_type.reverse,
            )
        elif content_type.sort_key == "date":
            # Dates were validated at load, so sort chronologically directly.
            items.sort(
                key=lambda x: parse_date(x["date"]) or datetime.min,
                reverse=content_type.reverse,
            )
        elif content_type.sort_key == "published_date":
            # Sort by published_date from metadata (post creation date)
            items.sort(
                key=lambda x: parse_date(x["metadata"].get("published_date")) or datetime.min,
                reverse=content_type.reverse,
            )
        else:
            items.sort(
                key=lambda x: x[content_type.sort_key] or "",
                reverse=content_type.reverse,
            )
        return items

    def resolve_news_html(self, ref: str):
        """Resolve an announcement/report reference to (html_filename, exists)."""
        if self._news_map is None:
            self._news_map = build_news_index(self.content_dir / "news")
        return resolve_news_html(self._news_map, ref)

    def generate_index_hero(self, static_content: str) -> str:
        """Generate index hero by adding future meeting info to static content."""
        if "<hr/>" not in static_content and "<hr>" not in static_content:
            return static_content

        split_on = "<hr/>" if "<hr/>" in static_content else "<hr>"
        parts = static_content.split(split_on, 1)
        static_part = parts[0] + split_on

        # Get all future meetings
        future_meetings = self.get_future_meetings()
        generated_part = self.format_future_meetings_section(future_meetings)

        return static_part + "\n" + generated_part

    def get_future_meetings(self) -> list[dict[str, Any]]:
        """Get all meetings with dates in the future, sorted by date ascending."""
        meetings_dir = self.content_dir / "meetings"
        if not meetings_dir.exists():
            return []

        today = datetime.now().date()
        future_meetings = []

        for md_file in meetings_dir.glob("*.md"):
            metadata = frontmatter.load(md_file).metadata
            date_str = metadata.get("date")
            if not date_str:
                continue

            try:
                meeting_date = parse_date(date_str).date()
            except ValueError as e:
                raise ValueError(f"{md_file}: {e}") from e

            if meeting_date >= today:
                future_meetings.append(
                    {
                        "metadata": metadata,
                        "date_obj": meeting_date,
                        "title": metadata.get("title", ""),
                    }
                )

        # Sort by date ascending (nearest first)
        future_meetings.sort(key=lambda x: x["date_obj"])
        return future_meetings

    def format_future_meetings_section(self, meetings: list[dict[str, Any]]) -> str:
        """Render the 2 nearest future meetings via the hero template."""
        # Only show the 2 nearest meetings
        context_meetings = []
        for meeting in meetings[:2]:
            metadata = meeting["metadata"]

            is_handson = classify_meeting(metadata) == "handson"
            label = "Next Hands-On Meeting" if is_handson else "Next Main Meeting"

            parsed = parse_date(metadata.get("date"))
            date = parsed.strftime("%B %d, %Y") if parsed else ""
            time = metadata.get("time", "")
            datetime_str = f"{date} at {time}" if date and time else date or time or ""

            html, exists = self.resolve_news_html(metadata.get("announcement", ""))

            context_meetings.append(
                {
                    "label": label,
                    "datetime_str": datetime_str,
                    "url": f"news/{html}" if exists else "",
                }
            )

        template = self.jinja_env.get_template("components/upcoming-meetings-hero.html")
        return template.render(meetings=context_meetings)

    def build_hero_content(self, page_name: str = "index") -> dict[str, Any]:
        """Build hero content from page-specific markdown file."""
        hero_file = self.content_dir / "heroes" / f"{page_name}.md"
        if not hero_file.exists():
            raise FileNotFoundError(f"Missing hero file: {hero_file}")

        md_processor = self.setup_markdown_processor()
        hero_data = self.process_markdown_file(hero_file, md_processor)
        hero_content = hero_data["content"]

        if page_name == "index":
            hero_content = self.generate_index_hero(hero_content)

        return {
            "hero_title": hero_data["title"],
            "hero_subtitle": hero_data["metadata"].get("subtitle", ""),
            "hero_content": hero_content,
            "banner_image": hero_data["metadata"].get("banner_image"),
            "banner_title": hero_data["metadata"].get("banner_title"),
            "banner_subtitle": hero_data["metadata"].get("banner_subtitle"),
        }

    def process_single_content_file(self, filename: str) -> str:
        """Process a single content file and return HTML content."""
        content_file = self.content_dir / filename
        if not content_file.exists():
            raise FileNotFoundError(f"Missing content file: {content_file}")

        md_processor = self.setup_markdown_processor()
        return self.process_markdown_file(content_file, md_processor)["content"]
