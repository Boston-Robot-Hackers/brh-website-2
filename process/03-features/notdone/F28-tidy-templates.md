# F28 — Tidy the templates
**Priority**: Medium
**Date Created:** 2026-11-05
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no

**Description**:

* Clean up the template problems the 2026-11-05 HTML and CSS audit found, now that the CSS is cleaned up (F25, F27).
* **Pages look exactly the same.** The changes are in markup, metadata and code structure, so screenshots before and after should match pixel for pixel.

**Shared detail-page pieces**:

* The news and project detail templates repeat the article body and its "On this page" sidebar. A partial, `components/detail-body.html`, replaces both copies.
* All five detail templates (news, project, member and the two ROSbot ones) repeat the label and title at the top. A macro replaces those copies.

**One root path**:

* `'../' if is_detail_page else ''` appears 18 times across `head.html`, `navigation.html` and `base.html`.
* The build passes one `root` value to every page, `''` or `'../'`, and templates use `{{ root }}`.
* `is_detail_page` goes away if nothing else needs it.

**Template comments**:

* **31 templates use `<!-- -->` comments, so up to 40 of them ship in every page**, some before `<!DOCTYPE html>`.
* They become `{# #}` Jinja comments, which never reach the page.

**The meeting address in config**:

* "Artisans Asylum, 96 Holton Street, Allston" and its link are typed into `home-lead.html`, `index.html` and `meetings.html`.
* They move to a `meeting_place` entry in `config/site.json`, which the build requires.
* The address in `content/calendar.yaml` and in news posts stays, since that's content.

**Member card logic in Python**:

* `member-card.html` counts each member's linked projects with two Jinja loops and namespaces.
* `render_member_cards` works out the projects to show (up to 4) and how many more there are, and the template just loops over them.

**One `h1` per page**:

* 59 of 61 pages have two `h1`s, because the banner's "Boston Robot Hackers" is always an `h1`.
* The banner title stays an `h1` only on pages with no title of their own: About, Learn, Meetings, Build-A-ROSBot and content pages.
* Elsewhere it becomes a paragraph, styled exactly as before.
* `h1`s written inside content files are left alone.

**Meta descriptions**:

* No page has a `<meta name="description">`, which search engines and link previews use.
* Detail pages use their excerpt or summary. Other pages use a new `description` entry in `config/site.json`.
* **The default text is the first sentence of Home's mission**, unless the user gives other wording.

**Non-goals**:

* No visual changes.
* No changes to content files, which is F29.
* No social preview tags beyond the description.

## How to Demo
**Setup**: before screenshots and build from TF28.0, then `make try`.

**Steps**:

1. Compare screenshots of every page before and after.
2. View the source of Home, a news page and About.
3. Run `uv run pytest`.

**Expected output**:

* Screenshots match on every page.
* Page source has no HTML comments from templates, one `h1`, and a meta description.
* All tests pass.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
