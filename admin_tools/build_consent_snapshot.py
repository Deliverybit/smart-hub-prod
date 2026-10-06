"""Build a test snapshot with a normal HTML consent checkbox."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

LOGS = Path(r"C:\Users\hakee\.cursor\browser-logs")
HTML_SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else LOGS / "cdp-response-Runtime.evaluate-2026-10-05T04-23-39-515Z.json"
CSS_SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else LOGS / "cdp-response-Runtime.evaluate-2026-10-05T04-23-39-445Z.json"
OUT = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).resolve().parents[1] / "preview" / "nyse.html"
ORIGIN = "http://localhost:8501"

html = json.loads(HTML_SRC.read_text(encoding="utf-8"))["result"]["value"]
css = json.loads(CSS_SRC.read_text(encoding="utf-8"))["result"]["value"]
html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)
html = re.sub(
    r'(href|src)="(?!https?:|data:|#|mailto:)([^"]+)"',
    lambda m: f'{m.group(1)}="{ORIGIN}/{m.group(2).lstrip("./")}"',
    html,
)
html = re.sub(r"<html\b", '<html data-scoop-consent="0"', html, count=1)
for streamlit_path, preview_file in (
    ("/NYSE_Top_10", "nyse.html"),
    ("/NASDAQ_Top_10", "nasdaq.html"),
    ("/Crypto_Top_10", "crypto.html"),
    ("/CME_Top_10", "cme.html"),
    ("/ICE_Top_10", "ice.html"),
):
    html = html.replace(f"{ORIGIN}{streamlit_path}", preview_file)

gate = """
<div id="scoop-results" hidden></div>
<div id="scoop-html-gate">
  <p class="scoop-html-warn">Please agree to the <strong>Disclaimer &amp; Terms of Service</strong> to view results.</p>
  <p><a class="scoop-html-terms" href="http://localhost:8501/Terms_of_Service">Disclaimer &amp; Terms</a></p>
  <label class="scoop-html-check">
    <input id="scoop-consent" type="checkbox">
    <span>I agree to the Disclaimer &amp; Terms</span>
  </label>
