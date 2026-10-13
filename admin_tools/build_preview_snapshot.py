"""Build a styled comparison copy of the captured Streamlit page."""
from __future__ import annotations

import json
import re
from pathlib import Path

LOGS = Path(r"C:\Users\hakee\.cursor\browser-logs")
HTML_SRC = LOGS / "cdp-response-Runtime.evaluate-2026-10-05T04-02-32-028Z.json"
CSS_SRC = LOGS / "cdp-response-Runtime.evaluate-2026-10-05T04-02-20-758Z.json"
OUT = Path(__file__).resolve().parents[1] / "preview" / "nyse.html"
ORIGIN = "http://localhost:8501"

html = json.loads(HTML_SRC.read_text(encoding="utf-8"))["result"]["value"]
css = json.loads(CSS_SRC.read_text(encoding="utf-8"))["result"]["value"]
html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)
html = re.sub(
    r"(href|src)=\"(?!https?:|data:|#|mailto:)([^\"]+)\"",
    lambda m: f'{m.group(1)}="{ORIGIN}/{m.group(2).lstrip("./")}"',
    html,
)
html = html.replace(
    "</head>",
    "<style id=\"scoop-snapshot-css\">\n" + css + "\n</style>\n</head>",
    1,
)
hook = """
<script>
document.addEventListener("click", function (event) {
  var text = (event.target.innerText || "").trim();
  if (text === "Dark mode" || text === "Dark") {
    var root = document.documentElement;
    var dark = root.getAttribute("data-scoop-theme") !== "dark";
    root.setAttribute("data-scoop-theme", dark ? "dark" : "light");
    event.preventDefault();
    event.stopPropagation();
  }
});
</script>
"""
html = html.replace("</body>", hook + "</body>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("<!DOCTYPE html>\n" + html, encoding="utf-8")
print(OUT, OUT.stat().st_size)
