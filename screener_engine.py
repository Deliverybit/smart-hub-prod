"""Run screener scans outside Streamlit for the snapshot worker."""

from __future__ import annotations

import ast
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any, Callable

from app_config import get_screener_symbol_limit
from analyze_snapshot import build_analyze_bundles
from headline_service import enrich_result_row
from market_data import MarketData
from screener_selection import (
    INTERNAL_THRESHOLD_PCT,
    MAX_PAD_CAP_PCT,
    TARGET_COUNT,
    ProximitySelection,
    select_proximity_results,
)
from screener_snapshots import save_snapshot
from sentiment_engine import headline_is_severe

DISPLAY_TZ = ZoneInfo("America/Chicago")

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"


@dataclass(frozen=True)
class ScreenerDefinition:
    key: str
    page_name: str
    universe_expr: str
    deps: tuple[str, ...]
    kind: str
    label_field: str
    names_key: str
    asset_noun: str


SCREENER_DEFINITIONS: tuple[ScreenerDefinition, ...] = (
    ScreenerDefinition(
        "NYSE",
        "1_NYSE_Top_10.py",
        "list(COMPANY_NAMES.keys())",
        ("COMPANY_NAMES",),
        "stock",
        "Company",
        "COMPANY_NAMES",
        "stocks",
    ),
    ScreenerDefinition(
        "NASDAQ",
        "2_NASDAQ_Top_10.py",
        "list(COMPANY_NAMES.keys())",
        ("COMPANY_NAMES",),
        "stock",
        "Company",
        "COMPANY_NAMES",
        "stocks",
    ),
    ScreenerDefinition(
        "CRYPTO",
        "3_Crypto_Top_10.py",
        "list(CRYPTO_DATA.keys())",
        ("CRYPTO_DATA",),
        "crypto",
        "Name",
        "CRYPTO_NAMES",
        "cryptos",
    ),
    ScreenerDefinition(
        "LSE",
        "3b_LSE_Top_10.py",
        "list(COMPANY_NAMES.keys())",
        ("COMPANY_NAMES",),
        "stock",
        "Company",
        "COMPANY_NAMES",
        "stocks",
    ),
    ScreenerDefinition(
        "TSX",
        "3c_TSX_Top_10.py",
        "list(COMPANY_NAMES.keys())",
        ("COMPANY_NAMES",),
        "stock",
        "Company",
        "COMPANY_NAMES",
        "stocks",
    ),
)


def _literal_assignments(path: Path) -> dict[str, object]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    values: dict[str, object] = {}
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
    return values


def load_page_env(defn: ScreenerDefinition) -> dict[str, object]:
    path = PAGES / defn.page_name
    env = _literal_assignments(path)
    missing = [name for name in defn.deps if name not in env]
    if missing:
        raise RuntimeError(f"{path.name} missing constants: {', '.join(missing)}")

    if defn.kind == "crypto" and "CRYPTO_DATA" in env:
        crypto_data = env["CRYPTO_DATA"]
        if isinstance(crypto_data, dict):
            env.setdefault(
                "CRYPTO_NAMES",
                {key: value[0] for key, value in crypto_data.items()},
            )
            env.setdefault(
                "CRYPTO_EXCHANGES",
                {key: value[1] for key, value in crypto_data.items()},
            )
        env.setdefault("DISPLAY_TICKERS", {})

    safe_globals = {"list": list, "sorted": sorted, **env}
    universe = eval(defn.universe_expr, safe_globals, env)  # noqa: S307
    if not isinstance(universe, list):
        raise RuntimeError(f"{path.name} universe expression did not return a list")
    env["_universe"] = [str(item) for item in universe]
    return env


def _market_mood(pct_above_low: float) -> str:
    if pct_above_low < 0:
        return "BELOW LOW"
    if pct_above_low <= 2:
        return "AT LOW"
    return "NEAR LOW"


