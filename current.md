# Current State - Boston Robot Hackers Website

**Date**: January 30, 2026
**Context**: Completed home page meetings calendar redesign. Code needs refactoring to fix rules.md violations.

## Current Todo List
⚠️ **PENDING** - Rules.md compliance refactoring needed (see detailed instructions below)

## Project Status

### ✅ Recently Completed Work (January 2026)
- **Home Page Calendar Redesign**: Replaced monthly meeting cards with calendar-style table
  - Shows only upcoming meetings (future dates only)
  - Clean date column (day, month/year, time) + meeting details column
  - Added "view all meetings" link
  - Created new `templates/components/upcoming-meetings-calendar.html`
  - Added `render_upcoming_meetings_calendar()` method to PageBuilder

### ✅ Previous Work (September 2025)
- **Meetings Functionality**: Full implementation of meetings content type with templates and processing
- **Build System Refactoring**: Moved from monolithic to modular architecture
- **File Cleanup**: Renamed build scripts, removed obsolete documentation
- **UI Improvements**: Two-column whatsnew page, meeting card styling with borders

### 🏗️ Current Architecture

**Build System** (Modular - Currently Active):
- `build/build.py` - Main orchestrator (222 lines)
- `build/content_manager.py` - Content loading/processing (333 lines) ⚠️ EXCEEDS 300 LINE LIMIT
- `build/page_builder.py` - Template rendering (316 lines) ⚠️ EXCEEDS 300 LINE LIMIT
- `build/asset_manager.py` - Static asset management (65 lines)
- `archive/build.py` - Original version (archived for reference)

**Content Structure**:
- `content/news/` - 6 news posts (3 highlighted)
- `content/meetings/` - 3 meetings with image support
- `content/projects/` - 7 projects
- `content/members/` - 11 members
- `content/heroes/` - Hero content for each page type

**Templates**:
- Pages: index, whatsnew, meetings, projects, members, about
- Cards: news-card, compact-news-card, compact-meeting-card, monthly-meeting-card, project-card, member-card
- Components: upcoming-meetings-calendar (new - table-style calendar for home page)
- Details: news-detail, meeting-detail, project-detail, member-detail

### 🎯 Current Features
- **Home page upcoming meetings calendar**: Table-style display showing future meetings only
  - Date column: Day, month/year, time
  - Details column: Meeting type, description/blurb
  - Link to full meetings page
- **Two-column whatsnew page**: News (7/12 width) + Recent Meetings (5/12 width)
- **Meeting cards**: Monthly grouped cards with announcement/report links
- **Image frontmatter support**: Meetings can specify image paths
- **Redirect system**: `/nextmeeting/` → `/meetings/nextmeeting.html`
- **Responsive design**: Bootstrap-based, mobile-friendly
- **Auto-deployment**: GitHub Actions builds and deploys on push

### ⚠️ Current Warnings/Issues
- Missing `content/heroes/meetings.md` - causes warning but build succeeds with blank hero
- Build always shows "Warning: content/heroes/meetings.md not found"

### 🔧 Technical State
- **Dependencies**: All managed via `uv` with `build/pyproject.toml`
- **Build Command**: `uv run python build/build.py`
- **Test Command**: `cd output && python -m http.server 8000`
- **Git Status**: Clean working tree, all changes pushed to `origin/main`
- **Deploy Status**: GitHub Actions configured and working

## Potential Next Steps (No immediate action needed)

### 🔍 Minor Improvements
1. **Create meetings hero**: Add `content/heroes/meetings.md` to remove warning
2. **Meeting navigation**: Consider adding meetings link to main navigation
3. **Image optimization**: Could add image resizing/optimization to build process
4. **Meeting archives**: Consider date-based organization for older meetings

### 🚀 Future Enhancements
1. **Search functionality**: Add client-side search across content
2. **RSS feeds**: Generate RSS/Atom feeds for news and meetings
3. **Event calendar**: Integration with calendar services
4. **Member profiles**: Enhanced member pages with more details
5. **Project status tracking**: Visual indicators for project status

