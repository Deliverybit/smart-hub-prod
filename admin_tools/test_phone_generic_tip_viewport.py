#!/usr/bin/env python3
"""Phone generic tips stay viewport-centered; Headlines path unchanged."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_phone_final_css_beats_page_right_edge() -> None:
    from admin_tools.tablet_mobile_layout_css import PHONE_GENERIC_TIP_FINAL_CSS

    css = PHONE_GENERIC_TIP_FINAL_CSS
    assert "@media (max-width: 743px)" in css
    assert "--scoop-mobile-tip-left" in css
    assert "--scoop-mobile-tip-top" in css
    assert "right: auto !important" in css
    assert "position: fixed !important" in css
    assert ".tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text" in css
    assert ".tip-wrap.headlines-tip" not in css
    # Must retarget fr-val so page right:0 cannot park tips off-screen.
    assert ".fr-val .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open > .tip-text" in css


def test_phone_positioner_in_tooltip_scroll() -> None:
    source = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "applyPhoneViewportCenteredGenericTip" in source
    assert "ensurePhoneGenericTipRuntimeCss" in source
    assert "PHONE_GENERIC_TIP_FINAL_CSS" in source
    assert "scoop-phone-generic-tip-final-css" in source
    assert "scoop-phone-generic-tip-runtime-css" in source
    assert "scoop-phone-generic-tip-standalone" in source
    assert "_PHONE_GENERIC_TIP_STANDALONE_JS" in source
    assert "__scoopPhoneGenericTipStandalone = 4" in source
    assert "_MOBILE_TABLET_TIP_EXCLUSIVE_JS" in source
    assert "closeResponsiveHeadlinesPopups" in source
    assert "--scoop-mobile-tip-left" in source
    # Headlines phone path stays separate.
    assert "getPhoneMobileHeadlinesSlot" in source
    assert "_MOBILE_PHONE_HEADLINES_FIXED_CSS" in source
    # Standalone must not retarget Headlines.
    phone_js = source.split("_PHONE_GENERIC_TIP_STANDALONE_JS = r\"\"\"", 1)[1].split(
        "\"\"\"", 1
    )[0]
    assert "isHeadlinesTarget" in phone_js
    assert "const MAX = 743" in phone_js
    assert ".closest(\"thead\")" in phone_js
    # Dismiss: dead space, outside scroll, other tip (Headlines ignored).
    assert "onScrollDismiss" in phone_js
    assert "isScrollInsideOpenPopup" in phone_js
    assert "touchmove" in phone_js
    assert "Dead space" in phone_js or "closeAll()" in phone_js
    assert "OPEN_GRACE_MS" in phone_js
    assert "closeHeadlines();" in phone_js
    assert "hl-tip-cb:checked" in phone_js


def test_override_css_uses_mobile_tip_left_var() -> None:
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS

    phone = RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS.split(
        "@media (max-width: 743px)"
    )[1].split("@media")[0]
    assert "--scoop-mobile-tip-left" in phone
    assert "translateX(-50%)" not in phone
    assert ".fr-val .tip-wrap:not(.headlines-tip) .tip-text" in phone


if __name__ == "__main__":
    tests = [
        test_phone_final_css_beats_page_right_edge,
        test_phone_positioner_in_tooltip_scroll,
        test_override_css_uses_mobile_tip_left_var,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} phone generic tip viewport checks passed.")
