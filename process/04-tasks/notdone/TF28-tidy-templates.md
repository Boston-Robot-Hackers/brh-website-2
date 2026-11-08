# TF28 Tidy the templates for Feature F28
**Date Created:** 2026-11-05

## TF28.0 — Save the before state
**Status**: not done

**Description**: Save a build outside `output/`, and take screenshots of every page at 375px and 1200px in both themes, with the F27 screenshot script.

**Test**: not feasible, this step only saves a reference for TF28.9.

## TF28.1 — Turn template comments into Jinja comments
**Status**: not done

**Description**: Change every `<!-- -->` in `templates/` to `{# #}`.

**Test**: no built page contains `<!--`, and every page starts with `<!DOCTYPE html>`.

## TF28.2 — Pass one root path
**Status**: not done

**Description**: Have the build pass `root` to every page, and replace the `'../' if is_detail_page else ''` expressions with it. Remove `is_detail_page` if nothing else uses it.

**Test**: no template contains `if is_detail_page`, and a top-level page and a detail page both link `css/base.css` correctly.

## TF28.3 — Share the detail-page body and title
**Status**: not done

**Description**: Add `components/detail-body.html` for the article body and "On this page" sidebar, used by news and project detail. Add a macro for the label and title, used by all five detail templates.

**Test**: news and project pages with headings still show the sidebar, and pages without headings still drop it.

## TF28.4 — Move the meeting address to config
**Status**: not done

**Description**: Add `meeting_place` (name, address and link) to `config/site.json`, require it in the build, and use it in the three templates.

**Test**: the address in built Home and Meetings comes from config, and a missing `meeting_place` fails the build.

## TF28.5 — Move member card logic to Python
**Status**: not done

**Description**: Have `render_member_cards` pass each member's projects to show and the count of the rest. Simplify `member-card.html` to a single loop.

**Test**: a member with 6 linked projects shows 4 and "+2 more", and one with no linked projects shows no project block.

## TF28.6 — Use one `h1` per page
**Status**: not done

**Description**: Pages with their own title tell the banner, and it renders its title as a paragraph with the same look. The banner stays an `h1` on the other pages.

**Test**: every built page has exactly one `h1`, not counting `h1`s written in content files.

## TF28.7 — Add meta descriptions
**Status**: not done

**Description**: Add `description` to `config/site.json`, and a `<meta name="description">` to every page, from the excerpt or summary on detail pages and from config elsewhere.

**Test**: every built page has one non-empty meta description, and a news page's matches its excerpt.

## TF28.8 — Write the feature's tests
**Status**: not done

**Description**: Add the tests from TF28.1 to TF28.7 in `tests/test_template_tidy.py`, and update existing tests that depend on the old markup.

**Test**: `uv run pytest` passes in full.

## TF28.9 — Compare screenshots
**Status**: not done

**Description**: Take after screenshots and compare them with TF28.0.

**Test**: no differences beyond the known nav photo timing noise.

## TF28.10 — Check it in a browser
**Status**: not done

**Description**: Run the F28 demo.

**Test**: not feasible to automate, so the user signs off.
