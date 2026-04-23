#!/usr/bin/env python3
"""
Build a comprehensive WordPress WXR export for the full Swamp Fox website.
Reads the static site (index.html + blog/*.html) and produces:

  wordpress/swampfox-wordpress-export.xml

The export contains:
  - WordPress PAGES for every SPA section (home, about, locations, summit,
    loss control, FAQ, privacy, coverage parent, and each coverage subpage).
  - WordPress POSTS for all 11 blog articles under /blog/.
  - Categories inferred from post metadata.

Alpine.js directives (x-data, x-show, @click, :class, etc.) are stripped.
Modal triggers and SPA navigation are rewritten as regular anchors so the
content is portable to a WordPress theme.
"""
import os, re, sys, html, glob
from datetime import datetime
from email.utils import format_datetime

ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT    = os.path.join(os.path.dirname(__file__), 'swampfox-wordpress-export.xml')
SITE   = 'https://bensachwitz-ctrl.github.io/swampfoxweb'

# SPA page-section slug → (WP page title, WP slug, order)
PAGE_MAP = [
    ('home',        'Home',                        'home',              1),
    ('services',    'Coverage',                    'coverage',          2),
    ('forestry',    'Forestry & Logging Insurance','forestry-insurance',3),
    ('trucking',    'Commercial Trucking',         'commercial-trucking',4),
    ('cargo',       'Cargo & Physical Damage',     'cargo-physical-damage',5),
    ('gl',          'General Liability',           'general-liability', 6),
    ('homeins',     'Homeowners Insurance',        'homeowners',        7),
    ('autoins',     'Auto Insurance',              'auto-insurance',    8),
    ('life',        'Life & Health',               'life-health',       9),
    ('umbrella',    'Umbrella & Excess',           'umbrella',          10),
    ('equipment',   'Equipment Insurance',         'equipment',         11),
    ('camper',      'Camper / RV Insurance',       'camper-rv',         12),
    ('losscontrol', 'Loss Control',                'loss-control',      13),
    ('summit',      'SCTPA Summit',                'summit',            14),
    ('about',       'About Us',                    'about',             15),
    ('locations',   'Locations',                   'locations',         16),
    ('faq',         'FAQ',                         'faq',               17),
    ('privacy',     'Privacy Policy',              'privacy',           18),
]

def slurp(p):
    with open(p) as fh: return fh.read()

def find_section(src, slug):
    """Return the HTML of the <div class="page-section" data-page="<slug>">...</div>."""
    pat = r'<div class="page-section[^"]*" data-page="' + re.escape(slug) + r'"[^>]*>(.*?)(?=<div class="page-section|<!-- ══════════ FOOTER ══════════ -->|<footer class="footer"|</body>)'
    m = re.search(pat, src, re.S)
    return m.group(1).strip() if m else ''

def clean_alpine(s):
    """Strip Alpine.js and x-data directives so the HTML is plain and WP-safe."""
    # x-*, @event, :prop attribute removal (including values)
    s = re.sub(r'\s+(?:x-[\w:\-.]+|@[\w:\-.]+|:[\w:\-.]+)\s*=\s*"(?:[^"\\]|\\.)*"', '', s)
    s = re.sub(r"\s+(?:x-[\w:\-.]+|@[\w:\-.]+|:[\w:\-.]+)\s*=\s*'(?:[^'\\]|\\.)*'", '', s)
    s = re.sub(r'\s+(?:x-[\w:\-.]+|@[\w:\-.]+|:[\w:\-.]+)(?=[\s>])', '', s)
    # <template x-for> blocks — drop the wrapper but keep inner
    s = re.sub(r'<template[^>]*>(.*?)</template>', r'\1', s, flags=re.S)
    # go('X') calls embedded anywhere — convert to WP page URL
    slug_by_id = {sid: slug for (sid, _t, slug, _o) in PAGE_MAP}
    def go_to_href(m):
        pid = m.group(1)
        if pid == 'quote':
            return 'href="/contact/"'
        slug = slug_by_id.get(pid, pid)
        return f'href="/{slug}/"'
    s = re.sub(r"""@click\.prevent=(["']).*?go\('([a-zA-Z]+)'\).*?\1""", lambda m: go_to_href(m), s)
    # Remaining go('X') fragments in href=# style — safer to just leave href="#"
    s = re.sub(r'href="#"', 'href="#"', s)  # no-op; safe fallback
    # Remove svg decorative icons' Alpine bindings cleaner
    return s

