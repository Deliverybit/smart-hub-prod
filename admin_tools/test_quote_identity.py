"""A stale or mismatched ticker must not become a snapshot price."""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from market_data import quote_is_usable, symbol_matches_company


def test_short_stale_series_is_rejected() -> None:
    dates = [datetime(2026, 6, day) for day in (4, 5, 8, 9, 10)]
    assert quote_is_usable(dates, today=datetime(2026, 10, 12)) is False


def test_recent_series_is_kept() -> None:
    dates = [datetime(2026, 9, 1) + __import__("datetime").timedelta(days=i) for i in range(40)]
    assert quote_is_usable(dates, today=datetime(2026, 10, 12)) is True


def test_old_ticker_does_not_match_the_company() -> None:
    matches = [
        {"1. symbol": "BNY", "3. type": "Equity", "4. region": "United States", "9. matchScore": "0.92"},
    ]
    assert symbol_matches_company("BK", matches) is False
    assert symbol_matches_company("BNY", matches) is True


def test_foreign_listing_does_not_drop_the_us_ticker() -> None:
    matches = [
        {"1. symbol": "0Q1F.LON", "3. type": "Equity", "4. region": "United Kingdom", "9. matchScore": "1.0"},
    ]
    assert symbol_matches_company("JPM", matches) is True


if __name__ == "__main__":
    test_short_stale_series_is_rejected()
    test_recent_series_is_kept()
    test_old_ticker_does_not_match_the_company()
    test_foreign_listing_does_not_drop_the_us_ticker()
    print("ok")
