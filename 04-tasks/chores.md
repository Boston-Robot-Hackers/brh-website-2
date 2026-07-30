# Chores

- [ ] 1. Move hero HTML building (format_future_meetings_section, generate_index_hero in build/content_manager.py) out of Python string concat into a Jinja template — style guide MUST: no inline HTML strings in Python source.
- [ ] 2. Extract shared announcement/report link resolution in build/page_builder.py into one helper — duplicated in build_detail_pages (63-68), render_cards (111-116), render_monthly_meeting_cards (222-235).
- [ ] 3. Delete unused check_news_file_exists in build/page_builder.py (no callers anywhere in repo).
- [ ] 4. Move local `import re` (build/build.py:194, 234) and `defaultdict`/`datetime, date` (build/page_builder.py:168, 247) imports to file top; the datetime,date import shadows the module-level datetime import.
- [ ] 5. Add required file header (module name, one-line description, Author: Pito Salas and Claude Code, Open Source Under MIT license) and shebang to build/build.py, content_manager.py, page_builder.py, asset_manager.py, news_links.py.
- [ ] 6. Change ContentType.__init__ params in build/content_manager.py (detail_template, page_template, output_filename) from `str = None` to `str | None = None`.
- [ ] 7. Fix broken indentation on the 'hashtags' dict entry in build/page_builder.py:157 (0 spaces vs sibling 16-space indent).
- [ ] 8. Wrap lines over 88 chars in build.py, content_manager.py, page_builder.py (~30 lines, up to 118 chars).
