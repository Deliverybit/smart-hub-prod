"""Third-party open-source license notices (hidden from default nav)."""

from pathlib import Path

import streamlit as st

from branding import logo_path_str, render_environment_banner
from landing_page import _landing_view_100_script, render_responsive_navigation
from licenses_format import notice_to_html
from theme_mode import inject_dark_mode_styles, install_theme_support
from tooltip_scroll import install_tooltip_scroll_handler

st.set_page_config(
    page_title="Third-party licenses",
    page_icon=logo_path_str(),
    layout="wide",
)
st.html(
    """
<script>
(function() {
    try {
        const win = (window.parent && window.parent !== window) ? window.parent : window;
        const w = win.innerWidth || window.innerWidth || 0;
        document.documentElement.setAttribute("data-scoop-terms-active", "1");
        document.documentElement.setAttribute("data-scoop-licenses-page", "1");
        try { win.document.documentElement.setAttribute("data-scoop-terms-active", "1"); } catch (e) {}
        try { win.document.documentElement.setAttribute("data-scoop-licenses-page", "1"); } catch (e) {}
        if (w <= 1366) {
            document.documentElement.setAttribute("data-scoop-tab-nav", "1");
            document.documentElement.removeAttribute("data-scoop-desktop-layout");
        }
    } catch (e) {}
})();
</script>
"""
    + _landing_view_100_script(),
    unsafe_allow_javascript=True,
)
render_environment_banner(st)
install_theme_support()
render_responsive_navigation(current_page="pages/_Licenses.py")
install_tooltip_scroll_handler()

notice_path = Path(__file__).resolve().parent.parent / "NOTICE"
notice = notice_path.read_text(encoding="utf-8") if notice_path.is_file() else "NOTICE file is missing."

st.markdown(
    """
    <style>
    html[data-scoop-licenses-page="1"],
    html[data-scoop-licenses-page="1"] body {
        zoom: 1 !important;
    }
    html, body, [class*="css"] {
        font-size: 30px !important;
        line-height: 1.7 !important;
    }
    h1 { font-size: 5rem !important; font-weight: 800 !important; }
    h2 { font-size: 3.2rem !important; }
    h3 { font-size: 2.6rem !important; }
    p, li, span { font-size: 1.6rem !important; line-height: 1.75 !important; }
    .stMarkdown p { font-size: 1.6rem !important; }
    .scoop-licenses-copy a { color: #93c5fd; font-weight: 600; }
    @media (min-width: 1367px) {
        [data-testid="stMainBlockContainer"] h1 {
            margin-top: 0 !important;
            font-size: clamp(32px, 2.4vw, 48px) !important;
            line-height: 1.15 !important;
        }
    }
    @media (max-width: 768px) {
        html, body, [class*="css"] { font-size: 18px !important; line-height: 1.55 !important; }
        h1 { font-size: clamp(1.85rem, 6.3vw, 2.55rem) !important; }
        h2 { font-size: clamp(1.48rem, 5.2vw, 2.05rem) !important; }
        h3 { font-size: clamp(1.32rem, 4.7vw, 1.78rem) !important; }
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        .scoop-licenses-copy p,
        .scoop-licenses-copy li {
            font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important;
            line-height: 1.68 !important;
        }
    }
    @media (min-width: 769px) and (max-width: 1366px) {
        html, body, [class*="css"] { font-size: clamp(21px, 2.35vw, 24px) !important; line-height: 1.62 !important; }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; }
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        .scoop-licenses-copy p,
        .scoop-licenses-copy li {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Third-party licenses")
st.markdown(
    '<div class="scoop-licenses-copy" style="'
    "background:#0f172a;border:1px solid #334155;border-left:4px solid #60a5fa;"
    "border-radius:12px;padding:2rem 2.5rem;margin-bottom:2rem;"
    'color:#e2e8f0;">'
    "<p>Open-source notices required by the libraries used in The Scoop 52.</p>"
    + notice_to_html(notice)
    + "</div>",
    unsafe_allow_html=True,
)

inject_dark_mode_styles()
