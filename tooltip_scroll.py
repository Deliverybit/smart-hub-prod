import json

import streamlit as st

from admin_tools.tablet_mobile_layout_css import (
    DESKTOP_ANALYZE_TOP_COMPACT,
    RESPONSIVE_ANALYZE_TOP_COMPACT,
    CRYPTO_ANALYZE_RESPONSIVE_METRICS_CSS,
    DESKTOP_SCREENER_TOP_COMPACT,
    DESKTOP_SCREENER_GATING_LAYOUT,
    RESPONSIVE_SCREENER_TOP_COMPACT,
    MOBILE_TABLET_INDEX_BANNER_CSS,
    RESPONSIVE_TERMS_TOP_COMPACT,
    DESKTOP_TERMS_TOP_COMPACT,
    DESKTOP_SIDEBAR_LAYOUT,
    DESKTOP_SIDEBAR_NAV_MARKET,
    DESKTOP_ZOOM_LAYOUT,
    MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS,
    MOBILE_CARD_FIELD_ORDER,
    MOBILE_HEADLINES_CARD_OVERLAY,
    DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS,
    RESPONSIVE_GENERIC_TOOLTIP_LAYOUT,
    EARLY_STREAMLIT_CHROME_HIDE,
    RESPONSIVE_SIDEBAR_BOOTSTRAP,
    RESPONSIVE_TAB_NAV_BOOTSTRAP,
    MOBILE_TABLET_HL_HEADING_COLOR_CSS,
    SIDEBAR_NAV_COMPACT,
    RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER,
    DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER,
    DESKTOP_SIDEBAR_LOGO_RULES,
    DESKTOP_TABLET_DISCLAIMER_FLOW,
    TABLET_ANALYZE_LINK_CSS,
    PHONE_ANALYZE_MOBILE_TIP_CSS,
    _MOBILE_TABLET_ANALYZE_LINK_FINAL,
    IPAD_MINI_POPUP_CLAMP_CSS,
)

_MOBILE_HEADLINES_CSS = f"""
@media (max-width: 743px) {{
{MOBILE_HEADLINES_CARD_OVERLAY}
}}
"""

_MOBILE_PHONE_HEADLINES_FIXED_CSS = """
@media (max-width: 743px) {
    /* Phone mobile: fixed panel at top of page; width inset inside card; heading never clipped. */
    .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
        position: static !important;
        z-index: auto !important;
        overflow: visible !important;
    }
    .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
        position: static !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
        position: static !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        position: fixed !important;
        top: var(--hl-fixed-top, calc(5.6rem + env(safe-area-inset-top, 0px))) !important;
        left: var(--hl-fixed-left, 0.75rem) !important;
        right: auto !important;
        bottom: auto !important;
        width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        height: auto !important;
        max-height: var(--hl-fixed-max-height, 75dvh) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        overflow: hidden !important;
        transform: none !important;
        position-anchor: none !important;
        anchor-name: none !important;
        z-index: 100002 !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        position: relative !important;
        top: auto !important;
        left: auto !important;
        width: auto !important;
        max-width: none !important;
        flex: 0 0 auto !important;
        flex-shrink: 0 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        overflow: visible !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
        color: #93c5fd !important;
        background: #1e1e2f !important;
        border: none !important;
        border-bottom: 1px solid #334155 !important;
        border-radius: 14px 14px 0 0 !important;
        padding: 0.55rem 0.75rem !important;
        font-size: calc(0.82rem + 4pt) !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
        z-index: 2 !important;
    }
    html.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading,
    body.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        visibility: visible !important;
        opacity: 1 !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        max-height: none !important;
        margin-top: 0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
        overscroll-behavior-y: contain !important;
        padding: 0.28rem 0.35rem 0.35rem 0.55rem !important;
    }
    html.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    body.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }
}
"""

_MOBILE_TABLET_CARD_ORDER_CSS = f"""
@media (max-width: 1366px),
       (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px) {{
{MOBILE_CARD_FIELD_ORDER}
}}
"""

_RESPONSIVE_GENERIC_TOOLTIP_CSS = f"""
@media (max-width: 1366px) {{
{RESPONSIVE_GENERIC_TOOLTIP_LAYOUT}
}}
"""

_GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS = """
(() => {
    const VERSION = 22;
    let appDoc = document;
    let appWin = window;
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            appDoc = window.parent.document;
            appWin = window.parent;
        }
    } catch (e) {
        appDoc = document;
        appWin = window;
    }
    if (appWin.__scoopGenericTooltipBindVersion === VERSION) {
        return;
    }
    appWin.__scoopGenericTooltipBindVersion = VERSION;

    const DESKTOP_MIN = 1367;
    const OPEN_CLASS = "scoop-desktop-name-tip-open";
    const HEADER_OPEN = "scoop-desktop-header-tip-open";
    const GENERIC_OPEN = "scoop-desktop-generic-tip-open";
    const TIP_CLEAR_PROPS = [
        "position",
        "left",
        "top",
        "right",
        "bottom",
        "transform",
        "width",
        "max-width",
        "min-width",
        "max-height",
        "overflow-y",
        "visibility",
        "opacity",
        "margin-left",
        "z-index",
        "pointer-events",
        "display",
        "--tip-center-x",
        "--tip-center-y",
        "--tip-fixed-width",
        "--tip-fixed-max-height",
        "--scoop-mobile-tip-top",
        "--scoop-se-name-tip-top",
    ];
    const isDesktop = () => (appWin.innerWidth || 0) >= DESKTOP_MIN;

    const isDesktopHeaderTip = (wrap) =>
        !!(wrap && wrap.classList && !wrap.classList.contains("headlines-tip") && wrap.closest("thead"));

    const isDesktopNameTip = (wrap) => {
        if (!wrap || !wrap.classList || wrap.classList.contains("headlines-tip")) {
            return false;
        }
        if (wrap.classList.contains("scoop-name-tip")) {
            return true;
        }
        const td = wrap.closest(
            'td[data-label="Company"], td[data-label="Name"], td[data-label="Commodity"]'
        );
        return !!(td && wrap.closest(".fr-val"));
    };

    const clearDesktopNameTipLayout = (wrap) => {
        wrap.classList.remove(OPEN_CLASS);
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        TIP_CLEAR_PROPS.forEach((prop) => tip.style.removeProperty(prop));
        tip.style.setProperty("display", "none", "important");
        tip.style.setProperty("visibility", "hidden", "important");
        tip.style.setProperty("opacity", "0", "important");
        tip.style.setProperty("pointer-events", "none", "important");
        tip.style.setProperty("transition", "none", "important");
    };

    const resetGenericTooltips = () => {
        appDoc.querySelectorAll(".tip-wrap:not(.headlines-tip)").forEach((wrap) => {
            wrap.classList.remove(
                "generic-tip-open",
                "scoop-mobile-tip-open",
                OPEN_CLASS,
                HEADER_OPEN,
                GENERIC_OPEN
            );
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) {
                return;
            }
            TIP_CLEAR_PROPS.forEach((prop) => tip.style.removeProperty(prop));
        });
    };

    const getDesktopLayoutParts = () => {
        const view = appDoc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = appDoc.querySelector('section[data-testid="stSidebar"]');
        if (!view) {
            return { view: null, sidebar: null, main: null };
        }
        const main = [...view.children].find(
            (child) => child.getAttribute("data-testid") !== "stSidebar"
        );
        return { view, sidebar: sidebar || null, main: main || null };
    };

    // Fixed positioning escapes column overflow clipping under the sidebar.
    // First-column tips (CME/Crypto/etc.) are pinned just right of the nav, like NASDAQ.
    const positionDesktopNameTip = (wrap) => {
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip || !isDesktop() || !wrap.classList.contains(OPEN_CLASS)) {
            return;
        }
        const { sidebar } = getDesktopLayoutParts();
        const gap = 12;
        const sbRight = sidebar ? sidebar.getBoundingClientRect().right : 0;
        const viewRight =
            Math.min(
                appWin.innerWidth - gap,
                (appDoc.documentElement && appDoc.documentElement.clientWidth) || appWin.innerWidth
            ) - gap;
        const minW = 360;
        const maxW = Math.max(minW, Math.min(700, viewRight - (sbRight + gap)));

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "none", "important");
        tip.style.setProperty("z-index", "2147483000", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("white-space", "normal", "important");
        tip.style.setProperty("overflow-wrap", "break-word", "important");
        tip.style.setProperty("word-break", "normal", "important");
        tip.style.setProperty("box-sizing", "border-box", "important");
        tip.style.setProperty("font-size", "1.25rem", "important");
        tip.style.setProperty("line-height", "1.55", "important");
        tip.style.setProperty("padding", "1.15rem 1.35rem", "important");
        tip.style.setProperty("min-width", `${minW}px`, "important");
        tip.style.setProperty("max-width", `${maxW}px`, "important");
        tip.style.setProperty("width", "auto", "important");

        const raw = wrap.getBoundingClientRect();
        const vh = appWin.innerHeight || 800;
        const visTop = Math.min(Math.max(raw.top, gap), vh - gap);
        const visBottom = Math.max(Math.min(raw.bottom, vh - gap), visTop + 8);
        const tipRect = tip.getBoundingClientRect();
        const height = Math.min(tipRect.height || 72, vh - gap * 2);
        const boxW = Math.max(minW, Math.min(maxW, tipRect.width || minW));

        // Use the on-screen slice of the name so tall table cells do not park the tip off-screen.
        let left = raw.left + raw.width / 2 - boxW / 2;
        if (left < sbRight + gap) {
            left = sbRight + gap;
        }
        if (left + boxW > viewRight) {
            left = Math.max(sbRight + gap, viewRight - boxW);
        }
        let top = visTop - height - 12;
        if (top < gap) {
            top = Math.min(vh - height - gap, visBottom + 12);
        }
        top = Math.max(gap, Math.min(top, vh - height - gap));

        tip.style.setProperty("left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("top", `${Math.round(top)}px`, "important");
    };

    const openDesktopNameTip = (wrap) => {
        if (!isDesktop() || !isDesktopNameTip(wrap)) {
            return;
        }
        appDoc.querySelectorAll(`.tip-wrap.${OPEN_CLASS}`).forEach((other) => {
            if (other !== wrap) {
                clearDesktopNameTipLayout(other);
            }
        });
        wrap.classList.add(OPEN_CLASS);
        const tip = wrap.querySelector(":scope > .tip-text");
        if (tip) {
            tip.style.setProperty("display", "block", "important");
        }
        positionDesktopNameTip(wrap);
        appWin.requestAnimationFrame(() => {
            positionDesktopNameTip(wrap);
            appWin.requestAnimationFrame(() => positionDesktopNameTip(wrap));
        });
    };

    const closeDesktopNameTip = (wrap) => {
        if (!wrap || !wrap.classList.contains(OPEN_CLASS)) {
            return;
        }
        clearDesktopNameTipLayout(wrap);
    };

    const bindDesktopNameTips = () => {
        if (appWin.__scoopGenericTooltipNameOver) {
            appDoc.removeEventListener("mouseover", appWin.__scoopGenericTooltipNameOver, true);
            appDoc.removeEventListener("mouseout", appWin.__scoopGenericTooltipNameOut, true);
            appDoc.removeEventListener("mouseleave", appWin.__scoopGenericTooltipNameOut, true);
        }
        const onOver = (event) => {
            if (!isDesktop()) {
                return;
            }
            const raw = event.target;
            const el = raw && raw.nodeType === 1 ? raw : raw && raw.parentElement;
            if (!el || typeof el.closest !== "function") {
                return;
            }
            const wrap = el.closest(".tip-wrap:not(.headlines-tip)");
            if (!wrap) {
                return;
            }
            if (isDesktopNameTip(wrap)) {
                openDesktopNameTip(wrap);
                return;
            }
            wrap.classList.add(GENERIC_OPEN);
            if (isDesktopHeaderTip(wrap)) {
                wrap.classList.add(HEADER_OPEN);
            }
        };
        const onOut = (event) => {
            const raw = event.target;
            const el = raw && raw.nodeType === 1 ? raw : raw && raw.parentElement;
            if (!el || typeof el.closest !== "function") {
                return;
            }
            const wrap = el.closest(".tip-wrap:not(.headlines-tip)");
            if (!wrap) {
                return;
            }
            const related = event.relatedTarget;
            if (related && typeof related.nodeType === "number") {
                if (wrap.contains(related)) {
                    return;
                }
            }
            wrap.classList.remove(HEADER_OPEN, GENERIC_OPEN);
            if (wrap.classList.contains(OPEN_CLASS)) {
                try {
                    if (wrap.matches(":hover")) {
                        return;
                    }
                } catch (e) {}
                closeDesktopNameTip(wrap);
            }
        };
        appWin.__scoopGenericTooltipNameOver = onOver;
        appWin.__scoopGenericTooltipNameOut = onOut;
        appDoc.addEventListener("mouseover", onOver, true);
        appDoc.addEventListener("mouseout", onOut, true);
        appWin.addEventListener(
            "scroll",
            () => {
                if (!isDesktop()) {
                    return;
                }
                appDoc.querySelectorAll(`.tip-wrap.${OPEN_CLASS}`).forEach(positionDesktopNameTip);
            },
            true
        );
        appWin.addEventListener("resize", () => {
            if (!isDesktop()) {
                appDoc.querySelectorAll(`.tip-wrap.${OPEN_CLASS}`).forEach(closeDesktopNameTip);
                return;
            }
            appDoc.querySelectorAll(`.tip-wrap.${OPEN_CLASS}`).forEach(positionDesktopNameTip);
        });
    };

    resetGenericTooltips();
    bindDesktopNameTips();
    appWin.__scoopGenericTooltipApi = {
        positionGenericTooltip: () => {},
        scheduleGenericTooltipPosition: () => {},
        repositionVisibleGenericTooltips: resetGenericTooltips,
    };
})();
"""

_GENERIC_TOOLTIP_MOBILE_JS = _GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS

GENERIC_TOOLTIP_CSS_VERSION = 33
GENERIC_TOOLTIP_CSS_KEY = "_scoop_generic_tooltip_css_version"

_DARK_RESPONSIVE_TIP_UNDERLINE_CSS = (
    """
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
"""
    + DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS
)

# Tip popup outlines: same on phone/tablet/desktop.
# Light/normal: green (#22c55e). Dark: white. Beats page `border: 1px solid #555`.
_DARK_POPUP_OUTLINE_CSS = """
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip .tip-text,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip) .tip-text {
    border: 2px solid #ffffff !important;
}
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
    border: 2px solid #ffffff !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.45) !important;
}
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll,
html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
}
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip .tip-text,
html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip .tip-text,
html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip) .tip-text {
    border: 2px solid #22c55e !important;
}
"""

_DESKTOP_HEADLINES_CSS = """
@media (min-width: 1367px) {
    /* Desktop: count only — hide checkbox chrome and wrap border (avoids ". 10" artifact). */
    .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb,
    .full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb,
    .tip-wrap.headlines-tip .hl-tip-cb {
        display: none !important;
        appearance: none !important;
        position: absolute !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip,
    .tip-wrap.headlines-tip {
        border-bottom: none !important;
        line-height: inherit !important;
        font-size: inherit !important;
    }
    .stMarkdown .tip-wrap.headlines-tip .hl-tip-count,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .hl-tip-count,
    .tip-wrap.headlines-tip .hl-tip-count {
        cursor: pointer !important;
        text-decoration: inherit !important;
        pointer-events: auto !important;
        display: inline-block !important;
        line-height: inherit !important;
        font-size: inherit !important;
        list-style: none !important;
        border-bottom: 1px dashed #888 !important;
    }
    html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .hl-tip-count,
    html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .hl-tip-count {
        border-bottom: 2px dashed #ffffff !important;
    }
    .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .hl-tip-backdrop {
        display: none !important;
    }
    .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
        display: block !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 100019 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: default !important;
        pointer-events: auto !important;
    }
    .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
        display: none !important;
    }
    /* JS positions via --hl-fixed-*; disable anchor positioning (stray box at row). */
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
        position-anchor: none !important;
        anchor-name: none !important;
        position: fixed !important;
        top: var(--hl-fixed-top, -10000px) !important;
        left: var(--hl-fixed-left, -10000px) !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: none !important;
        transition: none !important;
        --hl-pop-w: min(28rem, 44vw);
        --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
        height: var(--hl-fixed-height, auto) !important;
        min-height: 0 !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        overflow: hidden !important;
        padding: 0 !important;
        z-index: 100020 !important;
        box-sizing: border-box !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)):not(.hl-tip-desktop-open):hover > .tip-text,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)):not(.hl-tip-desktop-open) > .tip-text:hover {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        left: -10000px !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        position: fixed !important;
        /* Stay in the desktop slot. Never use a bare var() — invalid left
           collapses the panel into the ~40px count cell. */
        top: var(--hl-fixed-top, 12px) !important;
        left: var(--hl-fixed-left, -10000px) !important;
        width: var(--hl-fixed-width, 410px) !important;
        min-width: 410px !important;
        max-width: var(--hl-fixed-width, 44vw) !important;
        right: auto !important;
        bottom: auto !important;
        transform: none !important;
        background: #111827 !important;
        border: 2px solid #22c55e !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        height: var(--hl-fixed-height, auto) !important;
        min-height: 280px !important;
        overflow: hidden !important;
        overscroll-behavior: contain !important;
        touch-action: pan-y !important;
        transition: none !important;
        z-index: 100020 !important;
    }
    /* Desktop light: green container outline. */
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        border: 2px solid #22c55e !important;
        outline: none !important;
    }
    /* Desktop dark: white container outline and white headline links. */
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        border: 2px solid #ffffff !important;
        outline: none !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        display: block !important;
        visibility: visible !important;
        position: relative !important;
        top: auto !important;
        z-index: 2 !important;
        margin: 0 !important;
        padding: 0.75rem 0.7rem 0.55rem 0.7rem !important;
        background: #1e1e2f !important;
        color: #93c5fd !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        line-height: 1.3 !important;
        border: 0 !important;
        border-bottom: 1px solid #334155 !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        white-space: normal !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        display: block !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        max-height: var(--hl-scroll-max-height, none) !important;
        overscroll-behavior: contain !important;
        overscroll-behavior-y: contain !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: thin !important;
        scrollbar-gutter: auto !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
        padding: 0.65rem 1rem 0.65rem 1rem !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.45rem !important;
        min-width: 0 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
        display: block !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        min-width: 0 !important;
        font-size: 1.25rem !important;
        line-height: 1.55 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::before,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::after {
        display: none !important;
    }
    html.scoop-tooltip-scrolling .full-results-wrap .tip-wrap.headlines-tip:not(.hl-tip-desktop-open):not(:has(.hl-tip-cb:checked)) .tip-text,
    body.scoop-tooltip-scrolling .full-results-wrap .tip-wrap.headlines-tip:not(.hl-tip-desktop-open):not(:has(.hl-tip-cb:checked)) .tip-text {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    /* Override page/tablet rules inside stMarkdown on desktop open state. */
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        display: flex !important;
        flex-direction: column !important;
        position: fixed !important;
        top: var(--hl-fixed-top, 12px) !important;
        left: var(--hl-fixed-left, -10000px) !important;
        overflow: hidden !important;
        touch-action: pan-y !important;
        height: var(--hl-fixed-height, auto) !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        width: var(--hl-fixed-width, 160px) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, 160px) !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-height: 4.5rem !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        visibility: visible !important;
        opacity: 1 !important;
        max-height: var(--hl-scroll-max-height, none) !important;
        scrollbar-width: thin !important;
        scrollbar-gutter: auto !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-list,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
        pointer-events: auto !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line {
        color: #ffffff !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        color: #ffffff !important;
        text-decoration: underline !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        color: #ffffff !important;
        text-decoration: underline !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
}
"""

_DESKTOP_TOOLTIP_TYPE_CSS = """
@media (min-width: 1367px) {
    .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
    .full-results-wrap .full-results-table .tip-wrap:not(.headlines-tip) .tip-text,
    .full-results-table thead .tip-wrap .tip-text,
    [data-testid="stMarkdownContainer"] .tip-wrap:not(.headlines-tip) .tip-text {
        font-size: 1.25rem !important;
        line-height: 1.55 !important;
    }
    .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-name-tip) .tip-text,
    .full-results-wrap .full-results-table .tip-wrap:not(.headlines-tip):not(.scoop-name-tip) .tip-text,
    .full-results-table thead .tip-wrap .tip-text,
    [data-testid="stMarkdownContainer"] .tip-wrap:not(.headlines-tip):not(.scoop-name-tip) .tip-text {
        padding: 1.15rem 1.35rem !important;
        min-width: 24rem !important;
        max-width: min(44rem, calc(100vw - 2rem)) !important;
    }
    .stMarkdown .tip-wrap .tip-text a,
    .full-results-wrap .tip-wrap .tip-text a {
        font-size: inherit !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip):not(.scoop-name-tip) .tip-text {
        font-size: 1.2rem !important;
        min-width: 20rem !important;
        max-width: min(30rem, calc(100vw - 2rem)) !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.scoop-name-tip .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
        width: auto !important;
        min-width: 360px !important;
        max-width: min(700px, calc(100vw - 2rem)) !important;
        font-size: 1.25rem !important;
        line-height: 1.55 !important;
        padding: 1.15rem 1.35rem !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        height: auto !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        font-size: 1.65rem !important;
        line-height: 1.3 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
        font-size: 1.25rem !important;
        line-height: 1.55 !important;
    }

    /* Closed body tips must not stay in table layout. Header tips stay CSS-hover. */
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.scoop-name-tip:not(.scoop-desktop-name-tip-open) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:not(.hl-tip-desktop-open):not(:has(.hl-tip-cb:checked)) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-name-tip:not(.scoop-desktop-name-tip-open) > .tip-text {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-desktop-generic-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-desktop-header-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead .tip-wrap.scoop-desktop-header-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead .tip-wrap:hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead .tip-wrap .tip-text:hover {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
        z-index: 2147483000 !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead tr,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table thead th {
        overflow: visible !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap {
        display: inline-block !important;
        max-width: 100% !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody a.fr-analyze-link,
    html body .stApp [data-testid="stAppViewContainer"] .disclaimer-footer a,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text a,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text a {
        display: inline !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)):not(.hl-tip-desktop-open) .headlines-tip-list {
        display: none !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody tr,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td {
        overflow: visible !important;
    }

    /*
     * Desktop name tips: CSS :hover paints a cell-clipped vertical box after the
     * JS fixed (horizontal) tip closes. Never show name tips via CSS hover.
     */
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-name-tip > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-name-tip:hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.scoop-name-tip .tip-text:hover,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip):hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip):hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip):hover > .tip-text {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transition: none !important;
        position: fixed !important;
        left: -10000px !important;
        top: -10000px !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .tip-wrap.scoop-desktop-name-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .tip-wrap.scoop-name-tip.scoop-desktop-name-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .tip-wrap.scoop-desktop-name-tip-open:hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap.scoop-desktop-name-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap.scoop-desktop-name-tip-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap.scoop-desktop-name-tip-open > .tip-text {
        display: block !important;
        position: fixed !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: none !important;
        z-index: 2147483000 !important;
        transform: none !important;
        bottom: auto !important;
        right: auto !important;
        margin: 0 !important;
        left: auto !important;
        top: auto !important;
        transition: none !important;
    }
    /* Match mobile/tablet tip outlines on desktop. */
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
        border: 2px solid #22c55e !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
        border: 2px solid #ffffff !important;
    }
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        border: 2px solid #22c55e !important;
    }
}
"""

_TABLET_HEADLINES_POPUP_RULES = """
    /* Tablet / iPad Pro-style headlines popup (fixed slot via --hl-fixed-*). */
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
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        touch-action: auto !important;
        text-align: left !important;
        transform: none !important;
        position-anchor: none !important;
        anchor-name: none !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        z-index: 100002 !important;
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        box-sizing: border-box !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
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
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        min-height: 0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
        overscroll-behavior-y: contain !important;
    }
"""

