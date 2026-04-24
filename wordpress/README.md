# Swamp Fox — WordPress deployment kit

Everything needed to stand the Swamp Fox Insurance Agency site up on WordPress:

```
wordpress/
├── swampfox-wordpress-export.xml   ← 18 pages + 11 blog posts (WXR format)
├── swampfox-theme/                 ← minimal custom theme (matches the static site's look)
│   ├── style.css                   (theme header + site-wide CSS)
│   ├── functions.php               (enqueue, nav registration, fallback menu)
│   ├── header.php                  (topbar + sticky white nav)
│   ├── footer.php                  (compact forest footer)
│   ├── index.php                   (blog / archive fallback)
│   ├── page.php                    (default page template)
│   ├── single.php                  (single blog post template with hero + CTA)
│   └── front-page.php              (home page template)
├── build.py                        ← regenerates the WXR from the static site
└── README.md                       ← this file
```

---

## Deployment — step by step

### 1. Spin up WordPress

Any WP 6.0+ host works (WordPress.com, Bluehost, SiteGround, DigitalOcean,
Local by Flywheel for testing). You just need WP admin access.

### 2. Install & activate the Swamp Fox theme

**Option A — zip and upload via dashboard:**

```bash
cd wordpress
zip -r swampfox-theme.zip swampfox-theme
```

Then `WP Admin → Appearance → Themes → Add New → Upload Theme → swampfox-theme.zip → Install Now → Activate`.

**Option B — SFTP/filesystem:**

Copy the `swampfox-theme/` directory into `wp-content/themes/` on the server,
then activate via `WP Admin → Appearance → Themes`.

### 3. Add the logo

`WP Admin → Appearance → Customize → Site Identity → Select logo`.

Upload the Swamp Fox logo (`images/logo-swamp-fox-nav.webp` from this repo) and
the theme's `header.php` / `footer.php` will use `the_custom_logo()` automatically.

### 4. Import content

`WP Admin → Tools → Import → WordPress → Install Now → Run Importer`.

Upload `wordpress/swampfox-wordpress-export.xml` and:

- **Assign posts to**: an existing admin user or create a new "Swamp Fox" author.
- **Download and import file attachments**: leave unchecked. The images are
  hot-linked to the GitHub Pages site (or your existing CDN). If you want
  them self-hosted, see "Self-host images" below.

Click **Submit**. When done you'll have:

- **18 pages**: Home, Coverage (with subpages Forestry, Trucking, Cargo, GL,
  Homeowners, Auto, Life, Umbrella, Equipment, Camper/RV), Loss Control,
  Summit, About, Locations, FAQ, Privacy Policy.
- **11 blog posts** under the Blog category tree.

### 5. Set the home page

`WP Admin → Settings → Reading` → *A static page* → **Homepage: Home** and
**Posts page: (leave blank or pick "Blog")**.

### 6. Build the primary nav menu

`WP Admin → Appearance → Menus → Create New Menu`:

```
Home
Coverage
Loss Control
Summit
Blog
About
Locations
```

Assign to **Primary Navigation**. Save.

### 7. Configure permalinks

`WP Admin → Settings → Permalinks → Post name`. Save.

That's it — the site should render at your domain with the correct nav,
branding, blog posts, and coverage pages.

---

## Self-host images

If you want the images inside the WP Media Library instead of hot-linked:

1. From this repo, upload everything under `images/` to the WP Media Library
   (`WP Admin → Media → Library → Add New`).
2. Install a search-and-replace plugin (e.g. **Better Search Replace**).
3. Replace `https://bensachwitz-ctrl.github.io/swampfoxweb/images/` → your
   new media URL prefix (e.g. `https://yoursite.com/wp-content/uploads/`).

---

## Regenerating the WXR

The WXR is generated from the static site. To regenerate after content edits:

```bash
python3 wordpress/build.py
```

It rebuilds `swampfox-wordpress-export.xml` from `index.html` and `blog/*.html`.

---

## Notes on the converted content

- **Alpine.js directives** (`x-data`, `x-show`, `@click`, `:class`) are stripped
  during conversion — the content is plain HTML.
- **SPA quote modal / page switching** is replaced with regular anchors to
  `/contact/` and the appropriate slug (e.g. `go('forestry')` → `/forestry-insurance/`).
- **Decorative SVG icons** are removed from blog-post content so the WP
  editor doesn't show raw markup blocks in the post preview.
- **Featured images** are prepended to each blog post body as a wide `<img>`
  so the hero image still renders without a theme that supports
  `_thumbnail_id`. If you're using the included `swampfox-theme`, you can
  remove those and set real featured images after import.

---

## Gotchas

- The import creates the 11 blog post categories from each post's metadata
  (General Liability, Commercial Auto, Auto, Homeowners, Camper / RV, Commercial,
  Forestry Equipment). Don't rename them before import or the posts will end
  up uncategorized.
- If your WP host has a low `upload_max_filesize`, split the WXR into smaller
  chunks. Plugin: **WP All Import** handles large files cleanly.
- The theme's styles rely on Google Fonts (Playfair Display + Inter). If you
  serve from a jurisdiction that requires local-only fonts (GDPR), self-host
  them and swap the `wp_enqueue_style` call in `functions.php`.
