"""
Terms of Service & Financial Disclaimer
"""

import streamlit as st
from branding import logo_path_str, render_environment_banner
from landing_page import render_responsive_navigation
from theme_mode import install_theme_support, inject_dark_mode_styles
from tooltip_scroll import install_tooltip_scroll_handler

st.set_page_config(
    page_title="Terms of Service",
    page_icon=logo_path_str(),
    layout="wide",
)
# Phone/tablet: pin tab-nav before paint so consent → Terms never flashes desktop split.
st.html(
    """
<script>
(function() {
    try {
        const win = (window.parent && window.parent !== window) ? window.parent : window;
        const w = win.innerWidth || window.innerWidth || 0;
        document.documentElement.setAttribute("data-scoop-terms-active", "1");
        try { win.document.documentElement.setAttribute("data-scoop-terms-active", "1"); } catch (e) {}
        const forced = (win.sessionStorage || sessionStorage).getItem("scoop-terms-force-responsive") === "1"
            || (win.sessionStorage || sessionStorage).getItem("scoop-terms-nav-collapse") === "1";
        if (w <= 1366 || forced) {
            document.documentElement.setAttribute("data-scoop-tab-nav", "1");
            document.documentElement.removeAttribute("data-scoop-desktop-layout");
            try { win.document.documentElement.setAttribute("data-scoop-tab-nav", "1"); } catch (e) {}
            try { win.document.documentElement.removeAttribute("data-scoop-desktop-layout"); } catch (e) {}
        }
    } catch (e) {}
})();
</script>
""",
    unsafe_allow_javascript=True,
)
render_environment_banner(st)
install_theme_support()
render_responsive_navigation(current_page="pages/7_Terms_of_Service.py")
install_tooltip_scroll_handler()

st.html(
    '<script>document.documentElement.removeAttribute("data-scoop-screener-gated");</script>',
    unsafe_allow_javascript=True,
)

