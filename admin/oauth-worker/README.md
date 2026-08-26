# CMS login setup (one-time)

The `/admin` page (Decap CMS) lets someone add blog posts and FAQs through a
form instead of editing JSON files. To do that, it needs to commit changes to
the `kunalbajaj11/quadiq-advisory` GitHub repo on the client's behalf — which
requires a small piece of GitHub-login "glue" since Cloudflare Pages doesn't
have a built-in equivalent to Netlify Identity. This Worker is that glue.
Once it's deployed, nobody touches it again.

You'll need a Cloudflare account (you already have one, for Pages) and
Node.js installed (for the `wrangler` CLI).

## 1. Create a GitHub OAuth App

1. Go to <https://github.com/settings/developers> → **OAuth Apps** → **New OAuth App**.
2. Fill in:
   - **Application name**: `QuadIQ Advisory CMS`
   - **Homepage URL**: `https://quadiqadvisory.com`
   - **Authorization callback URL**: `https://quadiq-cms-auth.<your-subdomain>.workers.dev/callback`
     (you'll know the exact `<your-subdomain>` after step 2 — you can come
     back and edit this field afterwards)
3. Click **Register application**, then **Generate a new client secret**.
4. Keep the **Client ID** and **Client Secret** handy for step 3 — treat the
   secret like a password.

## 2. Deploy the Worker

From this folder:

```bash
cd admin/oauth-worker
npx wrangler login      # opens a browser to connect your Cloudflare account
npx wrangler deploy
```

Wrangler will print the Worker's URL, e.g.
`https://quadiq-cms-auth.your-subdomain.workers.dev`. If you didn't know
your subdomain in step 1, go back and fix the OAuth App's callback URL now —
it must be exactly `<worker-url>/callback`.

## 3. Set the secrets

```bash
npx wrangler secret put GITHUB_CLIENT_ID
npx wrangler secret put GITHUB_CLIENT_SECRET
```

Paste the values from step 1 when prompted. They're stored encrypted by
Cloudflare, not in this repo.

## 4. Point the CMS at the Worker

In [`admin/config.yml`](../config.yml), change:

```yaml
base_url: https://REPLACE-WITH-YOUR-WORKER.workers.dev
```

to your actual Worker URL from step 2. Commit and push — Cloudflare Pages
will redeploy automatically.

## 5. Give the client access to publish

Logging in through `/admin` authenticates as a real GitHub user, and that
user needs permission to push to this repo:

1. The client needs a GitHub account (free, a couple of minutes to create if
   they don't have one).
2. Add them as a collaborator: repo → **Settings** → **Collaborators** →
   **Add people** → invite by their GitHub username or email → they accept
   the invite.
   - Give them the **Write** role — enough to publish content, not admin
     access to repo settings.
3. They never need to see GitHub itself day-to-day — visiting
   `https://quadiqadvisory.com/admin`, they'll click **Login with GitHub**,
   authorize once, and from then on just use the CMS forms.

## 6. Make sure the site rebuilds static blog pages on publish

The CMS only commits JSON files (`content/posts/*.json`, `content/faq.json`).
Turning a new/edited blog post into an actual `blog/<slug>.html` page happens
in `scripts/generate-blog.py`, so that needs to run on every deploy. In the
Cloudflare Pages dashboard, for this project:

- **Settings** → **Builds & deployments** → **Build command**:
  ```
  python3 scripts/generate-blog.py
  ```
- **Build output directory**: `/` (unchanged)

FAQ changes don't need this — they're read live from `content/faq.json` by
the browser, so they show up as soon as the deploy finishes with no
generation step.

## Notes

- This Worker doesn't store or log anything; it only relays the one-time
  OAuth code exchange with GitHub. There's nothing to maintain after setup.
- If you ever need to rotate the GitHub secret, repeat step 3 with the new
  value — no redeploy needed.
- [Sveltia CMS](https://github.com/sveltia/sveltia-cms) is a drop-in,
  actively-developed alternative to Decap CMS that reads the exact same
  `admin/config.yml` and works with this same Worker — if `/admin` ever
  feels dated, swapping the `<script>` tag in `admin/index.html` is the only
  change needed.
