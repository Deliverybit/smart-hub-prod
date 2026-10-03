"""Headline fetch + sentiment enrichment without Streamlit."""

from __future__ import annotations

import re

from textblob import TextBlob

from market_data import MarketData

_LEGAL_SUFFIX = re.compile(
    r",?\s+\b(inc|incorporated|corp|corporation|ltd|limited|llc|plc|co|company|etf|etn)\.?\b",
    re.IGNORECASE,
)


def _fold(text: str) -> str:
    cleaned = (text or "").replace("'", "").replace("’", "").replace(".", "")
    return re.sub(r"[^a-z0-9]+", " ", cleaned.lower()).strip()


def asset_mention_labels(ticker: str, company_name: str = "") -> list[str]:
    """Ticker symbols and cleaned company name that a headline must contain."""
    labels: list[str] = []
    raw = (ticker or "").strip().upper()
    for token in (raw, raw.replace("-USD", ""), raw.replace("=F", "")):
        token = token.strip()
        if len(token) >= 2 and token not in labels:
            labels.append(token)
    name = company_name or ""
    for inner in re.findall(r"\(([^)]+)\)", name):
        inner = inner.strip().upper()
        if len(inner) >= 2 and inner not in labels and " " not in inner:
            labels.append(inner)
    name = re.sub(r"\([^)]*\)", " ", name)
    name = _LEGAL_SUFFIX.sub("", name)
    name = re.sub(r"\s+", " ", name).strip(" .,-")
    if name.lower().startswith("the "):
        name = name[4:].strip()
    if len(_fold(name)) >= 3:
        labels.append(name)
    return labels


def title_mentions_asset(title: str, ticker: str, company_name: str = "") -> bool:
    folded = _fold(title)
    if not folded:
        return False
    padded = f" {folded} "
    for label in asset_mention_labels(ticker, company_name):
        needle = _fold(label)
        if len(needle) < 2:
            continue
        if f" {needle} " in padded:
            return True
    return False


def row_company_name(row: dict) -> str:
    for key in ("Company", "Commodity", "Name"):
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return ""


def headlines_from_news_items(
    news_items: list,
    *,
    ticker: str = "",
    company_name: str = "",
) -> tuple[list[str], list[str]]:
    matched: list[tuple[float, int, str, str]] = []
    require_mention = bool(ticker or company_name)
    for index, item in enumerate(news_items):
        title = item.get("title", "")
        url = item.get("url", "")
        if not title or (not url and str(title).startswith("No current news found")):
            continue
        if require_mention and not title_mentions_asset(title, ticker, company_name):
            continue
        try:
            relevance = float(item.get("relevance") or 0)
        except (TypeError, ValueError):
            relevance = 0.0
        matched.append((relevance, -index, title, url))
    matched.sort(reverse=True)
    headlines = [title for _relevance, _index, title, _url in matched[:10]]
    urls = [url for _relevance, _index, _title, url in matched[:10]]
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

    company_name = row_company_name(enriched)
    news_items = fetch_news_items(ticker)
    headlines, urls = headlines_from_news_items(
        news_items,
        ticker=str(ticker),
        company_name=company_name,
    )
    polarity = polarity_from_headlines(headlines)

    enriched["Headline Sentiment"] = round(polarity, 3)
    enriched["Headlines"] = len(headlines)
    enriched["_headline_texts"] = headlines[:10]
    enriched["_headline_urls"] = urls[:10]
    return enriched


def enrich_result_rows(rows: list[dict]) -> list[dict]:
    return [enrich_result_row(row) for row in rows]
