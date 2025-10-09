"""
Content management module for the website builder.
Handles loading and processing of markdown content.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import frontmatter
import markdown


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

            # Handle date field - prefer frontmatter date over filename
            if 'date' in metadata:
                if isinstance(metadata['date'], datetime):
                    metadata['date'] = metadata['date'].isoformat()
                elif hasattr(metadata['date'], 'isoformat'):
                    metadata['date'] = metadata['date'].isoformat()
                elif isinstance(metadata['date'], str):
                    metadata['date'] = metadata['date']
            else:
                date_str = file_path.stem[:10]
                try:
                    metadata['date'] = datetime.strptime(date_str, '%Y-%m-%d').date().isoformat()
                except ValueError:
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
            items.sort(key=lambda x: x[content_type.sort_key], reverse=content_type.reverse)
        return items
    
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
    
    def process_single_content_file(self, filename: str) -> str:
        """Process a single content file and return HTML content."""
        content_file = self.content_dir / filename
        if not content_file.exists():
            print(f"Warning: {content_file} not found")
            return f"<p>{filename} content not found.</p>"
        
        md_processor = self.setup_markdown_processor()
        content_data = self.process_markdown_file(content_file, md_processor)
        return content_data['content'] if content_data else f"<p>Error processing {filename} content.</p>"