#!/usr/bin/env python3
# meeting_fixtures — Test helper that adds meetings to a temp calendar.yaml
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-10-28
# Updated: 2026-10-28
# Open Source Under MIT license
import yaml


def write_meeting(content_dir, meeting_id, **fields):
    """Append a meeting with id `meeting_id` to `content_dir`/calendar.yaml."""
    path = content_dir / "calendar.yaml"
    schedule = yaml.safe_load(path.read_text()) if path.exists() else {}
    schedule.setdefault("meetings", []).append({"id": meeting_id, **fields})
    path.write_text(yaml.safe_dump(schedule))
