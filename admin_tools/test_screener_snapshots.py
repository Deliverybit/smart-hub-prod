#!/usr/bin/env python3
"""Smoke tests for screener snapshot storage."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_database_url  # noqa: E402
from screener_engine import get_definition, refresh_screener  # noqa: E402
from screener_snapshots import fetch_snapshot, snapshot_is_fresh  # noqa: E402


def main() -> int:
    if not get_database_url():
        print("SKIP: DATABASE_URL not configured")
        return 0

    payload = refresh_screener(get_definition("NYSE"))
    assert payload["display_results"], "expected display_results"

    loaded = fetch_snapshot("NYSE")
    assert loaded is not None, "snapshot missing after save"
    assert snapshot_is_fresh(loaded), "snapshot should be fresh immediately after save"
    assert loaded["display_results"][0].get("_headline_texts") is not None

    print("screener snapshot smoke test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
