"""
Page building module for the website builder.
Handles template rendering and page generation.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from jinja2 import Environment

from content_manager import ContentType


class PageBuilder:
    """Handles page building and template rendering."""
    
    def __init__(self, jinja_env: Environment, dist_dir: Path, site_config: Dict):
        self.jinja_env = jinja_env
        self.dist_dir = dist_dir
        self.site_config = site_config
    
    def format_date(self, date_str: str) -> str:
        """Format date string for display."""
        if isinstance(date_str, str):
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime('%B %d, %Y')
            except ValueError:
                return date_str
        return str(date_str)
    
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
            'members': 'member',
            'meetings': 'meeting'
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
    
    def build_page(self, template_name: str, output_filename: str, **context):
        """Generic method to build a page with given template and context."""
        template = self.jinja_env.get_template(template_name)
        
        # Always include site config
        full_context = {'site': self.site_config, **context}
        
        html_content = template.render(**full_context)
        output_file = self.dist_dir / output_filename
        output_file.write_text(html_content, encoding='utf-8')
        
        return output_file