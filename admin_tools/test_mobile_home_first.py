#!/usr/bin/env python3
"""Mobile/tablet: home (market tabs) before screener; consent stays on market pages."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import landing_page  # noqa: E402


def test_landing_view_resets_to_100_percent() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        _LANDING_VIEW_100_CSS,
        DESKTOP_SCREENER_GATING_LAYOUT,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )
    from landing_page import _landing_view_100_script

    js = _landing_view_100_script()
    assert "initial-scale=1" in js
    assert "zoom" in js
    assert _LANDING_VIEW_100_CSS in RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert _LANDING_VIEW_100_CSS in DESKTOP_SCREENER_GATING_LAYOUT
    assert 'html[data-scoop-screener-gated="1"]' in DESKTOP_SCREENER_GATING_LAYOUT
    assert "font-size: 18px !important;" in DESKTOP_SCREENER_GATING_LAYOUT


def test_home_landing_attract_css_is_mobile_tablet_only() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        _HOME_LANDING_ATTRACT_CSS,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    css = _HOME_LANDING_ATTRACT_CSS
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css
    assert "radial-gradient(ellipse 90% 42% at 50% -8%" in css
    assert "border-left: 4px solid #0ea5e9" in css
    assert "html[data-scoop-theme=\"dark\"][data-scoop-tab-nav=\"1\"][data-scoop-home-page=\"1\"]" in css
    assert "linear-gradient(180deg, #243449 0%, #152033 100%)" in css
    assert "border: 2px solid #38bdf8" in css
    assert "scoop-home-nav-anchor" not in css
    assert '[data-testid="stHeader"]' in css
    assert "scoop-home-landing" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_home_ipad13_surface_pro10_css_is_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _HOME_IPAD13_SURFACE_PRO10_CSS,
    )
    from landing_page import _home_mini_type_flag_script, _responsive_viewport_js

    css = _HOME_IPAD13_SURFACE_PRO10_CSS
    assert 'html[data-scoop-home-mini-type="1"][data-scoop-home-page="1"]' in css
    assert "min(100%, 28rem)" in css
    assert "padding: 1.05rem 1.12rem 1.05rem 1.18rem !important;" in css
    assert "margin-bottom: 12px !important;" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP
    js = _responsive_viewport_js()
    assert "ipadMini" in js
    assert "ipad13" in js
    assert "surfacePro10" in js
    assert "data-scoop-home-ipad-mini" in _home_mini_type_flag_script()
    assert "data-scoop-home-mini-type" in _home_mini_type_flag_script()
    assert "data-scoop-home-surface-pro10" in _home_mini_type_flag_script()
    assert "scoop_home_device_family" in js
    assert "ipadMini || ipad13 || surfacePro10" in js
    assert "orientationchange" in _home_mini_type_flag_script()


def test_home_surface_pro10_nav_fill_is_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _HOME_SURFACE_PRO10_NAV_FILL_CSS,
    )

    css = _HOME_SURFACE_PRO10_NAV_FILL_CSS
    assert 'html[data-scoop-home-surface-pro10="1"][data-scoop-home-page="1"]' in css
    assert "clamp(21px, 2.35vw, 24px)" in css
    assert "clamp(1.2rem, 2.6vw, 1.45rem)" in css
    assert "clamp(1.15rem, 2.5vw, 1.38rem)" in css
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" in css
    assert "font-size: 30px !important;" in css
    assert "font-size: 1.6rem !important;" in css
    assert "margin-bottom: 12px !important;" in css
    assert 'html[data-scoop-home-mini-type="1"][data-scoop-home-page="1"]' in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_home_ipad_mini_market_type_is_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _HOME_IPAD_MINI_MARKET_TYPE_CSS,
    )

    css = _HOME_IPAD_MINI_MARKET_TYPE_CSS
    assert 'html[data-scoop-home-ipad-mini="1"][data-scoop-home-page="1"]' in css
    assert "font-size: 18px !important;" in css
    assert "clamp(1.85rem, 6.3vw, 2.55rem)" in css
    assert "clamp(1.08rem, 3.75vw, 1.28rem)" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_home_landing_stable_type_uses_market_breakpoints() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _HOME_LANDING_STABLE_TYPE_CSS,
    )

    css = _HOME_LANDING_STABLE_TYPE_CSS
    assert 'html[data-scoop-home-page="1"]' in css
    assert "@media (max-width: 768px)" in css
    assert "@media (min-width: 769px) and (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" in css
    assert "font-size: 18px !important;" in css
    assert "clamp(21px, 2.35vw, 24px)" in css
    assert "font-size: 30px !important;" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_cloud_dark_toggle_css_is_mobile_tablet_only() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        _MOBILE_TABLET_CLOUD_DARK_TOGGLE_CSS,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    css = _MOBILE_TABLET_CLOUD_DARK_TOGGLE_CSS
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css
    assert 'input[aria-label="Dark mode"]' in css
    assert "color: #0f172a !important;" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_results_divider_gap_css_is_mobile_tablet_only() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        _MOBILE_TABLET_RESULTS_DIVIDER_GAP_CSS,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    css = _MOBILE_TABLET_RESULTS_DIVIDER_GAP_CSS
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css
    assert "full-results-wrap" in css
    assert "stDivider" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


def test_desktop_screener_deadspace_css_is_desktop_only() -> None:
    from admin_tools.tablet_mobile_layout_css import DESKTOP_SCREENER_TOP_COMPACT

    css = DESKTOP_SCREENER_TOP_COMPACT
    assert "@media (min-width: 1367px)" in css
    assert "disclaimer-footer" in css
    assert "padding-top: 0.15rem !important;" in css
    assert "scoop-index-card" in css
    assert "radial-gradient(ellipse 80% 36% at 12% -8%" in css
    source = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "scoop-desktop-screener-top-compact-css" in source
    assert "applyCss(window.parent.document)" in source


def test_logo_tm_css_on_brand_images() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        DESKTOP_SIDEBAR_LOGO_RULES,
        LOGO_TM_CSS,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    assert 'content: "TM"' in LOGO_TM_CSS
    assert LOGO_TM_CSS in RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert LOGO_TM_CSS in DESKTOP_SIDEBAR_LOGO_RULES


def test_home_marks_seen_and_keeps_vertical_market_list() -> None:
    text = Path(landing_page.__file__).read_text(encoding="utf-8")
    assert "mark_mobile_home_seen()" in text
    assert "enforce_mobile_home_before_market" in text
    assert "MOBILE_MARKET_SCREENER_PAGES" in text
    # Landing layout stays vertical page_links (not horizontal tab chips).
    home_fn = text.split("def render_mobile_tablet_home")[1].split("def render_mobile_tab_nav_shell")[0]
    assert "for path, label in HOME_NAV_MARKETS:" in home_fn
    assert "scoop-home-market-tabs" not in home_fn
    assert "st.columns(len(HOME_NAV_MARKETS)" not in home_fn


def test_enforce_skips_desktop_and_non_screeners() -> None:
    calls: list[str] = []

    fake_st = SimpleNamespace(
        session_state={},
        query_params={},
        switch_page=lambda path: calls.append(path),
    )

    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=False
    ):
        landing_page.enforce_mobile_home_before_market("pages/1_NYSE_Top_10.py")
    assert calls == []

    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=True
    ):
        landing_page.enforce_mobile_home_before_market("pages/7_Terms_of_Service.py")
    assert calls == []


def test_enforce_redirects_mobile_screener_without_home() -> None:
    calls: list[str] = []
    fake_st = SimpleNamespace(
        session_state={},
        query_params={},
        switch_page=lambda path: calls.append(path),
        stop=lambda: None,
    )
    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=True
    ), patch.object(
        landing_page, "_hydrate_mobile_home_seen_from_storage", return_value=False
    ), patch.object(landing_page, "_mobile_analyze_return_bypass", return_value=False):
        landing_page.enforce_mobile_home_before_market("pages/1_NYSE_Top_10.py")
    assert calls == [landing_page.HOME_PAGE]


def test_enforce_allows_after_home_seen() -> None:
    calls: list[str] = []
    fake_st = SimpleNamespace(
        session_state={landing_page.MOBILE_HOME_SEEN_KEY: True},
        query_params={},
        switch_page=lambda path: calls.append(path),
    )
    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=True
    ):
        landing_page.enforce_mobile_home_before_market("pages/2_NASDAQ_Top_10.py")
    assert calls == []


def test_enforce_allows_analyze_return_before_viewport_probe() -> None:
    """Return query must mark home-seen even while the viewport probe is pending."""
    calls: list[str] = []
    fake_st = SimpleNamespace(
        session_state={},
        query_params={"scoop_from_analyze": "1"},
        switch_page=lambda path: calls.append(path),
        stop=lambda: None,
        html=lambda *args, **kwargs: None,
    )
    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=None
    ) as probe:
        landing_page.enforce_mobile_home_before_market("pages/1_NYSE_Top_10.py")
    assert calls == []
    assert fake_st.session_state.get(landing_page.MOBILE_HOME_SEEN_KEY) is True
    probe.assert_not_called()


def test_enforce_allows_when_storage_hydrates() -> None:
    calls: list[str] = []
    fake_st = SimpleNamespace(
        session_state={},
        query_params={},
        switch_page=lambda path: calls.append(path),
        stop=lambda: (_ for _ in ()).throw(RuntimeError("stop")),
    )
    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=True
    ), patch.object(
        landing_page, "_hydrate_mobile_home_seen_from_storage", return_value=True
    ):
        landing_page.enforce_mobile_home_before_market("pages/1_NYSE_Top_10.py")
    assert calls == []


def test_enforce_waits_when_storage_probe_pending() -> None:
    calls: list[str] = []
    stopped = []
    fake_st = SimpleNamespace(
        session_state={},
        query_params={},
        switch_page=lambda path: calls.append(path),
        stop=lambda: stopped.append(True),
    )
    with patch.object(landing_page, "st", fake_st), patch.object(
        landing_page, "probe_responsive_viewport", return_value=True
    ), patch.object(
        landing_page, "_hydrate_mobile_home_seen_from_storage", return_value=None
    ):
        landing_page.enforce_mobile_home_before_market("pages/1_NYSE_Top_10.py")
    assert calls == []
    assert stopped == [True]


def main() -> int:
    tests = [
        test_landing_view_resets_to_100_percent,
        test_home_landing_attract_css_is_mobile_tablet_only,
        test_home_ipad13_surface_pro10_css_is_scoped,
        test_home_surface_pro10_nav_fill_is_scoped,
        test_home_ipad_mini_market_type_is_scoped,
        test_home_landing_stable_type_uses_market_breakpoints,
        test_cloud_dark_toggle_css_is_mobile_tablet_only,
        test_results_divider_gap_css_is_mobile_tablet_only,
        test_desktop_screener_deadspace_css_is_desktop_only,
        test_logo_tm_css_on_brand_images,
        test_home_marks_seen_and_keeps_vertical_market_list,
        test_enforce_skips_desktop_and_non_screeners,
        test_enforce_redirects_mobile_screener_without_home,
        test_enforce_allows_after_home_seen,
        test_enforce_allows_analyze_return_before_viewport_probe,
        test_enforce_allows_when_storage_hydrates,
        test_enforce_waits_when_storage_probe_pending,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} mobile home-first checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
