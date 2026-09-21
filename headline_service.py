"""Headline fetch + sentiment enrichment without Streamlit."""

from __future__ import annotations

from textblob import TextBlob

from market_data import MarketData


def headlines_from_news_items(news_items: list) -> tuple[list[str], list[str]]:
    headlines: list[str] = []
    urls: list[str] = []
    for item in news_items[:10]:
        title = item.get("title", "")
        url = item.get("url", "")
        if not title or (not url and title.startswith("No current news found")):
            continue
        headlines.append(title)
        urls.append(url)
    return headlines, urls


def polarity_from_headlines(headlines: list[str]) -> float:
    if not headlines:
        return 0.0
    return sum(TextBlob(headline).sentiment.polarity for headline in headlines) / len(headlines)


def fetch_news_items(ticker: str, *, fail_fast: bool = False) -> list[dict]:
    try:
        return MarketData().get_news_items(ticker, fail_fast=fail_fast)
    except Exception:
        return []


def enrich_result_row(row: dict) -> dict:
    """Return a copy of a screener row with headline fields populated."""
    enriched = dict(row)
    ticker = enriched.get("_source_ticker") or enriched.get("Ticker")
    if not ticker:
        return enriched

    news_items = fetch_news_items(ticker)
    headlines, urls = headlines_from_news_items(news_items)
    polarity = polarity_from_headlines(headlines)

    enriched["Headline Sentiment"] = round(polarity, 3)
    enriched["Headlines"] = len(headlines)
    enriched["_headline_texts"] = headlines[:10]
    enriched["_headline_urls"] = urls[:10]
    return enriched


def enrich_result_rows(rows: list[dict]) -> list[dict]:
    return [enrich_result_row(row) for row in rows]
