"""
NYSE
Screens large-cap NYSE stocks for those trading at or near their
52-week / all-time low **and** whose recent headlines do NOT contain
signals of fraud, illegality, or imminent bankruptcy.
"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
from datetime import datetime
from legal_consent_logger import ensure_timezone_cookie, log_terms_acceptance, render_terms_gate, terms_accepted
from branding import logo_path_str, render_environment_banner
from theme_mode import install_theme_support
from market_data import MarketData
from app_config import get_screener_symbol_limit, SCREENER_CACHE_VERSION
from screener_headlines import enrich_headline_sentiment
from screener_page_data import load_screener_page_data
from screener_selection import (
    MAX_PAD_CAP_PCT,
    MARKET_MOOD_TIP,
    order_full_results_columns,
    render_screener_landing_intro,
    render_screener_last_updated,
    selection_status_message,
    sync_screener_gating_layout,
)
from screener_table import ANALYZE_COLUMN_TIP, analyze_link_html, build_source_ticker_map, render_full_results_heading
from landing_page import (
    render_desktop_index_banner,
    render_responsive_navigation,
    should_render_desktop_top_picks,
)
from tooltip_scroll import install_tooltip_scroll_handler
from desktop_headlines_dismiss import inject_desktop_headlines_dismiss
from desktop_screener_tips import inject_desktop_screener_tips
from desktop_headlines_narrow import inject_desktop_headlines_narrow
from post_consent_mobile_screener_hide import inject_post_consent_mobile_screener_hide
import html

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="NYSE",
    page_icon=logo_path_str(),
    layout="wide",
    initial_sidebar_state="expanded",
)
render_environment_banner(st)
install_theme_support()
render_responsive_navigation(current_page="pages/1_NYSE_Top_10.py")


@st.cache_resource
def get_market_data(_cache_version: int = SCREENER_CACHE_VERSION):
    return MarketData()

# ── Global responsive styling (shared with app.py) ────────────────────
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

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700&family=Roboto:wght@700&display=swap');

    /* ===== DESKTOP / HIGH-RES ===== */
    html, body, [class*="css"] {
        font-size: 30px !important;
        line-height: 1.7 !important;
    }
    h1 { font-size: 5rem !important; font-weight: 800 !important; }
    h2 { font-size: 3.2rem !important; }
    h3 { font-size: 2.6rem !important; }
    h4 { font-size: 2.1rem !important; }
    p, li, span, div { font-size: 1.6rem !important; line-height: 1.75 !important; }
    .stMarkdown p { font-size: 1.6rem !important; }
    /* Metrics */
    [data-testid="stMetricValue"] > div { font-size: 4rem !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] > div > div > p,
    [data-testid="stMetricLabel"] label { font-size: 1.7rem !important; }
    [data-testid="stMetricDelta"] > div { font-size: 1.5rem !important; }
    /* Alerts */
    .stAlert p, [data-testid="stAlert"] p { font-size: 1.6rem !important; }
    .stSuccess p, .stWarning p, .stInfo p { font-size: 1.6rem !important; }
    /* Slider */
    .stSlider label { font-size: 1.6rem !important; margin-bottom: 1rem !important; }
    .stSlider p { font-size: 1.5rem !important; }
    .stSlider [data-testid="stThumbValue"] { margin-bottom: 0.5rem !important; }
    /* Buttons */
    .stButton button, button[kind="primary"] {
        font-size: 1.7rem !important;
        padding: 1.1rem 2.2rem !important;
        min-height: 4rem !important;
    }
    /* Primary button — light blue */
    .stMainBlockContainer > div > div > .stButton button[kind="primary"],
    button[kind="primary"] {
        background-color: #60a5fa !important;
        border-color: #60a5fa !important;
        color: #fff !important;
    }
    button[kind="primary"]:hover {
        background-color: #93c5fd !important;
        border-color: #93c5fd !important;
    }
    /* Captions */
    .stCaption p, [data-testid="stCaptionContainer"] p { font-size: 1.4rem !important; }
    /* Subheaders inside columns */
    [data-testid="stHorizontalBlock"] h2,
    [data-testid="stHorizontalBlock"] h3 { font-size: 2.2rem !important; }
    /* st.table (HTML) */
    [data-testid="stTable"] table { width: 100% !important; }
    [data-testid="stTable"] th {
        font-size: 1.6rem !important; font-weight: 700 !important; padding: 14px 18px !important;
    }
    [data-testid="stTable"] td {
        font-size: 1.6rem !important; padding: 12px 18px !important;
    }
    /* Custom HTML results table & markdown tables */
    .stMarkdown table { width: 100% !important; border-collapse: collapse !important; }
    .stMarkdown table th {
        font-size: 1.6rem !important; font-weight: 700 !important;
        padding: 14px 18px !important; text-align: left !important;
        border-bottom: 2px solid #444 !important;
    }
    .stMarkdown table td {
        font-size: 1.6rem !important; padding: 12px 18px !important;
        border-bottom: 1px solid #333 !important;
    }
    .stMarkdown table tr:hover { background: rgba(255,255,255,0.04) !important; }

    /* Custom tooltip — appears ABOVE the element, interactive */
    .tip-wrap {
        position: relative !important;
        cursor: help !important;
        border-bottom: 1px dashed #888 !important;
    }
    .tip-wrap .tip-text {
        visibility: hidden !important;
        opacity: 0 !important;
        position: absolute !important;
        bottom: calc(100% + 12px) !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        min-width: 360px !important;
        max-width: 700px !important;
        background: #1e1e2f !important;
        color: #e2e8f0 !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        font-weight: 400 !important;
        white-space: normal !important;
        z-index: 9999 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.45) !important;
        pointer-events: auto !important;
        transition: opacity 0.15s ease-in-out, visibility 0.15s ease-in-out !important;
        overflow-y: visible !important;
        max-height: none !important;
    }
    /* Invisible bridge so mouse can travel from trigger to tooltip */
    .tip-wrap .tip-text::before {
        content: "" !important;
        position: absolute !important;
        bottom: -14px !important;
        left: 0 !important;
        width: 100% !important;
        height: 14px !important;
    }
    .tip-wrap .tip-text::after {
        content: "" !important;
        position: absolute !important;
        top: 100% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        border-width: 8px !important;
        border-style: solid !important;
        border-color: #1e1e2f transparent transparent transparent !important;
    }
    .tip-wrap:hover .tip-text,
    .tip-wrap .tip-text:hover {
        visibility: visible !important;
        opacity: 1 !important;
    }
    .tip-wrap .tip-text a {
        color: #60a5fa !important;
        text-decoration: underline !important;
        font-weight: 500 !important;
    }
    .tip-wrap .tip-text a:hover {
        color: #93c5fd !important;
    }

    @media (min-width: 1367px) {
        /* Full Results: keep header tooltips above the hovered heading so rows stay readable */
        .full-results-table thead .tip-wrap .tip-text {
            bottom: calc(100% + 12px) !important;
            top: auto !important;
        }
        .full-results-table thead .tip-wrap .tip-text::before {
            bottom: -14px !important;
            top: auto !important;
        }
        .full-results-table thead .tip-wrap .tip-text::after {
            top: 100% !important;
            bottom: auto !important;
            border-color: #1e1e2f transparent transparent transparent !important;
        }
        @supports (position-anchor: auto) {
            .full-results-table thead .tip-wrap .tip-text {
                position: fixed !important;
                left: anchor(center) !important;
                top: anchor(top) !important;
                bottom: auto !important;
                transform: translate(-50%, calc(-100% - 12px)) !important;
                max-width: min(700px, calc(100vw - 2rem)) !important;
            }
        }
        /* Body-row tooltips appear near the hovered text, upper-right of the trigger. */
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text {
            display: block !important;
            position: absolute !important;
            left: calc(100% + 12px) !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 8px) !important;
            transform: none !important;
            width: auto !important;
            min-width: 360px !important;
            max-width: min(700px, calc(100vw - 2rem)) !important;
            font-size: 1.25rem !important;
            line-height: 1.55 !important;
            padding: 1.15rem 1.35rem !important;
            white-space: normal !important;
            overflow-wrap: break-word !important;
            word-break: normal !important;
            max-height: min(45vh, 22rem) !important;
            overflow-y: auto !important;
            pointer-events: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text::before {
            display: block !important;
            content: "" !important;
            position: absolute !important;
            left: -14px !important;
            right: auto !important;
            top: 0 !important;
            bottom: 0 !important;
            width: 14px !important;
            height: 100% !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text::after {
            display: block !important;
            top: auto !important;
            bottom: 10px !important;
            left: -16px !important;
            transform: none !important;
            border-color: transparent #1e1e2f transparent transparent !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text:hover {
            visibility: hidden !important;
            opacity: 0 !important;
        }
    }

    /* Desktop/webview only: Headlines — narrow wrap + beside trigger (anchor) / right-edge fallback; mobile unchanged */
    @media (min-width: 1367px) {
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip {
            display: inline-block !important;
            padding: 0.2rem 0.45rem !important;
            margin: -0.1rem -0.25rem !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: flex !important;
            flex-direction: column !important;
            align-items: stretch !important;
            position: fixed !important;
            top: var(--hl-fixed-top, -10000px) !important;
            left: var(--hl-fixed-left, -10000px) !important;
            right: auto !important;
            bottom: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
            min-width: 0 !important;
            max-width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
            height: var(--hl-fixed-height, auto) !important;
            min-height: 0 !important;
            max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
            overflow: hidden !important;
            white-space: normal !important;
            text-align: left !important;
            word-break: normal !important;
            overflow-wrap: break-word !important;
            z-index: 100020 !important;
            color: #ffffff !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            transition: opacity 0.25s ease-in-out 0.18s, visibility 0s linear 0.9s !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            display: flex !important;
            flex-direction: column !important;
            top: var(--hl-fixed-top, 100px) !important;
            left: var(--hl-fixed-left) !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            overflow: hidden !important;
            overscroll-behavior: contain !important;
            touch-action: pan-y !important;
            transition: none !important;
        }
        html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
        html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
        html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
        html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
            border: 2px solid #22c55e !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
            flex: 1 1 0 !important;
            display: block !important;
            min-height: 0 !important;
            max-height: none !important;
            overflow-x: hidden !important;
            overflow-y: scroll !important;
            overscroll-behavior: contain !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #111827 !important;
            pointer-events: auto !important;
            touch-action: pan-y !important;
            padding: 0.65rem 1rem 0.65rem 1rem !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 10px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border: 2px solid #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
            display: block !important;
            flex: 0 0 auto !important;
            position: relative !important;
            top: auto !important;
            z-index: 2 !important;
            margin: 0 !important;
            padding: 1.45rem 1rem 0.85rem 1rem !important;
            background: #1e1e2f !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            border-bottom: 1px solid #334155 !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::before,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::after {
            display: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.45rem !important;
            padding-top: 0 !important;
            min-width: 0 !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.45rem 0.25rem !important;
            border-bottom: 1px solid rgba(148, 163, 184, 0.35) !important;
            line-height: 1.5 !important;
            font-size: 1.05rem !important;
            color: #ffffff !important;
            min-width: 0 !important;
            overflow-wrap: break-word !important;
            word-break: normal !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line:last-child {
            border-bottom: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: normal !important;
            overflow-wrap: break-word !important;
        }
        .full-results-wrap:has(.tip-wrap.headlines-tip .hl-tip-cb:checked),
        .full-results-wrap:has(.tip-wrap.headlines-tip.hl-tip-desktop-open) {
            overflow: visible !important;
        }
        /* Commodity pages: even full-width desktop table layout. */
        .full-results-wrap.commodity-results .full-results-table {
            display: table !important;
            table-layout: fixed !important;
            width: 100% !important;
            border-collapse: collapse !important;
        }
        .full-results-wrap.commodity-results .full-results-table thead {
            display: table-header-group !important;
        }
        .full-results-wrap.commodity-results .full-results-table tbody {
            display: table-row-group !important;
        }
        .full-results-wrap.commodity-results .full-results-table tr {
            display: table-row !important;
        }
        .full-results-wrap.commodity-results .full-results-table th,
        .full-results-wrap.commodity-results .full-results-table td {
            display: table-cell !important;
            vertical-align: middle !important;
            padding: 0.65rem 0.75rem !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
            box-sizing: border-box !important;
            text-align: left !important;
            white-space: normal !important;
        }
        .full-results-wrap.commodity-results .full-results-table th:first-child,
        .full-results-wrap.commodity-results .full-results-table td:first-child {
            width: 3.5rem !important;
        }
    }

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
    [data-testid="stSidebar"] .stButton button {
        font-size: 1.6rem !important;
        padding: 1.1rem 1.8rem !important;
        min-height: 3.8rem !important;
    }
    [data-testid="stSidebar"] input {
        font-size: 1.5rem !important;
        padding: 0.9rem 1.1rem !important;
        min-height: 3.4rem !important;
    }
    [data-testid="stSidebar"] .stSlider label { font-size: 1.5rem !important; }
    [data-testid="stSidebar"] .stSlider p { font-size: 1.4rem !important; }
    [data-testid="stSidebar"] .stCaption p { font-size: 1.3rem !important; }
    [data-testid="stSidebar"] a { font-size: 1.5rem !important; }
    /* Hide auto-generated multipage nav so we can use custom labels */
    [data-testid="stSidebarNav"] { display: none !important; }
    div[data-testid="stCheckbox"] {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 0.5rem 0.8rem;
        margin-top: 0.35rem;
    }
    div[data-testid="stCheckbox"] label p {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    /* Full Results (custom HTML table): wide content scrolls inside wrapper */
    .full-results-wrap {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        margin: 0.25rem 0 0.75rem 0 !important;
        max-width: 100% !important;
    }
    .full-results-wrap .full-results-table {
        display: table !important;
        width: max(100%, max-content) !important;
        border-collapse: collapse !important;
        table-layout: auto !important;
    }
    /* Mobile card layout adds a left-hand label; hide it on desktop tables */
    .full-results-wrap .full-results-table .fr-label {
        display: none !important;
    }
    .full-results-mobile-legend {
        display: none !important;
    }
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

        [data-testid="stMetricValue"] > div { font-size: clamp(1.95rem, 7.2vw, 2.8rem) !important; }
        [data-testid="stMetricLabel"] > div > div > p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; }
        [data-testid="stMetricDelta"] > div { font-size: clamp(1.04rem, 3.6vw, 1.22rem) !important; }

        .stButton button { font-size: clamp(1.08rem, 3.75vw, 1.24rem) !important; padding: 0.8rem 1.15rem !important; }
        .stCaption p { font-size: clamp(0.98rem, 3.4vw, 1.12rem) !important; }

        /* Sticky disclaimer: keep readable but not overwhelming */
        .disclaimer-footer {
            font-size: clamp(0.76rem, 2.9vw, 0.92rem) !important;
            line-height: 1.4 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.78rem, 3vw, 0.94rem) !important;
        }

        /* Mobile: center hover tooltips so no horizontal scrolling is needed */
        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: 92vw !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
        }

        /* Full Results (mobile cards): show the per-cell heading/label on mobile only */
        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
        }

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

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div { flex: 1 1 100% !important; min-width: 100% !important; }

        /* Sidebar brand title (The Scoop 52): larger on mobile only */

        /* Mobile: reduce gap under the Scoop 52 title */

        /* Sidebar page links: larger on mobile only */

        /* Top Picks (mobile only): make each pick read as a single card. */
        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 0.9rem 0.95rem 1rem 0.95rem !important;
            margin: 0 0 1rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.75rem 0.85rem 0.65rem 0.85rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.15rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 1.9rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.1rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.15rem 0 !important;
            padding: 0.6rem 0.85rem 0.85rem 0.85rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.15rem !important;
            line-height: 1.55 !important;
        }

        /* Full Results — column tips panel (optional) */
        .stMarkdown .full-results-mobile-legend {
            display: none !important;
            margin: 0 0 1rem 0 !important;
            padding: 0.65rem 0.75rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(0.9rem, 0.5rem + 2.2vw, 1rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.65rem !important;
            padding-bottom: 0.65rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.35rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.45 !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
        }

        /* Full Results — mobile: one vertical card per row (desktop: unchanged table) */
        .stMarkdown .full-results-wrap {
            margin-left: -0.5rem !important;
            margin-right: -0.5rem !important;
            width: calc(100% + 1rem) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 0.2rem max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.15rem 0 !important;
            padding: 0.65rem 0.85rem 0.75rem 0.85rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.35rem 0.65rem !important;
            align-items: start !important;
            padding: 0.48rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(0.95rem, 0.52rem + 2.4vw, 1.08rem) !important;
            line-height: 1.4 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        /* Tooltips — mobile: appear above the touched text; page scroll hides sticky hover */
        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(18rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(18rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }
        /* Headlines: tap count toggles checkbox; card overlay at top of row (same as tablet). */
        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: absolute !important;
            left: 0 !important;
            right: 0 !important;
            top: 0 !important;
            bottom: auto !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
            height: auto !important;
            max-height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            text-align: left !important;
            color: #ffffff !important;
            padding: 0.45rem 0.6rem !important;
            font-size: calc(0.82rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.15 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: scroll !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.28rem 0.35rem 0.35rem 0.55rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.28rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.32rem 0.38rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.28 !important;
            font-size: calc(0.72rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.72rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }
    }


    /* ===== TABLET (769px–1366px) — mobile card layout; mobile/desktop unchanged ===== */
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

        .stApp { overflow-x: hidden !important; }

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
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 2.75rem) !important;
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

        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) {
            position: relative !important;
            cursor: help !important;
            border-bottom: 1px dashed #888 !important;
        }
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            position: absolute !important;
            bottom: calc(100% + 12px) !important;
            left: 50% !important;
            right: auto !important;
            top: auto !important;
            transform: translateX(-50%) !important;
            width: max-content !important;
            min-width: min(360px, calc(100vw - 2rem)) !important;
            max-width: min(700px, calc(100vw - 2rem)) !important;
            background: #1e1e2f !important;
            color: #e2e8f0 !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 16px 20px !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            font-weight: 400 !important;
            white-space: normal !important;
            z-index: 100001 !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.45) !important;
            pointer-events: auto !important;
            transition: opacity 0.15s ease-in-out, visibility 0.15s ease-in-out !important;
            max-height: min(45vh, 22rem) !important;
            overflow-y: auto !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text::before {
            content: "" !important;
            display: block !important;
            position: absolute !important;
            bottom: -14px !important;
            left: 0 !important;
            width: 100% !important;
            height: 14px !important;
        }
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text::after {
            content: "" !important;
            display: block !important;
            position: absolute !important;
            top: 100% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            border-width: 8px !important;
            border-style: solid !important;
            border-color: #1e1e2f transparent transparent transparent !important;
        }
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):focus-within .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text:hover,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):hover .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):active .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):hover .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):active .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):hover .tip-text,
        html body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.tip-wrap:not(.headlines-tip):hover, .tip-wrap:not(.headlines-tip):active, .tip-wrap:not(.headlines-tip):focus-within) {
            overflow: visible !important;
            position: relative !important;
            z-index: 100003 !important;
        }
        .stMarkdown .full-results-wrap:has(.tip-wrap:not(.headlines-tip):hover, .tip-wrap:not(.headlines-tip):active, .tip-wrap:not(.headlines-tip):focus-within) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td:has(.tip-wrap:not(.headlines-tip):hover, .tip-wrap:not(.headlines-tip):active, .tip-wrap:not(.headlines-tip):focus-within) {
            overflow: visible !important;
            position: relative !important;
            z-index: 100004 !important;
        }
        [data-testid="stMarkdownContainer"]:has(.tip-wrap:not(.headlines-tip):hover, .tip-wrap:not(.headlines-tip):active, .tip-wrap:not(.headlines-tip):focus-within) {
            overflow: visible !important;
        }

        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
            font-size: clamp(1.1rem, 2.4vw, 1.32rem) !important;
        }

        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.72rem, 1.8vw, 1rem) !important;
            padding-bottom: clamp(0.72rem, 1.8vw, 1rem) !important;
            line-height: 1.55 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(1.08rem, 2.4vw, 1.28rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 1rem 1.05rem 1.1rem 1.05rem !important;
            margin: 0 0 1.15rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.85rem 0.95rem 0.75rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.35rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 2.35rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.25rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.2rem 0 !important;
            padding: 0.7rem 0.95rem 0.95rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.3rem !important;
            line-height: 1.58 !important;
        }

        .stMarkdown .full-results-mobile-legend {
            display: none !important;
            margin: 0 0 1.1rem 0 !important;
            padding: 0.8rem 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.72rem !important;
            padding-bottom: 0.72rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.4rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.5 !important;
            font-size: clamp(1.02rem, 2.1vw, 1.18rem) !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
            font-size: clamp(1.08rem, 2.25vw, 1.24rem) !important;
        }

        .stMarkdown .full-results-wrap {
            margin-left: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            margin-right: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            width: calc(100% + 2 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }

        /* Index banner cards: use full content width on tablet (desktop keeps inline 50%). */
        [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"] {
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .stMarkdown .full-results-wrap .full-results-table {
            display: block !important;
            width: 100% !important;
            border-collapse: separate !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody {
            display: block !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.2rem 0 !important;
            padding: 0.85rem 1rem 0.95rem 1rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.45rem 0.75rem !important;
            align-items: start !important;
            padding: 0.58rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(1.12rem, 2.5vw, 1.38rem) !important;
            line-height: 1.5 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
            font-size: clamp(1.08rem, 2.3vw, 1.28rem) !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            width: var(--hl-fixed-width, 40vw) !important;
            min-width: 0 !important;
            max-width: var(--hl-fixed-width, 40vw) !important;
            height: auto !important;
            max-height: var(--hl-fixed-max-height, calc(100dvh - 1.5rem)) !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            flex-shrink: 0 !important;
            display: block !important;
            visibility: visible !important;
            position: relative !important;
            z-index: 2 !important;
            text-align: left !important;
            color: #93c5fd !important;
            padding: 0.55rem 0.75rem !important;
            font-size: calc(1rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.35rem 0.45rem 0.45rem 0.65rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.35rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.42rem 0.48rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.35 !important;
            font-size: calc(0.95rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.95rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text:hover {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* Full Results card — reorder fields without changing card format/size */
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: flex !important;
            flex-direction: column !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="#"] {
            order: 0 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] {
            order: 1 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Ticker"] {
            order: 2 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Price"] {
            order: 3 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W Low"] {
            order: 4 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="% Above Low"] {
            order: 5 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W High"] {
            order: 6 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Exchanges"] {
            order: 7 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headlines"] {
            order: 8 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Market Mood"] {
            order: 9 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            order: 10 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Analyze"] {
            order: 11 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-link {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {
            display: inline-block !important;
            cursor: help !important;
            border-bottom: 1px dashed #888 !important;
            color: inherit !important;
            font-weight: 600 !important;
            text-decoration: none !important;
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
        /* Desktop: CME-style index banner row fills content width. */
        [data-testid="stMarkdownContainer"] div[style*="flex-wrap:wrap"][style*="margin-bottom:1rem"] {
            width: 100% !important;
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

        .stApp { overflow-x: hidden !important; }

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

        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
            font-size: clamp(1.1rem, 2.4vw, 1.32rem) !important;
        }

        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.72rem, 1.8vw, 1rem) !important;
            padding-bottom: clamp(0.72rem, 1.8vw, 1rem) !important;
            line-height: 1.55 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(1.08rem, 2.4vw, 1.28rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 1rem 1.05rem 1.1rem 1.05rem !important;
            margin: 0 0 1.15rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.85rem 0.95rem 0.75rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.35rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 2.35rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.25rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.2rem 0 !important;
            padding: 0.7rem 0.95rem 0.95rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.3rem !important;
            line-height: 1.58 !important;
        }

        .stMarkdown .full-results-mobile-legend {
            display: none !important;
            margin: 0 0 1.1rem 0 !important;
            padding: 0.8rem 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.72rem !important;
            padding-bottom: 0.72rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.4rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.5 !important;
            font-size: clamp(1.02rem, 2.1vw, 1.18rem) !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
            font-size: clamp(1.08rem, 2.25vw, 1.24rem) !important;
        }

        .stMarkdown .full-results-wrap {
            margin-left: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            margin-right: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            width: calc(100% + 2 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }

        /* Index banner cards: use full content width on tablet (desktop keeps inline 50%). */
        [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"] {
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .stMarkdown .full-results-wrap .full-results-table {
            display: block !important;
            width: 100% !important;
            border-collapse: separate !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody {
            display: block !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.2rem 0 !important;
            padding: 0.85rem 1rem 0.95rem 1rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.45rem 0.75rem !important;
            align-items: start !important;
            padding: 0.58rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(1.12rem, 2.5vw, 1.38rem) !important;
            line-height: 1.5 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(22rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(22rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 0.95rem 1.05rem !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
            font-size: clamp(1.08rem, 2.3vw, 1.28rem) !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            width: var(--hl-fixed-width, 40vw) !important;
            min-width: 0 !important;
            max-width: var(--hl-fixed-width, 40vw) !important;
            height: auto !important;
            max-height: var(--hl-fixed-max-height, calc(100dvh - 1.5rem)) !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            flex-shrink: 0 !important;
            display: block !important;
            visibility: visible !important;
            position: relative !important;
            z-index: 2 !important;
            text-align: left !important;
            color: #ffffff !important;
            padding: 0.55rem 0.75rem !important;
            font-size: calc(1rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.35rem 0.45rem 0.45rem 0.65rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.35rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.42rem 0.48rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.35 !important;
            font-size: calc(0.95rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.95rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }

        /* Full Results card — reorder fields without changing card format/size */
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: flex !important;
            flex-direction: column !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="#"] {
            order: 0 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] {
            order: 1 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Ticker"] {
            order: 2 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Price"] {
            order: 3 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W Low"] {
            order: 4 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="% Above Low"] {
            order: 5 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W High"] {
            order: 6 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Exchanges"] {
            order: 7 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headlines"] {
            order: 8 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Market Mood"] {
            order: 9 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            order: 10 !important;
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

        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
            font-size: clamp(1.1rem, 2.4vw, 1.32rem) !important;
        }

        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.72rem, 1.8vw, 1rem) !important;
            padding-bottom: clamp(0.72rem, 1.8vw, 1rem) !important;
            line-height: 1.55 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(1.08rem, 2.4vw, 1.28rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 1rem 1.05rem 1.1rem 1.05rem !important;
            margin: 0 0 1.15rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.85rem 0.95rem 0.75rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.35rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 2.35rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.25rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.2rem 0 !important;
            padding: 0.7rem 0.95rem 0.95rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.3rem !important;
            line-height: 1.58 !important;
        }

        .stMarkdown .full-results-mobile-legend {
            display: none !important;
            margin: 0 0 1.1rem 0 !important;
            padding: 0.8rem 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.72rem !important;
            padding-bottom: 0.72rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.4rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.5 !important;
            font-size: clamp(1.02rem, 2.1vw, 1.18rem) !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
            font-size: clamp(1.08rem, 2.25vw, 1.24rem) !important;
        }

        .stMarkdown .full-results-wrap {
            margin-left: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            margin-right: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            width: calc(100% + 2 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }

        /* Index banner cards: use full content width on tablet (desktop keeps inline 50%). */
        [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"] {
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .stMarkdown .full-results-wrap .full-results-table {
            display: block !important;
            width: 100% !important;
            border-collapse: separate !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody {
            display: block !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.2rem 0 !important;
            padding: 0.85rem 1rem 0.95rem 1rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.45rem 0.75rem !important;
            align-items: start !important;
            padding: 0.58rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(1.12rem, 2.5vw, 1.38rem) !important;
            line-height: 1.5 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(22rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(22rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 0.95rem 1.05rem !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
            font-size: clamp(1.08rem, 2.3vw, 1.28rem) !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            width: var(--hl-fixed-width, 40vw) !important;
            min-width: 0 !important;
            max-width: var(--hl-fixed-width, 40vw) !important;
            height: auto !important;
            max-height: var(--hl-fixed-max-height, calc(100dvh - 1.5rem)) !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            flex-shrink: 0 !important;
            display: block !important;
            visibility: visible !important;
            position: relative !important;
            z-index: 2 !important;
            text-align: left !important;
            color: #ffffff !important;
            padding: 0.55rem 0.75rem !important;
            font-size: calc(1rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.35rem 0.45rem 0.45rem 0.65rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.35rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.42rem 0.48rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.35 !important;
            font-size: calc(0.95rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.95rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }

        /* Full Results card — reorder fields without changing card format/size */
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: flex !important;
            flex-direction: column !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="#"] {
            order: 0 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] {
            order: 1 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Ticker"] {
            order: 2 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Price"] {
            order: 3 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W Low"] {
            order: 4 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="% Above Low"] {
            order: 5 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W High"] {
            order: 6 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Exchanges"] {
            order: 7 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headlines"] {
            order: 8 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Market Mood"] {
            order: 9 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            order: 10 !important;
        }

        /* Beat desktop (1367px) split-sidebar rules — same specificity, later cascade. */

    }

    .scoop-fr-heading-wrap {
        padding-top: 24px !important;
        padding-bottom: 24px !important;
        box-sizing: border-box !important;
    }
    .scoop-full-results-heading {
        margin-top: 24px !important;
        margin-bottom: 24px !important;
    }
    .scoop-fr-heading-wrap .scoop-full-results-heading {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    .scoop-fr-heading-spacer {
        display: none !important;
        height: 0 !important;
    }
    [data-testid="stElementContainer"]:has(.scoop-full-results-heading),
    [data-testid="element-container"]:has(.scoop-full-results-heading),
    [data-testid="stElementContainer"]:has(.scoop-fr-heading-spacer),
    [data-testid="element-container"]:has(.scoop-fr-heading-spacer) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    @media (min-width: 1367px) {
        .scoop-fr-heading-wrap {
            padding-top: 40px !important;
            padding-bottom: 0 !important;
        }
        .scoop-full-results-heading {
            margin-top: 40px !important;
            margin-bottom: 0 !important;
        }
        .scoop-fr-heading-wrap .scoop-full-results-heading {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        .scoop-fr-heading-spacer {
            display: block !important;
            height: 40px !important;
            width: 100% !important;
        }
    }
    html:not([data-scoop-theme="dark"]) .scoop-full-results-heading {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    html:not([data-scoop-theme="dark"]) body .stApp .scoop-full-results-heading .scoop-fr-title-box {
        display: inline-block !important;
        border: 2px solid #22c55e !important;
        border-radius: 10px !important;
        padding: 0.2em 0.55em !important;
        background: #f0fdf4 !important;
        box-sizing: border-box !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
    }
    html[data-scoop-theme="dark"] .scoop-full-results-heading,
    html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #0f172a !important;
    }
    html[data-scoop-theme="dark"] body .stApp .scoop-full-results-heading .scoop-fr-title-box,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stMarkdownContainer"] .scoop-full-results-heading .scoop-fr-title-box {
        display: inline-block !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
        padding: 0.2em 0.55em !important;
        background: #ffffff !important;
        color: #0f172a !important;
        box-sizing: border-box !important;
        font-size: inherit !important;
        line-height: inherit !important;
    }

    /* Phone/tablet: no Full Results legend panel. Desktop unchanged. */
    @media (max-width: 1366px) {
        html .full-results-mobile-legend,
        html .stMarkdown .full-results-mobile-legend {
            display: none !important;
        }
        /* Top 3 cards: flame beside the rank hashtag. Desktop unchanged. */
        .stMarkdown .full-results-wrap .full-results-table tbody tr:nth-child(-n+3) td[data-label="#"] .fr-label::after {
            content: " 🔥";
        }
        .scoop-full-results-heading,
        .scoop-full-results-heading .scoop-fr-title-box {
            font-weight: 800 !important;
        }
        html[data-scoop-theme="dark"] .scoop-full-results-heading,
        html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading,
        html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading span {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-weight: 800 !important;
        }
        html[data-scoop-theme="dark"] body .stApp .scoop-full-results-heading .scoop-fr-title-box,
        html[data-scoop-theme="dark"] body .stApp [data-testid="stMarkdownContainer"] .scoop-full-results-heading .scoop-fr-title-box {
            display: inline-block !important;
            border: 2px solid #ffffff !important;
            border-radius: 10px !important;
            padding: 0.2em 0.55em !important;
            background: #ffffff !important;
            color: #0f172a !important;
            box-sizing: border-box !important;
            font-weight: 800 !important;
            font-size: inherit !important;
            line-height: inherit !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

agreed = terms_accepted(st, "agree_terms_nyse")
sync_screener_gating_layout(st, gated=not agreed)
inject_post_consent_mobile_screener_hide()
ensure_timezone_cookie(st)
if agreed:
    log_terms_acceptance(st, consent_key="agree_terms_nyse")

# ── Constants ─────────────────────────────────────────────────────────
# A curated watchlist of 100 well-known U.S. stocks across sectors (NYSE-themed).
# We screen this list live each time the user clicks "Scan".
COMPANY_NAMES = {
    # Technology
    "IBM": "International Business Machines",
    "ORCL": "Oracle Corporation",
    "HPQ": "HP Inc.",
    "DELL": "Dell Technologies",
    "NET": "Cloudflare",
    "SNOW": "Snowflake",
    "PATH": "UiPath",
    "ESTC": "Elastic N.V.",
    "CRM": "Salesforce, Inc.",
    "ACN": "Accenture plc",
    "NOW": "ServiceNow, Inc.",
    "ANET": "Arista Networks",
    # Financials
    "JPM": "JPMorgan Chase & Co.",
    "BAC": "Bank of America",
    "WFC": "Wells Fargo & Co.",
    "GS": "Goldman Sachs Group",
    "MS": "Morgan Stanley",
    "C": "Citigroup Inc.",
    "BK": "Bank of New York Mellon",
    "USB": "U.S. Bancorp",
    "PNC": "PNC Financial Services",
    "SCHW": "Charles Schwab Corp.",
    "V": "Visa Inc.",
    "MA": "Mastercard Inc.",
    "AXP": "American Express Co.",
    "BLK": "BlackRock, Inc.",
    "SPGI": "S&P Global Inc.",
    "PGR": "The Progressive Corp.",
    "ICE": "Intercontinental Exchange",
    "FI": "Fiserv, Inc.",
    # Healthcare
    "JNJ": "Johnson & Johnson",
    "PFE": "Pfizer Inc.",
    "ABT": "Abbott Laboratories",
    "MRK": "Merck & Co.",
    "BMY": "Bristol-Myers Squibb",
    "LLY": "Eli Lilly & Co.",
    "CI": "The Cigna Group",
    "HUM": "Humana Inc.",
    "CVS": "CVS Health Corp.",
    "UNH": "UnitedHealth Group",
    "ABBV": "AbbVie Inc.",
    "TMO": "Thermo Fisher Scientific",
    "DHR": "Danaher Corp.",
    "SYK": "Stryker Corp.",
    "MDT": "Medtronic plc",
    "ELV": "Elevance Health",
    # Consumer / Retail
    "WMT": "Walmart Inc.",
    "KO": "The Coca-Cola Co.",
    "PEP": "PepsiCo Inc.",
    "PG": "Procter & Gamble Co.",
    "MCD": "McDonald's Corp.",
    "NKE": "Nike Inc.",
    "TGT": "Target Corp.",
    "DG": "Dollar General Corp.",
    "HD": "The Home Depot",
    "LOW": "Lowe's Companies",
    "TJX": "The TJX Companies",
    "PM": "Philip Morris International",
    "CL": "Colgate-Palmolive Co.",
    "GM": "General Motors Co.",
    # Energy
    "XOM": "Exxon Mobil Corp.",
    "CVX": "Chevron Corp.",
    "COP": "ConocoPhillips",
    "SLB": "Schlumberger (SLB)",
    "HAL": "Halliburton Co.",
    "OXY": "Occidental Petroleum",
    "PSX": "Phillips 66",
    "VLO": "Valero Energy Corp.",
    # Industrials
    "BA": "The Boeing Co.",
    "CAT": "Caterpillar Inc.",
    "GE": "GE Aerospace",
    "HON": "Honeywell International",
    "MMM": "3M Company",
    "UPS": "United Parcel Service",
    "FDX": "FedEx Corp.",
    "DE": "Deere & Company",
    "LMT": "Lockheed Martin Corp.",
    "RTX": "RTX Corporation",
    "ETN": "Eaton Corporation",
    "WM": "Waste Management",
    "GD": "General Dynamics",
    "NOC": "Northrop Grumman",
    # Telecom / Media
    "T": "AT&T Inc.",
    "VZ": "Verizon Communications",
    "DIS": "The Walt Disney Co.",
    "WBD": "Warner Bros. Discovery",
    # Real Estate / Utilities
    "AMT": "American Tower Corp.",
    "PLD": "Prologis Inc.",
    "SPG": "Simon Property Group",
    "DUK": "Duke Energy Corp.",
    "SO": "The Southern Company",
    "NEE": "NextEra Energy",
    "D": "Dominion Energy",
    # Materials
    "FCX": "Freeport-McMoRan",
    "NEM": "Newmont Corp.",
    "DOW": "Dow Inc.",
    "DD": "DuPont de Nemours",
    "SHW": "Sherwin-Williams Co.",
    "APD": "Air Products and Chemicals",
    "LIN": "Linde plc",
}

COMPANY_SUMMARIES = {
    "IBM": "Global technology company offering hybrid cloud, AI, and consulting services.",
    "ORCL": "Enterprise software giant specializing in cloud infrastructure and databases.",
    "HPQ": "Manufactures personal computers, printers, and related supplies.",
    "DELL": "Leading provider of PCs, servers, storage, and IT infrastructure solutions.",
    "NET": "Cloud platform providing CDN, DDoS protection, and internet security services.",
    "SNOW": "Cloud-based data warehousing and analytics platform.",
    "PATH": "Enterprise automation software using robotic process automation (RPA).",
    "ESTC": "Open-source search, observability, and security analytics platform.",
    "CRM": "Enterprise cloud software for customer relationship management and automation.",
    "ACN": "Global professional services firm in strategy, consulting, digital, and operations.",
    "NOW": "Cloud platform for digital workflows, IT service management, and enterprise automation.",
    "ANET": "Cloud networking company making high-speed switches for data centers and AI clusters.",
    "JPM": "Largest U.S. bank by assets; investment banking, asset management, and retail banking.",
    "BAC": "Major U.S. bank offering consumer banking, wealth management, and capital markets.",
    "WFC": "Diversified financial services company focused on banking and mortgage lending.",
    "GS": "Leading global investment bank and financial services firm.",
    "MS": "Global financial services firm in investment banking, wealth management, and trading.",
    "C": "Multinational bank providing consumer banking, corporate finance, and global markets.",
    "BK": "Global custody bank and asset servicing company.",
    "USB": "Regional bank providing consumer and commercial banking, payments, and wealth management.",
    "PNC": "Major U.S. regional bank offering retail and corporate banking services.",
    "SCHW": "Brokerage and wealth management firm serving individual investors and advisors.",
    "V": "Global payments network processing consumer and commercial card transactions.",
    "MA": "Global payments technology company operating a credit, debit, and commercial card network.",
    "AXP": "Integrated payments and travel company issuing charge and credit cards worldwide.",
    "BLK": "World's largest asset manager offering iShares ETFs and institutional investment services.",
    "SPGI": "Provider of credit ratings, market data, and benchmarks including the S&P 500.",
    "PGR": "Major U.S. auto insurer also offering home, renters, and commercial coverage.",
    "ICE": "Operator of global exchanges and clearing houses, including the NYSE.",
    "FI": "Payments and financial technology company serving banks, merchants, and billers.",
    "JNJ": "Diversified healthcare company in pharmaceuticals, medical devices, and consumer health.",
    "PFE": "Global pharmaceutical company known for vaccines, oncology, and specialty medicines.",
    "ABT": "Healthcare company making diagnostics, medical devices, nutritionals, and pharmaceuticals.",
    "MRK": "Pharmaceutical company focused on oncology, vaccines, and animal health.",
    "BMY": "Biopharmaceutical company specializing in oncology, immunology, and cardiovascular.",
    "LLY": "Pharmaceutical company known for diabetes, oncology, and neuroscience treatments.",
    "CI": "Global health services company offering insurance, pharmacy benefits, and care delivery.",
    "HUM": "Health insurance company focused on Medicare Advantage plans.",
    "CVS": "Healthcare company operating pharmacies, insurance (Aetna), and health services.",
    "UNH": "Largest U.S. health insurer; also operates Optum pharmacy and care-delivery services.",
    "ABBV": "Biopharmaceutical company in immunology, oncology, neuroscience, and aesthetics.",
    "TMO": "Life-science tools and diagnostics company serving labs, pharma, and biotech.",
    "DHR": "Science and technology conglomerate in diagnostics, life sciences, and environmental tools.",
    "SYK": "Medical technology company making orthopedic implants, surgical tools, and neuro devices.",
    "MDT": "Medical device company in cardiac, diabetes, surgical, and neuroscience products.",
    "ELV": "Health benefits company operating Anthem-branded commercial and government plans.",
    "WMT": "World's largest retailer operating discount stores, supercenters, and e-commerce.",
    "KO": "World's largest beverage company; iconic brands including Coca-Cola, Sprite, Fanta.",
    "PEP": "Global food and beverage company with brands like Pepsi, Lay's, Gatorade, Quaker.",
    "PG": "Consumer goods giant with brands in personal care, home care, and baby products.",
    "MCD": "World's largest fast-food restaurant chain by revenue.",
    "NKE": "Global leader in athletic footwear, apparel, and sports equipment.",
    "TGT": "Major U.S. retailer operating general merchandise and food discount stores.",
    "DG": "Discount retailer operating small-format stores in rural and suburban communities.",
    "HD": "Largest U.S. home improvement retailer selling tools, hardware, and building materials.",
    "LOW": "Home improvement retailer offering products for maintenance, repair, and remodeling.",
    "TJX": "Off-price retailer operating T.J. Maxx, Marshalls, HomeGoods, and related banners.",
    "PM": "International tobacco company behind Marlboro outside the U.S.; expanding smoke-free products.",
    "CL": "Consumer products company in oral care, personal care, and home care brands.",
    "GM": "U.S. automaker producing Chevrolet, GMC, Cadillac, and Buick vehicles plus EV platforms.",
    "XOM": "World's largest publicly traded oil and gas company; exploration, refining, and chemicals.",
    "CVX": "Integrated energy company in oil/gas exploration, refining, and renewable energy.",
    "COP": "Independent exploration and production company focused on oil and natural gas.",
    "SLB": "World's largest oilfield services company providing drilling and production technology.",
    "HAL": "Oilfield services company offering drilling, evaluation, and completion solutions.",
    "OXY": "Oil and gas exploration/production company with chemical manufacturing operations.",
    "PSX": "Downstream energy company operating refineries, pipelines, and petrochemicals.",
    "VLO": "Largest independent petroleum refiner and marketer in the U.S.",
    "BA": "Aerospace manufacturer of commercial aircraft, defense systems, and space technology.",
    "CAT": "World's largest construction and mining equipment manufacturer.",
    "GE": "Aerospace company making jet engines, power systems, and defense technologies.",
    "HON": "Industrial conglomerate in aerospace, building tech, and performance materials.",
    "MMM": "Diversified manufacturer of industrial, safety, healthcare, and consumer products.",
    "UPS": "World's largest package delivery company and supply chain management provider.",
    "FDX": "Global courier and logistics company offering express, freight, and e-commerce services.",
    "DE": "Leading manufacturer of agricultural, construction, and forestry equipment.",
    "LMT": "World's largest defense contractor; fighter jets, missiles, and space systems.",
    "RTX": "Aerospace and defense company formed from Raytheon and United Technologies merger.",
    "ETN": "Power management company in electrical, aerospace, and vehicle components.",
    "WM": "Largest U.S. waste and recycling company serving residential and commercial customers.",
    "GD": "Defense contractor in combat vehicles, ships, Gulfstream jets, and IT services.",
    "NOC": "Aerospace and defense company making bombers, autonomous systems, and mission systems.",
    "T": "Telecommunications giant providing wireless, broadband, and media services.",
    "VZ": "Major U.S. telecom operator offering wireless, internet, and business solutions.",
    "DIS": "Global entertainment conglomerate in theme parks, studios, streaming, and media.",
    "WBD": "Media company operating Warner Bros. studios, HBO, CNN, and Discovery networks.",
    "AMT": "Largest global REIT owning and operating wireless communication towers.",
    "PLD": "World's largest industrial REIT owning logistics and distribution warehouses.",
    "SPG": "Largest U.S. shopping mall REIT owning premier retail properties.",
    "DUK": "One of the largest electric power holding companies in the U.S.",
    "SO": "Major U.S. electric utility serving the southeastern United States.",
    "NEE": "World's largest generator of wind and solar energy; parent of Florida Power & Light.",
    "D": "Utility company providing electricity and natural gas across the eastern U.S.",
    "FCX": "World's largest publicly traded copper producer; also mines gold and molybdenum.",
    "NEM": "World's largest gold mining company with operations on five continents.",
    "DOW": "Global materials science company producing plastics, chemicals, and coatings.",
    "DD": "Specialty chemicals company serving electronics, water, and industrial markets.",
    "SHW": "Largest U.S. paints and coatings company serving consumers, contractors, and industry.",
    "APD": "Industrial gases company supplying atmospheric and process gases and related equipment.",
    "LIN": "World's largest industrial gases and engineering company.",
}

NYSE_UNIVERSE = list(COMPANY_NAMES.keys())

# Keywords that disqualify a stock (headlines suggesting illegal activity
# or the company going out of business).
DISQUALIFY_KEYWORDS = [
    "fraud", "illegal", "lawsuit", "bankrupt", "bankruptcy", "indicted",
    "indictment", "criminal", "sec charges", "securities fraud",
    "going out of business", "shutting down", "closing all",
    "delisted", "ponzi", "embezzlement", "money laundering",
    "accounting scandal", "class action", "fda rejection",
]

SCREENER_SYMBOL_LIMIT = get_screener_symbol_limit()


# ── Helper functions ──────────────────────────────────────────────────
def screen_stock(ticker: str) -> dict | None:
    """Return screening data for one ticker, or None on failure."""
    try:
        import math
        market_data = get_market_data()
        snapshot = market_data.get_market_snapshot(ticker)
        if not snapshot:
            return None
        current_price = snapshot["current_price"]
        year_low = snapshot["year_low"]
        year_high = snapshot["year_high"]

        if (current_price is None or year_low is None or year_high is None
                or (isinstance(year_low, float) and math.isnan(year_low))
                or (isinstance(year_high, float) and math.isnan(year_high))
                or (isinstance(current_price, float) and math.isnan(current_price))
                or year_low <= 0):
            return None

        pct_above_low = ((current_price - year_low) / year_low) * 100

        # Keep screener calls price-first so Alpha Vantage rate limits do not
        # block the whole Top 10 table. Detailed headline analysis remains on Search.
        news = []
        headlines = []
        headline_links = []
        for item in news:
            title = item.get("title", "")
            url = item.get("url", "")
            if title:
                headlines.append(title)
                headline_links.append(url)

        # Disqualify if any headline contains a red-flag keyword
        lower_headlines = " ".join(headlines).lower()
        for kw in DISQUALIFY_KEYWORDS:
            if kw in lower_headlines:
                return None

        # Quick sentiment score from headlines
        polarity = 0.0
        if headlines:
            for hl in headlines:
                polarity += TextBlob(hl).sentiment.polarity
            polarity /= len(headlines)

        # Extra penalty: if sentiment is very negative, skip
        if polarity < -0.35:
            return None

        if pct_above_low < 0:
            signal = "BELOW LOW"
        elif pct_above_low <= 2:
            signal = "AT LOW"
        else:
            signal = "NEAR LOW"

        return {
            "Ticker": ticker,
            "_source_ticker": ticker,
            "Company": COMPANY_NAMES.get(ticker, ticker),
            "Price": current_price,
            "52W Low": year_low,
            "52W High": year_high,
            "% Above Low": round(pct_above_low, 2),
            "Headline Sentiment": round(polarity, 3),
            "Headlines": len(headlines),
            "_headline_texts": headlines,
            "_headline_urls": headline_links,
            "Market Mood": signal,
        }
    except Exception:
        return None


# ── Exchange performance banner ───────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def _fetch_index(ticker: str):
    """Return (price, daily_change_pct) for an index ticker."""
    try:
        return get_market_data().get_daily_change(ticker)
    except Exception:
        return None, None


def _banner_card(label, price, chg, prefix="$"):
    if price is None:
        return ""
    c = "#22c55e" if chg >= 0 else "#ef4444"
    a = "▲" if chg >= 0 else "▼"
    return (
        f'<div class="scoop-index-card" style="flex:1;min-width:220px;max-width:50%;background:linear-gradient(135deg,#1e293b,#0f172a);'
        f'border:1px solid #334155;border-left:4px solid {c};border-radius:12px;'
        f'padding:1.2rem 1.8rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">'
        f'<span style="font-size:1.4rem;color:#e2e8f0;font-weight:500;">{label}</span>'
        f'<span style="font-size:2.2rem;font-weight:700;color:#f1f5f9;">{prefix}{price:,.2f}</span>'
        f'<span style="font-size:1.4rem;font-weight:600;color:{c};background:{c}18;'
        f'padding:0.3rem 0.8rem;border-radius:6px;">{a} {chg:+.2f}%</span></div>'
    )


_nya_price, _nya_chg = _fetch_index("^NYA")
_gspc_price, _gspc_chg = _fetch_index("^GSPC")
_dji_price, _dji_chg = _fetch_index("^DJI")
_cards = (
    _banner_card("NYSE Composite (^NYA) — Today", _nya_price, _nya_chg)
    + _banner_card("S&P 500 (^GSPC) — Today", _gspc_price, _gspc_chg)
    + _banner_card("Dow Jones (^DJI) — Today", _dji_price, _dji_chg)
)
if _cards:
    render_desktop_index_banner(
        st,
        f'<div class="scoop-banner-desktop" style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">{_cards}</div>',
        page="pages/1_NYSE_Top_10.py",
    )

# ── UI ────────────────────────────────────────────────────────────────
st.title("🏦 NYSE")
render_screener_landing_intro(
    st,
    market="NYSE",
    universe_size=len(NYSE_UNIVERSE),
    asset_label="stock",
    sentiment_profile="stock",
)

@st.cache_data(ttl=900, show_spinner="Refreshing NYSE data…")
def _run_screen(_cache_version: int = SCREENER_CACHE_VERSION):
    """Screen all NYSE stocks and return (results, timestamp)."""
    results = []
    scan_universe = NYSE_UNIVERSE[:SCREENER_SYMBOL_LIMIT]
    for tkr in scan_universe:
        row = screen_stock(tkr)
        if row is not None:
            results.append(row)
    return results, datetime.now().strftime("%b %d, %Y  %I:%M %p")

if not render_terms_gate(
    st,
    "agree_terms_nyse",
    "I agree to the [Disclaimer & Terms](/Terms_of_Service)",
):
    pass
else:
    loaded = load_screener_page_data(
        "NYSE",
        universe_size=len(NYSE_UNIVERSE),
        asset_noun="stocks",
        run_live=_run_screen,
    )
    all_results = loaded.all_results
    results = loaded.display_results
    last_updated = loaded.last_updated
    scanned_count = loaded.scanned_count
    selection = loaded.selection

    render_screener_last_updated(st, last_updated)

    if not all_results:
        st.warning(
            "No stock data is available right now. Alpha Vantage may be rate-limiting "
            "requests; wait a minute and refresh."
        )
        if st.button("Clear cache and refresh", key="refresh_nyse"):
            st.cache_data.clear()
            st.rerun()
    elif not results:
        st.warning(
            f"No stocks are within **{MAX_PAD_CAP_PCT}%** of their 52-week low right now."
        )
        if st.button("Clear cache and refresh", key="refresh_nyse"):
            st.cache_data.clear()
            st.rerun()
    else:
        df = pd.DataFrame(results)
        df = df.sort_values("% Above Low", ascending=True).reset_index(drop=True)
        if not loaded.headlines_enriched:
            df = enrich_headline_sentiment(df, get_market_data(), screener_key="NYSE")
        df["Headlines"] = df["Headlines"].clip(upper=10)
        df["_headline_texts"] = df["_headline_texts"].apply(lambda items: items[:10])
        df["_headline_urls"] = df["_headline_urls"].apply(lambda items: items[:10])
        df.index = df.index + 1  # 1-based rank

        level, status_msg = selection_status_message(
            selection,
            asset_noun=loaded.asset_noun,
            scanned_count=scanned_count,
            universe_size=len(NYSE_UNIVERSE),
        )
        getattr(st, level)(status_msg)

        # ── Metrics row for top 3 (desktop only) ──────────────────────
        if should_render_desktop_top_picks(page="pages/1_NYSE_Top_10.py"):
            st.markdown('<div class="scoop-top-picks-anchor" hidden></div>', unsafe_allow_html=True)
            st.markdown("### 🏆 Top Picks")
            top_cols = st.columns(min(3, len(df)))
            for idx, col in enumerate(top_cols):
                if idx >= len(df):
                    break
                row = df.iloc[idx]
                with col:
                    delta_txt = f"{row['% Above Low']:+.1f}% above 52W low"
                    st.metric(
                        label=f"#{idx + 1} 🔥  {row['Ticker']}",
                        value=f"${row['Price']:,.2f}",
                        delta=delta_txt,
                        delta_color="normal",
                    )
                    tip = COMPANY_SUMMARIES.get(row["Ticker"], "")
                    if row["Market Mood"] == "BELOW LOW":
                        badge = "🚨 BELOW 52W LOW — New Floor"
                    elif row["Market Mood"] == "AT LOW":
                        badge = "AT 52W LOW"
                    else:
                        badge = "📉 NEAR 52W LOW"
                    st.markdown(
                        f'<div style="font-size:1.5rem;line-height:1.8;">'
                        f'<span class="tip-wrap scoop-name-tip" style="font-weight:700;">'
                        f'{row["Company"]}'
                        f'<span class="tip-text">{tip}</span></span><br>'
                        f'52W Low: <b style="color:#22c55e;">${row["52W Low"]:,.2f}</b> · '
                        f'52W High: <b>${row["52W High"]:,.2f}</b><br>'
                        f'Sentiment: <b>{row["Headline Sentiment"]:+.3f}</b><br>'
                        f'<b>{badge}</b>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        # ── Full table (HTML with hover tooltips on Company) ─────────
        render_full_results_heading(st, "NYSE Top 10")
        st.markdown('<div class="scoop-fr-heading-spacer" aria-hidden="true"></div>', unsafe_allow_html=True)

        headline_map = {}
        for _, r in df.iterrows():
            texts = r.get("_headline_texts", [])
            urls = r.get("_headline_urls", [])
            headline_map[r["Ticker"]] = list(zip(texts, urls))

        source_ticker_map = build_source_ticker_map(df)

        display_df = df.drop(columns=["_source_ticker", "_headline_texts", "_headline_urls"], errors="ignore").copy()
        display_df["Price"] = display_df["Price"].apply(lambda x: f"${x:,.2f}")
        display_df["52W Low"] = display_df["52W Low"].apply(lambda x: f"${x:,.2f}")
        display_df["52W High"] = display_df["52W High"].apply(lambda x: f"${x:,.2f}")
        display_df["% Above Low"] = display_df["% Above Low"].apply(lambda x: f"{x:.2f}%")
        display_df["Headline Sentiment"] = display_df["Headline Sentiment"].apply(lambda x: f"{x:+.3f}")
        display_df["Analyze"] = ""
        display_df = display_df[order_full_results_columns(display_df.columns)]

        COLUMN_TIPS = {
            "Headline Sentiment": "Average polarity score of recent news headlines (TextBlob). Ranges from -1.0 (very negative) to +1.0 (very positive). Stocks below -0.35 are automatically disqualified.",
            "Headlines": "Number of recent news headlines found for this stock. More headlines give a more reliable sentiment reading.",
            "Market Mood": MARKET_MOOD_TIP,
            "% Above Low": "How far the current price is above the 52-week low, expressed as a percentage. Lower is closer to the floor.",
            "Analyze": ANALYZE_COLUMN_TIP,
        }

        def _tip(text, tooltip, anchor_id: str = "", extra_class: str = ""):
            anchor_style = f' style="anchor-name: {anchor_id};"' if anchor_id else ""
            tip_style = f' style="position-anchor: {anchor_id};"' if anchor_id else ""
            wrap_class = " ".join(part for part in ("tip-wrap", extra_class) if part)
            return (
                f'<span class="{wrap_class}"{anchor_style}>{text}'
                f'<span class="tip-text"{tip_style}>{tooltip}</span></span>'
            )

        def _headlines_tip(count_display, hl_pairs: list, row_idx: int) -> str:
            aid = f"--hl-r{int(row_idx)}"
            rows_inner = []
            for title, url in hl_pairs:
                stitle = html.escape(str(title))
                if url:
                    surl = html.escape(str(url), quote=True)
                    rows_inner.append(
                        f'<div class="hl-tip-line"><a href="{surl}" target="_blank" '
                        f'rel="noopener noreferrer">{stitle}</a></div>'
                    )
                else:
                    rows_inner.append(f'<div class="hl-tip-line">{stitle}</div>')
            list_html = "".join(rows_inner)
            cb_id = f"hl-cb-r{int(row_idx)}"
            return (
                f'<span class="tip-wrap headlines-tip" style="anchor-name: {aid};">'
                f'<input type="checkbox" id="{cb_id}" class="hl-tip-cb" aria-hidden="true">'
                f'<label class="hl-tip-count" for="{cb_id}">'
                f"{html.escape(str(count_display))}</label>"
                f'<label class="hl-tip-backdrop" for="{cb_id}" aria-hidden="true">'
                f"<span>&nbsp;</span></label>"
                f'<span class="tip-text" style="position-anchor: {aid};">'
                f'<span class="hl-tip-heading">Headlines</span>'
                f'<div class="headlines-tip-scroll">'
                f'<div class="headlines-tip-list">{list_html}</div>'
                f"</div>"
                f"</span></span>"
            )

        def _attr_html(s):
            return (
                str(s)
                .replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
            )

        def _td(col_label: str, inner_html: str, label_tip: str = "") -> str:
            label_html = _attr_html(col_label)
            if label_tip:
                label_html = _tip(_attr_html(col_label), html.escape(label_tip))
            return (
                f'<td data-label="{_attr_html(col_label)}">'
                f'<span class="fr-label">{label_html}</span>'
                f'<span class="fr-val">{inner_html}</span></td>'
            )

        def _build_html_table(dataframe):
            cols = list(dataframe.columns)
            rows_html = ""
            header_cells = '<th>#</th>'
            for idx_col, c in enumerate(cols):
                tip = COLUMN_TIPS.get(c, "")
                if tip:
                    header_cells += f'<th>{_tip(c, tip, f"--frh-{idx_col}")}</th>'
                else:
                    header_cells += f"<th>{c}</th>"
            for idx_row, (i, r) in enumerate(dataframe.iterrows()):
                cells = _td("#", str(i))
                for c in cols:
                    val = r[c]
                    if c == "Company":
                        tip = COMPANY_SUMMARIES.get(r["Ticker"], "")
                        cells += (
                            _td(c, _tip(val, tip, extra_class="scoop-name-tip"), COLUMN_TIPS.get(c, "")) if tip else _td(c, str(val), COLUMN_TIPS.get(c, ""))
                        )
                    elif c == "Headlines":
                        hl_pairs = headline_map.get(r["Ticker"], [])
                        if hl_pairs:
                            cells += _td(c, _headlines_tip(val, hl_pairs, idx_row), COLUMN_TIPS.get(c, ""))
                        else:
                            cells += _td(c, str(val), COLUMN_TIPS.get(c, ""))
                    elif c == "Analyze":
                        src = source_ticker_map.get(r["Ticker"], r["Ticker"])
                        cells += _td(
                            c,
                            analyze_link_html(src, from_path="/NYSE_Top_10"),
                            COLUMN_TIPS.get(c, ""),
                        )
                    else:
                        cells += _td(c, str(val), COLUMN_TIPS.get(c, ""))
                rows_html += f"<tr>{cells}</tr>"
            return (
                f'<div class="full-results-wrap commodity-results">'
                f'<table class="full-results-table"><thead><tr>{header_cells}</tr></thead>'
                f"<tbody>{rows_html}</tbody></table></div>"
            )

        st.markdown(_build_html_table(display_df), unsafe_allow_html=True)

        # ── Explanation card ──────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            """
            #### 🧠 Why these assets were selected

            | Criterion | Check |
            |-----------|-------|
            | **Near 52-week low** | Price is within 30% of the lowest price in the past year (15% preferred) |
            | **No scandal headlines** | Sentiment screening filters negative keywords—including scandal, bankruptcy, fraud, lawsuits, and delisting |
            | **Headline context** | Click **Analyze** for detailed headline sentiment and charts |

            > **Disclaimer:** This is an automated screen — not financial advice.
            > Always do your own due diligence before investing.
            """
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
        Past performance is not indicative of future results.
    </div>
    """,
    unsafe_allow_html=True,
)

if not agreed:
    sync_screener_gating_layout(st, gated=True)

import importlib
import tooltip_scroll as _tooltip_scroll
importlib.reload(_tooltip_scroll)
_tooltip_scroll.install_tooltip_scroll_handler()
inject_desktop_headlines_dismiss()
inject_desktop_screener_tips()
import desktop_headlines_narrow as _hl_narrow
importlib.reload(_hl_narrow)
_hl_narrow.inject_desktop_headlines_narrow()
inject_post_consent_mobile_screener_hide()
