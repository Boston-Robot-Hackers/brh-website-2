"""
Page building module for the website builder.
Handles template rendering and page generation.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from jinja2 import Environment

from content_manager import ContentType, classify_meeting, parse_date
from news_links import build_news_index, resolve_news_html


class PageBuilder:
    """Handles page building and template rendering."""

    def __init__(self, jinja_env: Environment, dist_dir: Path, site_config: Dict):
        self.jinja_env = jinja_env
        self.dist_dir = dist_dir
        self.site_config = site_config
        self._news_map = None
    
    def format_date(self, date_str: str) -> str:
        """Format a canonical ISO date for display (e.g. 'June 11, 2026')."""
        parsed = parse_date(date_str)
        return parsed.strftime('%B %d, %Y') if parsed else ""
    
    def build_detail_pages(self, items: List[Dict], content_type: ContentType, **extra_context):
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
                **extra_context,
            }

            # For meetings, resolve announcement and report links
            if content_type.name == 'meetings':
                ann_html, ann_exists = self.news_html_name(item['metadata'].get('announcement'))
                rep_html, rep_exists = self.news_html_name(item['metadata'].get('report'))
                template_vars[var_name]['announcement_exists'] = ann_exists
                template_vars[var_name]['report_exists'] = rep_exists
                template_vars[var_name]['announcement_html'] = ann_html
                template_vars[var_name]['report_html'] = rep_html

            html_content = detail_template.render(**template_vars)
            detail_file = detail_dir / f"{item['id']}.html"
            detail_file.write_text(html_content, encoding='utf-8')

        print(f"Built {len(items)} {content_type.name} detail pages")

    def news_html_name(self, ref: str):
        """Resolve an announcement/report reference to (html_filename, exists)."""
        if self._news_map is None:
            self._news_map = build_news_index(self.dist_dir.parent / 'content' / 'news')
        return resolve_news_html(self._news_map, ref)

    def check_news_file_exists(self, filename: str) -> bool:
        """Check if a referenced news file resolves to a real news item."""
        return self.news_html_name(filename)[1]
    
    def render_cards(self, items: List[Dict], template_name: str,
                     item_var_name: str = None, **extra_context) -> str:
        """Generic method to render cards using a template."""
        if not items:
            return ""

        template = self.jinja_env.get_template(template_name)
        cards_html = []

        for item in items:
            if item_var_name:
                # Template expects item as a nested object (e.g., project.title)
                context = {
                    item_var_name: item,
                    'formatted_date': self.format_date(item['date']) if item.get('date') else '',
                    **extra_context
                }
            else:
                # Template expects flat properties (e.g., title)
                context = {**item, **extra_context}
                if 'date' in item and item['date']:
                    context['formatted_date'] = self.format_date(item['date'])

            # For meeting cards, resolve announcement/report links and classify
            if 'compact-meeting-card' in template_name and 'metadata' in item:
                ann_html, ann_exists = self.news_html_name(item['metadata'].get('announcement'))
                rep_html, rep_exists = self.news_html_name(item['metadata'].get('report'))
                context['announcement_exists'] = ann_exists
                context['report_exists'] = rep_exists
                context['announcement_html'] = ann_html
                context['report_html'] = rep_html
                context['kind'] = classify_meeting(item['metadata'])

            card_html = template.render(**context)
            cards_html.append(card_html)

        return '\n'.join(cards_html)
    
    def render_news_cards(self, posts: List[Dict[str, Any]]) -> str:
        """Render news cards using the template."""
        # Add image classes to posts for the template
        image_classes = "image-base image-square d-flex align-items-center justify-content-center text-white fw-bold"
        return self.render_cards(posts, 'cards/news-card.html',
                               image_classes=image_classes)
    
    def render_compact_news_cards(self, posts):
        """Render compact news cards for the full news page."""
        return self.render_cards(posts, 'cards/compact-news-card.html')
    
    def render_projects_content(self, projects):
        """Render projects as full content articles using template."""
        return self.render_cards(projects, 'cards/project-listing-item.html', 'project')
    
    def render_project_cards_for_home(self, projects):
        """Render project cards for the home page display."""
        # Add status to each project for the template
        projects_with_status = []
        for project in projects:
            project_copy = project.copy()
            project_copy['status'] = project['metadata'].get('status', 'Unknown')
            projects_with_status.append(project_copy)

        return self.render_cards(projects_with_status, 'cards/project-card.html')
    
    def render_member_cards(self, members, projects_map=None):
        """Render member cards for the members page."""
        members_flattened = []
        for member in members:
            member_copy = member.copy()
            member_copy.update({
                'name': member['title'],
'hashtags': member['metadata'].get('hashtags', []),
                'projects': member['metadata'].get('projects', []),
                'card_text': member['metadata'].get('card-text', 'MEMBER'),
                'image': member['metadata'].get('image'),
            })
            members_flattened.append(member_copy)

        return self.render_cards(members_flattened, 'cards/member-card.html', projects_map=projects_map)

    def group_meetings_by_month(self, meetings: List[Dict]) -> List[Dict]:
        """Group meetings by month, pairing main and hands-on meetings."""
        from collections import defaultdict

        month_groups = defaultdict(lambda: {'main': None, 'handson': None})

        for meeting in meetings:
            date_obj = parse_date(meeting['metadata'].get('date'))
            if date_obj is None:
                continue

            month_key = date_obj.strftime('%Y-%m')
            month_label = date_obj.strftime('%B %Y')

            # Determine if main or hands-on
            slot = classify_meeting(meeting['metadata'])
            if month_groups[month_key][slot] is not None:
                existing = month_groups[month_key][slot].get('id', '?')
                print(f"Warning: month {month_key} already has a '{slot}' meeting "
                      f"('{existing}'); '{meeting.get('id', '?')}' will overwrite it "
                      f"on the meetings page")
            month_groups[month_key][slot] = meeting

            month_groups[month_key]['label'] = month_label
            month_groups[month_key]['sort_key'] = month_key

        # Convert to sorted list (newest month first)
        grouped = []
        for month_key in sorted(month_groups.keys(), reverse=True):
            group = month_groups[month_key]
            grouped.append({
                'month_label': group['label'],
                'main_meeting': group['main'],
                'handson_meeting': group['handson'],
                'sort_key': group['sort_key']
            })

        return grouped

    def render_monthly_meeting_cards(self, meetings: List[Dict]) -> str:
        """Render meetings grouped by month."""
        if not meetings:
            return ""

        grouped = self.group_meetings_by_month(meetings)
        template = self.jinja_env.get_template('cards/monthly-meeting-card.html')
        cards_html = []

        for group in grouped:
            context = {
                'month_label': group['month_label'],
                'main_meeting': group['main_meeting'],
                'handson_meeting': group['handson_meeting'],
            }

            # Resolve announcement/report links for main meeting
            if group['main_meeting']:
                ann_html, ann_exists = self.news_html_name(
                    group['main_meeting']['metadata'].get('announcement'))
                rep_html, rep_exists = self.news_html_name(
                    group['main_meeting']['metadata'].get('report'))
                context['main_announcement_exists'] = ann_exists
                context['main_report_exists'] = rep_exists
                context['main_announcement_html'] = ann_html
                context['main_report_html'] = rep_html
            else:
                context['main_announcement_exists'] = False
                context['main_report_exists'] = False
                context['main_announcement_html'] = ''
                context['main_report_html'] = ''

            card_html = template.render(**context)
            cards_html.append(card_html)

        return '\n'.join(cards_html)

    def render_upcoming_meetings_calendar(self, meetings: List[Dict]) -> str:
        """Render upcoming meetings in calendar format for home page."""
        if not meetings:
            return ""

        from datetime import datetime, date

        today = date.today()
        upcoming = []

        # Filter and format meetings
        for meeting in meetings:
            parsed = parse_date(meeting['metadata'].get('date'))
            if parsed is None:
                continue
            date_obj = parsed.date()

            if date_obj < today:
                continue

            # Determine meeting type label
            title = meeting.get('title', '')
            if classify_meeting(meeting['metadata']) == 'handson':
                type_label = 'Hands-On Meeting'
            else:
                type_label = 'Main Meeting'

            # Build announcement URL if it resolves to a real news item
            ann_html, ann_exists = self.news_html_name(meeting['metadata'].get('announcement'))
            announcement_url = f'news/{ann_html}' if ann_exists else ''

            # Format for template
            upcoming.append({
                'date_obj': date_obj,
                'day': date_obj.strftime('%d'),
                'month_abbr': date_obj.strftime('%b'),
                'year': date_obj.strftime('%Y'),
                'month_year': date_obj.strftime('%b %Y'),
                'time': meeting['metadata'].get('time', ''),
                'type_label': type_label,
                'text': meeting['metadata'].get('text', ''),
                'title': title,
                'announcement_url': announcement_url,
            })

        # Sort by date
        upcoming.sort(key=lambda x: x['date_obj'])

        # Render template
        template = self.jinja_env.get_template('components/upcoming-meetings-calendar.html')
        return template.render(meetings=upcoming)

    def build_page(self, template_name: str, output_filename: str, **context):
        """Generic method to build a page with given template and context."""
        template = self.jinja_env.get_template(template_name)
        
        # Always include site config
        full_context = {'site': self.site_config, **context}
        
        html_content = template.render(**full_context)
        output_file = self.dist_dir / output_filename
        output_file.write_text(html_content, encoding='utf-8')
        
        return output_file