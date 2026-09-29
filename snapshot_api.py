#!/usr/bin/env python3
"""Read-only screener snapshot API.

Routes:
    GET /screeners/{key}
    GET /health

Usage:
    python snapshot_api.py
"""

from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from screener_engine import SCREENER_DEFINITIONS
from screener_selection import _FULL_RESULTS_COLUMN_ORDER
from screener_snapshots import snapshot_age_seconds, snapshot_max_age_seconds

DISPLAY_ROW_LIMIT = 10
DISPLAY_ROW_FIELDS = (
    *_FULL_RESULTS_COLUMN_ORDER,
    "_headline_texts",
    "_headline_urls",
    "_source_ticker",
)
DISPLAY_META_FIELDS = (
    "screener_key",
    "updated_at",
    "last_updated_display",
    "asset_noun",
    "scanned_count",
    "universe_size",
    "selection_mode",
    "strict_count",
    "padded_count",
    "eligible_count",
    "headlines_enriched",
)

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))
POOL_MAX = 5
SCREENER_KEYS = {defn.key for defn in SCREENER_DEFINITIONS}
_pool = None
_pool_lock = threading.Lock()


def display_snapshot(payload: dict) -> dict:
    """Keep the fields required to render the top 10 table rows."""
    rows = []
    for row in list(payload.get("display_results") or [])[:DISPLAY_ROW_LIMIT]:
        item = {key: row.get(key) for key in DISPLAY_ROW_FIELDS if key in row}
        if "_headline_texts" in item:
            item["_headline_texts"] = list(item["_headline_texts"] or [])[:DISPLAY_ROW_LIMIT]
        if "_headline_urls" in item:
            item["_headline_urls"] = list(item["_headline_urls"] or [])[:DISPLAY_ROW_LIMIT]
        rows.append(item)
    body = {key: payload.get(key) for key in DISPLAY_META_FIELDS}
    body["display_results"] = rows
    return body


def get_pool():
    """Reuse up to POOL_MAX Postgres connections for this process."""
    global _pool
    if _pool is not None:
        return _pool
    with _pool_lock:
        if _pool is None:
            from app_config import get_database_url
            from psycopg_pool import ConnectionPool

            _pool = ConnectionPool(
                conninfo=get_database_url(required=True),
                min_size=1,
                max_size=POOL_MAX,
                timeout=5,
                open=True,
            )
        return _pool


def fetch_display_snapshot(screener_key: str) -> dict | None:
    """Load snapshot fields for the top-10 table, skipping scan and analyze blobs."""
    meta_object = ", ".join(
        f"'{key}', payload->'{key}'" for key in DISPLAY_META_FIELDS
    )
    query = f"""
        SELECT jsonb_build_object(
            {meta_object},
            'display_results', COALESCE((
                SELECT jsonb_agg(elem ORDER BY ord)
                FROM (
                    SELECT elem, ord
                    FROM jsonb_array_elements(
                        COALESCE(payload->'display_results', '[]'::jsonb)
                    ) WITH ORDINALITY AS rows(elem, ord)
                    ORDER BY ord
                    LIMIT {DISPLAY_ROW_LIMIT}
                ) limited
            ), '[]'::jsonb)
        )
        FROM screener_snapshots
        WHERE screener_key = %s
    """

    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (screener_key,))
            row = cur.fetchone()
    if not row or row[0] is None:
        return None
    payload = row[0]
    if isinstance(payload, str):
        payload = json.loads(payload)
    return payload if isinstance(payload, dict) else None


def screener_payload(screener_key: str) -> tuple[int, dict]:
    """Return the 10 display rows for one screener. Unknown or missing keys are 404."""
    if screener_key not in SCREENER_KEYS:
        return 404, {"error": "unknown screener"}
    payload = fetch_display_snapshot(screener_key)
    if payload is None:
        return 404, {"error": "snapshot not found", "screener_key": screener_key}
    return 200, display_snapshot(payload)


def health_payload() -> tuple[int, dict]:
    """200 only when every screener snapshot exists and is fresh."""
    missing: list[str] = []
    stale: list[str] = []
    max_age = snapshot_max_age_seconds()
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT screener_key, updated_at
                FROM screener_snapshots
                WHERE screener_key = ANY(%s)
                """,
                (sorted(SCREENER_KEYS),),
            )
            found = {key: updated for key, updated in cur.fetchall()}
    for key in sorted(SCREENER_KEYS):
        updated = found.get(key)
        if updated is None:
            missing.append(key)
            continue
        age = snapshot_age_seconds({"updated_at": updated.isoformat()})
        if age is None or age > max_age:
            stale.append(key)
    if missing or stale:
        return 503, {"ok": False, "missing": missing, "stale": stale}
    return 200, {"ok": True, "screeners": sorted(SCREENER_KEYS)}


class SnapshotHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path == "/health":
            status, body = health_payload()
            cache_control = "no-store"
        elif path.startswith("/screeners/"):
            key = path.removeprefix("/screeners/").strip()
            if not key or "/" in key:
                status, body = 404, {"error": "unknown screener"}
                cache_control = "no-store"
            else:
                status, body = screener_payload(key)
                cache_control = "public, max-age=60" if status == 200 else "no-store"
        else:
            status, body = 404, {"error": "not found"}
            cache_control = "no-store"
        self._send_json(status, body, cache_control)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[snapshot-api] {self.address_string()} {fmt % args}")

    def _send_json(self, status: int, body: dict, cache_control: str) -> None:
        raw = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", cache_control)
        self.send_header("X-Snapshot-Pool", str(POOL_MAX))
        self.end_headers()
        self.wfile.write(raw)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), SnapshotHandler)
    print(f"Snapshot API on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
