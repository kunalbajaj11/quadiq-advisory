/**
 * GitHub OAuth handshake for the /admin content editor (Decap CMS).
 *
 * Cloudflare Pages has no built-in equivalent to Netlify Identity, so
 * Decap's "github" backend needs something to run the OAuth exchange
 * (GitHub never hands an access token straight to a static page, since that
 * would expose the app's client secret in the browser). This Worker is that
 * something — deploy it once, point admin/config.yml's `base_url` at it, and
 * it handles login for every future editor session. It stores nothing; it
 * only brokers the one-time exchange between GitHub and the CMS popup.
 *
 * Setup steps are in admin/oauth-worker/README.md.
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/auth") {
      const authorizeUrl = new URL("https://github.com/login/oauth/authorize");
      authorizeUrl.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
      authorizeUrl.searchParams.set("redirect_uri", `${url.origin}/callback`);
      authorizeUrl.searchParams.set("scope", "repo,user");
      return Response.redirect(authorizeUrl.toString(), 302);
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      if (!code) return new Response("Missing OAuth code", { status: 400 });

      const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
        }),
      });
      const tokenData = await tokenRes.json();

      if (tokenData.error) {
        return new Response(`GitHub OAuth error: ${tokenData.error_description || tokenData.error}`, {
          status: 400,
        });
      }

      // Decap's popup handshake: the popup posts "authorizing:github" to
      // whichever origin opened it, waits for that origin to reply (proving
      // it's really the CMS and not an arbitrary page), then sends the token.
      const payload = JSON.stringify({ token: tokenData.access_token, provider: "github" });
      const body = `<!DOCTYPE html>
<html><body>
<script>
(function () {
  function receiveMessage(e) {
    window.opener.postMessage(
      'authorization:github:success:${payload.replace(/'/g, "\\'")}',
      e.origin
    );
    window.removeEventListener("message", receiveMessage, false);
  }
  window.addEventListener("message", receiveMessage, false);
  window.opener.postMessage("authorizing:github", "*");
})();
</script>
</body></html>`;

      return new Response(body, { headers: { "Content-Type": "text/html" } });
    }

    return new Response("Not found", { status: 404 });
  },
};
