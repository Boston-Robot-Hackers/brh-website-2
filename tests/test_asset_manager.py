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
    def test_copies_shared_and_main_css(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        css_src = root / "css"
        css_src.mkdir()
        (css_src / "shared.css").write_text("body {}")
        (css_src / "main.css").write_text(".main {}")
        am = AssetManager(root, dist)
        am.copy_css_files()
        assert (dist / "css" / "shared.css").read_text() == "body {}"
        assert (dist / "css" / "main.css").read_text() == ".main {}"

    def test_missing_css_files_skipped(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        (root / "css").mkdir()
        am = AssetManager(root, dist)
        am.copy_css_files()
        assert not (dist / "css" / "shared.css").exists()


class TestGenerateQrCode:
    def test_writes_valid_png(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        am = AssetManager(root, dist)
        am.generate_qr_code("https://example.com/signup")
        qr_file = dist / "images" / "signup-qr.png"
        assert qr_file.exists()
        assert qr_file.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"

    def test_different_urls_produce_different_images(self, tmp_path):
        root = tmp_path / "root"
        dist = tmp_path / "dist"
        root.mkdir()
        dist.mkdir()
        am = AssetManager(root, dist)
        am.generate_qr_code("https://example.com/one", filename="one.png")
        am.generate_qr_code("https://example.com/two", filename="two.png")
        assert (dist / "images" / "one.png").read_bytes() != (
            dist / "images" / "two.png"
        ).read_bytes()


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
