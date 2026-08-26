#!/usr/bin/env python3
"""Generate blog post pages, the blog listing cards, and the sitemap's blog
entries from content/posts/*.json.

Run this after content/posts/*.json changes (also wired up as the Cloudflare
Pages build command, so it runs automatically on every deploy — including
ones published from the /admin CMS):
    python3 scripts/generate-blog.py

Each file in content/posts/ is one post; the filename (minus .json) becomes
the URL slug, e.g. content/posts/my-post.json -> blog/my-post.html. Plain
text fields (title, category, excerpt, ...) are authored as normal text and
HTML-escaped automatically here — no manual "&amp;" needed. `body` is
Markdown (headings with "##", bullet lists with "-", **bold**, *italic*,
[link text](url)) and is converted to HTML by this script.
"""

import html
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
BLOG_DIR = ROOT / "blog"
BLOG_INDEX = BLOG_DIR / "index.html"
SITEMAP = ROOT / "sitemap.xml"
SITE_URL = "https://quadiqadvisory.com"

CARDS_START = "<!-- POSTS:START -->"
CARDS_END = "<!-- POSTS:END -->"
SITEMAP_START = "  <!-- BLOG-POSTS:START -->"
SITEMAP_END = "  <!-- BLOG-POSTS:END -->"


def esc(text: str) -> str:
    """Escape plain author-entered text for safe use in HTML/attributes."""
    return html.escape(text or "", quote=True)


def load_posts() -> list[dict]:
    posts = []
    for path in POSTS_DIR.glob("*.json"):
        with open(path, encoding="utf-8") as f:
            post = json.load(f)
        post["slug"] = path.stem
        posts.append(post)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def human_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d").date()
    return f"{d.day} {d.strftime('%B')} {d.year}"


def inline_markdown(text: str) -> str:
    """Escape text, then apply the small Markdown subset the CMS's rich-text
    editor produces: **bold**, *italic*/_italic_, and [label](url) links."""
    out = esc(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", out)
    out = re.sub(
        r"\[(.+?)\]\((.+?)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        out,
    )
    return out


def render_body(markdown_text: str) -> str:
    indent = "          "
    blocks = [b.strip() for b in re.split(r"\n\s*\n", markdown_text.strip()) if b.strip()]
    rendered = []
    seen_paragraph = False

    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        first = lines[0]

        if first.startswith("## "):
            rendered.append(f"{indent}<h2>{inline_markdown(first[3:].strip())}</h2>")
        elif first.startswith("### "):
            rendered.append(f"{indent}<h3>{inline_markdown(first[4:].strip())}</h3>")
        elif all(re.match(r"^[-*]\s+", l) for l in lines):
            strip_bullet = re.compile(r"^[-*]\s+")
            items = "\n".join(
                f"{indent}  <li>{inline_markdown(strip_bullet.sub('', l))}</li>" for l in lines
            )
            rendered.append(f"{indent}<ul>\n{items}\n{indent}</ul>")
        else:
            text = inline_markdown(" ".join(lines))
            css_class = ' class="lead"' if not seen_paragraph else ""
            seen_paragraph = True
            rendered.append(f"{indent}<p{css_class}>\n{indent}  {text}\n{indent}</p>")

    return "\n\n".join(rendered)


DEFAULT_CTA = {
    "heading": "Have a question about this?",
    "text": "Get in touch with our team for advice tailored to your business.",
    "primaryLabel": "Contact us",
    "primaryHref": "../index.html#contact",
    "secondaryLabel": "View services",
    "secondaryHref": "../index.html#services",
}


def render_cta(cta: dict | None) -> str:
    cta = cta or DEFAULT_CTA
    return f"""
    <section class="cta-band">
      <div class="container reveal">
        <h2>{esc(cta['heading'])}</h2>
        <p>{esc(cta['text'])}</p>
        <div class="cta-actions">
          <a href="{esc(cta['primaryHref'])}" class="btn btn-gold">{esc(cta['primaryLabel'])}</a>
          <a href="{esc(cta['secondaryHref'])}" class="btn btn-ghost">{esc(cta['secondaryLabel'])}</a>
        </div>
      </div>
    </section>"""


def image_path(post: dict) -> str:
    return post["image"].lstrip("/")


def render_post_html(post: dict) -> str:
    title = post["title"]
    seo = post.get("seo") or {}
    meta_title = seo.get("metaTitle") or f"{title} | QuadIQ Advisory"
    og_title = seo.get("ogTitle") or meta_title
    breadcrumb_label = seo.get("breadcrumbLabel") or title
    canonical = f"{SITE_URL}/blog/{post['slug']}.html"

    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-BCS0HP3KTW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-BCS0HP3KTW');
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(meta_title)}</title>
  <meta name="description" content="{esc(post['metaDescription'])}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{esc(og_title)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE_URL}/public/assets/og-image.jpg" />
  <link rel="icon" href="../public/assets/favicon.png" type="image/png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/styles.css" />
