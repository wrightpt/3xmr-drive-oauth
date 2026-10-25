# 3XMR Homelab Drive Backups — public OAuth disclosures

**Public information only.** This repository hosts the homepage, privacy policy,
and terms for a privately operated Google Drive backup OAuth application.
It never hosts backup files, OAuth tokens, private configuration or login services.

## Website

| Page | Source | Expected public URL |
| --- | --- | --- |
| Home | [index.html](./index.html) | https://drive-oauth.3xmr.com/ |
| Privacy | [privacy.html](./privacy.html) | https://drive-oauth.3xmr.com/privacy.html |
| Terms | [terms.html](./terms.html) | https://drive-oauth.3xmr.com/terms.html |
| Styles | [style.css](./style.css) | https://drive-oauth.3xmr.com/style.css |

No frameworks, scripts, third-party fonts, analytics tags, cookies or user input
forms are required. The site is intentionally a static disclosure surface.

## Hosting and DNS

- GitHub Pages: this repository's `main` branch, `/ (root)`.
- Custom domain: `drive-oauth.3xmr.com`.
- Cloudflare DNS **DNS-only** CNAME `drive-oauth` → `wrightpt.github.io`.
  Do not enable a broad tunnel, cluster ingress or wildcard route.
- GitHub profile-level verified domain: `3xmr.com`.
- The Cloudflare TXT record `_github-pages-challenge-wrightpt.3xmr.com`
  must be retained for continuous GitHub Pages domain-owner verification.
- The Google Search Console `3xmr.com` domain property was ownership-verified
  under the operator's account using existing provider verification.
- GitHub Pages may require time to issue the HTTPS certificate. **Do not**
  switch Google OAuth to production until all three public page URLs return
  HTTP 200 with a valid HTTPS certificate. Enforce HTTPS when available.

## Google OAuth application

- Google Cloud project ID: `homelab-gdrive-backups-2026`.
- Brand name: **Homelab Drive Backups**.
- Public app type: owner-operated, **External** audience (not a public service).
- OAuth client type: **Desktop** for rclone on the operator's workstation.
- OAuth client credentials are held only in an encrypted owner-controlled
  `pass` entry (path referenced in private runbooks) and **never** in Git.
- The new Drive API is enabled in the project; private backup publication is
  intentionally separate from this website and remains recovery-gated.

Google OAuth Branding should use **exactly** the homepage/privacy/terms URLs in
the table and add `3xmr.com` as an authorized domain. Google Search Console
ownership is distinct from GitHub Pages domain verification; both were checked.

## Editorial and security rules

- Do not publish screenshots of credentials, Gmail addresses beyond the existing
  public contact, OAuth bearer tokens, refresh tokens, private network endpoints,
  cluster manifests, backup inventories or encryption keys.
- The privacy policy must accurately reflect the app's real data collection,
  Drive scopes, encryption, retention, permitted use and contact channel. Do not
  claim a restore or production backup exists until separately verified.
- Update the effective date and policy text before changing user-data handling.
- Keep the homepage privacy-policy link identical to the Branding privacy URL.
- Review any change to the custom domain, Pages source, or DNS TXT/CNAME.
- For key and recovery workflow follow-ups, see the private platform runbook and
  tracking issue **wrightpt/homelab-gitops#248**.

## Non-secret verification

Before publishing or updating Google Branding, check:
```bash
dig +short @1.1.1.1 drive-oauth.3xmr.com CNAME
dig +short @1.1.1.1 _github-pages-challenge-wrightpt.3xmr.com TXT
for path in / /privacy.html /terms.html; do
  curl --fail --show-error --silent --output /dev/null \
    --write-out "%{http_code} %{ssl_verify_result} %{url_effective}\n" \
    "https://drive-oauth.3xmr.com$path"
done
```

A `200` response and TLS verification value `0` on **all** pages is needed
before publishing the Google OAuth app or claiming the website is fully live.
