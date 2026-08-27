# TF10 Description for Feature F10

## TF10.0 — Record current DNS state before changing anything
**Status**: done
**Description**: In Namecheap Advanced DNS for `bostonrobothackers.com`,
note the exact current record for host `pupper` (type — *URL Redirect
Record* — target URL, and redirect type) so it can be restored if this
approach needs to be undone.
**Test**: Not testable from this repo (external DNS panel, read-only
lookup). Verify by recording the current record's values in this task's
Result section before TF10.3 changes it.

**Result**: Confirmed via screenshot of Namecheap's Advanced DNS table
(and independently via `dig`, which resolved `pupper.bostonrobothackers.com`
to `192.64.119.180` — Namecheap's own forwarding IP): old record was
`Type: URL Redirect Record`, `Host: pupper`, `Value: https://bostonrobothack...`
(Permanent redirect, truncated in the panel view). Superseded by TF10.3's
CNAME record; the row has since been deleted.

## TF10.1 — Author the redirect page + CNAME as versioned source in this repo
**Status**: done
**Description**: Add `ops/pupper-redirect/index.html` — a static HTML
page with `<meta http-equiv="refresh" content="0; url=https://bostonrobothackers.com/projects/pupper.html">`
plus a visible fallback link (for the rare client that ignores
meta-refresh) — and `ops/pupper-redirect/CNAME` containing exactly
`pupper.bostonrobothackers.com`. These files aren't built or deployed by
this repo's own pipeline; they're the source of truth to copy into the
new standalone redirect repo (TF10.2), so the redirect content has git
history instead of being hand-typed once with no record.
**Test**: New `tests/test_pupper_redirect.py` asserts
`ops/pupper-redirect/index.html` exists and contains the exact target URL
string, and `ops/pupper-redirect/CNAME` exists and its content is exactly
`pupper.bostonrobothackers.com`. Guards against a future hand-edit
introducing a typo in either file.

**Result**: Added `ops/pupper-redirect/index.html` (meta-refresh + JS
`location.replace` + visible fallback link, all pointing at
`https://bostonrobothackers.com/projects/pupper.html`, `noindex` meta so
it doesn't get indexed as a duplicate) and `ops/pupper-redirect/CNAME`
(`pupper.bostonrobothackers.com`). New `tests/test_pupper_redirect.py`,
2/2 pass.

## TF10.2 — Create the standalone GitHub Pages redirect repo
**Status**: done
**Description**: Create a new, minimal public GitHub repo (suggested name
`brh-pupper-redirect`). Copy `index.html` and `CNAME` from
`ops/pupper-redirect/` into its root, push to `main`, then enable GitHub
Pages (Settings → Pages → Source: Deploy from a branch → `main` / root).
No build step needed — it's two static files.
**Test**: Not testable from this repo (external GitHub account action).
Verify manually: the repo's default Pages URL
(`https://<github-username>.github.io/brh-pupper-redirect/`) serves the
redirect page over HTTPS before touching DNS in TF10.3.

**Result**: User created the repo (initially named `bro-pupper-redirect`,
then renamed to `Boston-Robot-Hackers/brh-pupper-redirect` as originally
suggested) and pushed `index.html` + `CNAME` directly. Confirmed via
unauthenticated GitHub API + raw content fetch: repo is public, `main`
branch, `CNAME` contains `pupper.bostonrobothackers.com`, `index.html`
has the correct redirect target. `"has_pages": false` in the API response
— Pages is not yet enabled. Still to do: enable Pages (Settings → Pages →
source `main` / root) and confirm the default Pages URL loads over
HTTPS, before TF10.3's DNS change.

## TF10.3 — Repoint the `pupper` DNS record at Namecheap
**Status**: done
**Description**: In Namecheap Advanced DNS for `bostonrobothackers.com`,
delete the existing *URL Redirect Record* for host `pupper` and add a
**CNAME Record**: Host `pupper`, Value `<github-username>.github.io.`,
TTL Automatic. This is the actual fix: a real CNAME to GitHub's Pages
edge (rather than Namecheap's HTTP-only forwarding) lets GitHub issue and
serve a proper cert for the subdomain.
**Test**: Not testable from this repo. Verify manually via
`dig pupper.bostonrobothackers.com CNAME +short` once propagated — expect
it to resolve to `<github-username>.github.io.`.

**Result**: Confirmed propagated: `dig pupper.bostonrobothackers.com CNAME
+short` and a direct query against the authoritative nameserver
(`dns1.registrar-servers.com`) both resolve to
`boston-robot-hackers.github.io.`. `curl -I http://pupper.bostonrobothackers.com`
now returns `200 OK` serving the redirect page. `https://` still fails
(`SSL: no alternative certificate subject name matches target host name`)
— expected, since TF10.4 (set custom domain + enforce HTTPS in the new
repo's Pages settings) hasn't been done yet.

## TF10.4 — Set the custom domain and enforce HTTPS on the new repo
**Status**: not done
**Description**: In the new repo's Settings → Pages → Custom domain,
enter `pupper.bostonrobothackers.com` and save. Wait for GitHub's DNS
check to pass (can take minutes to a few hours), then enable "Enforce
HTTPS" once the checkbox becomes available — GitHub auto-provisions the
Let's Encrypt cert once DNS verification succeeds.
**Test**: Not testable from this repo. Verify manually: the repo's Pages
settings page shows the custom domain verified with a green check and
"Enforce HTTPS" enabled.

## TF10.5 — End-to-end verification
**Status**: not done
**Description**: Load `https://pupper.bostonrobothackers.com` in a
browser and confirm it reaches the live Pupper project page with no cert
warning. Cross-check with `curl`.
**Test**: `curl -sI https://pupper.bostonrobothackers.com` succeeds (TLS
handshake completes, no `-k`/`--insecure` flag needed) and returns a
redirect or 200; record the actual output in this task's Result section.

## TF10.6 — Tests + full suite verification
**Status**: done
**Description**: Run the full project test suite to confirm
`test_pupper_redirect.py` (TF10.1) passes and nothing else in the repo
regressed — this feature touches no other build code, so a full green run
is the expected outcome.
**Test**: `uv run pytest` — full suite passes, including the new
`tests/test_pupper_redirect.py`.

**Result**: `uv run pytest` — 131/131 pass (was 129; +2 new from
`tests/test_pupper_redirect.py`). No regressions.
