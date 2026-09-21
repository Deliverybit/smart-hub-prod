"""Analyze payloads: worker prerun plus on-demand fill cached 15 minutes."""

# Streamlit must reload this module so ensure_analyze_bundle is visible.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from market_data import MarketData
from predictor import Predictor
from screener_headlines import (
    _ticker_identity_variants,
    _ticker_matches_row,
    normalize_screener_ticker,
)
from screener_snapshots import snapshot_is_fresh
from sentiment_engine import SentimentEngine


def _news_from_row(row: dict[str, Any]) -> list[dict[str, str]]:
    texts = list(row.get("_headline_texts") or [])
    urls = list(row.get("_headline_urls") or [])
    items = []
    for idx, title in enumerate(texts[:10]):
        if not title:
            continue
        url = urls[idx] if idx < len(urls) else ""
        items.append({"title": str(title), "url": str(url), "source": ""})
    if not items:
        return [{"title": "No current news found", "url": "", "source": ""}]
    return items


def _slice_history(history: list, days) -> list:
    try:
        chart_days = 730 if days == "max" else min(int(days), 730)
    except (TypeError, ValueError):
        chart_days = 365
    return list(history or [])[-chart_days:]


def build_analyze_bundles(
    display_results: list[dict[str, Any]],
    market_data: MarketData | None = None,
    *,
    sentiment_eng: SentimentEngine | None = None,
    predictor_eng: Predictor | None = None,
) -> dict[str, dict[str, Any]]:
    """2-year Analyze payloads for displayed Top 10 rows (worker-only AV)."""
    md = market_data or MarketData()
    sentiment_eng = sentiment_eng or SentimentEngine()
    predictor_eng = predictor_eng or Predictor()
    bundles: dict[str, dict[str, Any]] = {}

    for row in display_results:
        ticker = row.get("_source_ticker") or row.get("Ticker")
        if not ticker:
            continue
        sym = normalize_screener_ticker(str(ticker))
        if any(key in bundles for key in _ticker_identity_variants(sym)):
            continue
        snapshot = {
            "Price": row.get("Price"),
            "52W Low": row.get("52W Low"),
            "52W High": row.get("52W High"),
        }
        price = md.get_analyze_price_bundle(sym, 730, snapshot=snapshot, fail_fast=False)
        if not price:
            continue
        news_items = _news_from_row(row)
        headlines = [item["title"] for item in news_items]
        sent_result = sentiment_eng.analyze_headlines(sym, headlines)
        history = list(price.get("history") or [])
        latest_price = price.get("latest_price") or 0
        if len(history) >= 2:
            prev_price = history[-2]["price"]
            price_change_pct = (latest_price - prev_price) / prev_price if prev_price else 0
        else:
            price_change_pct = 0
        result = predictor_eng.predict(
            sym,
            headlines,
            market_data=md,
            latest_price=latest_price,
            price_change_pct=price_change_pct,
            sentiment_score=sent_result["score"],
        )
        bundle = _finalize_bundle(
            news_items,
            sent_result,
            result,
            history,
            latest_price,
            price,
        )
        for key in _ticker_identity_variants(sym):
            bundles[key] = bundle
    return bundles


def _finalize_bundle(news_items, sent_result, result, history, latest_price, price) -> dict[str, Any]:
    return {
        "news_items": news_items,
        "sent_result": sent_result,
        "result": result,
        "history": history,
        "latest_price": latest_price,
        "week52_low": price.get("week52_low"),
        "week52_high": price.get("week52_high"),
        "low_date": price.get("low_date"),
        "high_date": price.get("high_date"),
        "cached_at": datetime.now(timezone.utc).isoformat(),
    }


def _row_for_ticker(payload: dict[str, Any] | None, ticker: str) -> dict[str, Any] | None:
    if not payload:
        return None
    rows = list(payload.get("display_results") or []) + list(payload.get("all_results") or [])
    for row in rows:
        if _ticker_matches_row(ticker, row):
            return row
    return None


