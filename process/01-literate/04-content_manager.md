---
version: "1.3"
generated: "2026-10-28"
---

# content_manager — from Markdown files to structured content

## What this module does

The whole site is generated from Markdown files with YAML frontmatter under
`content/`, plus one YAML schedule, `content/calendar.yaml`. `content_manager`
is the layer that **reads those files and hands the rest of the build clean
Python dicts**: parsed dates, rendered HTML,
meetings from the calendar, and derived views like "upcoming meetings" or "calendar
events".

It deliberately knows nothing about HTML page layout. That belongs to
`page_builder` and the Jinja templates.

```mermaid
flowchart LR
    MD["content/**/*.md"] --> CM["ContentManager"]
    Y["content/calendar.yaml<br/>(via calendar_source)"] --> CM
    CM --> I["item dicts<br/>(news, projects, members)"]
    CM --> M["meeting dicts"]
    CM --> H["hero content"]
    CM --> U["upcoming meetings"]
    CM --> E["calendar events"]
    I --> PB["page_builder / build.py"]
    H --> PB
    U --> TXT["upcoming-talks.txt"]
    E --> ICS["meetings.ics"]
```

## Validate at the boundary: dates

A small module-level function encodes the project's **"report, don't guess"**
rule for dates, and everything else leans on it.

**Dates** must be ISO `YYYY-MM-DD`:

```python
if not date_str:
    return None
try:
    return datetime.fromisoformat(str(date_str))
except ValueError as e:
    raise ValueError(
        f"Invalid date {date_str!r}: expected ISO format YYYY-MM-DD"
    ) from e
```

- Empty means "no date", which is a legitimate state.
- Anything else non-ISO is a **content bug** and fails the build. There is no
  attempt to parse "Oct 15" or "15/10/2026".

Meeting kinds used to be validated here too. That check now lives in
`calendar_source`, the one way meetings come in, so this module reads
`metadata["kind"]` directly.

`format_long_date` is the display counterpart: it renders "Thursday, October 5,
2026" without zero-padding by building the string from `%A`, `%B`, `.day`, and
`%Y`, avoiding the non-portable `%-d`.

## Loading one file

`process_markdown_file` is the unit of work. It returns a uniform dict whatever
the content type:

- `content`: Markdown rendered to HTML (with code highlighting, tables, and a
  table of contents).
- `toc_tokens`: the headings, for detail-page navigation.
- `reading_time`: words ÷ 200, minimum 1 minute.
- `metadata`: the raw frontmatter, which stays the **source of truth**.

One subtle step normalizes dates. YAML parses `date: 2026-10-15` into a Python
`date` object, while quoted dates stay strings. The loader converts both to one
ISO string and validates it *here*, naming the file on failure, so a bad date
anywhere fails with a useful message.

## ContentType: one loader, many kinds of content

Rather than one loader per content kind, a small **configuration object**
describes each kind (directory, sort key, templates), and `get_all_content`
does the rest:

- Files starting with `_` are skipped as scaffolding.
- Members get hashtag validation (a warning, not a failure).
- Items are sorted by `order`, by date (parsed, so it's chronological not
  lexical), or by any other field.

This is the *table-driven* pattern: behavior varies by data, not by subclass.

## The meeting pipeline

Meetings are the richest content, and several views are derived from them.
They no longer go through `get_all_content` at all: they share one loader,
backed by `calendar_source`:

```mermaid
flowchart TD
    L["load_meetings()<br/>calendar.yaml, ascending"] --> F["get_future_meetings(today)<br/>date >= today"]
    L --> E["get_calendar_events(duration)<br/>main only, past + future"]
    F --> H["format_future_meetings_section<br/>hero: next 2 meetings"]
    F --> T["get_upcoming_meetings(today)<br/>both kinds, for the text list"]
    P["meeting_page_path()<br/>announcement or calendar anchor"] -.-> T
    P -.-> E
```

### load_meetings

A one-line delegation to `calendar_source.load_calendar` on
`content/calendar.yaml`. It returns `{id, date_obj, metadata}` sorted
ascending, with defaults already merged and every entry already validated.
Keeping the method here means no consumer had to change when the source
moved from 35 Markdown files to one YAML file.

### get_future_meetings

A filter over `load_meetings`. It takes an optional `today` so tests can
**freeze time**; production passes nothing and gets the real date.

### get_upcoming_meetings

The data behind `upcoming-talks.txt`. It used to keep only confirmed talks;
now it keeps **every** future meeting, both kinds, and reshapes each one into
the flat fields the text template wants:

```python
"kind": metadata["kind"],
"topic": metadata.get("topic"),
"speaker": metadata.get("speaker"),
```

- `speaker`/`topic` are **`None` until a talk is confirmed**. The template
  branches on them (confirmed talk vs. "TBD") and on `kind` (hands-on), so the
  filtering decision moved from Python into presentation.
- The filename stayed `upcoming-talks.txt` so already-shared URLs keep
  working; only its content broadened.

### get_calendar_events

The data behind `meetings.ics`. Unlike the text list, it keeps **past** meetings too,
because subscribers' calendars would otherwise lose history. Each event gets a
timezone-aware start:

```python
start = datetime.combine(meeting["date_obj"], start_time, tzinfo=BOSTON)
```

`BOSTON` is `ZoneInfo("America/New_York")`, so daylight saving is handled by the
IANA tz database, not by hand-coded offsets. The end is start plus a configured
duration, because content has no end times.

### meeting_page_path

One rule shared by both views: link to the meeting's **announcement** post if it
resolves, else to the meeting's **anchor on the calendar page**:

```python
return f"news/{html}" if exists else f"meetings.html#{meeting['id']}"
```

Per-meeting detail pages are gone, so the anchor is the meeting's only
address. Having the rule in one place keeps the text list and the `.ics`
feed pointing at the same URL.

## Hero content

`build_hero_content` loads `content/heroes/<page>.md`. For the home page, the
Markdown contains an `<hr>`: everything above is static, and everything below
is **replaced** by a rendered "next two meetings" snippet. It's a simple
*template slot* convention that keeps the hero editable as plain Markdown.

## Observations and possible improvements

1. **The file is still past the ~300-line guideline** (about 345 lines). The
   meeting views (`get_future_meetings` through `get_calendar_events`) could
   move next to `calendar_source` as one meetings module.
2. **`get_all_content` has a pre-existing `noqa` for branch complexity.** The
   one remaining per-type special case (member hashtags) could move onto
   `ContentType` as an optional validator callable.
3. **Config is read in the constructor** for hashtags only, while `build.py`
   separately loads the same `site.json`. Passing the loaded config in would
   remove the duplicate read.
4. **`get_future_meetings` and `get_upcoming_meetings` are near-synonyms.**
   The first returns raw meeting dicts, the second the flattened text-list
   shape. A name that says what the second is for (say, `text_list_entries`)
   would stop a reader guessing which one to call.
