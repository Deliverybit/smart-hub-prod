"""Home entry routing: desktop -> NYSE Top 10; mobile/tablet -> landing + tab nav."""

from __future__ import annotations

import json
import re

import streamlit as st

DEFAULT_SCREENER_PAGE = "pages/1_NYSE_Top_10.py"
TERMS_PAGE = "pages/7_Terms_of_Service.py"
HOME_PAGE = "app.py"
RESPONSIVE_MAX_WIDTH = 1366

# Mobile/tablet top tabs: home + one tab per market (Terms linked from gating copy).
APP_NAV_PAGES: tuple[tuple[str, str], ...] = (
    (HOME_PAGE, "🏠 Home"),
    ("pages/1_NYSE_Top_10.py", "📊 NYSE"),
    ("pages/2_NASDAQ_Top_10.py", "💹 NASDAQ"),
    ("pages/3_Crypto_Top_10.py", "🪙 Crypto"),
    ("pages/5_CME_Top_10.py", "🌾 CME"),
    ("pages/6_ICE_Top_10.py", "🛢️ ICE"),
)

HOME_NAV_MARKETS: tuple[tuple[str, str], ...] = (
    ("pages/1_NYSE_Top_10.py", "📊 NYSE 10"),
    ("pages/2_NASDAQ_Top_10.py", "💹 NASDAQ 10"),
    ("pages/3_Crypto_Top_10.py", "🪙 Crypto 10"),
    ("pages/5_CME_Top_10.py", "🌾 CME Commodities 10"),
    ("pages/6_ICE_Top_10.py", "🛢️ ICE Commodities 10"),
)

# Market screener paths (mobile/tablet: visit home first, then consent on these pages).
MOBILE_MARKET_SCREENER_PAGES: frozenset[str] = frozenset(path for path, _ in HOME_NAV_MARKETS)

# Session flag: user has opened the mobile/tablet home (required before market pages).
MOBILE_HOME_SEEN_KEY = "_scoop_mobile_home_seen"
# Browser tab flag — survives Streamlit session remints on multipage URL loads.
MOBILE_HOME_SEEN_STORAGE = "scoop-mobile-home-seen"
# Set when phone/tablet consent Disclaimer & Terms is clicked; Terms must stay responsive.
TERMS_FORCE_RESPONSIVE_STORAGE = "scoop-terms-force-responsive"

SCOOP_52_DESCRIPTION = (
    "Screen major markets for assets trading at or near their 52-week lows — "
    "with headline sentiment checks to filter out fraud and bankruptcy signals."
)

# Backward-compatible alias (legacy landing labels).
HOME_MARKET_CARDS = HOME_NAV_MARKETS + ((TERMS_PAGE, "📜 Terms of Service"),)


def _large_tablet_home_detect_js() -> str:
    """iPad Mini, iPad 13 / Pro 12.9–13, and Surface Pro 10 (incl. Chrome presets)."""
    return (
        "(() => {"
        "  const win = (window.parent && window.parent !== window) ? window.parent : window;"
        "  const store = (() => { try { return win.sessionStorage || sessionStorage; } catch (e) { return null; } })();"
        "  const KEY = 'scoop_home_device_family';"
        "  const w = win.innerWidth || 0;"
        "  const h = win.innerHeight || 0;"
        "  const shortSide = Math.min(w, h);"
        "  const longSide = Math.max(w, h);"
        "  let ipadMini = shortSide >= 700 && shortSide <= 820 && longSide >= 980 && longSide <= 1200;"
        "  let ipad13 = shortSide >= 980 && shortSide <= 1060 && longSide >= 1160 && longSide <= 1420;"
        "  let surfacePro10 = "
        "(shortSide >= 880 && shortSide <= 1000 && longSide >= 1260 && longSide <= 1500) || "
        "(shortSide >= 1240 && shortSide <= 1320 && longSide >= 1760 && longSide <= 2000);"
        "  let family = ipadMini ? 'mini' : (ipad13 ? 'ipad13' : (surfacePro10 ? 'surface' : ''));"
        "  try {"
        "    const stored = store ? (store.getItem(KEY) || '') : '';"
        "    if (!family && stored) family = stored;"
        "    if (family && store) store.setItem(KEY, family);"
        "  } catch (e) {}"
        "  ipadMini = family === 'mini';"
        "  ipad13 = family === 'ipad13';"
        "  surfacePro10 = family === 'surface';"
        "  return {w, h, ipadMini, ipad13, surfacePro10, match: !!(ipadMini || ipad13 || surfacePro10)};"
        "})()"
    )


