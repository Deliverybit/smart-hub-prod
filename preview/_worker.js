const STATIC = /\.(?:css|js|mjs|png|jpe?g|svg|ico|woff2)$|\/analyze-assets\.json$/i;
const PRIVATE = /^\/(?:admin(?:\.php)?|login)(?:\/|$)/i;
const SESSION = /(?:^|;\s*)(?:session|sessionid|PHPSESSID)=/i;

function hasSessionCookie(request) {
  return SESSION.test(request.headers.get("cookie") || "");
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (STATIC.test(path)) {
      url.search = "";
      const cacheKey = new Request(url.toString(), { method: "GET" });
      const cache = caches.default;
      const hit = await cache.match(cacheKey);
      if (hit) return hit;
      const origin = await env.ASSETS.fetch(cacheKey);
      if (!origin.ok) return origin;
      const headers = new Headers(origin.headers);
      if (path === "/analyze-assets.json") {
        headers.set("Cache-Control", "public, max-age=600, s-maxage=2592000");
        headers.set("CDN-Cache-Control", "public, max-age=2592000");
      } else {
        headers.set("Cache-Control", "public, max-age=2592000");
      }
      const response = new Response(origin.body, {
        status: origin.status,
        statusText: origin.statusText,
        headers,
      });
      ctx.waitUntil(cache.put(cacheKey, response.clone()));
      return response;
    }

    if (PRIVATE.test(path) || hasSessionCookie(request)) {
      const origin = await env.ASSETS.fetch(request);
      const headers = new Headers(origin.headers);
      headers.set("Cache-Control", "private, no-store");
      return new Response(origin.body, {
        status: origin.status,
        statusText: origin.statusText,
        headers,
      });
    }

    if (path.endsWith(".html")) {
      const dest = path.slice(0, -".html".length) || "/";
      const response = new Response(null, {
        status: 308,
        headers: {
          Location: dest + url.search,
          "Cache-Control": "public, max-age=2592000",
        },
      });
      const cache = caches.default;
      ctx.waitUntil(cache.put(request, response.clone()));
      return response;
    }

    const origin = await env.ASSETS.fetch(request);
    const type = origin.headers.get("content-type") || "";
    if (!type.includes("text/html")) return origin;
    const headers = new Headers(origin.headers);
    headers.set(
      "Cache-Control",
      "public, max-age=600, s-maxage=600, stale-while-revalidate=60",
    );
    return new Response(origin.body, {
      status: origin.status,
      statusText: origin.statusText,
      headers,
    });
  },
};
