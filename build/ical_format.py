#!/usr/bin/env python3
# ical_format — RFC 5545 text mechanics for the meetings iCalendar feed
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-09-21
# Updated: 2026-09-21
# Open Source Under MIT license
"""Time parsing, text-value escaping, and CRLF line folding."""

import re
from datetime import time

MEETING_TIME_PATTERN = re.compile(r"(1[0-2]|[1-9]):([0-5][0-9])(am|pm)")
MAX_LINE_OCTETS = 75
CRLF = "\r\n"


def parse_meeting_time(value: str) -> time:
    """Parse a meeting time like '7:00pm'; any other shape is a content bug."""
    match = MEETING_TIME_PATTERN.fullmatch(str(value or ""))
    if not match:
        raise ValueError(f"meeting time must look like '7:00pm', got {value!r}")
    hour, minute, meridiem = int(match[1]), int(match[2]), match[3]
    return time(hour % 12 + (12 if meridiem == "pm" else 0), minute)


def ics_text(value: str) -> str:
    """Escape a value for an iCalendar TEXT property (RFC 5545 §3.3.11)."""
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold_line(line: str) -> list[str]:
    """Split one content line into <=75-octet pieces on character boundaries.

    Continuation pieces start with a space, which counts toward their 75
    octets. Splitting by character (not byte) keeps multi-byte UTF-8
    characters such as em dashes intact.
    """
    pieces = []
    current, size = "", 0
    for char in line:
        width = len(char.encode("utf-8"))
        if size + width > MAX_LINE_OCTETS:
            pieces.append(current)
            current, size = " ", 1
        current += char
        size += width
    pieces.append(current)
    return pieces


def fold_ics(text: str) -> str:
    """Turn rendered template text into CRLF-terminated, folded iCalendar text.

    Blank lines are template layout only: every TEXT value goes through
    `ics_text`, which escapes newlines, so real content never yields one.
    """
    lines = [line for line in text.splitlines() if line.strip()]
    return "".join(piece + CRLF for line in lines for piece in fold_line(line.rstrip()))