def _responsive_viewport_js() -> str:
    return (
        "(() => {"
        f"  const info = {_large_tablet_home_detect_js()};"
        f"  return ((info.w || 0) <= {RESPONSIVE_MAX_WIDTH} || info.match) ? '1' : '0';"
        "})()"
    )


def _home_mini_type_flag_script() -> str:
    return (
        "<script>(function(){"
        "  const apply = function() {"
        f"    const info = {_large_tablet_home_detect_js()};"
        "    const roots = [document.documentElement];"
        "    try { if (window.parent && window.parent.document) roots.push(window.parent.document.documentElement); } catch (e) {}"
        "    roots.forEach((root) => {"
        "      if (!root) return;"
        "      if (info.ipadMini) root.setAttribute('data-scoop-home-ipad-mini','1');"
        "      if (info.ipad13) root.setAttribute('data-scoop-home-mini-type','1');"
        "      if (info.surfacePro10) root.setAttribute('data-scoop-home-surface-pro10','1');"
        "    });"
        "  };"
        "  apply();"
        "  const win = (window.parent && window.parent !== window) ? window.parent : window;"
        "  if (!win.__scoopHomeDeviceFlagsBound) {"
        "    win.__scoopHomeDeviceFlagsBound = true;"
        "    win.addEventListener('resize', apply, {passive:true});"
        "    win.addEventListener('orientationchange', apply, {passive:true});"
        "  }"
        "})();</script>"
    )


