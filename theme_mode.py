"""Dark mode toggle and color-only theme support across all viewports."""

from __future__ import annotations

import json
import re

import streamlit as st

from admin_tools.dark_mode_css import DARK_MODE_CSS

SESSION_KEY = "scoop_dark_mode"
TOGGLE_KEY = "scoop_dark_mode_toggle"
MAIN_TOGGLE_KEY = "scoop_dark_mode_toggle_main"
STORAGE_KEY = "scoop-theme"
HYDRATED_KEY = "_scoop_theme_hydrated"
PAGE_KEY = "_scoop_theme_page"
SKIP_HYDRATE_KEY = "_scoop_theme_skip_hydrate"
WRITE_SEQ_KEY = "_scoop_theme_write_seq"
# Parent sessionStorage: same-origin Streamlit iframes each have their own
# sessionStorage, so iframe writes never stick. New browser tab still starts light.
_BROWSER_STORAGE = "sessionStorage"


def is_dark_mode() -> bool:
    """Session preference; defaults to light until hydrated or toggled."""
    return bool(st.session_state.get(SESSION_KEY, False))


def _theme_known_in_session() -> bool:
    return bool(st.session_state.get(HYDRATED_KEY))


def _parent_theme_store_js() -> str:
    """Read/write the parent tab's sessionStorage (shared across Streamlit iframes)."""
    storage = json.dumps(STORAGE_KEY)
    return (
        "function scoopThemeStore() {"
        "  var win = window;"
        "  try { if (window.parent && window.parent !== window) win = window.parent; } catch (e) {}"
        "  try { win.localStorage.removeItem(" + storage + "); } catch (e) {}"
        "  try { return win.sessionStorage || sessionStorage; } catch (e) { return sessionStorage; }"
        "}"
    )


def _set_theme_session(dark: bool, *, touch_toggle_key: bool = True) -> None:
    st.session_state[SESSION_KEY] = dark
    st.session_state[HYDRATED_KEY] = True
    if touch_toggle_key:
        st.session_state[TOGGLE_KEY] = dark
        st.session_state[MAIN_TOGGLE_KEY] = dark


def _calling_page_id() -> str:
    """Identify the active Streamlit page script (changes on sidebar navigation)."""
    import inspect

    for frame in inspect.stack():
        path = frame.filename.replace("\\", "/")
        if "/pages/" in path or path.endswith("/app.py"):
            return path
    return "unknown"


def _storage_read_key() -> str:
    """Unique per page so streamlit_js_eval does not reuse a stale cached value."""
    page = re.sub(r"[^a-zA-Z0-9_]+", "_", _calling_page_id())
    return f"scoop_theme_read_{page}"


def _dark_from_storage_value(stored: object) -> bool:
    """Only an explicit saved 'dark' enables dark mode; everything else is light."""
    return str(stored or "").strip().lower() == "dark"


def _hydrate_theme_from_storage() -> bool:
    """Load theme from sessionStorage into session state. False = js_eval not ready yet."""
    if st.session_state.pop(SKIP_HYDRATE_KEY, False):
        return True

    page = _calling_page_id()
    last_page = st.session_state.get(PAGE_KEY)

    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        if not _theme_known_in_session():
            _set_theme_session(False)
            st.session_state[PAGE_KEY] = page
        return True

    stored = streamlit_js_eval(
        js_expressions=(
            f"(() => {{ {_parent_theme_store_js()} "
            f"  try {{ return scoopThemeStore().getItem('{STORAGE_KEY}') || ''; }} "
            f"  catch (e) {{ return ''; }} "
            f"}})()"
        ),
        key=_storage_read_key(),
        want_output=True,
        height=0,
    )
    if stored is None:
        return False

    raw = str(stored)
    if "|" in raw:
        _prefix, theme_raw = raw.split("|", 1)
    else:
        theme_raw = raw

    should_sync = not _theme_known_in_session() or last_page != page
    if should_sync:
        _set_theme_session(_dark_from_storage_value(theme_raw))
        st.session_state[PAGE_KEY] = page

    return True


