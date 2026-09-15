#!/usr/bin/env python3
"""Verify dark mode defaults to off and only activates via toggle / saved preference."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import theme_mode  # noqa: E402


class _Session(dict):
    """Minimal stand-in for st.session_state (supports `in` and .get)."""

    def __getattr__(self, name: str):
        return self[name]

    def __setattr__(self, name: str, value) -> None:
        self[name] = value


def _fresh_session() -> _Session:
    theme_mode.st.session_state = _Session()
    return theme_mode.st.session_state


def test_is_dark_mode_defaults_false() -> None:
    _fresh_session()
    assert theme_mode.is_dark_mode() is False


def test_session_key_defaults_false() -> None:
    ss = _fresh_session()
    assert ss.get(theme_mode.SESSION_KEY, False) is False


def test_toggle_key_controls_mode() -> None:
    ss = _fresh_session()
    ss[theme_mode.HYDRATED_KEY] = True
    ss[theme_mode.SESSION_KEY] = True
    assert theme_mode.is_dark_mode() is True
    ss[theme_mode.SESSION_KEY] = False
    assert theme_mode.is_dark_mode() is False


def test_bootstrap_only_restores_explicit_dark() -> None:
    src = Path(theme_mode.__file__).read_text(encoding="utf-8")
    helper = src.split("def _parent_theme_store_js")[1].split("def _set_theme_session")[0]
    bootstrap = src.split("def _early_theme_bootstrap_script")[1].split("def apply_theme_from_query_param")[0]
    assert 'let theme = "light";' in bootstrap
    assert 'if (stored === "dark")' in bootstrap
    assert "scoopThemeStore" in bootstrap
    assert "localStorage.removeItem" in helper
    assert 'getAttribute("data-scoop-theme") === "dark"' not in bootstrap


def test_dark_from_storage_value() -> None:
    assert theme_mode._dark_from_storage_value("") is False
    assert theme_mode._dark_from_storage_value("light") is False
    assert theme_mode._dark_from_storage_value("dark") is True
    assert theme_mode._dark_from_storage_value("DARK") is True


def test_storage_read_key_is_unique_per_page() -> None:
    from unittest.mock import patch

    _fresh_session()
    frame_nyse = type("Frame", (), {"filename": "/project/pages/1_NYSE_Top_10.py"})()
    frame_nasdaq = type("Frame", (), {"filename": "/project/pages/2_NASDAQ_Top_10.py"})()
    with patch("inspect.stack", return_value=[frame_nyse]):
        key_a = theme_mode._storage_read_key()
    with patch("inspect.stack", return_value=[frame_nasdaq]):
        key_b = theme_mode._storage_read_key()
    assert key_a != key_b
    assert key_a.startswith("scoop_theme_read_")


def test_render_toggle_skips_until_theme_known() -> None:
    ss = _fresh_session()
    theme_mode.render_dark_mode_toggle()
    assert theme_mode.TOGGLE_KEY not in ss


def test_query_param_dark_only_when_explicit() -> None:
    _fresh_session()

    class _Params(dict):
        def get(self, key, default=None):
            return super().get(key, default)

        def __delitem__(self, key):
            super().__delitem__(key)

    theme_mode.st.query_params = _Params()
    theme_mode.apply_theme_from_query_param()
    assert theme_mode.is_dark_mode() is False

    theme_mode.st.query_params = _Params(theme="dark")
    theme_mode.apply_theme_from_query_param()
    assert theme_mode.is_dark_mode() is True


def test_hydrate_empty_storage_is_light() -> None:
    _fresh_session()

    class _FakeJsEval:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            return "0|"

    sys.modules["streamlit_js_eval"] = _FakeJsEval()
    assert theme_mode._hydrate_theme_from_storage() is True
    assert theme_mode.is_dark_mode() is False


def test_hydrate_dark_storage_restores_toggle() -> None:
    _fresh_session()

    class _FakeJsEval:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            return "0|dark"

    sys.modules["streamlit_js_eval"] = _FakeJsEval()
    theme_mode._hydrate_theme_from_storage()
    assert theme_mode.is_dark_mode() is True
    assert theme_mode.st.session_state[theme_mode.TOGGLE_KEY] is True
    assert theme_mode.st.session_state[theme_mode.MAIN_TOGGLE_KEY] is True


def test_apply_theme_uses_session_while_storage_pending() -> None:
    """If js_eval is pending, keep an in-session toggle until storage hydrates."""
    ss = _fresh_session()
    ss[theme_mode.SESSION_KEY] = True
    ss[theme_mode.HYDRATED_KEY] = True

    class _FakeJsEval:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            return None

    sys.modules["streamlit_js_eval"] = _FakeJsEval()
    theme_mode.apply_theme_early()
    assert theme_mode.is_dark_mode() is True


def test_page_navigation_rehydrates_from_storage() -> None:
    """Simulate a new page load reading an updated sessionStorage value."""
    from unittest.mock import patch

    ss = _fresh_session()
    frame_nyse = type("Frame", (), {"filename": "/project/pages/1_NYSE_Top_10.py"})()
    frame_nasdaq = type("Frame", (), {"filename": "/project/pages/2_NASDAQ_Top_10.py"})()

    class _FakeJsEval:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            assert kwargs.get("key", "").startswith("scoop_theme_read_")
            return "0|"

    sys.modules["streamlit_js_eval"] = _FakeJsEval()
    with patch("inspect.stack", return_value=[frame_nyse]):
        theme_mode.apply_theme_early()
    assert theme_mode.is_dark_mode() is False

    ss[theme_mode.HYDRATED_KEY] = True
    ss[theme_mode.PAGE_KEY] = "/project/pages/1_NYSE_Top_10.py"

    class _FakeJsEvalDark:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            return "0|dark"

    sys.modules["streamlit_js_eval"] = _FakeJsEvalDark()
    with patch("inspect.stack", return_value=[frame_nasdaq]):
        theme_mode.apply_theme_early()
    assert theme_mode.is_dark_mode() is True


def test_toggle_skip_hydrate_preserves_session() -> None:
    ss = _fresh_session()
    ss[theme_mode.HYDRATED_KEY] = True
    ss[theme_mode.SESSION_KEY] = True
    ss[theme_mode.PAGE_KEY] = "/project/pages/1_NYSE_Top_10.py"
    ss[theme_mode.SKIP_HYDRATE_KEY] = True

    class _FakeJsEval:
        @staticmethod
        def streamlit_js_eval(**kwargs):
            raise AssertionError("hydrate should be skipped after toggle")

    sys.modules["streamlit_js_eval"] = _FakeJsEval()
    assert theme_mode._hydrate_theme_from_storage() is True
    assert theme_mode.is_dark_mode() is True


def test_hydrate_reads_parent_session_storage() -> None:
    src = Path(theme_mode.__file__).read_text(encoding="utf-8")
    hydrate = src.split("def _hydrate_theme_from_storage")[1].split("def _write_theme_to_storage")[0]
    assert "scoopThemeStore" in hydrate
    assert "getEntriesByType('navigation')" not in hydrate
    assert 'reloaded == "1"' not in hydrate


def test_set_theme_session_syncs_main_toggle() -> None:
    ss = _fresh_session()
    theme_mode._set_theme_session(True)
    assert ss[theme_mode.SESSION_KEY] is True
    assert ss[theme_mode.TOGGLE_KEY] is True
    assert ss[theme_mode.MAIN_TOGGLE_KEY] is True


def test_static_css_requires_dark_attribute() -> None:
    from admin_tools.dark_mode_css import DARK_MODE_CSS

    assert "\nhtml,\n" not in DARK_MODE_CSS
    assert "\nhtml body {\n" not in DARK_MODE_CSS
    assert 'html [data-testid="stApp"]' not in DARK_MODE_CSS
    assert "html[data-scoop-theme=\"dark\"]" in DARK_MODE_CSS


def main() -> int:
    tests = [
        test_is_dark_mode_defaults_false,
        test_session_key_defaults_false,
        test_toggle_key_controls_mode,
        test_bootstrap_only_restores_explicit_dark,
        test_dark_from_storage_value,
        test_storage_read_key_is_unique_per_page,
        test_render_toggle_skips_until_theme_known,
        test_query_param_dark_only_when_explicit,
        test_hydrate_empty_storage_is_light,
        test_hydrate_dark_storage_restores_toggle,
        test_apply_theme_uses_session_while_storage_pending,
        test_page_navigation_rehydrates_from_storage,
        test_toggle_skip_hydrate_preserves_session,
        test_hydrate_reads_parent_session_storage,
        test_set_theme_session_syncs_main_toggle,
        test_static_css_requires_dark_attribute,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} theme mode checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
