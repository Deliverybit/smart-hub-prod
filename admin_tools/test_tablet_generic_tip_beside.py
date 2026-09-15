"""Unit checks: tablet/iPad Mini generic tips sit beside the trigger (Headlines unchanged)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_tablet_beside_css_excludes_headlines() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS,
        TABLET_GENERIC_TIP_FINAL_CSS,
    )

    css = RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    assert "@media (max-width: 743px)" in css
    assert "@media (min-width: 744px) and (max-width: 1366px)" in css
    assert "--scoop-mobile-tip-top" in css
    assert "--scoop-tablet-tip-left" in css
    assert "--scoop-tablet-tip-top" in css
    assert ".tip-wrap:not(.headlines-tip)" in css
    tablet_block = css.split("@media (min-width: 744px) and (max-width: 1366px)")[1]
    tablet_only = tablet_block.split("@media")[0]
    assert ".tip-wrap.headlines-tip .tip-text" not in tablet_only
    assert "scoop-mobile-tip-open > .tip-text" in TABLET_GENERIC_TIP_FINAL_CSS
    assert ".tip-wrap:not(.headlines-tip)" in TABLET_GENERIC_TIP_FINAL_CSS
    assert "@media (min-width: 744px) and (max-width: 1366px)" in TABLET_GENERIC_TIP_FINAL_CSS
    assert "50vw" in TABLET_GENERIC_TIP_FINAL_CSS
    assert "scoop-tip-title" in TABLET_GENERIC_TIP_FINAL_CSS
    assert "font-size: 1.08rem" in TABLET_GENERIC_TIP_FINAL_CSS
    assert "50vw" in css


def test_tooltip_scroll_has_tablet_beside_positioner() -> None:
    source = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "positionTabletBesideGenericTip" in source
    assert "TOOLTIP_SCRIPT_VERSION = 75" in source
    assert "__scoopTabletGenericTipStandalone = 9" in source
    assert "__scoopIpadMiniHeadlinesCenterStandalone = 1" in source
    assert "scoop-ipad-mini-headlines-center-standalone" in source
    assert "_IPAD_MINI_HEADLINES_CENTER_STANDALONE_JS" in source
    assert "__scoopTabletHeadlinesCenterStandalone = 1" in source
    assert "scoop-tablet-headlines-center-standalone" in source
    assert "_TABLET_HEADLINES_CENTER_STANDALONE_JS" in source
    assert "__scoopTabletTipDismissStandalone = 4" in source
    assert "scoop-tablet-tip-dismiss-standalone" in source
    assert "_TABLET_TIP_DISMISS_STANDALONE_JS" in source
    assert "_inject_js_source" in source
    assert "combined-page-v75" in source
    assert "TABLET_GENERIC_TIP_MIN = 744" in source
    assert "MOBILE_GENERIC_TIP_MAX = 743" in source
    # iPad Mini Headlines center is scoped 744–768 only.
    ipad_hl = source.split("_IPAD_MINI_HEADLINES_CENTER_STANDALONE_JS = r\"\"\"", 1)[1].split(
        "\"\"\"", 1
    )[0]
    assert "const MIN = 744" in ipad_hl
    assert "const MAX = 768" in ipad_hl
    assert "--hl-fixed-left" in ipad_hl
    # Tablet Headlines center stays 769+ (unchanged range).
    tab_hl = source.split("_TABLET_HEADLINES_CENTER_STANDALONE_JS = r\"\"\"", 1)[1].split(
        "\"\"\"", 1
    )[0]
    assert "const MIN = 769" in tab_hl
    assert "const MAX = 1366" in tab_hl
    # Dismiss covers tablet + iPad Mini and closes Headlines + generics.
    dismiss = source.split("_TABLET_TIP_DISMISS_STANDALONE_JS = r\"\"\"", 1)[1].split(
        "\"\"\"", 1
    )[0]
    assert "const MIN = 744" in dismiss
    assert "const MAX = 1366" in dismiss
    assert "hl-tip-cb:checked" in dismiss
    assert "scoop-mobile-tip-open" in dismiss
    assert "hl-tip-backdrop" in dismiss
    assert "onScrollDismiss" in dismiss
    assert "touchmove" in dismiss
    assert "isScrollInsideOpenPopup" in dismiss
    # Phone generic binder is separate from tablet beside placement.
    standalone = source.split("_TABLET_GENERIC_TIP_STANDALONE_JS = r\"\"\"", 1)[1].split(
        "\"\"\"", 1
    )[0]
    assert "const MIN = 744" in standalone
    assert "scoop-env-banner" in source
    assert "getPhoneMobileHeadlinesSlot" in source


if __name__ == "__main__":
    tests = [
        test_tablet_beside_css_excludes_headlines,
        test_tooltip_scroll_has_tablet_beside_positioner,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} tablet generic tip checks passed.")
