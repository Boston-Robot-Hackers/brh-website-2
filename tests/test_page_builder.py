import pytest
from content_manager import ContentType
from jinja2 import DictLoader, Environment
from page_builder import PageBuilder


@pytest.fixture
def dist(tmp_path):
    return tmp_path / "dist"


@pytest.fixture
def page_builder(dist):
    dist.mkdir()
    templates = {
        "pages/simple.html": "{{ site.name }} {{ title }}",
        "details/news-detail.html": "{{ site.name }} {{ post.title }}",
        "details/project-detail.html": "{{ site.name }} {{ project.title }}",
        "details/member-detail.html": "{{ site.name }} {{ member.title }}",
        "details/meeting-detail.html": "{{ site.name }} {{ meeting.title }}",
    }
    env = Environment(loader=DictLoader(templates))
    return PageBuilder(env, dist, {"name": "BRH"})


class TestFormatDate:
    def test_iso_date(self, page_builder):
        assert page_builder.format_date("2024-03-15") == "March 15, 2024"

    def test_empty_string_returns_empty(self, page_builder):
        assert page_builder.format_date("") == ""

    def test_none_returns_empty(self, page_builder):
        assert page_builder.format_date(None) == ""

    def test_non_iso_raises(self, page_builder):
        with pytest.raises(ValueError):
            page_builder.format_date("03/15/2024")
        with pytest.raises(ValueError):
            page_builder.format_date("not-a-date")


class TestResolveBanner:
    @pytest.fixture
    def pb(self, dist):
        dist.mkdir()
        env = Environment(loader=DictLoader({}))
        site_config = {
            "title": "Boston Robot Hackers",
            "subtitle": "CONNECT * LEARN * BUILD",
            "default_banner_image": "images/meetings/meeting1-1.jpg",
        }
        return PageBuilder(env, dist, site_config)

    def test_no_override_falls_back_to_site_defaults(self, pb):
        result = pb.resolve_banner({})
        assert result["banner_image"] == "images/meetings/meeting1-1.jpg"
        assert result["banner_title"] == "Boston Robot Hackers"
        assert result["banner_subtitle"] == "CONNECT * LEARN * BUILD"

    def test_full_override(self, pb):
        metadata = {
            "banner_image": "images/projects/pupper_standing.jpg",
            "banner_title": "Pupper",
            "banner_subtitle": "An open-source quadruped robot",
        }
        result = pb.resolve_banner(metadata)
        assert result["banner_image"] == "images/projects/pupper_standing.jpg"
        assert result["banner_title"] == "Pupper"
        assert result["banner_subtitle"] == "An open-source quadruped robot"

    def test_partial_override_falls_back_for_missing_fields(self, pb):
        result = pb.resolve_banner({"banner_image": "images/projects/custom.jpg"})
        assert result["banner_image"] == "images/projects/custom.jpg"
        assert result["banner_title"] == "Boston Robot Hackers"
        assert result["banner_subtitle"] == "CONNECT * LEARN * BUILD"

    def test_path_prefix_applied_to_override(self, pb):
        result = pb.resolve_banner(
            {"banner_image": "images/projects/custom.jpg"}, path_prefix="../"
        )
        assert result["banner_image"] == "../images/projects/custom.jpg"

    def test_path_prefix_applied_to_default(self, pb):
        result = pb.resolve_banner({}, path_prefix="../")
        assert result["banner_image"] == "../images/meetings/meeting1-1.jpg"


class TestBuildPage:
    def test_writes_html_to_output_file(self, page_builder, dist):
        page_builder.build_page("pages/simple.html", "output.html", title="Hello")
        output = dist / "output.html"
        assert output.exists()
        assert "BRH Hello" in output.read_text()

    def test_site_config_injected_automatically(self, page_builder, dist):
        page_builder.build_page("pages/simple.html", "site.html", title="Test")
        assert "BRH" in (dist / "site.html").read_text()

    def test_returns_output_path(self, page_builder, dist):
        result = page_builder.build_page("pages/simple.html", "out.html", title="X")
        assert result == dist / "out.html"


class TestResolveAnnouncementReport:
    def test_absent_refs_all_false(self, page_builder):
        result = page_builder.resolve_announcement_report({})
        assert result == {
            "announcement_exists": False,
            "report_exists": False,
            "announcement_html": "",
            "report_html": "",
        }

    def test_prefix_applied_to_all_keys(self, page_builder):
        result = page_builder.resolve_announcement_report({}, prefix="main_")
        assert set(result.keys()) == {
            "main_announcement_exists",
            "main_report_exists",
            "main_announcement_html",
            "main_report_html",
        }


class TestBuildDetailPages:
    def _make_items(self, ids):
        return [
            {"id": item_id, "title": item_id.capitalize(), "date": None, "metadata": {}}
            for item_id in ids
        ]

    def test_writes_one_file_per_item(self, page_builder, dist):
        items = self._make_items(["post-1", "post-2"])
        ct = ContentType(
            "news",
            "news",
            "date",
            True,
            "details/news-detail.html",
            "pages/news.html",
            "news.html",
        )
        page_builder.build_detail_pages(items, ct)
        assert (dist / "news" / "post-1.html").exists()
        assert (dist / "news" / "post-2.html").exists()

    def test_creates_subdirectory(self, page_builder, dist):
        items = self._make_items(["proj-1"])
        ct = ContentType(
            "projects",
            "projects",
            "title",
            False,
            "details/project-detail.html",
            "pages/projects.html",
            "projects.html",
        )
        page_builder.build_detail_pages(items, ct)
        assert (dist / "projects").is_dir()

    def test_empty_items_writes_nothing(self, page_builder, dist):
        ct = ContentType(
            "members",
            "members",
            "title",
            False,
            "details/member-detail.html",
            "pages/members.html",
            "members.html",
        )
        page_builder.build_detail_pages([], ct)
        assert not (dist / "members").exists()

    def test_formats_date_in_detail_page(self, dist):
        dist.mkdir()
        templates = {
            "details/news-detail.html": "{{ post.date }}",
        }
        env = Environment(loader=DictLoader(templates))
        pb = PageBuilder(env, dist, {"name": "BRH"})
        items = [
            {"id": "post-1", "title": "Post", "date": "2024-03-15", "metadata": {}}
        ]
        ct = ContentType(
            "news",
            "news",
            "date",
            True,
            "details/news-detail.html",
            "pages/news.html",
            "news.html",
        )
        pb.build_detail_pages(items, ct)
        content = (dist / "news" / "post-1.html").read_text()
        assert "March 15, 2024" in content


