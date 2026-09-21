"""Analyze payloads are prerun into screener snapshots (no live AV on the page)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analyze_snapshot import (  # noqa: E402
    analyze_bundle_from_payload,
    build_analyze_bundles,
    ensure_analyze_bundle,
)


def test_build_and_slice_analyze_bundles() -> None:
    history = [{"date": f"2026-01-{i:02d}", "price": 10.0 + i, "change_pct": 0.0} for i in range(1, 32)]
    md = MagicMock()
    md.get_analyze_price_bundle.return_value = {
        "history": history,
        "latest_price": 40.0,
        "week52_low": 8.0,
        "week52_high": 50.0,
        "low_date": "Jan 01, 2026",
        "high_date": "Jan 31, 2026",
    }
    sentiment = MagicMock()
    sentiment.analyze_headlines.return_value = {"score": 0.2, "label": "positive", "total": 1}
    predictor = MagicMock()
    predictor.predict.return_value = {"combined_score": 0.1, "signal": "BUY"}

    rows = [
        {
            "Ticker": "SEI",
            "_source_ticker": "SEI-USD",
            "Price": 40.0,
            "52W Low": 8.0,
            "52W High": 50.0,
            "_headline_texts": ["SEI rallies"],
            "_headline_urls": ["https://example.com"],
        }
    ]
    store = build_analyze_bundles(
        rows,
        md,
        sentiment_eng=sentiment,
        predictor_eng=predictor,
    )
    assert md.get_analyze_price_bundle.call_args.args[1] == 730
    assert "SEI-USD" in store and "SEI" in store
    assert store["SEI"] is store["SEI-USD"]

    payload = {"analyze_bundles": store}
    sliced = analyze_bundle_from_payload(payload, "SEI-USD", 7)
    assert sliced is not None
    assert len(sliced["history"]) == 7
    assert sliced["week52_low"] == 8.0
    assert analyze_bundle_from_payload(payload, "BTC-USD", 7) is None


def test_ensure_computes_and_persists_on_miss() -> None:
    from datetime import datetime, timezone
    from unittest.mock import patch

    history = [{"date": "2026-01-01", "price": 10.0, "change_pct": 0.0}]
    md = MagicMock()
    md.get_analyze_price_bundle.return_value = {
        "history": history,
        "latest_price": 10.0,
        "week52_low": 8.0,
        "week52_high": 12.0,
        "low_date": None,
        "high_date": None,
    }
    saved: dict = {}

    def _save(key, payload):
        saved["key"] = key
        saved["payload"] = payload

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "display_results": [
            {
                "Ticker": "LULU",
                "_source_ticker": "LULU",
                "Price": 10.0,
                "52W Low": 8.0,
                "52W High": 12.0,
                "_headline_texts": ["LULU holds"],
                "_headline_urls": [""],
            }
        ],
        "analyze_bundles": {},
    }
    with (
        patch("screener_snapshots._fetch_snapshot_uncached", return_value=payload),
        patch("screener_snapshots.save_snapshot", side_effect=_save),
        patch("analyze_snapshot.SentimentEngine") as sent_cls,
        patch("analyze_snapshot.Predictor") as pred_cls,
    ):
        sent_cls.return_value.analyze_headlines.return_value = {"score": 0.0, "label": "neutral"}
        pred_cls.return_value.predict.return_value = {"combined_score": 0.0}
        first = ensure_analyze_bundle("LULU", "NASDAQ", 30, market_data=md)
        assert first is not None
        assert md.get_analyze_price_bundle.call_count == 1
        assert saved["key"] == "NASDAQ"
        assert "LULU" in saved["payload"]["analyze_bundles"]

        payload["analyze_bundles"] = saved["payload"]["analyze_bundles"]
        second = ensure_analyze_bundle("LULU", "NASDAQ", 30, market_data=md)
        assert second is not None
        assert md.get_analyze_price_bundle.call_count == 1


def main() -> int:
    test_build_and_slice_analyze_bundles()
    test_ensure_computes_and_persists_on_miss()
    print("PASS analyze snapshot prerun")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