_TABLET_HEADLINES_POPUP_CSS = f"""
@media (min-width: 769px) and (max-width: 1366px) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_IPAD_MINI_HEADLINES_CSS = f"""
@media (min-width: 744px) and (max-width: 768px) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_SURFACE_DUO_HEADLINES_CSS = f"""
@media (width: 540px),
       ((width: 720px) and (max-height: 541px)),
       ((min-width: 1110px) and (max-width: 1118px) and (max-height: 741px)) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_IPAD_MINI_SURFACE_DUO_HEADLINES_CSS = _IPAD_MINI_HEADLINES_CSS + _SURFACE_DUO_HEADLINES_CSS

_ASUS_ZENBOOK_FOLD_HEADLINES_CSS = f"""
@media (min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),
       (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px),
       (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),
       (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),
       (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_RESPONSIVE_DOC_HELPER_JS = """
const __scoopGetAppDoc = () => {
    try {
        const parentDoc = window.parent && window.parent.document;
        if (parentDoc && parentDoc.querySelector('[data-testid="stAppViewContainer"]')) {
            return parentDoc;
        }
    } catch (e) {}
    return document;
};
const __scoopGetAppWin = () => __scoopGetAppDoc().defaultView || window;
const __scoopViewportWidth = () => __scoopGetAppWin().innerWidth || window.innerWidth;
const __scoopViewportHeight = () => __scoopGetAppWin().innerHeight || window.innerHeight;
const __scoopIsAnalyzePage = () => {
    try {
        return /Analyze/i.test(__scoopGetAppWin().location.pathname || "");
    } catch (e) {
        return false;
    }
};
const __scoopIsScreenerPage = () => {
    try {
        return /_Top_10/i.test(__scoopGetAppWin().location.pathname || "");
    } catch (e) {
        return false;
    }
};
const __scoopIsTermsPage = () => {
    try {
        return /Terms_of_Service/i.test(__scoopGetAppWin().location.pathname || "");
    } catch (e) {
        return false;
    }
};
const __scoopIsPhoneViewport = () => __scoopViewportWidth() <= 743;
const __scoopIsTabletViewport = () => {
    const w = __scoopViewportWidth();
    return w >= 744 && w <= 1366;
};
const __scoopIsTabletOnlyViewport = () => {
    const w = __scoopViewportWidth();
    return w >= 769 && w <= 1366;
};
// Phone + all tablet widths (≤1366): Terms stays in main-view chrome, never desktop split.
const __scoopShouldHoldTermsMainView = () => __scoopViewportWidth() <= 1366;
const __scoopClickFirstSidebarControl = (doc, selectors) => {
    for (const selector of selectors) {
        const node = doc.querySelector(selector);
        if (node) {
            node.click();
            return true;
        }
    }
    return false;
};
const __scoopApplySidebarExpandedState = (expanded) => {
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;
    const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
    if (!sidebar) {
        return;
    }
    const isExpanded = sidebar.getAttribute("aria-expanded") === "true";
    if (isExpanded === expanded) {
        layout()?.syncSidebarLayout?.();
        return;
    }
    // Mobile/tablet: tab nav replaces slideout; never click Streamlit Expand/Collapse.
    if (__scoopViewportWidth() <= 1366) {
        sidebar.setAttribute("aria-expanded", "false");
        layout()?.syncSidebarLayout?.();
        return;
    }
    sidebar.setAttribute("aria-expanded", expanded ? "true" : "false");
    layout()?.syncSidebarLayout?.();
};
const __scoopScheduleTabletSidebarLayoutSync = () => {
    if (!__scoopIsTabletOnlyViewport()) {
        return;
    }
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;
    appWin.requestAnimationFrame(() => layout()?.syncSidebarLayout?.());
    [50, 150, 350].forEach((delay) => {
        appWin.setTimeout(() => layout()?.syncSidebarLayout?.(), delay);
    });
};
const __scoopResolveTermsUrl = (link, appWin) => {
    const href = (link && (link.getAttribute("href") || link.href)) || "/Terms_of_Service";
    if (/^https?:\\/\\//i.test(href)) {
        return href;
    }
    const path = href.startsWith("/") ? href : `/${href}`;
    return `${appWin.location.origin}${path}`;
};
const __scoopNavigateMobileTerms = (link, appWin) => {
    appWin.location.assign(__scoopResolveTermsUrl(link, appWin));
};
"""

_RESPONSIVE_LAYOUT_CORE_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const appWin = __scoopGetAppWin();
    const doc = __scoopGetAppDoc();

    const PHONE_MAX = 743;
    const TABLET_MIN = 744;
    const TABLET_MAX = 1366;
    const DESKTOP_MIN = 1367;
    // Layout viewport floor when browser zoom shrinks CSS width on a physical desktop screen.
    const DESKTOP_ZOOM_MIN = 1024;

    const isPhoneViewport = () => __scoopViewportWidth() <= PHONE_MAX;
    const isSurfaceDuoViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        return (
            w === 540 ||
            (w === 720 && h <= 541) ||
            (w >= 1110 && w <= 1118 && h <= 741)
        );
    };
    const isIpad14ProMaxViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        return (
            (w >= 1028 && w <= 1036 && h >= 1370) ||
            (w >= 1370 && w <= 1382 && h <= 1040)
        );
    };
    const isAsusZenbookFoldViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        const near853 = (value) => value >= 849 && value <= 857;
        const near1280 = (value) => value >= 1276 && value <= 1284;
        const near1707 = (value) => value >= 1700 && value <= 1714;
        const near1920 = (value) => value >= 1910 && value <= 1930;
        const near1280u = (value) => value >= 1270 && value <= 1290;
        return (
            (near853(w) && near1280(h)) ||
            (near1280(w) && near853(h)) ||
            (near1707(w) && h >= 1000 && h <= 1120) ||
            (near1920(w) && near1280u(h)) ||
            (near1280u(w) && near1920(h))
        );
    };
    const isResponsiveViewport = () =>
        isPhoneViewport() ||
        isSurfaceDuoViewport() ||
        isIpad14ProMaxViewport() ||
        isAsusZenbookFoldViewport() ||
        (__scoopViewportWidth() >= TABLET_MIN && __scoopViewportWidth() <= TABLET_MAX);
    const isDesktopViewport = () => {
        const innerW = __scoopViewportWidth();
        const screenW = appWin.screen?.width || 0;
        if (isAsusZenbookFoldViewport()) {
            return false;
        }
        // Terms on phone/tablet: never treat as desktop (blocks zoom/screen-width heuristic).
        if (__scoopIsTermsPage() && innerW <= TABLET_MAX) {
            return false;
        }
        if (innerW >= DESKTOP_MIN) {
            return true;
        }
        // Browser zoom on a desktop monitor shrinks layout width below 1367px — keep split sidebar.
        return screenW >= DESKTOP_MIN && innerW >= DESKTOP_ZOOM_MIN;
    };

    const setDesktopLayoutFlag = (on) => {
        const root = doc.documentElement;
        if (on) {
            root.setAttribute("data-scoop-desktop-layout", "1");
        } else {
            root.removeAttribute("data-scoop-desktop-layout");
        }
    };

    const isAnalyzeReturnSuppressed = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        return !!(
            appWin.__scoopSuppressSidebarExpand &&
            Date.now() < appWin.__scoopSuppressSidebarExpand
        );
    };

    const shouldKeepResponsiveSidebarCollapsed = () => {
        if (!isResponsiveViewport()) {
            return false;
        }
        if (appWin.__scoopResponsiveSidebarUserToggled) {
            return false;
        }
        if (__scoopIsAnalyzePage()) {
            return !appWin.__scoopAnalyzeSidebarUserOpened;
        }
        return isAnalyzeReturnSuppressed();
    };

    const DESKTOP_INLINE_PROPS = {
        view: ["display", "flex-direction", "position", "width", "max-width", "margin-left", "padding-left"],
        sidebar: [
            "flex", "position", "transform", "translate", "transition", "visibility", "opacity",
            "overflow", "z-index", "height", "max-height", "min-height", "min-width", "width",
            "max-width", "left", "top", "box-shadow", "pointer-events", "align-self",
        ],
        inner: ["overflow-x", "overflow-y", "height", "max-height", "width", "max-width"],
        mainWrap: ["flex", "min-width", "width", "max-width"],
        mainSection: ["width", "max-width"],
    };

    const clearInlineProps = (node, props) => {
        if (!node) {
            return;
        }
        props.forEach((prop) => node.style.removeProperty(prop));
    };

    const clearDesktopInlineLayout = () => {
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        clearInlineProps(view, DESKTOP_INLINE_PROPS.view);
        clearInlineProps(sidebar, DESKTOP_INLINE_PROPS.sidebar);
        const inner =
            sidebar?.querySelector('[data-testid="stSidebarContent"]') ||
            sidebar?.firstElementChild;
        clearInlineProps(inner, DESKTOP_INLINE_PROPS.inner);
        const mainWrap = view?.querySelector(':scope > div:not([data-testid="stSidebar"])');
        clearInlineProps(mainWrap, DESKTOP_INLINE_PROPS.mainWrap);
        clearInlineProps(view?.querySelector("section.main"), DESKTOP_INLINE_PROPS.mainSection);
    };

    const isTabNavMode = () => doc.documentElement.getAttribute("data-scoop-tab-nav") === "1";

    const applyResponsiveSidebarLayout = () => {
        if (!isResponsiveViewport()) {
            return;
        }
        if (isTabNavMode()) {
            clearDesktopInlineLayout();
            const view = doc.querySelector('[data-testid="stAppViewContainer"]');
            if (view) {
                view.style.setProperty("display", "block", "important");
                view.style.setProperty("width", "100%", "important");
                view.style.setProperty("max-width", "100vw", "important");
                view.style.setProperty("margin-left", "0", "important");
                view.style.setProperty("padding-left", "0", "important");
            }
            return;
        }
        clearDesktopInlineLayout();
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!view || !sidebar) {
            return;
        }

        view.style.setProperty("display", "block", "important");
        view.style.setProperty("width", "100%", "important");
        view.style.setProperty("max-width", "100vw", "important");
        view.style.setProperty("margin-left", "0", "important");
        view.style.setProperty("padding-left", "0", "important");

        if (shouldKeepResponsiveSidebarCollapsed()) {
            __scoopApplySidebarExpandedState(false);
        }
        const expanded = shouldKeepResponsiveSidebarCollapsed()
            ? false
            : sidebar.getAttribute("aria-expanded") === "true";
        sidebar.style.setProperty("position", "fixed", "important");
        sidebar.style.setProperty("top", "0", "important");
        sidebar.style.setProperty("left", "0", "important");
        sidebar.style.setProperty("height", "100dvh", "important");
        sidebar.style.setProperty("min-height", "100dvh", "important");
        sidebar.style.setProperty("z-index", "1000010", "important");
        sidebar.style.setProperty("width", "min(92vw, 36rem)", "important");
        sidebar.style.setProperty("max-width", "min(92vw, 36rem)", "important");
        sidebar.style.setProperty(
            "transition",
            "transform 0.28s ease, visibility 0.28s ease",
            "important"
        );
        sidebar.style.setProperty(
            "transform",
            expanded ? "translateX(0)" : "translateX(-100vw)",
            "important"
        );
        sidebar.style.setProperty("visibility", expanded ? "visible" : "hidden", "important");
        sidebar.style.setProperty("pointer-events", expanded ? "auto" : "none", "important");

        const mainSection = view.querySelector("section.main");
        if (mainSection) {
            mainSection.style.setProperty("width", "100%", "important");
            mainSection.style.setProperty("max-width", "100vw", "important");
        }
        const mainWrap = view.querySelector(':scope > div:not([data-testid="stSidebar"])');
        if (mainWrap) {
            mainWrap.style.setProperty("width", "100%", "important");
            mainWrap.style.setProperty("max-width", "100vw", "important");
        }
    };

    const applyDesktopSidebarLayout = () => {
        if (!isDesktopViewport()) {
            return;
        }
        clearDesktopInlineLayout();
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!view || !sidebar) {
            return;
        }
        view.style.setProperty("display", "flex", "important");
        view.style.setProperty("flex-direction", "row", "important");
        view.style.setProperty("position", "relative", "important");
        view.style.setProperty("width", "100%", "important");
        view.style.setProperty("max-width", "100vw", "important");
        view.style.setProperty("margin-left", "0", "important");
        view.style.setProperty("padding-left", "0", "important");
        sidebar.style.setProperty("flex", "0 1 auto", "important");
        sidebar.style.setProperty("position", "relative", "important");
        sidebar.style.setProperty("transform", "none", "important");
        sidebar.style.setProperty("visibility", "visible", "important");
        sidebar.style.setProperty("overflow", "visible", "important");
        sidebar.style.setProperty("z-index", "2", "important");
        sidebar.style.setProperty("min-width", "min(10rem, 28vw)", "important");
        sidebar.style.setProperty("width", "var(--scoop-desktop-sidebar-width, clamp(10rem, min(20vw, 28rem), 36rem))", "important");
        sidebar.style.setProperty("max-width", "min(32vw, 36rem)", "important");
        sidebar.style.setProperty("height", "100vh", "important");
        sidebar.style.setProperty("max-height", "100vh", "important");
        const inner =
            sidebar.querySelector('[data-testid="stSidebarContent"]') ||
            sidebar.firstElementChild;
        if (inner) {
            inner.style.setProperty("overflow-x", "visible", "important");
            inner.style.setProperty("overflow-y", "auto", "important");
            inner.style.setProperty("min-width", "0", "important");
            inner.style.setProperty("height", "100vh", "important");
            inner.style.setProperty("max-height", "100vh", "important");
        }
        const mainWrap = view.querySelector(':scope > div:not([data-testid="stSidebar"])');
        if (mainWrap) {
            mainWrap.style.setProperty("flex", "1 1 0", "important");
            mainWrap.style.setProperty("min-width", "0", "important");
            mainWrap.style.setProperty("max-width", "100%", "important");
            mainWrap.style.setProperty("overflow-x", "auto", "important");
        }
        const mainSection = view.querySelector("section.main");
        if (mainSection) {
            mainSection.style.setProperty("min-width", "0", "important");
            mainSection.style.setProperty("max-width", "100%", "important");
            mainSection.style.setProperty("overflow-x", "auto", "important");
        }
    };

    const syncMainBlockHeaderPadding = () => {
        const header = doc.querySelector('[data-testid="stHeader"]');
        const targets = doc.querySelectorAll(
            '[data-testid="stMainBlockContainer"], section.main > div, [data-testid="stAppViewContainer"] > section.main'
        );
        if (!targets.length) {
            return;
        }
        const analyzeActive =
            __scoopIsAnalyzePage() &&
            /(?:\\?|&)ticker=/i.test(appWin.location.search || "");
        const screenerActive = __scoopIsScreenerPage();
        const termsActive = /Terms_of_Service/i.test(appWin.location.pathname || "");
        const isHomeLanding = () => {
            const path = (appWin.location.pathname || "").replace(/\/+$/, "") || "/";
            return path === "" || path === "/" || /\\/app$/i.test(path);
        };
        if (isTabNavMode()) {
            const homePad = isHomeLanding() ? "0px" : "4px";
            targets.forEach((el) => {
                el.style.setProperty("padding-top", homePad, "important");
            });
            return;
        }
        if (isDesktopViewport() && (analyzeActive || screenerActive || termsActive)) {
            if (analyzeActive) {
                doc.documentElement.setAttribute("data-scoop-analyze-active", "1");
            }
            const padTop = (termsActive || analyzeActive) ? "0px" : "12px";
            targets.forEach((el) => {
                el.style.setProperty("padding-top", padTop, "important");
            });
            return;
        }
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const padTop = Math.max(12, Math.round(headerBottom + 12));
        targets.forEach((el) => {
            el.style.setProperty("padding-top", `${padTop}px`, "important");
        });
    };

    const injectDesktopLayoutFixCss = () => {
        if (!isDesktopViewport()) {
            return;
        }
        const id = "scoop-desktop-nav-fix-css";
        let el = doc.getElementById(id);
        if (!el) {
            el = doc.createElement("style");
            el.id = id;
            (doc.body || doc.documentElement).appendChild(el);
        }
        el.textContent = `
@media (min-width: 1367px) {
  [data-testid="stAppViewContainer"] {
    display: flex !important;
    flex-direction: row !important;
    width: 100% !important;
    max-width: 100vw !important;
    min-width: 0 !important;
    margin-left: 0 !important;
    padding-left: 0 !important;
  }
  [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]) {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    width: auto !important;
    max-width: 100% !important;
  }
  section[data-testid="stSidebar"],
  section[data-testid="stSidebar"][aria-expanded="false"],
  section[data-testid="stSidebar"][aria-expanded="true"] {
    position: relative !important;
    transform: none !important;
    visibility: visible !important;
    pointer-events: auto !important;
    flex: 0 1 auto !important;
  }
  [data-testid="stMainBlockContainer"],
  section.main > div,
  [data-testid="stAppViewContainer"] > section.main {
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
}`;
    };

    const syncSidebarLayout = () => {
        // Tablet/phone Terms: stay in main-view tab-nav chrome (never flip to desktop split).
        if (__scoopIsTermsPage() && __scoopShouldHoldTermsMainView()) {
            setDesktopLayoutFlag(false);
            const fixElTerms = doc.getElementById("scoop-desktop-nav-fix-css");
            if (fixElTerms) {
                fixElTerms.remove();
            }
            doc.documentElement.setAttribute("data-scoop-tab-nav", "1");
            clearDesktopInlineLayout();
            applyResponsiveSidebarLayout();
            syncMainBlockHeaderPadding();
            return;
        }
        if (isDesktopViewport()) {
            doc.documentElement.removeAttribute("data-scoop-tab-nav");
            setDesktopLayoutFlag(true);
            applyDesktopSidebarLayout();
            injectDesktopLayoutFixCss();
            syncMainBlockHeaderPadding();
            return;
        }
        setDesktopLayoutFlag(false);
        const fixEl = doc.getElementById("scoop-desktop-nav-fix-css");
        if (fixEl) {
            fixEl.remove();
        }
        if (isResponsiveViewport()) {
            doc.documentElement.setAttribute("data-scoop-tab-nav", "1");
            applyResponsiveSidebarLayout();
            syncMainBlockHeaderPadding();
            return;
        }
        doc.documentElement.removeAttribute("data-scoop-tab-nav");
        clearDesktopInlineLayout();
        syncMainBlockHeaderPadding();
    };

    if (appWin.__scoopLayout) {
        appWin.__scoopLayout.syncSidebarLayout = syncSidebarLayout;
        appWin.__scoopLayout.applyResponsiveSidebarLayout = applyResponsiveSidebarLayout;
        appWin.__scoopLayout.applyDesktopSidebarLayout = applyDesktopSidebarLayout;
        return;
    }

    appWin.__scoopLayout = {
        isResponsiveViewport,
        isDesktopViewport,
        isAnalyzePage: __scoopIsAnalyzePage,
        isAnalyzeReturnSuppressed,
        shouldKeepResponsiveSidebarCollapsed,
        applyResponsiveSidebarLayout,
        applyDesktopSidebarLayout,
        clearDesktopInlineLayout,
        syncSidebarLayout,
    };
})();
"""
)

_PAGE_NAV_LAYOUT_RESYNC_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;
    const isTabNavMode = () => doc.documentElement.getAttribute("data-scoop-tab-nav") === "1";

    const resetScroll = () => {
        const scrollEl =
            doc.querySelector('[data-testid="stAppViewContainer"]') ||
            doc.scrollingElement ||
            doc.documentElement;
        if (scrollEl) {
            scrollEl.scrollTop = 0;
        }
        try {
            appWin.scrollTo(0, 0);
        } catch (e) {}
    };

    const syncMarketNavActive = () => {
        const isDesktop = layout()?.isDesktopViewport?.();
        const isResponsive = layout()?.isResponsiveViewport?.();
        if (!isDesktop && !isResponsive) {
            return;
        }
        const navSelector = isDesktop
            ? '[data-testid="stSidebar"] [data-testid="stPageLink"] a[href$="_Top_10"]'
            : isTabNavMode()
            ? '.scoop-mobile-tab-row [data-testid="stPageLink"] a'
            : '[data-testid="stSidebar"] [data-testid="stPageLink"] a';
        const normalize = (value) => (value || "").replace(/^\\/+|\\/+$/g, "").toLowerCase();
        const current = normalize(location.pathname);
        const isHomePath = !current || current === "app" || current.endsWith("/app");
        const markActive = (selector) => {
            doc.querySelectorAll(selector).forEach((a) => {
                const box = a.closest('[data-testid="stPageLink"]');
                if (!box) {
                    return;
                }
                const href = normalize(a.getAttribute("href") || "");
                const active = Boolean(href) && (
                    current === href ||
                    current.endsWith("/" + href) ||
                    (isHomePath && (href === "app" || href.endsWith("/app")))
                );
                if (active) {
                    box.setAttribute("data-scoop-nav-active", "");
                } else {
                    box.removeAttribute("data-scoop-nav-active");
                }
            });
        };
        markActive(navSelector);
        if (doc.documentElement.getAttribute("data-scoop-home-page") === "1") {
            markActive('.scoop-home-market-grid [data-testid="stPageLink"] a');
        }
    };

    const syncAnalyzePageFlag = () => {
        const root = doc.documentElement;
        const active =
            __scoopIsAnalyzePage() &&
            /(?:\\?|&)ticker=/i.test(appWin.location.search || "");
        if (active) {
            root.setAttribute("data-scoop-analyze-active", "1");
            let fromPath = "";
            try {
                fromPath = new URLSearchParams(appWin.location.search || "").get("from") || "";
            } catch (e) {}
            if (!fromPath) {
                try {
                    fromPath = (appWin.sessionStorage && appWin.sessionStorage.getItem("scoop-analyze-from")) || "";
                } catch (e2) {}
            }
            const upper = String(fromPath).toUpperCase();
            let source = "";
            if (upper.indexOf("CRYPTO") >= 0) source = "CRYPTO";
            else if (upper.indexOf("NASDAQ") >= 0) source = "NASDAQ";
            else if (upper.indexOf("NYSE") >= 0) source = "NYSE";
            else if (upper.indexOf("CME") >= 0) source = "CME";
            else if (upper.indexOf("ICE") >= 0) source = "ICE";
            if (!source) {
                try {
                    const ticker = new URLSearchParams(appWin.location.search || "").get("ticker") || "";
                    if (/-USD$/i.test(ticker)) source = "CRYPTO";
                } catch (e3) {}
            }
            if (source) {
                root.setAttribute("data-scoop-analyze-source", source);
            }
        } else {
            root.removeAttribute("data-scoop-analyze-active");
            root.removeAttribute("data-scoop-analyze-source");
        }
    };

    const syncScreenerPageFlag = () => {
        const root = doc.documentElement;
        if (__scoopIsScreenerPage()) {
            root.setAttribute("data-scoop-screener-active", "1");
        } else {
            root.removeAttribute("data-scoop-screener-active");
        }
    };

    const syncTermsPageFlag = () => {
        const root = doc.documentElement;
        if (/Terms_of_Service/i.test(appWin.location.pathname || "")) {
            root.setAttribute("data-scoop-terms-active", "1");
        } else {
            root.removeAttribute("data-scoop-terms-active");
        }
    };

    const resync = () => {
        syncAnalyzePageFlag();
        syncScreenerPageFlag();
        syncTermsPageFlag();
        holdMobileTermsMainView();
        layout()?.syncSidebarLayout?.();
        syncMarketNavActive();
        resetScroll();
    };

    const TERMS_NAV_COLLAPSE_KEY = "scoop-terms-nav-collapse";
    const TERMS_NAV_SUPPRESS_MS = 15000;
    const PAGE_NAV_BIND_VERSION = 13;

    const enforceMobileTermsMainView = () => {
        if (!__scoopShouldHoldTermsMainView()) {
            return;
        }
        doc.documentElement.removeAttribute("data-scoop-screener-gated");
        doc.documentElement.removeAttribute("data-scoop-desktop-layout");
        if (__scoopIsTabletOnlyViewport() || __scoopIsPhoneViewport()) {
            doc.documentElement.setAttribute("data-scoop-tab-nav", "1");
        }
        layout()?.clearDesktopInlineLayout?.();
        __scoopApplySidebarExpandedState(false);
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (view) {
            view.style.setProperty("display", "block", "important");
            view.style.setProperty("width", "100%", "important");
            view.style.setProperty("max-width", "100vw", "important");
        }
    };

    const markMobileTermsNav = () => {
        if (!__scoopShouldHoldTermsMainView()) {
            return;
        }
        try {
            appWin.sessionStorage.setItem(TERMS_NAV_COLLAPSE_KEY, "1");
            appWin.sessionStorage.setItem("scoop-responsive-sidebar-ready", "1");
            appWin.sessionStorage.setItem("scoop-terms-force-responsive", "1");
        } catch (e) {}
        appWin.__scoopSuppressSidebarExpand = Date.now() + TERMS_NAV_SUPPRESS_MS;
        if (typeof appWin.__scoopClearResponsiveExpandTimers === "function") {
            appWin.__scoopClearResponsiveExpandTimers();
        }
        enforceMobileTermsMainView();
    };

    const holdMobileTermsMainView = () => {
        if (!__scoopShouldHoldTermsMainView()) {
            return;
        }
        const hold =
            __scoopIsTermsPage() ||
            (() => {
                try {
                    return appWin.sessionStorage.getItem(TERMS_NAV_COLLAPSE_KEY) === "1";
                } catch (e) {
                    return false;
                }
            })();
        if (!hold) {
            return;
        }
        try {
            appWin.sessionStorage.removeItem(TERMS_NAV_COLLAPSE_KEY);
        } catch (e) {}
        appWin.__scoopSuppressSidebarExpand = Date.now() + TERMS_NAV_SUPPRESS_MS;
        enforceMobileTermsMainView();
    };

    const resolveGatingTermsLink = (node, event) => {
        if (!node || typeof node.closest !== "function") {
            return null;
        }
        // Only the Terms <a> itself — never the consent checkbox chrome.
        return node.closest('a[href*="Terms_of_Service"]');
    };

    const handleMobileTermsNavPointer = (event) => {
        const target = event.target;
        const el =
            target && target.nodeType === 1 ? target : target && target.parentElement;
        if (!el || typeof el.closest !== "function") {
            return;
        }
        // Analyze "Back to <market>" uses href*="Top_10" — let its own onclick
        // mark return flags; do not hijack that navigation.
        if (el.closest("a.scoop-analyze-back")) {
            return;
        }
        if (
            el.closest('[data-testid="stCheckbox"]') &&
            !el.closest('a[href*="Terms_of_Service"]')
        ) {
            return;
        }
        const gatingTerms = resolveGatingTermsLink(el, event);
        const link = gatingTerms || el.closest(
            '[data-testid="stPageLink"] a, [data-testid="stSidebarNav"] a, a[href*="Top_10"], a[href*="Terms_of_Service"]'
        );
        if (!link || link.classList?.contains("scoop-analyze-back")) {
            return;
        }
        const termsHref = `${link.getAttribute("href") || ""} ${link.href || ""}`;
        if (/Terms_of_Service/i.test(termsHref)) {
            // Mobile/tablet: the link lives inside the consent <label>. Streamlit
            // consumes touch on pointerdown and often never fires click. Navigate
            // on pointerdown (and click as fallback), once per gesture.
            if (event.type === "touchstart") {
                return;
            }
            if (__scoopShouldHoldTermsMainView()) {
                event.preventDefault();
                event.stopPropagation();
                if (typeof event.stopImmediatePropagation === "function") {
                    event.stopImmediatePropagation();
                }
                if (appWin.__scoopTermsNavLock && Date.now() < appWin.__scoopTermsNavLock) {
                    return;
                }
                appWin.__scoopTermsNavLock = Date.now() + 1500;
                link.setAttribute("target", "_self");
                markMobileTermsNav();
                __scoopNavigateMobileTerms(link, appWin);
            }
            return;
        }
        if (__scoopIsPhoneViewport()) {
            event.preventDefault();
            event.stopPropagation();
            __scoopApplySidebarExpandedState(false);
            appWin.location.assign(__scoopResolveTermsUrl(link, appWin));
            return;
        }
        if (__scoopIsTabletViewport()) {
            event.preventDefault();
            event.stopPropagation();
            __scoopApplySidebarExpandedState(false);
            appWin.location.assign(__scoopResolveTermsUrl(link, appWin));
            return;
        }
        __scoopApplySidebarExpandedState(false);
    };

    if (appWin.__scoopPageNavBindVersion !== PAGE_NAV_BIND_VERSION) {
        if (appWin.__scoopPageNavClickHandler) {
            doc.removeEventListener("click", appWin.__scoopPageNavClickHandler, true);
            doc.removeEventListener("touchstart", appWin.__scoopPageNavClickHandler, true);
            doc.removeEventListener("pointerdown", appWin.__scoopPageNavClickHandler, true);
        }
        appWin.__scoopPageNavClickHandler = handleMobileTermsNavPointer;
        doc.addEventListener("click", appWin.__scoopPageNavClickHandler, true);
        doc.addEventListener("touchstart", appWin.__scoopPageNavClickHandler, { passive: true, capture: true });
        doc.addEventListener("pointerdown", appWin.__scoopPageNavClickHandler, true);
        appWin.__scoopPageNavBindVersion = PAGE_NAV_BIND_VERSION;
    }

    resync();
    appWin.requestAnimationFrame(() => {
        resync();
        appWin.requestAnimationFrame(resync);
    });
    [120, 350, 800, 1500, 2500].forEach((delay) => {
        appWin.setTimeout(resync, delay);
    });

    const bindMainObserver = () => {
        const main = doc.querySelector('[data-testid="stMainBlockContainer"]');
        if (!main) {
            return false;
        }
        if (appWin.__scoopMainLayoutObserver) {
            appWin.__scoopMainLayoutObserver.disconnect();
        }
        appWin.__scoopMainLayoutObserver = new MutationObserver(() => {
            appWin.requestAnimationFrame(resync);
        });
        appWin.__scoopMainLayoutObserver.observe(main, {
            childList: true,
            subtree: true,
        });
        return true;
    };
    if (!bindMainObserver()) {
        let attempts = 0;
        const retry = appWin.setInterval(() => {
            attempts += 1;
            if (bindMainObserver() || attempts >= 16) {
                appWin.clearInterval(retry);
            }
        }, 200);
    }

})();
"""
)

