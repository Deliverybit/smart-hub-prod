from __future__ import annotations

import streamlit as st

from app_config import ALPHAVANTAGE_CACHE_TIMEOUT, SCREENER_CACHE_VERSION
from headline_service import (
    enrich_result_row,
    fetch_news_items,
    headlines_from_news_items,
    polarity_from_headlines,
)
from market_data import MarketData


def normalize_screener_ticker(ticker: str) -> str:
    """Normalize display/API tickers so BTC and BTC-USD share caches."""
    sym = str(ticker or "").strip().upper()
    if sym.endswith("-USD"):
        return sym
    if sym in MarketData._CRYPTO_SYMBOLS:
        return f"{sym}-USD"
    return sym


def _ticker_identity_variants(ticker: str) -> set[str]:
    """Normalized ticker aliases for matching screener rows to Analyze lookups."""
    sym = normalize_screener_ticker(ticker)
    bare = sym.replace("-USD", "")
    variants = {sym, bare, f"{bare}-USD"}
    alias = MarketData._CRYPTO_ID_ALIASES.get(bare)
    if alias:
        variants.add(alias)
        variants.add(f"{alias}-USD")
    return {v for v in variants if v}


def _ticker_matches_row(ticker: str, row: dict) -> bool:
    query = _ticker_identity_variants(ticker)
    row_variants: set[str] = set()
    for key in ("_source_ticker", "Ticker"):
        raw = str(row.get(key) or "").strip().upper()
        if raw:
            row_variants |= _ticker_identity_variants(raw)
    return bool(query & row_variants)


def news_items_from_snapshot(ticker: str, screener_key: str) -> list[dict] | None:
    """Return precomputed headline payloads from a screener snapshot when available."""
    if not screener_key:
        return None
    try:
        from screener_snapshots import fetch_snapshot

        payload = fetch_snapshot(screener_key)
    except Exception:
        return None
    if not payload or not payload.get("headlines_enriched"):
        return None

    rows = list(payload.get("display_results") or []) + list(payload.get("all_results") or [])
    seen_ids: set[int] = set()
    for row in rows:
        row_id = id(row)
        if row_id in seen_ids:
            continue
        seen_ids.add(row_id)
        if not _ticker_matches_row(ticker, row):
            continue
        texts = list(row.get("_headline_texts") or [])
        urls = list(row.get("_headline_urls") or [])
        if not texts:
            continue
        items = []
        for idx, title in enumerate(texts[:10]):
            url = urls[idx] if idx < len(urls) else ""
            items.append({"title": title, "url": url, "source": ""})
        return items
    return None


def snapshot_quote_for_ticker(ticker: str, screener_key: str | None = None) -> dict | None:
    """Return Price / 52W fields from a screener snapshot when available."""
    if not screener_key:
        return None
    try:
        from screener_snapshots import fetch_snapshot

        payload = fetch_snapshot(screener_key)
    except Exception:
        return None
    if not payload:
        return None
    rows = list(payload.get("display_results") or []) + list(payload.get("all_results") or [])
    for row in rows:
        if not _ticker_matches_row(ticker, row):
            continue
        price = row.get("Price")
        year_low = row.get("52W Low")
        year_high = row.get("52W High")
        if price is None or year_low is None or year_high is None:
            continue
        return {
            "Price": price,
            "52W Low": year_low,
            "52W High": year_high,
            "current_price": price,
            "year_low": year_low,
            "year_high": year_high,
        }
    return None


@st.cache_data(ttl=ALPHAVANTAGE_CACHE_TIMEOUT, show_spinner=False)
def _cached_news_items(
    ticker: str,
    screener_key: str | None = None,
    _cache_version: int = SCREENER_CACHE_VERSION,
) -> tuple[tuple[str, str, str], ...]:
    """Fetch and cache headline payloads per ticker (matches screener refresh cadence)."""
    sym = normalize_screener_ticker(ticker)
    snap_items = news_items_from_snapshot(sym, screener_key or "")
    if snap_items:
        return tuple(
            (item.get("title", ""), item.get("url", ""), item.get("source", "") or "")
            for item in snap_items[:10]
        )

    rows = []
    for item in fetch_news_items(sym, fail_fast=True)[:10]:
        rows.append((
            item.get("title", ""),
            item.get("url", ""),
            item.get("source", "") or item.get("source_domain", "") or "",
        ))
    return tuple(rows)


def get_cached_news_items(
    ticker: str,
    *,
    screener_key: str | None = None,
    cache_version: int = SCREENER_CACHE_VERSION,
) -> list[dict]:
    """Return headline dicts from snapshot, shared cache, or API."""
    sym = normalize_screener_ticker(ticker)
    cached_rows = _cached_news_items(sym, screener_key, _cache_version=cache_version)
    if not cached_rows:
        return [{"title": f"No current news found for {sym}", "url": "", "source": ""}]
    return [{"title": t, "url": u, "source": s} for t, u, s in cached_rows]


def enrich_headline_sentiment(
    df,
    _market_data,
    ticker_column: str = "_source_ticker",
    *,
    screener_key: str | None = None,
    cache_version: int = SCREENER_CACHE_VERSION,
):
    """Fetch headlines only for displayed screener rows and update sentiment fields."""

    if df.empty:
        return df

    enriched = df.copy()
    for idx, row in enriched.iterrows():
        if row.get("_headline_texts"):
            continue

        ticker = row.get(ticker_column) or row.get("Ticker")
        if not ticker:
            continue

        cached_rows = _cached_news_items(
            ticker,
            screener_key,
            _cache_version=cache_version,
        )
        news_items = [{"title": t, "url": u, "source": s} for t, u, s in cached_rows]
        headlines, urls = headlines_from_news_items(news_items)
        polarity = polarity_from_headlines(headlines)

        enriched.at[idx, "Headline Sentiment"] = round(polarity, 3)
        enriched.at[idx, "Headlines"] = len(headlines)
        enriched.at[idx, "_headline_texts"] = headlines
        enriched.at[idx, "_headline_urls"] = urls

    return enriched


def display_results_need_headlines(results: list[dict]) -> bool:
    """True when any displayed row is missing precomputed headline payloads."""
    for row in results:
        if not (row.get("_headline_texts") or []):
            return True
    return False
