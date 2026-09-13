"""Desktop company name tips stay compact/portrait, not a horizontal strip."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_css_caps_company_tip_width() -> None:
    from tooltip_scroll import _DESKTOP_TOOLTIP_TYPE_CSS

    css = _DESKTOP_TOOLTIP_TYPE_CSS
    assert "@media (min-width: 1367px)" in css
    assert "scoop-name-tip" in css
    assert "min-width: 360px !important" in css
    assert "max-width: min(700px, calc(100vw - 2rem)) !important" in css
    assert "font-size: 1.25rem !important" in css
    assert "line-height: 1.55 !important" in css
    assert "font-size: 16px !important" not in css
    assert "width: 220px !important" not in css


def main() -> int:
    test_css_caps_company_tip_width()
    from playwright.sync_api import sync_playwright

    url = os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NASDAQ_Top_10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        agree = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
        if agree.count():
            agree.locator("label").first.click(force=True, position={"x": 8, "y": 8})
            page.wait_for_timeout(8000)
        page.wait_for_selector(".full-results-wrap .scoop-name-tip", timeout=90000)
        page.wait_for_timeout(400)
        name = page.locator(".full-results-wrap .scoop-name-tip").first
        name.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        name.hover()
        page.wait_for_timeout(500)
        info = page.evaluate(
            """() => {
              const wrap = document.querySelector(".scoop-name-tip.scoop-desktop-name-tip-open")
                || document.querySelector(".scoop-name-tip:hover");
              const tips = [...document.querySelectorAll(".scoop-name-tip > .tip-text")].filter((el) => {
                const cs = getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return cs.visibility === "visible" && Number(cs.opacity) > 0.5 && r.width > 8 && r.top > -1000;
              });
              return {
                w: window.innerWidth,
                count: tips.length,
                sizes: tips.map((el) => {
                  const r = el.getBoundingClientRect();
                  return { width: Math.round(r.width), height: Math.round(r.height), whiteSpace: getComputedStyle(el).whiteSpace };
                }),
              };
            }"""
        )
        print(info)
        browser.close()

    if info.get("w", 0) < 1367:
        raise SystemExit("FAIL not desktop")
    if info.get("count", 0) < 1:
        raise SystemExit(f"FAIL no visible company tip: {info}")
    if info.get("count", 0) > 1:
        raise SystemExit(f"FAIL two company tip formats visible: {info}")
    size = info["sizes"][0]
    if size["width"] < 350 or size["width"] > 720:
        raise SystemExit(f"FAIL table tip should match Top Picks 360–700px box: {info}")
    if size["whiteSpace"] == "nowrap":
        raise SystemExit(f"FAIL horizontal nowrap tip: {info}")
    print("PASS desktop company tip compact portrait only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