def screen_ticker(
    market_data: MarketData,
    ticker: str,
    *,
    defn: ScreenerDefinition,
    env: dict[str, object],
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    try:
        if snapshot is None:
            snapshot = market_data.get_market_snapshot(ticker)
        if not snapshot:
            return None

        current_price = snapshot["current_price"]
        year_low = snapshot["year_low"]
        year_high = snapshot["year_high"]
        if (
            current_price is None
            or year_low is None
            or year_high is None
            or (isinstance(year_low, float) and math.isnan(year_low))
            or (isinstance(year_high, float) and math.isnan(year_high))
            or (isinstance(current_price, float) and math.isnan(current_price))
            or year_low <= 0
        ):
            return None

        pct_above_low = ((current_price - year_low) / year_low) * 100

        names = env.get(defn.names_key) or {}
        if not isinstance(names, dict):
            names = {}
        if defn.kind == "stock":
            company = str(names.get(ticker) or "")
            if company and not market_data.symbol_matches_company(ticker, company):
                return None

        headlines: list[str] = []
        headline_links: list[str] = []
        polarity = 0.0

        if defn.kind == "crypto":
            display_tickers = env.get("DISPLAY_TICKERS") or {}
            exchanges = env.get("CRYPTO_EXCHANGES") or {}
            raw = ticker.replace("-USD", "")
            display_ticker = display_tickers.get(ticker, raw) if isinstance(display_tickers, dict) else raw
            return {
                "Ticker": display_ticker,
                "_source_ticker": ticker,
                defn.label_field: names.get(ticker, display_ticker),
                "Exchanges": exchanges.get(ticker, "—") if isinstance(exchanges, dict) else "—",
                "Price": current_price,
                "52W Low": year_low,
                "52W High": year_high,
                "% Above Low": round(pct_above_low, 2),
                "Headline Sentiment": round(polarity, 3),
                "Headlines": len(headlines),
                "Market Mood": _market_mood(pct_above_low),
                "_headline_texts": headlines,
                "_headline_urls": headline_links,
            }

        if defn.kind == "commodity":
            display_ticker = ticker.replace("=F", "")
            return {
                "Ticker": display_ticker,
                "_source_ticker": ticker,
                defn.label_field: names.get(ticker, display_ticker),
                "Price": current_price,
                "52W Low": year_low,
                "52W High": year_high,
                "% Above Low": round(pct_above_low, 2),
                "Headline Sentiment": round(polarity, 3),
                "Headlines": len(headlines),
                "Market Mood": _market_mood(pct_above_low),
                "_headline_texts": headlines,
                "_headline_urls": headline_links,
            }

        shown = ticker.split(".", 1)[0] if "." in ticker else ticker
        return {
            "Ticker": shown,
            "_source_ticker": ticker,
            defn.label_field: names.get(ticker, ticker),
            "Price": current_price,
            "52W Low": year_low,
            "52W High": year_high,
            "% Above Low": round(pct_above_low, 2),
            "Headline Sentiment": round(polarity, 3),
            "Headlines": len(headlines),
            "_headline_texts": headlines,
            "_headline_urls": headline_links,
            "Market Mood": _market_mood(pct_above_low),
        }
    except Exception:
        return None


def run_screener_scan(
    defn: ScreenerDefinition,
    market_data: MarketData | None = None,
) -> tuple[list[dict[str, Any]], int, int]:
    env = load_page_env(defn)
    universe: list[str] = env["_universe"]
    symbol_limit = get_screener_symbol_limit()
    scan_universe = universe[:symbol_limit]
    md = market_data or MarketData()

    results: list[dict[str, Any]] = []
    total = len(scan_universe)
    print(f"Scanning {defn.key}: {total} names", flush=True)
    for index, ticker in enumerate(scan_universe, start=1):
        print(f"{defn.key} {index}/{total} {ticker}", flush=True)
        row = screen_ticker(
            md,
            ticker,
            defn=defn,
            env=env,
        )
        if row is not None:
            results.append(row)
    return results, len(scan_universe), len(universe)


def format_scan_display(moment: datetime | None = None) -> str:
    """Format a scan time in Central time, matching the clock visitors use."""
    if moment is None:
        moment = datetime.now(timezone.utc)
    elif moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    local = moment.astimezone(DISPLAY_TZ)
    return local.strftime("%b %d, %Y  %I:%M %p CT")


def _proximity_order(all_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Names within 30% of the low, strict 15% group first, then the rest."""

    def pct(row: dict[str, Any]) -> float:
        return float(row["% Above Low"])

    eligible = [row for row in all_results if pct(row) <= MAX_PAD_CAP_PCT]
    strict = sorted((row for row in eligible if pct(row) <= INTERNAL_THRESHOLD_PCT), key=pct)
    strict_tickers = {row.get("Ticker") for row in strict}
    padded = sorted(
        (row for row in eligible if row.get("Ticker") not in strict_tickers),
        key=pct,
    )
    return strict + padded


def select_display_results(
    all_results: list[dict[str, Any]],
    *,
    target: int = TARGET_COUNT,
) -> tuple[list[dict[str, Any]], ProximitySelection]:
    """Pick the nearest names whose headlines do not hit a severe phrase.

    Headlines are fetched in proximity order. A severe match drops that name
    and the next name fills the slot. Names with no headlines stay eligible.
    """
    kept: list[dict[str, Any]] = []
    for row in _proximity_order(all_results):
        enriched = enrich_result_row(row)
        texts = list(enriched.get("_headline_texts") or [])
        if any(headline_is_severe(text) for text in texts):
            print(
                f"Excluded {enriched.get('Ticker')} for a severe headline",
                flush=True,
            )
            continue
        kept.append(enriched)
        if len(kept) >= target:
            break
    return kept, select_proximity_results(kept)


def build_snapshot_payload(
    defn: ScreenerDefinition,
    market_data: MarketData | None = None,
) -> dict[str, Any]:
    all_results, scanned_count, universe_size = run_screener_scan(defn, market_data=market_data)
    display_results, selection = select_display_results(all_results)
    try:
        analyze_bundles = build_analyze_bundles(display_results, market_data)
    except Exception as exc:
        print(f"[ERROR] {defn.key} analyze bundles: {exc}", file=sys.stderr)
        analyze_bundles = {}
    updated = datetime.now(timezone.utc)
    payload = {
        "screener_key": defn.key,
        "updated_at": updated.isoformat(),
        "last_updated_display": format_scan_display(updated),
        "all_results": all_results,
        "display_results": display_results,
        "analyze_bundles": analyze_bundles,
        "selection_mode": selection.mode,
        "strict_count": selection.strict_count,
        "padded_count": selection.padded_count,
        "eligible_count": selection.eligible_count,
        "scanned_count": scanned_count,
        "universe_size": universe_size,
        "asset_noun": defn.asset_noun,
        "headlines_enriched": True,
    }
    if defn.key in {"LSE", "TSX"}:
        from price_display import stamp_usd_prices, usd_per_unit

        code = "GBP" if defn.key == "LSE" else "CAD"
        stamp_usd_prices(payload, usd_per_unit(code))
    return payload


def refresh_screener(defn: ScreenerDefinition, *, persist: bool = True) -> dict[str, Any]:
    payload = build_snapshot_payload(defn)
    if persist:
        save_snapshot(defn.key, payload)
    return payload


def apply_last_scan_time(
    payloads: list[dict[str, Any]],
    *,
    persist: bool = True,
) -> str:
    """Stamp every completed screener with the time the full scan finished."""
    completed = datetime.now(timezone.utc)
    display = format_scan_display(completed)
    completed_iso = completed.isoformat()
    for payload in payloads:
        payload["updated_at"] = completed_iso
        payload["last_updated_display"] = display
        payload["last_scan_completed_at"] = completed_iso
        if persist:
            save_snapshot(str(payload["screener_key"]), payload)
    return display


def refresh_all_screeners(*, persist: bool = True) -> list[dict[str, Any]]:
    market_data = MarketData()
    payloads: list[dict[str, Any]] = []
    for defn in SCREENER_DEFINITIONS:
        try:
            payload = build_snapshot_payload(defn, market_data=market_data)
        except Exception as exc:
            print(f"[ERROR] {defn.key}: {exc}", file=sys.stderr)
            continue
        if persist:
            save_snapshot(defn.key, payload)
        payloads.append(payload)
    if payloads:
        apply_last_scan_time(payloads, persist=persist)
    return payloads


def get_definition(screener_key: str) -> ScreenerDefinition:
    for defn in SCREENER_DEFINITIONS:
        if defn.key == screener_key:
            return defn
    raise KeyError(screener_key)


def selection_from_payload(payload: dict[str, Any]) -> ProximitySelection:
    return ProximitySelection(
        results=list(payload.get("display_results") or []),
        mode=str(payload.get("selection_mode") or "empty"),
        strict_count=int(payload.get("strict_count") or 0),
        padded_count=int(payload.get("padded_count") or 0),
        eligible_count=int(payload.get("eligible_count") or 0),
    )
