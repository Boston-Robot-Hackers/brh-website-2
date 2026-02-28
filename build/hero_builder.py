"""
Hero content builder module for the website builder.
Handles generation of dynamic hero section content.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import frontmatter
import yaml


class HeroBuilder:
    """Builds dynamic hero section content from meeting data."""

    def __init__(self, content_dir: Path):
        self.content_dir = content_dir

    def generate_index_hero(self, static_content: str) -> str:
        """Generate index hero by adding future meeting info to static content."""
        if '<hr/>' not in static_content and '<hr>' not in static_content:
            return static_content

        split_on = '<hr/>' if '<hr/>' in static_content else '<hr>'
        parts = static_content.split(split_on, 1)
        static_part = parts[0] + split_on

        future_meetings = self.get_future_meetings()
        generated_part = self.format_future_meetings_section(future_meetings)

        return static_part + '\n' + generated_part

    def get_future_meetings(self) -> List[Dict[str, Any]]:
        """Get all meetings with dates in the future, sorted by date ascending."""
        meetings_dir = self.content_dir / 'meetings'
        if not meetings_dir.exists():
            return []

        today = datetime.now().date()
        future_meetings = []

        for md_file in meetings_dir.glob('*.md'):
            try:
                post = frontmatter.load(md_file)
                metadata = post.metadata
                date_str = metadata.get('date', '')

                if not date_str:
                    continue

                try:
                    meeting_date = datetime.strptime(str(date_str), '%m/%d/%Y').date()
                except ValueError:
                    try:
                        meeting_date = datetime.strptime(str(date_str), '%Y-%m-%d').date()
                    except ValueError:
                        continue

                if meeting_date >= today:
                    future_meetings.append({
                        'metadata': metadata,
                        'date_obj': meeting_date,
                        'title': metadata.get('title', '')
                    })

            except (OSError, ValueError, yaml.YAMLError) as e:
                print(f"Error processing {md_file}: {e}")
                continue

        future_meetings.sort(key=lambda x: x['date_obj'])
        return future_meetings

    def format_future_meetings_section(self, meetings: List[Dict[str, Any]]) -> str:
        """Format the 2 nearest future meetings for the hero section."""
        if not meetings:
            return "<p><em>No upcoming meetings scheduled</em></p>"

        nearest_meetings = meetings[:2]
        meeting_parts = []

        for meeting in nearest_meetings:
            metadata = meeting['metadata']
            title = meeting['title']

            is_handson = 'Hands On' in title or 'Hands-On' in title
            label = "Next Hands-On Meeting" if is_handson else "Next Main Meeting"

            date = metadata.get('date', '')
            time = metadata.get('time', '')
            announcement = metadata.get('announcement', '')

            datetime_str = f"{date} at {time}" if date and time else date or time or ''

            if announcement:
                news_dir = self.content_dir / 'news'
                announcement_file = news_dir / announcement
                if announcement_file.exists():
                    link_href = f"news/{announcement.replace('.md', '.html')}"
                    meeting_link = f'<a href="{link_href}">{datetime_str}</a>'
                else:
                    meeting_link = datetime_str
            else:
                meeting_link = datetime_str

            meeting_parts.append(f"<strong>{label}:</strong> {meeting_link}")

        result = "<p>" + " | ".join(meeting_parts) + "</p>"
        return result

    def format_single_meeting_for_hero(self, label: str, meeting: Dict) -> str:
        """Format a single meeting entry for the hero section."""
        date = meeting.get('date', '')
        time = meeting.get('time', '')
        location = meeting.get('location', '')
        announcement = meeting.get('announcement', '')

        datetime_str = f"{date} at {time}" if date and time else date or time or ''

        if announcement:
            news_dir = self.content_dir / 'news'
            announcement_file = news_dir / announcement
            if announcement_file.exists():
                link_href = f"news/{announcement.replace('.md', '.html')}"
                meeting_link = f'<a href="{link_href}">{datetime_str}</a>'
            else:
                meeting_link = datetime_str
        else:
            meeting_link = datetime_str

        result = f"<p><strong>{label}:</strong> {meeting_link}"
        if location:
            result += f" at <a href='https://www.artisansasylum.com' target='_blank'>{location}</a>"
        result += "</p>"

        return result

    def load_meeting_info(self, filename: str) -> Dict[str, Any]:
        """Load meeting info from a meeting file."""
        meeting_file = self.content_dir / 'meetings' / filename
        if not meeting_file.exists():
            return None

        try:
            post = frontmatter.load(meeting_file)
            return post.metadata
        except (OSError, yaml.YAMLError) as e:
            print(f"Error loading {filename}: {e}")
            return None

    def format_meeting_section(self, nextmeeting: Dict, nexthandson: Dict) -> str:
        """Format the meeting info section for the hero."""
        sections = []

        if nextmeeting:
            sections.append(self.format_single_meeting("Next Meeting", nextmeeting))

        if nexthandson:
            sections.append(self.format_single_meeting("Next Hands-On Meeting", nexthandson))

        return '\n\n'.join(sections)

    def format_single_meeting(self, label: str, meeting: Dict) -> str:
        """Format a single meeting entry."""
        date = meeting.get('date', '')
        time = meeting.get('time', '')
        location = meeting.get('location', '')
        announcement = meeting.get('announcement', '')

        datetime_str = f"{date} at {time}" if date and time else date or time or ''

        if announcement:
            news_dir = self.content_dir / 'news'
            announcement_file = news_dir / announcement
            if announcement_file.exists():
                link_href = f"news/{announcement.replace('.md', '.html')}"
                meeting_link = f'<a href="{link_href}">{datetime_str}</a>'
            else:
                meeting_link = datetime_str
        else:
            meeting_link = '<em>coming soon</em>'

        result = f"<p><strong>{label}:</strong> {meeting_link}"
        if location and announcement:
            result += f" at {location}"
        result += "</p>"

        return result
