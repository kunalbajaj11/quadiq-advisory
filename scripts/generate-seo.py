#!/usr/bin/env python3
"""Regenerate robots.txt and sitemap.xml from seo/site.config.json."""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "seo" / "site.config.json"
TODAY = date.today().isoformat()


def load_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def write_robots(base_url: str) -> None:
    content = f"""# Generated from seo/site.config.json — do not edit by hand

User-agent: *
Allow: /

Disallow: /scripts/
Disallow: /seo/

Sitemap: {base_url.rstrip('/')}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(content, encoding="utf-8")
    print("Updated robots.txt")


def write_sitemap(base_url: str) -> None:
    base = base_url.rstrip("/")
    fragments = [
        ("", "1.0"),
        ("#about", "0.8"),
        ("#services", "0.9"),
        ("#approach", "0.7"),
        ("#contact", "0.85"),
    ]
    urls = "\n".join(
        f"""  <url>
    <loc>{base}/{frag.lstrip('/')}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        for frag, priority in fragments
    )
    # Fix home URL (empty fragment)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>{base}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en-in" href="{base}/" />
    <xhtml:link rel="alternate" hreflang="en" href="{base}/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/" />
  </url>
  <url>
    <loc>{base}/#about</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base}/#services</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{base}/#approach</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>{base}/#contact</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("Updated sitemap.xml")


def main() -> None:
    cfg = load_config()
    base_url = cfg["siteUrl"]
    write_robots(base_url)
    write_sitemap(base_url)
    print(f"Done. Base URL: {base_url}")


if __name__ == "__main__":
    main()
