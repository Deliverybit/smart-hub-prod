"""Crypto Analyze history requests Alpha Vantage full outputsize only."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402


def test_daily_cache_key_includes_crypto_outputsize() -> None:
    md = MarketData.__new__(MarketData)
    md._CRYPTO_SYMBOLS = MarketData._CRYPTO_SYMBOLS
    md._CRYPTO_ID_ALIASES = MarketData._CRYPTO_ID_ALIASES
    assert md._daily_cache_key("DOGE-USD", "compact") != md._daily_cache_key("DOGE-USD", "full")
    assert md._daily_cache_key("DOGE-USD", "full")[2] == "full"


def test_crypto_full_history_requests_av_outputsize_full() -> None:
    md = MarketData.__new__(MarketData)
    md.api_key = "demo"
    md.session = None
    md._daily_cache = {}
    md._CRYPTO_SYMBOLS = MarketData._CRYPTO_SYMBOLS
    md._CRYPTO_ID_ALIASES = MarketData._CRYPTO_ID_ALIASES

    av_days = pd.date_range("2024-09-20", periods=740, freq="D")
    av_series = {
        d.strftime("%Y-%m-%d"): {"2. high": "0.2", "3. low": "0.1", "4. close": "0.15"}
        for d in av_days
    }

    with patch.object(
        md,
        "_request",
        return_value={"Time Series (Digital Currency Daily)": av_series},
    ) as req:
        df = md._daily_history_frame("DOGE-USD", outputsize="full", max_rows=740)

    assert req.call_args.kwargs["outputsize"] == "full"
    assert req.call_args.kwargs["function"] == "DIGITAL_CURRENCY_DAILY"
    assert len(df) == 740
    assert not hasattr(md, "_yahoo_daily_history_frame")


def test_analyze_bundle_caps_chart_at_two_years() -> None:
    md = MarketData.__new__(MarketData)
    long_days = pd.date_range(end=pd.Timestamp.now().normalize(), periods=2000, freq="D")
    long_df = pd.DataFrame(
        {
            "date": long_days,
            "price": [0.15] * len(long_days),
            "low": [0.10] * len(long_days),
            "high": [0.20] * len(long_days),
        }
    )
    with patch.object(md, "_daily_history_frame", return_value=long_df):
        bundle = md.get_analyze_price_bundle("DOGE-USD", days="max")
        capped = md.get_analyze_price_bundle("DOGE-USD", days=1825)

    assert bundle is not None and capped is not None
    assert len(bundle["history"]) == 731
    assert len(capped["history"]) == 731


def test_short_range_uses_compact_when_snapshot_has_52w() -> None:
    md = MarketData.__new__(MarketData)
    md._daily_cache = {}
    compact_days = pd.date_range(end=pd.Timestamp.now().normalize(), periods=100, freq="D")
    compact_df = pd.DataFrame(
        {
            "date": compact_days,
            "price": [0.15] * len(compact_days),
            "low": [0.10] * len(compact_days),
            "high": [0.20] * len(compact_days),
        }
    )
    with patch.object(md, "_daily_history_frame", return_value=compact_df) as hist:
        bundle = md.get_analyze_price_bundle(
            "DOGE-USD",
            days=30,
            snapshot={"Price": 0.16, "52W Low": 0.08, "52W High": 0.42},
            fail_fast=True,
        )
    assert hist.call_args.kwargs["outputsize"] == "full"
    assert hist.call_args.kwargs["fail_fast"] is True
    assert bundle["week52_low"] == 0.10
    assert bundle["week52_high"] == 0.20
    assert len(bundle["history"]) == 31


def test_empty_chart_request_retries_until_bars_return() -> None:
    md = MarketData.__new__(MarketData)
    md._CRYPTO_SYMBOLS = MarketData._CRYPTO_SYMBOLS
    md._CRYPTO_ID_ALIASES = MarketData._CRYPTO_ID_ALIASES
    md._INDEX_SYMBOLS = MarketData._INDEX_SYMBOLS
    md._FUTURES_SYMBOLS = MarketData._FUTURES_SYMBOLS
    md._daily_cache = {}
    day = pd.Timestamp.now().normalize()
    series = {
        (day - pd.Timedelta(days=offset)).strftime("%Y-%m-%d"): {
            "2. high": "12",
            "3. low": "9",
            "4. close": "10",
            "5. adjusted close": "10",
            "8. split coefficient": "1",
        }
        for offset in range(40)
    }
    with patch.object(md, "_request", side_effect=[{}, {"Time Series (Daily)": series}]) as req:
        bundle = md.get_analyze_price_bundle(
            "GS",
            days=730,
            snapshot={"Price": 865.0, "52W Low": 754.0, "52W High": 1153.0},
            fail_fast=True,
        )
    assert [call.kwargs["fail_fast"] for call in req.call_args_list] == [True, False]
    assert bundle is not None
    assert len(bundle["history"]) >= 2


def test_failed_refetch_keeps_the_shorter_cached_series() -> None:
    md = MarketData.__new__(MarketData)
    md._CRYPTO_SYMBOLS = MarketData._CRYPTO_SYMBOLS
    md._CRYPTO_ID_ALIASES = MarketData._CRYPTO_ID_ALIASES
    md._daily_cache = {}
    short_days = pd.date_range("2026-06-01", periods=100, freq="D")
    short_df = pd.DataFrame(
        {
            "date": short_days,
            "price": [10.0] * len(short_days),
            "low": [9.0] * len(short_days),
            "high": [11.0] * len(short_days),
        }
    )
    md._daily_cache[md._daily_cache_key("GS", "full")] = short_df
    with patch.object(md, "_request", return_value={}):
        df = md._daily_history_frame("GS", outputsize="full", max_rows=740, fail_fast=True)
    assert len(df) == 100
    assert len(md._daily_cache[md._daily_cache_key("GS", "full")]) == 100


def test_empty_bundle_keeps_the_published_chart() -> None:
    from preview_tables import _catalog_asset

    previous = {
        "series": [{"d": "2026-11-01", "p": 100.0}, {"d": "2026-11-02", "p": 101.0}],
        "description": "Bank.",
    }
    payload = {"screener_key": "NYSE", "last_updated_display": "Nov 08, 2026  05:17 PM CT"}
    row = {"Ticker": "GS", "Company": "Goldman Sachs Group"}
    bundle = {
        "news_items": [],
        "sent_result": {"headline_scores": []},
        "history": [],
        "latest_price": 865.82,
        "week52_low": 754.0,
        "week52_high": 1153.99,
    }
    asset = _catalog_asset(payload, row, bundle, previous)
    assert asset["price"] == 865.82
    assert len(asset["series"]) == 2
    assert asset["series"][0]["d"] == "2026-11-01"


def test_history_reuses_full_cache_for_compact_request() -> None:
    md = MarketData.__new__(MarketData)
    md._CRYPTO_SYMBOLS = MarketData._CRYPTO_SYMBOLS
    md._CRYPTO_ID_ALIASES = MarketData._CRYPTO_ID_ALIASES
    md._daily_cache = {}
    full_days = pd.date_range("2024-09-20", periods=740, freq="D")
    full_df = pd.DataFrame(
        {
            "date": full_days,
            "price": [0.15] * len(full_days),
            "low": [0.10] * len(full_days),
            "high": [0.20] * len(full_days),
        }
    )
    md._daily_cache[md._daily_cache_key("DOGE-USD", "full")] = full_df
    with patch.object(md, "_request") as req:
        df = md._daily_history_frame("DOGE-USD", outputsize="compact", max_rows=110)
    assert req.call_count == 0
    assert len(df) == 110


def main() -> int:
    test_daily_cache_key_includes_crypto_outputsize()
    test_crypto_full_history_requests_av_outputsize_full()
    test_analyze_bundle_caps_chart_at_two_years()
    test_short_range_uses_compact_when_snapshot_has_52w()
    test_empty_chart_request_retries_until_bars_return()
    test_failed_refetch_keeps_the_shorter_cached_series()
    test_empty_bundle_keeps_the_published_chart()
    test_history_reuses_full_cache_for_compact_request()
    print("PASS crypto analyze history span")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
