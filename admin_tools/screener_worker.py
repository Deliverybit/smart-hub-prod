#!/usr/bin/env python3
"""
Precompute all screener snapshots and store them in Supabase.

Usage (from repo root):
    python admin_tools/screener_worker.py
    python admin_tools/screener_worker.py --loop
    python admin_tools/screener_worker.py --screener NYSE
    python admin_tools/screener_worker.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from screener_engine import (  # noqa: E402
    SCREENER_DEFINITIONS,
    get_definition,
    refresh_all_screeners,
    refresh_screener,
)


def _print_payloads(payloads: list[dict], *, dry_run: bool) -> None:
    for payload in payloads:
        display_count = len(payload.get("display_results") or [])
        all_count = len(payload.get("all_results") or [])
        analyze_count = len(payload.get("analyze_bundles") or {})
        print(
            f"[{'DRY-RUN' if dry_run else 'SAVED'}] "
            f"{payload['screener_key']}: {display_count} displayed / {all_count} scanned "
            f"analyze={analyze_count} "
            f"mode={payload.get('selection_mode')} "
            f"updated={payload.get('last_updated_display')}"
        )


def run_once(*, screener: str | None, persist: bool) -> list[dict]:
    if screener:
        defn = get_definition(screener)
        return [refresh_screener(defn, persist=persist)]
    return refresh_all_screeners(persist=persist)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh precomputed screener snapshots.")
    parser.add_argument(
        "--screener",
        choices=[defn.key for defn in SCREENER_DEFINITIONS],
        help="Refresh one screener instead of all.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build payloads without writing to Postgres.",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run full scans back to back. The next scan starts when the current one finishes.",
    )
    args = parser.parse_args()
    if args.loop and args.screener:
        print("ERROR: --loop refreshes every screener. Omit --screener.", file=sys.stderr)
        return 2

    persist = not args.dry_run
    while True:
        try:
            payloads = run_once(screener=args.screener, persist=persist)
        except Exception:
            traceback.print_exc()
            if not args.loop:
                return 1
            print("Full scan failed. Retrying in 30 seconds.", flush=True)
            time.sleep(30)
            continue

        _print_payloads(payloads, dry_run=args.dry_run)
        if not payloads:
            print("Full scan finished with no screener saved.", flush=True)
            if not args.loop:
                return 1
            print("Retrying in 30 seconds.", flush=True)
            time.sleep(30)
            continue
        print(
            f"Full scan finished. Last scan time: {payloads[0].get('last_updated_display')}",
            flush=True,
        )
        if not args.loop:
            return 0
        print("Starting the next full scan.", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
