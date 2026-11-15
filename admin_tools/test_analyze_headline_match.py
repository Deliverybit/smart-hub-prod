#!/usr/bin/env python3
"""Tests for Analyze snapshot headline ticker matching."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from screener_headlines import _ticker_matches_row, news_items_from_snapshot  # noqa: E402


def test_ticker_matches_row_requires_row_overlap() -> None:
    row = {"Ticker": "NKE", "_source_ticker": "NKE", "_headline_texts": ["a"]}
    assert _ticker_matches_row("NKE", row)
    assert not _ticker_matches_row("AAPL", row)


def test_ticker_matches_crypto_aliases() -> None:
    row = {"Ticker": "APT", "_source_ticker": "APT21794-USD", "_headline_texts": ["a"]}
    assert _ticker_matches_row("APT", row)
    assert _ticker_matches_row("APT21794-USD", row)


def test_news_items_from_snapshot_skips_empty_headline_rows() -> None:
    fake = {
        "headlines_enriched": True,
        "display_results": [
            {"Ticker": "FET", "_source_ticker": "FET-USD", "_headline_texts": []},
            {
                "Ticker": "HBAR",
                "_source_ticker": "HBAR-USD",
                "_headline_texts": ["HBAR rises after a network upgrade"],
                "_headline_urls": ["https://example.com"],
            },
        ],
        "all_results": [],
    }

    import screener_snapshots

    original = screener_snapshots.fetch_snapshot
    screener_snapshots.fetch_snapshot = lambda _key: fake
    try:
        items = news_items_from_snapshot("HBAR-USD", "CRYPTO")
        assert items is not None
        assert items[0]["title"] == "HBAR rises after a network upgrade"
        assert news_items_from_snapshot("BTC-USD", "CRYPTO") is None
    finally:
        screener_snapshots.fetch_snapshot = original


def test_snapshot_drops_headlines_that_omit_name_and_ticker() -> None:
    fake = {
        "headlines_enriched": True,
        "display_results": [
            {
                "Ticker": "NFLX",
                "Company": "Netflix Inc.",
                "_source_ticker": "NFLX",
                "_headline_texts": ["CX Institutional Buys Shares of The Gap, Inc."],
                "_headline_urls": ["https://example.com"],
            },
        ],
        "all_results": [],
    }

    import screener_snapshots

    original = screener_snapshots.fetch_snapshot
    screener_snapshots.fetch_snapshot = lambda _key: fake
    try:
        assert news_items_from_snapshot("NFLX", "NASDAQ") is None
    finally:
        screener_snapshots.fetch_snapshot = original


def test_livepeer_drops_unrelated_macro_headlines() -> None:
    from headline_service import headlines_from_news_items

    items = [
        {"title": "Fed Meeting Could Inject Volatility Into Dollar Trading", "url": "https://example.com/fed"},
        {"title": "Dollar Rises as Investors Move Into Safe Havens", "url": "https://example.com/dollar"},
        {"title": "Livepeer token slips as video demand cools", "url": "https://example.com/lpt"},
        {"title": "LPT holds near its yearly low", "url": "https://example.com/ticker"},
        {
            "title": "Video networks see quieter demand",
            "url": "https://example.com/body",
            "summary": "Transcoding fees on Livepeer fell with usage.",
        },
    ]
    titles, urls = headlines_from_news_items(
        items,
        ticker="LPT-USD",
        company_name="Livepeer",
    )
    assert titles == [
        "Livepeer token slips as video demand cools",
        "LPT holds near its yearly low",
        "Video networks see quieter demand",
    ]
    assert urls == ["https://example.com/lpt", "https://example.com/ticker", "https://example.com/body"]


def test_every_market_drops_headlines_that_omit_the_asset() -> None:
    from headline_service import headlines_from_news_items, scrub_stored_headlines

    titles, _urls = headlines_from_news_items(
        [
            {"title": "Dollar rises as investors seek safety", "url": "https://example.com/fx", "summary": "The yen weakened."},
            {"title": "Shell lifts its dividend", "url": "https://example.com/shel"},
        ],
        ticker="SHEL.LON",
        company_name="Shell",
    )
    assert titles == ["Shell lifts its dividend"]

    row = scrub_stored_headlines({
        "Ticker": "NFLX",
        "Company": "Netflix Inc.",
        "_source_ticker": "NFLX",
        "_headline_texts": ["CX Institutional Buys Shares of The Gap, Inc.", "Netflix adds subscribers"],
        "_headline_urls": ["https://example.com/gap", "https://example.com/nflx"],
        "Headlines": 2,
        "Headline Sentiment": 0.2,
    })
    assert row["_headline_texts"] == ["Netflix adds subscribers"]
    assert row["Headlines"] == 1


def test_crypto_close_name_match() -> None:
    from headline_service import title_mentions_asset

    assert title_mentions_asset(
        "Echelon token climbs after a game update",
        "PRIME-USD",
        "Echelon Prime",
    )
    assert not title_mentions_asset(
        "Stocks rise in a broad market rally",
        "PRIME-USD",
        "Echelon Prime",
    )
    assert not title_mentions_asset(
        "Strong Cash Flow and Strategic Growth",
        "FLOW-USD",
        "Flow",
    )
    assert not title_mentions_asset(
        "Stellar Blockchain to Power Turbo Energy's financing",
        "TURBO-USD",
        "Turbo",
    )
    assert title_mentions_asset(
        "TURBO Crypto Blasts 50%",
        "TURBO-USD",
        "Turbo",
    )


def main() -> int:
    tests = [
        test_ticker_matches_row_requires_row_overlap,
        test_ticker_matches_crypto_aliases,
        test_news_items_from_snapshot_skips_empty_headline_rows,
        test_snapshot_drops_headlines_that_omit_name_and_ticker,
        test_livepeer_drops_unrelated_macro_headlines,
        test_every_market_drops_headlines_that_omit_the_asset,
        test_crypto_close_name_match,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} headline match checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
