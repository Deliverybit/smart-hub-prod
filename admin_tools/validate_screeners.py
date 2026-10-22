#!/usr/bin/env python3
"""
Validate NYSE, NASDAQ, and Crypto universes against Alpha Vantage market data.

Usage (from repo root):
    python admin_tools/validate_screeners.py
    python admin_tools/validate_screeners.py --quick   # first 25 symbols per screener
    python admin_tools/validate_screeners.py --json
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_screener_symbol_limit  # noqa: E402
from market_data import MarketData  # noqa: E402

PAGES = ROOT / "pages"

SCREENER_PAGES = [
    {
        "name": "NYSE",
        "path": PAGES / "1_NYSE_Top_10.py",
        "universe_expr": "list(COMPANY_NAMES.keys())",
        "deps": ("COMPANY_NAMES",),
    },
    {
        "name": "NASDAQ",
        "path": PAGES / "2_NASDAQ_Top_10.py",
        "universe_expr": "list(COMPANY_NAMES.keys())",
        "deps": ("COMPANY_NAMES",),
    },
    {
        "name": "Crypto",
        "path": PAGES / "3_Crypto_Top_10.py",
        "universe_expr": "list(CRYPTO_DATA.keys())",
        "deps": ("CRYPTO_DATA",),
    },
]


def _literal_assignments(path: Path) -> dict[str, object]:
    """Load module-level literal assignments (dicts, ints, sets) from a page file."""
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


def load_universe(page: Path, universe_expr: str, deps: tuple[str, ...]) -> list[str]:
    env = _literal_assignments(page)
    missing = [name for name in deps if name not in env]
    if missing:
        raise RuntimeError(f"{page.name} missing constants: {', '.join(missing)}")
    safe_builtins = {"list": list, "sorted": sorted}
    safe_globals = {**safe_builtins, **env}
    universe = eval(universe_expr, safe_globals, env)  # noqa: S307
    if not isinstance(universe, list):
        raise RuntimeError(f"{page.name} universe expression did not return a list")
    return [str(item) for item in universe]


def screen_ticker(market_data: MarketData, ticker: str) -> dict | None:
    snapshot = market_data.get_market_snapshot(ticker)
    if not snapshot:
        return None

    current_price = snapshot["current_price"]
    year_low = snapshot["year_low"]
    year_high = snapshot["year_high"]
    if not current_price or not year_low or year_low <= 0:
        return None

    pct_above_low = ((current_price - year_low) / year_low) * 100
    return {
        "ticker": ticker,
        "price": current_price,
        "year_low": year_low,
        "year_high": year_high,
        "pct_above_low": round(pct_above_low, 2),
    }


def validate_screener(
    market_data: MarketData,
    *,
    name: str,
    universe: list[str],
    symbol_limit: int,
    quick: bool,
) -> dict:
    scan_universe = universe[:symbol_limit]
    if quick:
        scan_universe = scan_universe[:25]

    started = time.perf_counter()
    results: list[dict] = []
    failures = 0

    for ticker in scan_universe:
        try:
            row = screen_ticker(market_data, ticker)
        except Exception:
            failures += 1
            continue
        if row:
            results.append(row)
        else:
            failures += 1

    results.sort(key=lambda row: row["pct_above_low"])
    top10 = results[:10]
    elapsed = time.perf_counter() - started
    timestamp = datetime.now().strftime("%b %d, %Y  %I:%M %p")

    passed = len(top10) >= 1
    status = "PASS" if passed else "FAIL"

    return {
        "name": name,
        "status": status,
        "universe_size": len(universe),
        "scanned": len(scan_universe),
        "candidates": len(results),
        "top10_count": len(top10),
        "top10_tickers": [row["ticker"] for row in top10],
        "failures": failures,
        "last_updated": timestamp,
        "elapsed_sec": round(elapsed, 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all screener pages.")
    parser.add_argument("--quick", action="store_true", help="Scan only first 25 symbols per page")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    symbol_limit = get_screener_symbol_limit()
    market_data = MarketData()
    reports = []

    for screener in SCREENER_PAGES:
        universe = load_universe(screener["path"], screener["universe_expr"], screener["deps"])
        report = validate_screener(
            market_data,
            name=screener["name"],
            universe=universe,
            symbol_limit=symbol_limit,
            quick=args.quick,
        )
        reports.append(report)

    if args.json:
        print(json.dumps(reports, indent=2))
    else:
        print(f"Screener validation — {datetime.now().isoformat(timespec='seconds')}")
        print(f"SCREENER_SYMBOL_LIMIT={symbol_limit}  mode={'quick' if args.quick else 'full'}")
        print("-" * 72)
        for report in reports:
            print(f"[{report['status']}] {report['name']}")
            print(f"  Universe: {report['universe_size']}  Scanned: {report['scanned']}")
            print(f"  Candidates: {report['candidates']}  Top 10: {report['top10_count']}")
            print(f"  Last updated: {report['last_updated']}")
            print(f"  Top tickers: {', '.join(report['top10_tickers']) or '(none)'}")
            print(f"  Elapsed: {report['elapsed_sec']}s  Failures/skips: {report['failures']}")
            print()

        passed = sum(1 for report in reports if report["status"] == "PASS")
        print(f"Summary: {passed}/{len(reports)} screeners passed")

    return 0 if all(report["status"] == "PASS" for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
