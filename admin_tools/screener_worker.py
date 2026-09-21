#!/usr/bin/env python3
"""
Precompute all screener snapshots and store them in Supabase.

Usage (from repo root):
    python admin_tools/screener_worker.py
    python admin_tools/screener_worker.py --screener NYSE
    python admin_tools/screener_worker.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
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
    args = parser.parse_args()

    persist = not args.dry_run
    if args.screener:
        defn = get_definition(args.screener)
        payload = refresh_screener(defn, persist=persist)
        payloads = [payload]
    else:
        payloads = refresh_all_screeners(persist=persist)

    for payload in payloads:
        display_count = len(payload.get("display_results") or [])
        all_count = len(payload.get("all_results") or [])
        analyze_count = len(payload.get("analyze_bundles") or {})
        print(
            f"[{'DRY-RUN' if args.dry_run else 'SAVED'}] "
            f"{payload['screener_key']}: {display_count} displayed / {all_count} scanned "
            f"analyze={analyze_count} "
            f"mode={payload.get('selection_mode')} "
            f"updated={payload.get('last_updated_display')}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