_RESPONSIVE_LAYOUT_SYNC_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const sync = () => appWin.__scoopLayout?.syncSidebarLayout();
    let syncTimer = null;
    const schedule = () => {
        if (syncTimer) {
            return;
        }
        syncTimer = appWin.setTimeout(() => {
            syncTimer = null;
            sync();
        }, 80);
    };
    schedule();
    if (appWin.__scoopLayoutSyncBound) {
        return;
    }
    appWin.__scoopLayoutSyncBound = true;
    if (doc.readyState === "loading") {
        doc.addEventListener("DOMContentLoaded", schedule, { once: true });
    }
    if (!appWin.__scoopLayoutResizeBound) {
        appWin.__scoopLayoutResizeBound = true;
        appWin.addEventListener("resize", schedule);
        if (appWin.visualViewport) {
            appWin.visualViewport.addEventListener("resize", schedule);
        }
    }
    const bindSidebarObserver = () => {
        if (appWin.__scoopLayoutObserver) {
            return true;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) {
            return false;
        }
        appWin.__scoopLayoutObserver = new MutationObserver(schedule);
        appWin.__scoopLayoutObserver.observe(sidebar, {
            attributes: true,
            attributeFilter: ["aria-expanded", "class"],
        });
        return true;
    };
    if (!bindSidebarObserver()) {
        let attempts = 0;
        const retry = appWin.setInterval(() => {
            attempts += 1;
            if (bindSidebarObserver() || attempts >= 12) {
                appWin.clearInterval(retry);
            }
        }, 250);
    }
})();
"""
)

_ANALYZE_RETURN_NAV_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const RETURN_KEY = "scoop-return-from-analyze";
    const SUPPRESS_MS = 10000;

    const markAnalyzeReturn = () => {
        try {
            appWin.sessionStorage.setItem(RETURN_KEY, "1");
            appWin.sessionStorage.setItem("scoop-mobile-home-seen", "1");
            appWin.sessionStorage.setItem("scoop-landing-seen", "1");
            appWin.__scoopSuppressSidebarExpand = Date.now() + SUPPRESS_MS;
            if (typeof appWin.__scoopClearResponsiveExpandTimers === "function") {
                appWin.__scoopClearResponsiveExpandTimers();
            }
        } catch (e) {}
    };

    const shouldForceScreenerMainView = () => {
        if (__scoopIsAnalyzePage()) {
            return false;
        }
        const layout = appWin.__scoopLayout;
        if (!layout?.isResponsiveViewport?.()) {
            return false;
        }
        try {
            if (appWin.sessionStorage.getItem(RETURN_KEY) === "1") {
                return true;
            }
        } catch (e) {}
        return !!(appWin.__scoopSuppressSidebarExpand && Date.now() < appWin.__scoopSuppressSidebarExpand);
    };

    const forceScreenerMainView = () => {
        if (!shouldForceScreenerMainView()) {
            return;
        }
        if (doc.documentElement.getAttribute("data-scoop-tab-nav") === "1") {
            try {
                if (appWin.sessionStorage.getItem(RETURN_KEY) === "1") {
                    appWin.sessionStorage.removeItem(RETURN_KEY);
                }
            } catch (e) {}
            return;
        }
        try {
            if (appWin.sessionStorage.getItem(RETURN_KEY) === "1") {
                appWin.sessionStorage.removeItem(RETURN_KEY);
            }
        } catch (e) {}
        appWin.__scoopSuppressSidebarExpand = Date.now() + SUPPRESS_MS;
        __scoopApplySidebarExpandedState(false);
    };

    if (!appWin.__scoopAnalyzeReturnNavBound) {
        appWin.__scoopAnalyzeReturnNavBound = true;
        doc.addEventListener(
            "click",
            (event) => {
                if (event.target.closest("a.scoop-analyze-back")) {
                    markAnalyzeReturn();
                }
            },
            true
        );
    }
})();
"""
)

