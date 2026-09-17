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


def test_home_landing_attract_css_is_mobile_tablet_only() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        _HOME_LANDING_ATTRACT_CSS,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    css = _HOME_LANDING_ATTRACT_CSS
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css
    assert "linear-gradient(180deg, #e8eef8" in css
    assert '[data-testid="stHeader"]' in css
    assert "scoop-home-landing" in css
    assert css in RESPONSIVE_TAB_NAV_BOOTSTRAP


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
        test_home_landing_attract_css_is_mobile_tablet_only,
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