def _raw_bundle_from_payload(payload: dict[str, Any] | None, ticker: str) -> dict[str, Any] | None:
    if not payload:
        return None
    store = payload.get("analyze_bundles") or {}
    for key in _ticker_identity_variants(normalize_screener_ticker(ticker)):
        raw = store.get(key)
        if not raw:
            continue
        stamp = raw.get("cached_at") or payload.get("updated_at")
        if stamp and not snapshot_is_fresh({"updated_at": stamp}):
            return None
        return raw
    return None


def build_one_analyze_bundle(
    ticker: str,
    row: dict[str, Any] | None = None,
    market_data: MarketData | None = None,
    *,
    sentiment_eng: SentimentEngine | None = None,
    predictor_eng: Predictor | None = None,
    fail_fast: bool = True,
) -> dict[str, Any] | None:
    """Compute one Analyze payload and stamp it for the 15-minute snapshot cache."""
    md = market_data or MarketData()
    sentiment_eng = sentiment_eng or SentimentEngine()
    predictor_eng = predictor_eng or Predictor()
    row = row or {}
    sym = normalize_screener_ticker(ticker)
    snapshot = {
        "Price": row.get("Price"),
        "52W Low": row.get("52W Low"),
        "52W High": row.get("52W High"),
    }
    try:
        price = md.get_analyze_price_bundle(sym, 730, snapshot=snapshot, fail_fast=fail_fast)
    except TypeError:
        price = md.get_analyze_price_bundle(sym, 730)
    if not price:
        return None
    news_items = _news_from_row(row)
    headlines = [item["title"] for item in news_items]
    sent_result = sentiment_eng.analyze_headlines(sym, headlines)
    history = list(price.get("history") or [])
    latest_price = price.get("latest_price") or 0
    if len(history) >= 2:
        prev_price = history[-2]["price"]
        price_change_pct = (latest_price - prev_price) / prev_price if prev_price else 0
    else:
        price_change_pct = 0
    result = predictor_eng.predict(
        sym,
        headlines,
        market_data=md,
        latest_price=latest_price,
        price_change_pct=price_change_pct,
        sentiment_score=sent_result["score"],
    )
    return _finalize_bundle(news_items, sent_result, result, history, latest_price, price)


def persist_analyze_bundle(screener_key: str, ticker: str, bundle: dict[str, Any]) -> None:
    """Merge one ticker into the screener snapshot so the next user can reuse it."""
    from screener_snapshots import _fetch_snapshot_uncached, save_snapshot

    payload = _fetch_snapshot_uncached(screener_key) or {"screener_key": screener_key}
    store = dict(payload.get("analyze_bundles") or {})
    for key in _ticker_identity_variants(normalize_screener_ticker(ticker)):
        store[key] = bundle
    payload["analyze_bundles"] = store
    save_snapshot(screener_key, payload)


def ensure_analyze_bundle(
    ticker: str,
    screener_key: str | None,
    days,
    *,
    market_data: MarketData | None = None,
) -> dict[str, Any] | None:
    """Return a fresh-enough snapshot bundle, computing and storing on first miss."""
    payload = None
    if screener_key:
        try:
            from screener_snapshots import _fetch_snapshot_uncached

            payload = _fetch_snapshot_uncached(screener_key)
        except Exception:
            payload = None
        raw = _raw_bundle_from_payload(payload, ticker)
        if raw:
            return {**raw, "history": _slice_history(raw.get("history"), days)}

    row = _row_for_ticker(payload, ticker)
    computed = build_one_analyze_bundle(ticker, row, market_data)
    if not computed:
        return None
    if screener_key:
        try:
            persist_analyze_bundle(screener_key, ticker, computed)
        except Exception:
            pass
    return {**computed, "history": _slice_history(computed.get("history"), days)}


def analyze_bundle_from_payload(payload: dict[str, Any] | None, ticker: str, days) -> dict[str, Any] | None:
    raw = _raw_bundle_from_payload(payload, ticker)
    if not raw:
        return None
    return {**raw, "history": _slice_history(raw.get("history"), days)}


def analyze_bundle_from_snapshot(ticker: str, screener_key: str | None, days) -> dict[str, Any] | None:
    if not screener_key:
        return None
    try:
        from screener_snapshots import fetch_snapshot

        payload = fetch_snapshot(screener_key)
    except Exception:
        return None
    return analyze_bundle_from_payload(payload, ticker, days)
