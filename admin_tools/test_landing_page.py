#!/usr/bin/env python3
"""Verify home entry routing (desktop NYSE vs mobile/tablet sidebar)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import landing_page  # noqa: E402


def _patch_js(responsive: str | None) -> None:
    def fake_js_eval(*, js_expressions: str, key: str, want_output: bool, height: int):
        _ = js_expressions, key, want_output, height
        return responsive

    landing_page._js_eval = lambda expression, *, key: fake_js_eval(  # type: ignore[method-assign]
        js_expressions=expression,
        key=key,
        want_output=True,
        height=0,
    )
    landing_page.st.session_state.clear()


def test_resolve_home_mobile_tablet() -> None:
    _patch_js("1")
    assert landing_page.resolve_home_entry() == "mobile"


def test_resolve_home_desktop() -> None:
    _patch_js("0")
    assert landing_page.resolve_home_entry() == "desktop"


def test_resolve_home_waits_for_js() -> None:
    _patch_js(None)
    assert landing_page.resolve_home_entry() is None


def test_index_banner_rendered_on_mobile_tablet() -> None:
    _patch_js("1")
    calls: list[str] = []
    fake_st = type("ST", (), {"markdown": staticmethod(lambda html, **kwargs: calls.append(html))})()
    html = '<div class="scoop-banner-desktop"><div class="scoop-index-card">NYSE</div></div>'
    landing_page.render_desktop_index_banner(fake_st, html)
    assert calls == [html]


def test_index_banner_rendered_while_viewport_unknown() -> None:
    _patch_js(None)
    calls: list[str] = []
    fake_st = type("ST", (), {"markdown": staticmethod(lambda html, **kwargs: calls.append(html))})()
    html = '<div class="scoop-banner-desktop"><div class="scoop-index-card">NYSE</div></div>'
    landing_page.render_desktop_index_banner(fake_st, html)
    assert calls == [html]


def test_index_banner_rendered_on_desktop() -> None:
    _patch_js("0")
    calls: list[str] = []
    fake_st = type("ST", (), {"markdown": staticmethod(lambda html, **kwargs: calls.append(html))})()
    html = '<div class="scoop-banner-desktop"><div class="scoop-index-card">NYSE</div></div>'
    landing_page.render_desktop_index_banner(fake_st, html)
    assert calls == [html]


def test_top_picks_omitted_on_mobile_tablet() -> None:
    _patch_js("1")
    assert landing_page.should_render_desktop_top_picks() is False


def test_top_picks_kept_on_desktop() -> None:
    _patch_js("0")
    assert landing_page.should_render_desktop_top_picks() is True


def test_screener_pages_use_index_banner_helper() -> None:
    pages = [
        "pages/1_NYSE_Top_10.py",
        "pages/2_NASDAQ_Top_10.py",
        "pages/3_Crypto_Top_10.py",
        "pages/5_CME_Top_10.py",
        "pages/6_ICE_Top_10.py",
    ]
    root = Path(__file__).resolve().parents[1]
    for rel in pages:
        text = root.joinpath(rel).read_text(encoding="utf-8")
        assert "render_desktop_index_banner" in text, rel
        assert 'scoop-banner-compact">' not in text, rel


def main() -> int:
    tests = [
        test_resolve_home_mobile_tablet,
        test_resolve_home_desktop,
        test_resolve_home_waits_for_js,
        test_index_banner_rendered_on_mobile_tablet,
        test_index_banner_rendered_while_viewport_unknown,
        test_index_banner_rendered_on_desktop,
        test_screener_pages_use_index_banner_helper,
        test_top_picks_omitted_on_mobile_tablet,
        test_top_picks_kept_on_desktop,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} home routing checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