_RESPONSIVE_SIDEBAR_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;
    const isResponsiveViewport = () => layout()?.isResponsiveViewport() ?? false;
    const isAnalyzeReturnSuppressed = () => layout()?.isAnalyzeReturnSuppressed?.() ?? false;
    const isTabNavMode = () => doc.documentElement.getAttribute("data-scoop-tab-nav") === "1";

    const collapseSidebar = () => {
        if (isResponsiveViewport()) {
            appWin.__scoopResponsiveSidebarUserToggled = true;
            appWin.__scoopSuppressSidebarExpand = 0;
        }
        __scoopApplySidebarExpandedState(false);
        return true;
    };

    const expandSidebar = () => {
        if (
            isAnalyzeReturnSuppressed() &&
            !appWin.__scoopResponsiveSidebarUserToggled
        ) {
            return false;
        }
        if (__scoopIsAnalyzePage() && isResponsiveViewport() && !appWin.__scoopAnalyzeSidebarUserOpened) {
            return false;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") === "true") {
            return sidebar?.getAttribute("aria-expanded") === "true";
        }
        __scoopApplySidebarExpandedState(true);
        return (
            doc.querySelector('section[data-testid="stSidebar"]')?.getAttribute("aria-expanded") ===
            "true"
        );
    };

    const removeLegacyCloseButton = () => {
        doc.getElementById("scoop-responsive-sidebar-close")?.remove();
        doc.querySelectorAll(".scoop-responsive-sidebar-close").forEach((node) => {
            if (node.id !== "scoop-responsive-sidebar-close") {
                return;
            }
            node.remove();
        });
    };

    const shouldCloseSidebar = (event) => {
        if (!isResponsiveViewport()) {
            return false;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "true") {
            return false;
        }
        if (event.target.closest('[data-testid="stSidebarBackdrop"]')) {
            return true;
        }
        if (event.target.closest('section[data-testid="stSidebar"]')) {
            return false;
        }
        if (event.target.closest('[data-testid="stHeader"]')) {
            return false;
        }
        return event.target.closest('[data-testid="stAppViewContainer"]') != null;
    };

    let tabletBootstrapped = false;
    const ANALYZE_RETURN_KEY = "scoop-return-from-analyze";
    const POST_CONSENT_KEY = "scoop-post-consent-collapse";
    const SIDEBAR_BOOTSTRAP_KEY = "scoop-responsive-sidebar-ready";
    const TERMS_NAV_COLLAPSE_KEY = "scoop-terms-nav-collapse";
    const TERMS_NAV_SUPPRESS_MS = 15000;

    const markSidebarBootstrapped = () => {
        tabletBootstrapped = true;
        try {
            appWin.sessionStorage.setItem(SIDEBAR_BOOTSTRAP_KEY, "1");
        } catch (e) {}
    };

    try {
        tabletBootstrapped = appWin.sessionStorage.getItem(SIDEBAR_BOOTSTRAP_KEY) === "1";
    } catch (e) {}

    const isReturningFromAnalyze = () => {
        try {
            return appWin.sessionStorage.getItem(ANALYZE_RETURN_KEY) === "1";
        } catch (e) {
            return false;
        }
    };

    const clearReturningFromAnalyze = () => {
        try {
            appWin.sessionStorage.removeItem(ANALYZE_RETURN_KEY);
        } catch (e) {}
    };

    const isPostConsentCollapse = () => {
        if (!isResponsiveViewport()) {
            return false;
        }
        try {
            return appWin.sessionStorage.getItem(POST_CONSENT_KEY) === "1";
        } catch (e) {
            return false;
        }
    };

    const clearPostConsentCollapse = () => {
        try {
            appWin.sessionStorage.removeItem(POST_CONSENT_KEY);
        } catch (e) {}
    };

    const holdScreenerMainView = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        const suppressed =
            isAnalyzeReturnSuppressed() ||
            isReturningFromAnalyze();
        if (!suppressed) {
            return false;
        }
        if (isReturningFromAnalyze()) {
            clearReturningFromAnalyze();
        }
        appWin.__scoopSuppressSidebarExpand = Date.now() + 10000;
        markSidebarBootstrapped();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
            __scoopApplySidebarExpandedState(false);
        }
        layout()?.syncSidebarLayout?.();
        removeLegacyCloseButton();
        return true;
    };

    const holdMainViewAfterConsent = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        if (!isPostConsentCollapse()) {
            return false;
        }
        clearPostConsentCollapse();
        appWin.__scoopSuppressSidebarExpand = Date.now() + 12000;
        markSidebarBootstrapped();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
            __scoopApplySidebarExpandedState(false);
        }
        layout()?.syncSidebarLayout?.();
        removeLegacyCloseButton();
        return true;
    };

    const shouldHoldMobileTermsMainView = () => {
        if (!__scoopShouldHoldTermsMainView()) {
            return false;
        }
        if (__scoopIsTermsPage()) {
            return true;
        }
        try {
            return appWin.sessionStorage.getItem(TERMS_NAV_COLLAPSE_KEY) === "1";
        } catch (e) {
            return false;
        }
    };

    const holdMainViewForMobileTerms = () => {
        if (!shouldHoldMobileTermsMainView()) {
            return false;
        }
        try {
            appWin.sessionStorage.removeItem(TERMS_NAV_COLLAPSE_KEY);
        } catch (e) {}
        appWin.__scoopSuppressSidebarExpand = Date.now() + TERMS_NAV_SUPPRESS_MS;
        markSidebarBootstrapped();
        doc.documentElement.removeAttribute("data-scoop-screener-gated");
        doc.documentElement.removeAttribute("data-scoop-desktop-layout");
        doc.documentElement.setAttribute("data-scoop-tab-nav", "1");
        layout()?.clearDesktopInlineLayout?.();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
            __scoopApplySidebarExpandedState(false);
        }
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (view) {
            view.style.setProperty("display", "block", "important");
            view.style.setProperty("width", "100%", "important");
            view.style.setProperty("max-width", "100vw", "important");
            view.style.setProperty("flex-direction", "column", "important");
            view.style.setProperty("margin-left", "0", "important");
            view.style.setProperty("padding-left", "0", "important");
        }
        // Keep tablet/phone Terms in tab-nav main view; do not re-run desktop sync here.
        removeLegacyCloseButton();
        return true;
    };

    const scheduleCollapseAfterMobileTermsNav = () => {
        if (appWin.__scoopMobileTermsNavCollapseTimers) {
            appWin.__scoopMobileTermsNavCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
        }
        appWin.__scoopMobileTermsNavCollapseTimers = [];
        const run = () => holdMainViewForMobileTerms();
        run();
        appWin.requestAnimationFrame(run);
        [150, 500, 1200, 2500].forEach((delay) => {
            const timerId = appWin.setTimeout(run, delay);
            appWin.__scoopMobileTermsNavCollapseTimers.push(timerId);
        });
    };

    const ensureScreenerContentVisible = () => {
        holdScreenerMainView();
    };

    const scheduleCollapseAfterAnalyzeReturn = () => {
        if (appWin.__scoopAnalyzeReturnCollapseTimers) {
            appWin.__scoopAnalyzeReturnCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
        }
        appWin.__scoopAnalyzeReturnCollapseTimers = [];
        const run = () => holdScreenerMainView();
        run();
        appWin.requestAnimationFrame(run);
        [150, 500, 1200].forEach((delay) => {
            const timerId = appWin.setTimeout(run, delay);
            appWin.__scoopAnalyzeReturnCollapseTimers.push(timerId);
        });
    };

    const scheduleCollapseAfterConsent = () => {
        if (appWin.__scoopPostConsentCollapseTimers) {
            appWin.__scoopPostConsentCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
        }
        appWin.__scoopPostConsentCollapseTimers = [];
        const run = () => holdMainViewAfterConsent();
        run();
        appWin.requestAnimationFrame(run);
        [150, 500, 1200].forEach((delay) => {
            const timerId = appWin.setTimeout(run, delay);
            appWin.__scoopPostConsentCollapseTimers.push(timerId);
        });
    };

    appWin.__scoopResponsiveSidebarBound = appWin.__scoopResponsiveSidebarBound || false;
    removeLegacyCloseButton();

    if (!appWin.__scoopResponsiveSidebarBound) {
        appWin.__scoopResponsiveSidebarBound = true;

        if (appWin.__scoopLayout) {
            appWin.__scoopLayout.collapseSidebar = collapseSidebar;
            appWin.__scoopLayout.expandSidebar = expandSidebar;
        }

        doc.addEventListener(
            "click",
            (event) => {
                if (shouldCloseSidebar(event)) {
                    collapseSidebar();
                }
            },
            true
        );

        doc.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && isResponsiveViewport()) {
                collapseSidebar();
            }
        });

        doc.addEventListener(
            "click",
            (event) => {
                if (!isResponsiveViewport()) {
                    return;
                }
                const expandTarget = event.target.closest(
                    '[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"]'
                );
                const collapseTarget = event.target.closest(
                    '[data-testid="stSidebarCollapseButton"]'
                );
                if (!expandTarget && !collapseTarget) {
                    return;
                }
                event.preventDefault();
                event.stopPropagation();
            },
            true
        );
    }

    if (appWin.__scoopResponsiveSidebarInitDone) {
        if (__scoopIsAnalyzePage() && isResponsiveViewport()) {
            if (!appWin.__scoopAnalyzeSidebarUserOpened) {
                __scoopApplySidebarExpandedState(false);
            }
            layout()?.syncSidebarLayout();
            return;
        }
        if (isReturningFromAnalyze() || isAnalyzeReturnSuppressed()) {
            holdScreenerMainView();
        } else if (isPostConsentCollapse()) {
            holdMainViewAfterConsent();
        } else {
            layout()?.syncSidebarLayout();
        }
        return;
    }

    const ensureAnalyzeSidebarCollapsed = () => {
        if (!isResponsiveViewport() || !__scoopIsAnalyzePage()) {
            return;
        }
        if (appWin.__scoopAnalyzeSidebarUserOpened) {
            layout()?.syncSidebarLayout();
            return;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            collapseSidebar();
        }
        layout()?.syncSidebarLayout();
        removeLegacyCloseButton();
    };

    const scheduleAnalyzeSidebarCollapse = () => {
        if (!__scoopIsAnalyzePage() || !isResponsiveViewport()) {
            return;
        }
        appWin.__scoopAnalyzeSidebarUserOpened = false;
        ensureAnalyzeSidebarCollapsed();
        appWin.requestAnimationFrame(ensureAnalyzeSidebarCollapsed);
        [50, 150, 400, 900, 1600, 2500, 4000].forEach((delay) => {
            appWin.setTimeout(ensureAnalyzeSidebarCollapsed, delay);
        });
    };

    const ensureInitialResponsiveExpand = () => {
        if (!isResponsiveViewport()) {
            layout()?.syncSidebarLayout();
            return;
        }
        if (isTabNavMode()) {
            markSidebarBootstrapped();
            layout()?.syncSidebarLayout();
            return;
        }
        layout()?.syncSidebarLayout();
        if (__scoopIsAnalyzePage()) {
            markSidebarBootstrapped();
            scheduleAnalyzeSidebarCollapse();
            return;
        }
        if (
            isReturningFromAnalyze() ||
            isAnalyzeReturnSuppressed()
        ) {
            markSidebarBootstrapped();
            scheduleCollapseAfterAnalyzeReturn();
            return;
        }
        if (isPostConsentCollapse()) {
            markSidebarBootstrapped();
            scheduleCollapseAfterConsent();
            return;
        }
        if (shouldHoldMobileTermsMainView()) {
            markSidebarBootstrapped();
            scheduleCollapseAfterMobileTermsNav();
            return;
        }
        if (tabletBootstrapped) {
            layout()?.syncSidebarLayout();
            return;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) {
            return;
        }
        if (sidebar.getAttribute("aria-expanded") === "true") {
            markSidebarBootstrapped();
            layout()?.syncSidebarLayout();
            removeLegacyCloseButton();
            return;
        }
        if (expandSidebar()) {
            markSidebarBootstrapped();
            layout()?.syncSidebarLayout();
            removeLegacyCloseButton();
        }
    };

    ensureInitialResponsiveExpand();
    appWin.__scoopResponsiveSidebarInitDone = true;
    appWin.__scoopResponsiveExpandTimers = appWin.__scoopResponsiveExpandTimers || [];
    appWin.__scoopClearResponsiveExpandTimers = () => {
        (appWin.__scoopResponsiveExpandTimers || []).forEach((timerId) => {
            appWin.clearTimeout(timerId);
        });
        appWin.__scoopResponsiveExpandTimers = [];
        if (appWin.__scoopAnalyzeReturnCollapseTimers) {
            appWin.__scoopAnalyzeReturnCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
            appWin.__scoopAnalyzeReturnCollapseTimers = [];
        }
        if (appWin.__scoopPostConsentCollapseTimers) {
            appWin.__scoopPostConsentCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
            appWin.__scoopPostConsentCollapseTimers = [];
        }
        if (appWin.__scoopMobileTermsNavCollapseTimers) {
            appWin.__scoopMobileTermsNavCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
            appWin.__scoopMobileTermsNavCollapseTimers = [];
        }
    };
    if (
        !isAnalyzeReturnSuppressed() &&
        !isReturningFromAnalyze() &&
        !isPostConsentCollapse() &&
        !tabletBootstrapped
    ) {
        appWin.requestAnimationFrame(() => {
            ensureInitialResponsiveExpand();
            removeLegacyCloseButton();
        });
        const timerId = appWin.setTimeout(() => {
            ensureInitialResponsiveExpand();
            removeLegacyCloseButton();
        }, 400);
        appWin.__scoopResponsiveExpandTimers.push(timerId);
    }
})();
"""
)

_TOOLTIP_SCROLL_JS = """
(() => {
    const root = document.documentElement;
    const className = "scoop-tooltip-scrolling";
    const DESKTOP_MIN = 1367;
    const MOBILE_MAX = 743;
    const MOBILE_HEADLINES_BOTTOM_TAP_PAD = 80;
    const MOBILE_HEADLINES_CARD_WIDTH_INSET = 16;
    const RESPONSIVE_MIN = 769;
    const RESPONSIVE_MAX = 1366;
    const IPAD_MINI_MIN = 744;
    const IPAD_MINI_MAX = 768;
    const IPAD_MINI_HEADLINES_TOP = 90;
    const IPAD_MINI_HEADLINES_BOTTOM = 30;
    const IPAD_MINI_HEADLINES_MAX_WIDTH = 320;
    const VIEWPORT_PAD = 12;
    const GAP = 10;
    const HEADLINES_DESKTOP_OFFSET = 12;
    const DESKTOP_HEADLINES_MIN_WIDTH = 320;
    const DESKTOP_HEADLINES_WIDTH_TRIM = 70;
    const DESKTOP_HEADLINES_TOP = 100;
    const DESKTOP_HEADLINES_ANCHOR_GAP = 10;
    const DESKTOP_HEADLINES_ABOVE_HEADING = 30;
    // Phone tips: ≤743. iPad Mini (744–768) + tablet (769–1366) use beside-row tips.
    const MOBILE_GENERIC_TIP_MAX = 743;
    const TABLET_GENERIC_TIP_MIN = 744;
    const TABLET_GENERIC_TIP_MAX = 1366;
    const TABLET_GENERIC_TIP_OPEN_GRACE_MS = 450;
    const isMobileGenericTipViewport = () => window.innerWidth <= MOBILE_GENERIC_TIP_MAX;
    const isTabletGenericTipViewport = () => {
        const w = window.innerWidth;
        return w >= TABLET_GENERIC_TIP_MIN && w <= TABLET_GENERIC_TIP_MAX;
    };
    const isTapGenericTipViewport = () =>
        isMobileGenericTipViewport() || isTabletGenericTipViewport();
    const closeAllMobileGenericTips = () => {
        // Never clear Headlines wraps — they use scoop-mobile-tip-open only for generics.
        document.querySelectorAll(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open").forEach((wrap) => {
            wrap.classList.remove("scoop-mobile-tip-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) {
                return;
            }
            // Clear tablet/mobile inline placement so closed tips cannot stay painted on-screen.
            [
                "position",
                "left",
                "top",
                "right",
                "bottom",
                "transform",
                "width",
                "max-width",
                "min-width",
                "max-height",
                "overflow-y",
                "visibility",
                "opacity",
                "pointer-events",
                "display",
                "z-index",
                "--scoop-mobile-tip-top",
                "--scoop-mobile-tip-left",
                "--scoop-se-name-tip-top",
                "--scoop-tablet-tip-left",
                "--scoop-tablet-tip-top",
                "--scoop-tablet-tip-width",
            ].forEach((prop) => tip.style.removeProperty(prop));
        });
    };
    const clearTooltipScrollingHide = () => {
        root.classList.remove(className);
        document.body.classList.remove(className);
    };

    if (!window.__scoopDesktopHeadlinesHideTimers) {
        window.__scoopDesktopHeadlinesHideTimers = new WeakMap();
    }
    window.__scoopDesktopHeadlinesSyncing = false;

    const isResponsiveHeadlinesViewport = () =>
        window.innerWidth >= RESPONSIVE_MIN && window.innerWidth <= RESPONSIVE_MAX;

    const isIpadMiniViewport = () => {
        const w = window.innerWidth;
        return w >= IPAD_MINI_MIN && w <= IPAD_MINI_MAX;
    };

    const isIpadAirViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const near820 = (value) => value >= 816 && value <= 824;
        const near1180 = (value) => value >= 1176 && value <= 1184;
        return (
            (near820(w) && near1180(h)) ||
            (near1180(w) && near820(h))
        );
    };

    const isIpadMiniOrAirHeadlinesViewport = () =>
        isIpadMiniViewport() || isIpadAirViewport();

    const isSurfaceDuoViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        return (
            w === 540 ||
            (w === 720 && h <= 541) ||
            (w >= 1110 && w <= 1118 && h <= 741)
        );
    };

    const isAsusZenbookFoldViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const near853 = (value) => value >= 849 && value <= 857;
        const near1280 = (value) => value >= 1276 && value <= 1284;
        const near1707 = (value) => value >= 1700 && value <= 1714;
        const near1920 = (value) => value >= 1910 && value <= 1930;
        const near1280u = (value) => value >= 1270 && value <= 1290;
        return (
            (near853(w) && near1280(h)) ||
            (near1280(w) && near853(h)) ||
            (near1707(w) && h >= 1000 && h <= 1120) ||
            (near1920(w) && near1280u(h)) ||
            (near1280u(w) && near1920(h))
        );
    };

    const isDesktopLayoutViewport = () =>
        window.innerWidth >= DESKTOP_MIN && !isAsusZenbookFoldViewport();

    const usesTabletProHeadlinesPopup = () =>
        isResponsiveHeadlinesViewport() ||
        isIpadMiniViewport() ||
        isSurfaceDuoViewport() ||
        isAsusZenbookFoldViewport();

    const isPhoneMobileHeadlinesViewport = () =>
        window.innerWidth <= MOBILE_MAX && !usesTabletProHeadlinesPopup();

    const isPhoneMobileHeadlinesOpen = () =>
        isPhoneMobileHeadlinesViewport() &&
        !!document.querySelector(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked");

    const isTabletProHeadlinesOpen = () =>
        usesTabletProHeadlinesPopup() &&
        !!document.querySelector(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked");

    const isInsideDesktopHeadlinesPopup = (node) => {
        if (!isDesktopLayoutViewport() || !node || !node.closest) {
            return false;
        }
        return !!node.closest(
            ".full-results-wrap .tip-wrap.headlines-tip .tip-text, .full-results-wrap .tip-wrap.headlines-tip .headlines-tip-scroll"
        );
    };

    const isDesktopHeadlinesSessionOpen = () =>
        isDesktopLayoutViewport() &&
        !!document.querySelector(
            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
        );

    const lockDesktopHeadlinesPageScroll = () => {};
    const unlockDesktopHeadlinesPageScroll = () => {};

    const getDesktopHeadlinesScrollContainer = (wrap) => {
        if (!wrap) {
            return null;
        }
        return wrap.querySelector(":scope > .tip-text > .headlines-tip-scroll");
    };

    const isDesktopHeadlinesOpenWrap = (wrap) => {
        if (!wrap) {
            return false;
        }
        return (
            wrap.classList.contains("hl-tip-desktop-open") ||
            !!wrap.querySelector(":scope > .hl-tip-cb:checked")
        );
    };

    const getDesktopHeadlinesTipBorderY = (tip) => {
        const tipStyles = getComputedStyle(tip);
        return (
            (parseFloat(tipStyles.borderTopWidth) || 0) +
            (parseFloat(tipStyles.borderBottomWidth) || 0)
        );
    };

    const applyDesktopHeadlinesScrollStyles = (wrap, slot) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const heading = tip?.querySelector(".hl-tip-heading");
        if (!tip || !scroll) {
            return;
        }

        const tipHeight =
            parseFloat(tip.style.getPropertyValue("--hl-fixed-height")) ||
            tip.clientHeight ||
            (slot ? Math.max(120, slot.maxHeight - getDesktopHeadlinesTipBorderY(tip)) : 0);
        const headingHeight = heading ? heading.offsetHeight : 0;
        const tipBorderY = getDesktopHeadlinesTipBorderY(tip);
        const scrollHeight = Math.max(80, tipHeight - headingHeight - tipBorderY);

        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("overflow", "hidden", "important");
        scroll.style.setProperty("flex", "1 1 auto", "important");
        scroll.style.setProperty("min-height", "0", "important");
        scroll.style.setProperty("overflow-x", "hidden", "important");
        scroll.style.setProperty("overflow-y", "auto", "important");
        scroll.style.setProperty("-webkit-overflow-scrolling", "touch", "important");
        scroll.style.setProperty("scrollbar-width", "none", "important");
        scroll.style.setProperty("pointer-events", "auto", "important");
        scroll.style.setProperty("touch-action", "pan-y", "important");
        scroll.style.setProperty("--hl-scroll-max-height", `${scrollHeight}px`);
        scroll.style.setProperty("height", `${scrollHeight}px`, "important");
        scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
    };

    const hideTooltips = (event) => {
        // Tablet / iPad Mini: page scroll closes Headlines + company tips.
        // Scrolling inside an already-open popup keeps that popup open.
        if (isTabletGenericTipViewport()) {
            if (event && event.target && event.target.closest) {
                const t = event.target;
                const hlWrap = t.closest(".tip-wrap.headlines-tip");
                if (hlWrap) {
                    const cb = hlWrap.querySelector(".hl-tip-cb");
                    if (
                        cb &&
                        cb.checked &&
                        t.closest(".tip-text") &&
                        !t.closest(".hl-tip-backdrop")
                    ) {
                        root.classList.remove(className);
                        document.body.classList.remove(className);
                        return;
                    }
                }
                if (
                    t.closest(".tip-wrap.scoop-mobile-tip-open:not(.headlines-tip)") &&
                    t.closest(".tip-text")
                ) {
                    root.classList.remove(className);
                    document.body.classList.remove(className);
                    return;
                }
            }
            const openedAt = window.__scoopTabletGenericTipOpenedAt || 0;
            if (Date.now() - openedAt < TABLET_GENERIC_TIP_OPEN_GRACE_MS) {
                return;
            }
            if (typeof window.__scoopCloseTabletTips === "function") {
                window.__scoopCloseTabletTips({ headlines: true, generics: true });
            } else {
                document
                    .querySelectorAll(
                        ".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked"
                    )
                    .forEach((checkbox) => {
                        checkbox.checked = false;
                        const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                        if (wrap) {
                            clearHeadlinesPosition(wrap);
                        }
                    });
                closeAllMobileGenericTips();
            }
            root.classList.add(className);
            document.body.classList.add(className);
            return;
        }
        if (isDesktopLayoutViewport() && isDesktopHeadlinesSessionOpen()) {
            if (Date.now() - (window.__scoopDesktopHlOpenedAt || 0) < 500) {
                root.classList.remove(className);
                document.body.classList.remove(className);
                return;
            }
            if (event && isInsideDesktopHeadlinesPopup(event.target)) {
                root.classList.remove(className);
                document.body.classList.remove(className);
                return;
            }
            document
                .querySelectorAll(
                    ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
                )
                .forEach((wrap) => hideDesktopHeadlines(wrap));
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (isPhoneMobileHeadlinesOpen()) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (event && getDesktopHeadlinesScrollEl(event.target)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (event && isInsideDesktopHeadlinesPopup(event.target)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (isMobileGenericTipViewport()) {
            closeAllMobileGenericTips();
        }
        root.classList.add(className);
        document.body.classList.add(className);
    };
    const allowTooltip = (event) => {
        if (isDesktopHeadlinesSessionOpen()) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        const element = event.target;
        if (!element || !element.closest) {
            return;
        }
        if (element.closest(".tip-wrap:not(.headlines-tip)")) {
            root.classList.remove(className);
            document.body.classList.remove(className);
        }
        if (isInsideDesktopHeadlinesPopup(element)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
        }
    };

    const isDesktopHeadlinesWrap = (node) => {
        if (!node || !node.closest) {
            return null;
        }
        return node.closest(".full-results-wrap .tip-wrap.headlines-tip");
    };

    const ensureDesktopHeadlinesVisible = (wrap) => {
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
    };

    const clearHeadlinesPosition = (wrap) => {
        if (wrap) {
            wrap.classList.remove("hl-tip-desktop-open");
            const timerId = window.__scoopDesktopHeadlinesHideTimers?.get(wrap);
            if (timerId) {
                window.clearTimeout(timerId);
                window.__scoopDesktopHeadlinesHideTimers.delete(wrap);
            }
        }
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        tip.style.removeProperty("--hl-fixed-top");
        tip.style.removeProperty("--hl-fixed-left");
        tip.style.removeProperty("--hl-fixed-width");
        tip.style.removeProperty("--hl-fixed-max-height");
        tip.style.removeProperty("--hl-fixed-height");
        tip.style.removeProperty("height");
        tip.style.removeProperty("position-anchor");
        tip.style.removeProperty("visibility");
        tip.style.removeProperty("opacity");
        tip.style.removeProperty("pointer-events");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        if (scroll) {
            scroll.scrollTop = 0;
            scroll.style.removeProperty("flex");
            scroll.style.removeProperty("min-height");
            scroll.style.removeProperty("margin-top");
            scroll.style.removeProperty("overflow-x");
            scroll.style.removeProperty("overflow-y");
            scroll.style.removeProperty("-webkit-overflow-scrolling");
            scroll.style.removeProperty("pointer-events");
            scroll.style.removeProperty("touch-action");
            scroll.style.removeProperty("height");
            scroll.style.removeProperty("max-height");
            scroll.style.removeProperty("--hl-scroll-max-height");
            scroll.style.removeProperty("--hl-scroll-overflow-y");
        }
        tip.style.removeProperty("display");
        tip.style.removeProperty("flex-direction");
        tip.style.removeProperty("overflow");
        unbindDesktopHeadlinesScrollWheel(wrap);
        restoreHeadlinesHeading(wrap);
    };

    const getHeadlinesHeadingBaseLabel = (heading) => {
        if (!heading) {
            return "Headlines";
        }
        if (!heading.dataset.hlBaseLabel) {
            const current = (heading.textContent || "Headlines").trim();
            heading.dataset.hlBaseLabel = current.split(" - ")[0].trim() || "Headlines";
        }
        return heading.dataset.hlBaseLabel;
    };

    const getCompanyNameFromHeadlinesRow = (wrap) => {
        const row = wrap?.closest("tr");
        if (!row) {
            return "";
        }

        const inCommodityResults = !!wrap.closest(".commodity-results");
        const valueCell =
            row.querySelector('td[data-label="Company"] .fr-val') ||
            row.querySelector('td[data-label="Name"] .fr-val') ||
            (inCommodityResults
                ? row.querySelector('td[data-label="Commodity"] .fr-val')
                : null);
        if (!valueCell) {
            return "";
        }

        const tipWrap = valueCell.querySelector(".tip-wrap");
        if (tipWrap) {
            const clone = tipWrap.cloneNode(true);
            clone.querySelectorAll(".tip-text").forEach((node) => node.remove());
            return (clone.textContent || "").replace(/\\s+/g, " ").trim();
        }

        return (valueCell.textContent || "").replace(/\\s+/g, " ").trim();
    };

    const updateHeadlinesHeading = (wrap) => {
        if (!wrap) {
            return;
        }
        const heading = wrap.querySelector(".hl-tip-heading");
        if (!heading) {
            return;
        }

        const baseLabel = getHeadlinesHeadingBaseLabel(heading);
        const company = getCompanyNameFromHeadlinesRow(wrap);
        heading.textContent = company ? `${baseLabel} - ${company}` : baseLabel;
    };

    const restoreHeadlinesHeading = (wrap) => {
        const heading = wrap?.querySelector(".hl-tip-heading");
        if (!heading) {
            return;
        }
        heading.textContent = getHeadlinesHeadingBaseLabel(heading);
    };

    const measureDesktopHeadlinesContentHeight = (tip) => {
        const heading = tip.querySelector(".hl-tip-heading");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const headingHeight = heading ? heading.offsetHeight : 0;
        if (!scroll) {
            return headingHeight;
        }
        const list = scroll.querySelector(".headlines-tip-list");
        const styles = getComputedStyle(scroll);
        const scrollPadding =
            (parseFloat(styles.paddingTop) || 0) + (parseFloat(styles.paddingBottom) || 0);
        const listHeight = list ? list.scrollHeight : scroll.scrollHeight;
        return headingHeight + listHeight + scrollPadding;
    };

    const fitDesktopHeadlinesTip = (tip, slot) => {
        if (!tip || !slot) {
            return;
        }
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const tipHeight = Math.max(280, slot.maxHeight);
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-height", `${tipHeight}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${tipHeight}px`);
        tip.style.setProperty("top", `${slot.top}px`, "important");
        tip.style.setProperty("left", `${slot.left}px`, "important");
        tip.style.setProperty("width", `${slot.width}px`, "important");
        tip.style.setProperty("min-width", `${slot.width}px`, "important");
        tip.style.setProperty("max-width", `${slot.width}px`, "important");
        tip.style.setProperty("height", `${tipHeight}px`, "important");
        tip.style.setProperty("max-height", `${tipHeight}px`, "important");
        if (scroll) {
            const heading = tip.querySelector(".hl-tip-heading");
            const headingHeight = heading ? heading.offsetHeight : 0;
            const scrollHeight = Math.max(80, tipHeight - headingHeight);
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("height", `${scrollHeight}px`, "important");
            scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
            scroll.style.setProperty("min-height", "0", "important");
        }
    };

    const bindDesktopHeadlinesScrollWheel = (wrap) => {
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        if (!scroll) {
            return;
        }
        const bindTarget = (node) => {
            if (!node) {
                return;
            }
            if (node.__hlWheelHandler) {
                node.removeEventListener("wheel", node.__hlWheelHandler, true);
            }
            node.__hlWheelHandler = (event) => {
                scrollDesktopHeadlinesFromWheel(event, scroll);
            };
            node.addEventListener("wheel", node.__hlWheelHandler, { passive: false, capture: true });
        };
        bindTarget(scroll);
        bindTarget(tip);
    };

    const unbindDesktopHeadlinesScrollWheel = (wrap) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        [scroll, tip].forEach((node) => {
            if (node?.__hlWheelHandler) {
                node.removeEventListener("wheel", node.__hlWheelHandler, true);
                delete node.__hlWheelHandler;
            }
        });
    };

    const getFullResultsTableRect = () => {
        const table = document.querySelector(".full-results-wrap .full-results-table");
        return table ? table.getBoundingClientRect() : null;
    };

    const getTableHeaderColumnRect = (pattern) => {
        const header = [...document.querySelectorAll(".full-results-wrap .full-results-table thead th")].find(
            (th) => {
                const t = (th.textContent || "").replace(/\s+/g, " ").trim();
                if (pattern === "headlines-col") {
                    return t.startsWith("Headlines") && !t.startsWith("Headline ");
                }
                return pattern.test(t);
            }
        );
        return header ? header.getBoundingClientRect() : null;
    };

    const getHeadlinesColumnRect = () => {
        return getTableHeaderColumnRect("headlines-col");
    };

    const getDesktopHeadlinesPanelRect = () => {
        const headlinesCol = getHeadlinesColumnRect();
        if (headlinesCol) {
            const width = Math.max(280, Math.min(21 * 16, window.innerWidth * 0.36));
            const left = headlinesCol.right + HEADLINES_DESKTOP_OFFSET;
            return { left, right: left + width, width };
        }
        return null;
    };

    const getPageScrollEl = () =>
        document.querySelector('[data-testid="stAppViewContainer"]') ||
        document.scrollingElement ||
        document.documentElement;

    const restorePageScroll = (scrollTop) => {
        const scrollEl = getPageScrollEl();
        scrollEl.scrollTop = scrollTop;
        window.scrollTo(0, scrollTop);
    };

    const getThirdTopPickNearLowBadge = () => {
        const topPickHeading = [...document.querySelectorAll("h3")].find((heading) =>
            /Top Picks/i.test((heading.textContent || "").trim())
        );
        if (!topPickHeading) {
            return null;
        }

        const mainBlock =
            topPickHeading.closest('[data-testid="stMainBlockContainer"]') ||
            topPickHeading.closest('[data-testid="stAppViewContainer"]');
        if (!mainBlock) {
            return null;
        }

        for (const block of mainBlock.querySelectorAll('[data-testid="stHorizontalBlock"]')) {
            const columns = [...block.children].filter(
                (node) => node.getAttribute("data-testid") === "stColumn"
            );
            if (columns.length < 3) {
                continue;
            }

            const thirdColumn = columns[2];
            const metric = thirdColumn.querySelector('[data-testid="stMetric"]');
            if (!metric || !/#3\\b/i.test(metric.textContent || "")) {
                continue;
            }

            const badge = [...thirdColumn.querySelectorAll("b")].find((node) =>
                /52W LOW/i.test((node.textContent || "").trim())
            );
            if (badge) {
                return badge;
            }
        }

        return null;
    };

    const getThirdTopPickNearLowAnchorRect = () => {
        const badge = getThirdTopPickNearLowBadge();
        return badge ? badge.getBoundingClientRect() : null;
    };

    const getNearLowBadgeFloorTop = () => {
        const anchorRect = getThirdTopPickNearLowAnchorRect();
        if (!anchorRect) {
            return null;
        }
        if (anchorRect.bottom <= VIEWPORT_PAD || anchorRect.top >= window.innerHeight) {
            return null;
        }
        return Math.round(anchorRect.bottom + DESKTOP_HEADLINES_ANCHOR_GAP);
    };

    const getDesktopHeadlinesAnchorTop = (tipHeight = 0) => {
        const headlinesCol = getHeadlinesColumnRect();
        if (headlinesCol) {
            const desiredBottom = headlinesCol.top - DESKTOP_HEADLINES_ABOVE_HEADING;
            let top = desiredBottom - (tipHeight || 0);
            if (top < VIEWPORT_PAD) {
                top = VIEWPORT_PAD;
            }
            return Math.round(top);
        }
        return DESKTOP_HEADLINES_TOP;
    };

    const getDesktopHeadlinesSlot = (tipHeight = 0) => {
        const PAD = VIEWPORT_PAD;
        const MIN_W = 280;
        const EXTRA_W = 130;
        const MIN_H = 280;
        const viewH = window.innerHeight || 800;
        const viewW = window.innerWidth || 1600;
        const inView = (r) =>
            r && r.width > 40 && r.bottom > 0 && r.top < viewH && r.right > 0 && r.left < viewW;
        const moodTh = [...document.querySelectorAll(".full-results-wrap .full-results-table thead th")].find(
            (th) => (th.textContent || "").replace(/\s+/g, " ").trim().startsWith("Market Mood")
        );
        const moodTds = [...document.querySelectorAll('.full-results-wrap td[data-label="Market Mood"]')];
        const vis = moodTds.map((el) => el.getBoundingClientRect()).filter(inView);
        const thRect = moodTh ? moodTh.getBoundingClientRect() : null;
        const table = document.querySelector(".full-results-wrap .full-results-table");
        const tbody = table && table.tBodies && table.tBodies[0];
        const tableBottom = tbody
            ? tbody.getBoundingClientRect().bottom
            : (table ? table.getBoundingClientRect().bottom : viewH - PAD);
        let left = PAD;
        let width = MIN_W;
        let top = PAD;
        if (vis.length) {
            left = Math.min(...vis.map((r) => r.left));
            width = Math.max(...vis.map((r) => r.width));
            top = inView(thRect) ? thRect.top - 8 : Math.min(...vis.map((r) => r.top)) - 8;
        } else if (moodTds[0]) {
            const r = moodTds[0].getBoundingClientRect();
            left = r.left;
            width = r.width;
        }
        width = Math.max(MIN_W, Math.round(width)) + EXTRA_W;
        left = Math.round(left);
        top = Math.round(top);
        if (top < PAD) top = PAD;
        if (left < PAD) left = PAD;
        if (left + width > viewW - PAD) width = Math.max(MIN_W + EXTRA_W, viewW - PAD - left);
        let maxHeight = Math.round(Math.min(tableBottom, viewH - PAD) - top);
        if (vis.length) {
            maxHeight = Math.max(maxHeight, Math.round(Math.max(...vis.map((r) => r.bottom)) - top));
        }
        if (top + maxHeight > viewH - PAD) maxHeight = Math.round(viewH - PAD - top);
        maxHeight = Math.max(MIN_H, maxHeight);
        return {
            top,
            left,
            width,
            maxHeight,
            tableBottom,
        };
    };

    const positionDesktopHeadlinesTip = (wrap, preserveScroll = false) => {
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const prevScrollTop = preserveScroll && scroll ? scroll.scrollTop : 0;

        tip.style.setProperty("position-anchor", "none");
        updateHeadlinesHeading(wrap);

        const slot = getDesktopHeadlinesSlot();

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);

        if (!preserveScroll && scroll) {
            scroll.scrollTop = 0;
        }
        fitDesktopHeadlinesTip(tip, slot);
        applyDesktopHeadlinesScrollStyles(wrap, slot);
        if (preserveScroll && scroll) {
            scroll.scrollTop = prevScrollTop;
        }

        const tipHeight =
            parseFloat(tip.style.getPropertyValue("--hl-fixed-height")) ||
            tip.clientHeight ||
            0;

        if (isDesktopHeadlinesOpenWrap(wrap)) {
            ensureDesktopHeadlinesVisible(wrap);
            bindDesktopHeadlinesScrollWheel(wrap);
        }
    };

    const scheduleDesktopHeadlinesPosition = (wrap, preserveScroll = false) => {
        positionDesktopHeadlinesTip(wrap, preserveScroll);
        window.requestAnimationFrame(() => {
            positionDesktopHeadlinesTip(wrap, preserveScroll);
        });
    };

    const resolveDesktopHeadlinesWrap = (node) => {
        if (!node || !node.closest) {
            return null;
        }
        return node.closest(".full-results-wrap .tip-wrap.headlines-tip");
    };

    const getDesktopHeadlinesScrollEl = (node, event) => {
        if (!isDesktopLayoutViewport()) {
            return null;
        }

        let target = node && node.nodeType === Node.ELEMENT_NODE ? node : null;
        if (event && Number.isFinite(event.clientX) && Number.isFinite(event.clientY)) {
            const hit = document.elementFromPoint(event.clientX, event.clientY);
            if (hit && hit.nodeType === Node.ELEMENT_NODE) {
                target = hit;
            }
        }
        if (!target || !target.closest) {
            return null;
        }

        const resolvedWrap = target.closest(
            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
        );
        if (!resolvedWrap) {
            return null;
        }
        const scroll = getDesktopHeadlinesScrollContainer(resolvedWrap);
        if (!scroll) {
            return null;
        }
        if (scroll.contains(target) || target.closest(".headlines-tip-scroll") === scroll) {
            return scroll;
        }
        if (target.closest(".tip-text") && resolvedWrap.contains(target.closest(".tip-text"))) {
            return scroll;
        }
        return null;
    };

    const cancelDesktopHeadlinesHide = (wrap) => {
        if (!wrap || !window.__scoopDesktopHeadlinesHideTimers) {
            return;
        }
        const timerId = window.__scoopDesktopHeadlinesHideTimers.get(wrap);
        if (timerId) {
            window.clearTimeout(timerId);
            window.__scoopDesktopHeadlinesHideTimers.delete(wrap);
        }
    };

    const hideDesktopHeadlines = (wrap) => {
        if (!wrap) {
            return;
        }
        cancelDesktopHeadlinesHide(wrap);
        wrap.classList.remove("hl-tip-desktop-open");
        clearHeadlinesPosition(wrap);
    };

    const showDesktopHeadlines = (wrap) => {
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        cancelDesktopHeadlinesHide(wrap);
        wrap.classList.add("hl-tip-desktop-open");
        root.classList.remove(className);
        document.body.classList.remove(className);
        ensureDesktopHeadlinesVisible(wrap);
        scheduleDesktopHeadlinesPosition(wrap, false);
        window.requestAnimationFrame(() => {
            scheduleDesktopHeadlinesPosition(wrap, true);
        });
    };

    const closeOtherDesktopHeadlines = (activeCheckbox) => {
        window.__scoopDesktopHeadlinesSyncing = true;
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                if (checkbox === activeCheckbox) {
                    return;
                }
                checkbox.checked = false;
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    hideDesktopHeadlines(wrap);
                }
            });
        window.__scoopDesktopHeadlinesSyncing = false;
    };

    const handleDesktopHeadlinesChange = (checkbox) => {
        if (!isDesktopLayoutViewport() || !checkbox) {
            return;
        }
        const wrap = checkbox.closest(".tip-wrap.headlines-tip");
        if (!wrap) {
            return;
        }
        if (window.__scoopDesktopHeadlinesSyncing) {
            return;
        }
        if (checkbox.checked) {
            closeOtherDesktopHeadlines(checkbox);
            showDesktopHeadlines(wrap);
            return;
        }
        hideDesktopHeadlines(wrap);
    };

    const handleHeadlinesCheckboxChange = (event) => {
        const checkbox = event.target;
        if (!checkbox || !checkbox.classList || !checkbox.classList.contains("hl-tip-cb")) {
            return;
        }
        const wrap = checkbox.closest(".tip-wrap.headlines-tip");
        if (!wrap) {
            return;
        }
        if (isDesktopLayoutViewport()) {
            handleDesktopHeadlinesChange(checkbox);
            return;
        }
        if (checkbox.checked) {
            // Tablet / iPad Mini: only one tip popup at a time.
            if (usesTabletProHeadlinesPopup()) {
                window.__scoopDesktopHeadlinesSyncing = true;
                document
                    .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
                    .forEach((other) => {
                        if (other === checkbox) {
                            return;
                        }
                        other.checked = false;
                        const otherWrap = other.closest(".tip-wrap.headlines-tip");
                        if (otherWrap) {
                            clearHeadlinesPosition(otherWrap);
                        }
                    });
                window.__scoopDesktopHeadlinesSyncing = false;
                closeAllMobileGenericTips();
                scheduleResponsiveHeadlinesPosition(wrap);
            } else if (isPhoneMobileHeadlinesViewport()) {
                closeAllMobileGenericTips();
                const savedScrollTop = getPageScrollEl().scrollTop;
                schedulePhoneMobileHeadlinesPosition(wrap);
                window.requestAnimationFrame(() => {
                    restorePageScroll(savedScrollTop);
                    schedulePhoneMobileHeadlinesPosition(wrap);
                    window.requestAnimationFrame(() => {
                        restorePageScroll(savedScrollTop);
                        schedulePhoneMobileHeadlinesPosition(wrap);
                    });
                });
            }
            updateHeadlinesHeading(wrap);
            window.requestAnimationFrame(() => {
                if (usesTabletProHeadlinesPopup()) {
                    scheduleResponsiveHeadlinesPosition(wrap);
                } else if (isPhoneMobileHeadlinesViewport()) {
                    schedulePhoneMobileHeadlinesPosition(wrap);
                }
                updateHeadlinesHeading(wrap);
            });
        } else {
            clearHeadlinesPosition(wrap);
        }
    };

    const scrollDesktopHeadlinesFromWheel = (event, scrollEl) => {
        if (!isDesktopLayoutViewport() || !scrollEl || !event) {
            return false;
        }
        const delta = event.deltaY;
        if (!delta) {
            return false;
        }
        const maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
        event.preventDefault();
        event.stopPropagation();
        if (maxScroll <= 0) {
            return true;
        }
        scrollEl.scrollTop = Math.max(0, Math.min(maxScroll, scrollEl.scrollTop + delta));
        return true;
    };

    const handleDesktopHeadlinesWheel = (event) => {
        if (!isDesktopLayoutViewport()) {
            return;
        }
        if (!isDesktopHeadlinesSessionOpen()) {
            return;
        }
        const scrollEl = getDesktopHeadlinesScrollEl(event.target, event);
        if (!scrollEl) {
            return;
        }
        scrollDesktopHeadlinesFromWheel(event, scrollEl);
    };

    const repositionOpenDesktopHeadlines = () => {
        if (!isDesktopLayoutViewport()) {
            return;
        }
        document
            .querySelectorAll(
                ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
            )
            .forEach((wrap) => scheduleDesktopHeadlinesPosition(wrap, true));
    };

    /* Refresh on every Streamlit rerun — listeners are bound once below. */
    window.__scoopDesktopHeadlinesApi = {
        clearHeadlinesPosition,
        fitDesktopHeadlinesTip,
        getDesktopHeadlinesSlot,
        getThirdTopPickNearLowAnchorRect,
        getThirdTopPickNearLowBadge,
        getNearLowBadgeFloorTop,
        getDesktopHeadlinesAnchorTop,
        positionDesktopHeadlinesTip,
        scheduleDesktopHeadlinesPosition,
        repositionOpenDesktopHeadlines,
        showDesktopHeadlines,
        hideDesktopHeadlines,
        cancelDesktopHeadlinesHide,
        ensureDesktopHeadlinesVisible,
        handleDesktopHeadlinesChange,
        handleHeadlinesCheckboxChange,
        handleDesktopHeadlinesWheel,
        scrollDesktopHeadlinesFromWheel,
        getDesktopHeadlinesScrollEl,
        getDesktopHeadlinesScrollContainer,
        applyDesktopHeadlinesScrollStyles,
        bindDesktopHeadlinesScrollWheel,
        unbindDesktopHeadlinesScrollWheel,
    };

    const getIpadMiniHeadlinesSlot = () => {
        const top = IPAD_MINI_HEADLINES_TOP;
        const pad = VIEWPORT_PAD;
        const viewRight = window.innerWidth - pad;
        const viewLeft = pad;
        const availableWidth = viewRight - viewLeft;

        const width = Math.round(
            Math.min(
                availableWidth,
                IPAD_MINI_HEADLINES_MAX_WIDTH,
                Math.max(260, Math.round(window.innerWidth * 0.42))
            )
        );

        let left = Math.round((window.innerWidth - width) / 2);
        left = Math.max(viewLeft, Math.min(left, viewRight - width));

        const maxHeight = Math.max(
            160,
            window.innerHeight - top - IPAD_MINI_HEADLINES_BOTTOM
        );

        return {
            top,
            left: Math.round(left),
            width: Math.round(width),
            maxHeight: Math.round(maxHeight),
        };
    };

    const clampIpadMiniGenericTipInViewport = (tip, anchorY) => {
        const pad = VIEWPORT_PAD;
        const vh = window.innerHeight;
        const maxPanelHeight = Math.max(120, vh - 2 * pad);

        tip.style.setProperty("max-height", `${maxPanelHeight}px`, "important");
        tip.style.setProperty("--scoop-ipad-mini-tip-max-height", `${maxPanelHeight}px`, "important");
        tip.style.setProperty("overflow-y", "auto", "important");
        tip.style.setProperty("overflow-x", "hidden", "important");

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", "50vw", "important");
        const ipadW = tip.getBoundingClientRect().width || tip.offsetWidth;
        const ipadLeft = Math.max(pad, (window.innerWidth - ipadW) / 2);
        tip.style.setProperty("left", `${ipadLeft}px`, "important");

        let tipHeight = measureMobileGenericTipHeight(tip);
        tipHeight = Math.min(tipHeight, maxPanelHeight);

        const gap = MOBILE_GENERIC_TIP_GAP;
        let top = anchorY - tipHeight - gap;
        if (top < pad) {
            const below = anchorY + gap;
            if (below + tipHeight <= vh - pad) {
                top = below;
            } else {
                top = Math.max(pad, vh - pad - tipHeight);
            }
        }
        top = Math.max(pad, Math.min(top, vh - pad - tipHeight));

        const fittedMaxHeight = Math.max(80, vh - top - pad);
        tip.style.setProperty("--scoop-mobile-tip-top", `${Math.round(top)}px`, "important");
        tip.style.setProperty("max-height", `${fittedMaxHeight}px`, "important");
        tip.style.setProperty("--scoop-ipad-mini-tip-max-height", `${fittedMaxHeight}px`, "important");
    };

    const getResponsiveHeadlinesSlot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const viewRight = window.innerWidth - VIEWPORT_PAD;

        const top = Math.round(headerBottom + VIEWPORT_PAD);
        const maxHeight = Math.max(200, window.innerHeight - top - VIEWPORT_PAD);

        let viewLeft = VIEWPORT_PAD;
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            const sidebarRight = sidebar.getBoundingClientRect().right;
            viewLeft = Math.max(VIEWPORT_PAD, Math.round(sidebarRight + VIEWPORT_PAD));
        }

        const content =
            document.querySelector(".full-results-wrap") ||
            document.querySelector('[data-testid="stMainBlockContainer"]') ||
            document.querySelector('[data-testid="stAppViewContainer"]');

        const centerHorizontally =
            isResponsiveHeadlinesViewport() || isIpadMiniViewport();

        let widthBasisLeft = viewLeft;
        if (!centerHorizontally && content) {
            widthBasisLeft = Math.max(viewLeft, Math.round(content.getBoundingClientRect().left));
        }

        const availableWidth = viewRight - (centerHorizontally ? viewLeft : widthBasisLeft);
        const width = Math.round(
            Math.min(availableWidth, Math.max(280, window.innerWidth * 0.4))
        );

        let left = centerHorizontally
            ? Math.round(viewLeft + (viewRight - viewLeft - width) / 2)
            : widthBasisLeft;

        if (left + width > viewRight) {
            left = Math.max(viewLeft, viewRight - width);
        }
        if (left < viewLeft) {
            left = viewLeft;
        }

        if (isIpadAirViewport()) {
            left = Math.round((window.innerWidth - width) / 2);
            left = Math.max(VIEWPORT_PAD, Math.min(left, viewRight - width));
        }

        if (isSurfaceDuoViewport()) {
            left = Math.round((window.innerWidth - width) / 2);
            left = Math.max(VIEWPORT_PAD, Math.min(left, viewRight - width));
        }

        return {
            top,
            left: Math.round(left),
            width,
            maxHeight: Math.round(maxHeight),
        };
    };

    const getPhoneMobileHeadlinesSlot = (wrap) => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        let chromeBottom = headerBottom;
        [
            ".scoop-env-banner",
            ".scoop-mobile-back-home-bar",
            ".scoop-mobile-inner-top",
        ].forEach((sel) => {
            document.querySelectorAll(sel).forEach((el) => {
                const r = el.getBoundingClientRect();
                if (r.height > 1 && r.top < 28 && r.bottom > chromeBottom) {
                    chromeBottom = r.bottom;
                }
            });
        });
        const viewRight = window.innerWidth - VIEWPORT_PAD;
        const viewLeft = VIEWPORT_PAD;
        const top = Math.round(Math.max(chromeBottom, 0) + VIEWPORT_PAD);
        const maxHeight = Math.max(
            200,
            window.innerHeight - top - MOBILE_HEADLINES_BOTTOM_TAP_PAD
        );

        let left = viewLeft;
        let width = Math.round(
            Math.min(viewRight - viewLeft, Math.max(280, window.innerWidth - 2 * VIEWPORT_PAD))
        );

        const row = wrap?.closest("tr");
        if (row) {
            const cardRect = row.getBoundingClientRect();
            if (cardRect.width > 0) {
                width = Math.max(
                    240,
                    Math.round(cardRect.width - MOBILE_HEADLINES_CARD_WIDTH_INSET)
                );
                left = Math.round(cardRect.left + MOBILE_HEADLINES_CARD_WIDTH_INSET / 2);
                if (left + width > viewRight) {
                    left = Math.max(viewLeft, viewRight - width);
                }
                if (left < viewLeft) {
                    left = viewLeft;
                    width = Math.min(width, viewRight - viewLeft);
                }
            }
        }

        return {
            top,
            left: Math.round(left),
            width: Math.round(width),
            maxHeight: Math.round(maxHeight),
        };
    };

    const applyPhoneMobileHeadlinesSlot = (wrap, slot, resetScroll = true) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        if (!tip || !slot) {
            return;
        }

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("position-anchor", "none");
        tip.style.setProperty("height", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("overflow", "hidden", "important");

        if (resetScroll) {
            const scroll = tip.querySelector(".headlines-tip-scroll");
            if (scroll) {
                scroll.scrollTop = 0;
                scroll.style.removeProperty("margin-top");
            }
        }
    };

    const positionPhoneMobileHeadlinesTip = (wrap, preserveScroll = false) => {
        if (!isPhoneMobileHeadlinesViewport() || !wrap) {
            return;
        }
        const checkbox = wrap.querySelector(".hl-tip-cb");
        if (!checkbox || !checkbox.checked) {
            return;
        }

        applyPhoneMobileHeadlinesSlot(wrap, getPhoneMobileHeadlinesSlot(wrap), !preserveScroll);
        updateHeadlinesHeading(wrap);
    };

    const schedulePhoneMobileHeadlinesPosition = (wrap, preserveScroll = false) => {
        positionPhoneMobileHeadlinesTip(wrap, preserveScroll);
        window.requestAnimationFrame(() => positionPhoneMobileHeadlinesTip(wrap, preserveScroll));
    };

    const repositionOpenPhoneMobileHeadlines = () => {
        if (!isPhoneMobileHeadlinesViewport()) {
            return;
        }
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    schedulePhoneMobileHeadlinesPosition(wrap, true);
                }
            });
    };

    const positionResponsiveHeadlinesTip = (wrap) => {
        if (!usesTabletProHeadlinesPopup() || !wrap) {
            return;
        }
        const checkbox = wrap.querySelector(".hl-tip-cb");
        if (!checkbox || !checkbox.checked) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }

        const slot = isIpadMiniViewport()
            ? getIpadMiniHeadlinesSlot()
            : getResponsiveHeadlinesSlot();

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        updateHeadlinesHeading(wrap);

        const scroll = tip.querySelector(".headlines-tip-scroll");
        if (scroll) {
            scroll.scrollTop = 0;
        }
    };

    const scheduleResponsiveHeadlinesPosition = (wrap) => {
        positionResponsiveHeadlinesTip(wrap);
        window.requestAnimationFrame(() => positionResponsiveHeadlinesTip(wrap));
    };

    const repositionOpenResponsiveHeadlines = () => {
        if (!usesTabletProHeadlinesPopup()) {
            return;
        }
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    scheduleResponsiveHeadlinesPosition(wrap);
                }
            });
    };

    const resetGenericTooltips = () => {
        document.querySelectorAll(".tip-wrap:not(.headlines-tip)").forEach((wrap) => {
            if (
                isDesktopLayoutViewport() &&
                (wrap.classList.contains("scoop-name-tip") ||
                    wrap.classList.contains("scoop-desktop-name-tip-open"))
            ) {
                return;
            }
            wrap.classList.remove("generic-tip-open", "scoop-mobile-tip-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) {
                return;
            }
            [
                "position",
                "left",
                "top",
                "right",
                "bottom",
                "transform",
                "width",
                "max-width",
                "min-width",
                "max-height",
                "overflow-y",
                "visibility",
                "opacity",
                "pointer-events",
                "display",
                "z-index",
                "--tip-center-x",
                "--tip-center-y",
                "--tip-fixed-width",
                "--tip-fixed-max-height",
                "--scoop-mobile-tip-top",
                "--scoop-mobile-tip-left",
                "--scoop-se-name-tip-top",
                "--scoop-tablet-tip-left",
                "--scoop-tablet-tip-top",
                "--scoop-tablet-tip-width",
            ].forEach((prop) => tip.style.removeProperty(prop));
        });
    };

    const IPHONE_SE_MAX = 375;
    const MOBILE_GENERIC_TIP_GAP = 20;
    const TABLET_GENERIC_TIP_GAP = 12;
    const TABLET_GENERIC_TIP_PAD = 12;
    const isIphoneSEViewport = () => window.innerWidth <= IPHONE_SE_MAX;
    // Phone-sized only — iPad Mini+ uses tablet beside-row placement.
    const isOtherMobileViewport = () =>
        window.innerWidth > IPHONE_SE_MAX && window.innerWidth <= MOBILE_GENERIC_TIP_MAX;
    // Phone only — tablet uses beside-trigger placement instead of viewport centering.
    const usesTapCenteredGenericTip = () => isOtherMobileViewport();

    const isMobileGenericTipWrap = (wrap) =>
        !!wrap && !wrap.classList.contains("headlines-tip");

    const measureMobileGenericTipHeight = (tip) => {
        tip.style.setProperty("visibility", "hidden", "important");
        tip.style.setProperty("opacity", "1", "important");
        if (isIphoneSEViewport()) {
            tip.style.setProperty("top", "-9999px", "important");
        } else if (usesTapCenteredGenericTip() || isTabletGenericTipViewport()) {
            tip.style.setProperty("top", "-9999px", "important");
        } else {
            tip.style.setProperty("position", "fixed", "important");
            tip.style.setProperty("left", "-9999px", "important");
            tip.style.setProperty("top", "0", "important");
            tip.style.setProperty("width", "50vw", "important");
        }
        const height = tip.offsetHeight;
        tip.style.removeProperty("visibility");
        tip.style.removeProperty("opacity");
        tip.style.removeProperty("position");
        tip.style.removeProperty("left");
        tip.style.removeProperty("top");
        tip.style.removeProperty("width");
        return height;
    };

    const applyPhoneViewportCenteredGenericTip = (tip, topPx) => {
        // Phone only: force viewport-centered fixed box (page CSS uses absolute + right:0).
        if (!isMobileGenericTipViewport() || isTabletGenericTipViewport() || !tip) {
            return;
        }
        const pad = 8;
        const tipWidth = Math.round(window.innerWidth * 0.5);
        const maxWidth = tipWidth;
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", `${tipWidth}px`, "important");
        tip.style.setProperty("max-width", `${maxWidth}px`, "important");
        tip.style.setProperty("min-width", "0", "important");
        tip.style.setProperty("box-sizing", "border-box", "important");
        tip.style.setProperty("white-space", "normal", "important");
        tip.style.setProperty("word-break", "break-word", "important");
        tip.style.setProperty("overflow-wrap", "anywhere", "important");
        tip.style.setProperty("overflow-x", "hidden", "important");
        tip.style.setProperty("text-align", "left", "important");
        const width = tip.getBoundingClientRect().width || tip.offsetWidth || tipWidth;
        const left = Math.max(pad, Math.min((window.innerWidth - width) / 2, window.innerWidth - width - pad));
        tip.style.setProperty("--scoop-mobile-tip-left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("--scoop-mobile-tip-top", `${Math.round(topPx)}px`, "important");
        tip.style.setProperty("left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("top", `${Math.round(topPx)}px`, "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("display", "block", "important");
        tip.style.setProperty("z-index", "100002", "important");
    };

    // Tablet: place generic tip beside the tapped text, vertically centered on the card row.
    // Headlines tips are never passed here (filtered by isMobileGenericTipWrap).
    const positionTabletBesideGenericTip = (wrap) => {
        if (!isTabletGenericTipViewport() || !isMobileGenericTipWrap(wrap)) {
            return;
        }
        // Ignore stale rAF from a tip that was already closed.
        if (!wrap.classList.contains("scoop-mobile-tip-open")) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        const wrapRect = wrap.getBoundingClientRect();
        const card =
            wrap.closest("tr") ||
            wrap.closest(".full-results-wrap") ||
            wrap.closest('[data-testid="stElementContainer"]');
        const cardRect = card ? card.getBoundingClientRect() : wrapRect;
        const pad = TABLET_GENERIC_TIP_PAD;
        const gap = TABLET_GENERIC_TIP_GAP;
        const viewLeft = pad;
        const viewRight = window.innerWidth - pad;
        const viewTop = pad;
        const viewBottom = window.innerHeight - pad;
        const cardLeft = Math.max(viewLeft, cardRect.left + pad);
        const cardRight = Math.min(viewRight, cardRect.right - pad);
        const cardInnerW = Math.max(160, cardRight - cardLeft);

        // Value-side names (Company/Ticker/…) sit on the right — open into the card middle (left).
        // Label-side tips open to the right of the label.
        const preferLeft =
            !!wrap.closest(".fr-val") ||
            wrapRect.left > (cardLeft + cardRight) / 2;

        let tipWidth = Math.round(window.innerWidth * 0.5);
        tipWidth = Math.max(120, Math.min(tipWidth, viewRight - viewLeft));

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", `${tipWidth}px`, "important");
        tip.style.setProperty("--scoop-tablet-tip-width", `${tipWidth}px`, "important");

        let tipHeight = measureMobileGenericTipHeight(tip);
        // measureMobileGenericTipHeight clears width — restore before placement math/paint.
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", `${tipWidth}px`, "important");
        tip.style.setProperty("--scoop-tablet-tip-width", `${tipWidth}px`, "important");
        tipHeight = Math.min(tipHeight, Math.max(120, viewBottom - viewTop));
        tip.style.setProperty("max-height", `${Math.round(tipHeight)}px`, "important");

        let left;
        if (preferLeft) {
            left = wrapRect.left - gap - tipWidth;
            if (left < cardLeft) {
                left = cardLeft;
            }
        } else {
            left = wrapRect.right + gap;
            if (left + tipWidth > cardRight) {
                left = Math.max(cardLeft, wrapRect.left - gap - tipWidth);
            }
            if (left + tipWidth > cardRight) {
                left = cardLeft + Math.max(0, (cardInnerW - tipWidth) / 2);
            }
        }
        left = Math.max(viewLeft, Math.min(left, viewRight - tipWidth));

        // Vertically center on the tapped text / card row.
        const anchorMidY = wrapRect.top + wrapRect.height / 2;
        let top = anchorMidY - tipHeight / 2;
        const cardTop = Math.max(viewTop, cardRect.top + pad * 0.5);
        const cardBottom = Math.min(viewBottom, cardRect.bottom - pad * 0.5);
        if (top < cardTop) {
            top = cardTop;
        }
        if (top + tipHeight > cardBottom) {
            top = Math.max(cardTop, cardBottom - tipHeight);
        }
        top = Math.max(viewTop, Math.min(top, viewBottom - tipHeight));

        tip.style.setProperty("--scoop-tablet-tip-left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("--scoop-tablet-tip-top", `${Math.round(top)}px`, "important");
        tip.style.setProperty("left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("top", `${Math.round(top)}px`, "important");
        // Page screener CSS hides all generic tips; force open state on the element itself.
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("display", "block", "important");
        tip.style.setProperty("z-index", "100002", "important");
    };

    const positionMobileGenericTip = (wrap, event) => {
        if (!isTapGenericTipViewport() || !isMobileGenericTipWrap(wrap)) {
            return;
        }
        if (!wrap.classList.contains("scoop-mobile-tip-open")) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }

        if (isTabletGenericTipViewport()) {
            positionTabletBesideGenericTip(wrap);
            return;
        }

        const touch = event && event.touches && event.touches[0];
        const anchorY =
            (event && typeof event.clientY === "number" ? event.clientY : null) ??
            (touch ? touch.clientY : null) ??
            wrap.getBoundingClientRect().top;
        if (isIpadMiniViewport()) {
            clampIpadMiniGenericTipInViewport(tip, anchorY);
            return;
        }
        ensurePhoneGenericTipRuntimeCss();
        const tipHeight = measureMobileGenericTipHeight(tip);
        const maxTop = Math.max(8, window.innerHeight - tipHeight - 8);
        const top = Math.max(8, Math.min(anchorY - tipHeight - MOBILE_GENERIC_TIP_GAP, maxTop));
        applyPhoneViewportCenteredGenericTip(tip, top);
    };

    const scheduleMobileGenericTip = (wrap, event) => {
        positionMobileGenericTip(wrap, event);
        window.requestAnimationFrame(() => positionMobileGenericTip(wrap, event));
    };

    const closeResponsiveHeadlinesPopups = () => {
        if (!isTapGenericTipViewport()) {
            return;
        }
        document
            .querySelectorAll(".tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                checkbox.checked = false;
                const headlinesWrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (headlinesWrap) {
                    clearHeadlinesPosition(headlinesWrap);
                }
            });
    };

    const genericTipName = (wrap) => {
        const td = wrap.closest("td[data-label]");
        if (td) {
            const label = String(td.getAttribute("data-label") || "").trim();
            if (label) return label;
        }
        let t = "";
        wrap.childNodes.forEach((node) => {
            if (node.nodeType === Node.TEXT_NODE) t += node.textContent || "";
        });
        t = t.replace(/\s+/g, " ").trim();
        if (t) return t;
        const clone = wrap.cloneNode(true);
        clone.querySelectorAll(".tip-text, .hl-tip-cb, .scoop-tip-title").forEach((el) => el.remove());
        return (clone.textContent || "").replace(/\s+/g, " ").trim();
    };
    const ensureGenericTipTitle = (wrap) => {
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        let title = tip.querySelector(":scope > .scoop-tip-title");
        if (!title) {
            title = document.createElement("div");
            title.className = "scoop-tip-title";
            tip.insertBefore(title, tip.firstChild);
        }
        const name = genericTipName(wrap);
        title.textContent = name;
        title.style.display = name ? "block" : "none";
    };

    const openMobileGenericTip = (wrap, event) => {
        if (!isMobileGenericTipViewport() || !isMobileGenericTipWrap(wrap)) {
            return;
        }
        ensurePhoneGenericTipRuntimeCss();
        closeResponsiveHeadlinesPopups();
        closeAllMobileGenericTips();
        wrap.classList.add("scoop-mobile-tip-open");
        ensureGenericTipTitle(wrap);
        scheduleMobileGenericTip(wrap, event);
    };

    const openTabletGenericTip = (wrap, event) => {
        if (!isTabletGenericTipViewport() || !isMobileGenericTipWrap(wrap)) {
            return;
        }
        ensureTabletGenericTipRuntimeCss();
        closeResponsiveHeadlinesPopups();
        closeAllMobileGenericTips();
        wrap.classList.add("scoop-mobile-tip-open");
        ensureGenericTipTitle(wrap);
        clearTooltipScrollingHide();
        window.__scoopTabletGenericTipOpenedAt = Date.now();
        scheduleMobileGenericTip(wrap, event);
    };

    // Streamlit can reorder page <style> after our st.html inject (NASDAQ/NYSE tip CSS
    // with right:0 / left:50%). Re-append this block as the last stylesheet so tablet
    // beside-placement always wins. Headlines tips are excluded.
    const TABLET_GENERIC_TIP_RUNTIME_CSS = `
@media (min-width: 744px) and (max-width: 1366px) {
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):focus-within .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text {
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    right: auto !important;
    left: -10000px !important;
    transform: none !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
    position: fixed !important;
    left: var(--scoop-tablet-tip-left, -10000px) !important;
    top: var(--scoop-tablet-tip-top, -10000px) !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    margin: 0 !important;
    width: var(--scoop-tablet-tip-width, 50vw) !important;
    min-width: 0 !important;
    max-width: 50vw !important;
    font-size: 1.08rem !important;
    line-height: 1.42 !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text {
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    display: block !important;
    position: fixed !important;
    left: var(--scoop-tablet-tip-left, -10000px) !important;
    top: var(--scoop-tablet-tip-top, -10000px) !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text > .scoop-tip-title {
    display: block !important; font-weight: 700 !important; font-size: 1.12rem !important;
    line-height: 1.25 !important; margin: 0 0 0.45rem 0 !important; padding: 0 0 0.4rem 0 !important;
    border-bottom: 1px solid rgba(148, 163, 184, 0.45) !important; color: #f8fafc !important;
  }
}
`;

    const PHONE_GENERIC_TIP_RUNTIME_CSS = `
@media (max-width: 743px) {
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text {
    visibility: hidden !important; opacity: 0 !important; pointer-events: none !important;
    left: -10000px !important; right: auto !important; transform: none !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
    position: fixed !important;
    left: var(--scoop-mobile-tip-left, -10000px) !important;
    top: var(--scoop-mobile-tip-top, -10000px) !important;
    right: auto !important; bottom: auto !important; transform: none !important; margin: 0 !important;
    width: 50vw !important;
    max-width: 50vw !important;
    font-size: 1.08rem !important;
    line-height: 1.42 !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text {
    visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;
    display: block !important; position: fixed !important;
    left: var(--scoop-mobile-tip-left, 8px) !important;
    top: var(--scoop-mobile-tip-top, 8px) !important;
    right: auto !important; bottom: auto !important; transform: none !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text > .scoop-tip-title {
    display: block !important; font-weight: 700 !important; font-size: 1.12rem !important;
    line-height: 1.25 !important; margin: 0 0 0.45rem 0 !important; padding: 0 0 0.4rem 0 !important;
    border-bottom: 1px solid rgba(148, 163, 184, 0.45) !important; color: #f8fafc !important;
  }
}
`;

    const ensurePhoneGenericTipRuntimeCss = () => {
        if (!isMobileGenericTipViewport() || isTabletGenericTipViewport()) {
            return;
        }
        const id = "scoop-phone-generic-tip-runtime-css";
        let el = document.getElementById(id);
        if (!el) {
            el = document.createElement("style");
            el.id = id;
            el.textContent = PHONE_GENERIC_TIP_RUNTIME_CSS;
        } else if (el.textContent !== PHONE_GENERIC_TIP_RUNTIME_CSS) {
            el.textContent = PHONE_GENERIC_TIP_RUNTIME_CSS;
        }
        document.documentElement.appendChild(el);
    };

    const ensureTabletGenericTipRuntimeCss = () => {
        if (!isTabletGenericTipViewport()) {
            return;
        }
        const id = "scoop-tablet-generic-tip-runtime-css";
        let el = document.getElementById(id);
        if (!el) {
            el = document.createElement("style");
            el.id = id;
            el.textContent = TABLET_GENERIC_TIP_RUNTIME_CSS;
        } else if (el.textContent !== TABLET_GENERIC_TIP_RUNTIME_CSS) {
            el.textContent = TABLET_GENERIC_TIP_RUNTIME_CSS;
        }
        // Always move to the end so NASDAQ/NYSE page CSS cannot win on cascade order.
        document.documentElement.appendChild(el);
    };

    const bindMobileGenericTips = () => {
        if (window.__scoopMobileGenericTipBindVersion === 10) {
            return;
        }
        window.__scoopMobileGenericTipBindVersion = 10;

        const handleMobileGenericTipPointer = (event) => {
            if (!isMobileGenericTipViewport()) {
                return;
            }
            const wrap = event.target && event.target.closest
                ? event.target.closest(".tip-wrap:not(.headlines-tip)")
                : null;
            if (wrap && isMobileGenericTipWrap(wrap)) {
                openMobileGenericTip(wrap, event);
                return;
            }
            closeAllMobileGenericTips();
        };

        document.addEventListener("pointerdown", handleMobileGenericTipPointer, true);
        document.addEventListener("touchstart", handleMobileGenericTipPointer, { passive: true, capture: true });
    };

    const bindTabletGenericTips = () => {
        ensureTabletGenericTipRuntimeCss();

        // Rebind on every Streamlit script inject — session may keep window flags
        // after the previous listeners were discarded with the old document scripts.
        if (window.__scoopTabletGenericTipTapHandler) {
            document.removeEventListener(
                "pointerdown",
                window.__scoopTabletGenericTipTapHandler,
                true
            );
            document.removeEventListener(
                "click",
                window.__scoopTabletGenericTipTapHandler,
                true
            );
        }

        const handleTabletGenericTipTap = (event) => {
            if (!isTabletGenericTipViewport()) {
                return;
            }
            // Headlines keep their own centered popup — never hijack those taps.
            if (
                event.target &&
                event.target.closest &&
                event.target.closest(
                    ".tip-wrap.headlines-tip, .hl-tip-count, .hl-tip-cb, .hl-tip-backdrop, .headlines-tip-scroll, .hl-tip-heading"
                )
            ) {
                return;
            }
            ensureTabletGenericTipRuntimeCss();
            const wrap =
                event.target && event.target.closest
                    ? event.target.closest(".tip-wrap:not(.headlines-tip)")
                    : null;
            if (wrap && isMobileGenericTipWrap(wrap)) {
                if (event.type === "pointerdown") {
                    event.preventDefault();
                }
                openTabletGenericTip(wrap, event);
                return;
            }
            if (event.type === "click") {
                closeAllMobileGenericTips();
            }
        };

        window.__scoopTabletGenericTipTapHandler = handleTabletGenericTipTap;
        document.addEventListener("pointerdown", handleTabletGenericTipTap, true);
        document.addEventListener("click", handleTabletGenericTipTap, true);
        window.__scoopTabletGenericTipBindVersion = 9;

        if (!window.__scoopTabletGenericTipCssWatch) {
            window.__scoopTabletGenericTipCssWatch = true;
            window.setInterval(ensureTabletGenericTipRuntimeCss, 1500);
            document.addEventListener("visibilitychange", ensureTabletGenericTipRuntimeCss);
            window.addEventListener("resize", ensureTabletGenericTipRuntimeCss, { passive: true });
        }
    };

    bindMobileGenericTips();
    bindTabletGenericTips();

    const bindTabletHeadlinesTapReliability = () => {
        if (window.__scoopTabletHeadlinesTapBindVersion === 1) {
            return;
        }
        window.__scoopTabletHeadlinesTapBindVersion = 1;

        const handleTabletHeadlinesTap = (event) => {
            if (!usesTabletProHeadlinesPopup()) {
                return;
            }
            const label =
                event.target && event.target.closest
                    ? event.target.closest(".hl-tip-count")
                    : null;
            if (!label) {
                return;
            }
            clearTooltipScrollingHide();
            window.__scoopTabletHeadlinesTappedAt = Date.now();
            const wrap = label.closest(".tip-wrap.headlines-tip");
            const checkbox = wrap?.querySelector(".hl-tip-cb");
            window.requestAnimationFrame(() => {
                if (!checkbox || !checkbox.checked || !wrap) {
                    return;
                }
                scheduleResponsiveHeadlinesPosition(wrap);
                updateHeadlinesHeading(wrap);
            });
        };

        document.addEventListener("pointerdown", handleTabletHeadlinesTap, { capture: true, passive: true });
        document.addEventListener("click", handleTabletHeadlinesTap, { capture: true, passive: true });
    };

    bindTabletHeadlinesTapReliability();

    const repositionVisibleGenericTooltips = () => {
        if (!isTapGenericTipViewport()) {
            resetGenericTooltips();
            return;
        }
        document.querySelectorAll(".tip-wrap.scoop-mobile-tip-open").forEach((wrap) => {
            if (!isMobileGenericTipWrap(wrap)) {
                return;
            }
            scheduleMobileGenericTip(wrap, null);
        });
    };

    window.__scoopGenericTooltipApi = {
        positionGenericTooltip: () => {},
        scheduleGenericTooltipPosition: () => {},
        repositionVisibleGenericTooltips,
    };

    if ((window.__scoopGenericTooltipBindVersion || 0) < 7) {
        window.__scoopGenericTooltipBindVersion = 7;
        resetGenericTooltips();
    }

    if (!window.__scoopTooltipScrollBound) {
        window.__scoopTooltipScrollBound = true;

        window.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
        document.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
        document.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
        document.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
    }

    if (window.__scoopDesktopHeadlinesBindVersion !== 34) {
        window.__scoopDesktopHeadlinesBindVersion = 34;

        if (window.__scoopDesktopHeadlinesMouseLeave) {
            document.removeEventListener("mouseleave", window.__scoopDesktopHeadlinesMouseLeave, true);
        }
        if (window.__scoopDesktopHeadlinesMouseOut) {
            document.removeEventListener("mouseout", window.__scoopDesktopHeadlinesMouseOut, true);
        }
        if (window.__scoopDesktopHeadlinesMouseOver) {
            document.removeEventListener("mouseover", window.__scoopDesktopHeadlinesMouseOver, true);
        }
        if (window.__scoopDesktopHeadlinesPointerMove) {
            document.removeEventListener("pointermove", window.__scoopDesktopHeadlinesPointerMove, true);
        }
        if (window.__scoopDesktopHeadlinesWheel) {
            document.removeEventListener("wheel", window.__scoopDesktopHeadlinesWheel, true);
            document.removeEventListener("wheel", window.__scoopDesktopHeadlinesWheel, false);
        }
        if (window.__scoopDesktopHeadlinesResize) {
            window.removeEventListener("resize", window.__scoopDesktopHeadlinesResize);
        }
        if (window.__scoopDesktopHeadlinesWindowScroll) {
            window.removeEventListener("scroll", window.__scoopDesktopHeadlinesWindowScroll, true);
        }
        if (window.__scoopDesktopHeadlinesDocScroll) {
            document.removeEventListener("scroll", window.__scoopDesktopHeadlinesDocScroll, true);
        }

        window.__scoopDesktopHeadlinesWheel = (event) => {
            window.__scoopDesktopHeadlinesApi?.handleDesktopHeadlinesWheel(event);
        };

        window.__scoopDesktopHeadlinesResize = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            repositionOpenPhoneMobileHeadlines();
            repositionOpenResponsiveHeadlines();
            repositionVisibleGenericTooltips();
        };

        window.__scoopDesktopHeadlinesWindowScroll = (event) => {
            if (isDesktopLayoutViewport()) {
                if (!(event && isInsideDesktopHeadlinesPopup(event.target))) {
                    document
                        .querySelectorAll(
                            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
                        )
                        .forEach((wrap) => {
                            window.__scoopDesktopHeadlinesApi?.hideDesktopHeadlines(wrap);
                        });
                }
                return;
            }
            repositionOpenPhoneMobileHeadlines();
        };

        window.__scoopDesktopHeadlinesDocScroll = (event) => {
            if (isDesktopLayoutViewport()) {
                if (!(event && isInsideDesktopHeadlinesPopup(event.target))) {
                    document
                        .querySelectorAll(
                            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
                        )
                        .forEach((wrap) => {
                            window.__scoopDesktopHeadlinesApi?.hideDesktopHeadlines(wrap);
                        });
                }
                return;
            }
            repositionOpenPhoneMobileHeadlines();
        };

        window.addEventListener("resize", window.__scoopDesktopHeadlinesResize);
        window.addEventListener("scroll", window.__scoopDesktopHeadlinesWindowScroll, {
            passive: true,
            capture: true,
        });
        document.addEventListener("scroll", window.__scoopDesktopHeadlinesDocScroll, {
            passive: true,
            capture: true,
        });
        document.addEventListener("wheel", window.__scoopDesktopHeadlinesWheel, {
            passive: false,
            capture: true,
        });

        if (window.__scoopDesktopHeadlinesLabelClick) {
            document.removeEventListener("click", window.__scoopDesktopHeadlinesLabelClick, true);
        }
        window.__scoopDesktopHeadlinesLabelClick = (event) => {
            if (!isDesktopLayoutViewport()) {
                return;
            }
            const label =
                event.target && event.target.closest
                    ? event.target.closest(".hl-tip-count")
                    : null;
            if (!label) {
                return;
            }
            const wrap = label.closest(".tip-wrap.headlines-tip");
            const checkbox = wrap && wrap.querySelector(".hl-tip-cb");
            if (!checkbox) {
                return;
            }
            if (event.cancelable) {
                event.preventDefault();
            }
            event.stopPropagation();
            checkbox.checked = !checkbox.checked;
            try {
                checkbox.dispatchEvent(new Event("change", { bubbles: true }));
            } catch (e) {}
            const scrollEl =
                document.querySelector('[data-testid="stAppViewContainer"]') ||
                document.scrollingElement ||
                document.documentElement;
            const savedScrollTop = scrollEl.scrollTop;
            window.requestAnimationFrame(() => {
                scrollEl.scrollTop = savedScrollTop;
                window.scrollTo(0, savedScrollTop);
                window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            });
        };
        document.addEventListener("click", window.__scoopDesktopHeadlinesLabelClick, true);
    }

    if (!window.__scoopResponsiveHeadlinesBound) {
        window.__scoopResponsiveHeadlinesBound = true;

        document.addEventListener(
            "change",
            (event) => {
                window.__scoopDesktopHeadlinesApi?.handleHeadlinesCheckboxChange(event);
            },
            true
        );

        window.addEventListener("resize", repositionOpenResponsiveHeadlines, { passive: true });

        const bindResponsiveHeadlinesObserver = () => {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) {
                return false;
            }
            const sidebarHeadlinesObserver = new MutationObserver(repositionOpenResponsiveHeadlines);
            sidebarHeadlinesObserver.observe(sidebar, {
                attributes: true,
                attributeFilter: ["aria-expanded", "class"],
            });
            return true;
        };
        if (!bindResponsiveHeadlinesObserver()) {
            let attempts = 0;
            const retry = window.setInterval(() => {
                attempts += 1;
                if (bindResponsiveHeadlinesObserver() || attempts >= 12) {
                    window.clearInterval(retry);
                }
            }, 250);
        }
    }

})();
"""


_DESKTOP_SIDEBAR_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;

    const expandSidebarIfNeeded = () => {
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) {
            return false;
        }
        if (sidebar.getAttribute("aria-expanded") === "true") {
            return true;
        }
        const expand =
            doc.querySelector('[data-testid="stExpandSidebarButton"] button') ||
            doc.querySelector('[data-testid="stExpandSidebarButton"]') ||
            doc.querySelector('[data-testid="collapsedControl"] button') ||
            doc.querySelector('[data-testid="collapsedControl"]');
        if (expand && typeof expand.click === "function") {
            expand.click();
        }
        // Desktop CSS keeps the split sidebar visible; still force expanded state.
        if (typeof __scoopApplySidebarExpandedState === "function") {
            __scoopApplySidebarExpandedState(true);
        } else {
            sidebar.setAttribute("aria-expanded", "true");
        }
        return sidebar.getAttribute("aria-expanded") === "true";
    };

    const ensureDesktopSidebarOpen = () => {
        if (!layout()?.isDesktopViewport()) {
            layout()?.syncSidebarLayout();
            return;
        }
        doc.documentElement.setAttribute("data-scoop-desktop-layout", "1");
        doc.documentElement.removeAttribute("data-scoop-tab-nav");
        // Compact CSS keys off screener-active; gated consent views often miss it.
        try {
            if (/_Top_10/i.test(appWin.location.pathname || "")) {
                doc.documentElement.setAttribute("data-scoop-screener-active", "1");
            }
        } catch (e) {}
        expandSidebarIfNeeded();
        layout()?.syncSidebarLayout?.();
        // Re-assert after sync — bootstrap races can re-set tab-nav briefly.
        doc.documentElement.removeAttribute("data-scoop-tab-nav");
        expandSidebarIfNeeded();
    };

    if (!appWin.__scoopDesktopSidebarBound) {
        appWin.__scoopDesktopSidebarBound = true;
        doc.addEventListener(
            "click",
            (event) => {
                if (!layout()?.isDesktopViewport()) {
                    return;
                }
                const collapseTarget = event.target.closest(
                    '[data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"]'
                );
                if (collapseTarget) {
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    // Keep desktop sidebar open even if Streamlit tries to collapse.
                    appWin.setTimeout(ensureDesktopSidebarOpen, 0);
                }
            },
            true
        );
    }

    ensureDesktopSidebarOpen();
    [50, 150, 400, 1000, 2000].forEach((delay) => {
        appWin.setTimeout(ensureDesktopSidebarOpen, delay);
    });
})();
"""
)

