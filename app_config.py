import os
from pathlib import Path
import tomllib


def _load_local_streamlit_secret(name: str):
    """Read ignored local Streamlit secrets when not running inside Streamlit."""
    secrets_path = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
    try:
        with secrets_path.open("rb") as secrets_file:
            return tomllib.load(secrets_file).get(name)
    except (OSError, tomllib.TOMLDecodeError):
        return None


def _load_secret(name: str) -> str | None:
    """Load a secret from env, Streamlit secrets, or local secrets.toml."""
    value = os.getenv(name)
    if value:
        return str(value).strip() or None
    try:
        import streamlit as st

        raw = st.secrets.get(name)
        if raw is not None:
            return str(raw).strip() or None
    except Exception:
        pass
    raw = _load_local_streamlit_secret(name)
    if raw is not None:
        return str(raw).strip() or None
    return None


def get_app_env(default: str = "staging") -> str:
    """Deployment environment label: staging, production, or local."""
    raw = _load_secret("APP_ENV")
    env = (raw or default).strip().lower()
    return env if env in {"staging", "production", "local"} else default


def _normalize_database_url(url: str) -> str:
    """Strip whitespace and accidental quotes from copied connection strings."""
    cleaned = url.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1].strip()
    return cleaned


def get_database_url(required: bool = False) -> str | None:
    """
    Postgres connection string (Supabase).

    Prefer the Session pooler URI (port 5432) from Supabase:
    Project Settings → Database → Connection string → URI → Session mode.
    Append ``?sslmode=require`` if it is not already present.
    """
    url = _load_secret("DATABASE_URL")
    placeholders = {
        "",
        "replace-with-your-supabase-database-url",
        "postgresql://postgres:password@localhost:5432/postgres",
    }
    if url in placeholders:
        url = None
    if url:
        url = _normalize_database_url(url)
        if not url.startswith(("postgresql://", "postgres://")):
            raise RuntimeError(
                "DATABASE_URL must start with postgresql:// (Supabase Session pooler URI). "
                "Use the raw URI only — no surrounding quotes and no "
                "DATABASE_URL = prefix."
            )
    if required and not url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Set it in the environment, "
            ".streamlit/secrets.toml, or your host's secret store."
        )
    return url


def get_alpha_vantage_api_key(required: bool = False) -> str | None:
    """Load the Alpha Vantage API key from deployment secrets or local env."""
    key = _load_secret("ALPHA_VANTAGE_API_KEY")

    if key == "replace-with-your-alpha-vantage-key":
        key = None

    if required and not key:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY is not configured")

    return key


def get_screener_symbol_limit(default: int = 1000) -> int:
    """Limit Alpha Vantage screener calls; high default scans each full page universe."""
    raw_limit = _load_secret("SCREENER_SYMBOL_LIMIT")

    try:
        limit = int(raw_limit) if raw_limit is not None else default
    except (TypeError, ValueError):
        limit = default

    return max(1, limit)


# Bump when screener/API behavior changes to invalidate stale Streamlit caches.
SCREENER_CACHE_VERSION = 7

# Visible in the staging banner so Streamlit Cloud deploys are easy to verify.
APP_BUILD_ID = "2026-09-17-desktop-screener-pop"

# Back-compat aliases used by some page variants.
ALPHAVANTAGE_CACHE_TIMEOUT = 900


def get_selected_symbol_list(symbols, limit: int | None = None):
    """Return up to ``limit`` symbols from a screener universe."""
    max_symbols = limit if limit is not None else get_screener_symbol_limit()
    return list(symbols)[:max_symbols]
