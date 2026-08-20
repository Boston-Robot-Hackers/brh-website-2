# TF03 Description for Feature F03

Task file name must be `TFNN-<slug>.md` where `NN` matches the feature number.
Each step is numbered `TF03.N`, starting at `.0`.

## TF03.0 — Add `signup_url` to site config
**Status**: done

**Description**: Add a `signup_url` field to `config/site.json`, set to the
confirmed Google Form URL
(`https://docs.google.com/forms/d/e/1FAIpQLScYvvhPZmbpyqAoFFkcD_cis5RfagIL6OsL_Nk_qc4a7bsakQ/viewform`).
No Python code change needed for this step — `build/build.py`'s
`load_site_config()` loads `site.json` wholesale and `page_builder.py`
passes it to every template as `site.*` (same pattern already used by
`site.title`, `site.footer_text`), confirmed by reading both files.

**Test**: covered by the regression test written in TF03.4 (asserts
`config/site.json` has a non-empty `signup_url` string).

**Result**:
* Added `signup_url` to `config/site.json`, set to the confirmed Google
  Form URL.
* No Python change needed — confirmed `site.*` context injection already
  covers it.

## TF03.1 — Generate the QR image at build time
**Status**: done

**Description**: Add a QR-generation dependency (`qrcode`, with its
`Pillow` dependency) to `pyproject.toml`. Add a method to
`build/asset_manager.py`, alongside the existing `generate_pygments_css`
pattern, that renders a URL into a PNG and writes it to
`output/images/signup-qr.png`. Call it from `build/build.py`'s `build()`,
passing `site_config['signup_url']` directly — required, not defaulted, so
a missing field fails loudly at build time instead of silently skipping the
feature (per the style guide's boundary-validation rule).

**Test**: new automated test — call the generation function directly with
a fixed test URL and a temp output dir; assert a valid PNG is written
(file exists, non-zero size, PNG magic bytes) and that two different input
URLs produce different image bytes (locks in "config-driven image," not a
fixed checked-in asset).

**Result**:
* Added `qrcode[pil]>=7.4.2` to `pyproject.toml`; `uv sync` pulled in
  Pillow as its image backend.
* Added `AssetManager.generate_qr_code(url, filename="signup-qr.png")` in
  `build/asset_manager.py`, writing to `dist/images/`.
* Wired into `build/build.py`'s `build()`, right after `copy_assets()`,
  passing `site_config['signup_url']` directly (raises loudly if absent).
* `tests/test_asset_manager.py`: added `TestGenerateQrCode` (2 tests —
  valid PNG written, different URLs produce different bytes).
* Full build confirmed: `output/images/signup-qr.png` generated, valid PNG
  magic bytes.

## TF03.2 — Render the QR code in the home page header
**Status**: done

**Description**: Add the QR image to `templates/components/hero.html`,
sized and positioned as a prominent call-to-action, with descriptive `alt`
text (e.g. "Scan to sign up for Boston Robot Hackers"). `hero.html` is
included only by `templates/layouts/home.html`, itself used only by
`templates/pages/index.html` — this existing scoping is what keeps the QR
code home-page-only without adding a page-type conditional.

**Test**: covered by the regression test written in TF03.4 (asserts the
QR `<img>` appears in built `index.html` output and in no other built
page).

**Result**:
* Correction to the plan: `templates/components/hero.html` is **not**
  home-page-exclusive — `templates/layouts/page.html` (the shared listing
  layout) also includes it. Adding the QR there would have put it on
  every listing page too, contradicting F03's home-page-only requirement.
  Caught by grepping every template that includes `hero.html` before
  editing, rather than trusting the earlier assumption.
* Placed the QR markup directly in `templates/layouts/home.html` instead
  (confirmed via grep: only `templates/pages/index.html` extends this
  layout) — right after the `hero.html` include, before the page's
  `container` div.
* `src="images/signup-qr.png"` used unprefixed (no `../`) since this
  layout only ever renders a top-level page, never a detail page.

## TF03.3 — Style for legibility in both light and dark mode
**Status**: done

**Description**: In `css/main.css`, wrap the QR image in a fixed
light/white background card with padding (a standard QR "quiet zone"),
independent of the page's own light/dark theme variables. QR codes are
fixed black-on-white and don't recolor safely, so dual-theme legibility
comes from a themed *frame*, not a themed *code* — consistent with F01's
dark-mode work.

**Test**: Manual — visual contrast/scannability judgment, not practically
assertable by pytest. Record per `.claude/style_guide.md`'s manual-test-notes
convention: command/setup used, pages checked, expected vs. actual result,
in both themes.

**Result**:
* Added `.signup-qr-cta` (outer card: theme-aware `var(--bg-card)`/
  `var(--border)`, matches the existing `.hero` card look), `.signup-qr-frame`
  (fixed `#ffffff` background + padding — the actual quiet zone, deliberately
  not theme-aware), and `.signup-qr-caption` to `css/main.css`.
* `#ffffff` was already in `test_css_theme.py`'s `BESPOKE_CHROME_HEX`
  allowlist, so no test update was needed for the hardcoded-hex-color
  regression check.
* Manual check, done with real rendering (Playwright/Chromium, installed
  to a scratch npm project outside the repo — no `package.json` here,
  same approach as F01's TF01.7), not just static file inspection:
  command `uv run python build/build.py`, served `output/` via
  `python3 -m http.server`, loaded `index.html` under both
  `colorScheme: 'light'` and `'dark'` contexts, and via the `#theme-toggle`
  button.
* Screenshotted the QR card in both modes: frame background stays solid
  `rgb(255, 255, 255)` in both, clear black modules, visible quiet zone;
  the surrounding `.signup-qr-cta` card recolors with the theme
  (`var(--bg-card)`). Toggle button confirmed to flip `light` → `dark`
  live. No layout overlap/clipping around the card. Expected vs. actual:
  matched.
* Checked `page.on('response')` for 4xx/5xx on `index.html`: only the
  pre-existing, unrelated missing `images/robot-logo.png` (flagged during
  F01 and again during this feature's write-up) — no new errors from the
  QR addition.
* Cross-checked the confirmed `signup_url` against the site's existing
  "Request an invite to join us!" link in `content/heroes/index.md`
  (`https://forms.gle/JmxhSMc8iypZwj1z9`) — that short link redirects
  (302) to the exact same Google Form, confirming the two aren't
  conflicting signup mechanisms.

## TF03.4 — Write regression tests and do final verification
**Status**: done

**Description**: Dedicated test-writing task. Add automated tests: (a)
`config/site.json` has a non-empty `signup_url`; (b) the QR-generation
function produces a valid PNG and differs by input URL (may already exist
from TF03.1 — consolidate here if not); (c) built `index.html` contains the
QR `<img>` with non-empty `alt` text; (d) every other built page
(`whatsnew.html`, `meetings.html`, `projects.html`, `members.html`,
`about.html`, `learn.html`, plus one detail page) does not contain the QR
image reference. Then run a full build and manually check the home page in
both light and dark mode.

**Test**: `uv run pytest` includes and passes the new checks; manual pass
recorded per `.claude/style_guide.md`'s convention.

**Result**:
* Added `tests/test_signup_qr.py`: `config/site.json` has a non-empty
  `signup_url`; `templates/layouts/home.html` renders the QR `<img>` with
  alt text; none of the shared templates (`base.html`, `page.html`,
  `detail.html`, `hero.html`) render it.
* `uv run pytest` — 78 passed (73 pre-existing + 5 new: 2 in
  `TestGenerateQrCode`, 3 in `test_signup_qr.py`).
* Full build (`uv run python build/build.py`) verified clean; real-browser
  pass covered under TF03.3 (dual-theme legibility, home-page-only
  scoping via 5 pages checked with Playwright, no new console/network
  errors).
