"""Saved market tables can be refilled without touching the rest of the page."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from preview_tables import refill_page

def test_refill_keeps_header_and_writes_the_new_row() -> None:
    page = (ROOT / "preview" / "nyse.html").read_text(encoding="utf-8")
    before_header = page[page.find("<thead>"):page.find("</thead>")]
    updated = refill_page(
        page,
        [
            {
                "Company": "Example Co",
                "Ticker": "ZZZ",
                "Price": 10,
                "52W Low": 9,
                "52W High": 20,
                "% Above Low": 1.5,
                "Headlines": 1,
                "Market Mood": "AT LOW",
                "Headline Sentiment": 0.1,
                "_headline_texts": ["Example headline"],
                "_headline_urls": ["https://example.com/story"],
                "_source_ticker": "ZZZ",
            }
        ],
        label_field="Company",
        from_path="/NYSE_Top_10",
    )
    assert updated[updated.find("<thead>"):updated.find("</thead>")] == before_header
    assert updated.count("<tbody>") == page.count("<tbody>")
    assert "Example Co" in updated
    assert 'data-ticker="ZZZ"' in updated
    assert 'href="/analyze.html?ticker=ZZZ&amp;from=%2FNYSE_Top_10"' in updated
    assert "Example headline" in updated
    assert "$10.00" in updated
    assert "PEP" not in updated[updated.find("<tbody>"):updated.find("</tbody>")]


def test_company_tip_stays_with_its_ticker() -> None:
    page = (
        '<table class="full-results-table"><thead><tr><th>Company</th></tr></thead>'
        "<tbody><tr>"
        '<td data-label="Company"><span class="fr-label">Company</span>'
        '<span class="fr-val"><span class="tip-wrap scoop-name-tip">PepsiCo Inc.'
        '<span class="tip-text">Global food company</span></span></span></td>'
        '<td data-label="Ticker"><span class="fr-label">Ticker</span>'
        '<span class="fr-val">PEP</span></td>'
        '<td data-label="% Above Low"><span class="fr-label"><span class="tip-wrap">% Above Low'
        '<span class="tip-text">How far the current price is above the 52-week low</span></span></span>'
        '<span class="fr-val">0.58%</span></td>'
        "</tr></tbody></table>"
    )
    updated = refill_page(
        page,
        [{"Company": "PepsiCo Inc.", "Ticker": "PEP", "Price": 1, "52W Low": 1, "52W High": 2, "% Above Low": 1, "Headlines": 0, "Market Mood": "AT LOW", "Headline Sentiment": 0}],
        label_field="Company",
        from_path="/NYSE_Top_10",
    )
    assert "Global food and beverage company" in updated
    assert updated.find("Global food company") < updated.find("How far the current price")


if __name__ == "__main__":
    test_refill_keeps_header_and_writes_the_new_row()
    test_company_tip_stays_with_its_ticker()
    print("ok")
