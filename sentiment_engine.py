import re

from textblob import TextBlob

# One match sets the headline. Checked before TextBlob so legal and
# market phrases are not scored as ordinary English.
_SEVERE_NEGATIVE = (
    "lawsuit",
    "class action",
    "securities fraud",
    "fraud",
    "sec charges",
    "indicted",
    "indictment",
    "criminal",
    "bankrupt",
    "bankruptcy",
    "ponzi",
    "embezzlement",
    "money laundering",
    "accounting scandal",
    "delisted",
    "going out of business",
)

_MILD_NEGATIVE = (
    "shareholder alert",
    "deadline alert",
    "underperforms",
    "price target cut",
    "lowers target",
    "cuts target",
    "downgrade",
    "recall",
    "slump",
    "investigation",
    "falls",
    "crash",
    "drop",
)

_STRONG_POSITIVE = (
    "earnings beat",
    "tops estimates",
    "top estimates",
    "topped estimates",
    "price target raised",
    "raises target",
    "lifts target",
    "target raised",
    "upgrade",
    "outperforms",
    "dividend increase",
    "raises guidance",
    "raised guidance",
    "raised outlook",
    "raised revenue outlook",
)

_MILD_POSITIVE = (
    "buy rating",
    "maintains buy",
    "awarded",
    "rises",
    "gains",
    "jumps",
)

_BOOST_WORDS = ("surge", "rally", "record", "breakout")


def _has_phrase(text: str, phrase: str) -> bool:
    if " " in phrase:
        return phrase in text
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def _declares_dividend(text: str) -> bool:
    return "dividend" in text and re.search(r"\bdeclar\w*\b", text) is not None


def headline_polarity(headline: str) -> float:
    """Score one headline from -1 to 1.

    Severe legal or fraud language wins outright. A target cut in the same
    headline as a buy rating stays negative. Ordinary wording still uses TextBlob.
    """
    text = (headline or "").lower()
    if any(_has_phrase(text, phrase) for phrase in _SEVERE_NEGATIVE):
        return -1.0
    if any(_has_phrase(text, phrase) for phrase in _MILD_NEGATIVE):
        return -0.5
    if any(_has_phrase(text, phrase) for phrase in _STRONG_POSITIVE):
        return 0.5
    if _declares_dividend(text) or any(_has_phrase(text, phrase) for phrase in _MILD_POSITIVE):
        return 0.2

    polarity = TextBlob(headline or "").sentiment.polarity
    if any(_has_phrase(text, word) for word in _BOOST_WORDS):
        polarity += 0.1
    return max(min(polarity, 1.0), -1.0)


class SentimentEngine:
    def __init__(self):
        pass

    def analyze_headlines(self, ticker, headlines):
        """Analyzes a list of headlines and returns an aggregated sentiment report."""
        if not headlines or "No current news" in headlines[0]:
            return {"score": 0.0, "label": "neutral", "total": 0, "headline_scores": []}

        headline_scores = []
        total_polarity = 0.0
        for headline in headlines:
            polarity = headline_polarity(headline)
            total_polarity += polarity
            headline_scores.append((headline, round(polarity, 2)))

        avg_polarity = total_polarity / len(headlines)
        if avg_polarity > 0.05:
            label = "bullish"
        elif avg_polarity < -0.05:
            label = "bearish"
        else:
            label = "neutral"

        return {
            "score": round(avg_polarity, 4),
            "label": label,
            "total": len(headlines),
            "headline_scores": headline_scores,
        }
