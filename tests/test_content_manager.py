from pathlib import Path

import pytest

from content_manager import ContentManager, ContentType
from hero_builder import HeroBuilder


class TestProcessMarkdownFile:
    def test_extracts_title_and_excerpt(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: My Post\nexcerpt: Brief summary.\n---\nBody text.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["title"] == "My Post"
        assert result["excerpt"] == "Brief summary."

    def test_converts_body_to_html(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Test\n---\nHello **world**.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert "<p>" in result["content"]
        assert "<strong>world</strong>" in result["content"]

    def test_id_is_filename_stem(self, tmp_path):
        f = tmp_path / "my-article.md"
        f.write_text("---\ntitle: Article\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["id"] == "my-article"

    def test_title_falls_back_to_name_field(self, tmp_path):
        f = tmp_path / "member.md"
        f.write_text("---\nname: Alice\n---\nBio.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["title"] == "Alice"


class TestDateHandling:
    def test_frontmatter_date_object_serialized_to_iso(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Post\ndate: 2024-03-15\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["date"] is not None
        assert "2024-03-15" in str(result["date"])

    def test_frontmatter_string_date_preserved(self, tmp_path):
        f = tmp_path / "post.md"
        f.write_text("---\ntitle: Post\ndate: \"03/15/2024\"\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["date"] == "03/15/2024"

    def test_date_from_filename_stem(self, tmp_path):
        f = tmp_path / "2024-06-01-my-post.md"
        f.write_text("---\ntitle: Post\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["date"] == "2024-06-01"

    def test_non_date_filename_yields_none(self, tmp_path):
        f = tmp_path / "my-post.md"
        f.write_text("---\ntitle: Post\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        result = cm.process_markdown_file(f, cm.setup_markdown_processor())
        assert result["date"] is None


class TestGetAllContent:
    def test_news_sorted_date_descending(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        ct = ContentType("news", "news", {"sort_key": "date", "reverse": True, "detail_template": "details/news-detail.html", "page_template": "pages/news.html", "output_filename": "news.html"})
        items = cm.get_all_content(ct)
        assert len(items) == 2
        assert items[0]["date"] >= items[1]["date"]

    def test_members_sorted_title_ascending(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        ct = ContentType("members", "members", {"sort_key": "title", "reverse": False, "detail_template": "details/member-detail.html", "page_template": "pages/members.html", "output_filename": "members.html"})
        items = cm.get_all_content(ct)
        assert len(items) == 2
        assert items[0]["title"] == "Alice"
        assert items[1]["title"] == "Bob"

    def test_missing_directory_returns_empty(self, tmp_path):
        cm = ContentManager(tmp_path)
        ct = ContentType("news", "news", {"sort_key": "date", "reverse": True, "detail_template": "details/news-detail.html", "page_template": "pages/news.html", "output_filename": "news.html"})
        assert cm.get_all_content(ct) == []


class TestHeroGeneration:
    def test_get_future_meetings_excludes_past(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        meetings = hb.get_future_meetings()
        titles = [m["title"] for m in meetings]
        assert "Main Meeting" in titles
        assert "Past Meeting" not in titles

    def test_get_future_meetings_sorted_ascending(self, tmp_content_dir):
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "near-future.md").write_text(
            "---\ntitle: Near Meeting\ndate: 01/15/2099\ntime: 7pm\n---\n"
        )
        hb = HeroBuilder(tmp_content_dir)
        meetings = hb.get_future_meetings()
        assert len(meetings) >= 2
        for i in range(len(meetings) - 1):
            assert meetings[i]["date_obj"] <= meetings[i + 1]["date_obj"]

    def test_get_future_meetings_parses_iso_date(self, tmp_content_dir):
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "iso-date-meeting.md").write_text(
            "---\ntitle: ISO Meeting\ndate: \"2099-06-15\"\ntime: 7pm\n---\n"
        )
        hb = HeroBuilder(tmp_content_dir)
        meetings = hb.get_future_meetings()
        titles = [m["title"] for m in meetings]
        assert "ISO Meeting" in titles

    def test_format_future_meetings_empty_list(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        result = hb.format_future_meetings_section([])
        assert "No upcoming meetings" in result

    def test_format_future_meetings_shows_at_most_two(self, tmp_content_dir):
        meetings_dir = tmp_content_dir / "meetings"
        for i in range(3):
            (meetings_dir / f"extra-{i}.md").write_text(
                f"---\ntitle: Extra Meeting {i}\ndate: 0{i + 1}/10/2099\ntime: 7pm\n---\n"
            )
        hb = HeroBuilder(tmp_content_dir)
        meetings = hb.get_future_meetings()
        result = hb.format_future_meetings_section(meetings)
        assert result.count("<strong>") <= 2

    def test_get_future_meetings_no_meetings_dir(self, tmp_path):
        hb = HeroBuilder(tmp_path)
        assert hb.get_future_meetings() == []

    def test_format_future_meetings_with_announcement(self, tmp_content_dir):
        news_dir = tmp_content_dir / "news"
        (news_dir / "2099-01-01-announce.md").write_text(
            "---\ntitle: Announcement\n---\nDetails.\n"
        )
        meetings_dir = tmp_content_dir / "meetings"
        (meetings_dir / "linked-meeting.md").write_text(
            "---\ntitle: Linked Meeting\ndate: 06/15/2099\ntime: 7pm\nannouncement: 2099-01-01-announce.md\n---\n"
        )
        hb = HeroBuilder(tmp_content_dir)
        meetings = hb.get_future_meetings()
        linked = [m for m in meetings if m["title"] == "Linked Meeting"]
        assert len(linked) == 1
        result = hb.format_future_meetings_section(linked)
        assert "<a href=" in result

    def test_generate_index_hero_inserts_meeting_info(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        static_content = "<p>Welcome</p><hr/><p>old meeting info</p>"
        result = hb.generate_index_hero(static_content)
        assert "<hr/>" in result
        assert "Welcome" in result

    def test_generate_index_hero_no_hr_returns_unchanged(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        static_content = "<p>No separator here</p>"
        result = hb.generate_index_hero(static_content)
        assert result == static_content

    def test_build_hero_content_loads_from_file(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        hero = cm.build_hero_content("projects")
        assert hero["hero_title"] == ""
        assert hero["hero_content"] == ""

    def test_build_hero_content_index_page(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        hero = cm.build_hero_content("index")
        assert hero["hero_title"] == "Welcome"
        assert hero["hero_subtitle"] == "Boston Robot Hackers"

    def test_process_single_content_file(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        result = cm.process_single_content_file("about.md")
        assert "<p>" in result

    def test_process_single_content_file_missing(self, tmp_content_dir):
        cm = ContentManager(tmp_content_dir)
        result = cm.process_single_content_file("nonexistent.md")
        assert "not found" in result

    def test_get_all_content_order_sort(self, tmp_path):
        items_dir = tmp_path / "items"
        items_dir.mkdir()
        (items_dir / "a.md").write_text("---\ntitle: A\norder: 2\n---\nContent.\n")
        (items_dir / "b.md").write_text("---\ntitle: B\norder: 1\n---\nContent.\n")
        cm = ContentManager(tmp_path)
        ct = ContentType("items", "items", {"sort_key": "order", "reverse": False, "detail_template": "details/items-detail.html", "page_template": "pages/items.html", "output_filename": "items.html"})
        items = cm.get_all_content(ct)
        assert items[0]["metadata"]["order"] == 1
        assert items[1]["metadata"]["order"] == 2


class TestLegacyMeetingMethods:
    def test_format_single_meeting_for_hero_with_time(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7:00pm", "location": "", "announcement": ""}
        result = hb.format_single_meeting_for_hero("Test Label", meeting)
        assert "Test Label" in result
        assert "03/15/2024" in result

    def test_format_single_meeting_for_hero_with_announcement(self, tmp_content_dir):
        news_dir = tmp_content_dir / "news"
        (news_dir / "announce.md").write_text("---\ntitle: Announce\n---\nDetails.\n")
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7pm", "location": "Lab", "announcement": "announce.md"}
        result = hb.format_single_meeting_for_hero("Label", meeting)
        assert "<a href=" in result

    def test_load_meeting_info_exists(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        result = hb.load_meeting_info("meeting-future.md")
        assert result is not None
        assert result["title"] == "Main Meeting"

    def test_load_meeting_info_missing(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        result = hb.load_meeting_info("nonexistent.md")
        assert result is None

    def test_format_meeting_section_both_present(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7pm", "location": "", "announcement": "x.md"}
        result = hb.format_meeting_section(meeting, meeting)
        assert "Next Meeting" in result
        assert "Next Hands-On Meeting" in result

    def test_format_meeting_section_one_missing(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7pm", "location": "", "announcement": ""}
        result = hb.format_meeting_section(meeting, None)
        assert "Next Meeting" in result
        assert "Next Hands-On Meeting" not in result

    def test_format_single_meeting_with_announcement(self, tmp_content_dir):
        news_dir = tmp_content_dir / "news"
        (news_dir / "event.md").write_text("---\ntitle: Event\n---\nDetails.\n")
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7pm", "location": "Lab", "announcement": "event.md"}
        result = hb.format_single_meeting("Meeting", meeting)
        assert "<a href=" in result

    def test_format_single_meeting_no_announcement(self, tmp_content_dir):
        hb = HeroBuilder(tmp_content_dir)
        meeting = {"date": "03/15/2024", "time": "7pm", "location": "", "announcement": ""}
        result = hb.format_single_meeting("Meeting", meeting)
        assert "coming soon" in result
