#!/usr/bin/env python3
"""Verify page navigation requires per-page session consent gating."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import legal_consent_logger as consent  # noqa: E402


class _SessionState(dict):
    def get(self, key, default=None):  # noqa: ANN001
        return super().get(key, default)


class _FakeComponentsHtml:
    @staticmethod
    def html(*_args, **_kwargs) -> None:
        return None


class _FakeComponents:
    v1 = _FakeComponentsHtml


class _FakeSt:
    def __init__(
        self,
        *,
        cookie_data: dict | None = None,
        query_params: dict | None = None,
    ) -> None:
        self.session_state = _SessionState()
        self.query_params = dict(query_params or {})
        self.components = _FakeComponents()
        headers = {}
        if cookie_data is not None:
            encoded = quote(json.dumps(cookie_data))
            headers["cookie"] = f"{consent.TERMS_STORAGE_KEY}={encoded}"
        self.context = SimpleNamespace(headers=headers)
        self.warnings: list[str] = []
        self.checkboxes: list[tuple[str, str]] = []
        self.page_links: list[tuple[str, str]] = []

    def warning(self, text: str) -> None:
        self.warnings.append(text)

    def page_link(self, path: str, *, label: str, use_container_width: bool = False) -> None:
        self.page_links.append((path, label))

    def html(self, *_args, **_kwargs) -> None:
        return None

    def checkbox(self, label: str, *, key: str) -> bool:  # noqa: ARG002
        self.checkboxes.append((label, key))
        return False


def test_restore_terms_from_browser_returns_false_without_cookie() -> None:
    st = _FakeSt()
    assert consent.restore_terms_from_browser(st, "agree_terms_nyse") is False
    assert consent.terms_accepted(st, "agree_terms_nyse") is False


def test_cookie_does_not_skip_gate_without_session() -> None:
    st = _FakeSt(cookie_data={"agree_terms_nyse": True})
    allowed = consent.render_terms_gate(
        st,
        "agree_terms_nyse",
        "I agree to the terms",
    )
    assert allowed is False
    assert consent.terms_accepted(st, "agree_terms_nyse") is False
    assert st.warnings
    assert st.checkboxes
    assert st.page_links == [("pages/7_Terms_of_Service.py", "Disclaimer & Terms")]


def test_other_page_cookie_does_not_skip_gate() -> None:
    st = _FakeSt(cookie_data={"agree_terms_nyse": True})
    allowed = consent.render_terms_gate(
        st,
        "agree_terms_nasdaq",
        "I agree to the terms",
    )
    assert allowed is False
    assert consent.terms_accepted(st, "agree_terms_nasdaq") is False
    assert st.warnings
    assert st.checkboxes


def test_session_acceptance_skips_gate() -> None:
    st = _FakeSt()
    st.session_state["agree_terms_nyse"] = True
    original_persist = consent.persist_terms_to_browser
    consent.persist_terms_to_browser = lambda _key: None
    try:
        assert consent.render_terms_gate(
            st,
            "agree_terms_nyse",
            "I agree to the terms",
        )
        assert st.warnings == []
    finally:
        consent.persist_terms_to_browser = original_persist


def test_analyze_return_query_skips_gate_without_session() -> None:
    st = _FakeSt(query_params={"scoop_from_analyze": "1"})
    original_persist = consent.persist_terms_to_browser
    original_clear = consent._clear_analyze_return_storage
    original_probe = consent._probe_analyze_return_storage
    consent.persist_terms_to_browser = lambda _key: None
    consent._clear_analyze_return_storage = lambda _key: None
    consent._probe_analyze_return_storage = lambda _st, _key: False
    try:
        assert consent.render_terms_gate(
            st,
            "agree_terms_nyse",
            "I agree to the terms",
        )
        assert consent.terms_accepted(st, "agree_terms_nyse") is True
        assert st.warnings == []
        assert "scoop_from_analyze" not in st.query_params
    finally:
        consent.persist_terms_to_browser = original_persist
        consent._clear_analyze_return_storage = original_clear
        consent._probe_analyze_return_storage = original_probe


def test_pending_analyze_return_skips_gate_for_source_page_only() -> None:
    st = _FakeSt()
    st.session_state[consent.PENDING_ANALYZE_RETURN_CONSENT] = "agree_terms_nyse"
    original_persist = consent.persist_terms_to_browser
    consent.persist_terms_to_browser = lambda _key: None
    try:
        assert consent.render_terms_gate(
            st,
            "agree_terms_nyse",
            "I agree to the terms",
        )
        assert consent.terms_accepted(st, "agree_terms_nyse") is True
        assert consent.PENDING_ANALYZE_RETURN_CONSENT not in st.session_state

        st.session_state[consent.PENDING_ANALYZE_RETURN_CONSENT] = "agree_terms_nyse"
        blocked = consent.render_terms_gate(
            st,
            "agree_terms_nasdaq",
            "I agree to the terms",
        )
        assert blocked is False
        assert consent.terms_accepted(st, "agree_terms_nasdaq") is False
    finally:
        consent.persist_terms_to_browser = original_persist


def test_normal_navigation_still_gates_without_session() -> None:
    st = _FakeSt()
    original_probe = consent._probe_analyze_return_storage
    consent._probe_analyze_return_storage = lambda _st, _key: False
    try:
        allowed = consent.render_terms_gate(
            st,
            "agree_terms_nyse",
            "I agree to the terms",
        )
        assert allowed is False
        assert st.warnings
    finally:
        consent._probe_analyze_return_storage = original_probe


def test_mark_post_consent_collapsed_view_targets_mobile_tablet() -> None:
    import inspect

    source = inspect.getsource(consent.mark_post_consent_collapsed_view)
    assert "POST_CONSENT_COLLAPSE_KEY" in source
    assert "__scoopSuppressSidebarExpand" in source
    assert "RESPONSIVE_MAX_WIDTH" in source
    assert consent.POST_CONSENT_COLLAPSE_KEY == "scoop-post-consent-collapse"


def main() -> int:
    tests = [
        test_restore_terms_from_browser_returns_false_without_cookie,
        test_cookie_does_not_skip_gate_without_session,
        test_other_page_cookie_does_not_skip_gate,
        test_session_acceptance_skips_gate,
        test_analyze_return_query_skips_gate_without_session,
        test_pending_analyze_return_skips_gate_for_source_page_only,
        test_normal_navigation_still_gates_without_session,
        test_mark_post_consent_collapsed_view_targets_mobile_tablet,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} navigation consent checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
