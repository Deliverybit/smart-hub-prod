"""Desktop-only Headlines popup dismiss (outside click, other tooltip, scroll)."""

from __future__ import annotations

import streamlit as st

_JS = r"""
(() => {
    const VERSION = 3;
    const DESKTOP_MIN = 1367;
    let appDoc = document;
    let appWin = window;
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            appDoc = window.parent.document;
            appWin = window.parent;
        }
    } catch (e) {}
    appWin.__scoopDesktopHlDismissV = VERSION;

    const isDesktop = () => (appWin.innerWidth || 0) >= DESKTOP_MIN;

    const closeAll = () => {
        if (!isDesktop()) return;
        appDoc.querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip").forEach((wrap) => {
            const cb = wrap.querySelector(".hl-tip-cb");
            if (cb) cb.checked = false;
            wrap.classList.remove("hl-tip-desktop-open");
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) return;
            [
                "--hl-fixed-top", "--hl-fixed-left", "--hl-fixed-width",
                "--hl-fixed-max-height", "--hl-fixed-height", "height",
                "visibility", "opacity", "pointer-events",
            ].forEach((p) => tip.style.removeProperty(p));
            const heading = wrap.querySelector(".hl-tip-heading");
            if (heading && heading.dataset && heading.dataset.hlBaseLabel) {
                heading.textContent = heading.dataset.hlBaseLabel;
            }
        });
    };

    const isInsideOpenPopup = (node) => {
        if (!node || !node.closest) return false;
        const wrap = node.closest(".tip-wrap.headlines-tip");
        if (!wrap) return false;
        const cb = wrap.querySelector(".hl-tip-cb");
        const open = (cb && cb.checked) || wrap.classList.contains("hl-tip-desktop-open");
        if (!open) return false;
        return !!(node.closest(".tip-text") && !node.closest(".hl-tip-backdrop") && !node.closest(".hl-tip-count"));
    };

    const onPointer = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        if (event.button && event.button !== 0) return;
        const t = event.target;
        if (t.closest(".hl-tip-count")) {
            appWin.__scoopDesktopHlOpenedAt = Date.now();
            return;
        }
        if (isInsideOpenPopup(t)) return;
        if (Date.now() - (appWin.__scoopDesktopHlOpenedAt || 0) < 500) return;
        closeAll();
    };

    const onScroll = (event) => {
        if (!isDesktop()) return;
        if (event && event.target && isInsideOpenPopup(event.target)) return;
        if (Date.now() - (appWin.__scoopDesktopHlOpenedAt || 0) < 500) return;
        closeAll();
    };

    const bindScroller = (el) => {
        if (!el || el.__scoopHlDismissScroll === VERSION) return;
        el.__scoopHlDismissScroll = VERSION;
        el.addEventListener("scroll", onScroll, { capture: true, passive: true });
        el.addEventListener("wheel", onScroll, { capture: true, passive: true });
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

    if (appWin.__scoopDesktopHlDismissPtr) {
        appDoc.removeEventListener("pointerdown", appWin.__scoopDesktopHlDismissPtr, true);
        appDoc.removeEventListener("mousedown", appWin.__scoopDesktopHlDismissPtr, true);
    }
    appWin.__scoopDesktopHlDismissPtr = onPointer;
    appDoc.addEventListener("pointerdown", onPointer, true);
    appDoc.addEventListener("mousedown", onPointer, true);
    scrollTargets().forEach(bindScroller);
    if (!appWin.__scoopDesktopHlDismissWatch) {
        appWin.__scoopDesktopHlDismissWatch = true;
        appWin.setInterval(() => {
            if (!isDesktop()) return;
            scrollTargets().forEach(bindScroller);
        }, 800);
    }
})();
"""


_CSS = """
@media (min-width: 1367px) {
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        border: 2px solid #22c55e !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        border: 2px solid #ffffff !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        color: #93c5fd !important;
        border: 0 !important;
        border-bottom: 1px solid #334155 !important;
    }
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html:not([data-scoop-theme="dark"]) body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html[data-scoop-theme="light"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
}
"""


def inject_desktop_headlines_dismiss() -> None:
    """Always inject last so desktop Headlines dismiss binds on the app document."""
    st.html(
        f"<style id='scoop-desktop-hl-normal-outline'>{_CSS}</style>"
        f"<script id='scoop-desktop-hl-dismiss'>{_JS}</script>",
        unsafe_allow_javascript=True,
    )
