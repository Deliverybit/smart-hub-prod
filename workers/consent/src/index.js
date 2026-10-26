import postgres from "postgres";

const ALLOWED_ORIGINS = new Set([
  "https://thescoop52.com",
  "https://www.thescoop52.com",
]);

let sql;

function db(env) {
  if (!sql) {
    sql = postgres(env.HYPERDRIVE.connectionString, {
      max: 1,
      fetch_types: false,
      prepare: false,
    });
  }
  return sql;
}

function allowedOrigin(request) {
  const origin = (request.headers.get("Origin") || "").replace(/\/$/, "");
  if (ALLOWED_ORIGINS.has(origin)) return origin;
  const referer = request.headers.get("Referer") || "";
  for (const allowed of ALLOWED_ORIGINS) {
    if (referer === allowed || referer.startsWith(`${allowed}/`)) return allowed;
  }
  return null;
}

function json(status, body, origin) {
  const headers = { "Content-Type": "application/json", "Cache-Control": "no-store" };
  if (origin) {
    headers["Access-Control-Allow-Origin"] = origin;
    headers.Vary = "Origin";
  }
  return new Response(JSON.stringify(body), { status, headers });
}

async function sha256(value) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function isPublicIp(ip) {
  if (!ip || ip === "0.0.0.0" || ip === "::1") return false;
  if (ip.startsWith("10.") || ip.startsWith("192.168.") || ip.startsWith("127.")) return false;
  const second = Number((ip.split(".")[1] || ""));
  if (ip.startsWith("172.") && second >= 16 && second <= 31) return false;
  return true;
}

async function detectVpn(ip, env) {
  if (!isPublicIp(ip)) return { isVpn: null, provider: null };
  const params = new URLSearchParams({ vpn: "1", asn: "1", risk: "1", seen: "1", tag: "scoop52-consent" });
  const key = (env.PROXYCHECK_API_KEY || "").trim();
  if (key) params.set("key", key);
  try {
    const response = await fetch(`https://proxycheck.io/v2/${encodeURIComponent(ip)}?${params}`, {
      signal: AbortSignal.timeout(2500),
    });
    if (!response.ok) return { isVpn: null, provider: null };
    const payload = await response.json();
    const row = payload[ip];
    if (!row || typeof row !== "object") return { isVpn: null, provider: null };
    const flag = String(row.proxy || "").toLowerCase();
    const isVpn = flag === "yes" ? true : flag === "no" ? false : null;
    const provider = row.provider || row.organisation || row.asn || null;
    return { isVpn, provider: provider ? String(provider).slice(0, 255) : null };
  } catch {
    return { isVpn: null, provider: null };
  }
}

function offsetMinutes(timeZone, date) {
  try {
    const raw = new Intl.DateTimeFormat("en-US", {
      timeZone,
      timeZoneName: "shortOffset",
    })
      .formatToParts(date)
      .find((part) => part.type === "timeZoneName")?.value || "";
    const match = raw.match(/GMT([+-])(\d{1,2})(?::(\d{2}))?/);
    if (!match) return 0;
    const sign = match[1] === "-" ? -1 : 1;
    return sign * (Number(match[2]) * 60 + Number(match[3] || 0));
  } catch {
    return 0;
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/consent") {
      return json(404, { error: "not found" });
    }

    const origin = allowedOrigin(request);
    if (request.method === "OPTIONS") {
      if (!origin) return json(403, { error: "forbidden" });
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": origin,
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
          Vary: "Origin",
        },
      });
    }

    if (request.method !== "POST") {
      return json(404, { error: "not found" }, origin);
    }
    if (!origin) return json(403, { error: "forbidden" });

    const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
    const { success } = await env.CONSENT_LIMIT.limit({ key: ip });
    if (!success) return json(429, { error: "too many consent writes" }, origin);

    const length = Number(request.headers.get("Content-Length") || "0");
    if (length <= 0 || length > 4096) {
      return json(400, { error: "invalid consent body" }, origin);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json(400, { error: "invalid consent body" }, origin);
    }
    if (body?.accepted !== true) {
      return json(400, { error: "acceptance is required" }, origin);
    }

    const userAgent = (request.headers.get("User-Agent") || "unknown").slice(0, 2000);
    const acceptLanguage = request.headers.get("Accept-Language") || "unknown";
    const timezoneName = String(body.timezone || "America/Chicago").trim().slice(0, 80) || "America/Chicago";
    const gpc = request.headers.get("Sec-GPC") === "1";
    const now = new Date();
    const fingerprint = await sha256(`${userAgent}|${acceptLanguage}|public`);
    const vpn = await detectVpn(ip, env);

    try {
      await db(env)`
        INSERT INTO legal_consents (
          id, timestamp_utc, timestamp_local, timezone_name, timezone_offset, ip_address, user_agent,
          tos_version, fingerprint_hash, consent_action,
          is_vpn, vpn_service_provider,
          gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode
        ) VALUES (
          ${crypto.randomUUID()},
          ${now},
          ${now},
          ${timezoneName},
          ${offsetMinutes(timezoneName, now)},
          ${ip},
          ${userAgent},
          ${"2026-03-16"},
          ${fingerprint},
          ${"click_wrap_accept"},
          ${vpn.isVpn},
          ${vpn.provider},
          ${gpc},
          ${false},
          ${gpc},
          ${gpc ? "gpc" : ""},
          ${gpc ? "limited" : "standard"}
        )
      `;
    } catch (error) {
      console.error(error instanceof Error ? error.message : "consent insert failed");
      return json(503, { error: "consent was not stored" }, origin);
    }

    return json(201, { ok: true }, origin);
  },
};