# ── Global responsive styling (shared with other pages) ───────────────
st.markdown(
    """
    <style>
    :root {
        --scoop-sidebar-width: clamp(12rem, 20vw, 36rem);
    }
    /* Sidebar: rem-based width scales with browser zoom; no label clipping */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        min-width: var(--scoop-sidebar-width) !important;
        width: var(--scoop-sidebar-width) !important;
        max-width: min(92vw, 36rem) !important;
        overflow-x: visible !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a,
    [data-testid="stSidebar"] [data-testid="stPageLink"] span,
    [data-testid="stSidebar"] [data-testid="stPageLink"] p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] .stCaption p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }

    /* ===== DESKTOP / HIGH-RES ===== */
    html, body, [class*="css"] {
        font-size: 30px !important;
        line-height: 1.7 !important;
    }
    h1 { font-size: 5rem !important; font-weight: 800 !important; }
    h2 { font-size: 3.2rem !important; }
    h3 { font-size: 2.6rem !important; }
    h4 { font-size: 2.1rem !important; }
    p, li, span { font-size: 1.6rem !important; line-height: 1.75 !important; }
    .stMarkdown p { font-size: 1.6rem !important; }
    /* Desktop: do not inflate empty Streamlit wrappers (was a large top band). */
    @media (min-width: 1367px) {
        [data-testid="stMainBlockContainer"],
        [data-testid="stMainBlockContainer"].block-container,
        section.main > div,
        .block-container {
            padding-top: 0 !important;
        }
        [data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            overflow: hidden !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style):not(:has(h1)):not(:has(h2)):not(:has(.scoop-env-banner)):not(:has(.disclaimer-footer)),
        [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] style):not(:has(h1)):not(:has(h2)):not(:has(.scoop-env-banner)):not(:has(.disclaimer-footer)),
        [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stHtml"]):not(:has(.scoop-env-banner)):not(:has(.disclaimer-footer)),
        [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stHtml"]):not(:has(.scoop-env-banner)):not(:has(.disclaimer-footer)),
        [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[data-testid="stCustomComponentV1"]),
        [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(iframe[data-testid="stCustomComponentV1"]) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }
        [data-testid="stMainBlockContainer"] h1 {
            margin-top: 0 !important;
            margin-bottom: 0.35rem !important;
            font-size: clamp(32px, 2.4vw, 48px) !important;
            line-height: 1.15 !important;
        }
        [data-testid="stMainBlockContainer"] [data-testid="stHeading"] {
            margin: 0 !important;
            padding: 0 !important;
        }
    }
    /* Alerts */
    .stAlert p, [data-testid="stAlert"] p { font-size: 1.6rem !important; }
    /* Captions */
    .stCaption p, [data-testid="stCaptionContainer"] p { font-size: 1.4rem !important; }

    /* Sidebar — larger text & inputs */
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div { font-size: 1.5rem !important; }
    [data-testid="stSidebar"] h1 { font-size: 2.8rem !important; }
    .sidebar-brand {
        font-size: 60px !important;
        font-weight: 400 !important;
        color: #000000 !important;
        line-height: 1.05 !important;
        background: #ffffff !important;
        display: block !important;
        width: calc(100% + 2rem) !important;
        margin: 0.15rem -1rem 0.35rem -1rem !important;
        padding: 0.7rem 1rem !important;
        box-sizing: border-box !important;
        white-space: nowrap !important;
    }
    .sidebar-brand-row {
        display: inline-flex !important;
        align-items: flex-end !important;
        gap: 10px !important;
    }
    .sidebar-brand-text {
        font-size: 60px !important;
        font-weight: 400 !important;
        color: #000000 !important;
        text-decoration: underline !important;
        text-underline-offset: 6px !important;
    }
    [data-testid="stSidebar"] a { font-size: 1.5rem !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    /* ===== MOBILE ===== */
    @media (max-width: 768px) {
        /* Mobile-friendly type scale (desktop unaffected) */
        html, body, [class*="css"] { font-size: 18px !important; line-height: 1.55 !important; }
        h1 { font-size: clamp(1.85rem, 6.3vw, 2.55rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.48rem, 5.2vw, 2.05rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.32rem, 4.7vw, 1.78rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.2rem, 4.1vw, 1.55rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; line-height: 1.68 !important; }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; line-height: 1.68 !important; }

        .stCaption p { font-size: clamp(0.98rem, 3.4vw, 1.12rem) !important; }

        /* Tables: scale vertically on mobile (more row height) */
        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.6rem, 2.6vw, 0.9rem) !important;
            padding-bottom: clamp(0.6rem, 2.6vw, 0.9rem) !important;
            line-height: 1.5 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(0.95rem, 3.25vw, 1.08rem) !important;
        }

        /* Sticky disclaimer: keep readable but not overwhelming */
        .disclaimer-footer {
            font-size: clamp(0.76rem, 2.9vw, 0.92rem) !important;
            line-height: 1.4 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.78rem, 3vw, 0.94rem) !important;
        }

        /* Sidebar brand title (The Scoop 52): larger on mobile only */

        /* Mobile: reduce gap under the Scoop 52 title */

        /* Sidebar page links: larger on mobile only */
        
    }


    /* ===== TABLET (769px–1366px) — mobile-style layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {

        :root {
    --footer-sidebar-width: 0px;
    --scoop-tablet-gutter: clamp(0.85rem, 2.5vw, 1.1rem);
}

        html, body {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
            overflow-x: hidden !important;
        }

        .stApp {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

    }


    @media (min-width: 1367px) {

        :root {
            --footer-sidebar-width: clamp(12rem, 20vw, 36rem);
        }

        /* Desktop: sidebar always visible — no slide-out overlay. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: relative !important;
            transform: none !important;
            translate: none !important;
            transition: none !important;
            pointer-events: auto !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            box-shadow: none !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            margin-left: 0 !important;
            left: auto !important;
            top: auto !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            height: auto !important;
            min-height: auto !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: none !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"]) [data-testid="stAppViewContainer"]::before {
            display: none !important;
            content: none !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: auto !important;
            max-width: none !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div {
            width: auto !important;
            max-width: none !important;
        }
        [data-testid="stSidebar"] #scoop-title {
            font-size: 60px !important;
            line-height: 1.05 !important;
        }
    }


    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (folded) ===== */
    @media (min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),
           (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px) {

        :root {
    --footer-sidebar-width: 0px;
}

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

    }
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (unfolded) ===== */
    @media (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),
           (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),
           (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px) {

        :root {
    --footer-sidebar-width: 0px;
}

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

        /* Beat desktop (1367px) split-sidebar rules — same specificity, later cascade. */

    }


    </style>
    """,
    unsafe_allow_html=True,
)

