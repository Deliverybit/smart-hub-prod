"""Desktop-only: on-screen, scrollable, narrow Headlines panel right of the column."""

from __future__ import annotations

import streamlit as st

_CSS = """
@media (min-width: 1367px) {
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)):not(.hl-tip-desktop-open) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text:hover {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked):hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open:hover > .tip-text {
        position: fixed !important;
        display: flex !important;
        flex-direction: column !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: none !important;
        right: auto !important;
        bottom: auto !important;
        box-sizing: border-box !important;
        width: var(--hl-fixed-width, 410px) !important;
        max-width: var(--hl-fixed-width, 44vw) !important;
        min-width: 410px !important;
        min-height: 280px !important;
        border: 2px solid #22c55e !important;
        max-height: var(--hl-fixed-max-height, calc(100vh - 24px)) !important;
        overflow: hidden !important;
        z-index: 2147483000 !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        hyphens: none !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked):hover > .tip-text,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open:hover > .tip-text {
        border: 2px solid #ffffff !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        hyphens: none !important;
        line-height: 1.3 !important;
        color: #93c5fd !important;
        border: 0 !important;
        border-bottom: 1px solid #334155 !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .headlines-tip-scroll,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .headlines-tip-scroll {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        flex: 1 1 auto !important;
        min-height: 8rem !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        pointer-events: auto !important;
        scrollbar-width: thin !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line a {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #ffffff !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line a,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
}
"""