def _write_theme_to_storage(theme: str) -> None:
    seq = int(st.session_state.get(WRITE_SEQ_KEY, 0)) + 1
    st.session_state[WRITE_SEQ_KEY] = seq
    _save_theme_preference(theme)


def _session_dark_css() -> str:
    """Dark overrides keyed off html — injected last so they beat page CSS."""
    if not is_dark_mode():
        return ""
    return DARK_MODE_CSS.replace('html[data-scoop-theme="dark"]', "html")


def _inject_static_dark_mode_css() -> None:
    """Inject on every page; only applies when bootstrap sets data-scoop-theme='dark'."""
    css_json = json.dumps(DARK_MODE_CSS)
    st.html(
        f"""
<script>
(function() {{
    const css = {css_json};
    const id = "scoop-theme-static-css";
    function apply(doc) {{
        if (!doc || !doc.documentElement) return;
        let el = doc.getElementById(id);
        if (!el) {{
            el = doc.createElement("style");
            el.id = id;
        }}
        el.textContent = css;
        const root = doc.body || doc.documentElement;
        root.appendChild(el);
    }}
    let parentDoc = null;
    try {{
        parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    }} catch (e) {{
        parentDoc = null;
    }}
    apply(parentDoc || document);
    if (parentDoc && parentDoc !== document) apply(document);
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def _apply_theme_dom(theme: str) -> None:
    payload = json.dumps(theme)
    st.html(
        f"""
<script>
(function() {{
    const theme = {payload};
    function apply(doc) {{
        if (!doc || !doc.documentElement) return;
        const root = doc.documentElement;
        root.setAttribute("data-scoop-theme", theme);
        root.classList.toggle("scoop-dark", theme === "dark");
    }}
    let parentDoc = null;
    try {{
        parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    }} catch (e) {{
        parentDoc = null;
    }}
    apply(parentDoc || document);
    if (parentDoc && parentDoc !== document) apply(document);
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def _save_theme_preference(theme: str) -> None:
    payload = json.dumps("dark" if theme == "dark" else "")
    st.html(
        f"""
<script>
(function() {{
    {_parent_theme_store_js()}
    try {{
        var store = scoopThemeStore();
        if ({payload} === "dark") store.setItem({json.dumps(STORAGE_KEY)}, "dark");
        else store.removeItem({json.dumps(STORAGE_KEY)});
    }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def inject_dark_mode_styles() -> None:
    """Apply dark palette last in the document (after inline page <style> blocks)."""
    css = _session_dark_css()
    css_json = json.dumps(css)
    st.html(
        f"""
<script>
(function() {{
    const css = {css_json};
    const id = "scoop-dark-mode-css";
    function apply(doc) {{
        if (!doc || !doc.documentElement) return;
        let el = doc.getElementById(id);
        if (!css) {{
            if (el) el.remove();
            return;
        }}
        if (!el) {{
            el = doc.createElement("style");
            el.id = id;
        }}
        el.textContent = css;
        const root = doc.body || doc.documentElement;
        root.appendChild(el);
    }}
    const parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    apply(parentDoc || document);
    if (parentDoc && parentDoc !== document) apply(document);
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def _early_theme_bootstrap_script() -> None:
    """Apply session theme to <html> before first paint on every page load."""
    storage = json.dumps(STORAGE_KEY)
    st.html(
        f"""
<script>
(function() {{
    {_parent_theme_store_js()}
    const doc = window.parent && window.parent.document ? window.parent.document : document;
    const root = doc.documentElement;
    let theme = "light";
    try {{
        const stored = scoopThemeStore().getItem({storage});
        if (stored === "dark") {{
            theme = "dark";
        }}
    }} catch (e) {{}}
    root.setAttribute("data-scoop-theme", theme);
    root.classList.toggle("scoop-dark", theme === "dark");
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def apply_theme_from_query_param() -> None:
    """Honor ?theme=dark|light once when landing from Analyze links, then drop it."""
    if "theme" not in st.query_params:
        return
    raw = st.query_params.get("theme", "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    theme = str(raw).strip().lower()
    if theme == "dark":
        _set_theme_session(True)
        _write_theme_to_storage("dark")
    elif theme == "light":
        _set_theme_session(False)
        _write_theme_to_storage("light")
    try:
        del st.query_params["theme"]
    except Exception:
        pass


def _apply_current_theme() -> None:
    theme = "dark" if is_dark_mode() else "light"
    _apply_theme_dom(theme)
    inject_dark_mode_styles()


def apply_theme_early() -> None:
    """Inject theme CSS/scripts before main page content renders."""
    apply_theme_from_query_param()
    hydrated = _hydrate_theme_from_storage()
    if not hydrated and not _theme_known_in_session():
        return
    _apply_current_theme()


def install_theme_support() -> None:
    """Hydrate saved preference early; CSS is injected last via inject_dark_mode_styles()."""
    _early_theme_bootstrap_script()
    _inject_static_dark_mode_css()
    apply_theme_early()
    from tooltip_scroll import inject_streamlit_chrome_hide, install_responsive_layout_bootstrap

    inject_streamlit_chrome_hide()
    install_responsive_layout_bootstrap()
    from tooltip_scroll import inject_desktop_sidebar_nav_market

    inject_desktop_sidebar_nav_market()
    inject_streamlit_chrome_hide()


def _on_dark_mode_toggle_change() -> None:
    dark = bool(st.session_state.get(TOGGLE_KEY, False))
    _set_theme_session(dark)
    st.session_state[PAGE_KEY] = _calling_page_id()
    st.session_state[SKIP_HYDRATE_KEY] = True
    _write_theme_to_storage("dark" if dark else "light")


def render_dark_mode_toggle() -> None:
    """Sidebar toggle; persists across pages via sessionStorage + session state."""
    if not _theme_known_in_session():
        return

    if TOGGLE_KEY not in st.session_state:
        st.session_state[TOGGLE_KEY] = is_dark_mode()

    st.sidebar.toggle(
        "Dark mode",
        key=TOGGLE_KEY,
        help="Switch light/dark colors on desktop, tablet, and phone.",
        on_change=_on_dark_mode_toggle_change,
    )
    st.session_state[SESSION_KEY] = bool(st.session_state[TOGGLE_KEY])
    st.session_state[HYDRATED_KEY] = True
    _apply_current_theme()


def render_dark_mode_toggle_main(*, label: str = "Dark") -> None:
    """Main-area toggle for mobile/tablet tab navigation header.

    Always render on first paint so the control is visible before storage
    hydration completes (market inner pages especially).
    """
    main_key = MAIN_TOGGLE_KEY
    if main_key not in st.session_state:
        st.session_state[main_key] = is_dark_mode()

    def _on_main_toggle_change() -> None:
        dark = bool(st.session_state.get(main_key, False))
        _set_theme_session(dark)
        st.session_state[PAGE_KEY] = _calling_page_id()
        st.session_state[SKIP_HYDRATE_KEY] = True
        _write_theme_to_storage("dark" if dark else "light")

    st.toggle(
        label,
        key=main_key,
        help="Switch light/dark colors.",
        on_change=_on_main_toggle_change,
    )
    st.session_state[SESSION_KEY] = bool(st.session_state[main_key])
    st.session_state[HYDRATED_KEY] = True
    _apply_current_theme()


def chart_axis_colors() -> tuple[dict, dict]:
    """Plotly tick/title font colors for current theme."""
    color = "#e2e8f0" if is_dark_mode() else "#111827"
    tick = dict(color=color)
    title = dict(color=color)
    return tick, title


def chart_hoverlabel() -> dict:
    if is_dark_mode():
        return dict(
            bgcolor="#1e293b",
            bordercolor="#475569",
            font=dict(color="#f1f5f9", size=26),
            align="left",
            namelength=-1,
        )
    return dict(
        bgcolor="#ffffff",
        bordercolor="#cbd5e1",
        font=dict(color="#111827", size=26),
        align="left",
        namelength=-1,
    )


def chart_paper_bgcolor() -> str:
    return "#111827" if is_dark_mode() else "#ffffff"


def chart_plot_bgcolor() -> str:
    return "#0b1220" if is_dark_mode() else "#ffffff"


def chart_template() -> str:
    return "plotly_dark" if is_dark_mode() else "plotly_white"