</div>
"""
html = re.sub(r"<body\b([^>]*)>", lambda m: "<body" + m.group(1) + ">" + gate, html, count=1)
html = html.replace(
    "</head>",
    "<style id=\"scoop-snapshot-css\">\n" + css + "\n</style>\n</head>",
    1,
)
extra = """
<style id="scoop-html-gate-css">
#scoop-html-gate { margin: 0.75rem 0 1rem; }
html[data-scoop-theme="dark"] #scoop-html-gate .scoop-html-warn,
html[data-scoop-theme="dark"] #scoop-html-gate .scoop-html-warn p,
html[data-scoop-theme="dark"] #scoop-html-gate .scoop-html-warn strong,
.scoop-html-warn,
.scoop-html-warn p,
.scoop-html-warn strong {
  background: #fff3cd;
  color: #664d03 !important;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  margin: 0 0 0.75rem;
}
.scoop-html-warn p,
.scoop-html-warn strong {
  padding: 0;
  margin: 0;
  border-radius: 0;
}
.scoop-html-terms { color: #1d4ed8; font-weight: 600; }
.scoop-html-check {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #0f172a;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 0.7rem 0.9rem;
  width: fit-content;
}
.scoop-html-check input { width: 1.05rem; height: 1.05rem; }
html[data-scoop-consent="0"] .scoop-hold { display: none !important; }
html[data-scoop-consent="1"] #scoop-html-gate { display: none !important; }
@media (max-width: 1366px) {
  .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text {
    visibility: visible !important;
    opacity: 1 !important;
    display: block !important;
    position: fixed !important;
    left: 8px !important;
    right: 8px !important;
    top: 12vh !important;
    width: auto !important;
    max-width: none !important;
    z-index: 100003 !important;
    pointer-events: auto !important;
  }
}
</style>
<style id="scoop-terms-border">
html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html[data-scoop-theme="dark"][data-scoop-tab-nav="1"][data-scoop-home-page="1"] body [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html:not([data-scoop-theme="dark"]) body [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html[data-scoop-theme="dark"] body [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]) {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}
</style>
<style id="scoop-desktop-toggle">
html:not([data-scoop-theme="dark"]) body [data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type,
html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] body [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type {
  background: #94a3b8 !important;
  border-radius: 999px !important;
}
html[data-scoop-theme="dark"] body [data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type,
html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type {
  background: #38bdf8 !important;
  border-radius: 999px !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding: 2px !important;
  box-sizing: border-box !important;
  cursor: pointer !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type > div {
  margin-left: 0 !important;
  margin-right: auto !important;
  transform: none !important;
  transition: margin 0.15s ease !important;
}
html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type > div {
  margin-left: auto !important;
  margin-right: 0 !important;
}
</style>
<style id="scoop-tip-names">
html body .tip-text > .scoop-tip-title,
html body .tip-wrap.headlines-tip .hl-tip-heading {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 3 !important;
  flex: 0 0 auto !important;
  font-weight: 700 !important;
  line-height: 1.25 !important;
  margin: 0 0 0.45rem 0 !important;
  padding: 0 0 0.4rem 0 !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.45) !important;
  background: #1e1e2f !important;
  color: #f8fafc !important;
}
@media (min-width: 1367px) {
  html body .scoop-tip-title { display: block !important; }
}
</style>
<script>
var gate = document.getElementById("scoop-html-gate");
var updated = [...document.querySelectorAll(".scoop-screener-last-updated")].find(function (el) {
  var host = el.closest("[data-testid='stElementContainer']") || el;
  return getComputedStyle(host).display !== "none";
}) || document.querySelector(".scoop-screener-last-updated");
if (gate && updated) {
  var host = updated.closest("[data-testid='stElementContainer']") || updated.parentElement;
  var parent = host.parentElement;
  parent.insertBefore(gate, host);
  var hold = false;
  [...parent.children].forEach(function (child) {
    if (child === host) {
      hold = true;
      return;
    }
    if (child === gate) return;
    if (child.querySelector && child.querySelector(".disclaimer-footer")) {
      hold = false;
      return;
    }
    if (hold) child.classList.add("scoop-hold");
  });
  document.querySelectorAll(".scoop-hold").forEach(function (el) {
    el.style.setProperty("display", "none", "important");
  });
}
function scoopSetTheme(next) {
  var mode = next ? "dark" : "light";
  document.documentElement.setAttribute("data-scoop-theme", mode);
  try { localStorage.setItem("scoop-theme", mode); } catch (err) {}
  document.querySelectorAll("#scoop-mobile-dark-cb, input[aria-label='Dark mode']").forEach(function (input) {
    input.checked = next;
  });
}
try { if (localStorage.getItem("scoop-theme") === "dark") scoopSetTheme(true); } catch (err) {}
document.addEventListener("click", function (event) {
  var dark = event.target.closest && event.target.closest('[data-testid="stCheckbox"]');
  if (!dark || (dark.innerText || "").indexOf("Dark mode") === -1) return;
  var input = dark.querySelector("input");
  if (!input) return;
  event.preventDefault();
  scoopSetTheme(!input.checked);
});
document.addEventListener("change", function (event) {
  var input = event.target;
  if (!input) return;
  if (input.id === "scoop-mobile-dark-cb" || input.getAttribute("aria-label") === "Dark mode") {
    scoopSetTheme(!!input.checked);
  }
});
function scoopNarrow() { return window.innerWidth <= 1366; }
function scoopDesktop() { return window.innerWidth >= 1367; }
function scoopPlaceHeaderTip(wrap, event) {
  scoopGenericTitle(wrap);
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip) return;
  tip.style.setProperty("display", "block", "important");
  tip.style.setProperty("visibility", "visible", "important");
  tip.style.setProperty("opacity", "1", "important");
  tip.style.setProperty("position", "fixed", "important");
  tip.style.setProperty("transform", "none", "important");
  tip.style.setProperty("width", "max-content", "important");
  tip.style.setProperty("min-width", "0", "important");
  tip.style.setProperty("max-width", "100px", "important");
  tip.style.setProperty("white-space", "normal", "important");
  tip.style.setProperty("overflow", "visible", "important");
  tip.style.setProperty("height", "auto", "important");
  tip.style.setProperty("max-height", "none", "important");
  tip.style.setProperty("z-index", "100050", "important");
  var x = event && event.clientX ? event.clientX : wrap.getBoundingClientRect().left;
  var y = event && event.clientY ? event.clientY : wrap.getBoundingClientRect().bottom;
  var left = Math.max(8, Math.min(x + 12, window.innerWidth - 108));
  var top = Math.max(8, y + 14);
  tip.style.setProperty("left", Math.round(left) + "px", "important");
  tip.style.setProperty("top", Math.round(top) + "px", "important");
}
function scoopCloseTips() {
  document.querySelectorAll(".tip-wrap:not(.headlines-tip)").forEach(function (wrap) {
    wrap.classList.remove("scoop-mobile-tip-open");
    var tip = wrap.querySelector(":scope > .tip-text");
    if (!tip) return;
    tip.style.setProperty("display", "none", "important");
    tip.style.setProperty("visibility", "hidden", "important");
    tip.style.setProperty("opacity", "0", "important");
  });
}
function scoopReleaseTip(wrap) {
  if (!wrap || wrap.classList.contains("scoop-mobile-tip-open") || wrap.classList.contains("headlines-tip")) return;
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip) return;
  tip.style.removeProperty("display");
  tip.style.removeProperty("visibility");
  tip.style.removeProperty("opacity");
}
function scoopCompanyName(wrap) {
  var row = wrap.closest("tr");
  if (!row) return "";
  var cell = row.querySelector('td[data-label="Company"] .fr-val, td[data-label="Name"] .fr-val, td[data-label="Commodity"] .fr-val');
  if (!cell) return "";
  var clone = cell.cloneNode(true);
  clone.querySelectorAll(".tip-text").forEach(function (node) { node.remove(); });
  return (clone.textContent || "").replace(/\s+/g, " ").trim();
}
function scoopHeadlineTitle(wrap) {
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip) return;
  var heading = tip.querySelector(".hl-tip-heading");
  if (!heading) {
    heading = document.createElement("span");
    heading.className = "hl-tip-heading";
    tip.insertBefore(heading, tip.firstChild);
  }
  if (!heading.getAttribute("data-hl-base")) {
    var current = (heading.textContent || "Headlines").trim().split(" - ")[0].trim() || "Headlines";
    heading.setAttribute("data-hl-base", current);
  }
  var company = scoopCompanyName(wrap);
  var base = heading.getAttribute("data-hl-base") || "Headlines";
  heading.textContent = company ? base + " - " + company : base;
}
function scoopGenericTitle(wrap) {
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip || wrap.classList.contains("headlines-tip")) return;
  var title = tip.querySelector(":scope > .scoop-tip-title");
  if (!title) {
    title = document.createElement("div");
    title.className = "scoop-tip-title";
    tip.insertBefore(title, tip.firstChild);
  }
  var td = wrap.closest("td[data-label]");
  var label = td ? (td.getAttribute("data-label") || "").trim() : "";
  var text = "";
  wrap.childNodes.forEach(function (node) {
    if (node.nodeType === 3) text += node.textContent || "";
  });
  text = text.replace(/\s+/g, " ").trim();
  var name = (label === "Company" || label === "Name" || label === "Commodity") ? text : (label || text);
  title.textContent = name;
}
function scoopStampTipNames() {
  document.querySelectorAll(".tip-wrap.headlines-tip").forEach(scoopHeadlineTitle);
  document.querySelectorAll(".tip-wrap:not(.headlines-tip)").forEach(scoopGenericTitle);
}
function scoopPlaceTip(wrap, y) {
  scoopGenericTitle(wrap);
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip) return;
  var tablet = window.innerWidth >= 744;
  var w = Math.round(window.innerWidth * 0.5);
  tip.style.setProperty("position", "fixed", "important");
  tip.style.setProperty("visibility", "visible", "important");
  tip.style.setProperty("opacity", "1", "important");
  tip.style.setProperty("display", "block", "important");
  tip.style.setProperty("pointer-events", "auto", "important");
  tip.style.setProperty("z-index", "100002", "important");
  tip.style.setProperty("width", w + "px", "important");
  tip.style.setProperty("max-width", w + "px", "important");
  var h = tip.getBoundingClientRect().height || 120;
  var raw = wrap.getBoundingClientRect();
  var top = Math.max(8, Math.min((y || raw.top) - h - 12, window.innerHeight - h - 8));
  var left = Math.max(8, (window.innerWidth - w) / 2);
  if (tablet) {
    left = raw.right + 12;
    if (left + w > window.innerWidth - 8) left = Math.max(8, raw.left - w - 12);
    top = Math.max(8, Math.min(raw.top, window.innerHeight - h - 8));
  }
  ["left", "--scoop-tablet-tip-left", "--scoop-mobile-tip-left"].forEach(function (prop) {
    tip.style.setProperty(prop, Math.round(left) + "px", "important");
  });
  ["top", "--scoop-tablet-tip-top", "--scoop-mobile-tip-top"].forEach(function (prop) {
    tip.style.setProperty(prop, Math.round(top) + "px", "important");
  });
}
function scoopHideHeadlines() {
  document.querySelectorAll(".tip-wrap.headlines-tip").forEach(function (other) {
    var box = other.querySelector(".hl-tip-cb");
    if (box) box.checked = false;
    other.classList.remove("hl-tip-desktop-open");
    var tip = other.querySelector(":scope > .tip-text");
    if (!tip) return;
    tip.style.setProperty("display", "none", "important");
    tip.style.setProperty("visibility", "hidden", "important");
    tip.style.setProperty("opacity", "0", "important");
  });
}
function scoopShowHeadlines(wrap) {
  scoopHeadlineTitle(wrap);
  var tip = wrap.querySelector(":scope > .tip-text");
  if (!tip) return;
  wrap.classList.add("hl-tip-desktop-open");
  tip.style.setProperty("display", "flex", "important");
  tip.style.setProperty("flex-direction", "column", "important");
  tip.style.setProperty("visibility", "visible", "important");
  tip.style.setProperty("opacity", "1", "important");
  tip.style.setProperty("pointer-events", "auto", "important");
  tip.style.setProperty("z-index", "100050", "important");
  tip.style.setProperty("overflow", "hidden", "important");
  var scroll = tip.querySelector(".headlines-tip-scroll");
  if (scroll) {
    scroll.style.setProperty("overflow-y", "auto", "important");
    scroll.style.setProperty("max-height", "60vh", "important");
    scroll.style.setProperty("pointer-events", "auto", "important");
  }
  tip.querySelectorAll(".hl-tip-line a").forEach(function (link) {
    link.style.setProperty("pointer-events", "auto", "important");
  });
  var margin = 12;
  var width = Math.min(480, window.innerWidth - margin * 2);
  var left = Math.max(margin, (window.innerWidth - width) / 2);
  var top = Math.max(margin, Math.round(window.innerHeight * 0.12));
  if (window.innerWidth >= 1367) {
    var mood = document.querySelector('.full-results-wrap td[data-label="Market Mood"]');
    var rect = mood ? mood.getBoundingClientRect() : null;
    if (rect && rect.width > 24 && rect.top > margin && rect.bottom < window.innerHeight - 180) {
      left = rect.left;
      width = Math.max(220, Math.min(rect.width, window.innerWidth - left - margin));
      top = rect.top;
    }
  }
  var maxH = Math.max(180, window.innerHeight - top - margin);
  tip.style.setProperty("position", "fixed", "important");
  tip.style.setProperty("left", Math.round(left) + "px", "important");
  tip.style.setProperty("top", Math.round(top) + "px", "important");
  tip.style.setProperty("width", Math.round(width) + "px", "important");
  tip.style.setProperty("max-width", Math.round(width) + "px", "important");
  tip.style.setProperty("max-height", Math.round(maxH) + "px", "important");
}
document.addEventListener("click", function (event) {
  var t = event.target;
  if (!t || !t.closest) return;
  if (t.closest(".tip-text a")) return;
  var count = t.closest(".hl-tip-count");
  var backdrop = t.closest(".hl-tip-backdrop");
  if (count || backdrop) {
    event.preventDefault();
    var wrap = (count || backdrop).closest(".tip-wrap.headlines-tip");
    if (!wrap) return;
    var cb = wrap.querySelector(".hl-tip-cb");
    var willOpen = !!(count && cb && !cb.checked);
    scoopCloseTips();
    scoopHideHeadlines();
    if (willOpen) {
      cb.checked = true;
      scoopShowHeadlines(wrap);
    }
    return;
  }
  if (scoopDesktop()) {
    if (!t.closest(".tip-wrap")) scoopHideHeadlines();
    return;
  }
  var wrap = t.closest(".tip-wrap");
  if (!wrap) {
    scoopCloseTips();
    scoopHideHeadlines();
    return;
  }
  if (wrap.classList.contains("headlines-tip")) return;
  if (t.closest(".tip-text")) return;
  event.preventDefault();
  var open = wrap.classList.contains("scoop-mobile-tip-open");
  scoopHideHeadlines();
  scoopCloseTips();
  if (!open) {
    wrap.classList.add("scoop-mobile-tip-open");
    scoopPlaceTip(wrap, event.clientY);
  }
});
document.addEventListener("mouseover", function (event) {
  var t = event.target;
  if (!t || !t.closest) return;
  var wrap = t.closest(".tip-wrap:not(.headlines-tip)");
  if (!wrap) return;
  scoopHideHeadlines();
  if (scoopDesktop() && wrap.closest("thead")) {
    var tip = wrap.querySelector(":scope > .tip-text");
    if (tip) {
      ["position", "left", "top", "right", "bottom", "width", "max-width", "min-width", "height", "max-height", "transform", "white-space", "overflow"].forEach(function (prop) {
        tip.style.removeProperty(prop);
      });
      tip.style.setProperty("display", "block", "important");
      tip.style.setProperty("visibility", "visible", "important");
      tip.style.setProperty("opacity", "1", "important");
    }
    wrap.classList.add("scoop-desktop-header-tip-open");
  }
});
document.addEventListener("mouseout", function (event) {
  var t = event.target;
  if (!t || !t.closest) return;
  var wrap = t.closest(".tip-wrap:not(.headlines-tip)");
  if (!wrap) return;
  var next = event.relatedTarget;
  if (next && wrap.contains(next)) return;
  wrap.classList.remove("scoop-desktop-header-tip-open");
  scoopReleaseTip(wrap);
});
document.addEventListener("scroll", function (event) {
  var target = event.target;
  if (target && target.closest && target.closest(".tip-text")) return;
  scoopCloseTips();
  scoopHideHeadlines();
}, true);
function scoopShowResults(on) {
  document.documentElement.setAttribute("data-scoop-consent", on ? "1" : "0");
  document.querySelectorAll(".scoop-hold").forEach(function (el) {
    if (on) el.style.removeProperty("display");
    else el.style.setProperty("display", "none", "important");
  });
}
document.addEventListener("change", function (event) {
  if (!event.target || event.target.id !== "scoop-consent") return;
  var box = event.target;
  if (!box.checked) {
    scoopShowResults(false);
    return;
  }
  box.disabled = true;
  var zone = "";
  try { zone = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (err) {}
  fetch("https://data.thescoop52.com/consent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ accepted: true, timezone: zone }),
  }).then(function (response) {
    if (!response.ok) throw new Error("consent");
    scoopShowResults(true);
  }).catch(function () {
    box.checked = false;
    scoopShowResults(false);
  }).then(function () {
    box.disabled = false;
  });
});
scoopStampTipNames();
</script>
"""
html = html.replace(
    "http://localhost:8501/media/4c18d1172d4aeaf3916c2c8f08575f00.png",
    "logo.png",
)
html = html.replace("<head>", '<head><script>try{if(localStorage.getItem("scoop-theme")==="dark")document.documentElement.setAttribute("data-scoop-theme","dark")}catch(e){}</script>', 1)
html = html.replace("</body>", extra + "</body>")
OUT.write_text("<!DOCTYPE html>\n" + html, encoding="utf-8")
print(OUT, OUT.stat().st_size)
