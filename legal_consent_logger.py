"""
legal_consent_logger.py

Automatic legal consent logging for Streamlit click-wrap acceptance.
Stores append-only records in SQLite by default, with optional PostgreSQL
support when DATABASE_URL is configured and psycopg is available.
"""

from __future__ import annotations

import ipaddress
import hashlib
import json
import os
import sqlite3
import uuid
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo

import requests
from vpn_detection import detect_vpn_proxy

_SQLITE_PATH = Path(__file__).resolve().parent / "legal_consents.db"
_DEFAULT_TIMEZONE = os.getenv("CONSENT_DEFAULT_TIMEZONE", "America/Chicago").strip()
TERMS_STORAGE_KEY = "scoop-terms"
ANALYZE_RETURN_QUERY_KEY = "scoop_from_analyze"
ANALYZE_RETURN_STORAGE_KEY = "scoop-return-from-analyze"
PENDING_ANALYZE_RETURN_CONSENT = "_scoop_pending_analyze_return_consent"
POST_CONSENT_COLLAPSE_KEY = "scoop-post-consent-collapse"
MOBILE_CONSENT_VIEW_MAX = 743
RESPONSIVE_MAX_WIDTH = 1366


def _postgres_url() -> str:
    try:
        from app_config import get_database_url

        return get_database_url() or ""
    except Exception:
        return os.getenv("DATABASE_URL", "").strip()


def ensure_timezone_cookie(st_module) -> None:
    """
    Installs a tiny client-side bridge that stores browser timezone and privacy
    signals in cookies. This gives server-side Streamlit code best-effort access
    to end-user timezone and opt-out signals (e.g., GPC/DNT).
    """
    marker_key = "_tz_cookie_bridge_installed"
    if st_module.session_state.get(marker_key):
        return
    st_module.components.v1.html(
        """
        <script>
        (function () {
          try {
            const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
            if (!tz) return;
            const tzOffset = -new Date().getTimezoneOffset();
            document.cookie =
              "scoop_tz=" + encodeURIComponent(tz) + "; path=/; max-age=31536000; samesite=lax";
            document.cookie =
              "scoop_tz_offset=" + encodeURIComponent(String(tzOffset)) + "; path=/; max-age=31536000; samesite=lax";

            // Best-effort privacy signals (may be absent depending on browser).
            // GPC: https://globalprivacycontrol.org/
            const gpc = (typeof navigator.globalPrivacyControl === "boolean" && navigator.globalPrivacyControl) ? "1" : "0";
            document.cookie =
              "scoop_gpc=" + encodeURIComponent(gpc) + "; path=/; max-age=31536000; samesite=lax";

            // DNT: legacy signal; often "1" for enabled.
            const dntRaw = (navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack || "");
            const dnt = (String(dntRaw) === "1" || String(dntRaw).toLowerCase() === "yes") ? "1" : "0";
            document.cookie =
              "scoop_dnt=" + encodeURIComponent(dnt) + "; path=/; max-age=31536000; samesite=lax";
          } catch (e) {}
        })();
        </script>
        """,
        height=0,
    )
    st_module.session_state[marker_key] = True


def _normalized_headers(st_module) -> dict[str, str]:
    headers = {}
    try:
        raw_headers = getattr(getattr(st_module, "context", None), "headers", None)
        if raw_headers:
            for key, value in raw_headers.items():
                headers[str(key).lower()] = str(value)
    except Exception:
        return {}
    return headers