_COMBINED_PAGE_JS = (
    _TOOLTIP_SCROLL_JS
    + _RESPONSIVE_LAYOUT_CORE_JS
    + _RESPONSIVE_LAYOUT_SYNC_JS
    + _RESPONSIVE_SIDEBAR_JS
    + _ANALYZE_RETURN_NAV_JS
    + _DESKTOP_SIDEBAR_JS
    + _GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS
)

_RESPONSIVE_LAYOUT_SCRIPTS = (
    f"<script>{_RESPONSIVE_LAYOUT_CORE_JS}</script>"
    f"<script>{_RESPONSIVE_LAYOUT_SYNC_JS}</script>"
    f"<script>{_RESPONSIVE_SIDEBAR_JS}</script>"
    f"<script>{_ANALYZE_RETURN_NAV_JS}</script>"
    f"<script>{_DESKTOP_SIDEBAR_JS}</script>"
)


def _inject_responsive_bootstrap_css() -> str:
    import importlib

    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    sidebar_css_json = json.dumps(_tml.RESPONSIVE_SIDEBAR_BOOTSTRAP)
    tab_nav_css_json = json.dumps(_tml.RESPONSIVE_TAB_NAV_BOOTSTRAP)
    chrome_hide_css_json = json.dumps(_tml.EARLY_STREAMLIT_CHROME_HIDE)
    return f"""
<script>
(function() {{
    const sidebarCss = {sidebar_css_json};
    const tabNavCss = {tab_nav_css_json};
    const chromeHideCss = {chrome_hide_css_json};
    const id = "scoop-responsive-sidebar-bootstrap-css";
    const tabId = "scoop-responsive-tab-nav-bootstrap-css";
    const chromeId = "scoop-streamlit-chrome-hide-bootstrap";
    function apply(targetDoc) {{
        if (!targetDoc || !targetDoc.documentElement) {{
            return;
        }}
        const innerW = (targetDoc.defaultView && targetDoc.defaultView.innerWidth) || 0;
        const isMobileTablet = innerW > 0 && innerW <= 1366;
        let el = targetDoc.getElementById(id);
        if (!el) {{
            el = targetDoc.createElement("style");
            el.id = id;
            (targetDoc.head || targetDoc.documentElement).appendChild(el);
        }}
        el.textContent = sidebarCss;
        let tabEl = targetDoc.getElementById(tabId);
        if (!tabEl) {{
            tabEl = targetDoc.createElement("style");
            tabEl.id = tabId;
            (targetDoc.head || targetDoc.documentElement).appendChild(tabEl);
        }}
        tabEl.textContent = tabNavCss;
        let chromeEl = targetDoc.getElementById(chromeId);
        if (!chromeEl) {{
            chromeEl = targetDoc.createElement("style");
            chromeEl.id = chromeId;
            (targetDoc.head || targetDoc.documentElement).appendChild(chromeEl);
        }}
        chromeEl.textContent = chromeHideCss;
        if (isMobileTablet) {{
            targetDoc.documentElement.setAttribute("data-scoop-tab-nav", "1");
        }} else {{
            targetDoc.documentElement.removeAttribute("data-scoop-tab-nav");
        }}
        const hideTabNavSidebarControls = () => {{
            const w = (targetDoc.defaultView && targetDoc.defaultView.innerWidth) || 0;
            const nav = targetDoc.querySelectorAll('[data-testid="stSidebarNav"]');
            nav.forEach((node) => {{
                node.style.setProperty("display", "none", "important");
                node.style.setProperty("visibility", "hidden", "important");
            }});
            if (w > 1366) {{
                const desktopChevrons = targetDoc.querySelectorAll(
                    '[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"]'
                );
                desktopChevrons.forEach((node) => {{
                    node.style.setProperty("display", "none", "important");
                    node.style.setProperty("visibility", "hidden", "important");
                    node.style.setProperty("opacity", "0", "important");
                    node.style.setProperty("pointer-events", "none", "important");
                }});
                return;
            }}
            const sel =
                '[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"], [data-testid="stSidebarBackdrop"], section[data-testid="stSidebar"], [data-testid="stSidebarNav"]';
            targetDoc.querySelectorAll(sel).forEach((node) => {{
                node.style.setProperty("display", "none", "important");
                node.style.setProperty("visibility", "hidden", "important");
                node.style.setProperty("opacity", "0", "important");
                node.style.setProperty("pointer-events", "none", "important");
                node.style.setProperty("width", "0", "important");
                node.style.setProperty("height", "0", "important");
                node.style.setProperty("transform", "translateX(-100%)", "important");
            }});
        }};
        hideTabNavSidebarControls();
        if (!targetDoc.__scoopTabNavSidebarHideBound) {{
            targetDoc.__scoopTabNavSidebarHideBound = true;
            const root = targetDoc.documentElement;
            const observer = new MutationObserver(() => hideTabNavSidebarControls());
            observer.observe(root, {{ childList: true, subtree: true, attributes: true }});
            const appWin = targetDoc.defaultView;
            if (appWin) {{
                appWin.addEventListener("resize", hideTabNavSidebarControls);
            }}
        }}
    }}
    let parentDoc = null;
    try {{
        parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    }} catch (e) {{
        parentDoc = null;
    }}
    const appDoc = parentDoc || document;
    apply(appDoc);
    if (parentDoc && parentDoc !== document) {{
        apply(document);
    }}

    const appWin = appDoc.defaultView || window;
    if (/Analyze/i.test(appWin.location.pathname || "")) {{
        appWin.__scoopAnalyzeSidebarUserOpened = false;
    }}
    const bindAnalyzeClicks = (targetDoc) => {{
        if (!targetDoc || targetDoc.__scoopAnalyzeLinksBound) {{
            return;
        }}
        targetDoc.__scoopAnalyzeLinksBound = true;
        targetDoc.addEventListener(
            "click",
            (event) => {{
                try {{
                    if ((appWin.innerWidth || 0) < 1367) {{
                        return;
                    }}
                    // Desktop Cloud: do not hijack Analyze here. st.html often
                    // runs in a srcdoc frame; preventDefault + location.assign
                    // swallows the click. desktop_screener_tips owns desktop nav.
                    return;
                }} catch (e) {{}}
            }},
            true
        );
    }};
    bindAnalyzeClicks(appDoc);
    if (document !== appDoc) {{
        bindAnalyzeClicks(document);
    }}
}})();
</script>
"""


