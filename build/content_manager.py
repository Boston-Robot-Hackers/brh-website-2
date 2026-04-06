"""
Content management module for the website builder.
Handles loading and processing of markdown content.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import frontmatter
import markdown


def parse_date(date_str):
    """Parse a date string trying common formats. Returns datetime or None."""
    if not date_str:
        return None
    for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%d/%m/%Y']:
        try:
            return datetime.strptime(str(date_str), fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
    except ValueError:
        return None


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


class ContentManager:
    """Manages content loading and processing."""
    
    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
    
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
    
    def process_markdown_file(self, file_path: Path, md_processor=None) -> Dict[str, Any]:
        """Process a single markdown file and return structured data."""
        if md_processor is None:
            md_processor = self.setup_markdown_processor()

        try:
            post = frontmatter.load(file_path)
            html_content = md_processor.convert(post.content)
            metadata = post.metadata

            # Normalize date field from frontmatter
            if 'date' in metadata:
                if isinstance(metadata['date'], datetime):
                    metadata['date'] = metadata['date'].isoformat()
                elif hasattr(metadata['date'], 'isoformat'):
                    metadata['date'] = metadata['date'].isoformat()
                elif isinstance(metadata['date'], str):
                    metadata['date'] = metadata['date']
            else:
                metadata['date'] = None

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
        if content_type.sort_key == 'order':
            # For order field, default to 0 if not present, so items without order come first
            items.sort(key=lambda x: x['metadata'].get('order', 0), reverse=content_type.reverse)
        else:
            items.sort(key=lambda x: x[content_type.sort_key] or '', reverse=content_type.reverse)
        return items

    def generate_index_hero(self, static_content: str) -> str:
        """Generate index hero by adding future meeting info to static content."""
        if '<hr/>' not in static_content and '<hr>' not in static_content:
            return static_content

        split_on = '<hr/>' if '<hr/>' in static_content else '<hr>'
        parts = static_content.split(split_on, 1)
        static_part = parts[0] + split_on

        # Get all future meetings
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

                # Parse the date (format: MM/DD/YYYY)
                try:
                    meeting_date = datetime.strptime(str(date_str), '%m/%d/%Y').date()
                except ValueError:
                    # Try alternative format
                    try:
                        meeting_date = datetime.strptime(str(date_str), '%Y-%m-%d').date()
                    except ValueError:
                        continue

                # Only include future meetings
                if meeting_date >= today:
                    future_meetings.append({
                        'metadata': metadata,
                        'date_obj': meeting_date,
                        'title': metadata.get('title', '')
                    })

            except Exception as e:
                print(f"Error processing {md_file}: {e}")
                continue

        # Sort by date ascending (nearest first)
        future_meetings.sort(key=lambda x: x['date_obj'])
        return future_meetings

    def format_future_meetings_section(self, meetings: List[Dict[str, Any]]) -> str:
        """Format the 2 nearest future meetings for the hero section."""
        if not meetings:
            return "<p><em>No upcoming meetings scheduled</em></p>"

        # Only show the 2 nearest meetings
        nearest_meetings = meetings[:2]

        meeting_parts = []

        for meeting in nearest_meetings:
            metadata = meeting['metadata']
            title = meeting['title']

            # Determine if it's a hands-on meeting
            is_handson = 'Hands On' in title or 'Hands-On' in title
            label = "Next Hands-On Meeting" if is_handson else "Next Main Meeting"

            # Format the meeting
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

        # Combine both meetings on one line without location
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
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def format_meeting_section(self, nextmeeting: Dict, nexthandson: Dict) -> str:
        """Format the meeting info section for the hero."""
        sections = []

        if nextmeeting:
            section = self.format_single_meeting(
                "Next Meeting",
                nextmeeting
            )
            sections.append(section)

        if nexthandson:
            section = self.format_single_meeting(
                "Next Hands-On Meeting",
                nexthandson
            )
            sections.append(section)

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
    
    def build_hero_content(self, page_name: str = 'index') -> Dict[str, Any]:
        """Build hero content from page-specific markdown file."""
        hero_file = self.content_dir / 'heroes' / f'{page_name}.md'
        if not hero_file.exists():
            print(f"Warning: {hero_file} not found, leaving hero section blank")
            return {'hero_title': '', 'hero_subtitle': '', 'hero_content': ''}

        md_processor = self.setup_markdown_processor()
        hero_data = self.process_markdown_file(hero_file, md_processor)

        if not hero_data:
            print(f"Warning: Failed to process {hero_file}, leaving hero section blank")
            return {'hero_title': '', 'hero_subtitle': '', 'hero_content': ''}

        hero_content = hero_data['content']

        if page_name == 'index':
            hero_content = self.generate_index_hero(hero_content)

        return {
            'hero_title': hero_data['title'],
            'hero_subtitle': hero_data['metadata'].get('subtitle', ''),
            'hero_content': hero_content
        }
    
    def process_single_content_file(self, filename: str) -> str:
        """Process a single content file and return HTML content."""
        content_file = self.content_dir / filename
        if not content_file.exists():
            print(f"Warning: {content_file} not found")
            return f"<p>{filename} content not found.</p>"
        
        md_processor = self.setup_markdown_processor()
        content_data = self.process_markdown_file(content_file, md_processor)
        return content_data['content'] if content_data else f"<p>Error processing {filename} content.</p>"