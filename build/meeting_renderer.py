"""
Meeting renderer module for the website builder.
Handles rendering of meeting-related templates and calendars.
"""

from datetime import datetime, date
from pathlib import Path
from typing import List, Dict

from jinja2 import Environment


class MeetingRenderer:
    """Renders meeting-related templates for the website."""

    def __init__(self, jinja_env: Environment, dist_dir: Path):
        self.jinja_env = jinja_env
        self.dist_dir = dist_dir

    def check_news_file_exists(self, filename: str) -> bool:
        """Check if a news file exists in the content directory."""
        if not filename:
            return False
        news_file = self.dist_dir.parent / 'content' / 'news' / filename
        return news_file.exists()

    def group_meetings_by_month(self, meetings: List[Dict]) -> List[Dict]:
        """Group meetings by month, pairing main and hands-on meetings."""
        from collections import defaultdict

        month_groups = defaultdict(lambda: {'main': None, 'handson': None})

        for meeting in meetings:
            date_str = meeting['metadata'].get('date', '')
            if not date_str:
                continue

            for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d']:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    month_key = date_obj.strftime('%Y-%m')
                    month_label = date_obj.strftime('%B %Y')

                    title = meeting.get('title', '')
                    if 'Hands On' in title or 'Hands-On' in title or 'handson' in title.lower():
                        month_groups[month_key]['handson'] = meeting
                    else:
                        month_groups[month_key]['main'] = meeting

                    month_groups[month_key]['label'] = month_label
                    month_groups[month_key]['sort_key'] = month_key
                    break
                except ValueError:
                    continue

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

            if group['main_meeting']:
                context['main_announcement_exists'] = self.check_news_file_exists(
                    group['main_meeting']['metadata'].get('announcement')
                )
                context['main_report_exists'] = self.check_news_file_exists(
                    group['main_meeting']['metadata'].get('report')
                )
            else:
                context['main_announcement_exists'] = False
                context['main_report_exists'] = False

            card_html = template.render(**context)
            cards_html.append(card_html)

        return '\n'.join(cards_html)

    def render_upcoming_meetings_calendar(self, meetings: List[Dict]) -> str:
        """Render upcoming meetings in calendar format for home page."""
        if not meetings:
            return ""

        today = date.today()
        upcoming = []

        for meeting in meetings:
            date_str = meeting['metadata'].get('date', '')
            if not date_str:
                continue

            date_obj = None
            for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d']:
                try:
                    date_obj = datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue

            if not date_obj or date_obj < today:
                continue

            title = meeting.get('title', '')
            if 'Hands On' in title or 'Hands-On' in title or 'handson' in title.lower():
                type_label = 'Hands-On Meeting'
            else:
                type_label = 'Main Meeting'

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
            })

        upcoming.sort(key=lambda x: x['date_obj'])

        template = self.jinja_env.get_template('components/upcoming-meetings-calendar.html')
        return template.render(meetings=upcoming)
