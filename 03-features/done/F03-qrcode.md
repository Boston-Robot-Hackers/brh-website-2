# F03 — QR code to signup form on home page header
**Priority**: Low
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* No QR code exists anywhere on the site today.
* Target URL is not inferred from content — it's a new field in
  `config/site.json` (proposed name: `signup_url`), read into templates via
  the existing `site.*` context (same pattern as `site.title`,
  `site.footer_text`).
* Confirmed value (user-supplied): a Google Form —
  `https://docs.google.com/forms/d/e/1FAIpQLScYvvhPZmbpyqAoFFkcD_cis5RfagIL6OsL_Nk_qc4a7bsakQ/viewform`
  — distinct from the per-meeting Eventbrite "Register" links in
  `content/news/`, confirming those shouldn't be reused as the QR target.
* Renders once, prominently, in the home page's header/hero area — not
  site-wide, not in the footer, not on any other page. Lives in
  `templates/layouts/home.html` itself (the layout only `index.html`
  extends), not in the shared `hero.html` component — that component
  turned out to also be included by `templates/layouts/page.html` (every
  listing page), which would have put the QR everywhere.
* Since the target is config-driven, generate the QR image at build time
  from `site.json`'s field rather than checking in a static pre-generated
  image — editing the config regenerates the code automatically and avoids
  a stale QR if the URL changes without a manual regen step. Needs a
  QR-generation build dependency (e.g. Python `qrcode` package).
* Sized to read as a deliberate call-to-action, not a small icon — large
  enough to scan easily from a phone or a projected/printed page.
* Needs a light-enough quiet zone/background to stay scannable in both
  light and dark mode (per F01), and real alt text for accessibility.

**Non-goals**:
* QR codes on any page other than the home page.
* Per-meeting/deep-link QR codes pointing at a specific talk's Eventbrite
  registration URL — each announcement already has its own textual
  Register link.
* Custom QR styling (logo overlay, brand colors).
* Scan analytics/tracking.

## How to Demo
**Setup**: Run `uv run python build/build.py`, then serve `output/` locally
(e.g. `python3 -m http.server 8000 --directory output`) and open it in a
browser.

**Steps**:
1. Set `signup_url` in `config/site.json`, rebuild, open `index.html`.
   Confirm the QR code appears prominently in the header/hero area.
2. Open a non-home page (e.g. `meetings.html`, a member detail page).
   Confirm no QR code appears.
3. Scan the home page QR code with a phone camera and confirm it opens the
   URL currently set in `config/site.json`.
4. Change `signup_url` in `config/site.json`, rebuild, rescan. Confirm the
   QR code now points at the new URL.
5. Toggle dark/light mode (per F01's toggle button) and confirm the QR code
   stays clearly scannable in both.

**Expected output**:
* Only the home page shows a QR code, sized as a clear call-to-action in
  the header/hero area.
* It always points at whatever URL is currently set in `config/site.json`.
* Readable in both color modes, with alt text describing where it goes.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
