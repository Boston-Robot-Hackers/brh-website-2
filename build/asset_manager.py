#!/usr/bin/env python3
# asset_manager — Asset management module for the website builder
# Author: Pito Salas and Claude Code
# Version: 3
# Created: 2026-09-21
# Updated: 2026-11-05
# Open Source Under MIT license
"""Handles copying of static assets like CSS, JS, and images."""

import shutil
from pathlib import Path

import segno
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
        self.copy_directory("content/meeting-reports", "meeting-reports")

    def copy_css_files(self):
        """Copy every CSS file in css/ to output/css."""
        css_dest = self.dist_dir / "css"
        css_dest.mkdir(exist_ok=True)

        for src_file in sorted((self.root_dir / "css").glob("*.css")):
            shutil.copy2(src_file, css_dest / src_file.name)
            print(f"Copied {src_file.name} to {css_dest}")

    def generate_pygments_css(self, theme="default"):
        """Generate Pygments CSS for syntax highlighting."""
        formatter = HtmlFormatter(style=theme, cssclass="highlight")
        css_content = formatter.get_style_defs(".highlight")

        css_dir = self.dist_dir / "css"
        css_dir.mkdir(exist_ok=True)

        css_file = css_dir / "syntax.css"
        css_file.write_text(css_content)
        print(f"Generated syntax highlighting CSS: {css_file}")

    def generate_signup_qr(self, signup_url: str):
        """Write the signup QR, encoding signup_url, to dist/images/signup-qr.png."""
        output_path = self.dist_dir / "images" / "signup-qr.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        segno.make(signup_url, error="m", micro=False).save(
            output_path, scale=10, border=4
        )
        print(f"Generated signup QR code: {output_path}")

    def clean_output_directory(self):
        """Clean and recreate the output directory."""
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(exist_ok=True)
        print(f"Cleaned output directory: {self.dist_dir}")
