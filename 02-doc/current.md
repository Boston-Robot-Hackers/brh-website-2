# Current

## Open

**In progress: F10 — pupper.bostonrobothackers.com subdomain over HTTPS**
(`03-features/notdone/F10-pupper-subdomain-redirect.md`,
`04-tasks/notdone/TF10-pupper-subdomain-redirect.md`).

* Design: a second, minimal GitHub Pages site
  (`Boston-Robot-Hackers/brh-pupper-redirect`, public) serves a redirect
  page for `pupper.bostonrobothackers.com` → the live Pupper project page.
  Namecheap's old *URL Redirect Record* for `pupper` was HTTP-only, which
  is why `https://` never worked there; a real CNAME to GitHub's Pages
  edge lets GitHub issue a proper cert for that subdomain, same as the
  main site. Full rationale and rejected alternatives (Cloudflare
  nameserver move, second custom domain on this repo) are in the F10 file.
* Done so far (TF10.0–TF10.2, TF10.6): recorded the old DNS record for
  rollback; added `ops/pupper-redirect/index.html` + `CNAME` in this repo
  as versioned source (covered by `tests/test_pupper_redirect.py`, new,
  2/2 passing); user created/renamed the standalone repo to
  `brh-pupper-redirect`, pushed both files, enabled GitHub Pages on it
  (confirmed live via its default `github.io` URL, which now redirects
  correctly). Full suite: 131/131 passing, no regressions from this repo's
  side — this feature touches no build/deploy code.
* **In progress (TF10.3)**: Namecheap's `pupper` host record has been
  changed from the old URL Redirect Record to a `CNAME Record` pointing
  at `boston-robot-hackers.github.io.` — confirmed correct in the
  Namecheap panel, but as of the last check the authoritative nameserver
  (`dns1/2.registrar-servers.com`) hadn't yet picked it up (zone SOA
  serial unchanged). Waiting on propagation — Namecheap's own docs say
  this is typically minutes, up to ~30.
* **Not yet started**: TF10.4 (set `pupper.bostonrobothackers.com` as the
  new repo's custom domain in its Pages settings, wait for GitHub's DNS
  check, enable "Enforce HTTPS"), TF10.5 (end-to-end verification —
  browser + `curl -sI https://pupper.bostonrobothackers.com`).
* Next step for whoever picks this up: re-run
  `dig pupper.bostonrobothackers.com CNAME +short` (or ask the user to
  check) — once it resolves to `boston-robot-hackers.github.io.`, proceed
  to TF10.4.

The site's full visual redesign (F04 concept exploration, F05 real
implementation of Option D) is done and sits on branch
`f04-site-redesign`, pushed but not merged into `main` — merging/opening
a PR is a deliberate next step for whoever picks this up, not done as
part of the checkpoint.

Known, deliberately-deferred items (not urgent, no ticket filed):

* 3 ruff `DTZ` (naive-datetime) findings, left unfixed: `datetime.now()`
  and `datetime.min` in `build/content_manager.py`, `date.today()` in
  `build/page_builder.py`. The site only ever needs one local timezone
  (the group's own meetup "today"), so naive local dates are correct as
  written — forcing tz-awareness would be a real behavior-risk change with
  no matching `.claude/style_guide.md` rule, not a mechanical lint fix.
* `pyproject.toml`'s `[tool.uv] dev-dependencies` field is deprecated by
  `uv` in favor of `[dependency-groups] dev` — a cosmetic warning on every
  `uv` invocation, not urgent.
* `ruff` is not a project dependency (no entry in `pyproject.toml`); this
  session ran it via `uvx ruff` instead. Worth adding as a real dev
  dependency at some point so `uv run ruff` works directly.
* `01-literate/` has never actually been populated in this repo despite
  `.claude/process.md`'s "regenerate literate docs before committing"
  rule — confirmed via `git log` (no file has ever existed there).
  `build/content_manager.py`, `build/page_builder.py`, and `build/build.py`
  have all changed since (most recently for F09) with no literate docs
  generated for any of them. Deliberately skipped per user decision
  (2026-08-20) rather than starting a first-pass doc-gen project
  unprompted during a routine checkpoint.

See `02-doc/history.md` for the completed-work log.
