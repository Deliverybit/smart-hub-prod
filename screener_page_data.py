"""Load screener results from Supabase snapshots with live-scan fallback."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from app_config import get_screener_symbol_limit
from screener_engine import format_scan_display, selection_from_payload
from screener_selection import ProximitySelection, select_proximity_results
from screener_snapshots import fetch_snapshot, snapshot_is_fresh


@dataclass(frozen=True)
class ScreenerPageLoad:
    all_results: list[dict]
    display_results: list[dict]
    selection: ProximitySelection
    last_updated: str
    scanned_count: int
    universe_size: int
    asset_noun: str
    from_snapshot: bool
    snapshot_stale: bool
    headlines_enriched: bool


def _display_last_updated(payload: dict) -> str:
    """Show the stored UTC completion time in Central time."""
    raw = payload.get("last_scan_completed_at") or payload.get("updated_at")
    if raw:
        try:
            moment = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            return format_scan_display(moment)
        except ValueError:
            pass
    return str(payload.get("last_updated_display") or "")


def load_screener_page_data(
    screener_key: str,
    *,
    universe_size: int,
    asset_noun: str,
    run_live: Callable[[], tuple[list[dict], str]],
) -> ScreenerPageLoad:
    """Return the latest snapshot when available; live-scan only if none exists."""
    payload = fetch_snapshot(screener_key)
    if payload:
        stale = not snapshot_is_fresh(payload)
        selection = selection_from_payload(payload)
        return ScreenerPageLoad(
            all_results=list(payload.get("all_results") or []),
            display_results=list(payload.get("display_results") or []),
            selection=selection,
            last_updated=_display_last_updated(payload),
            scanned_count=int(payload.get("scanned_count") or 0),
            universe_size=int(payload.get("universe_size") or universe_size),
            asset_noun=str(payload.get("asset_noun") or asset_noun),
            from_snapshot=True,
            snapshot_stale=stale,
            headlines_enriched=bool(payload.get("headlines_enriched")),
        )

    all_results, last_updated = run_live()
    selection = select_proximity_results(all_results)
    symbol_limit = get_screener_symbol_limit()
    return ScreenerPageLoad(
        all_results=all_results,
        display_results=selection.results,
        selection=selection,
        last_updated=last_updated,
        scanned_count=min(symbol_limit, universe_size),
        universe_size=universe_size,
        asset_noun=asset_noun,
        from_snapshot=False,
        snapshot_stale=False,
        headlines_enriched=False,
    )
