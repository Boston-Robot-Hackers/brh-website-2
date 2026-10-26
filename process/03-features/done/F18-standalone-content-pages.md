# F18 — Standalone content pages, starting with Tips for Speakers
**Priority**: Medium
**Date Created:** 2026-10-26
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**: A simple way to publish a standalone markdown page that isn't one of the fixed nav pages, linked from About. The first one is **Tips for Speakers**.

## Scope

- **Source**: each `content/pages/<slug>.md` file, with a required `title` in its frontmatter.
- **Output**: `output/<slug>.html`, rendered with the shared page layout. The nav highlights **About**, since these pages hang off About.
- **Linking**: About links to each page with an ordinary hand-written markdown link. No auto-generated index, because one or two pages don't need one.
- **First page**: the speaker-tips draft moves out of `content/about.md` into `content/pages/speaker-tips.md`, and About gets a short "Speaking at BRH" link in its place.
- A missing `title` raises an error naming the file.

## Out of scope

- No nav-bar entry, and no per-page hero or banner config beyond what the shared layout already does.
- Writing further pages or expanding About's own text. That's content work you can do once the mechanism exists.

## How to Demo
**Setup**: `make try`.

**Steps**:
1. Open the About page.
2. Click the "Tips for Speakers" link.

**Expected output**: `speaker-tips.html` renders in the site layout, with About highlighted in the nav.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
