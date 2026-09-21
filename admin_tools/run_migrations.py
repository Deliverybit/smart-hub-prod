#!/usr/bin/env python3
"""
Apply SQL migrations to Postgres (Supabase smart-hub-prod).

Usage (from repo root):
    set DATABASE_URL=postgresql://postgres.[ref]:[password]@...supabase.com:5432/postgres?sslmode=require
    python admin_tools/run_migrations.py

Or put DATABASE_URL in .streamlit/secrets.toml and run without env vars.
"""

from __future__ import annotations

import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_config import get_app_env, get_database_url  # noqa: E402

MIGRATIONS_DIR = ROOT / "migrations"


def _assert_prod_target(database_url: str) -> None:
    if get_app_env() != "production":
        raise RuntimeError(
            "Refusing --require-prod: set APP_ENV=production in the environment."
        )


def main() -> int:
    require_prod = "--require-prod" in sys.argv
    database_url = get_database_url(required=True)
    if require_prod:
        _assert_prod_target(database_url)
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not files:
        print("No migration files found.", file=sys.stderr)
        return 1

    print(f"Connecting to Postgres ({len(files)} migration files)...")
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            for path in files:
                cur.execute(
                    "SELECT 1 FROM schema_migrations WHERE filename = %s",
                    (path.name,),
                )
                if cur.fetchone():
                    print(f"  skip  {path.name} (already applied)")
                    continue

                sql = path.read_text(encoding="utf-8")
                print(f"  apply {path.name}...")
                cur.execute(sql)
                cur.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)",
                    (path.name,),
                )
        conn.commit()

    print("Migrations complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
