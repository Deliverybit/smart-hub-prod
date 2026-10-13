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
import os
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
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


def _publish_saved_pages(written: list[str]) -> None:
    """Commit the refreshed preview files and push them to production master."""
    if not written:
        return
    paths = [str(ROOT / "preview" / name) for name in written]
    assets = ROOT / "preview" / "analyze-assets.json"
    chart = ROOT / "preview" / "analyze-chart.js"
    for extra in (assets, chart):
        if extra.exists():
            paths.append(str(extra))
    subprocess.run(["git", "add", "--", *paths], cwd=ROOT, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if staged.returncode == 0:
        print("Saved pages match master. Nothing to push.", flush=True)
        return
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Scoop Snapshot",
            "-c",
            "user.email=snapshots@thescoop52.com",
            "commit",
            "-m",
            "Publish the latest screener snapshots.",
        ],
        cwd=ROOT,
        check=True,
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        remote = f"https://x-access-token:{token}@github.com/Deliverybit/smart-hub-prod.git"
        subprocess.run(["git", "push", remote, "HEAD:master"], cwd=ROOT, check=True)
    else:
        subprocess.run(["git", "push", "prod", "HEAD:master"], cwd=ROOT, check=True)
    print("Pushed saved pages to master.", flush=True)
    _purge_edge_cache()


def _purge_edge_cache() -> None:
    """Drop the published HTML from Cloudflare so the next visitor gets this snapshot."""
    zone_id = os.environ.get("CLOUDFLARE_ZONE_ID", "").strip()
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not zone_id or not api_token:
        print(
            "Edge cache was not purged. Set CLOUDFLARE_ZONE_ID and CLOUDFLARE_API_TOKEN.",
            flush=True,
        )
        return
    request = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
        data=b'{"purge_everything":true}',
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        print(f"Edge cache purge failed ({exc.code}).", flush=True)
        return
    except urllib.error.URLError:
        print("Edge cache purge failed (network).", flush=True)
        return
    if '"success": true' in body or '"success":true' in body:
        print("Purged the Cloudflare edge cache.", flush=True)
        return
    print("Edge cache purge was not accepted.", flush=True)


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
        if persist and payloads:
            import importlib
            import preview_tables

            importlib.reload(preview_tables)
            written = preview_tables.refresh_preview_from_payloads(payloads)
            print(
                "Saved pages updated: " + (", ".join(written) if written else "none"),
                flush=True,
            )
            try:
                _publish_saved_pages(written)
            except Exception:
                traceback.print_exc()
                print("Saved pages were not pushed.", flush=True)
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
