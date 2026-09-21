# F11 — Plain-text list of upcoming talks
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* Build a plain-text page, `output/upcoming-talks.txt`.
  * Served at `https://bostonrobothackers.com/upcoming-talks.txt`.
  * Purpose: copy-paste into emails to other orgs so they can calendar our talks.
* **Which meetings qualify**: all three must hold.
  * Date is today or later (build date).
  * Not a hands-on meeting (`classify_meeting` → `main`).
  * Has both a `speaker` and a `topic` in frontmatter — TBA meetings drop out automatically.
* **New optional meeting frontmatter**: `speaker`, `topic`.
  * **Explicit fields, not parsed** from the announcement title or `text` — parsing free text would be guessing.
  * Backfill the two current talks: Oct 15 (Arjun Viswanathan), Nov 12 (Yun Chang).
* **Per-meeting block**: topic, speaker, summary, date, time, location, URL.
  * **Summary** = the meeting's existing `text` field.
  * **Date** = full weekday form, e.g. "Thursday, October 15, 2026".
* **URL rule**:
  * Announcement news page if one resolves; else the meeting's own detail page.
  * Same resolution the site already uses (`resolve_news_html`).
* **Plain absolute URLs**.
  * Built from a new `site_url` key in `config/site.json` (`https://bostonrobothackers.com`).
  * No redirect/tracking wrappers — nothing like `google.com/url?q=...`.
* Rendered from a Jinja text template, not Python strings (style guide: no inline templates).
* Short header (club name, generated date) and footer (Eventbrite registration link, full-schedule URL).

**Non-goals**:
* Not linked from the nav — an organizer utility, reached by URL.
* No `.ics` / calendar-file export.
* No hands-on sessions.

**Known limitation**:
* "Upcoming" is fixed at **build time**.
* The site rebuilds only on push, so a past talk lingers until the next deploy.

## How to Demo
**Setup**: `uv run python build/build.py`.

**Steps**:
1. `cat output/upcoming-talks.txt`.
2. Confirm it lists Oct 15 and Nov 12 only — no hands-on sessions, no TBA talks.
3. Check each URL starts with `https://bostonrobothackers.com/` and opens the right page.
4. After deploy, open `https://bostonrobothackers.com/upcoming-talks.txt` in a browser.

**Expected output**: plain text, one block per qualifying talk, clean clickable URLs, pastes into Gmail without formatting junk.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
