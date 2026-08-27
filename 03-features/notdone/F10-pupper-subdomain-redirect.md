# F10 — pupper.bostonrobothackers.com subdomain over HTTPS
**Priority**: Medium
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no

**Description**:
* Goal: `https://pupper.bostonrobothackers.com` reaches the Pupper project
  page (`content/projects/pupper.md`, built to
  `output/projects/pupper.html`) with a valid TLS cert — no browser
  warning.
* **Root cause**: this repo's GitHub Pages site already owns the apex
  domain `bostonrobothackers.com` as its one allowed custom domain. A
  *second* hostname like `pupper.bostonrobothackers.com` needs its own
  Pages site to get its own cert. Namecheap's "URL Redirect Record" (what's
  configured today) is a parking-page forward that only listens on port 80
  — it can't present a valid cert for the subdomain at all, which is why
  `http://` works and `https://` doesn't. This is a DNS/hosting-topology
  limitation, not a bug in this site's build.
* **Chosen design** — a second, minimal GitHub Pages redirect site:
  * A new, separate public GitHub repo (suggested: `brh-pupper-redirect`)
    holding one static `index.html` (meta-refresh + fallback link to the
    live Pupper page) and one `CNAME` file (`pupper.bostonrobothackers.com`).
  * Namecheap's `pupper` host record changes from *URL Redirect Record* to
    a plain **CNAME Record** pointing at `<github-username>.github.io.` —
    a genuine CNAME to GitHub's own edge, so GitHub can auto-issue a
    Let's Encrypt cert for that exact hostname the same way it does for
    the main site.
  * Enable "Enforce HTTPS" on the new repo's Pages settings once GitHub's
    DNS check passes.
* **Why this over the alternatives** (least disruptive to what already
  works):
  * *Moving the whole domain's nameservers to Cloudflare* (free-tier
    proxy + redirect rule) would also fix it, and could serve future
    subdomains more easily, but touches every existing DNS record on
    `bostonrobothackers.com` (apex, any mail/other records) — much larger
    blast radius for a single subdomain redirect.
  * *Adding `pupper` as a second custom domain on this same repo's Pages
    site* isn't possible — GitHub Pages accepts exactly one custom domain
    per repo (the `CNAME` file holds a single hostname).
  * The chosen design touches **zero** files in this repo's build/deploy
    path (`build/`, `templates/`, `.github/workflows/deploy.yml`) and
    **zero** existing DNS records other than the one `pupper` host record
    that's already broken.
* This repo (`brh-website-2`) only holds the *source* of the redirect
  page (`ops/pupper-redirect/`) for version history — the actual serving
  happens from the new, separate repo, since GitHub Pages requires the
  `CNAME`/`index.html` to live in the repo that owns that hostname.
* Most steps are manual actions in the Namecheap and GitHub UIs — outside
  what an agent can execute. Each such task is marked so in the task file
  with what to verify instead of an automated test.

**Non-goals**:
* No change to `build/`, `templates/`, `css/`, or `.github/workflows/deploy.yml`
  in this repo.
* No move of `bostonrobothackers.com`'s nameservers off Namecheap.
* No general-purpose subdomain-redirect system for future subdomains —
  this feature solves `pupper` only; a repeat of this pattern for another
  subdomain would be its own feature.

## How to Demo
**Setup**: DNS change propagated (can take minutes to a few hours) and the
new redirect repo's Pages custom domain shows "Enforce HTTPS" enabled.

**Steps**:
1. In a browser, load `https://pupper.bostonrobothackers.com`.
2. Confirm no certificate warning.
3. Confirm it lands on (or redirects to) the live Pupper project page.
4. `curl -sI https://pupper.bostonrobothackers.com` — TLS handshake
   succeeds, no `-k`/`--insecure` needed.

**Expected output**: subdomain loads over HTTPS with a browser-trusted
cert and shows the Pupper project content; `http://pupper.bostonrobothackers.com`
(if still reachable) is no longer the only working scheme.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
