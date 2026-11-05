#!/usr/bin/env python3
# test_signup_qr — Tests that the signup QR encodes signup_url, on the home page only
# Author: Pito Salas and Claude Code
# Version: 4
# Created: 2026-09-21
# Updated: 2026-11-05
# Open Source Under MIT license
import json
from pathlib import Path

import pytest
import zxingcpp
from asset_manager import AssetManager
from PIL import Image

from build import WebsiteBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
SIGNUP_URL = json.loads((REPO_ROOT / "config" / "site.json").read_text())["signup_url"]
QR_SRC = "images/signup-qr.png"
# The .home-lead__qr box in css/pages.css: 140px, less 5px padding and 1px border.
DISPLAYED_QR_PX = 128


def decoded_urls(image: Image.Image) -> list[str]:
    return [barcode.text for barcode in zxingcpp.read_barcodes(image.convert("RGB"))]


@pytest.fixture(scope="module")
def built_site(tmp_path_factory):
    """Runs the real build() into a temp directory, so the real output/ survives."""
    builder = WebsiteBuilder()
    builder.dist_dir = tmp_path_factory.mktemp("output")
    builder.asset_manager.dist_dir = builder.dist_dir
    builder.page_builder.dist_dir = builder.dist_dir
    builder.build()
    return builder.dist_dir


def test_built_qr_encodes_signup_url(built_site):
    assert decoded_urls(Image.open(built_site / QR_SRC)) == [SIGNUP_URL]


def test_built_qr_scans_at_displayed_size(built_site):
    image = Image.open(built_site / QR_SRC).convert("RGB")
    small = image.resize((DISPLAYED_QR_PX, DISPLAYED_QR_PX), Image.Resampling.BILINEAR)
    assert decoded_urls(small) == [SIGNUP_URL]


def test_qr_follows_the_url_it_is_given(tmp_path):
    other_url = "https://example.com/other-form"
    AssetManager(tmp_path, tmp_path).generate_signup_qr(other_url)
    assert decoded_urls(Image.open(tmp_path / QR_SRC)) == [other_url]


@pytest.mark.parametrize("page", ["content/home.md", "content/about.md"])
def test_signup_links_match_signup_url(page):
    assert SIGNUP_URL in (REPO_ROOT / page).read_text()


def test_qr_is_served_from_the_site_itself(built_site):
    assert f'src="{QR_SRC}"' in (built_site / "index.html").read_text()


def test_old_service_generated_image_is_gone():
    assert not (REPO_ROOT / "images" / "brh_qr.png").exists()


def test_qr_on_home_page_only(built_site):
    pages_with_qr = [
        page.relative_to(built_site).as_posix()
        for page in built_site.rglob("*.html")
        if "signup-qr.png" in page.read_text()
    ]
    assert pages_with_qr == ["index.html"]


def test_home_lead_has_alt_text_and_caption():
    home_lead_html = (
        REPO_ROOT / "templates" / "components" / "home-lead.html"
    ).read_text()
    assert 'alt="Scan to sign up' in home_lead_html
    assert "Join BRH" in home_lead_html
