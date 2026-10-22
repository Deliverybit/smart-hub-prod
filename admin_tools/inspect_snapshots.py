#!/usr/bin/env python3
"""Print screener snapshot status from Supabase."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_database_url  # noqa: E402
from screener_snapshots import fetch_snapshot, snapshot_age_seconds, snapshot_is_fresh  # noqa: E402


def main() -> int:
    database_url = get_database_url(required=True)
    import psycopg

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT screener_key, updated_at, payload
                FROM screener_snapshots
                ORDER BY screener_key
                """
            )
            rows = cur.fetchall()

    print(f"{'KEY':<8} {'UPDATED_AT':<28} {'ROWS':>4} {'FRESH':>5} {'AGE_MIN':>8} {'MODE':<14} HEADLINES")
    for key, updated_at, payload in rows:
        if isinstance(payload, str):
            payload = json.loads(payload)
        display = payload.get("display_results") or []
        age = snapshot_age_seconds(payload)
        age_min = f"{age / 60:.1f}" if age is not None else "?"
        print(
            f"{key:<8} {str(updated_at):<28} {len(display):>4} "
            f"{str(snapshot_is_fresh(payload)):>5} {age_min:>8} "
            f"{payload.get('selection_mode', '?'):<14} {payload.get('headlines_enriched')}"
        )

    expected = {"NYSE", "NASDAQ", "CRYPTO"}
    found = {row[0] for row in rows}
    missing = expected - found
    if missing:
        print(f"\nMISSING KEYS: {sorted(missing)}")

    for key in expected:
        loaded = fetch_snapshot(key)
        if loaded:
            symbols = [r.get("symbol") for r in (loaded.get("display_results") or [])[:3]]
            print(f"  {key} top symbols: {symbols}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
