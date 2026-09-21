"""Batched crypto screener quotes and 100-name universe."""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402
from screener_engine import SCREENER_DEFINITIONS, load_page_env, run_screener_scan  # noqa: E402


def _crypto_defn():
    return next(defn for defn in SCREENER_DEFINITIONS if defn.key == "CRYPTO")


def _market_data() -> MarketData:
    with patch("market_data.get_alpha_vantage_api_key", return_value="test-key"):
        return MarketData()


def test_crypto_universe_has_100_names() -> None:
    env = load_page_env(_crypto_defn())
    assert len(env["_universe"]) == 100
    source = (ROOT / "pages" / "3_Crypto_Top_10.py").read_text(encoding="utf-8")
    module = ast.parse(source)
    crypto_data = None
    for node in module.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "CRYPTO_DATA":
            crypto_data = ast.literal_eval(node.value)
    assert isinstance(crypto_data, dict)
    assert len(crypto_data) == 100


def test_crypto_snapshots_use_alpha_vantage_only() -> None:
    md = _market_data()
    tickers = [f"COIN{i}-USD" for i in range(3)]

    def _snap(ticker: str) -> dict:
        return {"current_price": 10.0, "year_low": 5.0, "year_high": 20.0}

    with patch.object(md.session, "get") as get_mock:
        with patch.object(md, "get_market_snapshot", side_effect=_snap) as av_mock:
            snaps = md.get_crypto_screener_snapshots(tickers)

    assert get_mock.call_count == 0
    assert av_mock.call_count == 3
    assert snaps["COIN0-USD"]["source"] == "alpha_vantage"
    assert snaps["COIN0-USD"]["current_price"] == 10.0


def test_run_screener_scan_uses_batched_crypto_snapshots() -> None:
    md = _market_data()
    env = load_page_env(_crypto_defn())
    universe = env["_universe"][:4]
    fake_snaps = {
        ticker: {
            "current_price": 10.0,
            "year_low": 8.0,
            "year_high": 20.0,
            "source": "alpha_vantage",
        }
        for ticker in universe
    }

    with patch.object(md, "get_screener_snapshots", return_value=fake_snaps) as batch_mock:
        with patch.object(md, "get_market_snapshot") as av_mock:
            with patch("screener_engine.get_screener_symbol_limit", return_value=4):
                results, scanned, total = run_screener_scan(_crypto_defn(), market_data=md)

    batch_mock.assert_called_once()
    assert av_mock.call_count == 0
    assert scanned == 4
    assert total == 100
    assert len(results) == 4
    assert results[0]["% Above Low"] == 25.0


def main() -> int:
    tests = [
        test_crypto_universe_has_100_names,
        test_crypto_snapshots_use_alpha_vantage_only,
        test_run_screener_scan_uses_batched_crypto_snapshots,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} crypto batch screener checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
