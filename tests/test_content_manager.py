#!/usr/bin/env python3
# test_content_manager — Tests for ContentManager loading, sorting, meetings, and talks
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-09-21
# Updated: 2026-09-21
# Open Source Under MIT license
from datetime import date

import pytest
from content_manager import ContentManager, ContentType, format_long_date
from jinja2 import DictLoader, Environment

HERO_MEETINGS_TEMPLATE = (
    "{% if not meetings %}<p><em>No upcoming meetings scheduled</em></p>"
    "{% else %}<p>{% for m in meetings %}<strong>{{ m.label }}:</strong> "
    '{% if m.url %}<a href="{{ m.url }}">{{ m.datetime_str }}</a>'
    "{% else %}{{ m.datetime_str }}{% endif %}"
    "{% if not loop.last %} | {% endif %}{% endfor %}</p>{% endif %}"
)


@pytest.fixture
def jinja_env():
    return Environment(
        loader=DictLoader(
            {
                "components/upcoming-meetings-hero.html": HERO_MEETINGS_TEMPLATE,
            }
        )
    )


class TestProcessMarkdownFile:
    def test_extracts_title_and_excerpt(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: My Post\nexcerpt: Brief summary.\n---\nBody text.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["title"] == "My Post"
        assert result["excerpt"] == "Brief summary."

    def test_converts_body_to_html(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Test\n---\nHello **world**.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert "<p>" in result["content"]
        assert "<strong>world</strong>" in result["content"]

    def test_id_is_filename_stem(self, tmp_path):
        f = tmp_path / "my-article.md"
        f.write_text("---\ntitle: Article\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["id"] == "my-article"

    def test_title_falls_back_to_name_field(self, tmp_path):
        f = tmp_path / "member.md"
        f.write_text("---\nname: Alice\n---\nBio.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["title"] == "Alice"

    def test_toc_tokens_lists_top_level_headings(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text(
            "---\ntitle: Post\n---\n"
            "### Meeting Announcement\nBody.\n"
            "### Agenda\nBody.\n"
            "### Featured Talk\nBody.\n"
            "#### Speaker: Someone\nBody.\n"
        )
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["toc_tokens"] == [
            {"id": "meeting-announcement", "name": "Meeting Announcement"},
            {"id": "agenda", "name": "Agenda"},
            {"id": "featured-talk", "name": "Featured Talk"},
        ]

    def test_toc_tokens_empty_when_no_headings(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Post\n---\nJust a paragraph, no headings.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["toc_tokens"] == []

    def test_reading_time_computed_from_word_count(self, tmp_path):
        f = tmp_path / "post.md"
        body = " ".join(["word"] * 400)
        f.write_text(f"---\ntitle: Post\n---\n{body}\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["reading_time"] == 2

    def test_reading_time_minimum_is_one(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Post\n---\nOne short sentence.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["reading_time"] == 1

    def test_toc_tokens_reset_between_files(self, tmp_path):
        f1 = tmp_path / "with-heading.md"
        f1.write_text("---\ntitle: One\n---\n### A Heading\nBody.\n")
        f2 = tmp_path / "without-heading.md"
        f2.write_text("---\ntitle: Two\n---\nNo heading here.\n")
        cm = ContentManager(tmp_path)
        md_processor = cm.setup_markdown_processor()
        first = cm.process_markdown_file(f1, md_processor)
        second = cm.process_markdown_file(f2, md_processor)
        assert first["toc_tokens"] != []
        assert second["toc_tokens"] == []


class TestParseDate:
    def test_parses_iso(self):
        from content_manager import parse_date

        assert parse_date("2026-06-11").strftime("%Y-%m-%d") == "2026-06-11"

    def test_empty_is_none(self):
        from content_manager import parse_date

        assert parse_date("") is None
        assert parse_date(None) is None

    def test_non_iso_raises(self):
        from content_manager import parse_date

        with pytest.raises(ValueError):
            parse_date("06/11/2026")
        with pytest.raises(ValueError):
            parse_date("not-a-date")


class TestDateHandling:
    def test_frontmatter_date_object_serialized_to_iso(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Post\ndate: 2024-03-15\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["date"] is not None
        assert "2024-03-15" in str(result["date"])

    def test_frontmatter_string_date_preserved(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text('---\ntitle: Post\ndate: "2024-03-15"\n---\nContent.\n')
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["date"] == "2024-03-15"

    def test_non_date_filename_yields_none(self, tmp_path):
        f = tmp_path / "my-post.md"
        f.write_text("---\ntitle: Post\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f)
        assert result["date"] is None


class TestGetAllContent:
    def test_news_sorted_date_descending(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        ct = ContentType(
            "news",
            "news",
            "date",
            True,
            "details/news-detail.html",
            "pages/news.html",
            "news.html",
        )
        items = cm.get_all_content(ct)
        assert len(items) == 2
        assert items[0]["date"] >= items[1]["date"]

    def test_members_sorted_title_ascending(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        ct = ContentType(
            "members",
            "members",
            "title",
            False,
            "details/member-detail.html",
            "pages/members.html",
            "members.html",
        )
        items = cm.get_all_content(ct)
        assert len(items) == 2
        assert items[0]["title"] == "Alice"
        assert items[1]["title"] == "Bob"

    def test_missing_directory_returns_empty(self, tmp_path):
        cm = ContentManager(tmp_path)
        ct = ContentType(
            "news",
            "news",
            "date",
            True,
            "details/news-detail.html",
            "pages/news.html",
            "news.html",
        )
        assert cm.get_all_content(ct) == []

    def test_leading_underscore_file_excluded(self, tmp_content_dir):
        (tmp_content_dir / "members" / "_template.md").write_text(
            "---\ntitle: Template\n---\nPlaceholder.\n"
        )
        cm = ContentManager(tmp_content_dir)
        ct = ContentType(
            "members",
            "members",
            "title",
            False,
            "details/member-detail.html",
            "pages/members.html",
            "members.html",
        )
        items = cm.get_all_content(ct)
        assert len(items) == 2
        assert "Template" not in [item["title"] for item in items]


class TestHeroGeneration:
    def test_get_future_meetings_excludes_past(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        meetings = cm.get_future_meetings()
        titles = [m["title"] for m in meetings]
        assert "Main Meeting" in titles
        assert "Past Meeting" not in titles

    def test_get_future_meetings_sorted_ascending(self, tmp_content_dir):
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "near-future.md").write_text(
            "---\ntitle: Near Meeting\ndate: 2099-01-15\nkind: main\ntime: 7pm\n---\n"
        )
        cm = ContentManager(tmp_content_dir)
        meetings = cm.get_future_meetings()
        assert len(meetings) >= 2
        for i in range(len(meetings) - 1):
            assert meetings[i]["date_obj"] <= meetings[i + 1]["date_obj"]

    def test_get_future_meetings_parses_iso_date(self, tmp_content_dir):
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "iso-date-meeting.md").write_text(
            '---\ntitle: ISO Meeting\ndate: "2099-06-15"\nkind: main\ntime: 7pm\n---\n'
        )
        cm = ContentManager(tmp_content_dir)
        meetings = cm.get_future_meetings()
        titles = [m["title"] for m in meetings]
        assert "ISO Meeting" in titles

    def test_format_future_meetings_empty_list(self, tmp_content_dir, jinja_env):
        cm = ContentManager(tmp_content_dir, jinja_env)
        result = cm.format_future_meetings_section([])
        assert "No upcoming meetings" in result

    def test_format_future_meetings_shows_at_most_two(self, tmp_content_dir, jinja_env):
        meetings_dir = tmp_content_dir / "meetings"
        for i in range(3):
            (meetings_dir / f"extra-{i}.md").write_text(
                f"---\ntitle: Extra Meeting {i}\ndate: 2099-0{i + 1}-10\n"
                "kind: main\ntime: 7pm\n---\n"
            )
        cm = ContentManager(tmp_content_dir, jinja_env)
        meetings = cm.get_future_meetings()
        result = cm.format_future_meetings_section(meetings)
        assert result.count("<strong>") <= 2

    def test_get_future_meetings_no_meetings_dir(self, tmp_path):
        cm = ContentManager(tmp_path)
        assert cm.get_future_meetings() == []

    def test_format_future_meetings_with_announcement(self, tmp_content_dir, jinja_env):
        news_dir = tmp_content_dir / "news"
        (news_dir / "2099-01-01-announce.md").write_text(
            "---\ntitle: Announcement\n---\nDetails.\n"
        )
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "linked-meeting.md").write_text(
            "---\ntitle: Linked Meeting\ndate: 2099-06-15\nkind: main\ntime: 7pm\n"
            "announcement: 2099-01-01-announce.md\n---\n"
        )
        cm = ContentManager(tmp_content_dir, jinja_env)
        meetings = cm.get_future_meetings()
        linked = [m for m in meetings if m["title"] == "Linked Meeting"]
        assert len(linked) == 1
        result = cm.format_future_meetings_section(linked)
        assert "<a href=" in result

    def test_generate_index_hero_inserts_meeting_info(self, tmp_content_dir, jinja_env):
        cm = ContentManager(tmp_content_dir, jinja_env)
        static_content = "<p>Welcome</p><hr/><p>old meeting info</p>"
        result = cm.generate_index_hero(static_content)
        assert "<hr/>" in result
        assert "Welcome" in result

    def test_generate_index_hero_no_hr_returns_unchanged(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        static_content = "<p>No separator here</p>"
        result = cm.generate_index_hero(static_content)
        assert result == static_content

    def test_build_hero_content_missing_file_raises(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        with pytest.raises(FileNotFoundError):
            cm.build_hero_content("projects")

    def test_build_hero_content_index_page(self, tmp_content_dir, jinja_env):
        cm = ContentManager(tmp_content_dir, jinja_env)
        hero = cm.build_hero_content("index")
        assert hero["hero_title"] == "Welcome"
        assert hero["hero_subtitle"] == "Boston Robot Hackers"

    def test_build_hero_content_no_banner_fields_returns_none(
        self, tmp_content_dir, jinja_env
    ):
        cm = ContentManager(tmp_content_dir, jinja_env)
        hero = cm.build_hero_content("index")
        assert hero["banner_image"] is None
        assert hero["banner_title"] is None
        assert hero["banner_subtitle"] is None

    def test_build_hero_content_returns_banner_fields_when_set(self, tmp_content_dir):
        (tmp_content_dir / "heroes" / "projects.md").write_text(
            "---\ntitle: Projects\n"
            "banner_image: images/projects/custom.jpg\n"
            "banner_title: Custom Banner Title\n"
            "banner_subtitle: Custom Banner Subtitle\n"
            "---\nProjects hero body.\n"
        )
        cm = ContentManager(tmp_content_dir)
        hero = cm.build_hero_content("projects")
        assert hero["banner_image"] == "images/projects/custom.jpg"
        assert hero["banner_title"] == "Custom Banner Title"
        assert hero["banner_subtitle"] == "Custom Banner Subtitle"

    def test_process_single_content_file(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        result = cm.process_single_content_file("about.md")
        assert "<p>" in result

    def test_process_single_content_file_missing(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        with pytest.raises(FileNotFoundError):
            cm.process_single_content_file("nonexistent.md")

    def test_get_all_content_order_sort(self, tmp_path):
        items_dir = tmp_path / "items"
        items_dir.mkdir()
        (items_dir / "a.md").write_text("---\ntitle: A\norder: 2\n---\nContent.\n")
        (items_dir / "b.md").write_text("---\ntitle: B\norder: 1\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        ct = ContentType(
            "items",
            "items",
            "order",
            False,
            "details/items-detail.html",
            "pages/items.html",
            "items.html",
        )
        items = cm.get_all_content(ct)
        assert items[0]["metadata"]["order"] == 1
        assert items[1]["metadata"]["order"] == 2


class TestClassifyMeeting:
    def test_returns_explicit_kind(self):
        from content_manager import classify_meeting

        assert classify_meeting({"kind": "main"}) == "main"
        assert classify_meeting({"kind": "handson"}) == "handson"

    def test_missing_kind_raises(self):
        from content_manager import classify_meeting

        with pytest.raises(ValueError):
            classify_meeting({})

    def test_unknown_kind_raises(self):
        from content_manager import classify_meeting

        with pytest.raises(ValueError):
            classify_meeting({"kind": "social"})


class TestResolveNewsHtml:
    def test_resolves_by_filename_stem(self, tmp_content_dir):
        (tmp_content_dir / "news" / "my-talk.md").write_text(
            "---\ntitle: Talk\n---\nx.\n"
        )
        cm = ContentManager(tmp_content_dir)
        assert cm.resolve_news_html("my-talk.md") == ("my-talk.html", True)
        assert cm.resolve_news_html("my-talk") == ("my-talk.html", True)

    def test_resolves_by_slug_decoupled_from_filename(self, tmp_content_dir):
        (tmp_content_dir / "news" / "2099-01-01-raw-name.md").write_text(
            "---\ntitle: Talk\nslug: stable-talk\n---\nx.\n"
        )
        cm = ContentManager(tmp_content_dir)
        # reference by slug resolves; output url uses the slug, not the filename
        assert cm.resolve_news_html("stable-talk") == ("stable-talk.html", True)
        assert cm.resolve_news_html("2099-01-01-raw-name") == ("stable-talk.html", True)

    def test_absent_reference_is_no_link(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        assert cm.resolve_news_html("") == ("", False)

    def test_present_but_unresolved_reference_raises(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        with pytest.raises(ValueError):
            cm.resolve_news_html("nope.md")


TODAY = date(2026, 9, 18)


def write_meeting(content_dir, name, **fields):
    lines = "".join(f'{key}: "{value}"\n' for key, value in fields.items())
    (content_dir / "meetings" / f"{name}.md").write_text(f"---\n{lines}---\n")


class TestFormatLongDate:
    def test_full_weekday_form_without_zero_padding(self):
        assert format_long_date(date(2026, 10, 5)) == "Monday, October 5, 2026"


class TestGetUpcomingTalks:
    TALK = {"kind": "main", "speaker": "Ada", "topic": "Arms", "time": "7:00pm"}

    def talk_topics(self, content_dir):
        talks = ContentManager(content_dir).get_upcoming_talks(TODAY)
        return [talk["topic"] for talk in talks]

    def test_qualifying_talks_included_sorted_ascending(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "later", date="2026-11-12", **self.TALK)
        sooner = {**self.TALK, "topic": "Legs"}
        write_meeting(tmp_path, "sooner", date="2026-10-15", **sooner)
        assert self.talk_topics(tmp_path) == ["Legs", "Arms"]

    def test_meeting_on_today_is_included(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "m", date=TODAY.isoformat(), **self.TALK)
        assert self.talk_topics(tmp_path) == ["Arms"]

    def test_past_talk_excluded(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "m", date="2026-09-17", **self.TALK)
        assert self.talk_topics(tmp_path) == []

    def test_handson_excluded(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        handson = {**self.TALK, "kind": "handson"}
        write_meeting(tmp_path, "m", date="2026-10-01", **handson)
        assert self.talk_topics(tmp_path) == []

    @pytest.mark.parametrize("missing", ["speaker", "topic"])
    def test_missing_speaker_or_topic_excluded(self, tmp_path, missing):
        (tmp_path / "meetings").mkdir()
        fields = {k: v for k, v in self.TALK.items() if k != missing}
        write_meeting(tmp_path, "m", date="2026-10-01", **fields)
        assert self.talk_topics(tmp_path) == []

    def test_page_path_uses_announcement_when_present(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        (tmp_path / "news").mkdir()
        (tmp_path / "news" / "ada-talk.md").write_text("---\ntitle: T\n---\nx.\n")
        write_meeting(
            tmp_path, "m", date="2026-10-01", announcement="ada-talk.md", **self.TALK
        )
        talks = ContentManager(tmp_path).get_upcoming_talks(TODAY)
        assert talks[0]["page_path"] == "news/ada-talk.html"

    def test_page_path_falls_back_to_meeting_page(self, tmp_path):
        (tmp_path / "meetings").mkdir()
        write_meeting(tmp_path, "25-meeting", date="2026-10-01", **self.TALK)
        talks = ContentManager(tmp_path).get_upcoming_talks(TODAY)
        assert talks[0]["page_path"] == "meetings/25-meeting.html"