def _sanitize_widget_key(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", value)


def _nav_viewport_key(page: str | None) -> str:
    return f"scoop_nav_viewport_{_sanitize_widget_key(page or 'app')}"


def _js_eval(expression: str, *, key: str) -> object | None:
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        return None
    try:
        from streamlit.errors import StreamlitAPIException
    except ImportError:
        StreamlitAPIException = Exception  # type: ignore[misc, assignment]
    try:
        return streamlit_js_eval(
            js_expressions=expression,
            key=key,
            want_output=True,
            height=0,
        )
    except StreamlitAPIException:
        return None


def probe_responsive_viewport(*, key: str = "scoop_nav_viewport") -> bool | None:
    """True when layout width is mobile/tablet (<=1366px). None = JS not ready."""
    cache_key = f"_scoop_viewport_cache_{key}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
    except Exception:
        ctx = None
    if ctx is not None:
        started = getattr(ctx, "_scoop_viewport_keys", None)
        if started is None:
            started = set()
            setattr(ctx, "_scoop_viewport_keys", started)
        if key in started:
            cached = st.session_state.get(cache_key)
            return cached if isinstance(cached, bool) else None
        started.add(key)

    value = _js_eval(_responsive_viewport_js(), key=key)
    if value is None:
        return None
    result = str(value).strip() == "1"
    st.session_state[cache_key] = result
    return result


def is_mobile_tablet_viewport(*, page: str | None = None) -> bool:
    """True for mobile/tablet; defaults mobile-safe while the viewport probe is loading."""
    responsive = probe_responsive_viewport(key=_nav_viewport_key(page))
    return responsive is not False


def is_desktop_viewport(*, page: str | None = None) -> bool | None:
    """True for desktop, False for mobile/tablet, None while the JS probe is loading."""
    responsive = probe_responsive_viewport(key=_nav_viewport_key(page))
    if responsive is None:
        return None
    return not responsive


def render_desktop_index_banner(st_module, html: str, *, page: str | None = None) -> None:
    """Render market index cards on every market page (desktop, tablet, and phone)."""
    _ = page
    if not html or not str(html).strip():
        return
    st_module.markdown(html, unsafe_allow_html=True)


def should_render_desktop_top_picks(*, page: str | None = None) -> bool:
    """True only on confirmed desktop. Phone/tablet omit Top Picks entirely."""
    return is_desktop_viewport(page=page) is True


def probe_terms_force_responsive() -> bool | None:
    """True when consent-page Terms navigation requested responsive chrome.

    Returns True/False when known, None while the JS probe is still loading.
    """
    cache_key = "_scoop_terms_force_responsive_cache"
    if cache_key in st.session_state:
        return bool(st.session_state[cache_key])

    value = _js_eval(
        (
            "(() => { try {"
            "  const win = (window.parent && window.parent !== window) ? window.parent : window;"
            f"  return (win.sessionStorage || sessionStorage).getItem('{TERMS_FORCE_RESPONSIVE_STORAGE}') || '';"
            "} catch (e) { return ''; } })()"
        ),
        key="scoop_terms_force_responsive_probe",
    )
    if value is None:
        return None
    forced = str(value).strip() == "1"
    st.session_state[cache_key] = forced
    return forced


def clear_terms_force_responsive_marker() -> None:
    """Clear the one-shot Terms responsive marker after Terms chrome is installed."""
    st.session_state.pop("_scoop_terms_force_responsive_cache", None)
    st.html(
        f"""
<script>
(function() {{
    try {{
        const win = (window.parent && window.parent !== window) ? window.parent : window;
        (win.sessionStorage || sessionStorage).removeItem({json.dumps(TERMS_FORCE_RESPONSIVE_STORAGE)});
    }} catch (e) {{}}
    try {{
        document.documentElement.setAttribute("data-scoop-tab-nav", "1");
        document.documentElement.removeAttribute("data-scoop-desktop-layout");
    }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def resolve_home_entry() -> str | None:
    """Return 'desktop', 'mobile', or None while the viewport probe is loading."""
    responsive = probe_responsive_viewport(key="scoop_home_viewport")
    if responsive is None:
        return None
    return "mobile" if responsive else "desktop"


def mark_mobile_home_seen() -> None:
    """Record that the mobile/tablet home (market tabs) was shown this session/tab."""
    st.session_state[MOBILE_HOME_SEEN_KEY] = True
    st.html(
        f"""
<script>
(function() {{
    try {{
        const win = (window.parent && window.parent !== window) ? window.parent : window;
        (win.sessionStorage || sessionStorage).setItem({json.dumps(MOBILE_HOME_SEEN_STORAGE)}, "1");
    }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def _hydrate_mobile_home_seen_from_storage() -> bool | None:
    """Restore home-seen from sessionStorage.

    Returns True/False when known, None while the JS probe is still loading.
    """
    if st.session_state.get(MOBILE_HOME_SEEN_KEY):
        return True
    value = _js_eval(
        (
            "(() => { try {"
            "  const win = (window.parent && window.parent !== window) ? window.parent : window;"
            f"  return (win.sessionStorage || sessionStorage).getItem('{MOBILE_HOME_SEEN_STORAGE}') || '';"
            "} catch (e) { return ''; } })()"
        ),
        key="scoop_mobile_home_seen_probe",
    )
    if value is None:
        return None
    if str(value).strip() == "1":
        st.session_state[MOBILE_HOME_SEEN_KEY] = True
        return True
    return False


def _mobile_analyze_return_bypass() -> bool:
    """True when returning from Analyze — do not bounce the user back to home."""
    try:
        from legal_consent_logger import (
            ANALYZE_RETURN_QUERY_KEY,
            PENDING_ANALYZE_RETURN_CONSENT,
        )
    except Exception:
        return False
    if st.session_state.get(PENDING_ANALYZE_RETURN_CONSENT):
        return True
    raw = st.query_params.get(ANALYZE_RETURN_QUERY_KEY, "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return str(raw).strip() == "1"


def enforce_mobile_home_before_market(current_page: str | None) -> None:
    """Mobile/tablet only: require home (market tabs) before a screener page.

    Desktop is unchanged. Analyze-return navigations are exempt.
    """
    if not current_page or current_page not in MOBILE_MARKET_SCREENER_PAGES:
        return

    # Honor Analyze-return before the viewport probe. The return query can be
    # present on an early run (responsive still None) and cleared by the terms
    # gate on a later run — waiting for the probe caused a first-click bounce
    # to home on phone/tablet.
    if _mobile_analyze_return_bypass():
        mark_mobile_home_seen()
        return

    # Strict True — do not treat an in-flight viewport probe as mobile.
    responsive = probe_responsive_viewport(key=_nav_viewport_key(current_page))
    if responsive is not True:
        return
    if st.session_state.get(MOBILE_HOME_SEEN_KEY):
        return
    seen = _hydrate_mobile_home_seen_from_storage()
    if seen is True:
        return
    if seen is None:
        # Wait for sessionStorage probe — do not redirect on a false negative.
        st.stop()
        return
    st.switch_page(HOME_PAGE)


def install_responsive_tab_nav() -> None:
    """Enable mobile/tablet tab navigation (hides slide-out sidebar via CSS)."""
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP
    from tooltip_scroll import inject_streamlit_chrome_hide

    inject_streamlit_chrome_hide()
    st.html(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_javascript=True,
    )
    st.html(
        '<script>document.documentElement.setAttribute("data-scoop-tab-nav","1");</script>',
        unsafe_allow_javascript=True,
    )


def render_desktop_sidebar_nav() -> None:
    """Desktop-only sidebar navigation."""
    from branding import logo_path_str
    from theme_mode import render_dark_mode_toggle

    st.sidebar.image(logo_path_str(), use_container_width=True)
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
          <div class="sidebar-brand-row">
            <span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">The Scoop 52</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_dark_mode_toggle()
    st.sidebar.markdown("---")
    for path, label in HOME_NAV_MARKETS:
        st.sidebar.page_link(path, label=label, use_container_width=True)
    st.sidebar.markdown("---")
    st.sidebar.page_link(TERMS_PAGE, label="📜 Terms of Service", use_container_width=True)


def render_mobile_back_home_bar(*, current_page: str | None) -> None:
    """Fixed top-left back link on inner pages; CSS hides on desktop (1367px+)."""
    if not current_page or current_page == HOME_PAGE:
        return
    import importlib
    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    MOBILE_BACK_HOME_BAR = _tml.MOBILE_BACK_HOME_BAR

    st.markdown(
        f'<style id="scoop-mobile-back-home-css">{MOBILE_BACK_HOME_BAR}</style>',
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="scoop-mobile-back-home-bar">'
            '<a class="scoop-mobile-back-home" href="/" target="_self">← Back to Home</a>'
            '<label class="scoop-mobile-fixed-dark" title="Switch light/dark colors.">'
            '<input type="checkbox" id="scoop-mobile-dark-cb" class="scoop-mobile-fixed-dark-cb" />'
            '<span class="scoop-mobile-fixed-dark-switch" aria-hidden="true"></span>'
            '<span class="scoop-mobile-fixed-dark-label">Dark mode</span>'
            "</label>"
            "</div>"
            '<div class="scoop-mobile-back-home-spacer" aria-hidden="true"></div>'
        ),
        unsafe_allow_html=True,
    )
    st.html(
        """
<script>
(function() {
    const STORAGE = "scoop-theme";
    const win = (window.parent && window.parent !== window) ? window.parent : window;
    function docs() {
        const out = [document];
        try {
            if (win.document && win.document !== document) out.push(win.document);
        } catch (e) {}
        return out;
    }
    function roots() {
        return docs().map(function(d) { return d.documentElement; }).filter(Boolean);
    }
    function readDark() {
        try {
            return (win.sessionStorage || sessionStorage).getItem(STORAGE) === "dark";
        } catch (e) {
            return false;
        }
    }
    function syncSheets(dark) {
        docs().forEach(function(doc) {
            const sessionSheet = doc.getElementById("scoop-dark-mode-css");
            if (sessionSheet) {
                sessionSheet.disabled = !dark;
                if (!dark) sessionSheet.textContent = "";
            }
        });
    }
    function apply(dark) {
        // Mobile/tablet only: apply theme in-place. Never location.replace —
        // a full reload clears Streamlit session and re-triggers the terms gate.
        roots().forEach(function(root) {
            root.setAttribute("data-scoop-theme", dark ? "dark" : "light");
            root.classList.toggle("scoop-dark", dark);
        });
        syncSheets(dark);
        try {
            const store = win.sessionStorage || sessionStorage;
            if (dark) store.setItem(STORAGE, "dark");
            else store.removeItem(STORAGE);
            (win.localStorage || localStorage).removeItem(STORAGE);
        } catch (e) {}
        // Keep static dark CSS live; session sheet may be empty until next Streamlit run.
        docs().forEach(function(doc) {
            const staticSheet = doc.getElementById("scoop-theme-static-css");
            if (staticSheet) staticSheet.disabled = false;
        });
    }
    function bind(cb) {
        if (!cb || cb.dataset.scoopThemeBound === "1") return;
        cb.dataset.scoopThemeBound = "1";
        cb.checked = readDark();
        apply(cb.checked);
    }
    function revealDisclaimerBanner(doc) {
        if (!doc || !doc.querySelectorAll) return;
        doc.querySelectorAll(".disclaimer-footer").forEach(function(footer) {
            const slot = footer.closest(
                '[data-testid="stElementContainer"], [data-testid="element-container"]'
            );
            if (!slot) return;
            slot.classList.add("scoop-disclaimer-slot");
            // Inline !important beats stale bootstrap collapse rules until CSS reloads.
            slot.style.setProperty("display", "block", "important");
            slot.style.setProperty("height", "auto", "important");
            slot.style.setProperty("max-height", "none", "important");
            slot.style.setProperty("min-height", "min-content", "important");
            slot.style.setProperty("overflow", "visible", "important");
            slot.style.setProperty("flex", "0 0 auto", "important");
            slot.style.setProperty("flex-shrink", "0", "important");
            footer.style.setProperty("display", "block", "important");
            footer.style.setProperty("visibility", "visible", "important");
            footer.style.setProperty("position", "static", "important");
        });
    }
    function revealAll() {
        docs().forEach(revealDisclaimerBanner);
    }
    function bindAll() {
        docs().forEach(function(doc) {
            bind(doc.getElementById("scoop-mobile-dark-cb"));
        });
    }
    function onThemeChange(ev) {
        const t = ev && ev.target;
        if (t && t.id === "scoop-mobile-dark-cb") apply(t.checked);
    }
    docs().forEach(function(doc) {
        const root = doc.documentElement;
        if (!root || root.dataset.scoopThemeListen === "1") return;
        root.dataset.scoopThemeListen = "1";
        doc.addEventListener("change", onThemeChange, true);
    });
    bindAll();
    revealAll();
    [120, 400, 1000, 2000].forEach(function(ms) {
        setTimeout(function() { bindAll(); revealAll(); }, ms);
    });
    try {
        const obs = new MutationObserver(function() { bindAll(); revealAll(); });
        docs().forEach(function(doc) {
            obs.observe(doc.documentElement, { childList: true, subtree: true });
        });
    } catch (e) {}
})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def render_mobile_inner_top_bar(
    *,
    current_page: str | None,
) -> None:
    """Mobile/tablet inner pages: tab-nav CSS (dark mode lives in the fixed back bar)."""
    if not current_page or current_page == HOME_PAGE:
        return
    import importlib
    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    from theme_mode import inject_dark_mode_styles

    install_responsive_tab_nav()
    inject_dark_mode_styles()
    st.html(
        '<script>document.documentElement.removeAttribute("data-scoop-home-page");</script>',
        unsafe_allow_javascript=True,
    )

    st.html(
        f'<style id="scoop-mobile-inner-top-css">{_tml.MOBILE_INNER_TOP_BAR}</style>'
        f'<style id="scoop-dark-mode-unbox-css">{_tml._MOBILE_TABLET_DARK_MODE_UNBOX_ALWAYS}</style>',
        unsafe_allow_javascript=True,
    )


def render_mobile_back_home_link(*, current_page: str | None) -> None:
    """Backward-compatible alias — use render_mobile_back_home_bar."""
    render_mobile_back_home_bar(current_page=current_page)


def prepare_mobile_home_landing() -> None:
    """Mark the landing page and enable tab-nav CSS before first paint."""
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP
    from tooltip_scroll import inject_streamlit_chrome_hide

    inject_streamlit_chrome_hide()
    st.html(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_javascript=True,
    )
    st.html(
        '<script>'
        'document.documentElement.setAttribute("data-scoop-tab-nav","1");'
        'document.documentElement.setAttribute("data-scoop-home-page","1");'
        '</script>'
        + _home_mini_type_flag_script(),
        unsafe_allow_javascript=True,
    )


def render_mobile_tablet_home() -> None:
    """Mobile/tablet home: sidebar-style landing (logo, title, dark mode, description, nav)."""
    from branding import logo_path_str
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    # Gating sequence only — does not change landing layout.
    mark_mobile_home_seen()
    inject_dark_mode_styles()

    st.markdown('<div class="scoop-mobile-home-shell-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    st.image(logo_path_str(), use_container_width=True)
    st.markdown(
        """
        <div class="sidebar-brand">
          <div class="sidebar-brand-row">
            <span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">The Scoop 52</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="scoop-mobile-inner-top">', unsafe_allow_html=True)
    st.markdown('<div class="scoop-mobile-inner-top-toggle">', unsafe_allow_html=True)
    render_dark_mode_toggle_main(label="Dark mode")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        f'<div class="scoop-home-landing"><p>{SCOOP_52_DESCRIPTION}</p></div>',
        unsafe_allow_html=True,
    )
    for path, label in HOME_NAV_MARKETS:
        st.page_link(path, label=label, use_container_width=True)
    st.markdown("---")
    st.page_link(TERMS_PAGE, label="📜 Terms of Service", use_container_width=True)


def render_mobile_tab_nav_shell(*, current_page: str | None = None) -> None:
    """Mobile/tablet header + horizontal tab bar in the main content area."""
    from branding import logo_path_str
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    install_responsive_tab_nav()
    inject_dark_mode_styles()
    st.html(
        '<script>document.documentElement.removeAttribute("data-scoop-home-page");</script>',
        unsafe_allow_javascript=True,
    )

    st.markdown('<div class="scoop-mobile-nav-shell">', unsafe_allow_html=True)

    header = st.columns([1, 4, 2], gap="small")
    with header[0]:
        st.image(logo_path_str(), width=52)
    with header[1]:
        st.markdown(
            '<p class="scoop-mobile-nav-title">The Scoop 52</p>',
            unsafe_allow_html=True,
        )
    with header[2]:
        st.markdown('<div class="scoop-mobile-nav-toggle">', unsafe_allow_html=True)
        render_dark_mode_toggle_main(label="Dark mode")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="scoop-mobile-tab-row">', unsafe_allow_html=True)
    tab_cols = st.columns(len(APP_NAV_PAGES), gap="small")
    for col, (path, label) in zip(tab_cols, APP_NAV_PAGES):
        with col:
            st.page_link(path, label=label, use_container_width=False)
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_responsive_navigation(*, current_page: str | None = None) -> None:
    """Render desktop sidebar or mobile/tablet chrome — never both."""
    from tooltip_scroll import inject_streamlit_chrome_hide

    inject_streamlit_chrome_hide()
    # Mobile/tablet: home (market tabs) before any screener; consent stays on market pages.
    enforce_mobile_home_before_market(current_page)
    render_mobile_back_home_bar(current_page=current_page)
    render_mobile_inner_top_bar(current_page=current_page)

    # Terms opened from phone/tablet consent: never mount desktop sidebar chrome.
    if current_page == TERMS_PAGE:
        force_responsive = probe_terms_force_responsive()
        if force_responsive is None:
            # Wait for sessionStorage probe — do not flash desktop sidebar.
            st.stop()
            return
        if force_responsive is True:
            # Drop a stale desktop viewport cache from an earlier wide-window visit.
            st.session_state.pop(
                f"_scoop_viewport_cache_{_nav_viewport_key(current_page)}",
                None,
            )
            clear_terms_force_responsive_marker()
            inject_streamlit_chrome_hide()
            return

    # Always mount sidebar nav widgets. Mobile/tablet CSS hides the Streamlit
    # sidebar; desktop must never skip this or navigation is missing entirely
    # when a stale "mobile" viewport cache wins.
    render_desktop_sidebar_nav()
    inject_streamlit_chrome_hide()
