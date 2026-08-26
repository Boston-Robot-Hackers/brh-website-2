from pathlib import Path

from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent


def render_banner(**context):
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "templates")))
    template = env.get_template("components/banner.html")
    return template.render(**context)


SITE = {
    "title": "Boston Robot Hackers",
    "subtitle": "CONNECT * LEARN * BUILD",
    "default_banner_image": "images/meetings/meeting1-1.jpg",
}


def test_uses_resolved_banner_fields():
    html = render_banner(
        site=SITE,
        banner_image="images/projects/pupper_standing.jpg",
        banner_title="Pupper",
        banner_subtitle="An open-source quadruped robot",
    )
    assert "background-image: url('images/projects/pupper_standing.jpg')" in html
    assert "<h1>Pupper</h1>" in html
    assert "<p>An open-source quadruped robot</p>" in html


def test_falls_back_to_site_defaults_when_banner_vars_missing():
    html = render_banner(site=SITE)
    assert "background-image: url('images/meetings/meeting1-1.jpg')" in html
    assert "<h1>Boston Robot Hackers</h1>" in html
    assert "<p>CONNECT * LEARN * BUILD</p>" in html