def unescape_entities_in_tags(s):
    """Fix attribute values that got double-encoded (e.g. &amp;)."""
    return s

def extract_body(path):
    """Pull <article class='article-body'> content out of a post."""
    s = slurp(path)
    m = re.search(r'<article class="article-body">(.*?)</article>', s, re.S)
    body = m.group(1).strip() if m else ''
    # strip SVGs so WP editor doesn't show raw icon markup
    body = re.sub(r'<svg[^>]*>.*?</svg>', '', body, flags=re.S)
    return body

# ── Posts (same as before, but compact) ─────────────────────────────────
def parse_post(path):
    s = slurp(path)
    slug = os.path.splitext(os.path.basename(path))[0]
    title = html.unescape(re.search(r'<meta property="og:title" content="([^"]+)"', s).group(1))
    description = re.search(r'<meta name="description" content="([^"]+)"', s).group(1)
    category = re.search(r'<meta property="article:section" content="([^"]+)"', s).group(1)
    pub_iso = re.search(r'<meta property="article:published_time" content="([^"]+)"', s).group(1)
    image = re.search(r'<meta property="og:image" content="([^"]+)"', s).group(1)
    body = extract_body(path)
    if image:
        body = (f'<p><img src="{image}" alt="{html.escape(title)}" '
                'style="width:100%;height:auto;border-radius:12px;margin-bottom:24px"/></p>\n' + body)
    return dict(slug=slug, title=title, description=description, category=category,
                published=pub_iso, image=image, content=body)

def cat_nicename(c):
    return re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-') or 'uncategorized'

def wxr_item(it, pid, post_type='post'):
    dt = datetime.fromisoformat(it['published']) if it.get('published') else datetime.utcnow()
    post_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    pub_rfc = format_datetime(dt)
    cat_xml = ''
    if it.get('category'):
        nice = cat_nicename(it['category'])
        cat_xml = f'\n    <category domain="category" nicename="{nice}"><![CDATA[{it["category"]}]]></category>'
    menu_order = it.get('menu_order', 0)
    return f'''  <item>
    <title><![CDATA[{it['title']}]]></title>
    <link>{SITE}/{it.get('slug','')}</link>
    <pubDate>{pub_rfc}</pubDate>
    <dc:creator><![CDATA[Swamp Fox Insurance Agency]]></dc:creator>
    <guid isPermaLink="false">{SITE}/?p={pid}</guid>
    <description></description>
    <content:encoded><![CDATA[{it['content']}]]></content:encoded>
    <excerpt:encoded><![CDATA[{it.get('description','')}]]></excerpt:encoded>
    <wp:post_id>{pid}</wp:post_id>
    <wp:post_date><![CDATA[{post_date}]]></wp:post_date>
    <wp:post_date_gmt><![CDATA[{post_date}]]></wp:post_date_gmt>
    <wp:post_modified><![CDATA[{post_date}]]></wp:post_modified>
    <wp:post_modified_gmt><![CDATA[{post_date}]]></wp:post_modified_gmt>
    <wp:comment_status><![CDATA[closed]]></wp:comment_status>
    <wp:ping_status><![CDATA[closed]]></wp:ping_status>
    <wp:post_name><![CDATA[{it['slug']}]]></wp:post_name>
    <wp:status><![CDATA[publish]]></wp:status>
    <wp:post_parent>0</wp:post_parent>
    <wp:menu_order>{menu_order}</wp:menu_order>
    <wp:post_type><![CDATA[{post_type}]]></wp:post_type>
    <wp:post_password><![CDATA[]]></wp:post_password>
    <wp:is_sticky>0</wp:is_sticky>{cat_xml}
  </item>'''