### 📋 Code Quality Notes
- ✅ All methods under 50 lines (rules.md compliant)
- ❌ **2 files exceed 300 lines** (content_manager.py: 333, page_builder.py: 316)
- ❌ **ContentType.__init__() has 6 parameters** (max 3 allowed)
- ❌ **6 functions use default parameters** (not allowed by rules.md)
- ❌ **3 bare Exception handlers** (should be specific exceptions)
- ✅ No duplicate code (DRY principle followed)
- ✅ Modular architecture with single responsibility
- ✅ Type hints partially implemented
- ✅ No HTML/CSS in Python files

**See "Rules Violations to Fix" section below for detailed refactoring instructions.**

## 🔧 Rules Violations to Fix

### Overview
The codebase has 4 types of violations against `rules.md`:
1. Two files exceed 300 line limit
2. One function has too many parameters
3. Six functions use default parameters
4. Three functions use bare Exception handlers

### VIOLATION 1: File Length Violations

#### A. content_manager.py (333 lines → target: ~250 lines)

**Problem**: File is 33 lines over the 300 line limit.

**Solution**: Split into two files:
1. `build/content_manager.py` - Keep core content loading (ContentManager class)
2. `build/hero_builder.py` - Extract hero-related functionality (new HeroBuilder class)

**Step-by-step refactoring**:

```
1. Create build/hero_builder.py with these methods moved from ContentManager:
   - generate_index_hero()
   - get_future_meetings()
   - format_future_meetings_section()
   - format_single_meeting_for_hero()
   - load_meeting_info()
   - format_meeting_section()
   - format_single_meeting()

2. Create HeroBuilder class:
   class HeroBuilder:
       def __init__(self, content_dir: Path):
           self.content_dir = content_dir

3. Update ContentManager.build_hero_content() to use HeroBuilder:
   def build_hero_content(self, page_name: str = 'index'):
       hero_file = self.content_dir / 'heroes' / f'{page_name}.md'
       ...
       if page_name == 'index':
           hero_builder = HeroBuilder(self.content_dir)
           hero_content = hero_builder.generate_index_hero(hero_content)

4. Update build/build.py imports:
   from hero_builder import HeroBuilder

5. Test: Run build and verify hero section still works correctly

This reduces content_manager.py to ~240 lines
```

#### B. page_builder.py (316 lines → target: ~280 lines)

**Problem**: File is 16 lines over the 300 line limit.

**Solution**: Extract meeting-specific rendering to separate file.

**Step-by-step refactoring**:

```
1. Create build/meeting_renderer.py

2. Move these methods from PageBuilder to new MeetingRenderer class:
   - group_meetings_by_month()
   - render_monthly_meeting_cards()
   - render_upcoming_meetings_calendar()

3. Create MeetingRenderer class:
   class MeetingRenderer:
       def __init__(self, jinja_env: Environment, dist_dir: Path):
           self.jinja_env = jinja_env
           self.dist_dir = dist_dir

4. Update PageBuilder to delegate to MeetingRenderer:
   def __init__(self, jinja_env, dist_dir, site_config):
       ...
       self.meeting_renderer = MeetingRenderer(jinja_env, dist_dir)

   def render_monthly_meeting_cards(self, meetings):
       return self.meeting_renderer.render_monthly_meeting_cards(meetings)

   def render_upcoming_meetings_calendar(self, meetings):
       return self.meeting_renderer.render_upcoming_meetings_calendar(meetings)

5. Update imports in build.py if needed

6. Test: Run build and verify meetings page and home page calendar work

This reduces page_builder.py to ~260 lines
```

### VIOLATION 2: Too Many Function Parameters

#### ContentType.__init__() has 6 parameters (max 3 after self)

**Problem**: `build/content_manager.py:16`
```python
def __init__(self, name: str, directory: str, sort_key: str = 'date',
             reverse: bool = True, detail_template: str = None,
             page_template: str = None, output_filename: str = None):
```

**Solution**: Use a configuration dictionary or builder pattern.

**Option A - Configuration Dictionary** (Recommended):

