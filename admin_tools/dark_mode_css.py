"""Color-only dark mode overrides (layout/s sizing unchanged)."""

from admin_tools.tablet_mobile_layout_css import DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS

DARK_MODE_CSS = """
html[data-scoop-theme="dark"],
html[data-scoop-theme="dark"] body {
    background-color: #0b1220 !important;
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] [data-testid="stApp"],
html[data-scoop-theme="dark"] .stApp,
html[data-scoop-theme="dark"] [data-testid="stAppViewContainer"],
html[data-scoop-theme="dark"] [data-testid="stMainBlockContainer"],
html[data-scoop-theme="dark"] section.main {
    background-color: #0b1220 !important;
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] [data-testid="stHeader"],
html[data-scoop-theme="dark"] [data-testid="stToolbar"] {
    background-color: #0f172a !important;
}

html[data-scoop-theme="dark"] [data-testid="stSidebar"],
html[data-scoop-theme="dark"] [data-testid="stSidebar"] > div,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background-color: #111827 !important;
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] h1,
html[data-scoop-theme="dark"] h2,
html[data-scoop-theme="dark"] h3,
html[data-scoop-theme="dark"] h4,
html[data-scoop-theme="dark"] h5,
html[data-scoop-theme="dark"] h6,
html[data-scoop-theme="dark"] p,
html[data-scoop-theme="dark"] li,
html[data-scoop-theme="dark"] span,
html[data-scoop-theme="dark"] label,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] p,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] li,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] span,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] div,
html[data-scoop-theme="dark"] .stMarkdown p,
html[data-scoop-theme="dark"] .stCaption p {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] .scoop-full-results-heading,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    color: #0f172a !important;
}
html[data-scoop-theme="dark"] .scoop-full-results-heading .scoop-fr-title-box,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading .scoop-fr-title-box {
    display: inline-block !important;
    border: 2px solid #ffffff !important;
    border-radius: 10px !important;
    padding: 0.2em 0.55em !important;
    background: #ffffff !important;
    color: #0f172a !important;
    box-sizing: border-box !important;
}
@media (max-width: 1366px) {
    html[data-scoop-theme="dark"] .scoop-full-results-heading,
    html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-weight: 800 !important;
    }
    html[data-scoop-theme="dark"] .scoop-full-results-heading .scoop-fr-title-box,
    html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] .scoop-full-results-heading .scoop-fr-title-box {
        display: inline-block !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
        padding: 0.2em 0.55em !important;
        background: #ffffff !important;
        color: #0f172a !important;
        box-sizing: border-box !important;
        font-weight: 800 !important;
    }
}

html[data-scoop-theme="dark"] .sidebar-brand,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] .sidebar-brand {
    background: #111827 !important;
    color: #f1f5f9 !important;
}

html[data-scoop-theme="dark"] .sidebar-brand-text,
html[data-scoop-theme="dark"] #scoop-title,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] .sidebar-brand-text,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] #scoop-title {
    color: #f1f5f9 !important;
    text-decoration-color: #94a3b8 !important;
}

html[data-scoop-theme="dark"] [data-testid="stSidebar"] h1,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] p,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] label,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] span,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] a,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] a,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] span,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] p {
    color: #f1f5f9 !important;
}

html[data-scoop-theme="dark"] [data-testid="stMetricLabel"] p,
html[data-scoop-theme="dark"] [data-testid="stMetricLabel"] div {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] [data-testid="stMetricValue"] > div {
    color: #f8fafc !important;
}

html[data-scoop-theme="dark"] [data-testid="stTextInput"] label p,
html[data-scoop-theme="dark"] [data-testid="stTextInput"] input,
html[data-scoop-theme="dark"] div[data-baseweb="input"] input {
    color: #f1f5f9 !important;
    background-color: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] div[data-baseweb="input"] > div {
    background-color: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .stAlert,
html[data-scoop-theme="dark"] [data-testid="stAlert"],
html[data-scoop-theme="dark"] .stInfo,
html[data-scoop-theme="dark"] .stSuccess,
html[data-scoop-theme="dark"] .stWarning,
html[data-scoop-theme="dark"] .stError {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] table,
html[data-scoop-theme="dark"] [data-testid="stTable"],
html[data-scoop-theme="dark"] .stMarkdown table {
    background-color: #111827 !important;
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] table th,
html[data-scoop-theme="dark"] [data-testid="stMarkdownContainer"] table td,
html[data-scoop-theme="dark"] [data-testid="stTable"] th,
html[data-scoop-theme="dark"] [data-testid="stTable"] td,
html[data-scoop-theme="dark"] .stMarkdown table th,
html[data-scoop-theme="dark"] .stMarkdown table td {
    color: #e2e8f0 !important;
    border-color: #334155 !important;
}

html[data-scoop-theme="dark"] .stMarkdown table tr:hover {
    background-color: rgba(148, 163, 184, 0.12) !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-table .fr-label,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table .fr-label,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .tip-wrap {
    color: #e2e8f0 !important;
}

@media (min-width: 1367px) {
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap:not(.headlines-tip) {
    border-bottom-color: #64748b !important;
}
}

@media (max-width: 1366px) {
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown [data-testid="stMarkdownContainer"] .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown div .tip-wrap:not(.headlines-tip) {
    border-bottom: 2px dashed #ffffff !important;
}

html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip {
    border-bottom: none !important;
}

html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
    border-bottom: 2px dashed #ffffff !important;
    display: inline-block !important;
    text-decoration: none !important;
}
}

html[data-scoop-theme="dark"] [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]),
html[data-scoop-theme="dark"] .stApp div[data-testid="metric-container"],
html[data-scoop-theme="dark"] .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"],
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody tr,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td,
html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody tr,
html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody td {
    background: #1e293b !important;
    border-color: #475569 !important;
    color: #e2e8f0 !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22) !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td {
    border-bottom-color: #334155 !important;
}

@media (max-width: 1366px) {
    html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody tr,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody tr,
    html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody tr {
        border: 2px solid #22c55e !important;
        border-left: 6px solid #22c55e !important;
    }
    html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td,
    html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody td {
        border-color: transparent !important;
        box-shadow: none !important;
    }
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-mobile-legend {
    background: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
    border-bottom-color: #334155 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-mobile-legend p {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-mobile-legend strong {
    color: #f1f5f9 !important;
}

html[data-scoop-theme="dark"] .tip-wrap .tip-count,
html[data-scoop-theme="dark"] .tip-wrap .hl-tip-count {
    color: #93c5fd !important;
}

html[data-scoop-theme="dark"] .tip-wrap .tip-text,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap .tip-text {
    background: #0f172a !important;
    color: #e5e7eb !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45) !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text {
    background-color: #111827 !important;
    color: #f1f5f9 !important;
}

@media (max-width: 1366px) {
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text {
    border: 2px solid #ffffff !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
    background-color: #111827 !important;
    color: #f1f5f9 !important;
    border: 2px solid #ffffff !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.45) !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll,
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
}
}

@media (max-width: 1366px) {
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll li,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll a {
    color: #e2e8f0 !important;
}
}

@media (min-width: 1367px) {
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
    border: 2px solid #ffffff !important;
}
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll a,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll a {
    color: #ffffff !important;
}
}

html[data-scoop-theme="dark"] div[data-testid="stCheckbox"] {
    background-color: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] div[data-testid="stCheckbox"] label p {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] .disclaimer-footer,
html[data-scoop-theme="dark"] .disclaimer-footer p,
html[data-scoop-theme="dark"] .disclaimer-footer strong {
    background-color: #0f172a !important;
    color: #cbd5e1 !important;
    border-color: #334155 !important;
}

html[data-scoop-theme="dark"] .disclaimer-footer a {
    background-color: #0f172a !important;
    color: #93c5fd !important;
    border-color: #334155 !important;
    text-decoration: underline !important;
    text-underline-offset: 0.14em !important;
}

html[data-scoop-theme="dark"] .scoop-selected-asset-card {
    background-color: #1e293b !important;
    border-color: #475569 !important;
    border-left-color: #60a5fa !important;
}

html[data-scoop-theme="dark"] .scoop-selected-asset-card .scoop-muted {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .scoop-selected-asset-card .scoop-title-text {
    color: #f8fafc !important;
}

html[data-scoop-theme="dark"] .scoop-selected-asset-card .scoop-subtitle-text {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .scoop-crypto-price-card {
    background: #1e293b !important;
    box-shadow: 0 8px 22px rgba(2, 6, 23, 0.35) !important;
}
@media (max-width: 1366px) {
    html[data-scoop-theme="dark"] .scoop-crypto-price-card,
    html[data-scoop-theme="dark"] body .stApp .scoop-crypto-price-card {
        border: 2px solid #22c55e !important;
        border-left: 6px solid #22c55e !important;
    }
    html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-item,
    html[data-scoop-theme="dark"] body .stApp .scoop-crypto-price-card .cpc-item {
        border: 2px solid #ffffff !important;
    }
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-kicker,
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-label {
    color: #94a3b8 !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-live-value,
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-value,
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-section {
    color: #f8fafc !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-section {
    border-top-color: #334155 !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-item {
    background: #0f172a !important;
    border: 2px solid #e2e8f0 !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-meta {
    color: #cbd5e1 !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-delta.up,
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-meta.up {
    color: #86efac !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-delta.up {
    background: #14532d !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-delta.down,
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-meta.down {
    color: #fca5a5 !important;
}
html[data-scoop-theme="dark"] .scoop-crypto-price-card .cpc-delta.down {
    background: #7f1d1d !important;
}

html[data-scoop-theme="dark"] .scoop-mood-summary {
    background-color: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .scoop-mood-summary .scoop-mood-label {
    color: #f1f5f9 !important;
}

html[data-scoop-theme="dark"] .scoop-mood-summary .scoop-mood-detail {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .mood-feed {
    background-color: #111827 !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .mood-feed table th,
html[data-scoop-theme="dark"] .mood-feed table td,
html[data-scoop-theme="dark"] .mood-feed table a {
    color: #e2e8f0 !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] a {
    color: #93c5fd !important;
}

html[data-scoop-theme="dark"] hr.search-52w-range-divider {
    border-color: #475569 !important;
    background-color: #475569 !important;
}

html[data-scoop-theme="dark"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
html[data-scoop-theme="dark"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
html[data-scoop-theme="dark"] [data-testid="stHeader"] [data-testid="collapsedControl"] button {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] .js-plotly-plot .plotly .bg {
    fill: #111827 !important;
}

html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
html[data-scoop-theme="dark"] [data-testid="stSidebar"] .stCheckbox label p {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-baseweb="switch"] {
    background-color: #334155 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td,
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td a,
html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody td,
html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table tbody td a {
    color: #e2e8f0 !important;
}

html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table thead th,
html[data-scoop-theme="dark"] .stMarkdown .top-picks-wrap .top-picks-table thead th {
    background-color: #0f172a !important;
    color: #f1f5f9 !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .landing-hero p {
    color: #cbd5e1 !important;
}

html[data-scoop-theme="dark"] .landing-card {
    background: #1e293b !important;
    border-color: #475569 !important;
}

html[data-scoop-theme="dark"] .landing-card p {
    color: #cbd5e1 !important;
}

@media (max-width: 1366px) {
    html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        color: #93c5fd !important;
    }
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"],
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] svg,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] button {
        color: #ffffff !important;
        stroke: #ffffff !important;
    }
}
""" + DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS
