"""Phone/tablet: index cards on the market page only, full viewport width."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_responsive_css_hides_banners_on_gate() -> None:
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_SCREENER_TOP_COMPACT

    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert "@media (max-width: 1366px)" in css
    assert 'html[data-scoop-screener-gated="1"]' in css
    assert "display: none !important" in css
    assert 'html:not([data-scoop-screener-gated="1"])' in css
    assert "--scoop-tablet-gutter" in css
    assert "flex-direction: column !important" in css
    assert "flex-direction: row !important" in css
    assert 'html:has([class*="st-key-agree_terms"])' in css
    assert 'html:not([data-scoop-screener-gated="1"]):not(:has([class*="st-key-agree_terms"]))' in css
    assert "max-width: 100% !important" in css
    assert "min-width: 0 !important" in css
    assert "[style*=\"max-width:50%\"]" in css or '[style*="max-width:50%"]' in css
    assert "font-size: 1.28rem !important" in css
    assert "font-size: 1.18rem !important" in css
    assert "font-size: 2.05rem !important" in css
    assert "font-size: 1.85rem !important" in css
    assert ".scoop-index-card > span:nth-child(2)" in css


def test_landing_still_emits_banner_markup_on_mobile() -> None:
    import landing_page

    landing_page.st.session_state.clear()
    calls: list[str] = []
    fake_st = type("ST", (), {"markdown": staticmethod(lambda html, **kwargs: calls.append(html))})()
    html = '<div class="scoop-banner-desktop"><div class="scoop-index-card">CME</div></div>'
    landing_page.render_desktop_index_banner(fake_st, html, page="pages/5_CME_Top_10.py")
    assert calls == [html]


def test_banner_css_is_injected_to_parent() -> None:
    from pathlib import Path

    src = Path(__file__).resolve().parents[1].joinpath("tooltip_scroll.py").read_text(encoding="utf-8")
    assert "scoop-mobile-tablet-index-banner-parent-css" in src
    assert "scoop-mobile-tablet-index-banner-page-css" in src
    assert "MOBILE_TABLET_INDEX_BANNER_CSS" in src
    assert "_inject_mobile_tablet_index_banner_parent_css" in src


if __name__ == "__main__":
    tests = [
        test_responsive_css_hides_banners_on_gate,
        test_landing_still_emits_banner_markup_on_mobile,
        test_banner_css_is_injected_to_parent,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} index banner checks passed.")
