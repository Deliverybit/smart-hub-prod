"""Shared helpers for the Analyze deep-dive page (pages/_Analyze.py)."""

from __future__ import annotations

import streamlit as st

ANALYZE_PAGE_PATH = "/Analyze"
ANALYZE_TICKER_SESSION_KEY = "analyze_deep_dive_ticker"
ANALYZE_SOURCE_SESSION_KEY = "analyze_source_path"
MAIN_SCREENER_PATH = "/NYSE_Top_10"
MAIN_SCREENER_PAGE = "pages/1_NYSE_Top_10.py"

SCREENER_RETURN_PAGES: dict[str, tuple[str, str]] = {
    "/NYSE_Top_10": ("pages/1_NYSE_Top_10.py", "NYSE Top 10"),
    "/NASDAQ_Top_10": ("pages/2_NASDAQ_Top_10.py", "NASDAQ Top 10"),
    "/LSE_Top_10": ("pages/3b_LSE_Top_10.py", "LSE Top 10"),
    "/TSX_Top_10": ("pages/3c_TSX_Top_10.py", "TSX Top 10"),
    "/Crypto_Top_10": ("pages/3_Crypto_Top_10.py", "Crypto Top 10"),
    "/CME_Top_10": ("pages/5_CME_Top_10.py", "CME Top 10"),
    "/ICE_Top_10": ("pages/6_ICE_Top_10.py", "ICE Top 10"),
}

SCREENER_CONSENT_BY_PATH: dict[str, str] = {
    "/NYSE_Top_10": "agree_terms_nyse",
    "/NASDAQ_Top_10": "agree_terms_nasdaq",
    "/LSE_Top_10": "agree_terms_lse",
    "/TSX_Top_10": "agree_terms_tsx",
    "/Crypto_Top_10": "agree_terms_crypto_top10",
    "/CME_Top_10": "agree_terms_cme",
    "/ICE_Top_10": "agree_terms_ice",
}

SCREENER_SNAPSHOT_KEY_BY_PATH: dict[str, str] = {
    "/NYSE_Top_10": "NYSE",
    "/NASDAQ_Top_10": "NASDAQ",
    "/LSE_Top_10": "LSE",
    "/TSX_Top_10": "TSX",
    "/Crypto_Top_10": "CRYPTO",
    "/CME_Top_10": "CME",
    "/ICE_Top_10": "ICE",
}

SCREENER_TERMS_KEYS = (
    "agree_terms_nyse",
    "agree_terms_nasdaq",
    "agree_terms_lse",
    "agree_terms_tsx",
    "agree_terms_crypto_top10",
    "agree_terms_cme",
    "agree_terms_ice",
)


