#!/usr/bin/env python3
"""
Build script for Boston Robot Hackers website.
Uses template-based architecture with refactored common patterns.
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


class ContentType:
    """Configuration for different content types."""
    def __init__(self, name: str, directory: str, sort_key: str = 'date', 
                 reverse: bool = True, detail_template: str = None,
                 page_template: str = None, output_filename: str = None):
        self.name = name
        self.directory = directory
        self.sort_key = sort_key
        self.reverse = reverse
        self.detail_template = detail_template or f'details/{name}-detail.html'
        self.page_template = page_template or f'pages/{name}.html'
        self.output_filename = output_filename or f'{name}.html'


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
        
        # Set up Jinja2 environment
        template_paths = [str(self.templates_dir)]
        self.jinja_env = Environment(loader=FileSystemLoader(template_paths))
        
        # Define content types
        self.content_types = {
            'news': ContentType('news', 'news', output_filename='whatsnew.html', 
                              page_template='pages/whatsnew.html', 
                              detail_template='details/news-detail.html'),
            'projects': ContentType('projects', 'projects',
                                  detail_template='details/project-detail.html'),
            'members': ContentType('members', 'members', sort_key='title', reverse=False,
                                 detail_template='details/member-detail.html'),
            'meetings': ContentType('meetings', 'meetings', output_filename='meetings.html',
                                  page_template='pages/meetings.html',
                                  detail_template='details/meeting-detail.html'),
        }
    
    def load_site_config(self) -> Dict[str, Any]:
        """Load site configuration."""
        config_file = self.config_dir / "site.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        return {}
    
    def setup_markdown_processor(self):
        """Set up markdown processor with syntax highlighting."""
        return markdown.Markdown(
            extensions=['codehilite', 'fenced_code', 'tables', 'toc'],
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
        
        css_dir = self.dist_dir / 'css'
        css_dir.mkdir(exist_ok=True)
        
        css_file = css_dir / 'syntax.css'
        css_file.write_text(css_content)
        print(f"Generated syntax highlighting CSS: {css_file}")
    
    def process_markdown_file(self, file_path: Path, md_processor) -> Dict[str, Any]:
        """Process a single markdown file and return structured data."""
        try:
            post = frontmatter.load(file_path)
            html_content = md_processor.convert(post.content)
            metadata = post.metadata
            
            # Parse date from filename if not in front matter
            if 'date' not in metadata:
                date_str = file_path.stem[:10]
                try:
                    metadata['date'] = datetime.strptime(date_str, '%Y-%m-%d').date().isoformat()
                except ValueError:
                    metadata['date'] = datetime.now().date().isoformat()
            elif isinstance(metadata['date'], datetime):
                metadata['date'] = metadata['date'].isoformat()
            elif hasattr(metadata['date'], 'isoformat'):
                metadata['date'] = metadata['date'].isoformat()
            
            return {
                'id': file_path.stem,
                'title': metadata.get('title', metadata.get('name', 'Untitled')),
                'date': metadata.get('date'),
                'image': metadata.get('image', ''),
                'text': metadata.get('text', metadata.get('emoji')),
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
    
    # REFACTORED COMMON METHODS
    
    def get_all_content(self, content_type: ContentType) -> List[Dict[str, Any]]:
        """Generic method to get all content of a given type."""
        content_dir = self.content_dir / content_type.directory
        if not content_dir.exists():
            print(f"Warning: {content_dir} directory not found")
            return []
        
        md_processor = self.setup_markdown_processor()
        items = []
        
        for md_file in content_dir.glob('*.md'):
            item_data = self.process_markdown_file(md_file, md_processor)
            if item_data:
                items.append(item_data)
        
        # Sort by specified key
        items.sort(key=lambda x: x[content_type.sort_key], reverse=content_type.reverse)
        return items
    
    def build_detail_pages(self, items: List[Dict], content_type: ContentType):
        """Generic method to build detail pages."""
        if not items:
            return
            
        detail_template = self.jinja_env.get_template(content_type.detail_template)
        detail_dir = self.dist_dir / content_type.directory
        detail_dir.mkdir(exist_ok=True)
        
        # Map content type to expected template variable name
        template_var_map = {
            'news': 'post',
            'projects': 'project', 
            'members': 'member'
        }
        
        for item in items:
            # Format date if it exists
            item_with_formatted_date = item.copy()
            if 'date' in item and item['date']:
                item_with_formatted_date['date'] = self.format_date(item['date'])
            
            # Use correct variable name for templates
            var_name = template_var_map.get(content_type.name, content_type.name[:-1])
            template_vars = {
                'site': self.site_config,
                var_name: item_with_formatted_date,
            }
            
            html_content = detail_template.render(**template_vars)
            detail_file = detail_dir / f"{item['id']}.html"
            detail_file.write_text(html_content, encoding='utf-8')
        
        print(f"Built {len(items)} {content_type.name} detail pages")
    
    def render_cards(self, items: List[Dict], template_name: str, **extra_context) -> str:
        """Generic method to render cards using a template."""
        if not items:
            return ""
            
        template = self.jinja_env.get_template(template_name)
        cards_html = []
        
        for item in items:
            context = {**item, **extra_context}
            if 'date' in item and item['date']:
                context['formatted_date'] = self.format_date(item['date'])
            
            card_html = template.render(**context)
            cards_html.append(card_html)
        
        return '\n'.join(cards_html)
    
    def build_content_page(self, content_type: ContentType, extra_context: Dict = None):
        """Generic method to build any content page."""
        print(f"Building {content_type.name} page...")
        
        # Get content
        items = self.get_all_content(content_type)
        
        # Build detail pages
        self.build_detail_pages(items, content_type)
        
        # Generate hero content
        hero_content = self.build_hero_content(content_type.name)
        
        # Prepare template context
        template_context = {
            'site': self.site_config,
            'hero': hero_content,
        }
        
        # Add extra context if provided
        if extra_context:
            template_context.update(extra_context)
        
        # Load and render template
        template = self.jinja_env.get_template(content_type.page_template)
        html_content = template.render(**template_context)
        
        # Write output file
        output_file = self.dist_dir / content_type.output_filename
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built {content_type.output_filename} with {len(items)} {content_type.name}")
        
        return items
    
    def copy_directory(self, src_name: str, dest_name: str = None):
        """Generic method to copy a directory."""
        dest_name = dest_name or src_name
        src_path = self.root_dir / src_name
        dest_path = self.dist_dir / dest_name
        
        if src_path.exists():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"Copied {src_name} to {dest_path}")
    
    # ORIGINAL SPECIALIZED METHODS (kept for specific logic)
    
    def build_hero_content(self, page_name: str = 'index') -> Dict[str, Any]:
        """Build hero content from page-specific markdown file."""
        hero_file = self.content_dir / 'heroes' / f'{page_name}.md'
        if not hero_file.exists():
            print(f"Warning: {hero_file} not found, leaving hero section blank")
            return {'hero_title': '', 'hero_subtitle': '', 'hero_content': ''}
        
        md_processor = self.setup_markdown_processor()
        hero_data = self.process_markdown_file(hero_file, md_processor)
        
        if hero_data:
            return {
                'hero_title': hero_data['title'],
                'hero_subtitle': hero_data['metadata'].get('subtitle', ''),
                'hero_content': hero_data['content']
            }
        
        print(f"Warning: Failed to process {hero_file}, leaving hero section blank")
        return {'hero_title': '', 'hero_subtitle': '', 'hero_content': ''}
    
    def build_whatsnew(self) -> str:
        """Build the What's New section from markdown files (highlighted only)."""
        posts = self.get_all_content(self.content_types['news'])
        highlighted_posts = [post for post in posts if post['metadata'].get('highlight', False)]
        
        news_html = self.render_cards(highlighted_posts, 'cards/news-card.html')
        print(f"Generated {len(highlighted_posts)} highlighted posts from {len(posts)} total")
        return news_html
    
    def build_news_page(self):
        """Build the whatsnew.html page with all news items."""
        posts = self.get_all_content(self.content_types['news'])
        self.build_detail_pages(posts, self.content_types['news'])
        
        news_content = self.render_cards(posts, 'cards/compact-news-card.html')
        hero_content = self.build_hero_content('whatsnew')
        
        context = {'news_content': news_content}
        template = self.jinja_env.get_template('pages/whatsnew.html')
        
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            news_content=news_content
        )
        
        output_file = self.dist_dir / 'whatsnew.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built whatsnew.html with {len(posts)} posts")
    
    def build_projects_page(self):
        """Build projects page using refactored method."""
        projects = self.get_all_content(self.content_types['projects'])
        self.build_detail_pages(projects, self.content_types['projects'])
        
        # Render projects content using specific template that expects 'project' variable
        template = self.jinja_env.get_template('cards/project-listing-item.html')
        projects_content_sections = []
        
        for project in projects:
            section_html = template.render(
                project=project,
                formatted_date=self.format_date(project['date'])
            )
            projects_content_sections.append(section_html)
        
        projects_content = '\n'.join(projects_content_sections)
        
        hero_content = self.build_hero_content('projects')
        page_template = self.jinja_env.get_template('pages/projects.html')
        
        html_content = page_template.render(
            site=self.site_config,
            hero=hero_content,
            projects_content=projects_content
        )
        
        output_file = self.dist_dir / 'projects.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built projects.html with {len(projects)} projects")
    
    def build_members_page(self):
        """Build members page using refactored method."""
        members = self.get_all_content(self.content_types['members'])
        self.build_detail_pages(members, self.content_types['members'])
        
        # Render member cards using specific template that expects member variables
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
        
        members_content = '\n'.join(cards_html)
        hero_content = self.build_hero_content('members')
        
        page_template = self.jinja_env.get_template('pages/members.html')
        html_content = page_template.render(
            site=self.site_config,
            hero=hero_content,
            members_content=members_content
        )
        
        output_file = self.dist_dir / 'members.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built members.html with {len(members)} members")
    
    def build_about_page(self):
        """Build the about.html page with about content."""
        about_file = self.content_dir / 'about.md'
        if not about_file.exists():
            print(f"Warning: {about_file} not found")
            about_content = "<p>About content not found.</p>"
        else:
            md_processor = self.setup_markdown_processor()
            about_data = self.process_markdown_file(about_file, md_processor)
            about_content = about_data['content'] if about_data else "<p>Error processing about content.</p>"
        
        hero_content = self.build_hero_content('about')
        template = self.jinja_env.get_template('pages/about.html')
        
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            about_content=about_content,
        )
        
        output_file = self.dist_dir / 'about.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built about.html")
    
    def build_nextmeeting_page(self):
        """Build the nextmeeting.html page with nextmeeting content."""
        nextmeeting_file = self.content_dir / 'nextmeeting.md'
        if not nextmeeting_file.exists():
            print(f"Warning: {nextmeeting_file} not found")
            nextmeeting_content = "<p>Next meeting content not found.</p>"
            hero_content = {'hero_title': 'Next Meeting', 'hero_subtitle': '', 'hero_content': ''}
        else:
            md_processor = self.setup_markdown_processor()
            nextmeeting_data = self.process_markdown_file(nextmeeting_file, md_processor)
            nextmeeting_content = nextmeeting_data['content'] if nextmeeting_data else "<p>Error processing next meeting content.</p>"
            
            if nextmeeting_data:
                hero_content = {
                    'hero_title': nextmeeting_data['title'],
                    'hero_subtitle': nextmeeting_data['metadata'].get('subtitle', ''),
                    'hero_content': ''
                }
            else:
                hero_content = {'hero_title': 'Next Meeting', 'hero_subtitle': '', 'hero_content': ''}
        
        template = self.jinja_env.get_template('pages/nextmeeting.html')
        html_content = template.render(
            site=self.site_config,
            hero=hero_content,
            nextmeeting_content=nextmeeting_content
        )
        
        nextmeeting_dir = self.dist_dir / 'nextmeeting'
        nextmeeting_dir.mkdir(exist_ok=True)
        output_file = nextmeeting_dir / 'index.html'
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Built nextmeeting/index.html")
    
    def render_project_cards_for_home(self, projects):
        """Render project cards for the home page display."""
        return self.render_cards(projects, 'cards/project-card.html')
    
    def build_index(self):
        """Build the main index.html file."""
        news_content = self.build_whatsnew()
        hero_content = self.build_hero_content()
        
        projects = self.get_all_content(self.content_types['projects'])
        projects_content = self.render_project_cards_for_home(projects)
        
        template = self.jinja_env.get_template('pages/index.html')
        html_content = template.render(
            site=self.site_config,
            news_content=news_content,
            hero=hero_content,
            projects_content=projects_content,
        )
        
        output_file = self.dist_dir / 'index.html'
        output_file.write_text(html_content)
        print(f"Generated {output_file}")
    
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
        self.copy_css_files()
        
        # Generate syntax highlighting CSS
        self.generate_pygments_css('default')
        
        # Build pages
        self.build_index()
        self.build_news_page()
        self.build_projects_page()
        self.build_members_page()
        self.build_about_page()
        self.build_nextmeeting_page()
        
        print("Build complete!")


def main():
    """Main entry point."""
    builder = WebsiteBuilder()
    builder.build()


if __name__ == '__main__':
    main()