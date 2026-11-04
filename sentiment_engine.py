import re

from textblob import TextBlob

# One match sets the headline. Checked before TextBlob so legal and
# market phrases are not scored as ordinary English.
_SEVERE_NEGATIVE = (
    "lawsuit",
    "class action",
    "lawsuits",
    "investor suit",
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
    "workers die",
    "fatality",
    "killed",
    "elder abuse",
    "fined",
    "fine of",
    "fine",
    "probe",
    "hack",
    "hacks",
    "depeg",
)

_MILD_NEGATIVE = (
    "shareholder alert",
    "deadline alert",
    "underperforms",
    "price target cut",
    "price target lowered",
    "lowers target",
    "cuts target",
    "guidance cut",
    "rated \"reduce\"",
    "reduce rating",
    "downgrade",
    "recall",
    "slump",
    "investigation",
    "investigations",
    "falls",
    "fall",
    "fallen",
    "crash",
    "drop",
    "drops",
    "decline",
    "declines",
    "sell-off",
    "downgrades",
    "strong sell",
    "misses",
    "miss",
    "miss estimates",
    "earnings miss",
    "growth miss",
    "52-week low",
    "insider selling",
    "insider sells",
    "sells shares",
    "moved down",
    "shares down",
    "costs rise",
    "slide",
    "slides",
    "plunges",
    "plunge",
    "tumbles",
    "tumble",
    "dipped",
    "edges lower",
    "target cuts",
    "pt lowered",
    "facility cuts",
    "losers",
    "pulls back",
    "share price weakness",
    "price weakness",
    "sinks",
    "suspend",
    # Downward financial-news cues (FinBERT / financial phrase style).
    "fell",
    "profit warning",
    "profit fell",
    "profits fell",
    "profit decreased",
    "operating loss",
    "sales fell",
    "sales declined",
    "net sales decreased",
    "lowered guidance",
    "cut guidance",
    "cuts guidance",
    "job cuts",
    "laid off",
    "layoffs",
    "weak demand",
    "fell short",
    "write-down",
    "writedown",
    "impairment",
    "discontinue",
    "warning signs",
    "lose signal",
    "contamination",
    "gambling ban",
    "hit from",
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
    "raised earnings guidance",
    "raises full-year guidance",
    "raised full-year guidance",
    "raised outlook",
    "raised revenue outlook",
    "raises outlook",
    "eps beat",
    "beats estimates",
    "revenue topped",
    "revenues increase",
    "revenue gain",
    "margin expands",
    "margins improving",
    "net income",
    "guidance reaffirmed",
    "fda approval",
    "met primary endpoint",
    "positive data",
    # Upward financial-news cues (FinBERT / financial phrase style).
    "profit rose",
    "profits rose",
    "profit increased",
    "profits increased",
    "earnings rose",
    "earnings increased",
    "sales rose",
    "sales increased",
    "net sales increased",
    "margin rose",
    "order intake",
    "orders rose",
    "guidance raise",
    "raised to buy",
    "upbeat",
)

_MILD_POSITIVE = (
    "buy rating",
    "maintains buy",
    "awarded",
    "rises",
    "gains",
    "jumps",
    "jump",
    "pumps",
    "rallies",
    "climbs",
    "closed up",
    "buyback",
    "buybacks",
    "buys back",
    "buy back",
    "repurchases",
    "shareholders approve",
    "shareholders back",
    "adding jobs",
    "purchases",
    "makes new investment",
    "rose",
    "signed an agreement",
    "cooperation agreement",
    "new contract",
    "contract worth",
    "won a contract",
    "joint venture",
    "partnership",
    "expansion",
    "to rise",
    "revenues rise",
    "shareholder return",
    "month high",
    "in grants",
)

_BOOST_WORDS = ("surge", "rally", "record", "breakout")


def _has_phrase(text: str, phrase: str) -> bool:
    if " " in phrase:
        return phrase in text
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def _declares_dividend(text: str) -> bool:
    return "dividend" in text and re.search(r"\bdeclar\w*\b", text) is not None


def _sells_shares(text: str) -> bool:
    return "shares" in text and re.search(r"\bsells\b", text) is not None


def _tops_estimates(text: str) -> bool:
    return re.search(r"\btops?\b", text) is not None and "estimate" in text


def _raises_outlook(text: str) -> bool:
    return "outlook" in text and re.search(r"\braises?\b|\braised\b", text) is not None