BOOTSTRAP_INSTALLED_KEY = "_scoop_responsive_bootstrap_installed"
BOOTSTRAP_SCRIPT_VERSION = 12
TOOLTIP_INSTALLED_KEY = "_scoop_tooltip_scroll_installed"
TOOLTIP_SCRIPT_VERSION = 75
SIDEBAR_HANDLER_INSTALLED_KEY = "_scoop_responsive_sidebar_handler_v3"


def _responsive_bootstrap_markup() -> str:
    """Bootstrap CSS/JS once per session (shared across pages)."""
    # Always re-emit chrome-hide CSS so multipage nav / chevrons cannot flash after navigation.
    chrome_style = (
        f"<style id='scoop-streamlit-chrome-hide'>{EARLY_STREAMLIT_CHROME_HIDE}</style>"
    )
    if st.session_state.get(BOOTSTRAP_INSTALLED_KEY) == BOOTSTRAP_SCRIPT_VERSION:
        return chrome_style
    st.session_state[BOOTSTRAP_INSTALLED_KEY] = BOOTSTRAP_SCRIPT_VERSION
    return (
        chrome_style
        + f"<style id='scoop-responsive-generic-tooltip-css'>{_RESPONSIVE_GENERIC_TOOLTIP_CSS}</style>"
        + _inject_responsive_bootstrap_css()
        + f"<script>{_RESPONSIVE_LAYOUT_CORE_JS}</script>"
        + f"<script>{_RESPONSIVE_LAYOUT_SYNC_JS}</script>"
    )


def _inject_name_tooltip_override() -> None:
    """Inject generic tooltip override + tablet final open/beside CSS after page styles."""
    import importlib

    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    # st.html keeps <style> intact and runs late enough to beat screener page CSS.
    st.html(
        f"<style id='scoop-name-value-tooltip-override-css'>{_tml.RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS}</style>"
        f"<style id='scoop-phone-generic-tip-final-css'>{_tml.PHONE_GENERIC_TIP_FINAL_CSS}</style>"
        f"<style id='scoop-tablet-generic-tip-final-css'>{_tml.TABLET_GENERIC_TIP_FINAL_CSS}</style>",
        unsafe_allow_javascript=True,
    )


def _inject_tablet_analyze_link_css() -> None:
    """Tablet Analyze row: blue underlined link; reload CSS module so edits always apply."""
    import importlib

    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    # Use st.html — st.markdown strips/mangles <style> and can dump CSS onto the page.
    st.html(
        f"<style id='scoop-tablet-analyze-link-css'>{_tml.TABLET_ANALYZE_LINK_CSS}</style>"
        f"<style id='scoop-phone-analyze-mobile-tip-css'>{_tml.PHONE_ANALYZE_MOBILE_TIP_CSS}</style>"
        f"<style id='scoop-mobile-tablet-analyze-link-final-css'>{_tml._MOBILE_TABLET_ANALYZE_LINK_FINAL}</style>",
        unsafe_allow_javascript=True,
    )


def _inject_tablet_hl_heading_color_css() -> None:
    """Tablet/mobile Headlines title color — reload CSS module so edits always apply."""
    import importlib

    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    css = _tml.MOBILE_TABLET_HL_HEADING_COLOR_CSS
    st.html(
        f"<style id='scoop-mobile-tablet-hl-heading-color'>{css}</style>"
        f"<style id='scoop-tablet-hl-heading-blue-final-v45'>{css}</style>",
        unsafe_allow_javascript=True,
    )


def _inject_desktop_headlines_css() -> None:
    """Always inject desktop Headlines count styling (survives tooltip handler early return)."""
    # st.html keeps complex :has() / attribute selectors; st.markdown can truncate them.
    st.html(
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>"
        f"<style id='scoop-desktop-tooltip-type-css'>{_DESKTOP_TOOLTIP_TYPE_CSS}</style>",
        unsafe_allow_javascript=True,
    )


def _inject_ipad_mini_headlines_css() -> None:
    """Always inject iPad Mini Headlines popup styling after page CSS."""
    st.markdown(
        f"<style id='scoop-ipad-mini-headlines-css'>{_IPAD_MINI_HEADLINES_CSS}</style>"
        f"<style id='scoop-ipad-mini-popup-clamp-css'>{IPAD_MINI_POPUP_CLAMP_CSS}</style>",
        unsafe_allow_html=True,
    )


def _inject_mobile_phone_headlines_css() -> None:
    """Always inject phone mobile Headlines top-panel styling after page CSS."""
    st.markdown(
        f"<style id='scoop-mobile-phone-headlines-fixed-css'>{_MOBILE_PHONE_HEADLINES_FIXED_CSS}</style>",
        unsafe_allow_html=True,
    )


def _ensure_generic_tooltip_mobile_assets() -> None:
    """Inject centered generic tooltip CSS/JS after page styles on mobile/tablet."""
    if st.session_state.get(GENERIC_TOOLTIP_CSS_KEY) != GENERIC_TOOLTIP_CSS_VERSION:
        st.markdown(
            f"<style id='scoop-responsive-generic-tooltip-css'>{_RESPONSIVE_GENERIC_TOOLTIP_CSS}</style>",
            unsafe_allow_html=True,
        )
        st.session_state[GENERIC_TOOLTIP_CSS_KEY] = GENERIC_TOOLTIP_CSS_VERSION
    st.components.v1.html(f"<script>{_GENERIC_TOOLTIP_MOBILE_JS}</script>", height=0)


def install_page_layout_resync() -> None:
    """Re-sync sidebar width and header clearance after Streamlit page navigation."""
    st.html(f"<script>{_PAGE_NAV_LAYOUT_RESYNC_JS}</script>", unsafe_allow_javascript=True)


def inject_desktop_sidebar_nav_market() -> None:
    """Inject global per-page sidebar CSS (nav containers, top compact, brand spacing)."""
    st.html(
        f"<style id='scoop-desktop-sidebar-nav-market-css'>{DESKTOP_SIDEBAR_NAV_MARKET}</style>"
        f"<style id='scoop-desktop-screener-gating-layout-css'>{DESKTOP_SCREENER_GATING_LAYOUT}</style>"
        f"<style id='scoop-responsive-screener-top-compact-css-v3'>{RESPONSIVE_SCREENER_TOP_COMPACT}</style>"
        f"<style id='scoop-responsive-terms-top-compact-css'>{RESPONSIVE_TERMS_TOP_COMPACT}</style>"
        f"<style id='scoop-mobile-consent-terms-main-view-css-v3'>{MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS}</style>"
        f"<style id='scoop-desktop-terms-top-compact-css'>{DESKTOP_TERMS_TOP_COMPACT}</style>"
        f"<style id='scoop-responsive-sidebar-brand-toggle-buffer-css'>{RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER}</style>"
        f"<style id='scoop-desktop-sidebar-brand-toggle-buffer-css'>{DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER}</style>"
        f"<style id='scoop-desktop-sidebar-logo-css'>{DESKTOP_SIDEBAR_LOGO_RULES}</style>",
        unsafe_allow_javascript=True,
    )
    # Separate inject so Streamlit cannot drop this block when co-bundled.
    # Cloud: copy CSS onto the parent doc and mark both html roots.
    _desktop_screener_css_json = json.dumps(DESKTOP_SCREENER_TOP_COMPACT)
    st.html(
        f"<style id='scoop-desktop-screener-top-compact-css'>{DESKTOP_SCREENER_TOP_COMPACT}</style>"
        f"""<script>(() => {{ try {{
  const css = {_desktop_screener_css_json};
  const id = "scoop-desktop-screener-top-compact-css";
  function applyCss(doc) {{
    if (!doc || !doc.documentElement) return;
    let el = doc.getElementById(id);
    if (!el) {{
      el = doc.createElement("style");
      el.id = id;
      (doc.head || doc.documentElement).appendChild(el);
    }}
    if (el.textContent !== css) el.textContent = css;
  }}
  function mark(doc) {{
    if (!doc || !doc.documentElement) return;
    const win = doc.defaultView || window;
    const path = ((win.location && win.location.pathname) || "") + ((window.location && window.location.pathname) || "");
    if (/_Top_10/i.test(path)) {{
      doc.documentElement.setAttribute("data-scoop-screener-active", "1");
    }}
  }}
  applyCss(document);
  mark(document);
  try {{
    if (window.parent && window.parent.document) {{
      applyCss(window.parent.document);
      mark(window.parent.document);
    }}
  }} catch (e) {{}}
}} catch (e) {{}} }})();</script>""",
        unsafe_allow_javascript=True,
    )
    _inject_mobile_tablet_index_banner_parent_css()


def _inject_mobile_tablet_index_banner_parent_css() -> None:
    """Ship index-banner CSS in the page (Cloud) and copy it onto parent docs."""
    css = MOBILE_TABLET_INDEX_BANNER_CSS
    st.markdown(
        f'<style id="scoop-mobile-tablet-index-banner-page-css">{css}</style>',
        unsafe_allow_html=True,
    )
    css_json = json.dumps(css)
    st.html(
        f"""<script>
(function() {{
  try {{
    const css = {css_json};
    const id = "scoop-mobile-tablet-index-banner-parent-css";
    function apply(doc) {{
      if (!doc || !doc.documentElement) return;
      let el = doc.getElementById(id);
      if (!el) {{
        el = doc.createElement("style");
        el.id = id;
        (doc.head || doc.documentElement).appendChild(el);
      }}
      if (el.textContent !== css) el.textContent = css;
    }}
    apply(document);
    try {{
      if (window.parent && window.parent.document) apply(window.parent.document);
    }} catch (e) {{}}
  }} catch (e) {{}}
}})();
</script>""",
        unsafe_allow_javascript=True,
    )


def inject_desktop_tablet_disclaimer_flow() -> None:
    """Flow disclaimer below content on tablet/desktop (no fixed overlay bar)."""
    st.html(
        f"<style id='scoop-desktop-tablet-disclaimer-flow-css'>{DESKTOP_TABLET_DISCLAIMER_FLOW}</style>",
        unsafe_allow_javascript=True,
    )


def inject_desktop_analyze_top_compact() -> None:
    """Tighten Analyze deep-dive top spacing on desktop (padding, js_eval gaps, hr lines, card polish)."""
    from analyze_page import analyze_screener_snapshot_key, is_crypto_analyze_context, query_param_ticker

    source = "".join(ch for ch in str(analyze_screener_snapshot_key() or "") if ch.isalnum())
    if not source and is_crypto_analyze_context(None, query_param_ticker()):
        source = "CRYPTO"
    source_js = (
        f'root.setAttribute("data-scoop-analyze-source","{source}");'
        if source
        else 'root.removeAttribute("data-scoop-analyze-source");'
    )
    st.html(
        f"<style id='scoop-desktop-analyze-top-compact-css'>{DESKTOP_ANALYZE_TOP_COMPACT}</style>"
        f"<style id='scoop-responsive-analyze-top-compact-css'>{RESPONSIVE_ANALYZE_TOP_COMPACT}</style>"
        f"<style id='scoop-crypto-analyze-responsive-metrics-css'>{CRYPTO_ANALYZE_RESPONSIVE_METRICS_CSS}</style>"
        + "<script>(function(){try{"
        + "var doc=(window.parent&&window.parent!==window&&window.parent.document)?window.parent.document:document;"
        + "var win=doc.defaultView||window;"
        + "var root=doc.documentElement;"
        + 'root.setAttribute("data-scoop-analyze-active","1");'
        + source_js
        + "if(win.__scoopDesktopAnalyzeMoodV===3)return;"
        + "win.__scoopDesktopAnalyzeMoodV=3;"
        + "var size=function(){"
        + "if((win.innerWidth||0)<1367)return;"
        + "if(root.getAttribute('data-scoop-analyze-active')!=='1')return;"
        + "var feed=doc.querySelector('.mood-feed');if(!feed)return;"
        + "var footer=doc.querySelector('.disclaimer-footer');"
        + "var row=feed.closest('[data-testid=\"stHorizontalBlock\"]');"
        + "var top=feed.getBoundingClientRect().top;"
        + "var bottom=top+480;"
        + "if(row){var rb=row.getBoundingClientRect().bottom;if(rb>top)bottom=rb-8;}"
        + "if(footer){var ft=footer.getBoundingClientRect().top;if(ft>top)bottom=Math.min(bottom,ft-12);}"
        + "var h=Math.max(320,Math.round(bottom-top));"
        + "feed.style.setProperty('height',h+'px','important');"
        + "feed.style.setProperty('max-height',h+'px','important');"
        + "};"
        + "var tick=function(){try{size();}catch(e){}};"
        + "tick();"
        + "win.requestAnimationFrame(tick);"
        + "win.addEventListener('resize',tick);"
        + "if(win.MutationObserver){new MutationObserver(tick).observe(doc.body,{childList:true,subtree:true});}"
        + "}catch(e){}})();</script>",
        unsafe_allow_javascript=True,
    )


def inject_streamlit_chrome_hide() -> None:
    """Hide default Streamlit multipage nav / slideout chevrons (early + last wins)."""
    st.html(
        f'<style id="scoop-streamlit-chrome-hide">{EARLY_STREAMLIT_CHROME_HIDE}</style>',
        unsafe_allow_javascript=True,
    )


def install_responsive_layout_bootstrap() -> None:
    """Early CSS + layout sync so mobile/tablet first paint uses overlay sidebar."""
    inject_streamlit_chrome_hide()
    markup = _responsive_bootstrap_markup()
    if markup:
        st.html(markup, unsafe_allow_javascript=True)
    install_page_layout_resync()
    inject_streamlit_chrome_hide()


def install_responsive_sidebar_handler() -> None:
    """Responsive sidebar close (tablet) + always-open sidebar (desktop)."""
    if not st.session_state.get(SIDEBAR_HANDLER_INSTALLED_KEY):
        st.session_state[SIDEBAR_HANDLER_INSTALLED_KEY] = True
        st.html(
            _responsive_bootstrap_markup()
            + f"<style id='scoop-desktop-sidebar-layout-css'>{DESKTOP_SIDEBAR_LAYOUT}</style>"
            + f"<style id='scoop-desktop-zoom-layout-css'>{DESKTOP_ZOOM_LAYOUT}</style>"
            + f"<style id='scoop-sidebar-nav-compact-css'>{SIDEBAR_NAV_COMPACT}</style>"
            + _RESPONSIVE_LAYOUT_SCRIPTS,
            unsafe_allow_javascript=True,
        )
    inject_desktop_sidebar_nav_market()
    install_page_layout_resync()


def _inject_js_source(js: str, *, key: str) -> None:
    """Inject JS in small <script> tags inside one st.html call.

    Streamlit silently drops oversized inline <script> blocks (~130KB combined
    tip bundle). Multiple separate st.html() calls can also reorder, so chunk
    pushes and the join must stay in a single markup string.
    """
    chunk_size = 8000
    chunks = [js[i : i + chunk_size] for i in range(0, len(js), chunk_size)]
    key_json = json.dumps(key)
    script_id_json = json.dumps("scoop-js-" + key)
    parts = [
        f"<script>window.__scoopJsChunks=window.__scoopJsChunks||{{}};window.__scoopJsChunks[{key_json}]=[];</script>"
    ]
    for chunk in chunks:
        parts.append(
            f"<script>window.__scoopJsChunks[{key_json}].push({json.dumps(chunk)});</script>"
        )
    parts.append(
        f"""<script>
(function() {{
  const parts = window.__scoopJsChunks && window.__scoopJsChunks[{key_json}];
  if (!parts || parts.length !== {len(chunks)}) {{
    return;
  }}
  const existing = document.getElementById({script_id_json});
  if (existing) {{
    existing.remove();
  }}
  const s = document.createElement("script");
  s.id = {script_id_json};
  s.textContent = parts.join("");
  document.documentElement.appendChild(s);
}})();
</script>"""
    )
    st.html("".join(parts), unsafe_allow_javascript=True)


