# QuadIQ Advisory — Website

Professional website for **QuadIQ Advisory Private Limited**.

## Brand

- **Colors:** Navy `#1a2438`, Cream `#f0f4e1`
- **Tagline:** Global Reach · Local Depth
- **Assets:** `public/assets/logo.png` (navy, transparent), `logo-light.png` (cream, for dark footer), `favicon.png`
- To re-process from a raw export, save it as `public/assets/logo-source.png` and run `python3 scripts/process-logo.py`

## Run locally

From this folder:

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

Or use any static file server (e.g. `npx serve .`).

## Structure

- `index.html` — single-page site (About, Services, Contact)
- `css/styles.css` — responsive styles
- `js/main.js` — navigation, form handling, scroll animations

## Contact (on site)

- **Anshum:** +91 88604 03399
- **Ankit:** +91 88601 50035
- **Office:** 27-28, Phase IV, Udyog Vihar, Sector 18, Gurugram, Haryana 122015

## SEO

| File | Purpose |
|------|---------|
| `robots.txt` | Search engine crawl rules |
| `sitemap.xml` | URL map for Google / Bing |
| `site.webmanifest` | Mobile / PWA metadata |
| `seo/site.config.json` | Business URL, keywords, address (edit before launch) |
| `seo/structured-data.json` | Schema.org reference |
| `seo/README.md` | Pre-launch checklist |

Update your live domain in `seo/site.config.json`, then run:

```bash
python3 scripts/generate-seo.py
```

Replace `public/assets/og-image.jpg` with a **1200×630** image for social link previews.

## Deploy

Upload the project root to any static host (Netlify, Vercel, GitHub Pages, S3, etc.). No build step required.

Ensure `robots.txt` and `sitemap.xml` are served from the site root. Submit the sitemap in [Google Search Console](https://search.google.com/search-console).

To wire the contact form to email, connect it to Formspree, Netlify Forms, or your backend API.
