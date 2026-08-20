# Project Spec

## App Name
Boston Robot Hackers Website (brh-website-2)

## Description
* Static marketing/community website for **Boston Robot Hackers**, a
  Boston-area robotics club that meets monthly at Artisans Asylum in
  Allston, MA.
* Built with Python + Jinja2 + Markdown content; `build/build.py` renders
  everything in `content/` and `templates/` to static HTML in `output/`.
* GitHub Actions builds and deploys `output/` to GitHub Pages on every
  push to `main` — no server-side runtime, database, or accounts.
* Six areas, all reachable from the top nav: **Home** (hero + highlighted
  news + upcoming meetings), **Learn** (curated external robotics
  resources), **Members** (member directory/profiles), **Projects**
  (community project listings), **About** (mission, meeting info,
  contact), and **What's New** (news/announcements archive, linked from
  Home rather than the top nav).

## Goals
* Give Boston Robot Hackers a public front door: explain who the club is,
  where and when it meets, and how to join.
* Showcase the community's activity — news, meetings, member profiles,
  and projects — kept current via Markdown content edits, not code
  changes.
* Convert visitors into members: a prominent signup link/QR code
  (`config/site.json`'s `signup_url`) drives to an external Google Form.
* Point newcomers and existing members at curated learning resources for
  robotics (ROS, CV, ML, SLAM, motion planning, etc.).
* Stay simple to maintain: plain Markdown + frontmatter content, no CMS,
  no backend, cheap/free static hosting on GitHub Pages.

## Non-Goals
* No user accounts, login, or authentication — content editing is
  file-based (Markdown + git), not through the live site.
* No dynamic/server-side behavior — everything is pre-rendered at build
  time to static HTML.
* No in-site data collection (signup, RSVPs, forms) — those are delegated
  to external tools (Google Forms, Eventbrite links in news posts).
* No e-commerce, payments, or member-only/gated content.
* No mobile app — responsive static web only.

## Key Users
* **Prospective members** — browse Home/About/Learn, decide whether to
  join, and use the signup link/QR code to request an invite.
* **Current club members** — check upcoming meetings, read news/updates,
  browse projects and the member directory, use Learn's curated links.
* **Club organizer(s)** (currently Pito Salas, per `content/about.md`) —
  the site's content maintainer: adds news/meeting/project/member entries
  as Markdown files and edits `config/site.json` for site-wide text.