def _raw_query_ticker() -> str:
    if "ticker" not in st.query_params:
        return ""
    raw = st.query_params.get("ticker", "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return str(raw).strip()


def query_param_ticker() -> str:
    """Return ticker from ?ticker= query param or analyze session fallback."""
    raw = _raw_query_ticker()
    if raw:
        normalized = raw.upper()
        st.session_state[ANALYZE_TICKER_SESSION_KEY] = normalized
        return normalized
    cached = st.session_state.get(ANALYZE_TICKER_SESSION_KEY, "")
    return str(cached).strip().upper()


def is_analyze_mode() -> bool:
    return bool(query_param_ticker())


def analyze_screener_snapshot_key() -> str | None:
    """Supabase snapshot key for the screener that opened Analyze."""
    path = _normalize_screener_path(st.session_state.get(ANALYZE_SOURCE_SESSION_KEY, ""))
    return SCREENER_SNAPSHOT_KEY_BY_PATH.get(path)


def is_crypto_analyze_context(screener_key: str | None, ticker: str = "") -> bool:
    """True for Crypto Analyze, or a crypto pair opened on Analyze."""
    if screener_key == "CRYPTO":
        return True
    return str(ticker).upper().endswith("-USD")


def should_stack_crypto_analyze_layout(screener_key: str | None, *, responsive: bool) -> bool:
    """Crypto Analyze phone/tablet: stack 52-week metrics and mood under the price block."""
    return screener_key == "CRYPTO" and bool(responsive)


def screener_terms_accepted() -> bool:
    return any(st.session_state.get(key) for key in SCREENER_TERMS_KEYS)


def _persist_terms_click_js(storage_key: str, consent_key: str) -> str:
    """Inline click handler — must use single-quoted JS strings (no double quotes)."""
    sk = storage_key.replace("'", "\\'")
    ck = consent_key.replace("'", "\\'")
    return (
        "(function(){try{"
        f"var sk='{sk}',k='{ck}',d={{}};"
        "var r=document.cookie.split(';').map(function(s){return s.trim()})"
        ".find(function(s){return s.indexOf(sk+'=')===0});"
        "if(r){try{d=JSON.parse(decodeURIComponent(r.split('=')[1]))}catch(e){}}"
        "d[k]=true;var v=encodeURIComponent(JSON.stringify(d));"
        "document.cookie=sk+'='+v+'; path=/; max-age=31536000; samesite=lax';"
        "localStorage.setItem(sk,JSON.stringify(d));"
        "}catch(e){}})();"
    )


def _mark_analyze_return_js() -> str:
    """Mobile/tablet: land on screener content after Back, not the sidebar overlay."""
    return (
        "try{"
        "var aw=window.parent||window;"
        "aw.sessionStorage.setItem('scoop-return-from-analyze','1');"
        # Must match landing_page.MOBILE_HOME_SEEN_STORAGE so home-first gating
        # does not bounce the first Back tap to the landing page.
        "aw.sessionStorage.setItem('scoop-mobile-home-seen','1');"
        "aw.sessionStorage.setItem('scoop-landing-seen','1');"
        "aw.__scoopSuppressSidebarExpand=Date.now()+10000;"
        "if(typeof aw.__scoopClearResponsiveExpandTimers==='function')"
        "aw.__scoopClearResponsiveExpandTimers();"
        "}catch(e){}"
    )


def inherit_screener_terms_for_analyze() -> None:
    """Analyze is only linked from Top 10 results, which are terms-gated there."""
    if not is_analyze_mode():
        return

    st.session_state["search_terms_accepted"] = True
    path = _normalize_screener_path(st.session_state.get(ANALYZE_SOURCE_SESSION_KEY, ""))
    consent_key = SCREENER_CONSENT_BY_PATH.get(path)
    if not consent_key:
        return

    st.session_state[consent_key] = True
    from legal_consent_logger import PENDING_ANALYZE_RETURN_CONSENT, persist_terms_to_browser

    st.session_state[PENDING_ANALYZE_RETURN_CONSENT] = consent_key
    marker = f"_scoop_analyze_terms_persisted::{consent_key}"
    if not st.session_state.get(marker):
        persist_terms_to_browser(consent_key)
        st.session_state[marker] = True


def peek_query_ticker() -> str:
    """Read ?ticker= without touching session state (for app.py routing)."""
    return _raw_query_ticker().upper()


def stash_analyze_ticker(ticker: str) -> None:
    """Persist ticker across app.py → Analyze navigation."""
    sym = str(ticker).strip().upper()
    if sym:
        st.session_state[ANALYZE_TICKER_SESSION_KEY] = sym


def _normalize_screener_path(raw: str) -> str:
    """Map a URL/path fragment to a known screener route (/NASDAQ_Top_10, …)."""
    path = str(raw or "").strip()
    if not path:
        return ""
    if "?" in path:
        path = path.split("?", 1)[0]
    if "#" in path:
        path = path.split("#", 1)[0]
    path = path.replace("\\", "/")
    if not path.startswith("/"):
        path = f"/{path}"
    cleaned = path.rstrip("/") or "/"
    if cleaned in SCREENER_RETURN_PAGES:
        return cleaned

    parts = [part for part in cleaned.split("/") if part and part not in ("~", "+")]
    for part in reversed(parts):
        candidate = f"/{part}"
        if candidate in SCREENER_RETURN_PAGES:
            return candidate
        lower = candidate.lower()
        for known in SCREENER_RETURN_PAGES:
            if known.lower() == lower:
                return known
    return ""


def inject_analyze_source_restore() -> None:
    """If Analyze loaded without ?from=, recover screener from sessionStorage once."""
    if st.session_state.get(ANALYZE_SOURCE_SESSION_KEY):
        return
    if "from" in st.query_params:
        return
    st.html(
        """
<script>
(() => {
    try {
        const aw = window.parent || window;
        const params = new URLSearchParams(aw.location.search || "");
        if (params.get("from")) return;
        if (!params.get("ticker")) return;
        const saved = aw.sessionStorage.getItem("scoop-analyze-from") || "";
        const known = [
            "/NYSE_Top_10",
            "/NASDAQ_Top_10",
            "/LSE_Top_10",
            "/TSX_Top_10",
            "/Crypto_Top_10",
            "/CME_Top_10",
            "/ICE_Top_10",
        ];
        if (!known.includes(saved)) return;
        params.set("from", saved);
        const next = aw.location.pathname + "?" + params.toString() + (aw.location.hash || "");
        aw.location.replace(next);
    } catch (e) {}
})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def capture_analyze_source_from_query() -> None:
    """Remember which screener page opened Analyze, then drop ?from= from the URL."""
    raw = ""
    if "from" in st.query_params:
        raw = st.query_params.get("from", "")
        if isinstance(raw, list):
            raw = raw[0] if raw else ""
    path = _normalize_screener_path(raw)
    if path in SCREENER_RETURN_PAGES:
        st.session_state[ANALYZE_SOURCE_SESSION_KEY] = path
    if "from" in st.query_params:
        try:
            del st.query_params["from"]
        except Exception:
            pass


def analyze_back_target() -> tuple[str, str]:
    """Return (streamlit page script, button label) for Back navigation."""
    path = _normalize_screener_path(st.session_state.get(ANALYZE_SOURCE_SESSION_KEY, ""))
    if path in SCREENER_RETURN_PAGES:
        page, label = SCREENER_RETURN_PAGES[path]
        return page, label
    return MAIN_SCREENER_PAGE, SCREENER_RETURN_PAGES[MAIN_SCREENER_PATH][1]


def analyze_back_href(page_script: str) -> str:
    """Map a Streamlit page script path to its browser URL."""
    for href, (script, _label) in SCREENER_RETURN_PAGES.items():
        if script == page_script:
            return href
    return MAIN_SCREENER_PATH


def _analyze_back_consent_key() -> str:
    path = _normalize_screener_path(st.session_state.get(ANALYZE_SOURCE_SESSION_KEY, ""))
    return SCREENER_CONSENT_BY_PATH.get(path, "agree_terms_nyse")


def render_analyze_back_button() -> None:
    """Prominent back link for Analyze deep-dive (desktop, tablet, and phone)."""
    import html as html_module

    from legal_consent_logger import ANALYZE_RETURN_QUERY_KEY, TERMS_STORAGE_KEY

    page_script, label = analyze_back_target()
    href = f"{analyze_back_href(page_script)}?{ANALYZE_RETURN_QUERY_KEY}=1"
    consent_key = _analyze_back_consent_key()
    persist_js = _persist_terms_click_js(TERMS_STORAGE_KEY, consent_key)
    return_js = _mark_analyze_return_js()
    st.markdown(
        f"""
<style>
a.scoop-analyze-back {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    margin: 0 0 1rem 0;
    padding: 0.7rem 1.2rem;
    min-height: 44px;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    color: #0f172a !important;
    font-weight: 700;
    font-size: clamp(0.95rem, 2.4vw, 1.15rem) !important;
    line-height: 1.2 !important;
    text-decoration: none !important;
    box-sizing: border-box;
    width: fit-content;
    max-width: 100%;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
}}
a.scoop-analyze-back:hover {{
    background: #e2e8f0;
    border-color: #94a3b8;
    color: #0f172a !important;
}}
html[data-scoop-theme="dark"] a.scoop-analyze-back {{
    background: #1e293b;
    border-color: #475569;
    color: #f1f5f9 !important;
    box-shadow: none;
}}
html[data-scoop-theme="dark"] a.scoop-analyze-back:hover {{
    background: #334155;
    border-color: #64748b;
    color: #ffffff !important;
}}
@media (max-width: 768px) {{
    a.scoop-analyze-back {{
        width: 100%;
        justify-content: center;
        margin-bottom: 0.85rem;
    }}
}}
@media (max-width: 1366px) {{
    a.scoop-analyze-back {{
        font-size: clamp(1.12rem, 2.9vw, 1.38rem) !important;
    }}
}}
@media (min-width: 1367px) {{
    a.scoop-analyze-back {{
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        padding: 0.95rem 1.45rem !important;
        min-height: 3.6rem !important;
    }}
}}
</style>
<a class="scoop-analyze-back" href="{html_module.escape(href, quote=True)}" target="_self"
   onclick="{persist_js}{return_js}">
    ← Back to {html_module.escape(label)}
</a>
""",
        unsafe_allow_html=True,
    )
