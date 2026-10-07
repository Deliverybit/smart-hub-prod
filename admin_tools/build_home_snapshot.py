"""Save the phone/tablet home page from a Streamlit browser dump."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HTML_SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "preview" / "index.html"
ORIGINS = ("http://localhost:8501", "http://127.0.0.1:8501")

html = json.loads(HTML_SRC.read_text(encoding="utf-8"))["result"]["value"]
html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)
html = re.sub(
    r'(href|src)="(?!https?:|data:|#|mailto:)([^"]+)"',
    lambda m: f'{m.group(1)}="{ORIGINS[0]}/{m.group(2).lstrip("./")}"',
    html,
)
for origin in ORIGINS:
    for streamlit_path, preview_file in (
        ("/NYSE_Top_10", "nyse.html"),
        ("/NASDAQ_Top_10", "nasdaq.html"),
        ("/Crypto_Top_10", "crypto.html"),
        ("/CME_Top_10", "cme.html"),
        ("/ICE_Top_10", "ice.html"),
    ):
        html = html.replace(f"{origin}{streamlit_path}", preview_file)
    html = html.replace(f'href="{origin}/"', 'href="index.html"')

extra = """
<style id="scoop-home-fit">
@font-face {
  font-family: "Source Sans";
  font-weight: 100 900;
  font-style: normal;
  src: url("http://localhost:8501/static/media/SourceSansVF-Upright.ttf.BsWL4Kly.woff2") format("woff2");
}
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"],
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] #scoop-title,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .sidebar-brand-text,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .scoop-home-landing,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .scoop-home-landing p,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"],
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] a,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] p,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] span,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] label,
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] p {
  font-family: "Source Sans", sans-serif !important;
  letter-spacing: 0 !important;
}
html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  overflow-x: hidden;
}
html[data-scoop-home-page="1"] .withScreencast,
html[data-scoop-home-page="1"] [data-testid="stApp"],
html[data-scoop-home-page="1"] [data-testid="stAppViewContainer"],
html[data-scoop-home-page="1"] [data-testid="stMain"],
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] {
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  box-sizing: border-box !important;
}
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMain"],
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"],
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stAppViewContainer"] {
  max-height: none !important;
  height: auto !important;
  overflow: visible !important;
}
html[data-scoop-home-page="1"] [data-testid="stElementToolbar"],
html[data-scoop-home-page="1"] [data-testid="stTooltipIcon"] {
  display: none !important;
}
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"],
html[data-scoop-home-page="1"] [data-testid="stVerticalBlock"],
html[data-scoop-home-page="1"] .scoop-home-landing,
html[data-scoop-home-page="1"] .scoop-home-landing p {
  max-width: 100% !important;
  box-sizing: border-box !important;
  white-space: normal !important;
  overflow-wrap: anywhere !important;
}
html[data-scoop-home-page="1"] [data-testid="stCheckbox"] input {
  position: absolute !important;
  opacity: 0 !important;
  width: 1px !important;
  height: 1px !important;
  margin: 0 !important;
  pointer-events: none !important;
}
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  padding: 2px !important;
  box-sizing: border-box !important;
  cursor: pointer !important;
  background: #cbd5e1 !important;
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type {
  background: #60a5fa !important;
}
html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type > div {
  margin-left: 0 !important;
  margin-right: auto !important;
  transform: none !important;
  transition: margin 0.15s ease !important;
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label > div:first-of-type > div {
  margin-left: auto !important;
  margin-right: 0 !important;
}
html[data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"] {
  display: flex !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  text-decoration: none !important;
  white-space: normal !important;
  overflow-wrap: anywhere !important;
  background: #fff !important;
  color: #31333f !important;
  border: 1px solid #7dd3fc !important;
  border-radius: 0.5rem !important;
  padding: 0.45rem 0.8rem !important;
  margin: 0.3rem 0 !important;
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"],
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"] p {
  background: #262730 !important;
  color: #fafafa !important;
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"] {
  border: 1px solid #7dd3fc !important;
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"] p {
  border: none !important;
}
@media (max-width: 743px) {
  html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href="nyse.html"]),
  html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href="nyse.html"]) a {
    margin-top: 1rem !important;
  }
}
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"][aria-current="page"],
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"]:active,
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"][aria-current="page"] p,
html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stPageLink-NavLink"]:active p {
  background: #3d424d !important;
  color: #fafafa !important;
}
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] a,
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] a span,
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] a p {
  font-size: 1rem !important;
  line-height: 1.25 !important;
  min-height: 0 !important;
  height: auto !important;
}
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stPageLink"] a p {
  margin: 0 !important;
}
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMain"] [data-testid="stImage"],
html[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMain"] [data-testid="stImage"] img {
  max-height: 6.5rem !important;
  width: auto !important;
  object-fit: contain !important;
}
html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"][data-scoop-tab-nav="1"] body [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html[data-scoop-theme="dark"][data-scoop-tab-nav="1"][data-scoop-home-page="1"] body [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html:not([data-scoop-theme="dark"]) body [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]),
html[data-scoop-theme="dark"] body [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]) {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}
</style>
<script>
if (window.innerWidth >= 1367) {
  window.location.replace("nyse.html");
}
window.addEventListener("resize", function () {
  if (window.innerWidth >= 1367 && !/nyse\.html$/.test(window.location.pathname)) {
    window.location.replace("nyse.html");
  }
});
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
document.addEventListener("click", function (event) {
  var link = event.target.closest && event.target.closest('[data-testid="stPageLink-NavLink"]');
  if (!link || !link.getAttribute("href") || link.getAttribute("href").indexOf(".html") === -1) return;
  document.querySelectorAll('[data-testid="stPageLink-NavLink"]').forEach(function (el) {
    el.removeAttribute("aria-current");
  });
  link.setAttribute("aria-current", "page");
});
</script>
"""
for origin in ORIGINS:
    html = html.replace(
        f"{origin}/media/e84614c848ece5e96dfb8d839d84c62ba8c59d5e8ab7596167c388a1.png",
        "logo.png",
    )
html = html.replace("<head>", '<head><script>try{if(localStorage.getItem("scoop-theme")==="dark")document.documentElement.setAttribute("data-scoop-theme","dark")}catch(e){}</script>', 1)
html = html.replace("</body>", extra + "</body>")
OUT.write_text("<!DOCTYPE html>\n" + html, encoding="utf-8")
print(OUT, OUT.stat().st_size)
