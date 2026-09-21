"""NOTICE and license page credit TextBlob, Plotly, and Streamlit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_notice_lists_required_packages() -> None:
    text = (ROOT / "NOTICE").read_text(encoding="utf-8")
    for token in ("TextBlob", "Plotly", "Streamlit", "pandas", "MIT License", "Apache License"):
        assert token in text, token


def test_licenses_page_reads_notice() -> None:
    source = (ROOT / "pages" / "_Licenses.py").read_text(encoding="utf-8")
    assert "NOTICE" in source
    assert "notice_to_html" in source
    assert "st.code" not in source
    assert "_landing_view_100_script" in source
    assert "data-scoop-licenses-page" in source
    assert "Third-party licenses" in source


def test_notice_html_uses_body_copy() -> None:
    from licenses_format import notice_to_html

    html = notice_to_html((ROOT / "NOTICE").read_text(encoding="utf-8"))
    assert "<h2" in html
    assert "<h3" in html
    assert "<p>" in html
    assert "TextBlob" in html
    assert "<pre" not in html


def test_terms_and_footers_link_licenses() -> None:
    terms = (ROOT / "pages" / "7_Terms_of_Service.py").read_text(encoding="utf-8")
    assert 'href="/Licenses"' in terms
    assert "Plotly" in terms
    footer_pages = (
        "1_NYSE_Top_10.py",
        "2_NASDAQ_Top_10.py",
        "3_Crypto_Top_10.py",
        "5_CME_Top_10.py",
        "6_ICE_Top_10.py",
        "_Analyze.py",
    )
    for name in footer_pages:
        body = (ROOT / "pages" / name).read_text(encoding="utf-8")
        assert 'href="/Licenses"' in body, name


def main() -> int:
    test_notice_lists_required_packages()
    test_licenses_page_reads_notice()
    test_notice_html_uses_body_copy()
    test_terms_and_footers_link_licenses()
    print("PASS third-party notice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