# Compact phone-only generic tip binder. Combined page JS is often dropped on mobile;
# this keeps company/name tips opening viewport-centered. Headlines unchanged.
_PHONE_GENERIC_TIP_STANDALONE_JS = r"""
(() => {
    const MAX = 743;
    const GAP = 20;
    const PAD = 8;
    const isPhone = () => window.innerWidth <= MAX;
    const isHeadlinesTarget = (node) =>
        !!(node && node.closest && node.closest(
            ".tip-wrap.headlines-tip, .hl-tip-count, .hl-tip-cb, .hl-tip-backdrop, .headlines-tip-scroll, .hl-tip-heading"
        ));
    const isGeneric = (wrap) =>
        !!wrap &&
        !wrap.classList.contains("headlines-tip") &&
        !wrap.closest(".tip-wrap.headlines-tip") &&
        !wrap.closest("thead");
    const clearTipStyles = (tip) => {
        if (!tip) return;
        [
            "position", "left", "top", "right", "bottom", "transform", "width",
            "max-width", "min-width", "max-height", "overflow-y", "overflow-x",
            "visibility", "opacity", "pointer-events", "display", "z-index",
            "white-space", "word-break", "overflow-wrap", "box-sizing", "text-align",
            "--scoop-mobile-tip-left", "--scoop-mobile-tip-top",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const closeAll = () => {
        document.querySelectorAll(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open").forEach((wrap) => {
            wrap.classList.remove("scoop-mobile-tip-open");
            clearTipStyles(wrap.querySelector(":scope > .tip-text"));
        });
    };
    const closeHeadlines = () => {
        if (!isPhone()) return;
        document
            .querySelectorAll(".tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((cb) => {
                cb.checked = false;
                const wrap = cb.closest(".tip-wrap.headlines-tip");
                if (!wrap) return;
                wrap.classList.remove("hl-tip-desktop-open");
                const tip = wrap.querySelector(":scope > .tip-text");
                if (!tip) return;
                [
                    "--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width",
                    "--hl-fixed-max-height", "--hl-fixed-height",
                    "height", "position", "left", "top", "right", "bottom", "transform",
                    "width", "max-width", "max-height", "visibility", "opacity",
                    "pointer-events", "display", "flex-direction", "overflow",
                ].forEach((p) => tip.style.removeProperty(p));
            });
    };
    const RUNTIME_CSS = `
@media (max-width: 743px) {
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text {
    visibility: hidden !important; opacity: 0 !important; pointer-events: none !important;
    left: -10000px !important; right: auto !important; transform: none !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
    position: fixed !important;
    left: var(--scoop-mobile-tip-left, -10000px) !important;
    top: var(--scoop-mobile-tip-top, -10000px) !important;
    right: auto !important; bottom: auto !important; transform: none !important; margin: 0 !important;
    width: 50vw !important;
    max-width: 50vw !important;
    font-size: 1.08rem !important;
    line-height: 1.42 !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text {
    visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;
    display: block !important; position: fixed !important;
    left: var(--scoop-mobile-tip-left, 8px) !important;
    top: var(--scoop-mobile-tip-top, 8px) !important;
    right: auto !important; bottom: auto !important; transform: none !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text > .scoop-tip-title {
    display: block !important; font-weight: 700 !important; font-size: 1.12rem !important;
    line-height: 1.25 !important; margin: 0 0 0.45rem 0 !important; padding: 0 0 0.4rem 0 !important;
    border-bottom: 1px solid rgba(148, 163, 184, 0.45) !important; color: #f8fafc !important;
  }
}`;
    const ensureCss = () => {
        if (!isPhone()) return;
        const id = "scoop-phone-generic-tip-runtime-css";
        let el = document.getElementById(id);
        if (!el) {
            el = document.createElement("style");
            el.id = id;
        }
        if (el.textContent !== RUNTIME_CSS) el.textContent = RUNTIME_CSS;
        document.documentElement.appendChild(el);
    };
    const position = (wrap, clientY) => {
        if (!isPhone() || !isGeneric(wrap) || !wrap.classList.contains("scoop-mobile-tip-open")) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        const tipWidth = Math.round(window.innerWidth * 0.5);
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", tipWidth + "px", "important");
        tip.style.setProperty("max-width", tipWidth + "px", "important");
        tip.style.setProperty("box-sizing", "border-box", "important");
        tip.style.setProperty("white-space", "normal", "important");
        tip.style.setProperty("word-break", "break-word", "important");
        tip.style.setProperty("overflow-wrap", "anywhere", "important");
        tip.style.setProperty("overflow-x", "hidden", "important");
        tip.style.setProperty("overflow-y", "auto", "important");
        tip.style.setProperty("visibility", "hidden", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("display", "block", "important");
        tip.style.setProperty("left", "-9999px", "important");
        tip.style.setProperty("top", "0", "important");
        let tipHeight = tip.offsetHeight || 120;
        tipHeight = Math.min(tipHeight, Math.max(80, window.innerHeight - PAD * 2));
        const anchorY = typeof clientY === "number" ? clientY : wrap.getBoundingClientRect().top;
        let top = anchorY - tipHeight - GAP;
        if (top < PAD) top = Math.min(anchorY + GAP, window.innerHeight - PAD - tipHeight);
        top = Math.max(PAD, Math.min(top, window.innerHeight - PAD - tipHeight));
        const width = tip.getBoundingClientRect().width || tipWidth;
        const left = Math.max(PAD, Math.min((window.innerWidth - width) / 2, window.innerWidth - width - PAD));
        tip.style.setProperty("--scoop-mobile-tip-left", Math.round(left) + "px", "important");
        tip.style.setProperty("--scoop-mobile-tip-top", Math.round(top) + "px", "important");
        tip.style.setProperty("left", Math.round(left) + "px", "important");
        tip.style.setProperty("top", Math.round(top) + "px", "important");
        tip.style.setProperty("max-height", Math.round(window.innerHeight - top - PAD) + "px", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("z-index", "100002", "important");
    };
    const OPEN_GRACE_MS = 400;
    const open = (wrap, clientY) => {
        if (!isPhone() || !isGeneric(wrap)) return;
        ensureCss();
        closeHeadlines();
        closeAll();
        wrap.classList.add("scoop-mobile-tip-open");
        window.__scoopPhoneGenericTipOpenedAt = Date.now();
        document.documentElement.classList.remove("scoop-tooltip-scrolling");
        document.body.classList.remove("scoop-tooltip-scrolling");
        (function ensureTitle() {
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) return;
            let title = tip.querySelector(":scope > .scoop-tip-title");
            if (!title) {
                title = document.createElement("div");
                title.className = "scoop-tip-title";
                tip.insertBefore(title, tip.firstChild);
            }
            const td = wrap.closest("td[data-label]");
            let name = td ? String(td.getAttribute("data-label") || "").trim() : "";
            if (!name) {
                let t = "";
                wrap.childNodes.forEach((node) => {
                    if (node.nodeType === Node.TEXT_NODE) t += node.textContent || "";
                });
                name = t.replace(/\s+/g, " ").trim();
            }
            title.textContent = name;
            title.style.display = name ? "block" : "none";
        })();
        position(wrap, clientY);
        requestAnimationFrame(() => position(wrap, clientY));
    };
    const onTap = (event) => {
        if (!isPhone() || !event || !event.target || !event.target.closest) return;
        // Leave Headlines entirely to their own handlers.
        if (isHeadlinesTarget(event.target)) return;
        if (event.type === "pointerdown" && event.pointerType === "mouse" && event.button !== 0) {
            return;
        }
        // Prefer pointerdown; click is a fallback when pointerdown was skipped.
        if (event.type === "click" && event.pointerType) return;
        ensureCss();
        const t = event.target;
        // Keep taps/scroll gestures inside an already-open tip content intact.
        const openWrap = t.closest(".tip-wrap.scoop-mobile-tip-open:not(.headlines-tip)");
        if (openWrap && t.closest(".tip-text")) return;

        const wrap = t.closest(".tip-wrap:not(.headlines-tip)");
        if (wrap) {
            closeHeadlines();
            if (!isGeneric(wrap)) {
                closeAll();
                return;
            }
            if (event.type === "pointerdown" && event.cancelable) event.preventDefault();
            // Same tip trigger again → close; other tip → switch.
            if (wrap.classList.contains("scoop-mobile-tip-open")) {
                closeAll();
                return;
            }
            const y = typeof event.clientY === "number" ? event.clientY : null;
            open(wrap, y);
            return;
        }
        // Dead space: dismiss any open generic tip.
        closeAll();
    };
    const isScrollInsideOpenPopup = (event) => {
        const t = event && event.target;
        if (!t || !t.closest) return false;
        return !!(
            t.closest(".tip-wrap.scoop-mobile-tip-open:not(.headlines-tip)") &&
            t.closest(".tip-text")
        );
    };
    const onScrollDismiss = (event) => {
        if (!isPhone()) return;
        if (isScrollInsideOpenPopup(event)) return;
        const openedAt = window.__scoopPhoneGenericTipOpenedAt || 0;
        if (Date.now() - openedAt < OPEN_GRACE_MS) return;
        if (!document.querySelector(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open")) {
            return;
        }
        closeAll();
    };
    if (window.__scoopPhoneGenericTipTapHandler) {
        document.removeEventListener("pointerdown", window.__scoopPhoneGenericTipTapHandler, true);
        document.removeEventListener("click", window.__scoopPhoneGenericTipTapHandler, true);
    }
    if (window.__scoopPhoneGenericTipScrollHandler) {
        window.removeEventListener("scroll", window.__scoopPhoneGenericTipScrollHandler, true);
        document.removeEventListener("scroll", window.__scoopPhoneGenericTipScrollHandler, true);
        document.removeEventListener("wheel", window.__scoopPhoneGenericTipScrollHandler, true);
        document.removeEventListener("touchmove", window.__scoopPhoneGenericTipScrollHandler, true);
    }
    window.__scoopPhoneGenericTipTapHandler = onTap;
    window.__scoopPhoneGenericTipScrollHandler = onScrollDismiss;
    document.addEventListener("pointerdown", onTap, true);
    document.addEventListener("click", onTap, true);
    window.addEventListener("scroll", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("scroll", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("wheel", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("touchmove", onScrollDismiss, { passive: true, capture: true });
    ensureCss();
    if (!window.__scoopPhoneGenericTipCssWatch) {
        window.__scoopPhoneGenericTipCssWatch = true;
        setInterval(ensureCss, 1500);
        window.addEventListener("resize", ensureCss, { passive: true });
    }
    window.__scoopPhoneGenericTipStandalone = 6;
})();
"""

# Compact tablet-only generic tip binder. Kept small so Streamlit will not drop it
# when the large combined bundle fails to load (NASDAQ/NYSE after disclaimer agree).
_TABLET_GENERIC_TIP_STANDALONE_JS = r"""
(() => {
    // iPad Mini (744–768) + tablet / iPad Pro-class (769–1366). Not phone. Not Headlines.
    const MIN = 744;
    const MAX = 1366;
    const GAP = 12;
    const PAD = 12;
    const isTablet = () => {
        const w = window.innerWidth;
        return w >= MIN && w <= MAX;
    };
    // Headlines use their own centered --hl-fixed-* path. Never treat them as generic tips.
    const isHeadlinesTarget = (node) =>
        !!(node && node.closest && node.closest(
            ".tip-wrap.headlines-tip, .hl-tip-count, .hl-tip-cb, .hl-tip-backdrop, .headlines-tip-scroll, .hl-tip-heading"
        ));
    const isGeneric = (wrap) =>
        !!wrap &&
        !wrap.classList.contains("headlines-tip") &&
        !wrap.closest(".tip-wrap.headlines-tip");
    const clearTipStyles = (tip) => {
        [
            "position", "left", "top", "right", "bottom", "transform", "width",
            "max-width", "min-width", "max-height", "overflow-y", "overflow-x",
            "visibility", "opacity", "pointer-events", "display", "z-index",
            "white-space", "word-break", "overflow-wrap", "box-sizing", "text-align",
            "--scoop-tablet-tip-left", "--scoop-tablet-tip-top", "--scoop-tablet-tip-width",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const closeAll = () => {
        document.querySelectorAll(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open").forEach((wrap) => {
            wrap.classList.remove("scoop-mobile-tip-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (tip) clearTipStyles(tip);
        });
    };
    const RUNTIME_CSS = `
@media (min-width: 744px) and (max-width: 1366px) {
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text {
    visibility: hidden !important; opacity: 0 !important; pointer-events: none !important;
    right: auto !important; left: -10000px !important; transform: none !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
    position: fixed !important;
    left: var(--scoop-tablet-tip-left, -10000px) !important;
    top: var(--scoop-tablet-tip-top, -10000px) !important;
    right: auto !important; bottom: auto !important; transform: none !important; margin: 0 !important;
    width: var(--scoop-tablet-tip-width, 50vw) !important;
    min-width: 0 !important; max-width: 50vw !important;
    font-size: 1.08rem !important; line-height: 1.42 !important;
    white-space: normal !important; word-break: break-word !important; overflow-wrap: anywhere !important;
    box-sizing: border-box !important; text-align: left !important;
    overflow-x: hidden !important; overflow-y: auto !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text {
    visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;
    display: block !important; position: fixed !important;
    left: var(--scoop-tablet-tip-left, -10000px) !important;
    top: var(--scoop-tablet-tip-top, -10000px) !important;
    right: auto !important; bottom: auto !important; transform: none !important;
    white-space: normal !important; word-break: break-word !important; overflow-wrap: anywhere !important;
    z-index: 100002 !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text > .scoop-tip-title {
    display: block !important; font-weight: 700 !important; font-size: 1.12rem !important;
    line-height: 1.25 !important; margin: 0 0 0.45rem 0 !important; padding: 0 0 0.4rem 0 !important;
    border-bottom: 1px solid rgba(148, 163, 184, 0.45) !important; color: #f8fafc !important;
  }
}`;
    const ensureCss = () => {
        if (!isTablet()) return;
        const id = "scoop-tablet-generic-tip-runtime-css";
        let el = document.getElementById(id);
        if (!el) {
            el = document.createElement("style");
            el.id = id;
        }
        if (el.textContent !== RUNTIME_CSS) el.textContent = RUNTIME_CSS;
        document.documentElement.appendChild(el);
    };
    const applyWrapBox = (tip, width) => {
        tip.style.setProperty("box-sizing", "border-box", "important");
        tip.style.setProperty("white-space", "normal", "important");
        tip.style.setProperty("word-break", "break-word", "important");
        tip.style.setProperty("overflow-wrap", "anywhere", "important");
        tip.style.setProperty("min-width", "0", "important");
        tip.style.setProperty("max-width", width + "px", "important");
        tip.style.setProperty("width", width + "px", "important");
        tip.style.setProperty("overflow-x", "hidden", "important");
        tip.style.setProperty("overflow-y", "auto", "important");
        tip.style.setProperty("text-align", "left", "important");
    };
    const measureHeight = (tip, width) => {
        tip.style.setProperty("visibility", "hidden", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("left", "-9999px", "important");
        tip.style.setProperty("top", "0", "important");
        applyWrapBox(tip, width);
        const h = tip.offsetHeight || 120;
        tip.style.removeProperty("visibility");
        tip.style.removeProperty("opacity");
        tip.style.removeProperty("left");
        tip.style.removeProperty("top");
        return h;
    };
    const position = (wrap) => {
        if (!isTablet() || !isGeneric(wrap) || !wrap.classList.contains("scoop-mobile-tip-open")) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        const wrapRect = wrap.getBoundingClientRect();
        const card = wrap.closest("tr") || wrap.closest(".full-results-wrap") || wrap;
        const cardRect = card.getBoundingClientRect();
        const viewLeft = PAD;
        const viewRight = window.innerWidth - PAD;
        const viewTop = PAD;
        const viewBottom = window.innerHeight - PAD;
        const cardLeft = Math.max(viewLeft, cardRect.left + PAD);
        const cardRight = Math.min(viewRight, cardRect.right - PAD);
        const preferLeft = !!wrap.closest(".fr-val") || wrapRect.left > (cardLeft + cardRight) / 2;

        // Free lane beside the trigger — tip is centered in that lane.
        let laneLeft = cardLeft;
        let laneRight = cardRight;
        if (preferLeft) {
            laneRight = Math.max(laneLeft + 140, wrapRect.left - GAP);
        } else {
            laneLeft = Math.min(laneRight - 140, wrapRect.right + GAP);
        }
        const laneW = Math.max(140, laneRight - laneLeft);
        let tipWidth = Math.round(window.innerWidth * 0.5);
        tipWidth = Math.max(120, Math.min(tipWidth, viewRight - viewLeft));

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        applyWrapBox(tip, tipWidth);
        tip.style.setProperty("--scoop-tablet-tip-width", tipWidth + "px", "important");

        let tipHeight = measureHeight(tip, tipWidth);
        tipHeight = Math.min(tipHeight, Math.min(280, viewBottom - viewTop));
        applyWrapBox(tip, tipWidth);
        tip.style.setProperty("max-height", Math.round(tipHeight) + "px", "important");
        // Remeasure after max-height so vertical centering uses the painted box.
        tipHeight = Math.min(tip.getBoundingClientRect().height || tipHeight, tipHeight);

        let left = laneLeft + Math.max(0, (laneW - tipWidth) / 2);
        left = Math.max(viewLeft, Math.min(left, viewRight - tipWidth));
        if (preferLeft && left + tipWidth > wrapRect.left - 4) {
            left = Math.max(viewLeft, wrapRect.left - GAP - tipWidth);
        }
        if (!preferLeft && left < wrapRect.right + 4) {
            left = Math.min(viewRight - tipWidth, wrapRect.right + GAP);
        }
        left = Math.max(viewLeft, Math.min(left, viewRight - tipWidth));

        const anchorMidY = wrapRect.top + wrapRect.height / 2;
        let top = anchorMidY - tipHeight / 2;
        const cardTop = Math.max(viewTop, cardRect.top + PAD * 0.5);
        const cardBottom = Math.min(viewBottom, cardRect.bottom - PAD * 0.5);
        if (top < cardTop) top = cardTop;
        if (top + tipHeight > cardBottom) top = Math.max(cardTop, cardBottom - tipHeight);
        top = Math.max(viewTop, Math.min(top, viewBottom - tipHeight));

        tip.style.setProperty("--scoop-tablet-tip-left", Math.round(left) + "px", "important");
        tip.style.setProperty("--scoop-tablet-tip-top", Math.round(top) + "px", "important");
        tip.style.setProperty("left", Math.round(left) + "px", "important");
        tip.style.setProperty("top", Math.round(top) + "px", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("display", "block", "important");
        tip.style.setProperty("z-index", "100002", "important");
    };
    const open = (wrap) => {
        if (!isTablet() || !isGeneric(wrap)) return;
        ensureCss();
        if (typeof window.__scoopCloseTabletTips === "function") {
            window.__scoopCloseTabletTips({ headlines: true, generics: false });
        }
        closeAll();
        wrap.classList.add("scoop-mobile-tip-open");
        document.documentElement.classList.remove("scoop-tooltip-scrolling");
        document.body.classList.remove("scoop-tooltip-scrolling");
        (function ensureTitle() {
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) return;
            let title = tip.querySelector(":scope > .scoop-tip-title");
            if (!title) {
                title = document.createElement("div");
                title.className = "scoop-tip-title";
                tip.insertBefore(title, tip.firstChild);
            }
            const td = wrap.closest("td[data-label]");
            let name = td ? String(td.getAttribute("data-label") || "").trim() : "";
            if (!name) {
                let t = "";
                wrap.childNodes.forEach((node) => {
                    if (node.nodeType === Node.TEXT_NODE) t += node.textContent || "";
                });
                name = t.replace(/\s+/g, " ").trim();
            }
            title.textContent = name;
            title.style.display = name ? "block" : "none";
        })();
        position(wrap);
        requestAnimationFrame(() => position(wrap));
    };
    const onTap = (event) => {
        if (!isTablet()) return;
        // Leave Headlines taps/clicks entirely to the headlines handlers (stay centered).
        if (isHeadlinesTarget(event.target)) return;
        ensureCss();
        const wrap = event.target && event.target.closest
            ? event.target.closest(".tip-wrap:not(.headlines-tip)")
            : null;
        if (wrap && isGeneric(wrap)) {
            if (event.type === "pointerdown") event.preventDefault();
            open(wrap);
            return;
        }
        if (event.type === "click") {
            if (typeof window.__scoopCloseTabletTips === "function") {
                window.__scoopCloseTabletTips({ headlines: true, generics: true });
            } else {
                closeAll();
            }
        }
    };
    if (window.__scoopTabletGenericTipTapHandler) {
        document.removeEventListener("pointerdown", window.__scoopTabletGenericTipTapHandler, true);
        document.removeEventListener("click", window.__scoopTabletGenericTipTapHandler, true);
    }
    window.__scoopTabletGenericTipTapHandler = onTap;
    document.addEventListener("pointerdown", onTap, true);
    document.addEventListener("click", onTap, true);
    ensureCss();
    if (!window.__scoopTabletGenericTipCssWatch) {
        window.__scoopTabletGenericTipCssWatch = true;
        setInterval(ensureCss, 1500);
        window.addEventListener("resize", ensureCss, { passive: true });
    }
    window.__scoopTabletGenericTipBindVersion = 13;
    window.__scoopTabletGenericTipStandalone = 9;
})();
"""

# Tablet + iPad Mini (744–1366): dismiss open tip popups on dead-space / other-tip taps.
# Keeps taps inside an already-open popup (links/scroll) from closing it.
_TABLET_TIP_DISMISS_STANDALONE_JS = r"""
(() => {
    const MIN = 744;
    const MAX = 1366;
    const isRange = () => {
        const w = window.innerWidth;
        return w >= MIN && w <= MAX;
    };
    const clearGenericTip = (tip) => {
        if (!tip) return;
        [
            "position", "left", "top", "right", "bottom", "transform", "width",
            "max-width", "min-width", "max-height", "overflow-y", "overflow-x",
            "visibility", "opacity", "pointer-events", "display", "z-index",
            "white-space", "word-break", "overflow-wrap", "box-sizing", "text-align",
            "--scoop-tablet-tip-left", "--scoop-tablet-tip-top", "--scoop-tablet-tip-width",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const clearHlTip = (tip) => {
        if (!tip) return;
        [
            "--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width",
            "--hl-fixed-max-height", "--hl-fixed-height",
            "height", "position", "left", "top", "right", "bottom", "transform",
            "width", "max-width", "max-height", "visibility", "opacity",
            "pointer-events", "display", "flex-direction", "overflow",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const closeHeadlines = (exceptWrap) => {
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((cb) => {
                const wrap = cb.closest(".tip-wrap.headlines-tip");
                if (exceptWrap && wrap === exceptWrap) return;
                cb.checked = false;
                if (wrap) {
                    wrap.classList.remove("hl-tip-desktop-open");
                    clearHlTip(wrap.querySelector(":scope > .tip-text"));
                }
            });
    };
    const closeGenerics = (exceptWrap) => {
        document
            .querySelectorAll(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open")
            .forEach((wrap) => {
                if (exceptWrap && wrap === exceptWrap) return;
                wrap.classList.remove("scoop-mobile-tip-open");
                clearGenericTip(wrap.querySelector(":scope > .tip-text"));
            });
    };
    const closeTips = (opts) => {
        if (!isRange()) return;
        const o = opts || {};
        if (o.headlines !== false) closeHeadlines(o.exceptHeadlines || null);
        if (o.generics !== false) closeGenerics(o.exceptGeneric || null);
    };
    const onDismiss = (event) => {
        if (!isRange() || !event || !event.target || !event.target.closest) return;
        if (event.type === "pointerdown" && event.pointerType === "mouse" && event.button !== 0) {
            return;
        }
        // Prefer pointerdown; click is a fallback when pointerdown was skipped.
        if (event.type === "click" && event.pointerType) {
            return;
        }
        const t = event.target;

        const hlWrap = t.closest(".tip-wrap.headlines-tip");
        if (hlWrap) {
            const cb = hlWrap.querySelector(".hl-tip-cb");
            const inOpenPopup =
                cb &&
                cb.checked &&
                t.closest(".tip-text") &&
                !t.closest(".hl-tip-backdrop") &&
                !t.closest(".hl-tip-count");
            if (inOpenPopup) return;

            if (t.closest(".hl-tip-count")) {
                closeHeadlines(hlWrap);
                closeGenerics(null);
                return;
            }

            if (t.closest(".hl-tip-backdrop")) {
                if (cb && cb.checked) {
                    cb.checked = false;
                    hlWrap.classList.remove("hl-tip-desktop-open");
                    clearHlTip(hlWrap.querySelector(":scope > .tip-text"));
                    try {
                        cb.dispatchEvent(new Event("change", { bubbles: true }));
                    } catch (e) {}
                }
                closeGenerics(null);
                if (event.cancelable) event.preventDefault();
                return;
            }
        }

        const openGeneric = t.closest(".tip-wrap.scoop-mobile-tip-open");
        if (
            openGeneric &&
            !openGeneric.classList.contains("headlines-tip") &&
            t.closest(".tip-text")
        ) {
            return;
        }

        const genericWrap = t.closest(".tip-wrap:not(.headlines-tip)");
        if (genericWrap) {
            closeHeadlines(null);
            closeGenerics(genericWrap);
            return;
        }

        closeHeadlines(null);
        closeGenerics(null);
    };

    const isScrollInsideOpenPopup = (event) => {
        const t = event && event.target;
        if (!t || !t.closest) return false;
        const hlWrap = t.closest(".tip-wrap.headlines-tip");
        if (hlWrap) {
            const cb = hlWrap.querySelector(".hl-tip-cb");
            if (
                cb &&
                cb.checked &&
                t.closest(".tip-text") &&
                !t.closest(".hl-tip-backdrop")
            ) {
                return true;
            }
        }
        if (
            t.closest(".tip-wrap.scoop-mobile-tip-open:not(.headlines-tip)") &&
            t.closest(".tip-text")
        ) {
            return true;
        }
        return false;
    };

    const onScrollDismiss = (event) => {
        if (!isRange()) return;
        if (isScrollInsideOpenPopup(event)) return;
        const hasOpen =
            document.querySelector(
                ".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked"
            ) || document.querySelector(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open");
        if (!hasOpen) return;
        closeHeadlines(null);
        closeGenerics(null);
    };

    if (window.__scoopTabletTipDismissHandler) {
        document.removeEventListener("pointerdown", window.__scoopTabletTipDismissHandler, true);
        document.removeEventListener("click", window.__scoopTabletTipDismissHandler, true);
    }
    if (window.__scoopTabletTipScrollDismissHandler) {
        window.removeEventListener("scroll", window.__scoopTabletTipScrollDismissHandler, true);
        document.removeEventListener("scroll", window.__scoopTabletTipScrollDismissHandler, true);
        document.removeEventListener("wheel", window.__scoopTabletTipScrollDismissHandler, true);
        document.removeEventListener("touchmove", window.__scoopTabletTipScrollDismissHandler, true);
    }
    window.__scoopTabletTipDismissHandler = onDismiss;
    window.__scoopTabletTipScrollDismissHandler = onScrollDismiss;
    document.addEventListener("pointerdown", onDismiss, true);
    document.addEventListener("click", onDismiss, true);
    window.addEventListener("scroll", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("scroll", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("wheel", onScrollDismiss, { passive: true, capture: true });
    document.addEventListener("touchmove", onScrollDismiss, { passive: true, capture: true });
    window.__scoopCloseTabletTips = closeTips;
    window.__scoopTabletTipDismissStandalone = 4;
})();
"""

# Phone + tablet only: one tip at a time. Does not move or restyle tips.
_MOBILE_TABLET_TIP_EXCLUSIVE_CSS = """
@media (max-width: 1366px) {
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover > .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active > .tip-text {
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
  html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
  }
}
"""

_MOBILE_TABLET_TIP_EXCLUSIVE_JS = r"""
(() => {
    const DESKTOP_MIN = 1367;
    const isDesktop = () =>
        (window.innerWidth || 0) >= DESKTOP_MIN ||
        window.matchMedia("(min-width: 1367px)").matches;
    const isPhoneOrTablet = () => !isDesktop();
    const isDesktopTipTarget = (node) =>
        !!(
            node &&
            node.closest &&
            node.closest(
                ".scoop-desktop-name-tip-open, .scoop-desktop-generic-tip-open, .scoop-desktop-header-tip-open, .hl-tip-desktop-open"
            )
        );
    const clearHl = (tip) => {
        if (!tip) return;
        [
            "--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width",
            "--hl-fixed-max-height", "--hl-fixed-height",
            "height", "position", "left", "top", "right", "bottom", "transform",
            "width", "max-width", "max-height", "visibility", "opacity",
            "pointer-events", "display", "flex-direction", "overflow",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const clearGeneric = (tip) => {
        if (!tip) return;
        [
            "position", "left", "top", "right", "bottom", "transform", "width",
            "max-width", "min-width", "max-height", "overflow-y", "overflow-x",
            "visibility", "opacity", "pointer-events", "display", "z-index",
            "white-space", "word-break", "overflow-wrap", "box-sizing", "text-align",
            "--scoop-mobile-tip-left", "--scoop-mobile-tip-top",
            "--scoop-tablet-tip-left", "--scoop-tablet-tip-top", "--scoop-tablet-tip-width",
        ].forEach((p) => tip.style.removeProperty(p));
    };
    const closeHeadlines = (exceptWrap) => {
        if (isDesktop()) return;
        document.querySelectorAll(".tip-wrap.headlines-tip .hl-tip-cb:checked").forEach((cb) => {
            const wrap = cb.closest(".tip-wrap.headlines-tip");
            if (exceptWrap && wrap === exceptWrap) return;
            cb.checked = false;
        });
    };
    const closeGenerics = (exceptWrap) => {
        if (isDesktop()) return;
        document.querySelectorAll(".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open").forEach((wrap) => {
            if (exceptWrap && wrap === exceptWrap) return;
            wrap.classList.remove("scoop-mobile-tip-open");
            clearGeneric(wrap.querySelector(":scope > .tip-text"));
        });
    };
    const onTap = (event) => {
        if (isDesktop() || !isPhoneOrTablet() || !event || !event.target || !event.target.closest) return;
        if (isDesktopTipTarget(event.target)) return;
        if (event.type === "pointerdown" && event.pointerType === "mouse" && event.button !== 0) return;
        if (event.type === "click" && event.pointerType) return;
        const t = event.target;
        const hlWrap = t.closest(".tip-wrap.headlines-tip");
        const count = t.closest(".hl-tip-count");
        const genWrap = t.closest(".tip-wrap:not(.headlines-tip)");
        if (hlWrap || count) {
            const inOpenBody =
                hlWrap &&
                hlWrap.querySelector(".hl-tip-cb") &&
                hlWrap.querySelector(".hl-tip-cb").checked &&
                t.closest(".tip-text") &&
                !t.closest(".hl-tip-backdrop") &&
                !t.closest(".hl-tip-count");
            if (inOpenBody) return;
            closeGenerics(null);
            return;
        }
        if (genWrap) {
            const inOpenBody =
                genWrap.classList.contains("scoop-mobile-tip-open") && t.closest(".tip-text");
            if (inOpenBody) return;
            closeHeadlines(null);
            closeGenerics(genWrap);
        }
    };
    if (window.__scoopMobileTabletTipExclusiveHandler) {
        document.removeEventListener("pointerdown", window.__scoopMobileTabletTipExclusiveHandler, true);
        document.removeEventListener("click", window.__scoopMobileTabletTipExclusiveHandler, true);
    }
    window.__scoopMobileTabletTipExclusiveHandler = onTap;
    document.addEventListener("pointerdown", onTap, true);
    document.addEventListener("click", onTap, true);
    window.__scoopMobileTabletTipExclusive = 3;
})();
"""

