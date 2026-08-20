#!/usr/bin/env python3
"""
asset_manager.py — Asset management module for the website builder.
Handles copying of static assets like CSS, JS, and images.

Author: Pito Salas and Claude Code
Open Source Under MIT license
"""

import shutil
from pathlib import Path

import qrcode
from pygments.formatters import HtmlFormatter


class AssetManager:
    """Manages static asset copying and CSS generation."""

    def __init__(self, root_dir: Path, dist_dir: Path):
        self.root_dir = root_dir
        self.dist_dir = dist_dir

    def copy_directory(self, src_name: str, dest_name: str | None = None):
        """Generic method to copy a directory."""
        dest_name = dest_name or src_name
        src_path = self.root_dir / src_name
        dest_path = self.dist_dir / dest_name

        if src_path.exists():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"Copied {src_name} to {dest_path}")

    def copy_assets(self):
        """Copy static assets to output directory."""
        self.copy_directory("images")
        self.copy_directory("scripts")

    def copy_css_files(self):
        """Copy CSS files to output/css directory."""
        css_dest = self.dist_dir / "css"
        css_dest.mkdir(exist_ok=True)

        css_src_dir = self.root_dir / "css"

        for css_file in ["shared.css", "main.css"]:
            src_file = css_src_dir / css_file
            if src_file.exists():
                shutil.copy2(src_file, css_dest / css_file)
                print(f"Copied {css_file} to {css_dest}")

    def generate_pygments_css(self, theme="default"):
        """Generate Pygments CSS for syntax highlighting."""
        formatter = HtmlFormatter(style=theme, cssclass="highlight")
        css_content = formatter.get_style_defs(".highlight")

        css_dir = self.dist_dir / "css"
        css_dir.mkdir(exist_ok=True)

        css_file = css_dir / "syntax.css"
        css_file.write_text(css_content)
        print(f"Generated syntax highlighting CSS: {css_file}")

    def generate_qr_code(self, url: str, filename: str = "signup-qr.png"):
        """Generate a QR code PNG linking to url, written to dist/images."""
        output_path = self.dist_dir / "images" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        qrcode.make(url).save(output_path)
        print(f"Generated QR code: {output_path}")

    def clean_output_directory(self):
        """Clean and recreate the output directory."""
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(exist_ok=True)
        print(f"Cleaned output directory: {self.dist_dir}")
