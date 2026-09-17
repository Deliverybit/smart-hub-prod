"""Desktop-only: company name tooltips + Headlines panel position/content."""

from __future__ import annotations

import streamlit as st

_CSS = """
@media (min-width: 1367px) {
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text {
        display: flex !important;
        flex-direction: column !important;
        visibility: visible !important;
        opacity: 1 !important;
        overflow: hidden !important;
        width: var(--hl-fixed-width, 160px) !important;
        max-width: var(--hl-fixed-width, 160px) !important;
        min-width: 0 !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .headlines-tip-scroll,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .headlines-tip-scroll {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        min-height: 5rem !important;
        overflow-y: auto !important;
        pointer-events: auto !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line a,
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line a {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #ffffff !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line a,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stAppViewContainer"] .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
}
"""

_JS = r"""
(() => {
    const VERSION = 9;
    const DESKTOP_MIN = 1367;
    const OPEN_CLASS = "scoop-desktop-name-tip-open";
    const PAD = 12;
    const RIGHT_GAP = 12;
    const ABOVE_HEADING = 30;
    const NARROW_W = 264;
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
    appWin.__scoopDesktopScreenerTipsV = VERSION;

    const isDesktop = () => {
        let w = window.innerWidth || 0;
        try { if (window.parent && window.parent.innerWidth) w = Math.max(w, window.parent.innerWidth); } catch (e) {}
        return w >= DESKTOP_MIN;
    };

    const isNameTip = (wrap) => {
        if (!wrap || !wrap.classList || wrap.classList.contains("headlines-tip")) return false;
        if (wrap.classList.contains("scoop-name-tip")) return true;
        const td = wrap.closest('td[data-label="Company"], td[data-label="Name"], td[data-label="Commodity"]');
        return !!(td && wrap.closest(".fr-val"));
    };

    const clearNameTip = (wrap) => {
        if (!wrap) return;
        wrap.classList.remove(OPEN_CLASS);
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        ["position","left","top","right","bottom","transform","width","max-width","min-width",
         "visibility","opacity","z-index","pointer-events"].forEach((p) => tip.style.removeProperty(p));
        tip.style.setProperty("visibility", "hidden", "important");
        tip.style.setProperty("opacity", "0", "important");
        tip.style.setProperty("left", "-10000px", "important");
        tip.style.setProperty("top", "-10000px", "important");
        tip.style.setProperty("transition", "none", "important");
    };

    const positionNameTip = (wrap) => {
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip || !isDesktop() || !wrap.classList.contains(OPEN_CLASS)) return;
        const sidebar = appDoc.querySelector('section[data-testid="stSidebar"]');
        const sbRight = sidebar ? sidebar.getBoundingClientRect().right : 0;
        const viewRight = Math.min(appWin.innerWidth - PAD, (appDoc.documentElement && appDoc.documentElement.clientWidth) || appWin.innerWidth) - PAD;
        const minW = 360;
        const maxW = Math.max(minW, Math.min(700, viewRight - (sbRight + PAD)));
        const anchor = wrap.getBoundingClientRect();
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
        tip.style.setProperty("font-size", "1.25rem", "important");
        tip.style.setProperty("line-height", "1.55", "important");
        tip.style.setProperty("padding", "1.15rem 1.35rem", "important");
        tip.style.setProperty("min-width", `${minW}px`, "important");
        tip.style.setProperty("max-width", `${maxW}px`, "important");
        tip.style.setProperty("width", "auto", "important");
        const tipRect = tip.getBoundingClientRect();
        const height = tipRect.height || 72;
        const width = Math.max(minW, Math.min(maxW, tipRect.width || minW));
        let left = anchor.left + anchor.width / 2 - width / 2;
        if (left < sbRight + PAD) left = sbRight + PAD;
        if (left + width > viewRight) left = Math.max(sbRight + PAD, viewRight - width);
        let top = anchor.top - height - 12;
        if (top < PAD) top = Math.min(appWin.innerHeight - height - PAD, anchor.bottom + 12);
        tip.style.setProperty("left", `${Math.round(left)}px`, "important");
        tip.style.setProperty("top", `${Math.round(top)}px`, "important");
    };

    const openNameTip = (wrap) => {
        if (!isDesktop() || !isNameTip(wrap)) return;
        appDoc.querySelectorAll(".tip-wrap." + OPEN_CLASS).forEach((other) => {
            if (other !== wrap) clearNameTip(other);
        });
        wrap.classList.add(OPEN_CLASS);
        const tip = wrap.querySelector(":scope > .tip-text");
        if (tip) {
            tip.style.setProperty("display", "block", "important");
        }
        positionNameTip(wrap);
        appWin.requestAnimationFrame(() => positionNameTip(wrap));
    };

    const headlinesTh = () => {
        return [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) => {
            const t = (th.textContent || "").replace(/\s+/g, " ").trim();
            return t.startsWith("Headlines") && !t.startsWith("Headline ");
        }) || null;
    };

    const slotFor = (wrap, tipHeight = 0) => {
        const viewH = appWin.innerHeight || 800;
        const viewW = appWin.innerWidth || 1600;
        const moodTh = [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) =>
            (th.textContent || "").replace(/\s+/g, " ").trim().startsWith("Market Mood")
        );
        const moodTd = appDoc.querySelector('.full-results-wrap td[data-label="Market Mood"]');
        const mood = (moodTh && moodTh.getBoundingClientRect().width > 24)
            ? moodTh.getBoundingClientRect()
            : (moodTd ? moodTd.getBoundingClientRect() : null);
        const table = appDoc.querySelector(".full-results-wrap .full-results-table");
        const tbody = table && table.tBodies && table.tBodies[0];
        const tableBottom = tbody
            ? tbody.getBoundingClientRect().bottom
            : (table ? table.getBoundingClientRect().bottom : viewH - PAD);
        let left = PAD;
        let width = 160;
        let top = PAD;
        if (mood && mood.width > 0) {
            left = Math.round(mood.left);
            width = Math.round(mood.width);
            top = Math.round(mood.top - 8);
        }
        if (top < PAD) top = PAD;
        if (left < PAD) left = PAD;
        if (left + width > viewW - PAD) width = Math.max(120, viewW - PAD - left);
        let maxHeight = Math.round(tableBottom - top);
        if (top + maxHeight > viewH - PAD) maxHeight = Math.round(viewH - PAD - top);
        maxHeight = Math.max(160, maxHeight);
        return { top, left, width, maxHeight, colRight: left + width };
    };

    const applySlot = (tip, slot) => {
        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("left", `${slot.left}px`, "important");
        tip.style.setProperty("top", `${slot.top}px`, "important");
        tip.style.setProperty("width", `${slot.width}px`, "important");
        tip.style.setProperty("max-width", `${slot.width}px`, "important");
        tip.style.setProperty("min-width", "0", "important");
        tip.style.setProperty("right", "auto", "important");
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
        tip.style.removeProperty("height");
        if (scroll) {
            scroll.style.removeProperty("height");
            scroll.style.removeProperty("max-height");
        }
        const headingHeight = heading ? heading.offsetHeight : 0;
        const list = scroll && scroll.querySelector(".headlines-tip-list");
        const listHeight = list ? list.scrollHeight : (scroll ? scroll.scrollHeight : 0);
        const contentHeight = Math.max(tip.scrollHeight, headingHeight + listHeight + 24);
        const usable = Math.max(280, slot.maxHeight);
        const needsScroll = contentHeight > usable + 1;
        const tipHeight = needsScroll ? usable : Math.max(contentHeight, headingHeight + 80);
        tip.style.setProperty("--hl-fixed-height", `${tipHeight}px`);
        tip.style.setProperty("height", `${tipHeight}px`, "important");
        if (scroll) {
            const scrollHeight = Math.max(120, tipHeight - headingHeight);
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("flex", "1 1 auto", "important");
            scroll.style.setProperty("min-height", "5rem", "important");
            scroll.style.setProperty("height", `${scrollHeight}px`, "important");
            scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
            scroll.style.setProperty("visibility", "visible", "important");
            scroll.style.setProperty("opacity", "1", "important");
        }
        return tipHeight;
    };

    const applyHeadlines = (wrap) => {
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
        let slot = slotFor(wrap);
        applySlot(tip, slot);
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        const tipHeight = fitTip(tip, slot);
        slot = slotFor(wrap, tipHeight);
        applySlot(tip, slot);
        fitTip(tip, slot);
    };

    const onNameOver = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        const wrap = event.target.closest(".tip-wrap:not(.headlines-tip)");
        if (!wrap || !isNameTip(wrap)) return;
        openNameTip(wrap);
    };

    const onNameOut = (event) => {
        if (!event || !event.target || !event.target.closest) return;
        const wrap = event.target.closest(".tip-wrap:not(.headlines-tip)");
        if (!wrap || !wrap.classList.contains(OPEN_CLASS)) return;
        const related = event.relatedTarget;
        if (related && wrap.contains(related)) return;
        // relatedTarget is often null while moving across text nodes; keep the tip if still hovered.
        try {
            if (wrap.matches(":hover")) return;
        } catch (e) {}
        clearNameTip(wrap);
    };

    const httpWin = () => {
        const cands = [window];
        try { if (window.parent) cands.push(window.parent); } catch (e) {}
        try { if (window.top) cands.push(window.top); } catch (e) {}
        for (let i = cands.length - 1; i >= 0; i -= 1) {
            const w = cands[i];
            try {
                const href = w.location && w.location.href;
                if (href && /^https?:/i.test(href)) return w;
            } catch (e) {}
        }
        return window;
    };

    const goAnalyze = (link) => {
        const ticker = (link.getAttribute("data-ticker") || "").trim();
        if (!ticker) return false;
        const w = httpWin();
        let origin = "";
        let path = "/";
        try {
            origin = w.location.origin || "";
            path = w.location.pathname || "/";
        } catch (e) {
            return false;
        }
        if (!origin) return false;
        const knownFrom = ["NYSE_Top_10", "NASDAQ_Top_10", "Crypto_Top_10", "CME_Top_10", "ICE_Top_10"];
        let fromPath = "/NYSE_Top_10";
        for (const slug of knownFrom) {
            if (path.indexOf(slug) !== -1) {
                fromPath = "/" + slug;
                break;
            }
        }
        let theme = "light";
        try {
            if ((w.sessionStorage && w.sessionStorage.getItem("scoop-theme")) === "dark") theme = "dark";
        } catch (e) {}
        try {
            w.sessionStorage.setItem("scoop-analyze-from", fromPath);
        } catch (e) {}
        const prefix = String(path).replace(/[^/]*$/, "");
        const dest = origin + prefix + "Analyze?ticker=" + encodeURIComponent(ticker)
            + "&from=" + encodeURIComponent(fromPath)
            + "&theme=" + encodeURIComponent(theme);
        try {
            w.location.assign(dest);
            return true;
        } catch (e) {
            try {
                w.location.href = dest;
                return true;
            } catch (e2) {
                return false;
            }
        }
    };

    const onAnalyzeNav = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        const el = event.target.nodeType === 1 ? event.target : event.target.parentElement;
        if (!el || !el.closest) return;
        const analyzeCell = el.closest('td[data-label="Analyze"]');
        const link = el.closest("a.fr-analyze-link") || (analyzeCell && analyzeCell.querySelector("a.fr-analyze-link"));
        if (!link) return;
        if (goAnalyze(link)) {
            event.preventDefault();
            if (event.stopImmediatePropagation) event.stopImmediatePropagation();
        }
    };

    const onHlClick = (event) => {
        if (!isDesktop() || !event || !event.target || !event.target.closest) return;
        if (event.target.closest("a.fr-analyze-link, td[data-label='Analyze']")) return;
        const label = event.target.closest(".hl-tip-count");
        if (!label) return;
        const wrap = label.closest(".tip-wrap.headlines-tip");
        if (!wrap) return;
        appWin.__scoopDesktopHlOpenedAt = Date.now();
        const run = () => applyHeadlines(wrap);
        run();
        appWin.requestAnimationFrame(run);
        appWin.setTimeout(run, 50);
        appWin.setTimeout(run, 200);
    };

    const onHlChange = (event) => {
        if (!isDesktop() || !event || !event.target) return;
        if (!event.target.classList || !event.target.classList.contains("hl-tip-cb")) return;
        const wrap = event.target.closest(".tip-wrap.headlines-tip");
        if (event.target.checked) applyHeadlines(wrap);
    };

    if (appWin.__scoopDesktopScreenerTipsOver) {
        scoopDocs().forEach((d) => {
            d.removeEventListener("mouseover", appWin.__scoopDesktopScreenerTipsOver, true);
            d.removeEventListener("mouseout", appWin.__scoopDesktopScreenerTipsOut, true);
            d.removeEventListener("click", appWin.__scoopDesktopScreenerTipsClick, true);
            d.removeEventListener("change", appWin.__scoopDesktopScreenerTipsChange, true);
            d.removeEventListener("click", appWin.__scoopDesktopAnalyzeNav, true);
            d.removeEventListener("pointerdown", appWin.__scoopDesktopAnalyzeNav, true);
        });
    }
    appWin.__scoopDesktopScreenerTipsOver = onNameOver;
    appWin.__scoopDesktopScreenerTipsOut = onNameOut;
    appWin.__scoopDesktopScreenerTipsClick = onHlClick;
    appWin.__scoopDesktopScreenerTipsChange = onHlChange;
    appWin.__scoopDesktopAnalyzeNav = onAnalyzeNav;
    scoopDocs().forEach((d) => {
        d.addEventListener("mouseover", onNameOver, true);
        d.addEventListener("mouseout", onNameOut, true);
        d.addEventListener("click", onHlClick, true);
        d.addEventListener("change", onHlChange, true);
        d.addEventListener("click", onAnalyzeNav, true);
        d.addEventListener("pointerdown", onAnalyzeNav, true);
    });
})();
"""


def inject_desktop_screener_tips() -> None:
    st.html(
        f"<style id='scoop-desktop-screener-tips-css'>{_CSS}</style>"
        f"<script id='scoop-desktop-screener-tips'>{_JS}</script>",
        unsafe_allow_javascript=True,
    )
