"""Unit checks: tablet Disclaimer & Terms stays in tablet main-view chrome."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_desktop_terms_top_has_no_padding() -> None:
    from admin_tools.tablet_mobile_layout_css import DESKTOP_TERMS_TOP_COMPACT

    css = DESKTOP_TERMS_TOP_COMPACT
    assert "@media (min-width: 1367px)" in css
    assert "padding-top: 0 !important;" in css
    assert 'html[data-scoop-desktop-layout="1"][data-scoop-terms-active="1"]' in css


def test_tablet_terms_main_view_css_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS

    css = MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS
    assert "@media (max-width: 1366px)" in css
    assert 'html[data-scoop-terms-active="1"]' in css
    assert "data-scoop-desktop-layout" in css
    # Desktop split must not be forced by this block.
    assert "@media (min-width: 1367px)" not in css


def test_tooltip_scroll_holds_terms_on_tablet() -> None:
    source = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "__scoopShouldHoldTermsMainView" in source
    assert "__scoopViewportWidth() <= 1366" in source
    assert "PAGE_NAV_BIND_VERSION = 10" in source
    assert (
        "if (__scoopIsTermsPage() && __scoopShouldHoldTermsMainView())" in source
    )
    assert "__scoopIsTermsPage() && innerW <= TABLET_MAX" in source
    assert "markMobileTermsNav();" in source


def test_consent_bridge_marks_tablet_tab_nav() -> None:
    source = (ROOT / "legal_consent_logger.py").read_text(encoding="utf-8")
    assert "__scoopMobileConsentTermsNavVersion !== 5" in source
    assert "scoop-terms-force-responsive" in source
    assert 'setAttribute("data-scoop-tab-nav", "1")' in source


def test_landing_skips_desktop_sidebar_for_forced_terms() -> None:
    source = (ROOT / "landing_page.py").read_text(encoding="utf-8")
    assert "TERMS_FORCE_RESPONSIVE_STORAGE" in source
    assert "probe_terms_force_responsive" in source
    assert "clear_terms_force_responsive_marker" in source
    assert 'current_page == TERMS_PAGE' in source


if __name__ == "__main__":
    tests = [
        test_desktop_terms_top_has_no_padding,
        test_tablet_terms_main_view_css_scoped,
        test_tooltip_scroll_holds_terms_on_tablet,
        test_consent_bridge_marks_tablet_tab_nav,
        test_landing_skips_desktop_sidebar_for_forced_terms,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} tablet terms nav checks passed.")