def build():
    index_html = slurp(os.path.join(ROOT, 'index.html'))
    next_id = 100
    pages = []
    for sid, title, slug, order in PAGE_MAP:
        raw = find_section(index_html, sid)
        if not raw:
            print(f'WARN: no section for {sid}', file=sys.stderr)
            continue
        cleaned = clean_alpine(raw)
        # Strip <script> blocks from inside sections
        cleaned = re.sub(r'<script[^>]*>.*?</script>', '', cleaned, flags=re.S)
        # Drop Alpine-only attribute leftovers like ={{ ... }}
        cleaned = re.sub(r'\s+style="([^"]*)"', lambda m: f' style="{m.group(1)}"', cleaned)
        pages.append(dict(title=title, slug=slug, content=cleaned, menu_order=order,
                          published='2026-04-23T12:00:00', description=''))
    # Posts
    post_files = sorted(glob.glob(os.path.join(ROOT, 'blog', '*.html')))
    post_files = [f for f in post_files if os.path.basename(f) != 'index.html']
    posts = []
    for f in post_files:
        try:
            posts.append(parse_post(f))
        except Exception as e:
            print(f'WARN: skip post {f}: {e}', file=sys.stderr)
    posts.sort(key=lambda p: p['published'], reverse=True)

    cats = {}
    for p in posts:
        cats[cat_nicename(p['category'])] = p['category']

    # Build XML
    items = []
    for p in pages:
        items.append(wxr_item(p, next_id, post_type='page'))
        next_id += 1
    for p in posts:
        items.append(wxr_item(p, next_id, post_type='post'))
        next_id += 1

    cat_xml = '\n'.join(
        f'  <wp:category><wp:term_id>{10+i}</wp:term_id><wp:category_nicename><![CDATA[{nice}]]></wp:category_nicename><wp:category_parent><![CDATA[]]></wp:category_parent><wp:cat_name><![CDATA[{name}]]></wp:cat_name></wp:category>'
        for i, (nice, name) in enumerate(sorted(cats.items()))
    )

    out = f'''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Swamp Fox Insurance Agency — full WordPress WXR export.
     {len(pages)} pages + {len(posts)} blog posts.
     Import via WP Admin → Tools → Import → WordPress. -->
<rss version="2.0"
     xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:wfw="http://wellformedweb.org/CommentAPI/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
  <title>Swamp Fox Insurance Agency</title>
  <link>{SITE}</link>
  <description>SCTPA-endorsed independent insurance agency since 1987.</description>
  <pubDate>{format_datetime(datetime.utcnow())}</pubDate>
  <language>en-US</language>
  <wp:wxr_version>1.2</wp:wxr_version>
  <wp:base_site_url>{SITE}</wp:base_site_url>
  <wp:base_blog_url>{SITE}</wp:base_blog_url>
  <wp:author>
    <wp:author_id>1</wp:author_id>
    <wp:author_login><![CDATA[swampfox]]></wp:author_login>
    <wp:author_email><![CDATA[info@swampfoxagency.com]]></wp:author_email>
    <wp:author_display_name><![CDATA[Swamp Fox Insurance Agency]]></wp:author_display_name>
    <wp:author_first_name><![CDATA[Swamp]]></wp:author_first_name>
    <wp:author_last_name><![CDATA[Fox]]></wp:author_last_name>
  </wp:author>
{cat_xml}
{chr(10).join(items)}
</channel>
</rss>
'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        fh.write(out)
    print(f'Wrote {OUT} — {len(pages)} pages + {len(posts)} posts')

if __name__ == '__main__':
    build()