```python
# In content_manager.py, replace ContentType class with:

class ContentType:
    """Configuration for different content types."""
    def __init__(self, name: str, directory: str, config: dict):
        self.name = name
        self.directory = directory
        self.sort_key = config.get('sort_key', 'date')
        self.reverse = config.get('reverse', True)
        self.detail_template = config.get('detail_template', f'details/{name}-detail.html')
        self.page_template = config.get('page_template', f'pages/{name}.html')
        self.output_filename = config.get('output_filename', f'{name}.html')

# In build.py, update usage:
self.content_types = {
    'news': ContentType('news', 'news', {
        'output_filename': 'whatsnew.html',
        'page_template': 'pages/whatsnew.html',
        'detail_template': 'details/news-detail.html'
    }),
    'projects': ContentType('projects', 'projects', {
        'detail_template': 'details/project-detail.html'
    }),
    'members': ContentType('members', 'members', {
        'sort_key': 'title',
        'reverse': False,
        'detail_template': 'details/member-detail.html'
    }),
    'meetings': ContentType('meetings', 'meetings', {
        'sort_key': 'date',
        'reverse': True,
        'output_filename': 'meetings.html',
        'page_template': 'pages/meetings.html',
        'detail_template': 'details/meeting-detail.html'
    }),
}

# Test: Run build and verify all pages generate correctly
```

**Option B - Factory Method**:

```python
# Create separate factory methods:
class ContentType:
    def __init__(self, name: str, directory: str):
        self.name = name
        self.directory = directory
        self.sort_key = 'date'
        self.reverse = True
        self.detail_template = f'details/{name}-detail.html'
        self.page_template = f'pages/{name}.html'
        self.output_filename = f'{name}.html'

    def with_sort_config(self, sort_key: str, reverse: bool):
        self.sort_key = sort_key
        self.reverse = reverse
        return self

    def with_templates(self, detail: str, page: str, output: str):
        self.detail_template = detail
        self.page_template = page
        self.output_filename = output
        return self
```

### VIOLATION 3: Default Parameters (6 violations)

**Problem**: Rules state "You shall not provide default parameters to functions"

**Locations and fixes**:

#### 1. asset_manager.py:19 - copy_directory(dest_name=None)
```python
# BEFORE:
def copy_directory(self, src_name: str, dest_name: str = None):
    target_name = dest_name if dest_name else src_name

# AFTER:
def copy_directory(self, src_name: str, dest_name: str):
    # Callers must provide dest_name explicitly

# Update callers in asset_manager.py copy_assets():
self.copy_directory('images', 'images')  # instead of copy_directory('images')
self.copy_directory('scripts', 'scripts')
```

#### 2. asset_manager.py:49 - generate_pygments_css(theme='default')
```python
# BEFORE:
def generate_pygments_css(self, theme='default'):

# AFTER:
def generate_pygments_css(self, theme: str):

# Update caller in build.py:
self.asset_manager.generate_pygments_css('default')
```

#### 3. content_manager.py:47 - process_markdown_file(md_processor=None)
```python
# BEFORE:
def process_markdown_file(self, file_path: Path, md_processor=None):
    if md_processor is None:
        md_processor = self.setup_markdown_processor()

# AFTER:
def process_markdown_file(self, file_path: Path, md_processor):
    # Callers must create and pass md_processor

# Update callers in get_all_content() and other methods:
md_processor = self.setup_markdown_processor()
for md_file in content_dir.glob('*.md'):
    item_data = self.process_markdown_file(md_file, md_processor)
```

#### 4. content_manager.py:299 - build_hero_content(page_name='index')
```python
# BEFORE:
def build_hero_content(self, page_name: str = 'index'):

# AFTER:
def build_hero_content(self, page_name: str):

# Update callers in build.py:
hero_content = self.content_manager.build_hero_content('index')
# Instead of just build_hero_content()
```

