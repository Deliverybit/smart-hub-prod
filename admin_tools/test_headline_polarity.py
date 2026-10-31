"""Phrase overrides for headline polarity."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sentiment_engine import SentimentEngine, headline_polarity  # noqa: E402


def test_severe_legal_language_scores_minus_one():
    assert headline_polarity("Gildan securities class action lawsuit deadline") == -1.0
    assert headline_polarity("Bank faces criminal probe after fraud fine") == -1.0


def test_target_cut_beats_a_buy_rating():
    title = "B of A Securities maintains Buy on Alamos Gold, lowers target to $39"
    assert headline_polarity(title) == -0.5


def test_strong_and_mild_positive_phrases():
    assert headline_polarity("United Parcel Service earnings beat by $0.06, revenue topped estimates") == 0.5
    assert headline_polarity("Northrop Grumman Price Target Raised to $430") == 0.5
    assert headline_polarity("National Bank lifts target for Emera stock") == 0.5
    assert headline_polarity("Cameco stock rises Tuesday, outperforms market") == 0.5
    assert headline_polarity("Eaton Jumps 4% After Declaring Its Quarterly Dividend") == 0.2
    assert headline_polarity("Eaton declares $1.10 quarterly dividend") == 0.2


def test_phrases_from_other_screens():
    assert headline_polarity("Two workers die after Kinross Gold accidents") == -1.0
    assert headline_polarity("Coinbase shares slide 11% as Binance hack weighs") == -1.0
    assert headline_polarity("Haleon sinks 14.7% after Q3 growth miss") == -0.5
    assert headline_polarity("Zacks downgrades Haleon stock from Hold to Strong Sell") == -0.5
    assert headline_polarity("Take-Two Interactive stock hits 52-week low") == -0.5
    assert headline_polarity("Sterling Capital Sells 6,430 Shares of Take-Two") == -0.5
    assert headline_polarity("Caught Out By Charter Communications' 58% Fall") == -0.5
    assert headline_polarity("T-Mobile US Jumps 5.3% on EPS Beat") == 0.5
    assert headline_polarity("T-Mobile Tops Q3 Estimates") == 0.5
    assert headline_polarity("T-Mobile Raises 2026 Outlook") == 0.5
    assert headline_polarity("GSK Wins FDA Approval For Chronic Hepatitis B Drug") == 0.5
    assert headline_polarity("Lululemon Rallies Over 3%") == 0.2
    assert headline_polarity("Haleon Launches £500m Share Buyback") == 0.2
    assert headline_polarity("GSK to Invest $800M and Create 300 New Jobs") == 0.2


def test_volatility_surge_is_not_a_boost():
    score = headline_polarity("Implied Volatility Surging for Kinross Gold Stock Options")
    assert score < 0.2


def test_gildan_average_is_bearish():
    headlines = [
        "DEADLINE ALERT for Gildan: Securities Fraud Class Actions",
        "Gildan Securities Class Action Deadline",
        "Gildan Securities Class Action Lawsuit",
        "Gildan stock falls Tuesday, underperforms market",
        "Gildan stock price target cut to $64",
    ]
    result = SentimentEngine().analyze_headlines("GIL", headlines)
    assert result["label"] == "bearish"
    assert result["score"] <= -0.5


if __name__ == "__main__":
    test_severe_legal_language_scores_minus_one()
    test_target_cut_beats_a_buy_rating()
    test_strong_and_mild_positive_phrases()
    test_phrases_from_other_screens()
    test_volatility_surge_is_not_a_boost()
    test_gildan_average_is_bearish()
    print("ok")
