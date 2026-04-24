# Swamp Fox Dashboard

This folder is the mount point for the Swamp Fox Agency internal dashboard
(originally from https://github.com/bensachwitz-ctrl/SFA-dash).

## How to drop in `SFA-dash`

From the root of this repo on your local machine:

```bash
git clone https://github.com/bensachwitz-ctrl/SFA-dash.git /tmp/sfa-dash
rm -rf dashboard
cp -r /tmp/sfa-dash dashboard
rm -rf dashboard/.git
git checkout -b import-dashboard
git add dashboard
git commit -m "Import SFA-dash into /dashboard"
git push -u origin import-dashboard
```

Or in the GitHub web UI: download SFA-dash as a ZIP, unzip, then use
"Add file" → "Upload files" on this repo and drag the unzipped folder
(renamed to `dashboard`) into the upload area.

## Shared data lake

Both the public site (contact forms, quote requests, newsletter signups)
and this dashboard read/write the same backend, configured in
`dashboard/config.js`. Update that file once to point at the production
OneLake / Fabric / Supabase / Airtable endpoint and both halves of the
app stay in sync.

## Shared navigation

Once `SFA-dash` is imported, the public site automatically exposes a
"Dashboard" link in the footer nav that routes here. The link is gated
by a password stored in `dashboard/config.js` (`DASHBOARD_PASSWORD`) —
not secure against determined attackers, but enough to keep the public
site from exposing the admin UI. For real security move the dashboard
behind Cloudflare Access or a Vercel/Netlify auth wall.

## Files expected after import

- `dashboard/index.html` — dashboard entry point
- `dashboard/config.js` — shared data-layer config (already scaffolded)
- `dashboard/app.*` — dashboard application bundle
- plus any assets SFA-dash ships with

## What happens if the folder is empty

If nothing has been imported yet, the stub `dashboard/index.html`
renders a placeholder that links back to the main site, so a direct
visit to `/dashboard/` doesn't 404.