#### 5. page_builder.py:97 - render_cards(item_var_name=None)
```python
# BEFORE:
def render_cards(self, items: List[Dict], template_name: str,
                 item_var_name: str = None, **extra_context):

# AFTER - Option 1: Make it required
def render_cards(self, items: List[Dict], template_name: str,
                 item_var_name: str, **extra_context):

# AFTER - Option 2: Split into two methods (cleaner)
def render_cards_flat(self, items: List[Dict], template_name: str, **extra_context):
    """For templates expecting flat properties."""
    # Original logic for item_var_name=None

def render_cards_nested(self, items: List[Dict], template_name: str,
                       item_var_name: str, **extra_context):
    """For templates expecting nested object."""
    # Original logic for item_var_name != None

# Update callers to use appropriate method
```

#### 6. ContentType.__init__() - Already covered in VIOLATION 2 above

### VIOLATION 4: Bare Exception Handlers (3 violations)

**Problem**: Rules state "never have bare except Exception: you shall be specific"

#### 1. content_manager.py:83-85 in process_markdown_file()
```python
# BEFORE:
except Exception as e:
    print(f"Error processing {file_path}: {e}")
    return None

# AFTER:
except (OSError, ValueError, yaml.YAMLError) as e:
    print(f"Error processing {file_path}: {e}")
    return None
```

#### 2. content_manager.py:161-163 in get_future_meetings()
```python
# BEFORE:
except Exception as e:
    print(f"Error processing {md_file}: {e}")
    continue

# AFTER:
except (OSError, ValueError, yaml.YAMLError) as e:
    print(f"Error processing {md_file}: {e}")
    continue
```

#### 3. content_manager.py:248-250 in load_meeting_info()
```python
# BEFORE:
except Exception as e:
    print(f"Error loading {filename}: {e}")
    return None

# AFTER:
except (OSError, yaml.YAMLError) as e:
    print(f"Error loading {filename}: {e}")
    return None
```

**Note**: You'll need to import yaml: `import yaml` at the top of content_manager.py

### Refactoring Order (Recommended)

Do these in order to maintain working code at each step:

1. ✅ Fix bare Exception handlers (quick, isolated changes)
2. ✅ Remove default parameters (moderate, requires updating callers)
3. ✅ Fix ContentType parameters (affects build.py usage)
4. ✅ Split content_manager.py (extract hero_builder.py)
5. ✅ Split page_builder.py (extract meeting_renderer.py)

**After each step**: Run `uv run python build/build.py` and verify build succeeds.

**Testing checklist**:
- [ ] Home page displays correctly with calendar
- [ ] Meetings page shows all meetings
- [ ] News/whatsnew page works
- [ ] Projects page works
- [ ] Members page works
- [ ] About page works
- [ ] All hero sections display
- [ ] No build errors or warnings

## Context for Continuation

### 🧠 Key Knowledge
- Build system processes markdown with frontmatter using `python-frontmatter`
- Jinja2 templates with Bootstrap 5.3.2 for styling
- Content types use `ContentType` class for configuration-driven behavior
- Meeting cards intentionally exclude dates (design decision)
- Image paths in frontmatter are relative to site root

### 📂 Important File Locations
- **Main script**: `build/build.py`
- **Templates**: `templates/` (pages/, cards/, details/, layouts/)
- **Content**: `content/` (news/, meetings/, projects/, members/, heroes/)
- **Static assets**: `images/`, `scripts/`, `css/`
- **Output**: `output/` (generated, not in git)

### 🔄 Development Workflow
1. Edit content in `content/` directories
2. Run `uv run python build/build.py` to build
3. Test with local server: `cd output && python -m http.server 8000`
4. Commit and push - GitHub Actions handles deployment

### 🎨 Design Patterns Used
- **Template inheritance**: Base → Page → Specific pages
- **Component-based**: Reusable card templates
- **Configuration-driven**: ContentType classes define behavior
- **Separation of concerns**: Content, templates, and logic separated

## Status: Functional but Needs Refactoring ⚠️

The system is fully functional and the home page calendar redesign is complete. However, the codebase has grown and now violates several rules.md standards:
- 2 files exceed 300 line limit
- Multiple functions use default parameters (not allowed)
- Some functions have too many parameters
- Bare Exception handlers need to be specific

**Priority**: Medium - Code works correctly but should be refactored for maintainability.

**Next session**: Follow the detailed refactoring instructions in "Rules Violations to Fix" section above.