def _get_ip(headers: dict[str, str]) -> str:
    def _clean_candidate(value: str) -> str:
        candidate = (value or "").strip().strip('"').strip("'")
        if not candidate:
            return ""
        # RFC 7239 Forwarded header can include "for=<ip>:<port>" or "[ipv6]:port"
        if candidate.startswith("for="):
            candidate = candidate[4:].strip()
        # Remove brackets around IPv6
        if candidate.startswith("[") and "]" in candidate:
            candidate = candidate[1:candidate.index("]")]
        # Remove :port from IPv4 values
        if candidate.count(":") == 1 and "." in candidate:
            host_part, port_part = candidate.rsplit(":", 1)
            if port_part.isdigit():
                candidate = host_part
        return candidate

    def _valid_ip(value: str) -> str:
        cleaned = _clean_candidate(value)
        if not cleaned:
            return ""
        try:
            return str(ipaddress.ip_address(cleaned))
        except Exception:
            return ""

    forwarded = headers.get("forwarded", "")
    if forwarded:
        # Example: for=203.0.113.60;proto=https;by=203.0.113.43
        first_part = forwarded.split(",")[0]
        for token in first_part.split(";"):
            token = token.strip()
            if token.lower().startswith("for="):
                ip_val = _valid_ip(token)
                if ip_val:
                    return ip_val

    xff = headers.get("x-forwarded-for", "")
    if xff:
        first_hop = xff.split(",")[0].strip()
        ip_val = _valid_ip(first_hop)
        if ip_val:
            return ip_val

    for key in (
        "x-real-ip",
        "cf-connecting-ip",
        "true-client-ip",
        "x-client-ip",
        "x-original-forwarded-for",
        "x-envoy-external-address",
        "fly-client-ip",
        "x-appengine-user-ip",
    ):
        ip_val = _valid_ip(headers.get(key, ""))
        if ip_val:
            return ip_val

    # Local development fallback for localhost runs.
    host = headers.get("host", "").lower()
    if "localhost" in host or host.startswith("127.0.0.1"):
        return "127.0.0.1"
    return "unknown"


def _ensure_sqlite_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS legal_consents (
            id TEXT PRIMARY KEY,
            timestamp_utc TEXT NOT NULL,
            timestamp_local TEXT,
            timezone_name TEXT,
            timezone_offset INTEGER,
            ip_address TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            tos_version TEXT NOT NULL,
            fingerprint_hash TEXT NOT NULL,
            consent_action TEXT NOT NULL,
            is_vpn INTEGER,
            vpn_service_provider TEXT,
            gpc_signal INTEGER,
            manual_opt_out INTEGER,
            opt_out_effective INTEGER,
            opt_out_source TEXT,
            tracking_mode TEXT
        )
        """
    )
    # Backward-compatible upgrades for existing DB files.
    cols = {row[1] for row in conn.execute("PRAGMA table_info(legal_consents)").fetchall()}
    if "timestamp_local" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN timestamp_local TEXT")
    if "timezone_name" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN timezone_name TEXT")
    if "timezone_offset" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN timezone_offset INTEGER")
    if "is_vpn" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN is_vpn INTEGER")
    if "vpn_service_provider" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN vpn_service_provider TEXT")
    if "gpc_signal" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN gpc_signal INTEGER")
    if "manual_opt_out" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN manual_opt_out INTEGER")
    if "opt_out_effective" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN opt_out_effective INTEGER")
    if "opt_out_source" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN opt_out_source TEXT")
    if "tracking_mode" not in cols:
        conn.execute("ALTER TABLE legal_consents ADD COLUMN tracking_mode TEXT")
    conn.execute(
        """
        CREATE TRIGGER IF NOT EXISTS legal_consents_no_update
        BEFORE UPDATE ON legal_consents
        BEGIN
            SELECT RAISE(ABORT, 'legal_consents is append-only');
        END;
        """
    )
    conn.execute(
        """
        CREATE TRIGGER IF NOT EXISTS legal_consents_no_delete
        BEFORE DELETE ON legal_consents
        BEGIN
            SELECT RAISE(ABORT, 'legal_consents is append-only');
        END;
        """
    )
    conn.commit()


def _insert_sqlite(record: dict[str, str]) -> None:
    with sqlite3.connect(_SQLITE_PATH) as conn:
        _ensure_sqlite_schema(conn)
        conn.execute(
            """
            INSERT INTO legal_consents (
                id, timestamp_utc, timestamp_local, timezone_name, timezone_offset, ip_address, user_agent,
                tos_version, fingerprint_hash, consent_action, is_vpn, vpn_service_provider,
                gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["timestamp_utc"],
                record["timestamp_local"],
                record["timezone_name"],
                record["timezone_offset"],
                record["ip_address"],
                record["user_agent"],
                record["tos_version"],
                record["fingerprint_hash"],
                record["consent_action"],
                None if record["is_vpn"] is None else (1 if record["is_vpn"] else 0),
                record["vpn_service_provider"],
                None if record.get("gpc_signal") is None else (1 if record["gpc_signal"] else 0),
                None if record.get("manual_opt_out") is None else (1 if record["manual_opt_out"] else 0),
                None if record.get("opt_out_effective") is None else (1 if record["opt_out_effective"] else 0),
                record.get("opt_out_source"),
                record.get("tracking_mode"),
            ),
        )
        conn.commit()


