# SEO setup — QuadIQ Advisory

## Files (deploy all to site root)

| File | Purpose |
|------|---------|
| `robots.txt` | Crawler rules + sitemap URL |
| `sitemap.xml` | URL list for search engines |
| `site.webmanifest` | PWA / mobile browser metadata |
| `seo/site.config.json` | Single source of truth for URLs & business data |
| `seo/structured-data.json` | Schema.org reference (mirrored in `index.html`) |

## Before going live

1. **Domain** — Canonical URL is **`https://quadiqadvisory.com`**.  
   To change it later, edit `seo/site.config.json` → `siteUrl`, then run `python3 scripts/generate-seo.py`.  
   Deploy `_redirects` (Netlify) so `www` and `http` redirect to the apex domain.

2. **Social image** — Replace `public/assets/og-image.jpg` with a **1200×630** branded image for link previews.

3. **Google Search Console** — Verify ownership and submit `sitemap.xml`.

4. **Bing Webmaster Tools** — Submit the same sitemap.

5. **Analytics** — Add Google Analytics / Tag Manager in `index.html` if needed (see comment placeholder).

6. **Optional** — Fill `email` and `social` URLs in `site.config.json`.

## Recommended checks

- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