</head>
<body>
  <header class="site-header" id="top">
    <div class="container header-inner">
      <a href="../index.html#top" class="brand" aria-label="QuadIQ Advisory home">
        <img src="../public/assets/logo-light.png" alt="QUAD" class="brand-logo logo" width="120" height="63" data-logo-dark="../public/assets/logo.png" data-logo-light="../public/assets/logo-light.png" />
        <span class="brand-text">QuadIQ Advisory</span>
      </a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">
        <span></span><span></span><span></span>
      </button>
      <nav class="site-nav" id="site-nav" aria-label="Main navigation">
        <a href="../index.html#about">About Us</a>
        <a href="../index.html#services">Services</a>
        <a href="../index.html#approach">Approach</a>
        <a href="index.html">Blog</a>
        <a href="../index.html#faq">FAQs</a>
        <a href="../index.html#contact" class="nav-cta">Contact Us</a>
      </nav>
    </div>
  </header>

  <main id="main-content">
    <section class="page-hero page-hero--article" aria-label="Article">
      <div class="hero-pattern" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="../index.html">Home</a>
          <span class="sep" aria-hidden="true">/</span>
          <a href="index.html">Blog</a>
          <span class="sep" aria-hidden="true">/</span>
          <span aria-current="page">{esc(breadcrumb_label)}</span>
        </nav>
        <span class="blog-category blog-category--hero">{esc(post['category'])}</span>
        <h1>{esc(title)}</h1>
        <p class="article-meta">
          <time datetime="{post['date']}">{human_date(post['date'])}</time>
          <span aria-hidden="true">&middot;</span>
          <span>{esc(post['readTime'])}</span>
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <article class="article-content reveal">
{render_body(post['body'])}
        </article>
      </div>
    </section>
{render_cta(post.get('cta'))}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom">
        <p class="footer-copy">&copy; <span id="year"></span> QuadIQ Advisory Private Limited</p>
        <nav class="footer-legal" aria-label="Footer">
          <a href="index.html">All articles</a>
          <a href="../index.html#faq">FAQs</a>
          <a href="../index.html#contact">Contact Us</a>
        </nav>
      </div>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>
"""


def render_card(post: dict) -> str:
    return f"""          <article class="blog-card reveal">
            <a href="{post['slug']}.html" class="blog-card-link">
              <div class="blog-card-image">
                <img src="../{image_path(post)}" alt="" width="400" height="240" loading="lazy" />
                <span class="blog-category">{esc(post['category'])}</span>
              </div>
              <div class="blog-card-body">
                <time class="blog-date" datetime="{post['date']}">{human_date(post['date'])}</time>
                <h2>{esc(post['title'])}</h2>
                <p>{esc(post['excerpt'])}</p>
                <span class="blog-read-more">Read article</span>
              </div>
            </a>
          </article>"""


def update_between_markers(text: str, start_marker: str, end_marker: str, new_content: str) -> str:
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    if not pattern.search(text):
        raise RuntimeError(f"Markers not found: {start_marker!r} / {end_marker!r}")
    replacement = f"{start_marker}\n{new_content}\n{end_marker}" if new_content else f"{start_marker}\n{end_marker}"
    return pattern.sub(lambda _m: replacement, text, count=1)


def write_post_pages(posts: list[dict]) -> None:
    existing = {p.name for p in BLOG_DIR.glob("*.html") if p.name != "index.html"}
    current = set()
    for post in posts:
        out_path = BLOG_DIR / f"{post['slug']}.html"
        out_path.write_text(render_post_html(post), encoding="utf-8")
        current.add(out_path.name)
        print(f"Wrote {out_path.relative_to(ROOT)}")

    for stale in existing - current:
        (BLOG_DIR / stale).unlink()
        print(f"Removed stale {(BLOG_DIR / stale).relative_to(ROOT)} (no matching content/posts/*.json)")


def update_blog_index(posts: list[dict]) -> None:
    html_text = BLOG_INDEX.read_text(encoding="utf-8")
    cards = "\n".join(render_card(post) for post in posts)
    html_text = update_between_markers(html_text, CARDS_START, CARDS_END, cards)
    BLOG_INDEX.write_text(html_text, encoding="utf-8")
    print("Updated blog/index.html")


def update_sitemap(posts: list[dict]) -> None:
    xml = SITEMAP.read_text(encoding="utf-8")
    latest = posts[0]["date"] if posts else date.today().isoformat()
    entries = [
        f"""  <url>
    <loc>{SITE_URL}/blog/index.html</loc>
    <lastmod>{latest}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.75</priority>
  </url>"""
    ]
    for post in posts:
        entries.append(
            f"""  <url>
    <loc>{SITE_URL}/blog/{post['slug']}.html</loc>
    <lastmod>{post['date']}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>"""
        )
    xml = update_between_markers(xml, SITEMAP_START, SITEMAP_END, "\n".join(entries))
    SITEMAP.write_text(xml, encoding="utf-8")
    print("Updated sitemap.xml")


def main() -> None:
    posts = load_posts()
    write_post_pages(posts)
    update_blog_index(posts)
    update_sitemap(posts)
    print(f"Done. Generated {len(posts)} post page(s).")


if __name__ == "__main__":
    main()