def _mentions_target(text: str) -> bool:
    return "target" in text and "stake" not in text


def _cuts_target(text: str) -> bool:
    return _mentions_target(text) and re.search(r"\bcuts?\b|\blowers?\b|\blowered\b", text) is not None


def _raises_target(text: str) -> bool:
    if _cuts_target(text) or not _mentions_target(text):
        return False
    return re.search(r"\braises?\b|\braised\b", text) is not None


def _raises_price_target(text: str) -> bool:
    """'to $525 from $518' is a raise even without the word raised."""
    if "price target" not in text or " from " not in text:
        return False
    amounts = [
        float(number.replace(",", ""))
        for number in re.findall(r"\$(\d[\d,]*(?:\.\d+)?)", text)
    ]
    return len(amounts) >= 2 and amounts[0] > amounts[1]


def _axes_jobs(text: str) -> bool:
    return "jobs" in text and re.search(r"\baxe[sd]?\b", text) is not None


def _how_low_can_it_go(text: str) -> bool:
    return "how low can" in text and " go" in text


def _rejects_merger(text: str) -> bool:
    return "reject" in text and "merger" in text


def _bullish_outlook(text: str) -> bool:
    return "outlook" in text and "bullish" in text


def _boosts_forecasts(text: str) -> bool:
    return "forecast" in text and "boost" in text


def _secures_funding(text: str) -> bool:
    return "funding" in text and re.search(r"\bsecur\w*\b", text) is not None


def _price_down_percent(text: str) -> bool:
    return re.search(r"\b(lost|down)\s+\d", text) is not None


def _lowers_price_target(text: str) -> bool:
    """'Adjusts price target to $330 from $368' is a cut even without the word cut."""
    if "price target" not in text or " from " not in text:
        return False
    amounts = [
        float(number.replace(",", ""))
        for number in re.findall(r"\$(\d[\d,]*(?:\.\d+)?)", text)
    ]
    return len(amounts) >= 2 and amounts[0] < amounts[1]


def _creates_jobs(text: str) -> bool:
    return "jobs" in text and re.search(r"\b(adding|create|creates|creating)\b", text) is not None


def _commercial_win(text: str) -> bool:
    """Contract, plant, or revenue-scale headlines that read as ordinary English."""
    if re.search(r"\b(decline|declines|loss|losses|lower|weak)\b", text):
        return False
    if re.search(r"\brevenues?\b", text) and re.search(r"\b(billion|million)\b", text):
        return True
    if re.search(r"\b(helping|helps)\b", text) and re.search(r"\bbuild\w*\b", text):
        return True
    return "world's largest" in text


def _comparison_question(text: str) -> bool:
    """Horse-race headlines. The word 'better' is not a rating change."""
    if "?" not in text:
        return False
    return " vs" in text or "which " in text or text.startswith("should you")


def headline_is_severe(headline: str) -> bool:
    """True when a headline should remove the name from the Top 10."""
    text = (headline or "").lower()
    return any(_has_phrase(text, phrase) for phrase in _SEVERE_NEGATIVE)


def headline_polarity(headline: str) -> float:
    """Score one headline from -1 to 1.

    Severe legal or fraud language wins outright. A target cut in the same
    headline as a buy rating stays negative. Ordinary wording still uses TextBlob.
    """
    text = (headline or "").lower().replace("\u2019", "'").replace("\u2018", "'")
    if any(_has_phrase(text, phrase) for phrase in _SEVERE_NEGATIVE):
        return -1.0
    if (
        any(_has_phrase(text, phrase) for phrase in _MILD_NEGATIVE)
        or _sells_shares(text)
        or _lowers_price_target(text)
        or _cuts_target(text)
        or _axes_jobs(text)
        or _price_down_percent(text)
        or _how_low_can_it_go(text)
        or _rejects_merger(text)
    ):
        return -0.5
    if (
        any(_has_phrase(text, phrase) for phrase in _STRONG_POSITIVE)
        or _raises_outlook(text)
        or _tops_estimates(text)
        or _raises_target(text)
        or _raises_price_target(text)
        or _boosts_forecasts(text)
    ):
        return 0.5
    if _declares_dividend(text) or _creates_jobs(text) or _commercial_win(text) or _bullish_outlook(text) or _secures_funding(text) or any(
        _has_phrase(text, phrase) for phrase in _MILD_POSITIVE
    ):
        return 0.2
    if _comparison_question(text):
        return 0.0

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
