# WordPress import

This folder ships a ready-to-import **WordPress eXtended RSS** file:

```
blog/wordpress-export.xml
```

It contains all 11 blog posts with titles, publish dates, slugs, categories, and
full HTML body content.

## How to import

1. Sign in to WordPress as an administrator.
2. Go to **Tools → Import**.
3. Under **WordPress**, click **Install Now** (once), then **Run Importer**.
4. Upload `wordpress-export.xml` and click **Upload file and import**.
5. Assign posts to an existing author (or create a new "Swamp Fox" author).
6. Leave **Download and import file attachments** unchecked — images are hot-
   linked from the current site; if you want them self-hosted, upload them to
   the WP Media Library and search-and-replace the URLs afterward.

## What gets imported

- 11 posts, newest-first:
  - General Liability — "Could One Customer Accident Put Your Business at Risk?"
  - Commercial Auto — "How to Insure Service Vans Without Costly Coverage Gaps"
  - Auto — "Black Ice Accidents: What Auto Insurance Really Covers"
  - Homeowners — "Ice, Wind, & Leaks: Will Your Home Insurance Pay Out?"
  - Camper / RV — "Full-Time RVing: Coverage Gaps to Watch For"
  - Commercial Auto — "Fleet vs. Single Work Truck: Coverage Differences"
  - Camper / RV — "Top Reasons You Need Camper Insurance Today"
  - Auto — "Common Auto Insurance Mistakes That Cost Drivers Money"
  - Commercial — "Protect Your Bar with Liquor Liability and More"
  - Forestry Equipment — "Claim Lessons from Storm Season in the Timber Belt"
  - Auto — "Understanding Uninsured & Underinsured Motorist Coverage"
- Categories (matched to the post's section metadata).
- Post slugs identical to the static file names so URLs round-trip.

## Styling

The imported HTML uses classes (`callout`, `coverage-table`, `cta-box-inner`,
etc.). If you want the posts to look like the static version, either:

- Paste the relevant rules from `blog.css` into your WP theme's stylesheet, or
- Use a page builder / block theme that respects the class-based styles.

Otherwise WP's default post styles will render the content cleanly — lists,
tables, headings, and bold text all use standard HTML.

## Rebuilding the export

If you edit the static posts and want to regenerate the WXR:

```
python3 /tmp/build_wxr.py   # or copy the script next to blog/
```

Reads every `blog/*.html`, extracts each `<article class="article-body">` body,
and writes a fresh `wordpress-export.xml`.
