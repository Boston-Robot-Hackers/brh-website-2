---
version: "1.1"
generated: "2026-11-05"
---

# asset_manager — copying static files into output/ (appendix)

## What it does

`AssetManager` moves everything that isn't generated into `output/`:

- `images/`, `scripts/`, and `content/meeting-reports/` (PDF slides) are
  copied as whole directories.
- **Every `.css` file in `css/`** is copied into `output/css/`. Today that's
  `base.css`, `layout.css`, `components.css` and `pages.css`.
- A Pygments stylesheet, `output/css/syntax.css`, is **generated** for code
  highlighting in Markdown posts.
- `clean_output_directory` wipes and recreates `output/` at the start of each
  build.

## Copying stylesheets by pattern

`copy_css_files` globs the folder instead of naming files:

```python
for src_file in sorted((self.root_dir / "css").glob("*.css")):
    shutil.copy2(src_file, css_dest / src_file.name)
```

- **Why a glob**: adding or splitting a stylesheet needs no change here. Only
  `templates/components/head.html` has to link it.
- **Why sorted**: the copy order doesn't matter to browsers, but sorting keeps
  the build log stable from run to run.
- **What it doesn't decide**: cascade order. That lives in `head.html`, which
  links base, layout, components and pages in that order.

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
2. **A stylesheet can be copied but never linked.** The glob copies any `.css`
   file, but nothing checks that `head.html` links it. A test comparing the two
   lists would catch a forgotten link.
3. **No cache-busting.** Stylesheets are linked by plain name, so browsers can
   keep a stale copy after a deploy. Appending a content hash (for example
   `base.css?v=<hash>`) at copy time would fix that.