# ── Financial Disclaimer ─────────────────────────────────────────────
st.title("📜 Terms of Service & Financial Disclaimer")

st.markdown("---")

st.markdown(
    '<div style="'
    "background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);"
    "border:1px solid #334155;border-left:4px solid #f59e0b;"
    "border-radius:12px;padding:2rem 2.5rem;margin-bottom:2rem;"
    'font-size:1.4rem;line-height:1.8;color:#e2e8f0;">'
    '<h2 style="color:#f59e0b;font-size:2rem;margin-top:0;">'
    "⚠️ DISCLAIMER — NOT FINANCIAL ADVICE</h2>"
    "<p>The information provided by this market sentiment aggregator, including but not limited to "
    '<b>"Market Mood,"</b> and <b>"Recommendations,"</b> is for '
    "<b>informational and educational purposes only.</b></p>"
    "<p><b>No Advice:</b> This tool does not constitute investment, legal, or tax advice. "
    "We are not a registered broker-dealer or investment advisor.</p>"
    "<p><b>Risk of Loss:</b> Trading stocks and cryptocurrencies involves significant risk. "
    "You should never invest more than you are willing to lose.</p>"
    "<p><b>Accuracy:</b> While we strive for data accuracy, our AI models and sentiment analysis "
    "are based on third-party news and market data which may be delayed or incorrect.</p>"
    "<p><b>DIY Research:</b> Users are solely responsible for their own investment decisions. "
    "We strongly recommend consulting with a qualified professional before making any financial commitments.</p>"
    '<p style="font-weight:700;color:#f59e0b;font-size:1.5rem;margin-bottom:0;">'
    "PAST PERFORMANCE IS NOT INDICATIVE OF FUTURE RESULTS.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── Terms of Service ─────────────────────────────────────────────────
st.markdown("## 📋 Terms of Service")

st.markdown(
    '<div style="'
    "background:#0f172a;border:1px solid #334155;border-left:4px solid #60a5fa;"
    "border-radius:12px;padding:2rem 2.5rem;margin-bottom:2rem;"
    'font-size:1.35rem;line-height:1.8;color:#e2e8f0;">'
    '<h3 style="color:#60a5fa;font-size:1.5rem;">1. Acceptance of Terms</h3>'
    "<p>By accessing this website, you agree to be bound by these Terms of Service and all applicable "
    "laws and regulations. If you do not agree with any of these terms, you are prohibited from using "
    "or accessing this site.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">2. Use License</h3>'
    "<p>Permission is granted to use this market sentiment aggregator for <b>personal, non-commercial "
    "transitory viewing only.</b> You may not:</p>"
    "<ul>"
    "<li>Modify or copy the materials;</li>"
    "<li>Use the materials for any commercial purpose or public display;</li>"
    "<li>Attempt to decompile or reverse engineer any software contained on the website.</li>"
    "</ul>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">3. Limitation of Liability</h3>'
    "<p>In no event shall the creators of this market sentiment aggregator or its partners be liable for any damages "
    "(including, without limitation, damages for loss of data or profit, or due to business "
    "interruption) arising out of the use or inability to use the materials on this website.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">4. Affiliate Disclosure</h3>'
    "<p>This website may contain affiliate links. If you click on an affiliate link and make a "
    "purchase or sign up for a service, we may receive a commission at no additional cost to you. "
    "This helps support the development of our free market tools.</p>"
    "<p>Exchange listings (Coinbase, Binance, Kraken, KuCoin, Gemini) shown in our screening tools "
    "are provided for informational purposes. Some links may be affiliate links.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">5. Data Sources</h3>'
    "<p>Market data is sourced from Alpha Vantage and other third-party providers. "
    "News headline sentiment is computed using TextBlob natural language processing. "
    "Charts use Plotly. Open-source copyright notices are listed on "
    '<a href="/Licenses" target="_self">Third-party licenses</a>. '
    "Data may be delayed, incomplete, or inaccurate. We make no guarantees about data freshness "
    "or accuracy.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">6. Changes to Terms</h3>'
    "<p>We reserve the right to revise these terms at any time without notice. By continuing to "
    "use this website, you agree to be bound by the current version of these Terms of Service.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">7. Privacy Policy</h3>'
    "<p>"
    "We do not sell your personal information to third parties or share it for cross-contextual behavioral advertising. "
    "Our data collection is limited to strictly necessary information required to document your acceptance of our Terms of Use "
    "and to maintain the security of our services."
    "</p>"
    "<p><b>Information collected (stored in the <code>legal_consents</code> SQL table):</b></p>"
    "<ul>"
    "<li><code>id</code></li>"
    "<li><code>timestamp_utc</code></li>"
    "<li><code>timestamp_local</code></li>"
    "<li><code>timezone_name</code></li>"
    "<li><code>timezone_offset</code></li>"
    "<li><code>ip_address</code></li>"
    "<li><code>user_agent</code></li>"
    "<li><code>tos_version</code></li>"
    "<li><code>fingerprint_hash</code></li>"
    "<li><code>consent_action</code></li>"
    "<li><code>is_vpn</code></li>"
    "<li><code>vpn_service_provider</code></li>"
    "<li><code>gpc_signal</code></li>"
    "<li><code>manual_opt_out</code></li>"
    "<li><code>opt_out_effective</code></li>"
    "<li><code>opt_out_source</code></li>"
    "<li><code>tracking_mode</code></li>"
    "</ul>"
    "<p><b>Retention:</b> These records are retained for <b>6 years</b> pursuant to applicable statute(s) of law.</p>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:1.2rem;'>"
    "Last updated: February 2026</p>",
    unsafe_allow_html=True,
)

# ── Sticky disclaimer footer ─────────────────────────────────────────
st.markdown(
    """
    <style>
    .disclaimer-footer {
        position: fixed; bottom: 0; left: var(--footer-sidebar-width); width: calc(100% - var(--footer-sidebar-width));
        background: #020617; border-top: 1px solid #334155;
        padding: 0.6rem 1rem;
        box-sizing: border-box; z-index: 10000;
        font-size: clamp(0.78rem, 0.72rem + 0.15vw, 0.9rem) !important; color: #e2e8f0;
        text-align: center; line-height: 1.45; white-space: normal;
        transition: left 0.25s ease, width 0.25s ease, font-size 0.25s ease;
    }
    .disclaimer-footer a { color: #93c5fd; text-decoration: underline; font-weight: 600; }
    .stMainBlockContainer { padding-bottom: 9rem !important; }
    :root { --footer-sidebar-width: clamp(12rem, 20vw, 36rem); }
    
    @media (min-width: 769px) and (max-width: 1366px) {
        .disclaimer-footer {
            position: static !important;
            left: 0 !important;
            width: 100% !important;
            margin-top: 1.25rem !important;
            padding: 0.5rem 0.75rem !important;
            font-size: clamp(0.76rem, 1.8vw, 0.92rem) !important;
            line-height: 1.35 !important;
        }
        .disclaimer-footer strong,
        .disclaimer-footer a {
            font-size: inherit !important;
        }
        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"] {
            padding-bottom: 2.5rem !important;
        }
    }
    </style>
    <div class="disclaimer-footer">
        <strong>⚠️ ALGORITHMIC RESEARCH ONLY – NOT FINANCIAL ADVICE</strong>
        This tool provides automated sentiment analysis and 'Market Mood' scores based on third-party news data.
        It is intended for <strong>informational and educational purposes only</strong> and does not constitute investment advice.
        Market data is provided 'as-is' and may be delayed or inaccurate.
        <strong>Trading involves significant risk of loss.</strong>
        <a href="/Terms_of_Service" target="_self">Terms of Service</a> ·
        <a href="/Licenses" target="_self">Third-party licenses</a> ·
        Past performance is not indicative of future results.
    </div>
    """,
    unsafe_allow_html=True,
)

inject_dark_mode_styles()