@pytest.fixture
def rich_page_builder(dist):
    dist.mkdir()
    templates = {
        "cards/news-card.html": "{{ title }}",
        "cards/compact-news-card.html": "{{ title }}",
        "cards/project-card.html": "{{ title }}",
        "cards/project-listing-item.html": "{{ project.title }}",
        "cards/member-card.html": "{{ name }}",
        "cards/compact-meeting-card.html": "{{ title }}",
        "cards/monthly-meeting-card.html": "{{ month_label }}",
        "components/upcoming-meetings-calendar.html": "{{ meetings | length }}",
    }
    env = Environment(loader=DictLoader(templates))
    return PageBuilder(env, dist, {"name": "BRH"})


def _news_item(slug, title):
    return {
        "id": slug,
        "title": title,
        "date": "2024-01-01",
        "metadata": {},
        "image": "",
        "text": "",
        "excerpt": "",
    }


def _meeting_item(slug, title, date_str, kind="main"):
    return {
        "id": slug,
        "title": title,
        "date": date_str,
        "metadata": {"date": date_str, "time": "7pm", "kind": kind},
        "image": "",
        "text": "",
        "excerpt": "",
    }


class TestRenderCards:
    def test_render_news_cards_returns_html(self, rich_page_builder):
        items = [_news_item("a", "Alpha"), _news_item("b", "Beta")]
        result = rich_page_builder.render_news_cards(items)
        assert "Alpha" in result
        assert "Beta" in result

    def test_render_news_cards_empty_returns_empty(self, rich_page_builder):
        assert rich_page_builder.render_news_cards([]) == ""

    def test_render_compact_news_cards(self, rich_page_builder):
        items = [_news_item("x", "News Item")]
        result = rich_page_builder.render_compact_news_cards(items)
        assert "News Item" in result

    def test_render_project_cards_for_home(self, rich_page_builder):
        items = [
            {
                "id": "p1",
                "title": "Robot",
                "date": None,
                "metadata": {"status": "Active"},
                "image": "",
                "text": "",
                "excerpt": "",
            }
        ]
        result = rich_page_builder.render_project_cards_for_home(items)
        assert "Robot" in result

    def test_render_projects_content(self, rich_page_builder):
        items = [
            {
                "id": "p1",
                "title": "Drone",
                "date": None,
                "metadata": {},
                "image": "",
                "text": "",
                "excerpt": "",
            }
        ]
        result = rich_page_builder.render_projects_content(items)
        assert "Drone" in result

    def test_render_member_cards(self, rich_page_builder):
        members = [
            {
                "id": "m1",
                "title": "Alice",
                "date": None,
                "metadata": {"role": "Builder", "skills": [], "card-text": "M"},
                "image": "",
                "text": "",
                "excerpt": "",
            }
        ]
        result = rich_page_builder.render_member_cards(members)
        assert "Alice" in result


class TestGroupMeetingsByMonth:
    def test_groups_main_and_handson(self, rich_page_builder):
        meetings = [
            _meeting_item("main-jan", "January Meeting", "2024-01-15", kind="main"),
            _meeting_item(
                "hands-jan", "Hands On January", "2024-01-22", kind="handson"
            ),
        ]
        grouped = rich_page_builder.group_meetings_by_month(meetings)
        assert len(grouped) == 1
        assert grouped[0]["main_meeting"] is not None
        assert grouped[0]["handson_meeting"] is not None

    def test_sorted_descending_by_month(self, rich_page_builder):
        meetings = [
            _meeting_item("feb", "Feb Meeting", "2024-02-01"),
            _meeting_item("jan", "Jan Meeting", "2024-01-01"),
        ]
        grouped = rich_page_builder.group_meetings_by_month(meetings)
        assert grouped[0]["sort_key"] > grouped[1]["sort_key"]

    def test_skips_items_with_no_date(self, rich_page_builder):
        meetings = [
            {
                "id": "x",
                "title": "No Date",
                "date": None,
                "metadata": {"date": ""},
                "image": "",
                "text": "",
                "excerpt": "",
            }
        ]
        grouped = rich_page_builder.group_meetings_by_month(meetings)
        assert grouped == []


class TestRenderUpcomingCalendar:
    def test_renders_future_meetings(self, rich_page_builder):
        meetings = [_meeting_item("future", "Future Meeting", "2099-12-31")]
        result = rich_page_builder.render_upcoming_meetings_calendar(meetings)
        assert "1" in result

    def test_skips_past_meetings(self, rich_page_builder):
        meetings = [_meeting_item("old", "Old Meeting", "2020-01-01")]
        result = rich_page_builder.render_upcoming_meetings_calendar(meetings)
        assert result == "" or "0" in result

    def test_empty_list_returns_empty(self, rich_page_builder):
        assert rich_page_builder.render_upcoming_meetings_calendar([]) == ""
