"""Batched CME/ICE screener quotes and 100-name universes."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402
from screener_engine import SCREENER_DEFINITIONS  # noqa: E402


def _market_data() -> MarketData:
    with patch("market_data.get_alpha_vantage_api_key", return_value="test-key"):
        return MarketData()


def test_scanner_skips_cme_and_ice() -> None:
    keys = {item.key for item in SCREENER_DEFINITIONS}
    assert keys == {"NYSE", "NASDAQ", "LSE", "TSX", "CRYPTO"}


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


def main() -> int:
    tests = [
        test_scanner_skips_cme_and_ice,
        test_cme_snapshots_use_alpha_vantage_only,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} CME/ICE batch screener checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
