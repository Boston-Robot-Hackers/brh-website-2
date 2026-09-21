---
version: "1.0"
generated: "2026-09-21"
---

# asset_manager — copying static files into output/ (appendix)

## What it does

`AssetManager` moves everything that isn't generated into `output/`:

- `images/`, `scripts/`, and `content/meeting-reports/` (PDF slides) are
  copied as whole directories.
- `css/shared.css` and `css/main.css` are copied into `output/css/`.
- A Pygments stylesheet, `output/css/syntax.css`, is **generated** for code
  highlighting in Markdown posts.
- `clean_output_directory` wipes and recreates `output/` at the start of each
  build.

## Replace, don't merge

`copy_directory` deletes the destination before copying:

```python
if dest_path.exists():
    shutil.rmtree(dest_path)
shutil.copytree(src_path, dest_path)
```

A merge would leave deleted source files behind in `output/`. Since `build()`
also wipes `output/` up front, this is belt-and-braces, but it keeps the
method correct if it's ever called on its own.

## Observations and possible improvements

1. **Missing sources are skipped silently.** A typo in a directory name would
   produce a site without images and no error. Raising (or at least warning) for
   the known-required directories would follow the project's "report, don't
   guess" rule.
2. **The CSS file list is hard-coded.** A new stylesheet must be added here by
   hand; globbing `css/*.css` would remove that step.
3. **No cache-busting.** CSS is linked as plain `css/main.css`, so browsers can
   keep a stale copy after a deploy. Appending a content hash (for example
   `main.css?v=<hash>`) at copy time would fix that.
