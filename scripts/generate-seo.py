#!/usr/bin/env python3
"""Regenerate robots.txt from seo/site.config.json.

Does NOT touch sitemap.xml: that file has pages (services/, blog posts, faq,
privacy-policy) this script doesn't know about, and blog entries there are
owned by scripts/generate-blog.py (look for the BLOG-POSTS markers). Update
sitemap.xml by hand for anything else."""

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
Disallow: /admin/

Sitemap: {base_url.rstrip('/')}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(content, encoding="utf-8")
    print("Updated robots.txt")


def main() -> None:
    cfg = load_config()
    base_url = cfg["siteUrl"]
    write_robots(base_url)
    print(f"Done. Base URL: {base_url}")


if __name__ == "__main__":
    main()
