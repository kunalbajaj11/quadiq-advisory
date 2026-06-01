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

- **CA Rajat Garg:** 7827279427 · carajatgargqiq@gmail.com · [WhatsApp](https://wa.me/917827279427)
- **Office:** 27-28, Phase IV, Udyog Vihar, Sector 18, Gurugram, Haryana 122015
- **Form:** Submissions go to `carajatgargqiq@gmail.com` via [FormSubmit](https://formsubmit.co) — confirm the activation email on first deploy.

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

## Deploy on Cloudflare Pages

This site is static (no build step). Use **Cloudflare Pages** with your domain **quadiqadvisory.com**.

### Option A — Deploy from Git (recommended)

1. Push this folder to **GitHub** or **GitLab** (if not already):
   ```bash
   cd "/Users/kunalbajaj/Documents/QUAD IQ"
   git add .
   git commit -m "Prepare site for Cloudflare Pages"
   git push origin main
   ```

2. Log in to the [Cloudflare dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.

3. Select your repository and use these settings:

   | Setting | Value |
   |---------|--------|
   | **Production branch** | `main` |
   | **Framework preset** | None |
   | **Build command** | *(leave empty)* |
   | **Build output directory** | `/` *(project root — where `index.html` lives)* |

4. Click **Save and Deploy**. You’ll get a `*.pages.dev` URL to preview.

5. **Custom domain:** In the Pages project → **Custom domains** → **Set up a custom domain** → add `quadiqadvisory.com` and `www.quadiqadvisory.com`.

6. **DNS** (if the domain is already on Cloudflare):
   - **quadiqadvisory.com** → Pages will add the required records automatically, or use a **CNAME** to `<your-project>.pages.dev` (flattened to A at apex).
   - **www** → CNAME to `<your-project>.pages.dev`, or use a **Redirect Rule** (below).

7. **Redirect www → apex** (canonical URL is `https://quadiqadvisory.com`):
   - **Rules** → **Redirect Rules** → Create rule:
     - If hostname equals `www.quadiqadvisory.com`
     - Then **Dynamic** redirect to `https://quadiqadvisory.com${uri.path}` with status **301**
   - The repo’s `_redirects` file also works on Cloudflare Pages for path redirects.

8. After go-live, submit **https://quadiqadvisory.com/sitemap.xml** in [Google Search Console](https://search.google.com/search-console).

### Option B — Direct upload (no Git)

1. **Workers & Pages** → **Create** → **Pages** → **Upload assets**.
2. Zip the project (include `index.html`, `css/`, `js/`, `public/`, `robots.txt`, `sitemap.xml`, `_redirects`, `_headers`, `site.webmanifest` at the **root** of the zip).
3. Upload and attach **quadiqadvisory.com** under Custom domains.

### Cloudflare settings checklist

- **SSL/TLS** → **Full (strict)** (default once proxied).
- **Always Use HTTPS** → On.
- **Automatic HTTPS Rewrites** → On.
- **Brotli** → On (faster loads).

### Contact form on Cloudflare

The form uses **FormSubmit** (`formsubmit.co`) to deliver enquiries to `carajatgargqiq@gmail.com`. After first deploy, open the activation link sent to that inbox so submissions are enabled.

## Other hosts

You can also deploy to Netlify, Vercel, or GitHub Pages. The `_redirects` file is tailored for Netlify/Cloudflare-style redirects.

Ensure `robots.txt` and `sitemap.xml` are served from the site root.
