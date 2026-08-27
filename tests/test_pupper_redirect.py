from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REDIRECT_DIR = REPO_ROOT / "ops" / "pupper-redirect"
TARGET_URL = "https://bostonrobothackers.com/projects/pupper.html"
REDIRECT_DOMAIN = "pupper.bostonrobothackers.com"


def test_redirect_page_targets_pupper_project_page():
    """Regression test: a hand-edit to index.html must not typo the target URL."""
    html = (REDIRECT_DIR / "index.html").read_text()
    assert TARGET_URL in html


def test_cname_file_has_exact_subdomain():
    """Regression test: GitHub Pages matches the CNAME file byte-for-byte."""
    cname = (REDIRECT_DIR / "CNAME").read_text().strip()
    assert cname == REDIRECT_DOMAIN
