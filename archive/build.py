#!/usr/bin/env python3
"""
Build script for Boston Robot Hackers website.
Uses template-based architecture.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from pygments.formatters import HtmlFormatter


class WebsiteBuilder:
    def __init__(self):
        # Detect if running from build/ subdirectory or root directory
        current_dir = Path.cwd()
        if current_dir.name == "build":
            self.root_dir = Path("..")  # Build script is running from build/ subdirectory
        else:
            self.root_dir = Path(".")   # Build script is running from root directory
        self.templates_dir = self.root_dir / "templates"
        self.config_dir = self.root_dir / "config"
        self.content_dir = self.root_dir / "content"
        self.dist_dir = self.root_dir / "output"
        
        # Create dist directory if it doesn't exist
        self.dist_dir.mkdir(exist_ok=True)
        
        # Load configurations
        self.site_config = self.load_site_config()
        
        # CTA content removed - now included directly in hero markdown
        
        # Set up Jinja2 environment
        template_paths = [
            str(self.templates_dir),               # Main templates directory
        ]
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_paths)
        )
    
    def load_site_config(self) -> Dict[str, Any]:
        """Load site configuration."""
        config_file = self.config_dir / "site.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        return {}
    
    
    
    def setup_markdown_processor(self):
        """Set up markdown processor with syntax highlighting."""
        return markdown.Markdown(
            extensions=[
                'codehilite',
                'fenced_code',
                'tables',
                'toc'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True,
                    'noclasses': False,
                }
            }
        )
    
    def generate_pygments_css(self, theme='default'):
        """Generate Pygments CSS for syntax highlighting."""
        formatter = HtmlFormatter(style=theme, cssclass='highlight')
        css_content = formatter.get_style_defs('.highlight')
        
        # Create css directory if it doesn't exist
        css_dir = self.dist_dir / 'css'
        css_dir.mkdir(exist_ok=True)
        
        css_file = css_dir / 'syntax.css'
        css_file.write_text(css_content)
        print(f"Generated syntax highlighting CSS: {css_file}")
    
    def process_markdown_file(self, file_path: Path, md_processor) -> Dict[str, Any]:
        """Process a single markdown file and return structured data."""
        try:
            # Parse front matter and content
            post = frontmatter.load(file_path)
            
            # Process markdown content
            html_content = md_processor.convert(post.content)
            
            # Extract metadata
            metadata = post.metadata
            
            # Parse date from filename if not in front matter
            if 'date' not in metadata:
                # Assume filename format: YYYY-MM-DD-title.md
                date_str = file_path.stem[:10]  # First 10 chars should be date
                try:
                    metadata['date'] = datetime.strptime(date_str, '%Y-%m-%d').date().isoformat()
                except ValueError:
                    metadata['date'] = datetime.now().date().isoformat()
            elif isinstance(metadata['date'], datetime):
                metadata['date'] = metadata['date'].isoformat()
            elif hasattr(metadata['date'], 'isoformat'):
                metadata['date'] = metadata['date'].isoformat()
            
            # Ensure required fields have defaults
            return {
                'id': file_path.stem,
                'title': metadata.get('title', metadata.get('name', 'Untitled')),
                'date': metadata.get('date'),
                'image': metadata.get('image', ''),  # URL to 512x512 square image (scaled with CSS as needed)
                'text': metadata.get('text', metadata.get('emoji')),  # Simple text overlay
                'excerpt': metadata.get('excerpt', ''),
                'content': html_content,
                'metadata': metadata
            }
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def format_date(self, date_str: str) -> str:
        """Format date string for display."""
        if isinstance(date_str, str):
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime('%B %d, %Y')
            except ValueError:
                return date_str
        return str(date_str)
    
    def render_news_cards(self, posts: List[Dict[str, Any]]) -> str:
        """Render news cards using the template."""
        template = self.jinja_env.get_template('cards/news-card.html')
        
        cards_html = []
        for post in posts:
            # Use default image classes
            image_classes = "image-base image-square d-flex align-items-center justify-content-center text-white fw-bold"
            
            card_html = template.render(
                id=post['id'],
                title=post['title'],
                excerpt=post['excerpt'],
                text=post['text'],
                image=post['image'],
                formatted_date=self.format_date(post['date']),
                image_classes=image_classes
            )
            cards_html.append(card_html)
        
        return '\n'.join(cards_html)
    
    def build_hero_content(self, page_name: str = 'index') -> Dict[str, Any]:
        """Build hero content from page-specific markdown file."""
        hero_file = self.content_dir / 'heroes' / f'{page_name}.md'
        if not hero_file.exists():
            print(f"Warning: {hero_file} not found, leaving hero section blank")
            return {
                'hero_title': '',
                'hero_subtitle': '',
                'hero_content': ''
            }
        
        # Set up markdown processor
        md_processor = self.setup_markdown_processor()
        
        # Process hero markdown file
        hero_data = self.process_markdown_file(hero_file, md_processor)
        if hero_data:
            return {
                'hero_title': hero_data['title'],
                'hero_subtitle': hero_data['metadata'].get('subtitle', ''),
                'hero_content': hero_data['content']
            }
        
        print(f"Warning: Failed to process {hero_file}, leaving hero section blank")
        return {
            'hero_title': '',
            'hero_subtitle': '',
            'hero_content': ''
        }

    def get_all_news_posts(self):
        """Get all news posts from markdown files."""
        whatsnew_dir = self.content_dir / 'news'
        if not whatsnew_dir.exists():
            print(f"Warning: {whatsnew_dir} directory not found")
            return []
        
        # Set up markdown processor
        md_processor = self.setup_markdown_processor()
        
        # Process all markdown files
        posts = []
        for md_file in whatsnew_dir.glob('*.md'):
            post_data = self.process_markdown_file(md_file, md_processor)
            if post_data:
                posts.append(post_data)
        
        # Sort by date (newest first) 
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts

    def build_whatsnew(self) -> str:
        """Build the What's New section from markdown files (highlighted only)."""
        posts = self.get_all_news_posts()
        
        # Filter only highlighted posts for home page
        highlighted_posts = [post for post in posts if post['metadata'].get('highlight', False)]
        
        # Render news cards
        news_html = self.render_news_cards(highlighted_posts)
        
        print(f"Generated {len(highlighted_posts)} highlighted posts from {len(posts)} total")
        return news_html
    
    def render_compact_news_cards(self, posts):
        """Render compact news cards for the full news page."""
        template = self.jinja_env.get_template('cards/compact-news-card.html')
        cards_html = []
        
        for post in posts:
            # Format the date
            try:
                if isinstance(post['date'], str):
                    date_obj = datetime.fromisoformat(post['date']).date()
                else:
                    date_obj = post['date']
                formatted_date = date_obj.strftime("%B %d, %Y")
            except:
                formatted_date = str(post['date'])
            
            # Render the card
            card_html = template.render(
                id=post['id'],
                title=post['title'],
                excerpt=post['excerpt'],
                formatted_date=formatted_date,
                image=post['image'],
                text=post['text']
            )
            cards_html.append(card_html)
        
        return '\n'.join(cards_html)
    
    def build_news_detail_pages(self, posts):
        """Build individual detail pages for each news item."""
        detail_template = self.jinja_env.get_template('details/news-detail.html')
        
        for post in posts:
            # Create news detail directory if it doesn't exist
            news_detail_dir = self.dist_dir / 'news'
            news_detail_dir.mkdir(exist_ok=True)
            
            # Format date for display
            post_with_formatted_date = post.copy()
            post_with_formatted_date['date'] = self.format_date(post['date'])
            
            # Generate detail page
            html_content = detail_template.render(
                site=self.site_config,
                post=post_with_formatted_date,
            )
            
            # Write individual detail page
            detail_file = news_detail_dir / f"{post['id']}.html"
            detail_file.write_text(html_content, encoding='utf-8')
        
        print(f"Built {len(posts)} news detail pages")

    def build_news_page(self):
        """Build the whatsnew.html page with all news items."""
        posts = self.get_all_news_posts()
        
        # Build individual detail pages
        self.build_news_detail_pages(posts)
        
        news_content = self.render_compact_news_cards(posts)
        
        # Generate hero content for whatsnew page
        hero_content = self.build_hero_content('whatsnew')
        
        # Load and render the whatsnew template
        template = self.jinja_env.get_template('pages/whatsnew.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            news_content=news_content
        )
        
        # Write to whatsnew.html
        output_file = self.dist_dir / 'whatsnew.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built whatsnew.html with {len(posts)} posts")
    
    def get_all_projects(self):
        """Get all projects from markdown files."""
        projects_dir = self.content_dir / 'projects'
        if not projects_dir.exists():
            print(f"Warning: {projects_dir} directory not found")
            return []
        
        # Set up markdown processor
        md_processor = self.setup_markdown_processor()
        
        # Process all markdown files
        projects = []
        for md_file in projects_dir.glob('*.md'):
            project_data = self.process_markdown_file(md_file, md_processor)
            if project_data:
                projects.append(project_data)
        
        # Sort by date (newest first)
        projects.sort(key=lambda x: x['date'], reverse=True)
        return projects
    
    def render_projects_content(self, projects):
        """Render projects as full content articles using template."""
        template = self.jinja_env.get_template('cards/project-listing-item.html')
        content_sections = []
        
        for project in projects:
            section_html = template.render(
                project=project,
                formatted_date=self.format_date(project['date'])
            )
            content_sections.append(section_html)
        
        return '\n'.join(content_sections)
    
    def build_project_detail_pages(self, projects):
        """Build individual detail pages for each project."""
        detail_template = self.jinja_env.get_template('details/project-detail.html')
        
        for project in projects:
            # Create project detail directory if it doesn't exist
            project_detail_dir = self.dist_dir / 'projects'
            project_detail_dir.mkdir(exist_ok=True)
            
            # Format date for display
            project_with_formatted_date = project.copy()
            project_with_formatted_date['date'] = self.format_date(project['date'])
            
            # Generate detail page
            html_content = detail_template.render(
                site=self.site_config,
                project=project_with_formatted_date,
            )
            
            # Write individual detail page
            detail_file = project_detail_dir / f"{project['id']}.html"
            detail_file.write_text(html_content, encoding='utf-8')
        
        print(f"Built {len(projects)} project detail pages")

    def build_projects_page(self):
        """Build the projects.html page with all projects."""
        projects = self.get_all_projects()
        
        # Build individual detail pages
        self.build_project_detail_pages(projects)
        
        projects_content = self.render_projects_content(projects)
        
        # Generate hero content for projects page
        hero_content = self.build_hero_content('projects')
        
        # Load and render the projects template
        template = self.jinja_env.get_template('pages/projects.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            projects_content=projects_content,
        )
        
        # Write to projects.html
        output_file = self.dist_dir / 'projects.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built projects.html with {len(projects)} projects")
    
    def render_project_cards_for_home(self, projects):
        """Render project cards for the home page display."""
        template = self.jinja_env.get_template('cards/project-card.html')
        cards_html = []
        
        for project in projects:
            card_html = template.render(
                id=project['id'],
                title=project['title'],
                text=project['text'],
                excerpt=project['excerpt'],
                image=project['image'],
                status=project['metadata'].get('status', 'Unknown'),
            )
            cards_html.append(card_html)
        
        return '\n'.join(cards_html)
    
    def get_all_members(self):
        """Get all members from markdown files."""
        members_dir = self.content_dir / 'members'
        if not members_dir.exists():
            print(f"Warning: {members_dir} directory not found")
            return []
        
        # Set up markdown processor
        md_processor = self.setup_markdown_processor()
        
        # Process all markdown files
        members = []
        for md_file in members_dir.glob('*.md'):
            member_data = self.process_markdown_file(md_file, md_processor)
            if member_data:
                members.append(member_data)
        
        # Sort by name (alphabetical)
        members.sort(key=lambda x: x['title'])
        return members
    
    def build_member_detail_pages(self, members):
        """Build individual detail pages for each member."""
        detail_template = self.jinja_env.get_template('details/member-detail.html')
        
        for member in members:
            # Create member detail directory if it doesn't exist
            member_detail_dir = self.dist_dir / 'members'
            member_detail_dir.mkdir(exist_ok=True)
            
            # Generate detail page
            html_content = detail_template.render(
                site=self.site_config,
                member=member,
            )
            
            # Write individual detail page
            detail_file = member_detail_dir / f"{member['id']}.html"
            detail_file.write_text(html_content, encoding='utf-8')
        
        print(f"Built {len(members)} member detail pages")

    def render_member_cards(self, members):
        """Render member cards for the members page."""
        template = self.jinja_env.get_template('cards/member-card.html')
        cards_html = []
        
        for member in members:
            card_html = template.render(
                id=member['id'],
                name=member['title'],
                role=member['metadata'].get('role', 'Member'),
                skills=member['metadata'].get('skills', []),
                card_text=member['metadata'].get('card-text', 'MEMBER'),
                image=member['metadata'].get('image'),
                metadata=member['metadata'],
            )
            cards_html.append(card_html)
        
        return '\n'.join(cards_html)

    def build_members_page(self):
        """Build the members.html page with all members."""
        members = self.get_all_members()
        
        # Build individual detail pages
        self.build_member_detail_pages(members)
        
        members_content = self.render_member_cards(members)
        
        # Generate hero content for members page
        hero_content = self.build_hero_content('members')
        
        # Load and render the members template
        template = self.jinja_env.get_template('pages/members.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            members_content=members_content,
        )
        
        # Write to members.html
        output_file = self.dist_dir / 'members.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built members.html with {len(members)} members")
    
    def build_about_page(self):
        """Build the about.html page with about content."""
        # Process about content
        about_file = self.content_dir / 'about.md'
        if not about_file.exists():
            print(f"Warning: {about_file} not found")
            about_content = "<p>About content not found.</p>"
        else:
            # Set up markdown processor
            md_processor = self.setup_markdown_processor()
            about_data = self.process_markdown_file(about_file, md_processor)
            about_content = about_data['content'] if about_data else "<p>Error processing about content.</p>"
        
        # Generate hero content for about page
        hero_content = self.build_hero_content('about')
        
        # Load and render the about template
        template = self.jinja_env.get_template('pages/about.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            about_content=about_content,
        )
        
        # Write to about.html
        output_file = self.dist_dir / 'about.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built about.html")

    def build_nextmeeting_page(self):
        """Build the nextmeeting.html page with nextmeeting content."""
        # Process nextmeeting content
        nextmeeting_file = self.content_dir / 'nextmeeting.md'
        if not nextmeeting_file.exists():
            print(f"Warning: {nextmeeting_file} not found")
            nextmeeting_content = "<p>Next meeting content not found.</p>"
        else:
            # Set up markdown processor
            md_processor = self.setup_markdown_processor()
            nextmeeting_data = self.process_markdown_file(nextmeeting_file, md_processor)
            nextmeeting_content = nextmeeting_data['content'] if nextmeeting_data else "<p>Error processing next meeting content.</p>"
        
        # Generate hero content (use nextmeeting title and subtitle from markdown)
        if nextmeeting_data:
            hero_content = {
                'hero_title': nextmeeting_data['title'],
                'hero_subtitle': nextmeeting_data['metadata'].get('subtitle', ''),
                'hero_content': ''
            }
        else:
            hero_content = {
                'hero_title': 'Next Meeting',
                'hero_subtitle': '',
                'hero_content': ''
            }
        
        # Load and render the nextmeeting template
        template = self.jinja_env.get_template('pages/nextmeeting.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            nextmeeting_content=nextmeeting_content
        )
        
        # Write to nextmeeting/index.html
        nextmeeting_dir = self.dist_dir / 'nextmeeting'
        nextmeeting_dir.mkdir(exist_ok=True)
        output_file = nextmeeting_dir / 'index.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built nextmeeting/index.html")
    
    def build_index(self):
        """Build the main index.html file."""
        # Generate news content
        news_content = self.build_whatsnew()
        
        # Generate hero content
        hero_content = self.build_hero_content()
        
        # Generate project cards for home page
        projects = self.get_all_projects()
        projects_content = self.render_project_cards_for_home(projects)
        
        # Load and render the main template
        template = self.jinja_env.get_template('pages/index.html')
        
        # Render the template with all data
        html_content = template.render(
            site=self.site_config,
            news_content=news_content,
            hero=hero_content,
            projects_content=projects_content,
        )
        
        # Write the generated HTML
        output_file = self.dist_dir / 'index.html'
        output_file.write_text(html_content)
        
        print(f"Generated {output_file}")
    
    def copy_assets(self):
        """Copy static assets to output directory."""
        # Copy images
        images_src = self.root_dir / "images"
        images_dest = self.dist_dir / "images"
        if images_src.exists():
            if images_dest.exists():
                shutil.rmtree(images_dest)
            shutil.copytree(images_src, images_dest)
            print(f"Copied images to {images_dest}")
        
        # Copy scripts
        scripts_src = self.root_dir / "scripts"  
        scripts_dest = self.dist_dir / "scripts"
        if scripts_src.exists():
            if scripts_dest.exists():
                shutil.rmtree(scripts_dest)
            shutil.copytree(scripts_src, scripts_dest)
            print(f"Copied scripts to {scripts_dest}")
    
    def copy_css_files(self):
        """Copy CSS files to output/css directory."""
        # Create css directory
        css_dest = self.dist_dir / "css"
        css_dest.mkdir(exist_ok=True)
        
        # Copy CSS files from consolidated css directory
        css_src_dir = self.root_dir / "css"
        
        # Copy shared CSS
        shared_css_src = css_src_dir / "shared.css"
        if shared_css_src.exists():
            shutil.copy2(shared_css_src, css_dest / "shared.css")
            print(f"Copied shared.css to {css_dest}")
        
        # Copy main CSS
        main_css_src = css_src_dir / "main.css"
        if main_css_src.exists():
            shutil.copy2(main_css_src, css_dest / "main.css")
            print(f"Copied main.css to {css_dest}")
        
    
    def build(self):
        """Main build function."""
        print("Building Boston Robot Hackers website...")
        print("Using default design")
        
        # Clean output directory for fresh build
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(exist_ok=True)
        print(f"Cleaned output directory: {self.dist_dir}")
        
        # Copy static assets
        self.copy_assets()
        
        # Copy CSS files to css directory  
        self.copy_css_files()
        
        # Generate syntax highlighting CSS
        self.generate_pygments_css('default')
        
        # Build the main page
        self.build_index()
        
        # Build the news page
        self.build_news_page()
        
        # Build the projects page
        self.build_projects_page()
        
        # Build the members page
        self.build_members_page()
        
        # Build the about page
        self.build_about_page()
        
        # Build the next meeting page
        self.build_nextmeeting_page()
        
        print("Build complete!")


def main():
    """Main entry point."""
    builder = WebsiteBuilder()
    builder.build()


if __name__ == '__main__':
    main()