_JS = r"""
(() => {
    const VERSION = 7;
    const DESKTOP_MIN = 1367;
    const M = 12;
    const scoopDocs = () => {
        const docs = [document];
        try {
            if (window.parent && window.parent.document && window.parent.document !== document) {
                docs.push(window.parent.document);
            }
        } catch (e) {}
        return docs;
    };
    const tableDoc = () => scoopDocs().find((d) => d.querySelector(".full-results-wrap")) || document;
    let appDoc = tableDoc();
    let appWin = window;
    try {
        if (appDoc.defaultView) appWin = appDoc.defaultView;
        else if (window.parent && window.parent !== window) appWin = window.parent;
    } catch (e) {}
    appWin.__scoopDesktopHlNarrowV = VERSION;

    const isDesktop = () => {
        let w = window.innerWidth || 0;
        try { if (window.parent && window.parent.innerWidth) w = Math.max(w, window.parent.innerWidth); } catch (e) {}
        return w >= DESKTOP_MIN;
    };
    const inView = (r) => {
        const vh = appWin.innerHeight || 800;
        const vw = appWin.innerWidth || 1600;
        return r && r.width > 40 && r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw;
    };

    const headlinesTh = () => [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) => {
        const t = (th.textContent || "").replace(/\s+/g, " ").trim();
        return t.startsWith("Headlines") && !t.startsWith("Headline ");
    }) || null;

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
            clone.querySelectorAll(".tip-text").forEach((n) => n.remove());
            return (clone.textContent || "").replace(/\s+/g, " ").trim();
        }
        return (valueCell.textContent || "").replace(/\s+/g, " ").trim();
    };

    const place = (wrap) => {
        if (!isDesktop() || !wrap) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        wrap.classList.add("hl-tip-desktop-open");
        appWin.__scoopDesktopHlOpenedAt = Date.now();
        const heading = tip.querySelector(".hl-tip-heading");
        if (heading) {
            const company = companyName(wrap);
            heading.textContent = company ? `${headingBase(heading)} - ${company}` : headingBase(heading);
        }
        const ths = [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")];
        const moodTh = ths.find((el) => (el.textContent || "").replace(/\s+/g, " ").trim().startsWith("Market Mood"));
        const moodTds = [...appDoc.querySelectorAll('.full-results-wrap td[data-label="Market Mood"]')];
        const vis = moodTds.map((el) => el.getBoundingClientRect()).filter(inView);
        const thRect = moodTh ? moodTh.getBoundingClientRect() : null;
        const table = appDoc.querySelector(".full-results-wrap .full-results-table");
        const tbody = table && table.tBodies && table.tBodies[0];
        const vw = appWin.innerWidth || 1600;
        const vh = appWin.innerHeight || 900;
        const tableBottom = tbody
            ? tbody.getBoundingClientRect().bottom
            : (table ? table.getBoundingClientRect().bottom : vh - M);
        const MIN_W = 280;
        const EXTRA_W = 130;
        const MIN_H = 280;
        let left = M;
        let width = MIN_W;
        let top = M;
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
        if (top < M) top = M;
        if (left < M) left = M;
        if (left + width > vw - M) width = Math.max(MIN_W + EXTRA_W, vw - M - left);
        let height = Math.round(Math.min(tableBottom, vh - M) - top);
        if (vis.length) {
            height = Math.max(height, Math.round(Math.max(...vis.map((r) => r.bottom)) - top));
        }
        if (top + height > vh - M) height = Math.round(vh - M - top);
        height = Math.max(MIN_H, height);

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("left", left + "px", "important");
        tip.style.setProperty("top", top + "px", "important");
        tip.style.setProperty("width", width + "px", "important");
        tip.style.setProperty("max-width", width + "px", "important");
        tip.style.setProperty("min-width", "410px", "important");
        tip.style.setProperty("height", height + "px", "important");
        tip.style.setProperty("max-height", height + "px", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("--hl-fixed-left", left + "px");
        tip.style.setProperty("--hl-fixed-top", top + "px");
        tip.style.setProperty("--hl-fixed-width", width + "px");
        tip.style.setProperty("--hl-fixed-height", height + "px");
        tip.style.setProperty("--hl-fixed-max-height", height + "px");

        const scroll = tip.querySelector(".headlines-tip-scroll");
        const headingEl = tip.querySelector(".hl-tip-heading");
        const headingH = headingEl ? headingEl.offsetHeight : 48;
        if (scroll) {
            const scrollH = Math.max(80, height - headingH);
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("height", scrollH + "px", "important");
            scroll.style.setProperty("max-height", scrollH + "px", "important");
            scroll.style.setProperty("min-height", "0", "important");
            scroll.style.setProperty("visibility", "visible", "important");
        }
    };

    const onClick = (event) => {
        if (!isDesktop() || !event.target || !event.target.closest) return;
        const label = event.target.closest(".hl-tip-count");
        if (!label) return;
        const wrap = label.closest(".tip-wrap.headlines-tip");
        if (!wrap) return;
        const run = () => place(wrap);
        run();
        appWin.requestAnimationFrame(run);
        appWin.setTimeout(run, 40);
        appWin.setTimeout(run, 180);
    };

    const onChange = (event) => {
        if (!isDesktop() || !event.target || !event.target.classList) return;
        if (!event.target.classList.contains("hl-tip-cb")) return;
        const wrap = event.target.closest(".tip-wrap.headlines-tip");
        if (event.target.checked) place(wrap);
    };

    if (appWin.__scoopHlNarrowClick) {
        scoopDocs().forEach((d) => {
            d.removeEventListener("click", appWin.__scoopHlNarrowClick, true);
            d.removeEventListener("change", appWin.__scoopHlNarrowChange, true);
        });
    }
    appWin.__scoopHlNarrowClick = onClick;
    appWin.__scoopHlNarrowChange = onChange;
    scoopDocs().forEach((d) => {
        d.addEventListener("click", onClick, true);
        d.addEventListener("change", onChange, true);
    });
})();
"""


def inject_desktop_headlines_narrow() -> None:
    st.html(
        f"<style id='scoop-desktop-hl-narrow'>{_CSS}</style>"
        f"<script id='scoop-desktop-hl-narrow-js'>{_JS}</script>",
        unsafe_allow_javascript=True,
    )
