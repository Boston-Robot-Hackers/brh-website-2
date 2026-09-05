import pytest


@pytest.fixture
def tmp_content_dir(tmp_path):
    """Create a minimal content directory tree with sample markdown files."""
    for d in ["news", "projects", "members", "meetings", "heroes"]:
        (tmp_path / d).mkdir()

    (tmp_path / "news" / "2024-03-15-first-post.md").write_text(
        "---\ntitle: First Post\ndate: 2024-03-15\nexcerpt: A short excerpt.\n"
        "highlight: true\n---\nHello **world**.\n"
    )
    (tmp_path / "news" / "2024-01-10-old-post.md").write_text(
        "---\ntitle: Old Post\ndate: 2024-01-10\nexcerpt: Older news.\n"
        "highlight: false\n---\nOld content.\n"
    )
    (tmp_path / "projects" / "robot-arm.md").write_text(
        "---\ntitle: Robot Arm\nstatus: Active\n---\nA robot arm project.\n"
    )
    (tmp_path / "projects" / "aerial-drone.md").write_text(
        "---\ntitle: Aerial Drone\nstatus: Planning\n---\nA drone project.\n"
    )
    (tmp_path / "members" / "alice.md").write_text(
        "---\ntitle: Alice\nrole: Builder\n---\nAlice bio.\n"
    )
    (tmp_path / "members" / "bob.md").write_text(
        "---\ntitle: Bob\nrole: Designer\n---\nBob bio.\n"
    )
    (tmp_path / "meetings" / "meeting-future.md").write_text(
        "---\ntitle: Main Meeting\ndate: 2099-12-31\nkind: main\ntime: 7:00pm\n---\n"
    )
    (tmp_path / "meetings" / "meeting-past.md").write_text(
        "---\ntitle: Past Meeting\ndate: 2020-01-01\nkind: main\ntime: 7:00pm\n---\n"
    )
    (tmp_path / "heroes" / "index.md").write_text(
        "---\ntitle: Welcome\nsubtitle: Boston Robot Hackers\n---\n"
        "Hero content here.\n<hr/>\nMeeting info.\n"
    )
    (tmp_path / "about.md").write_text("---\ntitle: About\n---\nAbout the group.\n")
    return tmp_path
