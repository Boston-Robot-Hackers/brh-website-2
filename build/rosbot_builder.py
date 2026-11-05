#!/usr/bin/env python3
# rosbot_builder — Builds the Build-A-ROSBot section: overview, sessions, resources
# Author: Pito Salas and Claude Code
# Version: 2
# Created: 2026-11-05
# Updated: 2026-11-05
# Open Source Under MIT license
"""Build the Build-A-ROSBot program section from content/rosbot/.

Sources and outputs:

- content/rosbot/overview.md -> rosbot.html, the hand-written overview
  followed by generated Sessions and Resources lists.
- content/rosbot/sessions/<slug>.md -> rosbot-sessions/<slug>.html,
  ordered by the required integer `session`, with previous/next links.
- content/rosbot/resources/<slug>.md -> rosbot-resources/<slug>.html,
  ordered by optional integer `order`, then `title`; unordered ones last.

Output folders are one level deep so detail templates' "../" prefix works.
Files whose name starts with "_" are templates and are skipped.
"""

from pathlib import Path

from content_manager import ContentManager
from page_builder import PageBuilder

SESSIONS_OUT = "rosbot-sessions"
RESOURCES_OUT = "rosbot-resources"


def require_int(page: dict, field: str, source: Path):
    """Raise unless metadata[field] is an int (bool is rejected too)."""
    value = page["metadata"].get(field)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{source}: '{field}' must be an integer, got {value!r}")


def resource_sort_key(page: dict) -> tuple:
    order = page["metadata"].get("order")
    return (order is None, order or 0, page["title"].lower())


class RosbotSection:
    """Loads and renders every page of the Build-A-ROSBot section."""

    def __init__(self, content_manager: ContentManager, page_builder: PageBuilder):
        self.content_manager = content_manager
        self.page_builder = page_builder
        self.section_dir = content_manager.content_dir / "rosbot"

    def load_page(self, md_file: Path) -> dict:
        page = self.content_manager.process_markdown_file(md_file)
        if not page["metadata"].get("title"):
            raise ValueError(f"{md_file}: missing required 'title'")
        return page

    def load_folder(self, folder_name: str) -> list[tuple[Path, dict]]:
        folder = self.section_dir / folder_name
        return [
            (md_file, self.load_page(md_file))
            for md_file in sorted(folder.glob("*.md"))
            if not md_file.stem.startswith("_")
        ]

    def load_sessions(self) -> list[dict]:
        """Sessions sorted by `session`; a missing or repeated number raises."""
        by_number: dict[int, tuple[Path, dict]] = {}
        for source, page in self.load_folder("sessions"):
            require_int(page, "session", source)
            number = page["metadata"]["session"]
            if number in by_number:
                raise ValueError(
                    f"{source}: session {number} is already used by "
                    f"{by_number[number][0]}"
                )
            by_number[number] = (source, page)
        return [by_number[number][1] for number in sorted(by_number)]

    def load_resources(self) -> list[dict]:
        resources = []
        for source, page in self.load_folder("resources"):
            if page["metadata"].get("order") is not None:
                require_int(page, "order", source)
            resources.append(page)
        return sorted(resources, key=resource_sort_key)

    def write_detail(self, template: str, out_dir: str, page: dict, **context):
        (self.page_builder.dist_dir / out_dir).mkdir(exist_ok=True)
        self.page_builder.build_page(
            template,
            f"{out_dir}/{page['id']}.html",
            page=page,
            **self.page_builder.resolve_banner(page["metadata"], path_prefix="../"),
            **context,
        )

    def build(self):
        """Render the overview, every session and every resource page."""
        sessions = self.load_sessions()
        resources = self.load_resources()
        for i, session in enumerate(sessions):
            self.write_detail(
                "details/rosbot-session-detail.html",
                SESSIONS_OUT,
                session,
                previous=sessions[i - 1] if i > 0 else None,
                next_session=sessions[i + 1] if i + 1 < len(sessions) else None,
            )
        for resource in resources:
            self.write_detail(
                "details/rosbot-resource-detail.html", RESOURCES_OUT, resource
            )
        overview = self.load_page(self.section_dir / "overview.md")
        self.page_builder.build_page(
            "pages/rosbot.html",
            "rosbot.html",
            overview=overview,
            sessions=sessions,
            resources=resources,
            **self.page_builder.resolve_banner(overview["metadata"]),
        )
        print(
            f"Built rosbot.html, {len(sessions)} sessions, {len(resources)} resources"
        )
