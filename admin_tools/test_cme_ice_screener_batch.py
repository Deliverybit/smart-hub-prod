"""Batched CME/ICE screener quotes and 100-name universes."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402
from screener_engine import SCREENER_DEFINITIONS, load_page_env, run_screener_scan  # noqa: E402


def _defn(key: str):
    return next(item for item in SCREENER_DEFINITIONS if item.key == key)


def _market_data() -> MarketData:
    with patch("market_data.get_alpha_vantage_api_key", return_value="test-key"):
        return MarketData()


def test_cme_and_ice_universes_have_100_names() -> None:
    assert len(load_page_env(_defn("CME"))["_universe"]) == 100
    assert len(load_page_env(_defn("ICE"))["_universe"]) == 100


def test_cme_snapshots_use_alpha_vantage_only() -> None:
    md = _market_data()

    def _snap(ticker: str) -> dict:
        prices = {
            "CL=F": {"current_price": 70.0, "year_low": 60.0, "year_high": 90.0},
            "GLD": {"current_price": 180.0, "year_low": 150.0, "year_high": 200.0},
        }
        return prices[ticker]

    with patch.object(md.session, "get") as get_mock:
        with patch.object(md, "get_market_snapshot", side_effect=_snap) as av_mock:
            snaps = md.get_screener_snapshots(["CL=F", "GLD"])
    assert get_mock.call_count == 0
    assert av_mock.call_count == 2
    assert snaps["CL=F"]["current_price"] == 70.0
    assert snaps["GLD"]["year_low"] == 150.0
    assert snaps["CL=F"]["source"] == "alpha_vantage"


def test_run_cme_scan_uses_batched_snapshots() -> None:
    md = _market_data()
    env = load_page_env(_defn("CME"))
    universe = env["_universe"][:4]
    fake = {
        ticker: {
            "current_price": 10.0,
            "year_low": 8.0,
            "year_high": 20.0,
            "source": "alpha_vantage",
        }
        for ticker in universe
    }
    with patch.object(md, "get_screener_snapshots", return_value=fake) as batch_mock:
        with patch.object(md, "get_market_snapshot") as av_mock:
            with patch("screener_engine.get_screener_symbol_limit", return_value=4):
                results, scanned, total = run_screener_scan(_defn("CME"), market_data=md)
    batch_mock.assert_called_once()
    assert av_mock.call_count == 0
    assert scanned == 4
    assert total == 100
    assert len(results) == 4
    assert results[0]["% Above Low"] == 25.0


def main() -> int:
    tests = [
        test_cme_and_ice_universes_have_100_names,
        test_cme_snapshots_use_alpha_vantage_only,
        test_run_cme_scan_uses_batched_snapshots,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} CME/ICE batch screener checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
