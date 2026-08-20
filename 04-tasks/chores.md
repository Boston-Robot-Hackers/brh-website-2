# Chores

- [x] 1. Move hero HTML building (format_future_meetings_section, generate_index_hero in build/content_manager.py) out of Python string concat into a Jinja template — style guide MUST: no inline HTML strings in Python source.
- [x] 2. Extract shared announcement/report link resolution in build/page_builder.py into one helper — duplicated in build_detail_pages (63-68), render_cards (111-116), render_monthly_meeting_cards (222-235).
- [x] 3. Delete unused check_news_file_exists in build/page_builder.py (no callers anywhere in repo).
- [x] 4. Move local `import re` (build/build.py:194, 234) and `defaultdict`/`datetime, date` (build/page_builder.py:168, 247) imports to file top; the datetime,date import shadows the module-level datetime import.
- [x] 5. Add required file header (module name, one-line description, Author: Pito Salas and Claude Code, Open Source Under MIT license) and shebang to build/build.py, content_manager.py, page_builder.py, asset_manager.py, news_links.py.
- [x] 6. Change ContentType.__init__ params in build/content_manager.py (detail_template, page_template, output_filename) from `str = None` to `str | None = None`.
- [x] 7. Fix broken indentation on the 'hashtags' dict entry in build/page_builder.py:157 (0 spaces vs sibling 16-space indent).
- [x] 8. Wrap lines over 88 chars in build.py, content_manager.py, page_builder.py (~30 lines, up to 118 chars).
- [x] 9. Rename content/members/member_template.md and content/projects/project_template.md — they held real live content (Pito Salas's profile, the Dome ROBOT project) under template-looking filenames that got published. Renamed to pito-salas.md/dome-robot.md, fixed cross-refs in adam-ring.md and pito-salas.md's projects field, added a `_template.md` naming convention that content_manager.py's get_all_content now excludes from the build, and added genuine blank _template.md scaffolds for members/projects. (F02 finding 1)
- [x] 10. Remove legacy/ (earlier Tailwind prototype, including a git-tracked node_modules/) and archive/build.py — confirmed fully unreferenced by the live build, templates, docs, or CI. (F02 finding 2)
- [x] 11. Remove rules.md — a git-tracked symlink to an absolute path outside the repo that didn't even resolve on the machine that created it. (F02 finding 3)
- [x] 12. Standardize content/members/ filenames to lowercase-hyphenated slugs (was a mix of underscores, no separator, and one capitalized filename — the latter a real case-sensitivity risk between macOS dev and Linux CI). Fixed the one hand-written cross-reference (buddy_e -> buddy-e in a news post). (F02 finding 4)
- [x] 13. Rename the 3 remaining underscore-style content/news/ filenames to hyphens for consistency with the other 22. (F02 finding 5)
- [x] 14. Add image-sources/ to README.md's Project Structure tree (was real and in active use but undocumented from the root). (F02 finding 6)
- [x] 15. Fix README.md's scripts/ description (was "JavaScript" only; also holds the set-images.sh build utility). (F02 finding 7)
- [x] 16. Create the 05-issues/{open,closed,deferred}/ subfolders expected by .claude/process.md. (F02 finding 8)