def _insert_postgres(record: dict[str, str]) -> bool:
    postgres_url = _postgres_url()
    if not postgres_url:
        return False
    try:
        import psycopg
    except Exception:
        return False

    sql_with_vpn = """
        INSERT INTO legal_consents (
            id, timestamp_utc, timestamp_local, timezone_name, timezone_offset, ip_address, user_agent,
            tos_version, fingerprint_hash, consent_action, is_vpn, vpn_service_provider,
            gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode
        )
        VALUES (%s::uuid, %s::timestamptz, %s::timestamptz, %s, %s, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    sql_with_timezone = """
        INSERT INTO legal_consents (
            id, timestamp_utc, timestamp_local, timezone_name, ip_address, user_agent,
            tos_version, fingerprint_hash, consent_action,
            gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode
        )
        VALUES (%s::uuid, %s::timestamptz, %s::timestamptz, %s, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    sql_legacy = """
        INSERT INTO legal_consents (
            id, timestamp_utc, ip_address, user_agent,
            tos_version, fingerprint_hash, consent_action,
            gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode
        )
        VALUES (%s::uuid, %s::timestamptz, %s::inet, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    ip_for_db = record["ip_address"] if record["ip_address"] != "unknown" else "0.0.0.0"
    with psycopg.connect(postgres_url) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    sql_with_vpn,
                    (
                        record["id"],
                        record["timestamp_utc"],
                        record["timestamp_local"],
                        record["timezone_name"],
                        record["timezone_offset"],
                        ip_for_db,
                        record["user_agent"],
                        record["tos_version"],
                        record["fingerprint_hash"],
                        record["consent_action"],
                        record["is_vpn"],
                        record["vpn_service_provider"],
                        record.get("gpc_signal"),
                        record.get("manual_opt_out"),
                        record.get("opt_out_effective"),
                        record.get("opt_out_source"),
                        record.get("tracking_mode"),
                    ),
                )
            except Exception:
                try:
                    cur.execute(
                        sql_with_timezone,
                        (
                            record["id"],
                            record["timestamp_utc"],
                            record["timestamp_local"],
                            record["timezone_name"],
                            ip_for_db,
                            record["user_agent"],
                            record["tos_version"],
                            record["fingerprint_hash"],
                            record["consent_action"],
                            record.get("gpc_signal"),
                            record.get("manual_opt_out"),
                            record.get("opt_out_effective"),
                            record.get("opt_out_source"),
                            record.get("tracking_mode"),
                        ),
                    )
                except Exception:
                    cur.execute(
                        sql_legacy,
                        (
                            record["id"],
                            record["timestamp_utc"],
                            ip_for_db,
                            record["user_agent"],
                            record["tos_version"],
                            record["fingerprint_hash"],
                            record["consent_action"],
                            record.get("gpc_signal"),
                            record.get("manual_opt_out"),
                            record.get("opt_out_effective"),
                            record.get("opt_out_source"),
                            record.get("tracking_mode"),
                        ),
                    )
        conn.commit()
    return True


def _cookie_value(headers: dict[str, str], cookie_name: str) -> str:
    cookie_header = headers.get("cookie", "")
    if not cookie_header:
        return ""
    for part in cookie_header.split(";"):
        item = part.strip()
        if item.startswith(f"{cookie_name}="):
            return unquote(item.split("=", 1)[1]).strip()
    return ""


def _best_effort_bool(value: str) -> bool | None:
    if value is None:
        return None
    lowered = str(value).strip().lower()
    if lowered in ("1", "true", "t", "yes", "y", "on"):
        return True
    if lowered in ("0", "false", "f", "no", "n", "off", ""):
        return False
    return None


def _resolve_opt_out_signals(st_module, headers: dict[str, str]) -> tuple[bool | None, bool | None, bool, str, str]:
    """
    Returns (gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode).
    - gpc_signal: derived from Sec-GPC header and/or `scoop_gpc` cookie (best-effort)
    - manual_opt_out: derived from session state and/or `scoop_manual_opt_out` cookie (best-effort)
    - opt_out_effective: True if any opt-out signal is present/enabled (GPC/DNT/manual)
    - tracking_mode: "essential_only" when opted-out else "standard"
    """
    # Browser GPC can come via request header or our JS-set cookie.
    gpc_header = headers.get("sec-gpc", "").strip()
    gpc_cookie = _cookie_value(headers, "scoop_gpc")
    gpc_signal = None
    if gpc_header:
        gpc_signal = True if gpc_header == "1" else False
    else:
        gpc_signal = _best_effort_bool(gpc_cookie)

    # Legacy DNT: header or our JS-set cookie.
    dnt_header = headers.get("dnt", "").strip()
    dnt_cookie = _cookie_value(headers, "scoop_dnt")
    dnt_signal = None
    if dnt_header:
        dnt_signal = True if dnt_header == "1" else False
    else:
        dnt_signal = _best_effort_bool(dnt_cookie)

    # Manual opt-out: allow Streamlit code to set session_state["manual_opt_out"]
    # or via cookie set by a future UI control.
    manual_cookie = _cookie_value(headers, "scoop_manual_opt_out")
    manual_from_state = st_module.session_state.get("manual_opt_out")
    manual_opt_out = _best_effort_bool(manual_from_state) if manual_from_state is not None else _best_effort_bool(manual_cookie)

    sources: list[str] = []
    if gpc_signal is True:
        sources.append("gpc")
    if dnt_signal is True:
        sources.append("dnt")
    if manual_opt_out is True:
        sources.append("manual")
    opt_out_effective = bool(sources)
    opt_out_source = ",".join(sources) if sources else "none"
    tracking_mode = "essential_only" if opt_out_effective else "standard"
    return gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode


@lru_cache(maxsize=2048)
def _timezone_from_public_ip(ip_value: str) -> str:
    fallback_tz = _DEFAULT_TIMEZONE if _DEFAULT_TIMEZONE else "UTC"
    try:
        ip_obj = ipaddress.ip_address(ip_value)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return fallback_tz
    except Exception:
        return fallback_tz

    try:
        resp = requests.get(
            f"https://ip-api.com/json/{ip_value}?fields=status,timezone",
            timeout=2.0,
        )
        if resp.ok:
            payload = resp.json()
            tz_name = payload.get("timezone", "")
            if payload.get("status") == "success" and tz_name:
                ZoneInfo(tz_name)  # validate
                return tz_name
    except Exception:
        pass
    return fallback_tz


def _resolve_timezone(headers: dict[str, str], ip_address: str) -> str:
    cookie_header = headers.get("cookie", "")
    if cookie_header:
        for part in cookie_header.split(";"):
            item = part.strip()
            if item.startswith("scoop_tz="):
                tz_name = unquote(item.split("=", 1)[1]).strip()
                try:
                    ZoneInfo(tz_name)
                    return tz_name
                except Exception:
                    pass

    for key in ("x-timezone", "timezone", "x-time-zone"):
        tz_name = headers.get(key, "").strip()
        if tz_name:
            try:
                ZoneInfo(tz_name)
                return tz_name
            except Exception:
                continue
    return _timezone_from_public_ip(ip_address)


def _resolve_timezone_offset(headers: dict[str, str], tz_name: str) -> int:
    cookie_header = headers.get("cookie", "")
    if cookie_header:
        for part in cookie_header.split(";"):
            item = part.strip()
            if item.startswith("scoop_tz_offset="):
                raw_val = unquote(item.split("=", 1)[1]).strip()
                try:
                    return int(raw_val)
                except Exception:
                    pass
    try:
        now_utc = datetime.now(timezone.utc)
        offset = now_utc.astimezone(ZoneInfo(tz_name)).utcoffset()
        if offset is not None:
            return int(offset.total_seconds() // 60)
    except Exception:
        pass
    return 0


def _to_local_iso(utc_iso: str, tz_name: str) -> str:
    dt_utc = datetime.fromisoformat(utc_iso)
    try:
        return dt_utc.astimezone(ZoneInfo(tz_name)).isoformat()
    except Exception:
        return dt_utc.isoformat()


def log_terms_acceptance(
    st_module,
    consent_key: str,
    tos_version: str = "2026-03-16",
    consent_action: str = "click_wrap_accept",
) -> None:
    """
    Logs one acceptance event per Streamlit session for a given consent_key.
    """
    marker_key = f"_legal_consent_logged::{consent_key}"
    if st_module.session_state.get(marker_key):
        return

    headers = _normalized_headers(st_module)
    ip_address = _get_ip(headers)
    user_agent = headers.get("user-agent", "unknown")
    accept_language = headers.get("accept-language", "unknown")
    platform_hint = headers.get("sec-ch-ua-platform", "unknown")
    timezone_name = _resolve_timezone(headers, ip_address)
    timezone_offset = _resolve_timezone_offset(headers, timezone_name)
    gpc_signal, manual_opt_out, opt_out_effective, opt_out_source, tracking_mode = _resolve_opt_out_signals(
        st_module,
        headers,
    )

    # Stable fingerprint hash (server-side approximation without login):
    # intentionally excludes per-session/page-specific values so repeat users
    # correlate across visits.
    raw_fp = "|".join(
        (
            user_agent,
            accept_language,
            platform_hint,
        )
    )
    fingerprint_hash = hashlib.sha256(raw_fp.encode("utf-8")).hexdigest()
    is_vpn, vpn_service_provider = detect_vpn_proxy(ip_address)

    record = {
        "id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "timezone_name": timezone_name,
        "timezone_offset": timezone_offset,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "tos_version": tos_version,
        "fingerprint_hash": fingerprint_hash,
        "consent_action": consent_action,
        "is_vpn": is_vpn,
        "vpn_service_provider": vpn_service_provider,
        "gpc_signal": gpc_signal,
        "manual_opt_out": manual_opt_out,
        "opt_out_effective": opt_out_effective,
        "opt_out_source": opt_out_source,
        "tracking_mode": tracking_mode,
    }
    record["timestamp_local"] = _to_local_iso(record["timestamp_utc"], timezone_name)

    try:
        inserted_pg = _insert_postgres(record)
        if not inserted_pg:
            _insert_sqlite(record)
        st_module.session_state[marker_key] = True
    except Exception:
        # Never block user flow on logging failures.
        pass


def terms_accepted(st_module, accepted_key: str) -> bool:
    """Return whether the user accepted terms for this page/session flag."""
    return bool(st_module.session_state.get(accepted_key, False))


def _terms_from_cookie(headers: dict[str, str], consent_key: str) -> bool:
    raw = _cookie_value(headers, TERMS_STORAGE_KEY)
    if not raw:
        return False
    try:
        data = json.loads(raw)
        return bool(data.get(consent_key))
    except (TypeError, ValueError, json.JSONDecodeError):
        return False


def persist_terms_to_browser(consent_key: str) -> None:
    """Remember terms acceptance in a cookie + localStorage (survives full navigations)."""
    import streamlit as st

    ck = json.dumps(consent_key)
    storage = json.dumps(TERMS_STORAGE_KEY)
    # Prefer parent window so mobile/tablet theme reloads can restore consent.
    st.html(
        f"""
<script>
(function() {{
    try {{
        const storageKey = {storage};
        const consentKey = {ck};
        const win = (window.parent && window.parent !== window) ? window.parent : window;
        const doc = win.document || document;
        const store = win.localStorage || localStorage;
        const read = (doc.cookie || "").split(";").map(function(s) {{ return s.trim(); }})
            .find(function(s) {{ return s.indexOf(storageKey + "=") === 0; }});
        let data = {{}};
        if (read) {{
            try {{
                data = JSON.parse(decodeURIComponent(read.split("=")[1]));
            }} catch (e) {{}}
        }}
        if (!Object.keys(data).length) {{
            try {{
                data = JSON.parse(store.getItem(storageKey) || "{{}}") || {{}};
            }} catch (e) {{
                data = {{}};
            }}
        }}
        data[consentKey] = true;
        const encoded = encodeURIComponent(JSON.stringify(data));
        doc.cookie = storageKey + "=" + encoded + "; path=/; max-age=31536000; samesite=lax";
        store.setItem(storageKey, JSON.stringify(data));
    }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def restore_terms_from_browser(
    st_module,
    consent_key: str,
    *,
    session_flag: str | None = None,
) -> bool:
    """Hydrate session terms flags from the scoop-terms cookie when present."""
    flag = session_flag or consent_key
    if terms_accepted(st_module, flag):
        return True

    if _terms_from_cookie(_normalized_headers(st_module), consent_key):
        st_module.session_state[flag] = True
        return True

    return False


def _query_param_flag(st_module, name: str) -> bool:
    raw = st_module.query_params.get(name, "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return str(raw).strip() == "1"


def _probe_analyze_return_storage(st_module, consent_key: str) -> bool:
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        return False

    storage_key = json.dumps(ANALYZE_RETURN_STORAGE_KEY)
    value = streamlit_js_eval(
        js_expressions=(
            f"(() => {{ try {{ return sessionStorage.getItem({storage_key}) || ''; }}"
            " catch (e) { return ''; } })()"
        ),
        key=f"scoop_analyze_return_probe_{consent_key}",
        want_output=True,
        height=0,
    )
    return str(value).strip() == "1"


def _clear_analyze_return_storage(consent_key: str) -> None:
    import streamlit as st

    storage_key = json.dumps(ANALYZE_RETURN_STORAGE_KEY)
    st.components.v1.html(
        f"<script>(function(){{try{{sessionStorage.removeItem({storage_key});}}catch(e){{}}}})();</script>",
        height=0,
    )


def _accept_terms_after_analyze_return(
    st_module,
    consent_key: str,
    flag: str,
) -> bool:
    """Skip the gate when returning from Analyze to the source screener page."""
    pending = st_module.session_state.get(PENDING_ANALYZE_RETURN_CONSENT)
    if pending == consent_key:
        st_module.session_state.pop(PENDING_ANALYZE_RETURN_CONSENT, None)
        restore_terms_from_browser(st_module, consent_key, session_flag=flag)
        if not terms_accepted(st_module, flag):
            st_module.session_state[flag] = True
        return True

    from_query = _query_param_flag(st_module, ANALYZE_RETURN_QUERY_KEY)
    if not from_query:
        return False

    restore_terms_from_browser(st_module, consent_key, session_flag=flag)
    if not terms_accepted(st_module, flag):
        st_module.session_state[flag] = True

    try:
        del st_module.query_params[ANALYZE_RETURN_QUERY_KEY]
    except Exception:
        pass

    _clear_analyze_return_storage(consent_key)
    return True


def mark_post_consent_collapsed_view() -> None:
    """Mobile/tablet: no sidebar overlay after consent when tab navigation is active."""
    import streamlit as st

    storage_key = json.dumps(POST_CONSENT_COLLAPSE_KEY)
    st.components.v1.html(
        f"""
<script>
(function() {{
    try {{
        const w = (window.parent && window.parent.innerWidth) || window.innerWidth || 0;
        if (w > {RESPONSIVE_MAX_WIDTH}) {{
            return;
        }}
        const aw = window.parent || window;
        const doc = aw.document || document;
        if (doc.documentElement.getAttribute("data-scoop-tab-nav") === "1") {{
            return;
        }}
        aw.sessionStorage.setItem({storage_key}, "1");
        aw.sessionStorage.setItem("scoop-responsive-sidebar-ready", "1");
        aw.__scoopSuppressSidebarExpand = Date.now() + 12000;
        if (typeof aw.__scoopClearResponsiveExpandTimers === "function") {{
            aw.__scoopClearResponsiveExpandTimers();
        }}
    }} catch (e) {{}}
}})();
</script>
""",
        height=0,
    )


def inject_mobile_consent_terms_nav_bridge(st_module) -> None:
    """Mobile/tablet: consent-page Terms links navigate in main view (no slide-out sidebar)."""
    script = f"""
(function() {{
    const aw = (window.parent && window.parent !== window && window.parent.document)
        ? window.parent : window;
    const doc = aw.document || document;
    const TERMS_NAV_COLLAPSE_KEY = "scoop-terms-nav-collapse";
    const TERMS_NAV_SUPPRESS_MS = 15000;
    const retargetTermsLinks = () => {{
        doc.querySelectorAll('a[href*="Terms_of_Service"]').forEach((a) => {{
            a.setAttribute("target", "_self");
            a.style.setProperty("pointer-events", "auto", "important");
        }});
    }};
    const mark = () => {{
        try {{
            aw.sessionStorage.setItem(TERMS_NAV_COLLAPSE_KEY, "1");
        }} catch (e) {{}}
        try {{
            aw.sessionStorage.setItem("scoop-responsive-sidebar-ready", "1");
        }} catch (e) {{}}
        aw.__scoopSuppressSidebarExpand = Date.now() + TERMS_NAV_SUPPRESS_MS;
        if (typeof aw.__scoopClearResponsiveExpandTimers === "function") {{
            aw.__scoopClearResponsiveExpandTimers();
        }}
        doc.documentElement.removeAttribute("data-scoop-screener-gated");
        doc.documentElement.removeAttribute("data-scoop-desktop-layout");
        doc.documentElement.setAttribute("data-scoop-tab-nav", "1");
        try {{
            aw.sessionStorage.setItem("scoop-terms-force-responsive", "1");
        }} catch (e) {{}}
        aw.__scoopLayout?.clearDesktopInlineLayout?.();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {{
            sidebar.setAttribute("aria-expanded", "false");
        }}
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (view) {{
            view.style.setProperty("display", "block", "important");
            view.style.setProperty("width", "100%", "important");
            view.style.setProperty("max-width", "100vw", "important");
            view.style.setProperty("flex-direction", "column", "important");
            view.style.setProperty("margin-left", "0", "important");
            view.style.setProperty("padding-left", "0", "important");
        }}
    }};
    const termsHref = (link) => {{
        if (!link) {{
            return "";
        }}
        return `${{link.getAttribute("href") || ""}} ${{link.href || ""}}`;
    }};
    const onClick = (event) => {{
        if (event.type === "touchstart") {{
            return;
        }}
        const w = aw.innerWidth || window.innerWidth || 0;
        if (w > {RESPONSIVE_MAX_WIDTH}) {{
            return;
        }}
        const target = event.target;
        const el = target && target.nodeType === 1 ? target : target && target.parentElement;
        if (!el || typeof el.closest !== "function") {{
            return;
        }}
        let link = el.closest("a");
        if (!link || !/Terms_of_Service/i.test(termsHref(link))) {{
            const box = el.closest('[data-testid="stCheckbox"]');
            const termsLink = box && box.querySelector('a[href*="Terms_of_Service"]');
            if (!termsLink) {{
                return;
            }}
            const x = event.clientX;
            const y = event.clientY;
            if (!Number.isFinite(x) || !Number.isFinite(y)) {{
                return;
            }}
            const r = termsLink.getBoundingClientRect();
            const pad = 8;
            if (x < r.left - pad || x > r.right + pad || y < r.top - pad || y > r.bottom + pad) {{
                return;
            }}
            link = termsLink;
        }}
        if (!link || !/Terms_of_Service/i.test(termsHref(link))) {{
            return;
        }}
        event.preventDefault();
        event.stopPropagation();
        if (typeof event.stopImmediatePropagation === "function") {{
            event.stopImmediatePropagation();
        }}
        if (aw.__scoopTermsNavLock && Date.now() < aw.__scoopTermsNavLock) {{
            return;
        }}
        aw.__scoopTermsNavLock = Date.now() + 1500;
        link.setAttribute("target", "_self");
        mark();
        const href = link.getAttribute("href") || link.href || "/Terms_of_Service";
        const url = /^https?:\\/\\//i.test(href)
            ? href
            : `${{aw.location.origin}}${{href.startsWith("/") ? href : `/${{href}}`}}`;
        aw.location.assign(url);
    }};
    retargetTermsLinks();
    if (aw.__scoopMobileConsentTermsNavVersion !== 7) {{
        if (aw.__scoopMobileConsentTermsNavHandler) {{
            doc.removeEventListener("click", aw.__scoopMobileConsentTermsNavHandler, true);
            doc.removeEventListener("touchstart", aw.__scoopMobileConsentTermsNavHandler, true);
            doc.removeEventListener("pointerdown", aw.__scoopMobileConsentTermsNavHandler, true);
        }}
        aw.__scoopMobileConsentTermsNavHandler = onClick;
        aw.__scoopMobileConsentTermsNavVersion = 7;
        doc.addEventListener("click", aw.__scoopMobileConsentTermsNavHandler, true);
        doc.addEventListener("pointerdown", aw.__scoopMobileConsentTermsNavHandler, true);
    }}
    if (!aw.__scoopMobileConsentTermsRetarget) {{
        aw.__scoopMobileConsentTermsRetarget = true;
        try {{
            new MutationObserver(retargetTermsLinks).observe(doc.documentElement, {{
                childList: true,
                subtree: true,
            }});
        }} catch (e) {{}}
    }}
}})();
"""
    if hasattr(st_module, "html"):
        st_module.html(f"<script>{script}</script>", unsafe_allow_javascript=True)
    else:
        st_module.components.v1.html(f"<script>{script}</script>", height=0)


def render_terms_gate(
    st_module,
    consent_key: str,
    checkbox_label: str,
    *,
    accepted_key: str | None = None,
    warning_text: str = "Please agree to the **Disclaimer & Terms of Service** to view results.",
) -> bool:
    """Show the terms gate when needed; persist acceptance across reruns."""
    flag = accepted_key or consent_key
    if terms_accepted(st_module, flag):
        persisted_key = f"_scoop_terms_persisted::{consent_key}"
        if not st_module.session_state.get(persisted_key):
            persist_terms_to_browser(consent_key)
            st_module.session_state[persisted_key] = True
        return True

    if _accept_terms_after_analyze_return(st_module, consent_key, flag):
        persisted_key = f"_scoop_terms_persisted::{consent_key}"
        if not st_module.session_state.get(persisted_key):
            persist_terms_to_browser(consent_key)
            st_module.session_state[persisted_key] = True
        return True

    st_module.warning(warning_text)
    inject_mobile_consent_terms_nav_bridge(st_module)
    if st_module.checkbox(checkbox_label, key=f"{consent_key}__widget"):
        st_module.session_state[flag] = True
        persist_terms_to_browser(consent_key)
        mark_post_consent_collapsed_view()
        log_terms_acceptance(st_module, consent_key=consent_key)
        st_module.rerun()
    return False