# Compact tablet Headlines centering — independent of the large tip bundle (often dropped).
# Generic company tips must never change this path; Headlines stay horizontally centered.
_TABLET_HEADLINES_CENTER_STANDALONE_JS = r"""
(() => {
    const MIN = 769;
    const MAX = 1366;
    const PAD = 12;
    const isTablet = () => {
        const w = window.innerWidth;
        return w >= MIN && w <= MAX;
    };
    const slot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const top = Math.round(headerBottom + PAD);
        const viewLeft = PAD;
        const viewRight = window.innerWidth - PAD;
        const maxHeight = Math.max(200, window.innerHeight - top - PAD);
        const available = Math.max(240, viewRight - viewLeft);
        const width = Math.round(Math.min(available, Math.max(280, window.innerWidth * 0.4)));
        let left = Math.round(viewLeft + (available - width) / 2);
        left = Math.max(viewLeft, Math.min(left, viewRight - width));
        return { top, left, width, maxHeight };
    };
    const apply = (wrap) => {
        if (!isTablet() || !wrap || !wrap.classList.contains("headlines-tip")) return;
        const cb = wrap.querySelector(".hl-tip-cb");
        if (!cb || !cb.checked) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        // Strip any accidental generic-tip vars so company-tip CSS cannot pull Headlines off-center.
        tip.style.removeProperty("--scoop-tablet-tip-left");
        tip.style.removeProperty("--scoop-tablet-tip-top");
        tip.style.removeProperty("--scoop-tablet-tip-width");
        const s = slot();
        tip.style.setProperty("--hl-fixed-top", s.top + "px");
        tip.style.setProperty("--hl-fixed-left", s.left + "px");
        tip.style.setProperty("--hl-fixed-width", s.width + "px");
        tip.style.setProperty("--hl-fixed-max-height", s.maxHeight + "px");
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("top", s.top + "px", "important");
        tip.style.setProperty("left", s.left + "px", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", s.width + "px", "important");
        tip.style.setProperty("max-width", s.width + "px", "important");
        tip.style.setProperty("max-height", s.maxHeight + "px", "important");
    };
    const repositionOpen = () => {
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((cb) => apply(cb.closest(".tip-wrap.headlines-tip")));
    };
    const onHeadlinesTap = (event) => {
        if (!isTablet()) return;
        const count =
            event.target && event.target.closest
                ? event.target.closest(".hl-tip-count")
                : null;
        if (!count) return;
        const wrap = count.closest(".tip-wrap.headlines-tip");
        window.requestAnimationFrame(() => {
            apply(wrap);
            window.requestAnimationFrame(() => apply(wrap));
        });
    };
    if (window.__scoopTabletHeadlinesCenterTapHandler) {
        document.removeEventListener(
            "pointerdown",
            window.__scoopTabletHeadlinesCenterTapHandler,
            true
        );
        document.removeEventListener(
            "click",
            window.__scoopTabletHeadlinesCenterTapHandler,
            true
        );
    }
    window.__scoopTabletHeadlinesCenterTapHandler = onHeadlinesTap;
    document.addEventListener("pointerdown", onHeadlinesTap, true);
    document.addEventListener("click", onHeadlinesTap, true);
    document.addEventListener(
        "change",
        (event) => {
            if (!isTablet()) return;
            if (event.target && event.target.classList && event.target.classList.contains("hl-tip-cb")) {
                window.requestAnimationFrame(() =>
                    apply(event.target.closest(".tip-wrap.headlines-tip"))
                );
            }
        },
        true
    );
    if (!window.__scoopTabletHeadlinesCenterWatch) {
        window.__scoopTabletHeadlinesCenterWatch = true;
        window.addEventListener("resize", repositionOpen, { passive: true });
        window.setInterval(repositionOpen, 2000);
    }
    window.__scoopTabletHeadlinesCenterStandalone = 1;
    repositionOpen();
})();
"""

# iPad Mini only (744–768): center Headlines popup. Does not change tablet (769+) Headlines.
_IPAD_MINI_HEADLINES_CENTER_STANDALONE_JS = r"""
(() => {
    const MIN = 744;
    const MAX = 768;
    const PAD = 12;
    const isIpadMini = () => {
        const w = window.innerWidth;
        return w >= MIN && w <= MAX;
    };
    const slot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const top = Math.round(Math.max(PAD, headerBottom + PAD));
        const viewLeft = PAD;
        const viewRight = window.innerWidth - PAD;
        const maxHeight = Math.max(180, window.innerHeight - top - PAD);
        const available = Math.max(220, viewRight - viewLeft);
        const width = Math.round(Math.min(available, Math.max(260, window.innerWidth * 0.42)));
        let left = Math.round(viewLeft + (available - width) / 2);
        left = Math.max(viewLeft, Math.min(left, viewRight - width));
        return { top, left, width, maxHeight };
    };
    const apply = (wrap) => {
        if (!isIpadMini() || !wrap || !wrap.classList.contains("headlines-tip")) return;
        const cb = wrap.querySelector(".hl-tip-cb");
        if (!cb || !cb.checked) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        tip.style.removeProperty("--scoop-tablet-tip-left");
        tip.style.removeProperty("--scoop-tablet-tip-top");
        tip.style.removeProperty("--scoop-tablet-tip-width");
        const s = slot();
        tip.style.setProperty("--hl-fixed-top", s.top + "px");
        tip.style.setProperty("--hl-fixed-left", s.left + "px");
        tip.style.setProperty("--hl-fixed-width", s.width + "px");
        tip.style.setProperty("--hl-fixed-max-height", s.maxHeight + "px");
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("top", s.top + "px", "important");
        tip.style.setProperty("left", s.left + "px", "important");
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
        tip.style.setProperty("width", s.width + "px", "important");
        tip.style.setProperty("max-width", s.width + "px", "important");
        tip.style.setProperty("max-height", s.maxHeight + "px", "important");
    };
    const repositionOpen = () => {
        if (!isIpadMini()) return;
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((cb) => apply(cb.closest(".tip-wrap.headlines-tip")));
    };
    const onHeadlinesTap = (event) => {
        if (!isIpadMini()) return;
        const count =
            event.target && event.target.closest
                ? event.target.closest(".hl-tip-count")
                : null;
        if (!count) return;
        const wrap = count.closest(".tip-wrap.headlines-tip");
        window.requestAnimationFrame(() => {
            apply(wrap);
            window.requestAnimationFrame(() => apply(wrap));
        });
    };
    if (window.__scoopIpadMiniHeadlinesCenterTapHandler) {
        document.removeEventListener(
            "pointerdown",
            window.__scoopIpadMiniHeadlinesCenterTapHandler,
            true
        );
        document.removeEventListener(
            "click",
            window.__scoopIpadMiniHeadlinesCenterTapHandler,
            true
        );
    }
    window.__scoopIpadMiniHeadlinesCenterTapHandler = onHeadlinesTap;
    document.addEventListener("pointerdown", onHeadlinesTap, true);
    document.addEventListener("click", onHeadlinesTap, true);
    document.addEventListener(
        "change",
        (event) => {
            if (!isIpadMini()) return;
            if (event.target && event.target.classList && event.target.classList.contains("hl-tip-cb")) {
                window.requestAnimationFrame(() =>
                    apply(event.target.closest(".tip-wrap.headlines-tip"))
                );
            }
        },
        true
    );
    if (!window.__scoopIpadMiniHeadlinesCenterWatch) {
        window.__scoopIpadMiniHeadlinesCenterWatch = true;
        window.addEventListener("resize", repositionOpen, { passive: true });
        window.setInterval(repositionOpen, 2000);
    }
    window.__scoopIpadMiniHeadlinesCenterStandalone = 1;
    repositionOpen();
})();
"""

# Parent-document binder matching the pre-fix desktop Headlines slot and behaviors.
_DESKTOP_HEADLINES_STANDALONE_JS = r"""
(() => {
    const VERSION = 21;
    const DESKTOP_MIN = 1367;
    const PAD = 12;
    let appDoc = document;
    let appWin = window;
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            appDoc = window.parent.document;
            appWin = window.parent;
        }
    } catch (e) {
        appDoc = document;
        appWin = window;
    }
    if (appWin.__scoopDesktopHeadlinesStandalone === VERSION) {
        return;
    }
    appWin.__scoopDesktopHeadlinesStandalone = VERSION;

    const isDesktop = () => (appWin.innerWidth || 0) >= DESKTOP_MIN;

    const thEl = (test) =>
        [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) =>
            test((th.textContent || "").replace(/\s+/g, " ").trim())
        ) || null;

    const headerRect = (pattern, { exactHeadlines } = {}) => {
        const header = thEl((t) => {
            if (exactHeadlines) {
                return t.startsWith("Headlines") && !t.startsWith("Headline ");
            }
            return pattern.test(t);
        });
        return header ? header.getBoundingClientRect() : null;
    };

    const slotFor = () => {
        const MIN_W = 280;
        const EXTRA_W = 130;
        const MIN_H = 280;
        const viewH = appWin.innerHeight || 800;
        const viewW = appWin.innerWidth || 1600;
        const inView = (r) =>
            r && r.width > 40 && r.bottom > 0 && r.top < viewH && r.right > 0 && r.left < viewW;
        const th = thEl((t) => t.startsWith("Market Mood"));
        const thRect = th ? th.getBoundingClientRect() : null;
        const moodTds = [...appDoc.querySelectorAll('.full-results-wrap td[data-label="Market Mood"]')];
        const vis = moodTds.map((el) => el.getBoundingClientRect()).filter(inView);
        const table = appDoc.querySelector(".full-results-wrap .full-results-table");
        const tbody = table && table.tBodies && table.tBodies[0];
        const tableBottom = tbody
            ? tbody.getBoundingClientRect().bottom
            : (table ? table.getBoundingClientRect().bottom : viewH - PAD);
        let left = PAD;
        let width = MIN_W;
        let top = PAD;
        if (vis.length) {
            left = Math.min(...vis.map((r) => r.left));
            width = Math.max(...vis.map((r) => r.width));
            top = inView(thRect) ? thRect.top - 8 : Math.min(...vis.map((r) => r.top)) - 8;
        } else if (moodTds[0]) {
            const r = moodTds[0].getBoundingClientRect();
            left = r.left;
            width = r.width;
        }
        width = Math.max(MIN_W, Math.round(width)) + EXTRA_W;
        left = Math.round(left);
        top = Math.round(top);
        if (top < PAD) top = PAD;
        if (left < PAD) left = PAD;
        if (left + width > viewW - PAD) width = Math.max(MIN_W + EXTRA_W, viewW - PAD - left);
        let maxHeight = Math.round(Math.min(tableBottom, viewH - PAD) - top);
        if (vis.length) {
            maxHeight = Math.max(maxHeight, Math.round(Math.max(...vis.map((r) => r.bottom)) - top));
        }
        if (top + maxHeight > viewH - PAD) maxHeight = Math.round(viewH - PAD - top);
        maxHeight = Math.max(MIN_H, maxHeight);
        return { top, left, width, maxHeight };
    };

    const headingBase = (heading) => {
        if (!heading) return "Headlines";
        if (!heading.dataset.hlBaseLabel) {
            const current = (heading.textContent || "Headlines").trim();
            heading.dataset.hlBaseLabel = current.split(" - ")[0].trim() || "Headlines";
        }
        return heading.dataset.hlBaseLabel;
    };

    const companyName = (wrap) => {
        const row = wrap && wrap.closest("tr");
        if (!row) return "";
        const inCommodity = !!wrap.closest(".commodity-results");
        const valueCell =
            row.querySelector('td[data-label="Company"] .fr-val') ||
            row.querySelector('td[data-label="Name"] .fr-val') ||
            (inCommodity ? row.querySelector('td[data-label="Commodity"] .fr-val') : null);
        if (!valueCell) return "";
        const tipWrap = valueCell.querySelector(".tip-wrap");
        if (tipWrap) {
            const clone = tipWrap.cloneNode(true);
            clone.querySelectorAll(".tip-text").forEach((node) => node.remove());
            return (clone.textContent || "").replace(/\s+/g, " ").trim();
        }
        return (valueCell.textContent || "").replace(/\s+/g, " ").trim();
    };

    const fitTip = (tip, slot) => {
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const heading = tip.querySelector(".hl-tip-heading");
        const headingHeight = heading ? heading.offsetHeight : 0;
        const tipHeight = Math.max(280, slot.maxHeight);
        tip.style.setProperty("--hl-fixed-height", `${tipHeight}px`);
        tip.style.setProperty("height", `${tipHeight}px`);
        if (scroll) {
            const scrollHeight = Math.max(80, tipHeight - headingHeight);
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("flex", "1 1 auto", "important");
            scroll.style.setProperty("min-height", "0", "important");
            scroll.style.setProperty("height", `${scrollHeight}px`, "important");
            scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
        }
        return tipHeight;
    };

    const closeOthers = (keep) => {
        appDoc.querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip").forEach((wrap) => {
            if (wrap === keep) return;
            const cb = wrap.querySelector(".hl-tip-cb");
            if (cb) cb.checked = false;
            wrap.classList.remove("hl-tip-desktop-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) return;
            ["--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width", "--hl-fixed-max-height", "--hl-fixed-height", "height"]
                .forEach((p) => tip.style.removeProperty(p));
            const heading = wrap.querySelector(".hl-tip-heading");
            if (heading) heading.textContent = headingBase(heading);
        });
    };

    const apply = (wrap) => {
        if (!isDesktop() || !wrap) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        closeOthers(wrap);
        wrap.classList.add("hl-tip-desktop-open");
        appWin.__scoopDesktopHlOpenedAt = Date.now();
        const heading = tip.querySelector(".hl-tip-heading");
        if (heading) {
            const company = companyName(wrap);
            heading.textContent = company ? `${headingBase(heading)} - ${company}` : headingBase(heading);
        }
        let slot = slotFor();
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("top", `${slot.top}px`, "important");
        tip.style.setProperty("left", `${slot.left}px`, "important");
        tip.style.setProperty("width", `${slot.width}px`, "important");
        tip.style.setProperty("min-width", `${slot.width}px`, "important");
        tip.style.setProperty("max-width", `${slot.width}px`, "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        const tipHeight = fitTip(tip, slot);
        slot = slotFor(tipHeight);
        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("top", `${slot.top}px`, "important");
        tip.style.setProperty("left", `${slot.left}px`, "important");
        fitTip(tip, slot);
    };

    const sync = (wrap) => {
        if (!isDesktop() || !wrap) return;
        const cb = wrap.querySelector(".hl-tip-cb");
        if (cb && cb.checked) {
            apply(wrap);
            return;
        }
        wrap.classList.remove("hl-tip-desktop-open");
        const heading = wrap.querySelector(".hl-tip-heading");
        if (heading) heading.textContent = headingBase(heading);
    };

    const closeAll = () => {
        appDoc.querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip").forEach((wrap) => {
            const cb = wrap.querySelector(".hl-tip-cb");
            if (cb) cb.checked = false;
            wrap.classList.remove("hl-tip-desktop-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (tip) {
                ["--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width", "--hl-fixed-max-height", "--hl-fixed-height", "height"]
                    .forEach((p) => tip.style.removeProperty(p));
            }
            const heading = wrap.querySelector(".hl-tip-heading");
            if (heading) heading.textContent = headingBase(heading);
        });
    };

    const isInsideOpenPopup = (node) => {
        if (!node || !node.closest) return false;
        const wrap = node.closest(".tip-wrap.headlines-tip");
        if (!wrap) return false;
        const cb = wrap.querySelector(".hl-tip-cb");
        const open = (cb && cb.checked) || wrap.classList.contains("hl-tip-desktop-open");
        if (!open) return false;
        return !!(node.closest(".tip-text") && !node.closest(".hl-tip-backdrop"));
    };

    const onDismissPointer = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        if (event.type === "pointerdown" && event.pointerType === "mouse" && event.button !== 0) return;
        const t = event.target;
        if (t.closest(".hl-tip-count")) return;
        if (isInsideOpenPopup(t)) return;
        closeAll();
    };

    const onDismissScroll = (event) => {
        if (!isDesktop()) return;
        if (event && event.target && isInsideOpenPopup(event.target)) return;
        if (Date.now() - (appWin.__scoopDesktopHlOpenedAt || 0) < 250) return;
        closeAll();
    };

    const onClick = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        if (event.target.closest("a")) return;
        const label = event.target.closest(".hl-tip-count");
        if (!label) return;
        const wrap = label.closest(".tip-wrap.headlines-tip");
        if (!wrap) return;
        appWin.__scoopDesktopHlOpenedAt = Date.now();
        appWin.requestAnimationFrame(() => sync(wrap));
    };

    const onChange = (event) => {
        if (!isDesktop() || !event || !event.target) return;
        if (!event.target.classList || !event.target.classList.contains("hl-tip-cb")) return;
        sync(event.target.closest(".tip-wrap.headlines-tip"));
    };

    const bindScroller = (el) => {
        if (!el || el.__scoopHlScrollBound === VERSION) return;
        el.__scoopHlScrollBound = VERSION;
        el.addEventListener("scroll", onDismissScroll, { capture: true, passive: true });
        el.addEventListener("wheel", onDismissScroll, { capture: true, passive: true });
    };

    const scrollTargets = () => [
        appWin,
        appDoc,
        appDoc.scrollingElement,
        appDoc.documentElement,
        appDoc.body,
        appDoc.querySelector('[data-testid="stAppViewContainer"]'),
        appDoc.querySelector('[data-testid="stMain"]'),
        appDoc.querySelector(".stApp"),
    ].filter(Boolean);

    if (appWin.__scoopDesktopHlDismissPointer) {
        appDoc.removeEventListener("pointerdown", appWin.__scoopDesktopHlDismissPointer, true);
        appDoc.removeEventListener("mousedown", appWin.__scoopDesktopHlDismissPointer, true);
    }
    appWin.__scoopDesktopHlDismissPointer = onDismissPointer;
    appWin.__scoopDesktopHlDismissScroll = onDismissScroll;
    appDoc.addEventListener("pointerdown", onDismissPointer, true);
    appDoc.addEventListener("mousedown", onDismissPointer, true);
    appDoc.addEventListener("click", onClick, true);
    appDoc.addEventListener("change", onChange, true);
    scrollTargets().forEach(bindScroller);
    if (!appWin.__scoopDesktopHlScrollWatch) {
        appWin.__scoopDesktopHlScrollWatch = true;
        appWin.setInterval(() => {
            if (!isDesktop()) return;
            scrollTargets().forEach(bindScroller);
        }, 1200);
    }
})();
"""

_DESKTOP_HL_LOCK_JS = r"""
(() => {
    const VERSION = 3;
    const DESKTOP_MIN = 1367;
    const PAD = 12;
    const MIN_W = 280;
    const EXTRA_W = 130;
    const MIN_H = 280;
    let appDoc = document;
    let appWin = window;
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            appDoc = window.parent.document;
            appWin = window.parent;
        }
    } catch (e) {}
    if (appWin.__scoopDesktopHlLock === VERSION) return;
    appWin.__scoopDesktopHlLock = VERSION;

    const isDesktop = () => (appWin.innerWidth || 0) >= DESKTOP_MIN;
    const inView = (r) => {
        const viewH = appWin.innerHeight || 800;
        const viewW = appWin.innerWidth || 1600;
        return r && r.width > 40 && r.bottom > 0 && r.top < viewH && r.right > 0 && r.left < viewW;
    };

    const slotFor = () => {
        const viewH = appWin.innerHeight || 800;
        const viewW = appWin.innerWidth || 1600;
        const th = [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((el) =>
            (el.textContent || "").replace(/\s+/g, " ").trim().startsWith("Market Mood")
        );
        const thRect = th ? th.getBoundingClientRect() : null;
        const moodTds = [...appDoc.querySelectorAll('.full-results-wrap td[data-label="Market Mood"]')];
        const vis = moodTds.map((el) => el.getBoundingClientRect()).filter(inView);
        const table = appDoc.querySelector(".full-results-wrap .full-results-table");
        const tbody = table && table.tBodies && table.tBodies[0];
        const tableBottom = tbody
            ? tbody.getBoundingClientRect().bottom
            : (table ? table.getBoundingClientRect().bottom : viewH - PAD);
        let left = PAD;
        let width = MIN_W;
        let top = PAD;
        if (vis.length) {
            left = Math.min(...vis.map((r) => r.left));
            width = Math.max(...vis.map((r) => r.width));
            top = inView(thRect) ? thRect.top - 8 : Math.min(...vis.map((r) => r.top)) - 8;
        } else if (moodTds[0]) {
            const r = moodTds[0].getBoundingClientRect();
            left = r.left;
            width = r.width;
        }
        width = Math.max(MIN_W, Math.round(width)) + EXTRA_W;
        left = Math.round(left);
        top = Math.round(top);
        if (top < PAD) top = PAD;
        if (left < PAD) left = PAD;
        if (left + width > viewW - PAD) width = Math.max(MIN_W + EXTRA_W, viewW - PAD - left);
        let maxHeight = Math.round(Math.min(tableBottom, viewH - PAD) - top);
        if (vis.length) {
            maxHeight = Math.max(maxHeight, Math.round(Math.max(...vis.map((r) => r.bottom)) - top));
        }
        if (top + maxHeight > viewH - PAD) maxHeight = Math.round(viewH - PAD - top);
        maxHeight = Math.max(MIN_H, maxHeight);
        return { top, left, width, maxHeight };
    };

    const paint = () => {
        if (!isDesktop()) return;
        const wrap = appDoc.querySelector(
            ".full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked), .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open"
        );
        if (!wrap) return;
        const cb = wrap.querySelector(".hl-tip-cb");
        if (cb && !cb.checked && !wrap.classList.contains("hl-tip-desktop-open")) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        const slot = slotFor();
        const tipHeight = slot.maxHeight;
        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("left", slot.left + "px", "important");
        tip.style.setProperty("top", slot.top + "px", "important");
        tip.style.setProperty("width", slot.width + "px", "important");
        tip.style.setProperty("min-width", (MIN_W + EXTRA_W) + "px", "important");
        tip.style.setProperty("max-width", slot.width + "px", "important");
        tip.style.setProperty("height", tipHeight + "px", "important");
        tip.style.setProperty("min-height", MIN_H + "px", "important");
        tip.style.setProperty("max-height", tipHeight + "px", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("--hl-fixed-left", slot.left + "px");
        tip.style.setProperty("--hl-fixed-top", slot.top + "px");
        tip.style.setProperty("--hl-fixed-width", slot.width + "px");
        tip.style.setProperty("--hl-fixed-height", tipHeight + "px");
        tip.style.setProperty("--hl-fixed-max-height", tipHeight + "px");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const heading = tip.querySelector(".hl-tip-heading");
        if (scroll) {
            const headingH = heading ? heading.offsetHeight : 48;
            const scrollH = Math.max(120, tipHeight - headingH);
            scroll.style.setProperty("display", "block", "important");
            scroll.style.setProperty("visibility", "visible", "important");
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("height", scrollH + "px", "important");
            scroll.style.setProperty("max-height", scrollH + "px", "important");
            scroll.style.setProperty("min-height", "8rem", "important");
        }
    };

    appWin.setInterval(paint, 120);
})();
"""


def install_tooltip_scroll_handler() -> None:
    """Inject mobile headline CSS; HTML backdrop label closes panel on outside tap."""
    from theme_mode import inject_dark_mode_styles

    _inject_desktop_headlines_css()
    _inject_ipad_mini_headlines_css()
    _inject_mobile_phone_headlines_css()
    _ensure_generic_tooltip_mobile_assets()

    # Always re-inject tip/scroll JS. Streamlit reruns (disclaimer agree, widgets)
    # wipe prior <script> tags; session_state alone cannot keep handlers alive.
    st.html(
        f"<style id='scoop-mobile-headlines-css'>{_MOBILE_HEADLINES_CSS}</style>"
        f"<style id='scoop-mobile-tablet-card-order-css'>{_MOBILE_TABLET_CARD_ORDER_CSS}</style>"
        f"<style id='scoop-tablet-headlines-css'>{_TABLET_HEADLINES_POPUP_CSS}</style>"
        f"<style id='scoop-ipad-mini-headlines-css'>{_IPAD_MINI_HEADLINES_CSS}</style>"
        f"<style id='scoop-surface-duo-headlines-css'>{_SURFACE_DUO_HEADLINES_CSS}</style>"
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>"
        f"<style id='scoop-desktop-tooltip-type-css'>{_DESKTOP_TOOLTIP_TYPE_CSS}</style>"
        f"<style id='scoop-asus-zenbook-fold-headlines-css'>{_ASUS_ZENBOOK_FOLD_HEADLINES_CSS}</style>"
        f"<style id='scoop-mobile-phone-headlines-fixed-css'>{_MOBILE_PHONE_HEADLINES_FIXED_CSS}</style>"
        f"<style id='scoop-responsive-generic-tooltip-css'>{_RESPONSIVE_GENERIC_TOOLTIP_CSS}</style>"
        f"<style id='scoop-dark-responsive-tip-underline-css'>{_DARK_RESPONSIVE_TIP_UNDERLINE_CSS}</style>"
        f"<style id='scoop-dark-popup-outline-css'>{_DARK_POPUP_OUTLINE_CSS}</style>"
        + _responsive_bootstrap_markup()
        + f"<style id='scoop-desktop-sidebar-layout-css'>{DESKTOP_SIDEBAR_LAYOUT}</style>"
        + f"<style id='scoop-desktop-zoom-layout-css'>{DESKTOP_ZOOM_LAYOUT}</style>"
        + f"<style id='scoop-sidebar-nav-compact-css'>{SIDEBAR_NAV_COMPACT}</style>",
        unsafe_allow_javascript=True,
    )
    # Chunked: a single giant <script> is dropped by Streamlit; tablet tips never bind.
    _inject_js_source(_COMBINED_PAGE_JS, key="combined-page-v75")
    inject_desktop_sidebar_nav_market()
    inject_desktop_tablet_disclaimer_flow()
    st.session_state[TOOLTIP_INSTALLED_KEY] = TOOLTIP_SCRIPT_VERSION
    _inject_tablet_analyze_link_css()
    inject_dark_mode_styles()
    _inject_tablet_hl_heading_color_css()
    install_page_layout_resync()
    # Dedicated inject so desktop name-tip fixed positioning always binds.
    st.html(
        f"<script id='scoop-desktop-name-tip-js'>{_GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS}</script>",
        unsafe_allow_javascript=True,
    )
    st.html(
        f"<style id='scoop-streamlit-chrome-hide'>{EARLY_STREAMLIT_CHROME_HIDE}</style>",
        unsafe_allow_javascript=True,
    )
    # Final: after page/screener CSS so open tablet tips stay visible beside the trigger.
    _inject_name_tooltip_override()
    # Last paint: tablet Headlines heading blue in light (regular) and dark mode.
    _inject_tablet_hl_heading_color_css()
    # Small enough for Streamlit to keep; survives when the combined bundle is dropped.
    st.html(
        f"<script id='scoop-phone-generic-tip-standalone'>{_PHONE_GENERIC_TIP_STANDALONE_JS}</script>"
        f"<script id='scoop-tablet-generic-tip-standalone'>{_TABLET_GENERIC_TIP_STANDALONE_JS}</script>"
        f"<script id='scoop-tablet-headlines-center-standalone'>{_TABLET_HEADLINES_CENTER_STANDALONE_JS}</script>"
        f"<script id='scoop-ipad-mini-headlines-center-standalone'>{_IPAD_MINI_HEADLINES_CENTER_STANDALONE_JS}</script>"
        f"<script id='scoop-tablet-tip-dismiss-standalone'>{_TABLET_TIP_DISMISS_STANDALONE_JS}</script>"
        f"<style id='scoop-mobile-tablet-tip-exclusive-css'>{_MOBILE_TABLET_TIP_EXCLUSIVE_CSS}</style>"
        f"<script id='scoop-mobile-tablet-tip-exclusive'>{_MOBILE_TABLET_TIP_EXCLUSIVE_JS}</script>"
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>",
        unsafe_allow_javascript=True,
    )
    # Chunked inject: a full inline Headlines <script> is dropped by Streamlit.
    _inject_js_source(_DESKTOP_HEADLINES_STANDALONE_JS, key="desktop-hl-v21")
    _inject_js_source(_DESKTOP_HL_LOCK_JS, key="desktop-hl-lock-v3")
