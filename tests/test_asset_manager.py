#!/usr/bin/env python3
# test_asset_manager — Tests for AssetManager output cleaning and asset copying
# Author: Pito Salas and Claude Code
# Version: 3
# Created: 2026-09-21
# Updated: 2026-11-05
# Open Source Under MIT license
from asset_manager import AssetManager


class TestCleanOutputDirectory:
    def test_wipes_existing_files(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        (dist / "old_file.txt").write_text("old")
        am = AssetManager(root, dist)
        am.clean_output_directory()
        assert dist.exists()
        assert not (dist / "old_file.txt").exists()

    def test_creates_dist_if_absent(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        am = AssetManager(root, dist)
        am.clean_output_directory()
        assert dist.exists()


class TestCopyDirectory:
    def test_copies_tree_to_dist(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        images = root / "images"
        images.mkdir()
        (images / "photo.jpg").write_text("fake image data")
        am = AssetManager(root, dist)
        am.copy_directory("images")
        assert (dist / "images" / "photo.jpg").exists()

    def test_replaces_existing_dest(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        (root / "scripts").mkdir()
        (root / "scripts" / "app.js").write_text("new")
        dest_scripts = dist / "scripts"
        dest_scripts.mkdir()
        (dest_scripts / "old.js").write_text("old")
        am = AssetManager(root, dist)
        am.copy_directory("scripts")
        assert (dist / "scripts" / "app.js").exists()
        assert not (dist / "scripts" / "old.js").exists()

    def test_missing_src_is_silently_skipped(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        am = AssetManager(root, dist)
        am.copy_directory("nonexistent")
        assert not (dist / "nonexistent").exists()


class TestCopyCssFiles:
    def test_copies_every_css_file(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        css_src = root / "css"
        css_src.mkdir()
        (css_src / "base.css").write_text("body {}")
        (css_src / "pages.css").write_text(".page {}")
        (css_src / "notes.txt").write_text("not css")
        am = AssetManager(root, dist)
        am.copy_css_files()
        assert (dist / "css" / "base.css").read_text() == "body {}"
        assert (dist / "css" / "pages.css").read_text() == ".page {}"
        assert not (dist / "css" / "notes.txt").exists()

    def test_empty_css_dir_copies_nothing(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        (root / "css").mkdir()
        am = AssetManager(root, dist)
        am.copy_css_files()
        assert list((dist / "css").iterdir()) == []


class TestGeneratePygmentsCSS:
    def test_writes_nonempty_css_file(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        am = AssetManager(root, dist)
        am.generate_pygments_css("default")
        css_file = dist / "css" / "syntax.css"
        assert css_file.exists()
        assert len(css_file.read_text()) > 0
